#!/usr/bin/env python3
"""
模型评估脚本
对比蒸馏前后的性能差异
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import argparse
from pathlib import Path
from tqdm import tqdm
import time

class ModelEvaluator:
    def __init__(self, model_path, device="auto"):
        """初始化评估器"""
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map=device,
            trust_remote_code=True
        )
        self.model.eval()

    def generate(self, prompt, max_new_tokens=256, temperature=0.7):
        """生成回复"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        start_time = time.time()
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        end_time = time.time()

        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = generated[len(prompt):]

        num_tokens = len(outputs[0]) - len(inputs[0])
        time_taken = end_time - start_time
        tokens_per_sec = num_tokens / time_taken if time_taken > 0 else 0

        return response, tokens_per_sec

    def evaluate_accuracy(self, test_data):
        """评估准确率"""
        results = []
        correct = 0
        total_speed = 0

        for item in tqdm(test_data, desc="评估中"):
            prompt = item.get('input', item.get('instruction', ''))
            expected = item.get('output', item.get('response', ''))

            response, speed = self.generate(prompt)

            # 简单匹配（实际应更精细）
            is_correct = expected.strip().lower() in response.strip().lower()
            correct += is_correct
            total_speed += speed

            results.append({
                'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
                'expected': expected[:100] + '...' if len(expected) > 100 else expected,
                'generated': response[:200] + '...' if len(response) > 200 else response,
                'correct': is_correct,
                'speed': round(speed, 2)
            })

        accuracy = correct / len(test_data) if test_data else 0
        avg_speed = total_speed / len(test_data) if test_data else 0

        return {
            'accuracy': accuracy,
            'avg_speed': avg_speed,
            'results': results
        }

def compare_models(baseline_path, distilled_path, test_data):
    """对比基线模型和蒸馏模型"""
    print("=" * 60)
    print("模型对比评估")
    print("=" * 60)

    # 评估基线
    print(f"\n[1/2] 评估基线模型: {baseline_path}")
    baseline_eval = ModelEvaluator(baseline_path)
    baseline_results = baseline_eval.evaluate_accuracy(test_data)

    # 评估蒸馏模型
    print(f"\n[2/2] 评估蒸馏模型: {distilled_path}")
    distilled_eval = ModelEvaluator(distilled_path)
    distilled_results = distilled_eval.evaluate_accuracy(test_data)

    # 生成对比报告
    report = {
        'baseline': {
            'path': baseline_path,
            'accuracy': baseline_results['accuracy'],
            'avg_speed': baseline_results['avg_speed']
        },
        'distilled': {
            'path': distilled_path,
            'accuracy': distilled_results['accuracy'],
            'avg_speed': distilled_results['avg_speed']
        },
        'comparison': {
            'accuracy_change': distilled_results['accuracy'] - baseline_results['accuracy'],
            'speed_change': distilled_results['avg_speed'] - baseline_results['avg_speed'],
            'accuracy_change_pct': ((distilled_results['accuracy'] - baseline_results['accuracy']) / baseline_results['accuracy'] * 100) if baseline_results['accuracy'] > 0 else 0
        }
    }

    # 打印对比结果
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)
    print(f"{'指标':<20} {'基线':<15} {'蒸馏后':<15} {'变化':<15}")
    print("-" * 60)
    print(f"{'准确率':<20} {baseline_results['accuracy']:.2%}          {distilled_results['accuracy']:.2%}          {report['comparison']['accuracy_change']:+.2%}")
    print(f"{'推理速度':<20} {baseline_results['avg_speed']:.2f} tok/s     {distilled_results['avg_speed']:.2f} tok/s     {report['comparison']['speed_change']:+.2f} tok/s")
    print("=" * 60)

    return report

def main():
    parser = argparse.ArgumentParser(description="评估模型性能")
    parser.add_argument("--model", type=str, required=True, help="要评估的模型路径")
    parser.add_argument("--test_data", type=str, required=True, help="测试数据路径 (jsonl)")
    parser.add_argument("--output", type=str, default="eval_results.json", help="输出文件")
    parser.add_argument("--baseline", type=str, default=None, help="基线模型路径（用于对比）")
    args = parser.parse_args()

    # 加载测试数据
    with open(args.test_data, 'r', encoding='utf-8') as f:
        test_data = [json.loads(line) for line in f]

    print(f"加载测试数据: {len(test_data)} 条")

    if args.baseline:
        # 对比模式
        report = compare_models(args.baseline, args.model, test_data)
    else:
        # 单模型评估
        evaluator = ModelEvaluator(args.model)
        results = evaluator.evaluate_accuracy(test_data)

        report = {
            'model': args.model,
            'accuracy': results['accuracy'],
            'avg_speed': results['avg_speed'],
            'results': results['results']
        }

        print(f"\n准确率: {results['accuracy']:.2%}")
        print(f"平均推理速度: {results['avg_speed']:.2f} tokens/s")

    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存: {args.output}")

if __name__ == "__main__":
    main()
