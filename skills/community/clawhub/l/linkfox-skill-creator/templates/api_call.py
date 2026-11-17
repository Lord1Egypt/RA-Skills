#!/usr/bin/env python3
"""
linkfox 工具调用执行器（上下文保护）

作用：
    在不把大段原始数据灌进宿主 skill LLM 上下文的前提下，
    执行某个 linkfox-* 工具 skill 底层的 Python 脚本，并把
    返回的 JSON 结果直接落盘到指定文件。

    典型场景：宿主 skill 需要从 Jiimore / Keepa / SellerSprite /
    ABA 等平台拉一批结构化数据，再交给后续步骤（脚本 or LLM）
    局部处理。直接嵌套调用子 skill 会把整份响应作为上下文回
    注宿主 LLM，条数稍多就撑爆。api_call.py 让数据只在磁盘上
    流转，宿主只看一行摘要。

用法：
    python api_call.py <TARGET_SCRIPT> <OUTPUT_JSON> <PARAMS_JSON>

参数：
    TARGET_SCRIPT  被调用的 linkfox 工具 py 脚本路径（可用 ~ 展开）
                   例：~/.claude/skills/linkfox-jiimore-niche-by-keyword/\
                        scripts/jiimore_get_niche_info_by_keyword.py
    OUTPUT_JSON    结果落盘路径（父目录不存在会自动创建）
                   例：./data/step1c_jiimore_niche.json
    PARAMS_JSON    透传给目标脚本的 JSON 参数字符串
                   例：'{"keyword":"yoga mat","countryCode":"US","pageSize":10}'

stdout 行为：
    只打印一行 JSON 摘要（status / output 路径 / 字节数 / 形状），
    不打印原始数据。宿主 LLM 据此知道成功与否、到哪里读数据。

退出码：
    0  成功落盘
    2  用法错误 / 目标脚本不存在 / 参数非合法 JSON
    其它  目标脚本自身的 returncode（错误详情已落盘 + 打印摘要到 stdout）
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def summarize(obj):
    """给一个对象生成紧凑形状描述，不泄漏明细。"""
    if isinstance(obj, dict):
        keys = list(obj.keys())
        return {"type": "object", "top_keys": keys[:10], "key_count": len(keys)}
    if isinstance(obj, list):
        shape = {"type": "array", "length": len(obj)}
        if obj and isinstance(obj[0], dict):
            shape["first_item_keys"] = list(obj[0].keys())[:10]
        return shape
    return {"type": type(obj).__name__}


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: api_call.py <TARGET_SCRIPT> <OUTPUT_JSON> <PARAMS_JSON>",
            file=sys.stderr,
        )
        sys.exit(2)

    target_arg, output_arg, params_arg = sys.argv[1], sys.argv[2], sys.argv[3]

    target = Path(os.path.expanduser(target_arg)).resolve()
    if not target.is_file():
        print(f"Target script not found: {target}", file=sys.stderr)
        sys.exit(2)

    try:
        json.loads(params_arg)
    except json.JSONDecodeError as e:
        print(f"PARAMS_JSON is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)

    out = Path(output_arg).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        [sys.executable, str(target), params_arg],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if proc.returncode != 0:
        err_payload = {
            "error": "target script failed",
            "returncode": proc.returncode,
            "stderr": (proc.stderr or "").strip(),
            "stdout_head": (proc.stdout or "")[:500],
        }
        out.write_text(
            json.dumps(err_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(
            {"status": "error", "output": str(out), **err_payload},
            ensure_ascii=False,
        ))
        sys.exit(proc.returncode)

    raw = (proc.stdout or "").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        out.write_text(raw, encoding="utf-8")
        print(json.dumps({
            "status": "non_json_output",
            "output": str(out),
            "bytes": len(raw),
            "parse_error": str(e),
        }, ensure_ascii=False))
        return

    out.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "ok",
        "output": str(out),
        "bytes": out.stat().st_size,
        "shape": summarize(data),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
