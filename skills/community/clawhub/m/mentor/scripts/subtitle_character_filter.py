#!/usr/bin/env python3
"""
subtitle_character_filter.py — 从完整字幕中筛选特定角色的台词

用法: python3 subtitle_character_filter.py --input <字幕文件/目录> --character <角色名> --traits <特征描述> --output <输出文件>

B站字幕包含所有角色的对话，此脚本通过关键词+LLM辅助筛选出目标角色的台词。

第一步：基于关键词粗筛（口头禅/称呼/语气词）
第二步：生成 LLM prompt，由用户手动或自动调用 LLM 精筛
"""

import re, json, sys, os, argparse


def load_subtitles(path):
    """加载字幕文件"""
    if os.path.isdir(path):
        texts = []
        for f in sorted(os.listdir(path)):
            if f.endswith('.txt'):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as fh:
                    texts.append(f"--- {f} ---\n" + fh.read())
        return '\n'.join(texts)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


def keyword_filter(text, catchphrases=None, names=None, exclude_patterns=None):
    """基于关键词粗筛可能是目标角色的台词行"""
    lines = text.split('\n')
    scored_lines = []

    catchphrases = catchphrases or []
    names = names or []
    exclude_patterns = exclude_patterns or []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('---'):
            continue

        score = 0
        reasons = []

        # 口头禅匹配
        for cp in catchphrases:
            if cp in line:
                score += 3
                reasons.append(f'口头禅"{cp}"')

        # 提到其他角色名（可能是对他们说话）
        for name in names:
            if name in line:
                score += 1
                reasons.append(f'提到"{name}"')

        # 排除模式
        skip = False
        for ep in exclude_patterns:
            if re.search(ep, line):
                skip = True
                break

        if not skip and score > 0:
            scored_lines.append({
                'line_num': i + 1,
                'text': line,
                'score': score,
                'reasons': reasons
            })

    # 按分数排序
    scored_lines.sort(key=lambda x: -x['score'])
    return scored_lines


def generate_llm_prompt(character_name, traits, subtitle_text, work_name=""):
    """生成 LLM 精筛 prompt"""
    prompt = f"""以下是{'动画' if not work_name else work_name}的字幕文本。
请识别并提取角色「{character_name}」的台词。

已知「{character_name}」的特征:
{traits}

规则:
1. 只输出「{character_name}」说的话，每行一句
2. 不确定是否为该角色的台词，用 [?] 标注
3. 旁白、其他角色的台词不要包含
4. 保留原文，不要修改

字幕文本:
{subtitle_text[:8000]}
"""
    return prompt


def main():
    parser = argparse.ArgumentParser(description='从字幕中筛选特定角色台词')
    parser.add_argument('--input', required=True, help='字幕文件或目录')
    parser.add_argument('--character', required=True, help='目标角色名')
    parser.add_argument('--catchphrases', nargs='*', default=[], help='角色口头禅列表')
    parser.add_argument('--related-names', nargs='*', default=[], help='相关角色名（角色经常称呼的人）')
    parser.add_argument('--traits', default='', help='角色特征描述（用于LLM prompt）')
    parser.add_argument('--work', default='', help='作品名')
    parser.add_argument('--output', default=None, help='输出文件路径')
    parser.add_argument('--prompt-only', action='store_true', help='只生成LLM prompt，不做关键词筛选')
    args = parser.parse_args()

    subtitle_text = load_subtitles(args.input)
    total_lines = len([l for l in subtitle_text.split('\n') if l.strip()])
    print(f"📄 加载字幕: {total_lines} 行")

    if args.prompt_only:
        # 只生成 LLM prompt
        prompt = generate_llm_prompt(args.character, args.traits, subtitle_text, args.work)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ LLM prompt 已保存到 {args.output}")
        else:
            print(prompt)
        return

    # 关键词粗筛
    if args.catchphrases or args.related_names:
        results = keyword_filter(subtitle_text, args.catchphrases, args.related_names)
        print(f"\n🔍 关键词粗筛: {len(results)} 行可能是「{args.character}」的台词")

        if results:
            print(f"\nTOP 10 高置信台词:")
            for r in results[:10]:
                print(f"  [{r['score']}分] L{r['line_num']}: 「{r['text'][:80]}」 ← {', '.join(r['reasons'])}")

        if args.output:
            filtered_text = '\n'.join(r['text'] for r in results)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(filtered_text)
            print(f"\n✅ 粗筛结果已保存到 {args.output}")
    else:
        print("⚠️ 未提供口头禅或相关角色名，跳过关键词筛选")

    # 生成 LLM 精筛 prompt
    prompt = generate_llm_prompt(args.character, args.traits, subtitle_text, args.work)
    prompt_file = (args.output or '/tmp/character_filter') + '_llm_prompt.txt'
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"\n📝 LLM 精筛 prompt 已保存到 {prompt_file}")
    print(f"   可以将此 prompt 发给 AI 进行精确角色台词提取")


if __name__ == '__main__':
    main()
