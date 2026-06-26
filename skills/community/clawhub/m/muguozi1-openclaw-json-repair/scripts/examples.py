#!/usr/bin/env python3
"""
JSON Repair 使用示例
"""

import subprocess
import json

def example_1_repair_string():
    """示例 1: 修复 JSON 字符串"""
    print("=" * 60)
    print("示例 1: 修复 JSON 字符串")
    print("=" * 60)
    
    result = subprocess.run(
        ["node", "index.js", "--text={a:1,}", "--verbose"],
        capture_output=True, text=True
    )
    print(result.stdout)

def example_2_repair_file():
    """示例 2: 修复 JSON 文件"""
    print("=" * 60)
    print("示例 2: 修复 JSON 文件")
    print("=" * 60)
    
    # 创建测试文件
    test_file = "/tmp/test.json"
    with open(test_file, 'w') as f:
        f.write('{// comment\nname: \'test\',}')
    
    result = subprocess.run(
        ["node", "index.js", "--file=" + test_file, "--backup"],
        capture_output=True, text=True
    )
    print(result.stdout)

def example_3_llm_output():
    """示例 3: 处理 LLM 输出"""
    print("=" * 60)
    print("示例 3: 处理 LLM 输出")
    print("=" * 60)
    
    llm_output = """Here's the JSON:
{
  // 用户信息
  name: 'Alice',
  age: 25,
}"""
    
    print(f"LLM 输出:\n{llm_output}\n")
    print("提取并修复后:\n")
    
    # 使用 Python 简单实现
    import re
    json_str = re.search(r'\{.*\}', llm_output, re.DOTALL).group()
    json_str = json_str.replace("'", '"').replace(',}', '}')
    json_str = re.sub(r'([\{,])\s*([a-zA-Z_]+)\s*:', r'\1"\2":', json_str)
    
    print(json.dumps(json.loads(json_str), indent=2))

if __name__ == "__main__":
    example_1_repair_string()
    example_2_repair_file()
    example_3_llm_output()
    print("\n✅ 所有示例运行完成!")
