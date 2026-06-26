#!/usr/bin/env python3
"""
合并LoRA权重到基础模型
使用场景：蒸馏完成后，将LoRA权重合并以简化部署
"""

import torch
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
import argparse
from pathlib import Path

def merge_lora_weights(lora_model_path, output_path):
    """
    将LoRA权重合并到基础模型

    Args:
        lora_model_path: 包含LoRA权重的模型路径
        output_path: 合并后模型的输出路径
    """
    print(f"加载LoRA模型: {lora_model_path}")

    # 加载模型（包含LoRA权重）
    model = AutoPeftModelForCausalLM.from_pretrained(
        lora_model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    print("合并LoRA权重...")
    # 合并权重
    merged_model = model.merge_and_unload()

    # 保存合并后的模型
    print(f"保存合并后的模型到: {output_path}")
    Path(output_path).mkdir(parents=True, exist_ok=True)

    merged_model.save_pretrained(output_path)

    # 同时保存tokenizer
    tokenizer = AutoTokenizer.from_pretrained(lora_model_path)
    tokenizer.save_pretrained(output_path)

    print("✅ 合并完成！")
    print(f"合并后模型大小:")
    # 计算模型大小
    total_size = 0
    for file in Path(output_path).glob("*"):
        if file.is_file():
            total_size += file.stat().st_size

    size_mb = total_size / (1024 * 1024)
    size_gb = size_mb / 1024
    print(f"  {size_mb:.1f} MB ({size_gb:.2f} GB)")

def main():
    parser = argparse.ArgumentParser(description="合并LoRA权重到基础模型")
    parser.add_argument("--lora_path", type=str, required=True,
                        help="LoRA模型路径（如 outputs/final_model）")
    parser.add_argument("--output", type=str, default="outputs/merged_model",
                        help="合并后模型的输出路径")
    args = parser.parse_args()

    merge_lora_weights(args.lora_path, args.output)

if __name__ == "__main__":
    main()
