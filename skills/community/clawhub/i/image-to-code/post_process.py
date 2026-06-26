#!/usr/bin/env python3
"""
后处理脚本 - 合并被分割的标题行
"""

import re

def merge_title_lines(lines):
    """合并被分割的标题和内容"""
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检测空标题行 $word->title2("");
        match = re.match(r'\$word->title(\d+)\(""\);', line)
        if match:
            level = match.group(1)
            # 收集后续的中文字符行
            title_parts = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # 检测是否是正文行且内容较短（可能是标题的一部分）
                body_match = re.match(r'\$word->body\("正文=(.+?)="\.\$F\);', next_line)
                if body_match:
                    content = body_match.group(1)
                    # 如果是短文本（可能是标题），合并
                    if len(content) <= 10 and not any(c.isalpha() for c in content):
                        title_parts.append(content)
                        j += 1
                    else:
                        break
                else:
                    break
            
            # 生成合并后的标题
            if title_parts:
                title_text = ''.join(title_parts)
                result.append(f'$word->title{level}("{title_text}");')
                i = j
                continue
        
        result.append(line)
        i += 1
    
    return result

# 读取文件
with open('/tmp/test_new_image.txt', 'r', encoding='utf-8') as f:
    lines = f.read().strip().split('\n')

# 合并处理
merged = merge_title_lines(lines)

# 输出结果
print("="*60)
print("优化后的输出:")
print("="*60)
for line in merged:
    print(line)

# 保存
with open('/tmp/test_new_image_optimized.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(merged))

print("\n✅ 已保存到：/tmp/test_new_image_optimized.txt")
