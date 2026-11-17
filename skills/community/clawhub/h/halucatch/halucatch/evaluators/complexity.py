"""复杂度与可维护性评估：结构指标检测，无需语义理解。"""

import re

# ── 脚本支持相关 ────────────────────────────────────────────────

# SKILL.md 内嵌代码块的语言白名单
CODE_BLOCK_LANGS = frozenset({
    'python', 'py', 'bash', 'sh', 'shell', 'zsh',
    'ruby', 'rb', 'js', 'javascript', 'ts', 'typescript',
    'go', 'golang', 'c', 'cpp', 'c++', 'perl', 'pl',
    'makefile', 'make', 'dockerfile',
})

# 命令行调用模式
CLI_CALL_PAT = re.compile(
    r'(^|\s)('
    r'(python3?|python\s+-m)\s+'
    r'|\./([a-zA-Z0-9_-]+\.(?:py|sh|rb|js|pl|go|ts))'
    r'|bash\s+|sh\s+|node\s+|ruby\s+|go\s+run\s+'
    r'|\bpip\s+(?:install|run)\b'
    r'|\bnpx\s+'
    r'|\bmake\b'
    r')', re.MULTILINE
)

# 步骤模式
STEP_PAT = re.compile(
    r'(?:'
    r'^\s*(?:\d+\.|[-*])\s+'      # 编号列表 1. / - *
    r'|\[[ x]\]\s+'                 # checkbox [ ] / [x]
    r'|(?:步骤|第[一二三四五六七八九十\d]+步|Step\s*\d+|step\s*\d+)'
    r')', re.MULTILINE | re.IGNORECASE
)

# ── 各指标计算 ──────────────────────────────────────────────────

def _count_steps(md):
    """统计 SKILL.md 中的步骤数（仅 ## 指令类标题下）。"""
    if not md:
        return 0
    lines = md.split('\n')
    in_instructions = False
    count = 0
    for line in lines:
        if re.match(r'^## ', line):
            heading = line.lower()
            in_instructions = any(kw in heading for kw in (
                'instruction', 'usage', 'quick', 'steps', 'flow',
                'workflow', 'procedure', '指南', '指令', '步骤', '流程',
                '使用', '快速开始', 'how to', 'getting started', 'setup',
            ))
            continue
        if in_instructions and STEP_PAT.search(line):
            count += 1
    # 如果没找到任何指令章节，全文统计（回退）
    if count == 0:
        count = len(STEP_PAT.findall(md))
    return count


def _count_workflow_steps(md):
    """统计工作流步骤：步骤项中引用了脚本/代码块的。"""
    if not md:
        return 0
    lines = md.split('\n')
    in_instructions = False
    in_step = False
    workflow_lines = []
    step_block = ''
    for line in lines:
        if re.match(r'^## ', line):
            heading = line.lower()
            in_instructions = any(kw in heading for kw in (
                'instruction', 'usage', 'quick', 'steps', 'flow',
                'workflow', 'procedure', '指南', '指令', '步骤', '流程',
                '使用', '快速开始', 'how to', 'getting started', 'setup',
            ))
            continue
        if not in_instructions:
            continue
        if STEP_PAT.search(line):
            if in_step and step_block:
                workflow_lines.append(step_block)
            step_block = line
            in_step = True
        elif in_step and line.strip():
            step_block += '\n' + line
        else:
            in_step = False
            if step_block:
                workflow_lines.append(step_block)
            step_block = ''

    # 尾处理
    if step_block:
        workflow_lines.append(step_block)

    # 筛选：包含脚本引用/代码块的步骤算工作流步骤
    script_signal = re.compile(
        r'(?:'
        r'scripts/|src/|bin/|\[EXEC\]'
        r'|```\w'                                                                   # fenced code block (with lang tag)
        r'|`[^`]*\.(?:py|sh|go|rb|js|ts|pl|R|java|swift|kt)[^`]*`'                 # inline code: `xxx.py`
        r'|`[^`]*(?:python3?|bash|node|ruby|go run|npx|pip)[^`]*`'                 # inline code: `python3 xxx`
        r'|(?:python3?|bash|node|ruby|\./)\s+\S+\.(?:py|sh|go|rb|js|ts|pl|R)'      # plain CLI ref
        r')', re.MULTILINE
    )
    # 回退：如果没找到指令章节，全文统计
    if len(workflow_lines) == 0:
        workflow_lines = []
        for line in lines:
            if STEP_PAT.search(line):
                workflow_lines.append(line)
    return sum(1 for blk in workflow_lines if script_signal.search(blk))


def _count_script_refs(info):
    """统计脚本引用数：scripts/ 文件 + 内嵌代码块 + CLI 调用。"""
    if not info:
        return 0
    count = 0

    # 1) scripts/ 目录下的脚本文件
    if info.get('files'):
        for f in info['files']:
            fp = f.get('path', '') or f.get('name', '')
            # 在 scripts/ 或 src/ 目录下，排除 pycache 和 .pyc
            if ('scripts/' in fp or 'src/' in fp or '/bin/' in fp) and \
               '__pycache__' not in fp and not fp.endswith('.pyc'):
                count += 1

    # 2) SKILL.md 内嵌代码块（分两种）
    md = info.get('skill_md', '') or ''
    if md:
        # 2a) Fenced code blocks ```python\n...```
        fenced = re.findall(r'```(\w*)', md)
        for lang in fenced:
            if lang.lower() in CODE_BLOCK_LANGS:
                count += 1

        # 2b) Inline code: `command` or `path/to/script.py`
        # 匹配 `python3 xxx`、`./script.sh`、`xxx.py` 等 backtick 内的脚本引用
        inline_refs = set()
        for m in re.finditer(r'`([^`]+)`', md):
            content = m.group(1).strip()
            if (re.search(r'(?:python3?|bash|node|ruby|go\s+run|npx|pip|make|\./)\b', content)
                    or re.search(r'\b\w+\.(?:py|sh|go|rb|js|ts|pl|R|java|swift|kt)\b', content)):
                inline_refs.add(content)
        count += len(inline_refs)

    # 3) SKILL.md 中命令行调用
    if md:
        # 去重：同一个脚本被多次引用只算一次
        calls = set()
        for m in CLI_CALL_PAT.finditer(md):
            calls.add(m.group(2).strip())
        count += len(calls)

    return count


def _heading_depth(md):
    """章节深度：最深标题层级 × 2，仅反映最深处。"""
    if not md:
        return 0
    headings = re.findall(r'^(#{2,}) ', md, re.MULTILINE)
    if not headings:
        return 0
    max_depth = max(len(h) for h in headings)
    # h2→0, h3→2, h4→5, h5→8, h6→10
    depth_map = {2: 0, 3: 2, 4: 5, 5: 8, 6: 10}
    return depth_map.get(max_depth, 10)


def _heading_complexity(md):
    """章节复杂度：加权统计所有子标题的分散程度。"""
    if not md:
        return 0
    headings = re.findall(r'^(#{2,}) ', md, re.MULTILINE)
    if not headings:
        return 0
    # h3×1 + h4×2 + h5×3 + h6×4
    total = 0
    for h in headings:
        level = len(h)
        if level >= 3:
            total += (level - 2)  # h3→1, h4→2, h5→3, h6→4
    return min(total / 3, 10)


def _doc_ref_depth(info):
    """文档引用深度：SKILL.md → 文档 → 再引用文档，最高 2 层。"""
    md = info.get('skill_md', '')
    if not md:
        return 0
    doc_exts = r'(?:md|pdf|png|jpg|jpeg|gif|svg|doc|xlsx|csv|txt|yaml|yml|json|toml)'
    refs = re.findall(rf'\[.*?\]\(([^):]+\.{doc_exts})\)', md)
    depth = 1 if refs else 0
    if not depth or not info.get('files'):
        return depth
    for ref in refs:
        ref_content = None
        for f in info['files']:
            fn = f.get('name', '') or f.get('path', '')
            if ref in fn or fn.endswith(ref):
                ref_content = f.get('_content', '')
                break
        if ref_content:
            sub_refs = re.findall(rf'\[.*?\]\(([^):]+\.{doc_exts})\)', ref_content)
            if sub_refs:
                depth = 2
                break
    return depth


def _script_ref_depth(info):
    """脚本引用深度：SKILL.md → 脚本 → 脚本内引用的其他脚本/配置。"""
    md = info.get('skill_md', '')
    if not md:
        return 0
    code_exts = r'(?:py|sh|bash|go|js|ts|rb|rs|pl|R|java|swift|kt)'
    refs = re.findall(
        rf'(?:scripts|src|bin)/(\w+/)*[\w-]+\.{code_exts}|\./[\w/-]+\.{code_exts}|python3?\s+[\w/-]+\.{code_exts}',
        md
    )
    depth = 1 if refs else 0
    return depth


def _doc_ref_breadth(info):
    """文档引用广度：SKILL.md 中 Markdown 链接引用的文档文件数量。"""
    md = info.get('skill_md', '')
    if not md:
        return 0
    doc_exts = r'(?:md|pdf|png|jpg|jpeg|gif|svg|doc|xlsx|csv|txt|yaml|yml|json|toml)'
    return len(re.findall(rf'\[.*?\]\(([^):]+\.{doc_exts})\)', md))


def _script_ref_breadth(info):
    """脚本引用广度：SKILL.md 中引用的脚本路径 + scripts/ 文件数。"""
    md = info.get('skill_md', '') or ''
    code_exts = r'(?:py|sh|bash|go|js|ts|rb|rs|pl|R|java|swift|kt)'
    refs = len(re.findall(
        rf'(?:scripts|src|bin)/(\w+/)*[\w-]+\.{code_exts}|\./[\w/-]+\.{code_exts}|python3?\s+[\w/-]+\.{code_exts}',
        md
    ))
    # 加上 scripts/ 下的实际文件数（更准确）
    scripts_count = 0
    if info.get('files'):
        for f in info['files']:
            fp = f.get('path', '') or f.get('name', '')
            if ('scripts/' in fp or 'src/' in fp or '/bin/' in fp) and \
               '__pycache__' not in fp and not fp.endswith('.pyc'):
                scripts_count += 1
    return refs + scripts_count


def _code_doc_ratio(info):
    """文档占比：SKILL.md 行数 / (代码行数 + SKILL.md 行数)。越高 = 文档越充分。"""
    md = info.get('skill_md', '') or ''
    md_lines = len(md.splitlines()) if md else 0
    if md_lines == 0:
        return 1.0  # 只有代码无文档 → 最差

    code_lines = 0
    py_content = info.get('py', '') or ''
    if py_content:
        for line in py_content.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                code_lines += 1

    total = code_lines + md_lines
    return md_lines / max(total, 1)  # 文档占比


def _redundancy_score(md):
    """重复冗余度：bigram Jaccard 相似度检测 copy-paste 重复内容。"""
    if not md:
        return 0

    # 1. 只保留有意义的正文行（跳过标题/代码/表格/引用/短行）
    lines = []
    for ln in md.splitlines():
        s = ln.strip()
        if not s:
            continue
        first_ch = s[0]
        if first_ch in ('#', '`', '|', '-', '>'):
            continue
        if len(s) < 10:
            continue
        lines.append(s)

    n = len(lines)
    if n < 50:
        return 0

    # 2. 预计算 bigram set
    def _bigrams(s):
        return frozenset(s[i:i + 2] for i in range(len(s) - 1))

    print(f"  📐 重复冗余: {n} 行正文, 预计算 bigram...")
    bg_sets = [_bigrams(ln) for ln in lines]

    # 3. 全量对比 + 进度显示
    dup_lines = set()
    threshold = 0.6
    total_pairs = n * (n - 1) // 2
    pair_idx = 0
    last_pct = -1

    for i in range(n):
        for j in range(i + 1, n):
            pair_idx += 1
            # 每 5% 打印一次进度
            pct = pair_idx * 100 // total_pairs
            if pct >= last_pct + 5:
                print(f"      {pct}% ({pair_idx}/{total_pairs})")
                last_pct = pct

            # Jaccard = |A ∩ B| / |A ∪ B|
            a, b = bg_sets[i], bg_sets[j]
            inter = len(a & b)
            if inter == 0:
                continue
            union = len(a | b)
            if inter / union >= threshold:
                dup_lines.add(i)
                dup_lines.add(j)

    dup_count = len(dup_lines)
    score = min(dup_count / n * 20, 10)
    print(f"    ✅ 完成。{n} 行 → {total_pairs} 对比较 → {dup_count} 行有近似重复 → 得分 {score:.1f}")
    return score


def _table_complexity(md):
    """表格复杂度：按大小分级加权。

    小型表(≤3列 或 ≤2行): 10%    中型表(>3列,>2行,体量<30): 20%
    巨型表(体量≥30):     40%    最宽列: 15%    最大体量: 15%"""
    if not md:
        return 0
    seps = re.findall(r'^\|[-| :]+\|\s*$', md, re.MULTILINE)
    if not seps:
        return 0
    cols_list = [max(len(s.split('|')) - 2, 0) for s in seps]

    # 统计每张表的行数
    sep_positions = [m.start() for m in re.finditer(r'^\|[-| :]+\|\s*$', md, re.MULTILINE)]
    lines = md.split('\n')
    rows_per_table = []
    for i, pos in enumerate(sep_positions):
        line_idx = md[:pos].count('\n')
        next_line = sep_positions[i + 1] if i + 1 < len(sep_positions) else len(md)
        next_idx = md[:next_line].count('\n')
        body_rows = [ln for ln in lines[line_idx + 1:next_idx] if ln.strip().startswith('|')]
        rows_per_table.append(len(body_rows) + 1)

    # 分三类
    small, medium, large = 0, 0, 0
    big_cols, big_sizes = [], []
    for c, r in zip(cols_list, rows_per_table, strict=True):
        size = c * r
        if c <= 3 or r <= 2:
            small += 1
        elif size >= 30:
            large += 1
            big_cols.append(c)
            big_sizes.append(size)
        else:
            medium += 1
            big_cols.append(c)
            big_sizes.append(size)

    # 各项得分
    small_score = min(small / 3, 1) * 10 * 0.10
    medium_score = min(medium / 3, 1) * 10 * 0.20
    large_score = min(large / 2, 1) * 10 * 0.40

    width_score = (min(max(big_cols) / 8, 1) * 10 * 0.15) if big_cols else 0
    size_score = (min(max(big_sizes) / 50, 1) * 10 * 0.15) if big_sizes else 0

    return round(small_score + medium_score + large_score + width_score + size_score, 1)


def _instruction_density(md):
    """指令密度 = (祈使句 + 步骤项 + 代码块 + 条件分支) / 总行数，0-10 归一化。"""
    if not md:
        return 0
    lines = md.splitlines()
    total = max(len(lines), 1)

    # 祈使句：精确匹配——避免「请用/请使用」等示例型问法
    imperatives = len(re.findall(
        r'(?i)(?:'
        r'you\s+(?:should|must|cannot|need|have)\b|'
        r'\b[Mm]ake\s+sure\b|\b[Ee]nsure\b|\b[Dd]o\s+not\b|'
        r'\b[Nn]ever\s+|\b[Aa]lways\s+|'
        r'必须|应该|务必|切勿|禁止|'
        r'请(?:确保|检查|确认|不要|勿|执行|运行|参照|参考|遵循|记录|保存|输出)'
        r')',
        md
    ))
    steps = _count_steps(md)
    code_blocks = len(re.findall(r'```', md)) // 2  # 每对 ``` 算一个块

    # 条件分支：中文 + 英文的 if/else/when/unless 等
    conditionals = len(re.findall(
        r'(?i)(?:'
        r'如果|若[^干]|否则|取决于|视.*而定|'
        r'\bif\s+(?!in\b)\w|\belse\b|\bunless\b|'
        r'\bwhen\s+(?!in\b|it\b|user|running|executing|reading|using|the\b)(?:'
        r'\w+\s+(?:is|has|does|was|can|will|should|\w+s\b)|\w+\s*[=!<>])|'
        r'\bdepending\s+on\b'
        r')',
        md
    ))

    density = (imperatives + steps + code_blocks + conditionals) / total
    return min(density * 100, 10)


# ── 主评估函数 ──────────────────────────────────────────────────

def _score_to_level(score):
    """分数 → 等级映射。"""
    if score <= 3:
        return '🟢 低'
    elif score <= 6:
        return '🟡 中'
    return '🔴 高'


def _script_coverage_ratio(info):
    """计算脚本覆盖比：有脚本引用的步骤数 / 总步骤数。"""
    md = info.get('skill_md', '') or ''
    total_steps = _count_steps(md)
    workflow_steps = _count_workflow_steps(md)  # 有脚本引用的步骤数
    script_refs = _count_script_refs(info)

    # 无步骤 → 跳过
    if total_steps == 0:
        return 0.3, 1.0, total_steps, workflow_steps, script_refs

    ratio = min(workflow_steps / total_steps, 1.0)

    # 折扣 = 1 - √覆盖率（边际递减：第一个脚本降幅最大）
    import math
    multiplier = 1.0 - math.sqrt(ratio)
    coverage_score = 10 * multiplier  # 0-10 分，越高越严重

    return multiplier, ratio, total_steps, workflow_steps, script_refs, coverage_score


def check_complexity(info, skill_type='code-engineered'):
    """复杂度与可维护性评估。

    代码工程型：7 项指标 + 脚本覆盖比乘数
    纯方法论型：5 项指标（无脚本/代码相关），无乘数
    """
    md = info.get('skill_md', '') or ''
    is_code = skill_type == 'code-engineered'

    scores = {}

    # ── 共通指标 ──
    # 1) 章节深度
    hdepth = _heading_depth(md)
    scores['heading_depth'] = {
        'label': '章节深度',
        'value': f'{hdepth:.0f} 分',
        'score': hdepth,
        'level': _score_to_level(hdepth),
    }

    # 2) 章节复杂度
    hcomp = _heading_complexity(md)
    scores['heading_complexity'] = {
        'label': '章节复杂度',
        'value': f'{hcomp:.1f}',
        'score': hcomp,
        'level': _score_to_level(hcomp),
    }

    # 3) 文档引用链深度
    doc_ref_depth_val = _doc_ref_depth(info)
    scores['doc_ref_depth'] = {
        'label': '文档引用链深度',
        'value': f'{doc_ref_depth_val} 层',
        'score': doc_ref_depth_val * 5,
        'level': _score_to_level(doc_ref_depth_val * 5),
    }

    # 4) 文档引用链广度
    doc_ref_breadth = _doc_ref_breadth(info)
    scores['doc_ref_breadth'] = {
        'label': '文档引用链广度',
        'value': f'{doc_ref_breadth} 个',
        'score': min(doc_ref_breadth / 2, 10),
        'level': _score_to_level(min(doc_ref_breadth / 2, 10)),
    }

    # 5) 脚本引用链深度
    script_ref_depth_val = _script_ref_depth(info)
    scores['script_ref_depth'] = {
        'label': '脚本引用链深度',
        'value': f'{script_ref_depth_val} 层',
        'score': script_ref_depth_val * 5,
        'level': _score_to_level(script_ref_depth_val * 5),
    }

    # 6) 脚本引用链广度
    script_ref_breadth = _script_ref_breadth(info)
    scores['script_ref_breadth'] = {
        'label': '脚本引用链广度',
        'value': f'{script_ref_breadth} 个',
        'score': min(script_ref_breadth / 2, 10),
        'level': _score_to_level(min(script_ref_breadth / 2, 10)),
    }

    # 4) 重复冗余度
    redundancy = _redundancy_score(md)
    scores['redundancy'] = {
        'label': '重复冗余',
        'value': f'{redundancy:.1f}',
        'score': redundancy,
        'level': _score_to_level(redundancy),
    }

    # 5) 表格复杂度
    table_score = _table_complexity(md)
    scores['table'] = {
        'label': '表格复杂度',
        'value': f'{table_score:.1f}',
        'score': table_score,
        'level': _score_to_level(table_score),
    }

    # ── 代码工程型专属 ──
    if is_code:
        # 6) 脚本覆盖比（计算但不计入 weighted，用作乘数）
        multiplier, ratio, total_steps, wf_steps, script_count, coverage_score = _script_coverage_ratio(info)
        desc_steps = total_steps - wf_steps
        coverage_pct = f'{ratio:.0%}' if ratio > 0 else '0%'
        coverage_label = (
            '🟢 覆盖充分' if ratio >= 0.5 else (
                '🟡 覆盖不足' if ratio >= 0.25 else (
                    '🟠 覆盖薄弱' if ratio >= 0.1 else '🔴 基本无覆盖'
                )
            )
        )
        scores['coverage'] = {
            'label': '脚本覆盖比',
            'value': f'{coverage_pct} ({wf_steps}/{total_steps} 步有脚本, {desc_steps} 步无) — {coverage_label}',
            'score': coverage_score,
            'level': coverage_label,
            'multiplier': multiplier,
            'ratio': ratio,
            'total_steps': total_steps,
            'workflow_steps': wf_steps,
        }

        # 7) 代码/文档比（代码越少越红——代码型 skill 没代码是硬伤）
        cdr = _code_doc_ratio(info)
        cdr_pct = f'{cdr:.0%}'
        if cdr >= 0.81:
            cdr_score, cdr_label = 9, '🔴 代码稀缺，全靠嘴说'
        elif cdr >= 0.61:
            cdr_score, cdr_label = 6, '🟠 代码偏少，嘴比手多'
        elif cdr >= 0.46:
            cdr_score, cdr_label = 3, '🟡 代码差不多够'
        elif cdr >= 0.31:
            cdr_score, cdr_label = 0, '🟢 代码充足'
        elif cdr >= 0.15:
            cdr_score, cdr_label = 0, '🟢 代码充裕'
        else:
            cdr_score, cdr_label = 0, '🟢 你这是代码仓库啊，兄弟'
        scores['code_doc_ratio'] = {
            'label': '代码/文档比',
            'value': f'文档 {cdr_pct} — {cdr_label}',
            'score': cdr_score,
            'level': cdr_label,
        }

        # 8) 指令密度
        density = _instruction_density(md)
        scores['density'] = {
            'label': '指令密度',
            'value': f'{density:.1f}',
            'score': density,
            'level': _score_to_level(density),
        }

        # ── 加权平均 ──
        weights = {
            'heading_depth': 0.05,
            'heading_complexity': 0.05,
            'doc_ref_depth': 0.10,
            'doc_ref_breadth': 0.10,
            'script_ref_depth': 0.03,
            'script_ref_breadth': 0.02,

            'redundancy': 0.05,
            'table': 0.10,
            'coverage': 0.10,
            'code_doc_ratio': 0.15,
            'density': 0.25,
        }
    else:
        density = _instruction_density(md)
        scores['density'] = {
            'label': '指令密度',
            'value': f'{density:.1f}',
            'score': density,
            'level': _score_to_level(density),
        }

        weights = {
            'heading_depth': 0.10,
            'heading_complexity': 0.07,
            'doc_ref_depth': 0.15,
            'doc_ref_breadth': 0.10,
            'script_ref_depth': 0.03,
            'script_ref_breadth': 0.02,
            'redundancy': 0.15,
            'table': 0.13,
            'density': 0.25,
        }

    # 计算加权平均分
    weighted = sum(scores[k]['score'] * weights.get(k, 0) for k in scores)
    weighted = min(max(weighted, 0), 10)

    # 应用脚本覆盖比乘数（仅代码工程型）
    if is_code and 'coverage' in scores:
        final = weighted * scores['coverage']['multiplier']
    else:
        final = weighted

    # 最终评级
    if final <= 2:
        rating = '🟢 低风险'
    elif final <= 5:
        rating = '🟡 注意'
    else:
        rating = '🔴 复杂'

    # 构建 issues 列表
    issues = []
    for _key, s in scores.items():
        if s['score'] <= 3:
            issues.append((f"✅ {s['label']}: {s['value']}", 'pass'))
        elif s['score'] <= 6:
            issues.append((f"🟡 {s['label']}: {s['value']}", 'warn'))
        else:
            issues.append((f"🔴 {s['label']}: {s['value']}", 'fail'))

    if is_code and 'coverage' in scores:
        r = scores['coverage']
        issues.append(("📋 原始复杂度: " + f"{weighted:.1f}", 'info'))
        ra = r['ratio']
        # 折扣 = 1 - √覆盖率（连续函数，无阶梯档位）
        issues.append((
            f"📋 折扣 ×{r['multiplier']:.2f}（覆盖率 {ra:.0%}，{r['workflow_steps']}/{r['total_steps']} 步有脚本兜底）",
            'info'
        ))
        issues.append(("📋 最终复杂度: " + f"{final:.1f} / 10", 'info'))

    score_display = f'{final:.1f}/10'

    # 注入权重到每个指标
    for key in scores:
        if key in weights:
            scores[key]['weight'] = weights[key]

    return {
        'rating': rating,
        'score': score_display,
        'issues': issues,
        'raw': scores,
        'weighted': weighted,
        'final': final,
    }
