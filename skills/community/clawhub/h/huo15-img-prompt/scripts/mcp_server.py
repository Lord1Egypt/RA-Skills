#!/usr/bin/env python3
"""
huo15-img-prompt — MCP stdio server v2.6

让 Claude Code / Cursor / Cline / Continue.dev 等支持 MCP 的 IDE 直接调用本技能。

启动方式：python3 mcp_server.py（stdio 模式）

注册到 Claude Code：~/.claude/mcp.json
{
  "mcpServers": {
    "huo15-img-prompt": {
      "command": "python3",
      "args": ["/path/to/huo15-img-prompt/scripts/mcp_server.py"]
    }
  }
}

注册到 Cursor / Continue.dev：参考各 IDE MCP 配置文档。

实现协议：MCP 2024-11-05（JSON-RPC 2.0 over stdio），手写零依赖。
支持 method：initialize / tools/list / tools/call。
"""

import sys
import os
import json
import re
import traceback
from typing import Dict, List, Optional, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt, parse_mix_preset, resolve_preset,
    parse_requirement, STYLE_PRESETS,
    list_presets as _list_presets,
    preset_example_urls,
    compact_prompt,
)
from character import char_load, char_list, char_save

VERSION = "3.1.0"
SERVER_INFO = {"name": "huo15-img-prompt", "version": VERSION}
PROTOCOL_VERSION = "2024-11-05"


# ─────────────────────────────────────────────────────────
# Tools 定义
# ─────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "enhance_prompt",
        "description": "把一句话主体描述增强成专业 T2I 提示词。返回 positive/negative + camera/lighting/palette 五锁 + seed。支持 88 风格预设 + 混合（'A+B' 语法）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "主体描述（中文/英文均可）"},
                "preset": {"type": "string", "description": "风格预设。88 个可选，支持 'A+B' 混合，例：'赛博朋克' / '原神+敦煌壁画'"},
                "model": {"type": "string", "enum": ["Midjourney", "SD", "SDXL", "DALL-E", "Flux", "通用"], "default": "通用"},
                "aspect": {"type": "string", "description": "画幅 1:1/3:4/16:9/21:9/9:16，不给走预设默认", "default": ""},
                "tier": {"type": "string", "enum": ["basic", "pro", "master"], "default": "pro"},
                "mix_ratio": {"type": "number", "default": 0.6, "description": "混合预设主权重 0.1-0.9"},
                "compact": {"type": "boolean", "default": False, "description": "压缩到 CLIP 77 token 内"},
                "seed": {"type": "integer", "description": "种子，不给则按 subject+preset 哈希"},
            },
            "required": ["subject"],
        },
    },
    {
        "name": "list_presets",
        "description": "列出全部 88 风格预设，按 9 大类分组（摄影/动漫/插画/3D/设计/艺术/场景/游戏/东方）。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "preset_examples",
        "description": "查看一个预设的 5 平台参考图链接（Lexica/Civitai/Pinterest/Google/Unsplash）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {"type": "string", "description": "预设名（中文或英文别名）"},
            },
            "required": ["preset"],
        },
    },
    {
        "name": "suggest_presets",
        "description": "Claude 智能推荐 top-3 预设（描述模糊时用，例如『温柔感』『高级感』）。需要 ANTHROPIC_API_KEY。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "用户描述"},
            },
            "required": ["description"],
        },
    },
    {
        "name": "polish_prompt",
        "description": "Claude API 智能润色：把粗糙描述转专业摄影/绘画术语。需要 ANTHROPIC_API_KEY。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "原始描述"},
            },
            "required": ["subject"],
        },
    },
    {
        "name": "safety_lint",
        "description": "平台合规检查 + 艺术化重写。仅服务合法艺术创作；CSAM/真人色情/武器制造等红线直接拒答。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "platform": {"type": "string", "enum": ["DALL-E", "MJ", "SD", "SDXL", "Flux", "通用"], "default": "MJ"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "review_image",
        "description": "Claude Vision 五维评审一张图（subject_match/composition/lighting/palette/technical 各 0-10），输出可执行修复指令。需要 ANTHROPIC_API_KEY。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image": {"type": "string", "description": "图片本地路径或 URL"},
                "prompt": {"type": "string", "description": "原始 prompt（评审参考）", "default": ""},
                "quick": {"type": "boolean", "default": False, "description": "简评模式（只 overall_score）"},
            },
            "required": ["image"],
        },
    },
    {
        "name": "list_characters",
        "description": "列出已存的角色卡（~/.huo15/characters/）。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "load_character",
        "description": "加载角色卡：返回 subject_description + seed + preset 等锁定参数，下游可直接复用保持角色一致性。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        },
    },
]


# ─────────────────────────────────────────────────────────
# Tool 实现（dispatch 到具体函数）
# ─────────────────────────────────────────────────────────
def tool_enhance_prompt(args: Dict) -> Dict:
    subject = args["subject"]
    raw_preset = args.get("preset") or "写实摄影"
    primary, secondary = parse_mix_preset(raw_preset)
    if secondary:
        p1, p2 = resolve_preset(primary), resolve_preset(secondary)
        if not p1 or not p2:
            raise ValueError(f"未知预设: {primary} 或 {secondary}")
        preset, mix_secondary = p1, p2
    else:
        preset = resolve_preset(primary) or "写实摄影"
        mix_secondary = None

    model = args.get("model", "通用")
    aspect = args.get("aspect") or STYLE_PRESETS[preset].get("aspect", "1:1")
    tier = args.get("tier", "pro")
    mix_ratio = args.get("mix_ratio", 0.6)

    result = build_prompt(
        subject, preset, model, aspect,
        seed=args.get("seed"), quality_tier=tier,
        mix_secondary=mix_secondary, mix_ratio=mix_ratio,
    )

    if args.get("compact"):
        compacted, meta = compact_prompt(result["positive"])
        result["positive_original"] = result["positive"]
        result["positive"] = compacted
        result["compaction"] = meta

    return result


def tool_list_presets(args: Dict) -> Dict:
    by_cat: Dict[str, List[str]] = {}
    for name, data in STYLE_PRESETS.items():
        by_cat.setdefault(data["category"], []).append(name)
    return {"total": len(STYLE_PRESETS), "by_category": by_cat}


def tool_preset_examples(args: Dict) -> Dict:
    preset = args["preset"]
    resolved = resolve_preset(preset) or preset
    if resolved not in STYLE_PRESETS:
        raise ValueError(f"未知预设: {preset}")
    return {
        "preset": resolved,
        "category": STYLE_PRESETS[resolved]["category"],
        "tags": STYLE_PRESETS[resolved]["tags"],
        "default_aspect": STYLE_PRESETS[resolved].get("aspect"),
        "search_urls": preset_example_urls(resolved),
    }


def tool_suggest_presets(args: Dict) -> Dict:
    from claude_polish import suggest_presets
    return suggest_presets(args["description"])


def tool_polish_prompt(args: Dict) -> Dict:
    from claude_polish import call_claude, parse_claude_json
    resp = call_claude(args["subject"])
    return parse_claude_json(resp)


def tool_safety_lint(args: Dict) -> Dict:
    from safety_lint import lint
    return lint(args["text"], platform=args.get("platform", "MJ"))


def tool_review_image(args: Dict) -> Dict:
    from image_review import review_image
    return review_image(args["image"], prompt=args.get("prompt", ""), quick=args.get("quick", False))


def tool_list_characters(args: Dict) -> Dict:
    return {"characters": char_list()}


def tool_load_character(args: Dict) -> Dict:
    card = char_load(args["name"])
    if not card:
        raise ValueError(f"角色卡不存在: {args['name']}")
    return card


TOOL_DISPATCH = {
    "enhance_prompt": tool_enhance_prompt,
    "list_presets": tool_list_presets,
    "preset_examples": tool_preset_examples,
    "suggest_presets": tool_suggest_presets,
    "polish_prompt": tool_polish_prompt,
    "safety_lint": tool_safety_lint,
    "review_image": tool_review_image,
    "list_characters": tool_list_characters,
    "load_character": tool_load_character,
}


# ─────────────────────────────────────────────────────────
# JSON-RPC 协议
# ─────────────────────────────────────────────────────────
def make_response(req_id: Any, result: Any = None, error: Optional[Dict] = None) -> Dict:
    resp = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        resp["error"] = error
    else:
        resp["result"] = result
    return resp


def handle_request(req: Dict) -> Optional[Dict]:
    """处理一个 JSON-RPC 请求。返回响应或 None（通知不回复）。"""
    method = req.get("method")
    req_id = req.get("id")
    params = req.get("params") or {}

    # 通知（无 id）不回复
    if req_id is None:
        return None

    try:
        if method == "initialize":
            return make_response(req_id, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            })

        elif method == "tools/list":
            return make_response(req_id, {"tools": TOOLS})

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments") or {}
            if tool_name not in TOOL_DISPATCH:
                return make_response(req_id, error={
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}",
                })
            try:
                result = TOOL_DISPATCH[tool_name](tool_args)
            except Exception as e:
                return make_response(req_id, result={
                    "content": [{"type": "text", "text": f"Error: {e}\n{traceback.format_exc()}"}],
                    "isError": True,
                })
            # MCP tools/call 标准返回格式
            return make_response(req_id, {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
            })

        elif method in ("ping",):
            return make_response(req_id, {})

        else:
            return make_response(req_id, error={
                "code": -32601,
                "message": f"Method not found: {method}",
            })

    except Exception as e:
        return make_response(req_id, error={
            "code": -32603,
            "message": f"Internal error: {e}",
            "data": {"traceback": traceback.format_exc()},
        })


def serve_stdio():
    """主循环：从 stdin 读 JSON-RPC，写到 stdout（按 LSP framing 或裸 JSON 行）。"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 支持 batch（数组）
            if isinstance(req, list):
                resps = [handle_request(r) for r in req]
                resps = [r for r in resps if r is not None]
                if resps:
                    sys.stdout.write(json.dumps(resps, ensure_ascii=False) + "\n")
                    sys.stdout.flush()
            else:
                resp = handle_request(req)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                    sys.stdout.flush()

        except KeyboardInterrupt:
            break
        except Exception as e:
            # 写错误到 stderr，不影响协议流
            sys.stderr.write(f"[mcp_server] error: {e}\n")
            sys.stderr.flush()


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
        print(f"mcp_server.py v{VERSION}")
        return
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    serve_stdio()


if __name__ == "__main__":
    main()
