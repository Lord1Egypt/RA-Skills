import os
import re
import sys
from pathlib import Path

def check_chapter(filepath):
    """检查单个章节文件"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"无法读取文件: {e}"]
    
    # 检查 YAML frontmatter
    if not content.startswith('---'):
        issues.append("缺少 YAML frontmatter")
        return issues
    
    # 提取 frontmatter
    match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        issues.append("YAML frontmatter 格式错误")
        return issues
    
    frontmatter = match.group(1)
    
    # 检查必需字段
    required_fields = ['title', 'chapter', 'word_count', 'status']
    for field in required_fields:
        if f'{field}:' not in frontmatter:
            issues.append(f"缺少字段: {field}")
    
    # 检查 status 值
    status_match = re.search(r'status:\s*(\w+)', frontmatter)
    if status_match:
        status = status_match.group(1)
        valid_status = ['draft', 'review', 'approved']
        if status not in valid_status:
            issues.append(f"status 值无效: {status}，应为 draft/review/approved")
    
    # 检查字数是否匹配
    word_count_match = re.search(r'word_count:\s*(\d+)', frontmatter)
    if word_count_match:
        declared_count = int(word_count_match.group(1))
        # 统计实际字数（包含符号）
        body = content[match.end():].strip()
        actual_count = len(re.findall(r'\S', body))
        if abs(declared_count - actual_count) > actual_count * 0.1:  # 允许10%误差
            issues.append(f"字数不匹配: 声明{declared_count}, 实际{actual_count}")
    
    # 检查正文是否为空
    body = content[match.end():].strip()
    if len(body) < 100:
        issues.append("正文过短（<100字）")
    
    return issues

def check_all_chapters(chapters_dir):
    """检查所有章节文件"""
    chapters_path = Path(chapters_dir)
    
    if not chapters_path.exists():
        print(f"错误: 目录不存在 {chapters_dir}")
        sys.exit(1)
    
    chapter_files = sorted(chapters_path.glob('第*.md'))
    
    if not chapter_files:
        print(f"警告: 未找到章节文件 in {chapters_dir}")
        return
    
    print(f"检查 {len(chapter_files)} 个章节文件...\n")
    
    total_issues = 0
    for filepath in chapter_files:
        issues = check_chapter(filepath)
        if issues:
            print(f"❌ {filepath.name}")
            for issue in issues:
                print(f"   - {issue}")
            total_issues += len(issues)
        else:
            print(f"✅ {filepath.name}")
    
    print(f"\n{'='*50}")
    print(f"总计: {len(chapter_files)} 个文件, {total_issues} 个问题")
    
    if total_issues > 0:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        chapters_dir = "chapters"
    else:
        chapters_dir = sys.argv[1]
    
    check_all_chapters(chapters_dir)
