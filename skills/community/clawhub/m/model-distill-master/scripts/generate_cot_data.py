#!/usr/bin/env python3
"""
生成CoT（思维链）训练数据
使用教师模型为种子数据生成带有推理过程的标注
"""

import json
import argparse
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
import time

class CoTDataGenerator:
    def __init__(self, teacher_model_name="gpt-4"):
        """
        初始化CoT数据生成器

        Args:
            teacher_model_name: 教师模型名称或API端点
        """
        self.teacher_model = teacher_model_name
        self.cot_prompt_template = """请解决以下问题，并详细展示你的思考过程：

问题：{question}

要求：
1. 先分析问题类型和关键信息
2. 逐步推理，展示中间步骤（不要跳步）
3. 在关键步骤进行自我验证
4. 给出最终答案

请用以下格式回答：
思考过程：
[详细展示你的思考过程]

答案：
[最终答案]
"""

    def generate_cot_response(self, question, max_retries=3):
        """
        使用教师模型生成CoT回复

        注意：这是一个模板函数，实际实现需要根据教师模型的类型调整：
        - OpenAI API: 使用openai库
        - 本地模型: 使用transformers
        - Claude API: 使用anthropic库
        """
        prompt = self.cot_prompt_template.format(question=question)

        # 这里需要根据实际的教师模型类型实现
        # 示例使用模拟数据
        for attempt in range(max_retries):
            try:
                # TODO: 实现实际的API调用
                # 示例：
                # if "gpt" in self.teacher_model:
                #     return self._call_openai(prompt)
                # elif "claude" in self.teacher_model:
                #     return self._call_anthropic(prompt)
                # else:
                #     return self._call_local_model(prompt)

                # 模拟延迟
                time.sleep(0.1)

                # 返回模拟数据（实际应替换为真实API调用）
                return f"思考过程：\n让我一步步分析这个问题...\n\n答案：\n[示例答案]"

            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"生成失败: {e}")
                    return None
                time.sleep(2 ** attempt)  # 指数退避

        return None

    def process_item(self, item):
        """处理单个数据项"""
        question = item.get('input', item.get('instruction', item.get('question', '')))

        cot_response = self.generate_cot_response(question)

        if cot_response:
            return {
                'input': question,
                'output': cot_response,
                'metadata': {
                    'teacher_model': self.teacher_model,
                    'has_cot': True
                }
            }
        return None

    def generate_dataset(self, input_file, output_file, max_workers=5):
        """
        批量生成CoT数据集

        Args:
            input_file: 输入的jsonl文件（包含问题）
            output_file: 输出的jsonl文件（包含CoT标注）
            max_workers: 并行工作数（API调用限制）
        """
        # 加载输入数据
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = [json.loads(line) for line in f]

        print(f"加载输入数据: {len(input_data)} 条")
        print(f"使用教师模型: {self.teacher_model}")
        print(f"开始生成CoT数据...")

        results = []

        # 串行处理（避免API限流）
        for item in tqdm(input_data, desc="生成CoT"):
            result = self.process_item(item)
            if result:
                results.append(result)

            # 简单的速率限制
            time.sleep(0.5)

        # 保存结果
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in results:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

        print(f"\n✅ 生成完成！")
        print(f"成功生成: {len(results)}/{len(input_data)} 条")
        print(f"输出文件: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="生成CoT训练数据")
    parser.add_argument("--input", type=str, required=True,
                        help="输入的jsonl文件（包含问题）")
    parser.add_argument("--output", type=str, required=True,
                        help="输出的jsonl文件（包含CoT标注）")
    parser.add_argument("--teacher", type=str, default="gpt-4",
                        help="教师模型名称")
    parser.add_argument("--workers", type=int, default=1,
                        help="并行工作数（API限制建议设为1）")
    args = parser.parse_args()

    generator = CoTDataGenerator(teacher_model_name=args.teacher)
    generator.generate_dataset(args.input, args.output, max_workers=args.workers)

if __name__ == "__main__":
    main()
