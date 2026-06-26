#!/usr/bin/env python3
"""
基线测试脚本 - 测试gemma-3-4b-it的基础能力
生成基线报告供后续对比
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import time
import sys
from pathlib import Path

def load_model(model_path):
    """加载模型和分词器"""
    print(f"正在加载模型: {model_path}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    return model, tokenizer

def generate_response(model, tokenizer, prompt, max_new_tokens=256):
    """生成回复"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    start_time = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    end_time = time.time()

    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = generated[len(prompt):]

    # 计算速度
    num_tokens = len(outputs[0]) - len(inputs[0])
    time_taken = end_time - start_time
    tokens_per_sec = num_tokens / time_taken if time_taken > 0 else 0

    return response, tokens_per_sec

def run_tests(model, tokenizer):
    """运行测试用例"""

    test_cases = [
        {
            "name": "基础推理",
            "prompt": "1 + 1 = ?",
            "expected_keywords": ["2"]
        },
        {
            "name": "简单代码",
            "prompt": "写一个Python函数，计算两个数的和。",
            "expected_keywords": ["def", "return"]
        },
        {
            "name": "逻辑推理",
            "prompt": "如果A比B大，B比C大，那么A和C谁大？",
            "expected_keywords": ["A", "大"]
        },
        {
            "name": "数学计算",
            "prompt": "15 * 24 = ?",
            "expected_keywords": ["360"]
        }
    ]

    results = []
    total_speed = 0

    print("\n运行测试用例...\n")

    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] {test['name']}")

        response, speed = generate_response(model, tokenizer, test['prompt'])

        # 检查关键词
        has_keywords = all(kw in response for kw in test['expected_keywords'])

        result = {
            "name": test['name'],
            "prompt": test['prompt'],
            "response": response[:200] + "..." if len(response) > 200 else response,
            "speed": round(speed, 2),
            "has_keywords": has_keywords
        }
        results.append(result)

        print(f"  响应: {response[:100]}...")
        print(f"  速度: {speed:.2f} tokens/s")
        print(f"  关键词检查: {'✅' if has_keywords else '❌'}")
        print()

        total_speed += speed

    avg_speed = total_speed / len(test_cases)

    return results, avg_speed

def main():
    model_path = sys.argv[1] if len(sys.argv) > 1 else "./models/gemma-3-4b-it"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "./model-distill/outputs/baseline_report.json"

    # 确保输出目录存在
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    try:
        model, tokenizer = load_model(model_path)

        results, avg_speed = run_tests(model, tokenizer)

        # 生成报告
        report = {
            "model": model_path,
            "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "avg_speed": round(avg_speed, 2),
            "results": results
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("=" * 50)
        print("基线测试完成！")
        print(f"平均推理速度: {avg_speed:.2f} tokens/s")
        print(f"报告已保存: {output_file}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
