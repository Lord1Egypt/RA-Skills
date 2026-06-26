#!/usr/bin/env python3
"""OCR 数据处理脚本 - 从截图中提取文本，生成结构化数据"""
import json, os, re, csv
from datetime import datetime

def extract_from_tooltip(tooltip_text):
    """从 Tooltip 文本提取数据"""
    data = []
    
    # 提取日期
    date_match = re.search(r'(\w+ \d{1,2},? \d{4})', tooltip_text)
    date = date_match.group(1) if date_match else None
    
    # 提取模型和 Token 数据（修复正则表达式）
    lines = tooltip_text.replace('\n', ' ').split(' ')
    i = 0
    while i < len(lines) - 1:
        # 查找数字+B/T 模式
        if re.match(r'^[\d\.]+[BT]$', lines[i], re.IGNORECASE):
            value_str = lines[i]
            model_name = lines[i-1] if i > 0 else 'Unknown'
            
            # 解析数值
            match = re.match(r'([\d\.]+)([BT])', value_str, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                unit = match.group(2).upper()
                tokens = int(value * (1e12 if unit == 'T' else 1e9))
                
                data.append({
                    'date': date,
                    'model': model_name,
                    'tokens': tokens
                })
        i += 1
    
    return data

def process_screenshots(output_dir):
    """处理所有截图"""
    result_file = os.path.join(output_dir, 'extraction_result.json')
    
    if not os.path.exists(result_file):
        print(f"❌ 结果文件不存在：{result_file}")
        return []
    
    with open(result_file) as f:
        result = json.load(f)
    
    all_data = []
    
    for shot in result.get('screenshots', []):
        tooltip = shot.get('tooltip', '')
        if tooltip:
            data = extract_from_tooltip(tooltip)
            if data:
                all_data.extend(data)
                print(f"  ✅ 提取 {len(data)} 条数据：{tooltip[:50]}...")
    
    return all_data

def save_csv(data, output_file):
    """保存为 CSV"""
    if not data:
        print("⚠️  无数据可保存")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'model', 'tokens'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✅ CSV 已保存：{output_file}")
    print(f"📊 总记录数：{len(data)}")

def main():
    output_dir = '/root/.openclaw/workspace/skills/playwright_ocr/output'
    csv_file = f'{output_dir}/extracted_data.csv'
    
    print('=' * 60)
    print('🔍 OCR 数据处理')
    print('=' * 60)
    
    data = process_screenshots(output_dir)
    save_csv(data, csv_file)

if __name__ == '__main__':
    main()
