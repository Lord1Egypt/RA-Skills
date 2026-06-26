#!/usr/bin/env python3
"""
OpenCode Zen 免费模型基准测试脚本
测试每个免费模型的响应时间、tokens/s 和质量
调用地址: https://opencode.ai/zen/v1 (无需 API Key)
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime


# ─── 配置 ────────────────────────────────────────────────────────────────────

BASE_URL = "https://opencode.ai/zen/v1"
TIMEOUT = 60  # 单次请求超时秒数

# 测试 Prompt（用于评估响应速度与质量）
TEST_PROMPT = "Please count from 1 to 20, listing each number on a separate line."

# ─── 模型清单获取（集成，不依赖外部 skill）─────────────────────────────────

DOC_URL = "https://opencode.ai/docs/zh-cn/zen"

# 已知免费模型定义（名称、ID、端点类型）
# endpoint_type: "chat" = /chat/completions, "responses" = /responses
_KNOWN_MODELS = [
    ("Big Pickle",          "big-pickle",           "chat"),
    ("MiniMax M2.5 Free",   "minimax-m2.5-free",    "chat"),
    ("MiMo V2 Pro Free",    "mimo-v2-pro-free",     "chat"),
    ("MiMo V2 Omni Free",   "mimo-v2-omni-free",    "chat"),
    ("Nemotron 3 Super",    "nemotron-3-super-free", "chat"),
    ("GPT 5 Nano",          "gpt-5-nano",           "responses"),
]


def fetch_free_models() -> list:
    """
    从 OpenCode 官方文档实时爬取免费模型列表，自动过滤已下架模型。
    返回格式: [(display_name, model_id, endpoint_type), ...]
    """
    try:
        req = urllib.request.Request(
            DOC_URL,
            headers={"User-Agent": "opencode-benchmark/1.1"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # 过滤：只保留文档中仍存在的模型
        active = [
            (name, mid, ep)
            for name, mid, ep in _KNOWN_MODELS
            if mid in html
        ]
        
        if active:
            print(f"  📋 从官方文档获取到 {len(active)} 个免费模型（在线）")
            return active
        else:
            print("  ⚠️ 文档中未找到可用模型，使用已知列表")
            return _KNOWN_MODELS

    except Exception as e:
        print(f"  ⚠️ 在线获取失败 ({e})，使用已知模型列表")
        return _KNOWN_MODELS


MODELS = fetch_free_models()


# ─── 辅助函数 ──────────────────────────────────────────────────────────────────

def call_chat_completions(model_id: str) -> dict:
    """调用 /chat/completions 端点，返回测试结果"""
    url = f"{BASE_URL}/chat/completions"
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": TEST_PROMPT}],
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "opencode-benchmark/1.0",
        },
        method="POST",
    )

    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        t1 = time.monotonic()
        body = json.loads(resp.read().decode("utf-8"))

    elapsed = t1 - t0
    usage = body.get("usage", {})
    completion_tokens = usage.get("completion_tokens", 0)
    prompt_tokens = usage.get("prompt_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    content = ""
    choices = body.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "")

    tps = completion_tokens / elapsed if elapsed > 0 and completion_tokens > 0 else None

    return {
        "elapsed_s": round(elapsed, 3),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "tps": round(tps, 2) if tps else None,
        "content_preview": content[:120].replace("\n", "\\n"),
        "error": None,
    }


def call_responses_api(model_id: str) -> dict:
    """调用 /responses 端点，返回测试结果"""
    url = f"{BASE_URL}/responses"
    payload = json.dumps({
        "model": model_id,
        "input": TEST_PROMPT,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "opencode-benchmark/1.0",
        },
        method="POST",
    )

    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        t1 = time.monotonic()
        body = json.loads(resp.read().decode("utf-8"))

    elapsed = t1 - t0
    usage = body.get("usage", {})
    completion_tokens = usage.get("output_tokens", usage.get("completion_tokens", 0))
    prompt_tokens = usage.get("input_tokens", usage.get("prompt_tokens", 0))
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

    # 提取 output 文本
    content = ""
    output = body.get("output", [])
    if output:
        for item in output:
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") == "output_text":
                        content = c.get("text", "")
                        break

    tps = completion_tokens / elapsed if elapsed > 0 and completion_tokens > 0 else None

    return {
        "elapsed_s": round(elapsed, 3),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "tps": round(tps, 2) if tps else None,
        "content_preview": content[:120].replace("\n", "\\n"),
        "error": None,
    }


def benchmark_model(display_name: str, model_id: str, endpoint_type: str) -> dict:
    """对单个模型执行基准测试，返回结果字典"""
    print(f"  🔄 测试中: {display_name} ({model_id}) ...", flush=True)
    try:
        if endpoint_type == "responses":
            result = call_responses_api(model_id)
        else:
            result = call_chat_completions(model_id)

        tps_str = f"{result['tps']:.2f}" if result["tps"] else "N/A"
        print(f"     ✅ {result['elapsed_s']}s | {result['completion_tokens']} tokens | {tps_str} tok/s")
        return result
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        msg = f"HTTP {e.code}: {e.reason} | {body}"
        print(f"     ❌ {msg}")
        return {"error": msg, "elapsed_s": None, "prompt_tokens": 0,
                "completion_tokens": 0, "total_tokens": 0, "tps": None, "content_preview": ""}
    except Exception as e:
        msg = str(e)[:200]
        print(f"     ❌ {msg}")
        return {"error": msg, "elapsed_s": None, "prompt_tokens": 0,
                "completion_tokens": 0, "total_tokens": 0, "tps": None, "content_preview": ""}


# ─── 报告生成 ──────────────────────────────────────────────────────────────────

def build_report(results: list) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# OpenCode Zen 免费模型基准测试报告")
    lines.append("")
    lines.append(f"**测试时间**: {now}")
    lines.append(f"**调用地址**: {BASE_URL}")
    lines.append(f"**测试 Prompt**: `{TEST_PROMPT}`")
    lines.append(f"**超时设置**: {TIMEOUT}s")
    lines.append("")

    # 汇总表
    lines.append("## 测试结果汇总")
    lines.append("")
    lines.append("| 排名 | 模型名称 | 模型 ID | 响应时间(s) | 生成tokens | tokens/s | 状态 |")
    lines.append("|:---:|:--------|:--------|:-----------:|:----------:|:--------:|:----:|")

    # 按 tokens/s 排序（成功的排前，失败的排后）
    success = [(r, d) for r, d in results if not d["error"]]
    failed  = [(r, d) for r, d in results if d["error"]]
    success.sort(key=lambda x: x[1]["tps"] if x[1]["tps"] else 0, reverse=True)
    sorted_results = success + failed

    for rank, (row, data) in enumerate(sorted_results, 1):
        name, model_id, _ = row
        if data["error"]:
            lines.append(f"| {rank} | {name} | `{model_id}` | - | - | - | ❌ 失败 |")
        else:
            tps_str = f"{data['tps']:.2f}" if data["tps"] else "N/A"
            lines.append(
                f"| {rank} | {name} | `{model_id}` | "
                f"{data['elapsed_s']} | {data['completion_tokens']} | "
                f"{tps_str} | ✅ 成功 |"
            )

    lines.append("")

    # 详细结果表格
    lines.append("## 详细结果")
    lines.append("")
    lines.append("| 模型名称 | 模型 ID | 响应时间(s) | Prompt Tokens | 生成 Tokens | 总 Tokens | tokens/s | 输出预览 | 状态 |")
    lines.append("|:--------|:--------|:-----------:|:-------------:|:-----------:|:--------:|:--------:|:--------:|:----:|")

    for row, data in results:
        name, model_id, endpoint_type = row
        endpoint_str = "`/chat/completions`" if endpoint_type == "chat" else "`/responses`"
        preview = data["content_preview"][:50] + "..." if len(data["content_preview"]) > 50 else data["content_preview"]
        if data["error"]:
            lines.append(f"| {name} | `{model_id}` | - | - | - | - | - | - | ❌ 失败 |")
        else:
            tps_str = f"{data['tps']:.2f}" if data["tps"] else "N/A"
            lines.append(
                f"| {name} | `{model_id}` | {data['elapsed_s']} | "
                f"{data['prompt_tokens']} | {data['completion_tokens']} | "
                f"{data['total_tokens']} | {tps_str} | `{preview}` | ✅ 成功 |"
            )

    lines.append("")
    lines.append("> **端点说明**: `/chat/completions` 用于标准聊天模型，`/responses` 用于 OpenAI Responses API 兼容模型。")
    lines.append("")

    # 统计分析
    lines.append("## 统计分析")
    lines.append("")
    success_count = len(success)
    fail_count = len(failed)
    lines.append(f"- **测试模型数**: {len(results)}")
    lines.append(f"- **成功**: {success_count}  |  **失败**: {fail_count}")

    if success:
        best = success[0]
        best_name, best_id, _ = best[0]
        tps_vals = [d["tps"] for _, d in success if d["tps"]]
        avg_tps = sum(tps_vals) / len(tps_vals) if tps_vals else None
        avg_rt = sum(d["elapsed_s"] for _, d in success) / success_count

        lines.append(f"- **最快模型**: {best_name} (`{best_id}`) — {best[1]['tps']:.2f} tok/s")
        if avg_tps:
            lines.append(f"- **平均生成速度**: {avg_tps:.2f} tok/s")
        lines.append(f"- **平均响应时间**: {avg_rt:.3f} 秒")

    lines.append("")
    lines.append("---")
    lines.append("> 报告由 opencode-model-benchmark skill 自动生成")

    return "\n".join(lines)


# ─── 主程序 ────────────────────────────────────────────────────────────────────

def main():
    # output_path 不再需要，保留参数兼容性但不使用
    print("=" * 60)
    print("  OpenCode Zen 免费模型基准测试")
    print(f"  模型数量: {len(MODELS)}")
    print(f"  测试端点: {BASE_URL}")
    print("=" * 60)
    print()

    results = []
    for model in MODELS:
        name, model_id, endpoint_type = model
        data = benchmark_model(name, model_id, endpoint_type)
        results.append((model, data))
        time.sleep(1)  # 避免频率限制

    print()
    print("📊 生成测试报告 ...")
    report = build_report(results)

    # 直接输出报告到 stdout（不写文件）
    print()
    print(report)

    # 终端快速汇总（保留，作为辅助信息）
    success = [(r, d) for r, d in results if not d["error"]]
    print()
    print("─" * 50)
    print("  快速汇总 (按 tok/s 排序)")
    print("─" * 50)
    success.sort(key=lambda x: x[1]["tps"] if x[1]["tps"] else 0, reverse=True)
    for i, (row, data) in enumerate(success, 1):
        name, model_id, _ = row
        tps = f"{data['tps']:.2f}" if data["tps"] else "N/A"
        print(f"  {i}. {name} (`{model_id}`): {tps} tok/s | {data['elapsed_s']}s")
    if len(success) < len(results):
        failed = [(r, d) for r, d in results if d["error"]]
        for row, data in failed:
            name, model_id, _ = row
            print(f"  ✗  {name} (`{model_id}`): 失败")
    print("─" * 50)


if __name__ == "__main__":
    main()
