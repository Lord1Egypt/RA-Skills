#!/usr/bin/env python3
"""案例库检索脚本 - 支持多维度查询.

Usage:
    python search_cases.py --keyword "赋权"          # 关键词搜索
    python search_cases.py --topic 1                # 按专题编号
    python search_cases.py --chapter 改革创新篇      # 按章节
    python search_cases.py --type 医院              # 按单位类型
    python search_cases.py --first                  # 只看首例
    python search_cases.py --id 5                   # 按案例编号
    python search_cases.py --tag 收益分配            # 按标签
    python search_cases.py --library 全国            # 按数据来源库筛选
    python search_cases.py --list                   # 列出全部摘要
"""
import argparse
import json
import os
import sys

# 数据路径：优先找同目录（独立使用），其次 skill 的 references/ 目录（随技能打包）
_here = os.path.dirname(os.path.abspath(__file__))
LIB = None
for cand in (
    os.path.join(_here, 'case_library.json'),
    os.path.join(_here, '..', 'references', 'case_library.json'),
):
    if os.path.exists(cand):
        LIB = cand
        break
if LIB is None:
    sys.exit('[错误] 未找到 case_library.json（请在案例库目录或技能 references/ 下运行）')

with open(LIB, encoding='utf-8') as f:
    CASES = json.load(f)


def matches(c, args):
    if args.id is not None and c['id'] != args.id:
        return False
    if args.topic is not None and c['topic_number'] != args.topic:
        return False
    if args.chapter and c['chapter_name'] != args.chapter:
        return False
    if args.type and c['organization_type'] != args.type:
        return False
    if args.first and not c['first_case']:
        return False
    if args.tag and args.tag not in c['tags']:
        return False
    if args.library and args.library not in c.get('library', ''):
        return False
    if args.keyword:
        kw = args.keyword.lower()
        haystack = ' '.join([
            c['title'], c['organization'], c['topic_name'],
            c['summary'], c['content'], c['insights'],
            ' '.join(c['tags']), ' '.join(c['key_measures']),
            ' '.join(c['key_policies']),
        ]).lower()
        if kw not in haystack:
            return False
    return True


def fmt_case(c, brief=False):
    if brief:
        return (f"  #{c['id']:>2} | {c['organization']:<24} | "
                f"{c['topic_name'][:14]:<14} | {c['title'][:50]}")
    out = []
    out.append(f"━━━ 案例{c['id']}：{c['title']} ━━━")
    out.append(f"章节：第{c['chapter']}章 {c['chapter_name']} / 专题{c['topic_number']}. {c['topic_name']}")
    out.append(f"单位：{c['organization']}（{c['organization_type']}）")
    if c['first_case']:
        out.append("★ 北京/全国首例")
    out.append(f"标签：{'、'.join(c['tags'])}")
    out.append("")
    out.append(f"【摘要】{c['summary']}")
    return '\n'.join(out)


def cmd_list(_args):
    by_chapter = {}
    for c in CASES:
        by_chapter.setdefault(c['chapter_name'], []).append(c)
    for ch, cs in by_chapter.items():
        print(f"\n# {ch}（{len(cs)}个案例）")
        for c in cs:
            print(fmt_case(c, brief=True))


def main():
    p = argparse.ArgumentParser(description='科技成果转化案例库检索（北京31 + 全国10）')
    p.add_argument('--keyword', '-k', help='关键词搜索（标题/正文/标签）')
    p.add_argument('--id', type=int, help='案例编号 1-41')
    p.add_argument('--topic', type=int, help='专题编号 1-15')
    p.add_argument('--chapter', help='章节名（改革创新篇/能力建设篇/落地承接篇/全国精选篇）')
    p.add_argument('--type', help='单位类型（高校/科研院所/医院/企业/服务机构/政府部门）')
    p.add_argument('--first', action='store_true', help='只看首例')
    p.add_argument('--tag', help='标签筛选')
    p.add_argument('--library', help='数据来源库（北京典型案例集/全国精选案例）')
    p.add_argument('--list', action='store_true', help='列出全部')
    p.add_argument('--brief', action='store_true', help='简略输出')
    p.add_argument('--json', action='store_true', help='输出JSON')
    args = p.parse_args()

    if args.list:
        cmd_list(args)
        return

    results = [c for c in CASES if matches(c, args)]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"共找到 {len(results)} 个案例\n")
        for c in results:
            print(fmt_case(c, args.brief))
            print()


if __name__ == '__main__':
    main()