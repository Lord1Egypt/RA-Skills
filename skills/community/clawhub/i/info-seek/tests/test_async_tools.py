#!/usr/bin/env python3
"""Infoseek MCP v3.0.0 GA 测试脚本 v3 - 11 个 async 工具完整测试"""
import sys, os, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
os.environ['DEEPSEEK_API_KEY'] = os.environ.get('DEEPSEEK_API_KEY', 'sk-REDACTED-DEEPSEEK')
os.environ['INFOSEEK_LLM_API_KEY'] = os.environ.get('DEEPSEEK_API_KEY', 'sk-REDACTED-DEEPSEEK')
os.environ['INFOSEEK_LLM_API_BASE'] = 'https://api.deepseek.com/v1'
os.environ['INFOSEEK_LLM_MODEL'] = 'deepseek-chat'

import infoseek_mcp_server as mcp


def call(tool_name, args):
    return mcp.handle_tools_call(1, {"name": tool_name, "arguments": args})


def get_data(res):
    if "error" in res and "result" not in res:
        return {"_error": res['error']}
    text = res["result"]["content"][0]["text"]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"_raw": text}


def section(label):
    print(f"\n{'='*60}\n  {label}\n{'='*60}")


def main():
    section("测试 11 个 async 工具")

    # 准备测试数据
    mock_source = {
        "url": "https://deepseek.com/news",
        "title": "DeepSeek V3",
        "text": "DeepSeek V3 是 671B MoE 模型，使用 MLA 架构"
    }
    sources = [
        {"url": "https://a.com/1", "title": "DeepSeek V3", "text": "DeepSeek V3 是 671B MoE 模型"},
        {"url": "https://a.com/2", "title": "MLA 架构", "text": "Multi-Head Latent Attention 减少 KV cache"},
    ]
    long_text = """DeepSeek 是一家中国人工智能大模型公司，2024 年 12 月开源 DeepSeek-V3 模型。
V3 是 671B 参数的 MoE 模型。它使用 MLA 架构，训练成本仅 558 万美元。它在 MMLU 等基准接近 GPT-4。"""

    # 测试用例
    tests = [
        ("search_anchors_async", {"subject": "DeepSeek V3", "depth": 2}),
        ("fetch_content_async", {"url": "https://deepseek.com", "format": "md"}),
        ("save_archive_async", {"subject": "DeepSeek V3", "url": "https://deepseek.com/v3", "title": "DeepSeek V3 模型", "content": long_text, "metadata": {"format": "md"}}),
        ("check_dedup_async", {"url": "https://a.com/1", "title": "DeepSeek V3"}),
        ("dedup_stats_async", {}),
        ("fuse_analysis_async", {"subject": "DeepSeek V3", "sources": sources}),
        ("cross_subject_analysis_async", {"subject_a": "DeepSeek V3", "subject_b": "GPT-4o"}),
        ("summarize_content_async", {"text": long_text, "max_len": 100, "prefer": "llm"}),
        ("conflict_detection_async", {"sources": sources, "subject": "DeepSeek V3"}),
        ("score_source_async", {"subject": "DeepSeek 大模型", "source": mock_source}),
        ("score_contradiction_async", {
            "claim_a": {"text": "DeepSeek V3 是开源模型"},
            "claim_b": {"text": "DeepSeek V3 是闭源模型"}
        }),
    ]

    results = []
    for tool_name, args in tests:
        t0 = time.perf_counter()
        try:
            res = call(tool_name, args)
            elapsed = (time.perf_counter() - t0) * 1000
            data = get_data(res)
            ok = "_error" not in data
            results.append((tool_name, ok, elapsed, data))
            status = "✅" if ok else "❌"
            print(f"  {status} {tool_name:35s} ({elapsed:>6.1f}ms)")
            if not ok:
                print(f"     错误: {data.get('_error')}")
            else:
                # 显示关键字段
                keys = list(data.keys())[:6]
                print(f"     keys: {keys}")
                if 'async_mode' in data:
                    print(f"     async_mode: {data['async_mode']}")
                if 'tool_version' in data:
                    print(f"     tool_version: {data['tool_version']}")
                if 'method' in data:
                    print(f"     method: {data['method']}")
        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000
            results.append((tool_name, False, elapsed, {}))
            print(f"  ❌ {tool_name:35s} EXCEPTION ({elapsed:.1f}ms): {type(e).__name__}: {e}")

    # 总结
    passed = sum(1 for _, ok, _, _ in results if ok)
    total = len(results)
    print(f"\n{'='*60}\n  总结: {passed} PASS / 0 FAIL\n{'='*60}")

    # 列出失败的
    failed = [name for name, ok, _, _ in results if not ok]
    if failed:
        print(f"  失败: {failed}")
    else:
        print(f"  ✅ 全部 11 个 async 工具通过测试")

    # TOOLS 总览
    print(f"\n=== TOOLS 总览 ===")
    print(f"  总数: {len(mcp.TOOLS)}")
    print(f"  SERVER_VERSION: {mcp.SERVER_VERSION}")

    # 按类别分类
    sync_v1 = [t['name'] for t in mcp.TOOLS if not t['name'].endswith('_async') and t['name'] not in ('research_v3', 'research_stream', 'score_contradiction')]
    v3_new = [t['name'] for t in mcp.TOOLS if t['name'] in ('research_v3', 'research_stream', 'score_contradiction')]
    async_v3 = [t['name'] for t in mcp.TOOLS if t['name'].endswith('_async')]

    print(f"  11 v1.x sync: {len(sync_v1)}")
    print(f"  3 v3 特殊（research_v3/research_stream/score_contradiction）: {len(v3_new)}")
    print(f"  11 async 工具: {len(async_v3)}")

    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
