"""
COT (Chain of Thought) 清洗脚本
用于清洗已生成数据集中的 cot 字段，移除冗长的英文思维链框架文本，
保留中文推理内容。

用法：
  python clean_cot.py <input_json> [output_json]
  
  不加 output_json 参数时，默认输出到 input_json 同目录下的 *_cleaned.json
"""

import json
import re
import sys
import os


def clean_cot(text: str) -> str:
    """清洗单条 COT 文本"""
    if not text or not text.strip():
        return ""

    # Step 1: 移除开头的 "Here's a thinking process:" 或类似前缀
    text = re.sub(r'^Here\s+is\s+a\s+thinking\s+process\s*:?\s*\n*', '', text.strip(), flags=re.IGNORECASE)
    text = re.sub(r'^Here\'s\s+the\s+thinking\s+process\s*:?\s*\n*', '', text.strip(), flags=re.IGNORECASE)

    # Step 1.5: 去除每行开头的英文前缀（后跟中文内容的情况）
    # 例如 "Scanner mechanism:光电传感器..." → "光电传感器..."
    # 例如 "Explain the mechanism (hardware to software): 光电扫描..." → "光电扫描..."
    def strip_english_prefix(line):
        stripped = line.strip()
        # 匹配 "English phrase: Chinese content" 模式
        m = re.match(r'^([A-Za-z][A-Za-z\s/\(\)\-]+):\s*([\u4e00-\u9fff])', stripped)
        if m:
            return stripped[m.end(1)+1:]  # 去掉英文前缀和冒号
        # 匹配 "English phrase -> Chinese" 模式
        m = re.match(r'^([A-Za-z][A-Za-z\s/\(\)\-]+)\s*->\s*([\u4e00-\u9fff])', stripped)
        if m:
            return stripped[m.end(1)+2:]
        # 匹配 "English sentence at start of line followed by backtick-quoted Chinese"
        # e.g. "The reference explicitly states: `中文...`"
        m = re.match(r'^[A-Za-z][A-Za-z\s\-,;]+:\s*`([^`]*)`', stripped)
        if m:
            return m.group(1).strip()
        # 匹配 "The reference says: '...'" 模式
        m = re.match(r"^[A-Za-z][A-Za-z\s\-,;]+:\s*'([^']*)'", stripped)
        if m:
            return m.group(1).strip()
        # 匹配纯英文标记行（后面没有中文或内容为空）
        if re.match(r'^[A-Za-z][A-Za-z\s\-,;]+:\s*$', stripped):
            return ''
        return line

    text = '\n'.join(strip_english_prefix(l) for l in text.split('\n'))

    # Step 2: 按行处理，保留中文含量高的行
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append('')
            continue

        # 统计算中文/英文字符占比
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', stripped))
        total_chars = len(stripped)

        # 纯英文且无中文的行 → 跳过
        if chinese_chars == 0:
            continue

        # 中文字符占比 < 20% 且行以英文开头 → 跳过 (metadata annotations)
        if chinese_chars / max(total_chars, 1) < 0.2 and re.match(r'^[A-Za-z\s*\-]', stripped):
            continue

        # 移除行首的 Markdown 标记编号 (如 "1.  **", "    *   ")
        line = re.sub(r'^\d+\.?\s*\*\*\s*', '', stripped)
        line = re.sub(r'^\s*\*\s+', '', line)
        line = re.sub(r'^\*\s+', '', line)

        cleaned_lines.append(line)

    # Step 3: 合并行，压缩多余空行
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)

    # Step 4: 清理残留的英文标记
    result = re.sub(r'\((?:output|self[-\s]*correction|verification|check|done)\)', '', result, flags=re.IGNORECASE)
    result = re.sub(r'\b(?:Proceed|Draft|Output|Generation|Ready|Check)\b[^.]*\.', '', result, flags=re.IGNORECASE)
    result = re.sub(r'Output\s+Generation\s*\n?', '', result, flags=re.IGNORECASE)
    result = re.sub(r'\[Output\s*Generation\][^]]*\]', '', result, flags=re.IGNORECASE)
    result = re.sub(r'\*See\s*response\*', '', result, flags=re.IGNORECASE)

    # Step 5: 移除 Meta-commentary 行（英语注释/自引用）
    metacomment_patterns = [
        r'^\s*(?:All\s+derived\s+from|Reference\s+says|The\s+prompt\s+asks|The\s+question\s+asks)',
        r'^\s*(?:I\s+will\s+(?:frame|explicitly|use|make)|I\'ll\s+(?:frame|explicitly|use|make))',
        r'^\s*(?:Let\s+me|Let\'s|Now\s+I|I\s+need\s+to|I\s+should\s+need)',
        r'^\s*(?:Be\s+sure\s+to|Make\s+sure\s+to|Ensure\s+that\s+the)',
        r'^\s*(?:Self[- ]?Correction|Verification|Final\s+check)',
        r'^\s*->\s*I',
        r'^\s*-\s*(?:Reference|The\s+prompt|Let|I\s+will|I\'ll|All\s+derived|Check|Ensure)',
        r'^\s*\*\s*(?:Reference|The\s+prompt|Let|I\s+will|I\'ll|All\s+derived|Check|Ensure)',
    ]
    pattern = re.compile('|'.join(metacomment_patterns), re.IGNORECASE)
    lines = result.split('\n')
    
    # 从最后一个匹配的 meta-commentary 行之后截断
    first_meta = len(lines)
    for i, line in enumerate(lines):
        if pattern.match(line):
            first_meta = min(first_meta, i)
    
    if first_meta < len(lines):
        # 往前找最近的空行
        cut = first_meta
        while cut > 0 and lines[cut - 1].strip() != '':
            cut -= 1
        result = '\n'.join(lines[:cut])

    return result.strip()


def clean_dataset(input_path: str, output_path: str = None):
    """清洗整个数据集文件"""
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_cleaned{ext}"

    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: expected JSON array")
        return

    total = len(data)
    cleaned_count = 0
    for i, entry in enumerate(data):
        if 'cot' in entry:
            entry.pop('cot')
            cleaned_count += 1

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{total}")

    # 去重后重新保存
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {cleaned_count}/{total} entries COT cleaned")
    print(f"Output: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    clean_dataset(input_file, output_file)
