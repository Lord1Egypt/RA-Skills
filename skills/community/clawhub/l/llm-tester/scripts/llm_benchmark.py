#!/usr/bin/env python3
"""
LLM 模型对比测试工具

功能：
- 支持多个模型对比测试
- 支持批量测试多个样本文件
- 支持自定义 Prompt 模板
- 记录耗时、Token 消耗、成功率
- 生成 JSON 格式对比报告
- 超时自动跳过，不阻塞其他模型

使用方式：
  python3 llm_benchmark.py --samples samples/ --prompts prompts/ --models qwen3.6-plus qwen3-max --output report.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

# 配置
API_BASE = os.environ.get(
    "LLM_API_BASE",
    "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
)
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DEFAULT_TIMEOUT = 60
DEFAULT_MODELS = ["qwen3.6-plus", "qwen3-max-2026-01-23"]


def load_samples(samples_dir: str) -> list[dict[str, str]]:
    """加载测试样本"""
    samples = []
    samples_path = Path(samples_dir)
    if not samples_path.exists():
        raise FileNotFoundError(f"样本目录不存在：{samples_dir}")
    
    for txt_file in sorted(samples_path.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8")
        samples.append({
            "name": txt_file.stem,
            "content": content[:2000],  # 限制长度
            "length": len(content),
        })
    
    if not samples:
        raise ValueError(f"样本目录中没有找到 .txt 文件：{samples_dir}")
    
    return samples


def load_prompts(prompts_dir: str) -> list[dict[str, str]]:
    """加载 Prompt 模板"""
    prompts = []
    prompts_path = Path(prompts_dir)
    if not prompts_path.exists():
        raise FileNotFoundError(f"Prompt 目录不存在：{prompts_dir}")
    
    for txt_file in sorted(prompts_path.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8")
        prompts.append({
            "name": txt_file.stem,
            "template": content,
        })
    
    if not prompts:
        raise ValueError(f"Prompt 目录中没有找到 .txt 文件：{prompts_dir}")
    
    return prompts


def call_model(
    model: str,
    prompt: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """调用单个模型"""
    if not API_KEY:
        return {"status": "error", "time": 0, "error": "未设置 DASHSCOPE_API_KEY 环境变量"}
    
    start = time.time()
    try:
        resp = requests.post(
            API_BASE,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
            },
            timeout=timeout,
        )
        elapsed = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            result = json.loads(data["choices"][0]["message"]["content"])
            return {
                "status": "success",
                "time": round(elapsed, 2),
                "tokens": data.get("usage", {}).get("total_tokens", 0),
                "result": result,
            }
        else:
            return {
                "status": "error",
                "time": round(elapsed, 2),
                "error": f"HTTP {resp.status_code}: {resp.text[:100]}",
            }
    except requests.exceptions.Timeout:
        return {"status": "timeout", "time": timeout, "error": f"超时 ({timeout}s)"}
    except Exception as e:
        return {"status": "error", "time": round(time.time() - start, 2), "error": str(e)}


def run_benchmark(
    samples: list[dict],
    prompts: list[dict],
    models: list[str],
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """运行基准测试"""
    results = {}
    total_tests = len(samples) * len(prompts) * len(models)
    current_test = 0
    
    print("\n📋 测试配置：")
    print(f"  样本数：{len(samples)}")
    print(f"  Prompt 数：{len(prompts)}")
    print(f"  模型：{', '.join(models)}")
    print(f"  超时：{timeout}s")
    print(f"  总测试次数：{total_tests}")
    print("=" * 60)
    
    for sample in samples:
        for prompt_tpl in prompts:
            prompt = prompt_tpl["template"].format(text=sample["content"])
            sample_results = {}
            
            print(f"\n📝 测试：{sample['name']} + {prompt_tpl['name']}")
            
            for model in models:
                current_test += 1
                print(f"  [{current_test}/{total_tests}] {model}...", end=" ", flush=True)
                
                result = call_model(model, prompt, timeout)
                sample_results[model] = result
                
                if result["status"] == "success":
                    print(f"✅ {result['time']}s | {result['tokens']} tokens")
                    labels = result.get("result", {}).get("labels", [])
                    if labels:
                        print(f"    标签：{', '.join(labels)}")
                else:
                    print(f"❌ {result.get('error', 'unknown')}")
            
            results[f"{sample['name']}_{prompt_tpl['name']}"] = sample_results
    
    return results


def generate_summary(results: dict[str, Any], models: list[str]) -> dict[str, Any]:
    """生成汇总报告"""
    summary = {}
    
    for model in models:
        stats = {"success": 0, "fail": 0, "timeout": 0, "total_time": 0, "total_tokens": 0}
        
        for test_name, test_results in results.items():
            r = test_results.get(model, {})
            if r.get("status") == "success":
                stats["success"] += 1
                stats["total_time"] += r["time"]
                stats["total_tokens"] += r.get("tokens", 0)
            elif r.get("status") == "timeout":
                stats["timeout"] += 1
            else:
                stats["fail"] += 1
        
        total = stats["success"] + stats["fail"] + stats["timeout"]
        if total > 0:
            summary[model] = {
                "success_rate": f"{stats['success']}/{total} ({stats['success']/total*100:.0f}%)",
                "avg_time": f"{stats['total_time']/stats['success']:.1f}s" if stats["success"] > 0 else "N/A",
                "avg_tokens": f"{stats['total_tokens']/stats['success']:.0f}" if stats["success"] > 0 else "N/A",
                "total_time": f"{stats['total_time']:.1f}s",
                "total_tokens": stats["total_tokens"],
                "success": stats["success"],
                "fail": stats["fail"],
                "timeout": stats["timeout"],
            }
    
    return summary


def save_report(report: dict[str, Any], output_path: str) -> None:
    """保存报告"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n📄 报告已保存：{output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="LLM 模型对比测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 llm_benchmark.py --samples samples/ --prompts prompts/ --models qwen3.6-plus qwen3-max
  python3 llm_benchmark.py -s samples/ -p prompts/ -m qwen3.6-plus qwen3-max-2026-01-23 --timeout 90 --output report.json
        """
    )
    
    parser.add_argument(
        "--samples", "-s",
        required=True,
        help="测试样本目录（包含 .txt 文件）"
    )
    parser.add_argument(
        "--prompts", "-p",
        required=True,
        help="Prompt 模板目录（包含 .txt 文件）"
    )
    parser.add_argument(
        "--models", "-m",
        nargs="+",
        default=DEFAULT_MODELS,
        help="要测试的模型列表（默认：qwen3.6-plus qwen3-max-2026-01-23）"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="单个模型超时时间（秒，默认 60）"
    )
    parser.add_argument(
        "--output", "-o",
        default="reports/benchmark-report.json",
        help="报告输出路径（默认：reports/benchmark-report.json）"
    )
    
    args = parser.parse_args()
    
    try:
        samples = load_samples(args.samples)
        prompts = load_prompts(args.prompts)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ {e}")
        return 1
    
    # 运行测试
    results = run_benchmark(samples, prompts, args.models, args.timeout)
    
    # 生成汇总
    summary = generate_summary(results, args.models)
    
    # 打印汇总
    print("\n" + "=" * 60)
    print("性能汇总")
    print("=" * 60)
    for model, stats in summary.items():
        print(f"\n{model}:")
        print(f"  成功率：{stats['success_rate']}")
        print(f"  平均耗时：{stats['avg_time']}")
        print(f"  平均 Token：{stats['avg_tokens']}")
        print(f"  总耗时：{stats['total_time']}")
        print(f"  总 Token：{stats['total_tokens']}")
    
    # 保存报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "samples_dir": args.samples,
            "prompts_dir": args.prompts,
            "models": args.models,
            "timeout": args.timeout,
        },
        "summary": summary,
        "results": results,
    }
    save_report(report, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
