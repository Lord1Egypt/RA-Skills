#!/usr/bin/env python3
"""
🦞 龙虾医生 — 技能瘦身 (Skill Slim)

分析所有技能 description 的 token 消耗，支持一键精简。

精简策略：
  - 保留触发关键词（Activate when user mentions...）
  - 保留排除条件（NOT for...）
  - 删除冗余解释、示例、引导语
  - 中文技能描述尽量用中文

用法：
  python3 skill_slim.py report           查看报告（不修改）
  python3 skill_slim.py dry-run          预览精简效果（不修改）
  python3 skill_slim.py apply            应用精简（会修改SKILL.md）
"""

import os
import re
import sys
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"

# 技能扫描目录（按优先级）
SKILL_DIRS = [
    Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills",
    Path.home() / ".openclaw" / "skills",
    WORKSPACE / "skills",
]

# 核心技能白名单（不精简，始终保持完整描述）
CORE_SKILLS = {
    "lobster-doctor",  # 自己
}


def parse_frontmatter(content):
    """解析 SKILL.md 的 frontmatter，返回 (name, raw_description, rest_content)"""
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None, None, content

    fm = fm_match.group(1)
    rest = content[fm_match.end():]

    name_match = re.search(r'^name:\s*(.+)$', fm, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)

    name = name_match.group(1).strip().strip('"\'') if name_match else None
    raw_desc = desc_match.group(1) if desc_match else None

    return name, raw_desc, rest


def clean_description(raw_desc):
    """精简 description，保留关键信息，去除冗余

    优先级：核心功能句 > 触发关键词 > 排除条件 > 示例
    """
    # 去掉 YAML 多行前缀
    desc = re.sub(r'^\s*>\s*', '', raw_desc, flags=re.MULTILINE).strip()
    # 去掉引号包裹
    desc = desc.strip('"\'')
    # 合并多行为单行
    desc = re.sub(r'\n\s*', ' ', desc).strip()
    # 去掉多余空格
    desc = re.sub(r'\s+', ' ', desc)

    # 🆕 去除重复片段（检测连续重复的句子/短语）
    # 方法：用滑动窗口检测重复的连续序列
    words = desc.split()
    if len(words) >= 6:  # 降低阈值，支持短句
        # 尝试不同长度的窗口
        for window_size in range(min(20, len(words)//2), 4, -1):  # 改为 4，确保包含 5
            i = 0
            while i < len(words) - window_size * 2:
                # 归一化窗口内容（忽略标点）
                window = ' '.join(words[i:i+window_size]).lower()
                window_norm = re.sub(r'[^\w\s]', '', window)
                # 检查后面是否有相同的窗口
                for j in range(i + window_size, len(words) - window_size + 1):
                    candidate = ' '.join(words[j:j+window_size]).lower()
                    candidate_norm = re.sub(r'[^\w\s]', '', candidate)
                    if window_norm == candidate_norm:
                        # 发现重复，删除后面的重复部分
                        words = words[:j] + words[j+window_size:]
                        break
                i += 1
            if len(words) < len(desc.split()):
                break
        desc = ' '.join(words)

    # 🆕 清理相邻的重复单词（忽略标点）
    words = desc.split()
    cleaned_words = []
    prev_word = None
    for w in words:
        w_norm = re.sub(r'[^\w]', '', w.lower())
        prev_norm = re.sub(r'[^\w]', '', (prev_word or '').lower())
        if w_norm != prev_norm:
            cleaned_words.append(w)
        prev_word = w
    desc = ' '.join(cleaned_words)

    # 🆕 如果去重后的描述已经足够短，直接返回
    if len(desc) <= 150:
        return desc

    result_parts = []

    # 1. 提取核心功能句（第一句话，包含关键动词/名词）
    # 匹配模式：以大写字母开头，到第一个句号+空格结束（排除 URL 中的点）
    first_sentence_match = re.match(r'([A-Z][^.]*\.[a-z][^.]*\.(?:\s|$))', desc)
    if not first_sentence_match:
        # 尝试匹配到 ". " 处的第一个合理断句（至少15字符）
        first_sentence_match = re.match(r'(.{15,}?\.\s)', desc)
    if not first_sentence_match:
        # 备选：到 ". Use" / ". NOT" / ". Also" 等模式处截断
        first_sentence_match = re.match(r'(.+?\.)\s+(?:Use|NOT|Also|When|Supports?|Activ)', desc)
    core_sentence = first_sentence_match.group(1).strip().rstrip('.') if first_sentence_match else ''

    # 2. 保留 "Activate when user mentions:" 关键词
    activate_match = re.search(r'Activate when user mentions?:\s*(.+?)(?:\.\s*$|\.\s*[A-Z])', desc)
    activate_keywords = activate_match.group(1).strip().rstrip('.') if activate_match else ''

    # 3. 保留 "Triggers:" / "Trigger phrases:" 关键词
    triggers_match = re.search(r'Trigger(?:s)? phrases?:\s*"(.+?)"', desc)
    if not triggers_match:
        triggers_match = re.search(r'Trigger(?:s)?:\s*"(.+?)"', desc)
    triggers = triggers_match.group(1).strip() if triggers_match else ''

    # 4. 保留 "NOT for:" 排除条件（但只保留精简版，不超过100字符）
    not_for_match = re.search(r'NOT for:\s*(.+?)(?:\.\s|$)', desc)
    not_for = ''
    if not_for_match:
        not_for_raw = not_for_match.group(1).strip().rstrip('.')
        if len(not_for_raw) > 100:
            # 只保留前3个排除项
            items = re.split(r',\s*(?:or|and)\s*', not_for_raw)
            not_for = 'NOT for: ' + ', '.join(items[:3])
            if len(items) > 3:
                not_for += ', etc.'
        else:
            not_for = f'NOT for: {not_for_raw}'

    # 组装
    if core_sentence and len(core_sentence) > 15:
        result_parts.append(core_sentence)
    if activate_keywords:
        result_parts.append(activate_keywords)
    if triggers and not activate_keywords:
        result_parts.append(triggers)

    # 如果核心句子和关键词都不够，用 Use when
    if not result_parts:
        use_when_match = re.search(r'(?:Activates?|Use) when (?:the )?user mentions?:\s*(.+?)(?:\.\s|$)', desc)
        if use_when_match:
            result_parts.append(use_when_match.group(1).strip().rstrip('.'))

    # NOT for 放最后（作为补充而非主体）
    if not_for:
        result_parts.append(not_for)

    # 最终兜底
    if not result_parts:
        fallback = desc.split('.')[0] if '.' in desc else desc
        if len(fallback) > 200:
            fallback = fallback[:200] + "..."
        result_parts.append(fallback)

    slim = " ".join(result_parts)

    # 硬限制：不超过 150 字符
    if len(slim) > 150:
        # 优先保留核心句 + NOT for，砍掉触发关键词
        if core_sentence and len(core_sentence) > 15:
            slim = core_sentence + ('. ' + not_for if not_for else '')
        if len(slim) > 150:
            # 在句号处截断，避免句子不完整
            truncated = slim[:147]
            last_period = max(truncated.rfind('.'), truncated.rfind('。'), truncated.rfind('：'))
            if last_period > 50:  # 确保至少保留有意义的内容
                slim = slim[:last_period + 1]
            else:
                slim = truncated + "..."

    return slim


def scan_all_skills():
    """扫描所有技能目录，返回去重后的技能列表"""
    seen = {}
    for d in SKILL_DIRS:
        if not d.exists():
            continue
        for name in sorted(os.listdir(d)):
            skill_path = d / name / "SKILL.md"
            if not skill_path.exists():
                continue
            if name in seen:
                continue  # 高优先级已覆盖
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                parsed = parse_frontmatter(content)
                if parsed[0]:
                    seen[name] = {
                        'path': skill_path,
                        'content': content,
                        'name': parsed[0],
                        'raw_desc': parsed[1] or '',
                    }
            except Exception as e:
                print(f"⚠️ 读取失败: {skill_path}: {e}")
    return seen


def fmt_tokens(chars):
    """估算 token 数"""
    return f"~{chars // 4}"


def cmd_report(skills):
    """输出技能 token 消耗报告"""
    print("🦞 龙虾医生 — 技能 Token 消耗报告\n")

    total_original = 0
    total_slim = 0
    stats = []

    for name, info in sorted(skills.items(), key=lambda x: -len(x[1]['raw_desc'])):
        raw = info['raw_desc']
        clean = raw.strip().strip('"\'')
        # 处理多行
        clean = re.sub(r'^\s*>\s*', '', clean, flags=re.MULTILINE).strip()
        clean = re.sub(r'\s+', ' ', clean)

        slim = clean_description(info['raw_desc']) if name not in CORE_SKILLS else clean

        orig_chars = len(clean)
        slim_chars = len(slim)
        saved = orig_chars - slim_chars
        pct = (saved / orig_chars * 100) if orig_chars > 0 else 0

        total_original += orig_chars
        total_slim += slim_chars

        stats.append({
            'name': name,
            'orig': orig_chars,
            'slim': slim_chars,
            'saved': saved,
            'pct': pct,
            'slim_desc': slim,
            'path': info['path'],
            'protected': name in CORE_SKILLS,
        })

    # 汇总
    print(f"{'名称':35s} {'原始':>6s} {'精简后':>6s} {'节省':>6s} {'比例':>6s}")
    print("─" * 65)

    for s in stats:
        marker = "🔒" if s['protected'] else ("  " if s['saved'] > 0 else "  ")
        print(f"{marker}{s['name']:33s} {s['orig']:5d}c {s['slim']:5d}c {s['saved']:+5d}c {s['pct']:5.0f}%")

    print("─" * 65)
    total_saved = total_original - total_slim
    total_pct = (total_saved / total_original * 100) if total_original > 0 else 0
    print(f"{'合计':35s} {total_original:5d}c {total_slim:5d}c {total_saved:+5d}c {total_pct:5.0f}%")
    print()
    print(f"📊 原始注入估算: {fmt_tokens(total_original)} tokens")
    print(f"📊 精简后注入估算: {fmt_tokens(total_slim)} tokens")
    print(f"💰 每轮对话节省: {fmt_tokens(total_saved)} tokens")
    print()

    # XML 开销估算
    xml_overhead = sum(len(s['name']) + len(str(s['path'])) + 80 for s in stats)
    total_with_xml = total_original + xml_overhead
    slim_with_xml = total_slim + xml_overhead
    print(f"📋 含 XML 标签开销:")
    print(f"   原始: {fmt_tokens(total_with_xml)} tokens")
    print(f"   精简: {fmt_tokens(slim_with_xml)} tokens")


def cmd_dry_run(skills):
    """预览精简效果"""
    print("🦞 龙虾医生 — 技能瘦身预览 (--dry-run)\n")
    print("─" * 70)

    for name, info in sorted(skills.items(), key=lambda x: -len(x[1]['raw_desc'])):
        if name in CORE_SKILLS:
            continue

        raw = info['raw_desc'].strip().strip('"\'')
        clean = re.sub(r'^\s*>\s*', '', raw, flags=re.MULTILINE).strip()
        clean = re.sub(r'\s+', ' ', clean)

        slim = clean_description(info['raw_desc'])

        if len(clean) == len(slim):
            continue  # 无变化则不显示

        print(f"\n🔧 {name}")
        print(f"   原文 ({len(clean)}c): {clean[:120]}{'...' if len(clean)>120 else ''}")
        print(f"   精简 ({len(slim)}c): {slim}")
        print()

    print("─" * 70)
    print("💡 运行 `skill_slim.py apply` 应用精简（会修改 SKILL.md）")


def cmd_apply(skills):
    """应用精简"""
    print("🦞 龙虾医生 — 技能瘦身执行中...\n")

    modified = 0
    backup_dir = WORKSPACE / ".cleanup-backup" / "skill-slim"

    for name, info in sorted(skills.items()):
        if name in CORE_SKILLS:
            continue

        slim = clean_description(info['raw_desc'])
        content = info['content']

        # 检查是否需要修改
        raw_clean = info['raw_desc'].strip().strip('"\'')
        raw_clean = re.sub(r'^\s*>\s*', '', raw_clean, flags=re.MULTILINE).strip()
        raw_clean = re.sub(r'\s+', ' ', raw_clean)

        if len(raw_clean) <= len(slim):
            continue

        # 备份
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"{name}_SKILL.md"
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 替换 description
        # 找到 description 行并替换
        old_fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not old_fm_match:
            continue

        old_fm = old_fm_match.group(1)
        new_fm = re.sub(
            r'^description:.*$',
            f'description: {slim}',
            old_fm,
            flags=re.MULTILINE
        )

        new_content = content[:old_fm_match.start()] + f"---\n{new_fm}\n---" + content[old_fm_match.end():]

        # 写入
        try:
            with open(info['path'], 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified += 1
            print(f"  ✅ {name}: {len(raw_clean)}c → {len(slim)}c")
        except Exception as e:
            print(f"  ❌ {name}: 写入失败 - {e}")

    print(f"\n{'='*50}")
    print(f"🔧 已精简 {modified} 个技能")
    print(f"📦 备份位置: {backup_dir}")
    print()
    print("⚠️ 请重启 OpenClaw 使更改生效:")
    print("   systemctl --user restart openclaw-gateway.service")


def cmd_duplicates(skills):
    """扫描功能相似的重复技能"""
    import difflib

    print("🦞 龙虾医生 — 重复技能检测\n")

    names = list(skills.keys())
    descs = {}
    for name, info in skills.items():
        raw = info['raw_desc'].strip().strip('"\'')
        raw = re.sub(r'^\s*>\s*', '', raw, flags=re.MULTILINE).strip()
        raw = re.sub(r'\s+', ' ', raw)
        # 提取核心关键词用于比较
        slim = clean_description(info['raw_desc'])
        descs[name] = {
            'desc': raw,
            'slim': slim,
            'keywords': set(re.findall(r'[\w]+', slim.lower()))
        }

    # 已知的重复技能对（手动维护的规则库）
    KNOWN_DUPLICATES = [
        ("github", "github-ops", "GitHub 操作"),
        ("market-research", "nero-market-research", "市场调研"),
        ("news-briefing", "news-summary", "新闻摘要"),
        ("news-briefing", "news-aggregator", "新闻聚合"),
        ("news-summary", "news-aggregator", "新闻聚合"),
        ("stock-analysis", "stock-monitor", "股票分析"),
        ("nano-banana-pro", "ai-nano-banana-ima", "Nano Banana 生图"),
        ("find-skills", "ocms-ai-prompt-generator", "技能/提示词发现"),
        ("deep-research-pro", "competitor-research", "深度研究"),
        ("blog-writer", "ai-prompt-engineering-safety-review", "写作/提示词优化"),
    ]

    print("📋 已知重复技能对:\n")
    known_found = []
    for a, b, reason in KNOWN_DUPLICATES:
        if a in skills and b in skills:
            known_found.append((a, b, reason))
            a_len = len(descs[a]['desc'])
            b_len = len(descs[b]['desc'])
            waste = a_len + b_len
            print(f"  ⚠️  {a} ↔ {b}")
            print(f"      共同功能: {reason}")
            print(f"      description 总长: {waste} chars (建议禁用一个省 {min(a_len, b_len)} chars)")
            print()

    if not known_found:
        print("  ✅ 未发现已知重复技能对\n")

    # 基于关键词的语义相似度检测
    print("🔍 语义相似度检测 (关键词重叠):\n")
    potential_dupes = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            # 跳过已检测的已知对
            if any((a == x and b == y) or (a == y and b == x) for x, y, _ in known_found):
                continue
            ka = descs[a]['keywords']
            kb = descs[b]['keywords']
            if not ka or not kb:
                continue
            # Jaccard 相似度
            intersection = ka & kb
            union = ka | kb
            if len(union) == 0:
                continue
            similarity = len(intersection) / len(union)
            if similarity >= 0.5 and len(intersection) >= 3:
                potential_dupes.append((a, b, similarity, intersection))

    potential_dupes.sort(key=lambda x: -x[2])
    if potential_dupes:
        for a, b, sim, common in potential_dupes[:15]:
            print(f"  💡 {a} ↔ {b}")
            print(f"      相似度: {sim:.0%}  共同关键词: {', '.join(sorted(common)[:8])}")
            print()
    else:
        print("  ✅ 未发现其他相似技能\n")

    # 汇总建议
    total_waste = sum(
        len(descs[a]['desc']) + len(descs[b]['desc']) for a, b, _ in known_found
    )
    print("=" * 50)
    print(f"📊 检测结果汇总:")
    print(f"   已知重复对: {len(known_found)} 组")
    print(f"   疑似重复对: {len(potential_dupes)} 组")
    if total_waste > 0:
        print(f"   重复技能浪费 description: {total_waste} chars ({fmt_tokens(total_waste)} tokens)")
        print()
        print("💡 建议: 每组重复技能禁用其中一个（保留更新或更活跃的那个）")
        print("   禁用方法: openclaw config set skills.entries.<技能名>.enabled false")
    else:
        print("   ✅ 无重复技能浪费")


def main():
    if len(sys.argv) < 2:
        print("🦞 龙虾医生 — 技能瘦身 (Skill Slim)\n")
        print("命令:")
        print("  report       查看技能 token 消耗报告（不修改）")
        print("  dry-run      预览精简效果（不修改）")
        print("  apply        应用精简（修改 SKILL.md，自动备份）")
        print("  duplicates   检测功能相似的重复技能")
        return

    skills = scan_all_skills()
    if not skills:
        print("❌ 未找到任何技能")
        return

    cmd = sys.argv[1]
    if cmd == "report":
        cmd_report(skills)
    elif cmd == "dry-run":
        cmd_dry_run(skills)
    elif cmd == "apply":
        cmd_apply(skills)
    elif cmd == "duplicates":
        cmd_duplicates(skills)
    else:
        print(f"❌ 未知命令: {cmd}")


if __name__ == "__main__":
    main()
