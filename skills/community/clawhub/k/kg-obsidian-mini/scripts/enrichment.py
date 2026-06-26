#!/usr/bin/env python3
"""
enrichment.py — 笔记补完预览脚本。
用法: python scripts/enrichment.py <笔记.md> [--stdout]
功能: 读取笔记 frontmatter + 正文前 30 行，生成结构化的补完建议预览。
输出: JSON 格式，含笔记类型、L0摘要、已有内容摘要、推荐搜索关键词列表。
"""

import sys, json, re, os

def extract_frontmatter(content):
    if not content.startswith('---'):
        return {}
    end = content.find('---', 3)
    if end == -1:
        return {}
    fm = content[3:end]
    try:
        import yaml
        parsed = yaml.safe_load(fm)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}

def extract_body_start(content, max_lines=30):
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            body = content[end+3:].strip()
        else:
            body = content[3:].strip()
    else:
        body = content
    lines = body.split('\n')[:max_lines]
    clean = [l.strip() for l in lines if l.strip()]
    return clean[:15]  # 取前 15 条非空行

def suggest_search_keywords(tags, title, body_lines):
    keywords = []
    if tags:
        keywords.extend([t.strip() for t in tags if t.strip()])
    # 从标题提取关键词
    name = os.path.splitext(os.path.basename(title))[0]
    # 去掉关系笔记中的 " - "
    parts = [p.strip() for p in name.split(' - ')]
    keywords.extend(parts)
    return list(set(keywords))

def analyze(fp):
    if not os.path.isfile(fp):
        return {"error": f"文件不存在: {fp}"}
    
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    fm = extract_frontmatter(content)
    body_lines = extract_body_start(content)
    name = os.path.basename(fp)
    tags = fm.get('tags', [])

    result = {
        "file": name,
        "tags": tags if isinstance(tags, list) else [tags],
        "abstract": fm.get('abstract', ''),
        "type_hint": "",
        "body_preview": body_lines[:8],
        "search_keywords": suggest_search_keywords(tags, name, body_lines),
        "enrichment_sections": []
    }

    # 判断类型
    tag_str = ' '.join(result['tags']) if isinstance(result['tags'], list) else str(result['tags'])
    if '概念' in tag_str:
        result['type_hint'] = '概念笔记'
        result['enrichment_sections'] = ["核心规则", "来源", "应用场景", "相关概念"]
    elif '某物' in tag_str:
        result['type_hint'] = '某物笔记'
        result['enrichment_sections'] = ["基本信息", "属性/参数", "位置/时间"]
    elif 'skill' in tag_str.lower():
        result['type_hint'] = 'Skill笔记'
        result['enrichment_sections'] = ["步骤", "前提条件", "注意事项", "效果评估"]
    elif '关系' in tag_str:
        result['type_hint'] = '关系笔记'
        result['enrichment_sections'] = ["关系描述"]
    else:
        result['type_hint'] = '未分类'

    return result

if __name__ == '__main__':
    to_stdout = '--stdout' in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    if not files:
        print(json.dumps({"error": "用法: python enrichment.py <笔记.md> [--stdout]"}, ensure_ascii=False))
        sys.exit(1)
    
    results = {}
    for fp in files:
        result = analyze(fp)
        results[os.path.basename(fp)] = result
    
    output = json.dumps(results, ensure_ascii=False, indent=2)
    if to_stdout:
        sys.stdout.write(output)
        sys.stdout.write('\n')
    else:
        print(output)
