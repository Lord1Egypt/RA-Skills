#!/usr/bin/env python3
"""
run-evals.py — performance-mastery Eval Runner
加载 evals/ 目录下的 YAML 测试用例，向 LLM 发送 prompt，
检查输出中是否包含 expected_keywords 和 expected_not，输出评分报告。

用法:
  # 基本用法（需要设置 OPENAI_API_KEY 或 OPENAI_BASE_URL）
  python3 scripts/run-evals.py

  # 指定模型和 API
  python3 scripts/run-evals.py --model gpt-4o --base-url https://api.openai.com/v1

  # 只运行特定文件
  python3 scripts/run-evals.py --file evals/linux-system.yaml

  # 干跑模式（不调用 LLM，仅验证 YAML 格式）
  python3 scripts/run-evals.py --dry-run

  # 自定义通过阈值（默认 50%）
  python3 scripts/run-evals.py --threshold 0.6

评分标准:
  - 每个用例的 expected_keywords 命中率 >= threshold（默认 50%）视为 PASS
  - 如果 expected_not 中任意关键词出现在回答中，该用例标记为 WARN（不影响通过）
  - 最终报告显示总通过率和各文件的详细结果

依赖:
  pip install pyyaml openai
"""
import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_eval_files(eval_dir, specific_file=None):
    """加载 evals/ 目录下所有 YAML 文件或指定文件"""
    if specific_file:
        files = [specific_file]
    else:
        files = sorted(glob.glob(os.path.join(eval_dir, "*.yaml")))

    all_suites = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        tests = data.get("tests", data) if isinstance(data, dict) else data
        if isinstance(tests, list):
            all_suites.append({"file": os.path.basename(f), "tests": tests})
        else:
            print(f"  WARN  Skipping {f}: no 'tests' list found")
    return all_suites


def call_llm(prompt, model, base_url, api_key, system_prompt=None):
    """调用 OpenAI 兼容 API"""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package is required. Install with: pip install openai")
        sys.exit(1)

    client = OpenAI(base_url=base_url, api_key=api_key)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return resp.choices[0].message.content


def check_keywords(response, expected_keywords):
    """检查回答中命中了多少 expected_keywords（大小写不敏感）"""
    response_lower = response.lower()
    hits = []
    misses = []
    for kw in expected_keywords:
        if kw.lower() in response_lower:
            hits.append(kw)
        else:
            misses.append(kw)
    return hits, misses


def check_not_keywords(response, expected_not):
    """检查回答中是否包含不应出现的关键词"""
    if not expected_not:
        return []
    response_lower = response.lower()
    violations = []
    for kw in expected_not:
        if kw.lower() in response_lower:
            violations.append(kw)
    return violations


def run_eval(suite, model, base_url, api_key, threshold, dry_run=False):
    """运行一个 eval 文件中的所有测试用例"""
    results = []
    system_prompt = (
        "你是一位资深的 Linux 系统性能工程师和全栈性能优化专家。"
        "请用中文回答，给出具体的工具命令和参数。"
    )

    for test_case in suite["tests"]:
        name = test_case.get("name", "unnamed")
        input_prompt = test_case.get("input", "")
        expected_kw = test_case.get("expected_keywords", [])
        expected_not = test_case.get("expected_not", [])

        if dry_run:
            results.append({
                "name": name,
                "status": "DRY-RUN",
                "keywords_total": len(expected_kw),
                "expected_not_count": len(expected_not),
                "input_preview": input_prompt[:60],
            })
            continue

        # 调用 LLM
        try:
            response = call_llm(input_prompt, model, base_url, api_key, system_prompt)
        except Exception as e:
            results.append({
                "name": name,
                "status": "ERROR",
                "error": str(e),
            })
            continue

        # 检查关键词
        hits, misses = check_keywords(response, expected_kw)
        violations = check_not_keywords(response, expected_not)
        hit_rate = len(hits) / len(expected_kw) if expected_kw else 1.0
        passed = hit_rate >= threshold

        results.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "hit_rate": hit_rate,
            "hits": hits,
            "misses": misses,
            "violations": violations,
            "response_length": len(response),
        })

        # 避免 API 限流
        time.sleep(0.5)

    return results


def print_report(all_results, threshold):
    """打印评分报告"""
    print("\n" + "=" * 70)
    print("  performance-mastery Eval Report")
    print("=" * 70)
    print(f"  Pass threshold: {threshold*100:.0f}% of expected_keywords\n")

    total_pass = 0
    total_fail = 0
    total_error = 0
    total_dry = 0

    for suite_result in all_results:
        file_name = suite_result["file"]
        results = suite_result["results"]
        suite_pass = sum(1 for r in results if r["status"] == "PASS")
        suite_fail = sum(1 for r in results if r["status"] == "FAIL")
        suite_error = sum(1 for r in results if r["status"] == "ERROR")
        suite_dry = sum(1 for r in results if r["status"] == "DRY-RUN")

        print(f"── {file_name} ({len(results)} tests) ──")

        for r in results:
            name = r["name"]
            status = r["status"]

            if status == "DRY-RUN":
                print(f"  ⬜ DRY-RUN  {name}  "
                      f"(keywords={r['keywords_total']}, "
                      f"expected_not={r['expected_not_count']})")
            elif status == "ERROR":
                print(f"  ❌ ERROR    {name}  ({r.get('error', 'unknown')})")
            elif status == "PASS":
                warn = ""
                if r.get("violations"):
                    warn = f"  ⚠ found: {r['violations']}"
                print(f"  ✅ PASS     {name}  "
                      f"({r['hit_rate']*100:.0f}% hit, "
                      f"{len(r['hits'])}/{len(r['hits'])+len(r['misses'])}){warn}")
                if r.get("misses"):
                    print(f"              missed: {r['misses']}")
            else:  # FAIL
                warn = ""
                if r.get("violations"):
                    warn = f"  ⚠ found: {r['violations']}"
                print(f"  ❌ FAIL     {name}  "
                      f"({r['hit_rate']*100:.0f}% hit, "
                      f"{len(r['hits'])}/{len(r['hits'])+len(r['misses'])}){warn}")
                print(f"              missed: {r['misses']}")

        total_pass += suite_pass
        total_fail += suite_fail
        total_error += suite_error
        total_dry += suite_dry
        print()

    # 总结
    total = total_pass + total_fail + total_error + total_dry
    print("=" * 70)
    if total_dry > 0:
        print(f"  DRY-RUN: {total_dry}/{total} test cases validated")
        print("  (No LLM calls made — YAML format OK)")
    else:
        print(f"  Total: {total_pass}/{total_pass+total_fail} passed"
              f"  ({total_pass/(total_pass+total_fail)*100:.0f}%)"
              if (total_pass + total_fail) > 0 else "  No tests executed")
        if total_error > 0:
            print(f"  Errors: {total_error}")
    print("=" * 70)

    return total_fail == 0 and total_error == 0


def main():
    parser = argparse.ArgumentParser(
        description="performance-mastery Eval Runner — "
                    "测试 AI 对性能分析问题的回答质量"
    )
    parser.add_argument(
        "--file", "-f",
        help="只运行指定的 eval YAML 文件（默认运行 evals/ 下所有文件）"
    )
    parser.add_argument(
        "--model", "-m",
        default=os.environ.get("EVAL_MODEL", "gpt-4o"),
        help="LLM 模型名称（默认 gpt-4o，可通过 EVAL_MODEL 环境变量设置）"
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="OpenAI 兼容 API 地址（可通过 OPENAI_BASE_URL 环境变量设置）"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="API Key（可通过 OPENAI_API_KEY 环境变量设置）"
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float, default=0.5,
        help="关键词命中率通过阈值（默认 0.5，即 50%%）"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="干跑模式：仅验证 YAML 格式，不调用 LLM"
    )
    parser.add_argument(
        "--output", "-o",
        help="将结果输出为 JSON 文件"
    )

    args = parser.parse_args()

    # 定位 evals 目录
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    eval_dir = project_root / "evals"

    if not eval_dir.exists():
        print(f"ERROR: evals directory not found: {eval_dir}")
        sys.exit(1)

    # 加载测试用例
    suites = load_eval_files(str(eval_dir), args.file)
    if not suites:
        print("ERROR: No eval files found")
        sys.exit(1)

    total_tests = sum(len(s["tests"]) for s in suites)
    print(f"Loaded {len(suites)} eval file(s), {total_tests} test case(s)")

    if not args.dry_run and not args.api_key:
        print("\nWARN: No API key provided. Use --dry-run to validate YAML, "
              "or set OPENAI_API_KEY environment variable.")
        print("Falling back to --dry-run mode.\n")
        args.dry_run = True

    # 运行测试
    all_results = []
    for suite in suites:
        print(f"\nRunning: {suite['file']} ({len(suite['tests'])} tests)...")
        results = run_eval(
            suite, args.model, args.base_url, args.api_key,
            args.threshold, args.dry_run
        )
        all_results.append({"file": suite["file"], "results": results})

    # 输出报告
    success = print_report(all_results, args.threshold)

    # 可选 JSON 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
