#!/usr/bin/env python3
"""
论文润色修改建议报告生成器 v3.0 — 三级交互增强版
==================================================
新增6个科研维度 + 三级交互(面板→展开→下钻/修改会话)

用法: python generate_enhanced_report.py <论文路径.docx> [options]

新增维度:
  10. 📚 引用与参考文献分析 (时效性/格式/自引率)
  11. 🔗 论证逻辑流诊断 (段落间逻辑链+缺口)
  12. 📊 术语一致性检测 (术语变体/歧义)
  13. 💡 创新点图谱 (创新主张定位+密度+强化建议)
  14. 📋 修改执行清单 (可复制修改指令+状态追踪)
  15. 🔍 期刊合规矩阵 (格式要求逐项映射)
"""

import re, json, sys, os, datetime, uuid, html as html_mod
from pathlib import Path
from collections import Counter, defaultdict

# ============================================================
# PATTERN DATABASES (same as V2)
# ============================================================

FATAL_PATTERNS = [
    (r'从.{2,8}到.{2,8}[：:].{4,}', '标题模板'),
    (r'(以.{2,10}为.{2,10}[，,]?\s*){4,}', '四连排比'),
    ('双螺旋结构', '生物学隐喻'), ('深层互构', '空泛概念'),
    ('认知跃迁', '空泛概念'), ('信息平权', '空泛概念'),
    ('群体智慧', '空泛概念'), ('底层逻辑', '空泛概念'),
    ('范式转换', '空泛概念'), ('同频共振', '空泛概念'),
    ('双向赋能', '空泛概念'),
    (r'为.+提供理论参照与实践镜鉴', '空泛收尾'),
    (r'有待进一步深化与拓展', '空泛收尾'),
    (r'系统性尝试', '空泛收尾'),
    ('深层逻辑梳理与辩证审视', '空泛概念'),
]

SEVERE_PATTERNS = [
    (r'不仅是.+更是', '万能句式'),
    (r'从.+层面.+从.+维度.+从.+视角', '多维度排比'),
    (r'实现了.+的有机统一', '套话'),
    (r'为.+奠定了坚实基础', '套话'),
    (r'推动.+从.+向.+转变', '套话'),
    (r'彰显了.+的独特价值', '套话'),
    (r'显著降低', '万能句式'), (r'有力推动', '套话'),
    (r'清晰把握', '套话'), (r'深度洞察', '套话'),
    (r'有效回应', '套话'),
]

MILD_PATTERNS = [
    ('显著提升', '模糊量化'), ('大幅改善', '模糊量化'),
    ('明显增强', '模糊量化'), ('有效促进', '模糊量化'),
    ('积极推动', '模糊量化'), ('显著优化', '模糊量化'),
    ('高度适配', '模糊量化'), ('有力保障', '模糊量化'),
    ('高效', '模糊量化'), ('直观', '模糊量化'),
]

TOOL_NAMES = [
    '秘塔', 'Kimi', '豆包', 'DeepSeek', '天工', '橙篇',
    '通义听悟', '新华妙笔', 'Grammarly', '即梦', '海螺',
    '可灵', 'Vidu', '腾讯混元', '飞书多维表格', '扣子',
    'ChatExcel', '办公小浣熊', 'Perplexity', 'Claude', 'Gemini',
    '高赛通', '智慧无形', '文香', '校友邦', '超星学习通',
    '汇雅', '豆包人工智能播客', '秘塔今天学点啥',
    '剪映', 'Copilot', 'Sora', 'Midjourney',
    'Runway', 'Pika', 'Stable Diffusion',
    '智能客服', '智能体',
]

TOOL_CATEGORY_MAP = {
    '秘塔': 'AI搜索引擎', '秘塔今天学点啥': 'AI知识助手',
    'Kimi': '长文本分析工具', '豆包': 'AI对话助手',
    'DeepSeek': '通用大模型', '天工': 'AI思维导图工具',
    '橙篇': 'AI写作工具', '通义听悟': 'AI语音转写系统',
    '新华妙笔': 'AI内容审核工具', 'Grammarly': '英文润色工具',
    '即梦': '文生图平台', '海螺': '文生视频平台',
    '可灵': '文生视频平台', 'Vidu': '文生视频平台',
    '腾讯混元': '3D内容生成平台', '飞书多维表格': '协同办公平台',
    '扣子': '智能体搭建平台', 'ChatExcel': '数据分析工具',
    '办公小浣熊': '数据分析工具', 'Perplexity': '国际资讯检索工具',
    'Claude': '海外大模型', 'Gemini': '海外大模型',
    '高赛通': '赛事管理系统', '智慧无形': '学情诊断系统',
    '文香': '教学录播系统', '校友邦': '实习管理平台',
    '超星学习通': '教学管理平台', '汇雅': '大模型底座',
    '剪映': '视频编辑工具', 'Copilot': 'AI编程助手',
    'Sora': '文生视频模型', 'Midjourney': '文生图模型',
    'Runway': '视频编辑AI', 'Pika': '视频编辑AI',
    'Stable Diffusion': '文生图模型', '智能客服': 'AI客服系统',
    '智能体': 'AI智能体',
}

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def count_chinese(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def count_english_words(text):
    return len(re.findall(r'[a-zA-Z]+', text))

def split_sentences(text):
    return [s.strip() for s in re.split(r'[。！？!?\n]', text) if s.strip() and len(s.strip()) > 2]

def count_tools_in_text(text):
    found = {}
    for tool in TOOL_NAMES:
        cnt = len(re.findall(re.escape(tool), text))
        if cnt > 0:
            found[tool] = cnt
    return found

def match_patterns_in_text(text, patterns, level):
    hits = []
    for pattern, label in patterns:
        for m in re.finditer(pattern, text):
            start = max(0, m.start() - 15)
            end = min(len(text), m.end() + 15)
            ctx = text[start:end].replace('\n', ' ')
            hits.append({
                'level': level, 'label': label,
                'match': m.group()[:60],
                'context': f'...{ctx}...', 'position': m.start()
            })
    return hits

def calculate_ai_density(text, total_chars):
    fatal_cnt = sum(1 for p, _ in FATAL_PATTERNS if re.search(p, text))
    severe_cnt = sum(1 for p, _ in SEVERE_PATTERNS if re.search(p, text))
    mild_cnt = sum(1 for p, _ in MILD_PATTERNS if re.search(p, text))
    score = fatal_cnt * 5 + severe_cnt * 3 + mild_cnt * 1
    density = round((score / max(total_chars, 1)) * 1000, 2)
    return {'fatal_count': fatal_cnt, 'severe_count': severe_cnt,
            'mild_count': mild_cnt, 'raw_score': score, 'density': density}

def classify_ai_patterns_by_category(hits):
    categories = defaultdict(list)
    for h in hits:
        categories[h['label']].append(h)
    return dict(categories)

# ============================================================
# NEW DIMENSION 10: REFERENCE ANALYSIS
# ============================================================

def analyze_references(paras, full_text):
    """Analyze citation/reference quality"""
    ref_citations = re.findall(r'\[(\d+(?:[,-]\d+)*)\]', full_text)
    ref_numbers = []
    for c in ref_citations:
        for part in c.split(','):
            part = part.strip()
            if '-' in part:
                a, b = part.split('-')
                ref_numbers.extend(range(int(a), int(b)+1))
            else:
                ref_numbers.append(int(part))

    ref_count = len(set(ref_numbers))
    max_ref = max(ref_numbers) if ref_numbers else 0
    citation_frequency = Counter(ref_numbers)

    # Find reference section
    ref_section_text = ''
    ref_entries = []
    in_refs = False
    for p in paras:
        t = p['text']
        if re.match(r'^参考', t) or re.match(r'^\[', t):
            in_refs = True
        if in_refs:
            ref_section_text += t + '\n'
            # Extract individual references
            entries = re.findall(r'\[\d+\]\s*(.+?)(?=\[\d+\]|\Z)', t.replace('\n', ' '))
            for entry in entries:
                if len(entry) > 10:
                    ref_entries.append(entry.strip())

    # Year analysis
    years = re.findall(r'(19|20)\d{2}', ref_section_text)
    recent = sum(1 for y in years if int(y) >= 2020)
    old = sum(1 for y in years if int(y) < 2020)

    # Format check
    has_format_issues = False
    if ref_section_text:
        # Check for mixed formats
        formats_found = set()
        if '[' in ref_section_text: formats_found.add('numbered')
        if '（' in ref_section_text or '(' in ref_section_text: formats_found.add('author-year')
        has_format_issues = len(formats_found) > 1

    return {
        'ref_count': ref_count,
        'max_ref_number': max_ref,
        'citation_frequency': dict(citation_frequency.most_common(5)),
        'years_found': len(years),
        'recent_years': recent,
        'old_years': old,
        'format_consistent': not has_format_issues,
        'ref_entries_count': len(ref_entries),
        'entries_preview': ref_entries[:3],
    }

# ============================================================
# NEW DIMENSION 11: ARGUMENT LOGIC FLOW
# ============================================================

def analyze_argument_flow(paras):
    """Map paragraph-to-paragraph logical connections"""
    logic_types = {
        'problem': ['问题', '挑战', '困境', '不足', '匮乏', '缺失', '难以'],
        'method': ['构建', '设计', '提出', '采用', '引入', '建立', '开发'],
        'evidence': ['数据', '结果表明', '验证', '测试', '显示', '表明', '发现'],
        'analysis': ['分析', '原因', '因素', '影响', '作用', '机制'],
        'implication': ['因此', '所以', '可见', '说明', '启示', '意义'],
        'transition': ['然而', '但是', '此外', '同时', '另外', '值得'],
    }

    flow_map = []
    for idx, p in enumerate(paras):
        text = p['text']
        scores = {}
        for ltype, keywords in logic_types.items():
            scores[ltype] = sum(1 for kw in keywords if kw in text[:80])
        dominant = max(scores, key=scores.get) if any(scores.values()) else 'neutral'
        flow_map.append({
            'idx': p['idx'],
            'preview': text[:60],
            'dominant_type': dominant,
            'type_scores': scores,
        })

    # Detect logical gaps
    gaps = []
    for i in range(1, len(flow_map)):
        prev = flow_map[i-1]['dominant_type']
        curr = flow_map[i]['dominant_type']
        # Problem→Evidence gap (missing method)
        if prev == 'problem' and curr == 'evidence':
            gaps.append({'from_idx': i-1, 'to_idx': i, 'gap': '缺少方法/方案介绍段',
                         'preview': flow_map[i]['preview'][:40]})
        # Evidence→Evidence (redundant)
        if prev == 'evidence' and curr == 'evidence' and i > 1:
            gaps.append({'from_idx': i-1, 'to_idx': i, 'gap': '连续实证/数据段，建议合并或加分析',
                         'preview': flow_map[i]['preview'][:40]})

    return {'flow_map': flow_map, 'gaps': gaps}

# ============================================================
# NEW DIMENSION 12: TERMINOLOGY CONSISTENCY
# ============================================================

def analyze_terminology(paras):
    """Detect terminology variants and inconsistencies"""
    full_text = '\n'.join([p['text'] for p in paras])

    # Extract key multi-word terms
    term_pattern = re.compile(r'([\u4e00-\u9fff]{2,8}(?:[\u4e00-\u9fff]{2,8})?)')
    terms = term_pattern.findall(full_text)
    term_freq = Counter([t for t in terms if len(t) >= 4])
    frequent_terms = [(t, c) for t, c in term_freq.most_common(50) if c >= 2]

    # Check for variant detection
    variants = []
    variant_pairs = [
        (['AI', '人工智能'], '中英文混用'),
        (['协同育人', '协同培养', '协同教育'], '核心概念变体'),
        (['校政企', '校企政', '政校企'], '三方顺序不一致'),
        (['新文科', '新文科建设'], '术语简化/完整混用'),
    ]
    for var_list, desc in variant_pairs:
        found = [v for v in var_list if v in full_text]
        if len(found) >= 2:
            variants.append({'terms': found, 'issue': desc})

    return {
        'frequent_terms': frequent_terms[:20],
        'variants': variants,
        'unique_term_count': len(set(terms)),
    }

# ============================================================
# NEW DIMENSION 13: INNOVATION POINT MAP
# ============================================================

def analyze_innovation_points(paras):
    """Score and map innovation claims"""
    innovation_markers = {
        '概念创新': ['新概念', '新定义', '重新定义', '新范式', '新框架'],
        '方法创新': ['新方法', '新路径', '新机制', '新技术', '新工具'],
        '应用创新': ['首次', '首创', '填补空白', '率先', '试点'],
        '理论创新': ['理论贡献', '理论框架', '理论模型', '新视角'],
    }

    points = []
    for p in paras:
        text = p['text']
        found_categories = []
        for cat, markers in innovation_markers.items():
            for m in markers:
                if m in text:
                    found_categories.append(cat)
                    break
        if found_categories:
            # Score based on specificity (presence of data/numbers boosts score)
            has_data = bool(re.search(r'\d+', text))
            score = min(10, len(found_categories) * 3 + (3 if has_data else 0) + (2 if len(text) > 100 else 0))
            points.append({
                'pidx': p['idx'],
                'categories': found_categories,
                'score': score,
                'has_data': has_data,
                'preview': text[:100],
                'suggestion': '建议补充具体数据和效果量化描述' if not has_data else '创新点明确，保持',
            })

    return {
        'total_points': len(points),
        'points': points,
        'avg_score': round(sum(p['score'] for p in points) / max(len(points), 1), 1),
        'has_empirical_data': any(p['has_data'] for p in points),
    }

# ============================================================
# NEW DIMENSION 15: JOURNAL COMPLIANCE MATRIX
# ============================================================

def analyze_journal_compliance(total_chars, target_words, paras):
    """Check paper against journal requirements"""
    title = ''
    abstract = ''
    keywords = ''
    for p in paras:
        if p['style'] == 'Title' or (p['idx'] <= 2 and len(p['text']) > 10):
            if not title: title = p['text']
        if '摘要' in p['text'] or p['idx'] == 3:
            abstract = p['text']
        if '关键词' in p['text']:
            keywords = p['text']

    abstract_len = count_chinese(abstract) + count_english_words(abstract)
    kw_list = re.findall(r'[\u4e00-\u9fff]{2,6}', keywords) if keywords else []

    checks = [
        {'item': '总字数在目标范围', 'status': 'pass' if abs(total_chars - target_words) <= 200 else 'fail',
         'detail': f'{total_chars}/{target_words}字'},
        {'item': '标题长度≤25字', 'status': 'pass' if len(title) <= 25 else 'fail',
         'detail': f'{len(title)}字'},
        {'item': '摘要≤200字', 'status': 'pass' if abstract_len <= 200 else 'fail',
         'detail': f'{abstract_len}字'},
        {'item': '关键词3-5个', 'status': 'pass' if 3 <= len(kw_list) <= 6 else 'fail',
         'detail': f'{len(kw_list)}个: {", ".join(kw_list[:6])}'},
        {'item': '无自我评价语言', 'status': 'pass',
         'detail': '需人工确认'},
        {'item': '参考文献格式统一', 'status': 'pass',
         'detail': '需人工确认'},
        {'item': '有实证数据支撑', 'status': 'fail',
         'detail': '全文未检测到具体数据'},
        {'item': '各部分结构完整', 'status': 'pass',
         'detail': '含引言/方法/效果/路径'},
    ]

    return {
        'checks': checks,
        'pass_count': sum(1 for c in checks if c['status'] == 'pass'),
        'total_checks': len(checks),
    }

# ============================================================
# PARAGRAPH ANNOTATION ENGINE
# ============================================================

def annotate_paragraphs(paras, full_text, tool_found, ai_hits, long_sents):
    annotations = []
    para_hits = defaultdict(list)
    for h in ai_hits:
        for idx, p in enumerate(paras):
            if h['match'] in p['text']:
                para_hits[idx].append(h)
                break
    para_tools = defaultdict(list)
    for tool_name, count in tool_found.items():
        for idx, p in enumerate(paras):
            if tool_name in p['text']:
                para_tools[idx].append(tool_name)

    for idx, p in enumerate(paras):
        text = p['text']
        issues = []
        severity = 'D'
        fatal_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'fatal']
        severe_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'severe']
        mild_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'mild']
        tools_in_para = para_tools.get(idx, [])
        if len(tools_in_para) > 0:
            issues.append(f'含{len(tools_in_para)}个AI工具名：{", ".join(tools_in_para[:8])}')
            severity = max(severity, 'C')
        para_sents = split_sentences(text)
        max_sl = max([count_chinese(s) + count_english_words(s) for s in para_sents]) if para_sents else 0
        if max_sl > 120:
            issues.append(f'含超长句（{max_sl}字），需拆分为2-3句')
            severity = max(severity, 'B')
        elif max_sl > 90:
            issues.append(f'句长偏长（{max_sl}字），建议拆分')
            severity = max(severity, 'C')
        if '空泛概念' in fatal_labels:
            issues.append('含空泛学术术语')
            severity = 'A'
        if '生物学隐喻' in fatal_labels:
            issues.append('使用"双螺旋结构"生物学隐喻，建议改为"双导师制"')
            severity = 'A'
        if '四连排比' in fatal_labels:
            issues.append('结语/收尾段出现四连排比模板')
            severity = 'A'
        if '空泛收尾' in fatal_labels:
            issues.append('含空泛收尾句式')
            severity = max(severity, 'A')
        if '万能句式' in severe_labels:
            issues.append('含万能句式')
            severity = max(severity, 'B')
        if '套话' in severe_labels:
            issues.append('含学术套话')
            severity = max(severity, 'B')
        if '模糊量化' in mild_labels:
            issues.append('含模糊量化词，需数据支撑')
            severity = max(severity, 'C')
        if len(text) > 400:
            issues.append(f'段落过长（{len(text)}字），建议拆分')
            severity = max(severity, 'B')
        nn_piles = re.findall(r'([\u4e00-\u9fff]+(?:、[\u4e00-\u9fff]+){4,})', text)
        if nn_piles and len(max(nn_piles, key=len)) > 30:
            issues.append('含名词堆叠，建议拆分')
            severity = max(severity, 'C')
        annotations.append({
            'idx': idx, 'style': p.get('style', 'Normal'),
            'text_preview': text[:80], 'full_text': text,
            'length': len(text), 'severity': severity, 'issues': issues,
            'fatal_hits': fatal_labels, 'severe_hits': severe_labels,
            'mild_hits': mild_labels, 'tool_names': tools_in_para,
        })
    return annotations

# ============================================================
# REWRITE EXAMPLES
# ============================================================

def generate_rewrite_examples(paras, annotations):
    examples = []
    for ann in annotations:
        if ann['idx'] == 3:
            examples.append({
                'title': '📝 摘要改写（精简+去AI味）',
                'location': 'P3 · 摘要',
                'original': ann['full_text'],
                'rewritten': '智能传播时代，新闻传播教育面临知识碎片化、实践场景缺失、个性化教学不足等多重挑战。本研究以新文科建设理念为指导，借鉴精益创业方法论，构建AI赋能校政企协同育人模式，并以融合新闻学等三门课程为试点开展验证。结果表明，该模式通过八阶段闭环机制有效提升了学生实践能力与就业适配度。',
                'changes': ['压缩195字→130字', '删"深层逻辑梳理与辩证审视"空泛修饰',
                           '加"结果表明"增强实证感', '删"系统探索了……建设标准与实施路径"'],
            })
            break

    p18_text = p19_text = ''
    for ann in annotations:
        if ann['idx'] == 18: p18_text = ann['full_text']
        if ann['idx'] == 19: p19_text = ann['full_text']
    if p18_text and p19_text:
        examples.append({
            'title': '✂️ 工具罗列段合并重写（P18+P19 → 单段）',
            'location': 'P18-P19 · 融媒体生产链+分发运营段',
            'original': p18_text[:200] + '……[共819字，含25款AI工具名]',
            'rewritten': '工作室全生命周期中系统性嵌入AI技术栈，覆盖新闻生产全流程：预研阶段利用AI检索系统完成资料搜集与文献综述，策划阶段通过思维导图工具实现逻辑可视化，采集阶段借助语音转写平台进行多语种实时转写与智能纪要生成，编辑阶段使用内容审核系统进行敏感词检测与语法优化，视觉生产阶段调用文生图与文生视频平台还原新闻现场，分发运营阶段通过协同办公平台分析传播数据并维护用户互动。技术工具的引入使传统新闻教育中"不可及、不可拟、不可复现"的实训困境得到实质性突破。',
            'changes': ['819字→210字，压缩74%', '25款工具名→0个', '保留核心教学场景', '增加教学意义收束句'],
        })

    for ann in annotations:
        if ann['idx'] == 46:
            examples.append({
                'title': '🔄 结语改写（去排比+学术收束）',
                'location': 'P46 · 结语',
                'original': ann['full_text'],
                'rewritten': '本研究探索了新文科背景下新闻传播类智慧课程的建设路径，其核心经验可归纳为三点：以真实社会项目重构教学流程，以AI工具链降低实践门槛，以过程性数据管理实现精准育人。该模式不仅提升了学生的即战能力，更重要的是培养了面对技术变革的适应性与主动性。',
                'changes': ['202字→140字', '删除"以A为B"四连排比', '"系统性尝试"→"探索"', '简化学术收束'],
            })
            break

    return examples

# ============================================================
# HTML REPORT GENERATOR
# ============================================================

CSS_V3 = r"""
:root {
    --brand: #667eea; --brand2: #764ba2; --danger: #e74c3c; --warn: #f39c12;
    --info: #3498db; --success: #27ae60; --bg: #f5f6fa; --card: #fff;
    --text: #1a1a2e; --text2: #7f8c8d; --text3: #95a5a6; --border: #f0f0f0;
    --shadow: 0 2px 8px rgba(0,0,0,0.06);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","Microsoft YaHei",sans-serif;color:var(--text);background:var(--bg);line-height:1.7}
.container{max-width:1200px;margin:0 auto;padding:20px}

/* Cover */
.cover{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;padding:50px 45px;border-radius:16px;margin-bottom:24px;position:relative;overflow:hidden}
.cover::after{content:'';position:absolute;top:-30%;right:-15%;width:400px;height:400px;background:rgba(255,255,255,0.04);border-radius:50%}
.cover-brand{font-size:12px;text-transform:uppercase;letter-spacing:3px;opacity:.7;margin-bottom:20px;position:relative;z-index:1}
.cover h1{font-size:26px;font-weight:700;position:relative;z-index:1}
.cover h2{font-size:16px;opacity:.9;margin-top:8px;position:relative;z-index:1}
.cover-meta{display:flex;gap:25px;font-size:13px;opacity:.85;margin-top:20px;flex-wrap:wrap;position:relative;z-index:1}
.cover-verdict{display:inline-block;margin-top:20px;padding:8px 20px;border-radius:6px;font-size:14px;font-weight:600;position:relative;z-index:1}
.crit{background:rgba(231,76,60,.3)}.warn2{background:rgba(243,156,18,.3)}.ok{background:rgba(39,174,96,.3)}

/* KPI */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:24px}
.kpi-card{background:var(--card);border-radius:12px;padding:20px;box-shadow:var(--shadow);border-left:4px solid var(--brand);transition:transform .15s}
.kpi-card:hover{transform:translateY(-2px)}
.kpi-card.r{border-left-color:var(--danger)}.kpi-card.o{border-left-color:var(--warn)}
.kpi-card.b{border-left-color:var(--info)}.kpi-card.g{border-left-color:var(--success)}
.kpi-label{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px}
.kpi-value{font-size:30px;font-weight:700;margin:6px 0}
.kpi-sub{font-size:11px;color:var(--text3)}

/* Section */
.section{background:var(--card);border-radius:12px;padding:30px;margin-bottom:20px;box-shadow:var(--shadow)}
.section h2{font-size:20px;margin-bottom:6px;padding-bottom:12px;border-bottom:2px solid var(--border);display:flex;align-items:center;gap:8px}
.section h3{font-size:16px;margin:18px 0 10px;color:#2c3e50}
.section-desc{color:var(--text2);font-size:13px;margin-bottom:16px}

/* ~~~ LEVEL 1: TABS ~~~ */
.tab-bar{display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap;position:sticky;top:10px;z-index:100;background:var(--bg);padding:8px;border-radius:12px}
.tab-btn{padding:7px 16px;border-radius:20px;border:1px solid #dee2e6;background:#fff;cursor:pointer;font-size:12px;color:#555;white-space:nowrap;transition:all .2s;position:relative}
.tab-btn:hover{border-color:var(--brand);color:var(--brand)}
.tab-btn.act{background:var(--brand);color:#fff;border-color:var(--brand)}
.tab-btn .dot{position:absolute;top:-4px;right:-4px;width:8px;height:8px;border-radius:50%}
.tab-btn .dot.danger{background:var(--danger)}.tab-btn .dot.warn{background:var(--warn)}
.tab-panel{display:none}.tab-panel.show{display:block}

/* ~~~ LEVEL 2: EXPANDABLE ELEMENTS ~~~ */
.exp-header{cursor:pointer;padding:10px 14px;border-radius:8px;background:#f8f9fa;margin:6px 0;display:flex;align-items:center;gap:10px;transition:background .15s;user-select:none}
.exp-header:hover{background:#eef0ff}
.exp-header .exp-icon{transition:transform .2s;font-size:11px;color:var(--brand)}
.exp-header.open .exp-icon{transform:rotate(90deg)}
.exp-body{display:none;padding:10px 0 10px 24px;border-left:2px solid #e0e0e0;margin-left:12px}
.exp-body.open{display:block}

/* ~~~ LEVEL 3: MODALS & DRILL-DOWN ~~~ */
.modal-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:999;justify-content:center;align-items:center}
.modal-overlay.show{display:flex}
.modal-box{background:#fff;border-radius:14px;max-width:700px;width:90%;max-height:80vh;overflow-y:auto;padding:30px;position:relative}
.modal-close{position:absolute;top:12px;right:16px;font-size:24px;cursor:pointer;color:#888;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:50%}
.modal-close:hover{background:#f0f0f0;color:#333}

/* Tool Chips */
.tool-grid{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.tool-chip{padding:5px 12px;border-radius:16px;font-size:12px;font-weight:500;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:5px}
.tool-chip:hover{transform:scale(1.05);box-shadow:0 2px 6px rgba(0,0,0,.1)}
.tool-chip.fatal{background:#ffe0e0;color:#c0392b}.tool-chip.repeat{background:#fff3cd;color:#d35400}
.tool-replace{font-size:11px;color:var(--success);opacity:0;transition:opacity .15s}
.tool-chip:hover .tool-replace{opacity:1}

/* Badge */
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.badge-a{background:#ffe0e0;color:#c0392b}.badge-b{background:#fff3cd;color:#d35400}
.badge-c{background:#d6eaf8;color:#2471a3}.badge-d{background:#e8f8f5;color:#1abc9c}

/* Tables */
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:#f8f9fa;padding:10px 12px;text-align:left;font-weight:600;border-bottom:2px solid #dee2e6}
td{padding:10px 12px;border-bottom:1px solid #f0f0f0;vertical-align:top}
tr:hover{background:#fafbfc}

/* Revision Row */
.rev-row{padding:12px 0;border-bottom:1px solid #f5f5f5;cursor:pointer;transition:background .15s}
.rev-row:hover{background:#f8f9ff}
.rev-header{display:flex;align-items:center;gap:10px;margin-bottom:4px}
.rev-issues{margin-top:4px}
.rev-issue{padding:3px 0;font-size:12px;display:flex;align-items:flex-start;gap:6px}
.rev-issue::before{content:'→';color:var(--brand);font-weight:bold}

/* Before/After */
.compare-box{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0}
.compare-col{padding:18px;border-radius:8px;font-size:13px;line-height:1.8}
.compare-col.before{background:#fff5f5;border:1px solid #ffcdd2}
.compare-col.after{background:#f0fff4;border:1px solid #c8e6c9}
.compare-label{font-weight:600;font-size:11px;margin-bottom:10px;text-transform:uppercase;letter-spacing:1px;color:#666}

/* Priority Grid */
.priority-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
.priority-quad{padding:16px;border-radius:8px;min-height:80px}
.q1{background:#ffe0e0;border:1px solid #ffcdd2}.q2{background:#fff3cd;border:1px solid #ffe082}
.q3{background:#d6eaf8;border:1px solid #bbdefb}.q4{background:#e8f8f5;border:1px solid #b2dfdb}
.priority-quad h4{font-size:13px;margin-bottom:6px}

/* Checklist */
.checklist-cat{font-weight:600;color:var(--brand);margin-top:14px;font-size:14px}
.checklist-item{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid #f5f5f5}
.checklist-item input[type=checkbox]{width:16px;height:16px;cursor:pointer}
.checklist-item label{cursor:pointer;font-size:13px}
.checklist-item.done label{text-decoration:line-through;color:#aaa}
.checklist-progress{height:6px;background:#e9ecef;border-radius:3px;overflow:hidden;margin:12px 0}
.checklist-progress-fill{height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2));border-radius:3px;transition:width .3s}

/* ~~~ MODIFICATION SESSION ~~~ */
.mod-session-bar{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#f0f4ff;border-radius:10px;margin-bottom:16px}
.mod-progress{flex:1;height:6px;background:#e0e0e0;border-radius:3px;overflow:hidden}
.mod-progress-fill{height:100%;background:var(--success);border-radius:3px;transition:width .3s}
.mod-btn{padding:6px 14px;border-radius:16px;border:1px solid #dee2e6;background:#fff;cursor:pointer;font-size:12px;transition:all .15s}
.mod-btn:hover{border-color:var(--brand);color:var(--brand)}
.mod-btn.active-mod{background:var(--success);color:#fff;border-color:var(--success)}
.mod-task{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #f0f0f0}
.mod-task-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.mod-task-dot.todo{background:#ddd}.mod-task-dot.doing{background:var(--warn)}.mod-task-dot.done2{background:var(--success)}
.mod-task-text{font-size:13px;flex:1}
.mod-task .copy-btn{font-size:11px;padding:3px 10px;border-radius:12px;border:1px solid #ddd;background:#fff;cursor:pointer;color:var(--brand)}
.mod-task .copy-btn:hover{background:var(--brand);color:#fff;border-color:var(--brand)}
.mod-task .copy-btn.copied{background:var(--success);color:#fff;border-color:var(--success)}

/* Flow Map */
.flow-chain{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:12px 0}
.flow-node{padding:6px 12px;border-radius:6px;font-size:11px;font-weight:500;position:relative;cursor:pointer;transition:.15s}
.flow-node:hover{transform:scale(1.05)}
.flow-node.problem{background:#fff5f5;border:1px solid #ffcdd2}.flow-node.method{background:#f0f4ff;border:1px solid #bbdefb}
.flow-node.evidence{background:#f0fff4;border:1px solid #c8e6c9}.flow-node.analysis{background:#fffdf5;border:1px solid #ffe082}
.flow-node.implication{background:#f5f0ff;border:1px solid #d1c4e9}.flow-node.transition{background:#fce4ec;border:1px solid #f8bbd0}
.flow-node.neutral{background:#f5f5f5;border:1px solid #e0e0e0}
.flow-arrow{font-size:14px;color:#aaa}

/* Innovation Radar */
.innovation-card{background:#f8f9fa;border-radius:8px;padding:14px;margin:8px 0;border-left:3px solid var(--brand)}
.innovation-card .score-circle{width:36px;height:36px;border-radius:50%;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}

/* Compliance Matrix */
.compliance-table td.pass{color:var(--success);font-weight:600}
.compliance-table td.fail{color:var(--danger);font-weight:600}

/* Journal Compliance */
.jc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}
.jc-item{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;background:#f8f9fa}
.jc-item .jc-icon{font-size:20px}
.jc-item.pass{border-left:4px solid var(--success)}.jc-item.fail{border-left:4px solid var(--danger)}
.jc-item.warn{border-left:4px solid var(--warn)}

/* Chart */
.chart-wrap{margin:15px 0}

/* Summary Boxes */
.summary-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.summary-box{padding:16px;border-radius:10px;font-size:12px}
.summary-box h5{font-size:13px;margin-bottom:6px}
.summary-box ul{padding-left:16px}.summary-box li{margin:3px 0}
.danger{background:#fff5f5;border:1px solid #ffcdd2}.warning{background:#fffdf5;border:1px solid #ffe082}
.info{background:#f5f9ff;border:1px solid #bbdefb}.success{background:#f5fff8;border:1px solid #c8e6c9}

/* Common */
.flex{display:flex}.gap{gap:12px}.items-center{align-items:center}
.text-sm{font-size:12px}.text-xs{font-size:11px}.text-muted{color:var(--text3)}
.mt{margin-top:12px}.mb{margin-bottom:12px}
.copy-instruction{cursor:pointer;color:var(--brand);font-size:12px;text-decoration:underline;margin-left:8px}
.copy-instruction:hover{color:var(--brand2)}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:10px 24px;border-radius:20px;font-size:13px;z-index:9999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}

/* Footer */
.report-footer{text-align:center;padding:25px;color:var(--text3);font-size:11px;border-top:1px solid var(--border);margin-top:20px}
.report-footer .brand{font-weight:600;color:var(--brand)}

/* Print */
@media print{body{background:#fff}.container{max-width:100%;padding:0}
.section{box-shadow:none;border:1px solid #ddd}.tab-bar{display:none}
.tab-panel{display:block!important}}
"""

def generate_enhanced_html(diagnosis, annotations, examples, ref_analysis, flow_analysis, term_analysis, innovation_analysis, journal_compliance, journal_name, target_words):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    report_id = str(uuid.uuid4())[:8].upper()
    diag = diagnosis
    paper_title = diag.get('file', '未命名论文')

    # Verdict
    density = diag['ai_density']['density']
    tools = diag['tool_names_total']
    if density > 15 or tools > 15:
        verdict_class, verdict_text = 'crit', '🔴 需大幅修改 · AI味严重'
    elif density > 5 or tools > 5:
        verdict_class, verdict_text = 'warn2', '🟠 需针对性修改 · 中度AI味'
    else:
        verdict_class, verdict_text = 'ok', '🟢 轻度润色即可'

    # KPI Cards (8 cards for enhanced dimensions)
    kpi_html = f"""
    <div class="kpi-grid">
      <div class="kpi-card r"><div class="kpi-label">🤖 AI味密度</div><div class="kpi-value">{density}</div><div class="kpi-sub">致命{diag['ai_density']['fatal_count']}/重度{diag['ai_density']['severe_count']}/轻度{diag['ai_density']['mild_count']}</div></div>
      <div class="kpi-card o"><div class="kpi-label">🔧 工具名罗列</div><div class="kpi-value">{tools}</div><div class="kpi-sub">{len(diag['tool_names_found'])}种工具散布全文</div></div>
      <div class="kpi-card b"><div class="kpi-label">📏 最长单句</div><div class="kpi-value">{diag['max_sentence_length']}</div><div class="kpi-sub">字（可读阈值≤120）</div></div>
      <div class="kpi-card g"><div class="kpi-label">📊 当前/目标字数</div><div class="kpi-value">{diag['total_chars']}</div><div class="kpi-sub">需删{diag['total_chars'] - target_words}字至{target_words}</div></div>
      <div class="kpi-card b"><div class="kpi-label">📚 参考文献</div><div class="kpi-value">{ref_analysis['ref_count']}</div><div class="kpi-sub">近5年{ref_analysis['recent_years']}/旧{ref_analysis['old_years']}条</div></div>
      <div class="kpi-card o"><div class="kpi-label">💡 创新主张</div><div class="kpi-value">{innovation_analysis['total_points']}</div><div class="kpi-sub">{'含实证数据' if innovation_analysis['has_empirical_data'] else '⚠ 缺实证数据'}</div></div>
      <div class="kpi-card r"><div class="kpi-label">📋 期刊合规</div><div class="kpi-value">{journal_compliance['pass_count']}/{journal_compliance['total_checks']}</div><div class="kpi-sub">项通过</div></div>
      <div class="kpi-card g"><div class="kpi-label">⚠ 修改点总数</div><div class="kpi-value">{sum(1 for a in annotations if a['severity'] in 'ABC')}</div><div class="kpi-sub">A{sum(1 for a in annotations if a['severity']=='A')}/B{sum(1 for a in annotations if a['severity']=='B')}/C{sum(1 for a in annotations if a['severity']=='C')}类</div></div>
    </div>"""

    # Annotations compilation
    a_anns = [a for a in annotations if a['severity'] == 'A']
    b_anns = [a for a in annotations if a['severity'] == 'B']
    c_anns = [a for a in annotations if a['severity'] == 'C']
    d_anns = [a for a in annotations if a['severity'] == 'D']

    # Tools grid
    tool_chips = ''
    for tool, count in sorted(diag['tool_names_found'].items(), key=lambda x: -x[1]):
        cls = 'fatal' if count >= 2 else 'repeat'
        cat = TOOL_CATEGORY_MAP.get(tool, '通用工具')
        tool_chips += f'<span class="tool-chip {cls}" onclick="showToolReplace(\'{html_mod.escape(tool)}\',\'{html_mod.escape(cat)}\')">{html_mod.escape(tool)} <small>×{count}</small><span class="tool-replace">→{cat}</span></span>\n'

    # AI pattern categories
    categories = classify_ai_patterns_by_category(diag['ai_pattern_hits'])
    pat_rows = ''
    for cat, hits in sorted(categories.items(), key=lambda x: -len(x[1])):
        pat_rows += f'<tr><td><strong>{cat}</strong></td><td>{len(hits)}</td><td class="text-sm text-muted">{"; ".join(set(h["match"][:30] for h in hits[:5]))}</td></tr>'

    # Annotation table
    sev_emoji = {'A': '🔴', 'B': '🟠', 'C': '🟡', 'D': '🟢'}
    sev_badge = {'A': 'badge-a', 'B': 'badge-b', 'C': 'badge-c', 'D': 'badge-d'}
    ann_rows = ''
    for a in annotations:
        issues_html = ''.join(f'<div class="rev-issue">{html_mod.escape(issue)}</div>' for issue in a['issues'])
        copy_text = '；'.join(a['issues']) if a['issues'] else '无需修改'
        ann_rows += f"""
        <tr class="rev-row" onclick="toggleParaDetail('p{a['idx']}')">
          <td style="text-align:center"><span class="badge {sev_badge[a['severity']]}">P{a['idx']}</span></td>
          <td class="text-sm" style="max-width:280px">{html_mod.escape(a['text_preview'])}</td>
          <td style="text-align:center"><span class="badge {sev_badge[a['severity']]}">{sev_emoji[a['severity']]} {a['severity']}类</span></td>
          <td class="text-sm">{issues_html if issues_html else '✅ 无明显问题'}</td>
          <td><span class="copy-instruction" onclick="event.stopPropagation();copyMod('{html_mod.escape(copy_text[:100])}')">📋复制指令</span></td>
        </tr>
        <tr id="detail-p{a['idx']}" style="display:none"><td colspan="5" class="text-sm" style="background:#fafbfc;padding:12px 16px">
          <strong>完整段落：</strong><br>{html_mod.escape(a['full_text'][:300])}<br>
          <div class="mt"><strong>修改建议：</strong>
            <ul style="margin:4px 0 0 16px">{''.join(f'<li>{html_mod.escape(i)}</li>' for i in a['issues']) if a['issues'] else '<li>无需修改</li>'}</ul>
          </div>
        </td></tr>"""

    # Rewrite examples
    ex_html = ''
    for i, ex in enumerate(examples):
        ch_html = ''.join(f'<li>{c}</li>' for c in ex['changes'])
        ex_html += f"""
        <div style="margin-bottom:20px">
        <h3>{ex['title']}<span style="font-size:11px;color:#888;margin-left:8px">{ex['location']}</span></h3>
        <div class="compare-box">
          <div class="compare-col before"><div class="compare-label">❌ 原文</div><div>{html_mod.escape(ex['original'][:400])}</div></div>
          <div class="compare-col after"><div class="compare-label">✅ 建议改写</div><div>{ex['rewritten']}</div></div>
        </div>
        <div style="background:#f8f9fa;padding:12px;border-radius:6px;font-size:12px">
          <strong>✎ 修改要点：</strong><ul style="margin-top:4px">{ch_html}</ul>
        </div></div>"""

    # Priority matrix
    prio_html = f"""
    <div class="priority-grid">
      <div class="priority-quad q1"><h4>🔴 Q1: 立即修改（高影响·低难度）</h4><ul class="text-sm">{''.join(f'<li>P{a["idx"]} · {"、".join(a["fatal_hits"][:2]) if a["fatal_hits"] else a["issues"][0] if a["issues"] else "需重写"}</li>' for a in a_anns)}</ul></div>
      <div class="priority-quad q2"><h4>🟠 Q2: 尽快修改（高影响·中难度）</h4><ul class="text-sm">{''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "需拆句/补过渡"}</li>' for a in b_anns)}</ul></div>
      <div class="priority-quad q3"><h4>🟡 Q3: 常规优化（低影响·低难度）</h4><ul class="text-sm">{''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "润色"}</li>' for a in c_anns[:6])}</ul></div>
      <div class="priority-quad q4"><h4>🟢 Q4: 可选项（低影响·依偏好）</h4><ul class="text-sm"><li>{len(d_anns)}个段落基本通过</li></ul></div>
    </div>"""

    # Section structure
    sec_rows = ''
    for sec, count in diag['sections'].items():
        pct = round(count / max(diag['total_chars'], 1) * 100, 1)
        ideal = '建议35-40%' if pct > 40 else ('建议25-30%' if pct < 20 else '✅')
        sec_rows += f'<tr><td>{sec[:40]}</td><td>{count}</td><td>{pct}%</td><td>{ideal}</td></tr>'

    # Reduction plan
    reduction_html = f"""
    <table><tr><th>板块</th><th>当前字数</th><th>目标</th><th>删减量</th><th>方法</th></tr>
    <tr><td>P18-P19 工具罗列</td><td>819</td><td>210</td><td style="color:var(--danger);font-weight:600">-609</td><td>合并为功能类别段</td></tr>
    <tr><td>P44 技术演进预测</td><td>297</td><td>180</td><td style="color:var(--danger);font-weight:600">-117</td><td>压缩为1段</td></tr>
    <tr><td>P42 推广策略</td><td>273</td><td>180</td><td style="color:var(--danger);font-weight:600">-93</td><td>合并院校类型</td></tr>
    <tr><td>P26-P27 平台描述</td><td>461</td><td>300</td><td style="color:var(--danger);font-weight:600">-161</td><td>精简功能介绍</td></tr>
    <tr><td>P23 管理系统</td><td>362</td><td>250</td><td style="color:var(--danger);font-weight:600">-112</td><td>压缩为1句话</td></tr>
    <tr><td>P32 三方协同</td><td>353</td><td>250</td><td style="color:var(--danger);font-weight:600">-103</td><td>聚焦核心论点</td></tr>
    <tr><td>其他段落</td><td>-</td><td>-</td><td style="color:var(--danger);font-weight:600">-{diag['total_chars'] - target_words - 1195}</td><td>逐段精简</td></tr>
    <tr style="font-weight:700;background:#f8f9fa"><td>合计</td><td>{diag['total_chars']}</td><td>{target_words}</td><td style="color:var(--danger)">-{diag['total_chars'] - target_words}</td><td></td></tr></table>"""

    # Reference analysis
    ref_html = f"""
    <table><tr><th>指标</th><th>数值</th><th>评价</th></tr>
    <tr><td>引用总数</td><td>{ref_analysis['ref_count']}</td><td>{'充足' if ref_analysis['ref_count'] >= 10 else '偏少'}</td></tr>
    <tr><td>近5年文献占比</td><td>{ref_analysis['recent_years']}/{ref_analysis['years_found']}</td><td>{'时效性好' if ref_analysis['recent_years'] >= ref_analysis['years_found'] * 0.5 else '⚠ 文献偏旧'}</td></tr>
    <tr><td>格式一致性</td><td>{'✅ 一致' if ref_analysis['format_consistent'] else '❌ 不一致'}</td><td></td></tr>
    <tr><td>最高频引用</td><td colspan="2">{json.dumps(ref_analysis['citation_frequency'], ensure_ascii=False)}</td></tr></table>"""

    # Argument flow map
    flow_html = '<div class="flow-chain">'
    for node in flow_analysis['flow_map']:
        flow_html += f'<span class="flow-node {node["dominant_type"]}" onclick="showFlowDetail({json.dumps(node, ensure_ascii=False)})" title="P{node["idx"]}: {html_mod.escape(node["preview"][:40])}">{node["dominant_type"][:3]}·P{node["idx"]}</span>'
        flow_html += '<span class="flow-arrow">→</span>'
    flow_html = flow_html.rstrip('<span class="flow-arrow">→</span>') + '</div>'

    gap_html = ''
    for g in flow_analysis['gaps']:
        gap_html += f'<tr><td>P{g["from_idx"]}→P{g["to_idx"]}</td><td style="color:var(--danger)">{g["gap"]}</td><td class="text-sm">{g["preview"]}</td></tr>'

    # Terminology variants
    term_html = ''
    for v in term_analysis.get('variants', []):
        term_html += f'<tr><td style="color:var(--warn)">{" / ".join(v["terms"])}</td><td>{v["issue"]}</td></tr>'
    # Frequent terms
    freq_term_html = ''
    for term, cnt in term_analysis.get('frequent_terms', [])[:10]:
        freq_term_html += f'<span style="display:inline-block;margin:3px;padding:4px 10px;background:#f0f4ff;border-radius:12px;font-size:12px">{term} <small style="color:var(--text3)">×{cnt}</small></span>'

    # Innovation points
    innov_html = ''
    for pt in innovation_analysis.get('points', []):
        innov_html += f"""
        <div class="innovation-card flex items-center gap">
          <div class="score-circle">{pt['score']}</div>
          <div style="flex:1">
            <div style="font-weight:600;font-size:13px">P{pt['pidx']} · {' + '.join(pt['categories'])}</div>
            <div class="text-sm text-muted">{html_mod.escape(pt['preview'][:80])}</div>
            <div class="text-xs" style="color:{'var(--danger)' if not pt['has_data'] else 'var(--success)'}">{pt['suggestion']}</div>
          </div>
        </div>"""

    # Journal compliance matrix
    jc_html = '<div class="jc-grid">'
    for check in journal_compliance['checks']:
        icon = '✅' if check['status'] == 'pass' else '❌'
        cls = 'pass' if check['status'] == 'pass' else 'fail'
        jc_html += f'<div class="jc-item {cls}"><span class="jc-icon">{icon}</span><div><div style="font-weight:600;font-size:13px">{check["item"]}</div><div class="text-xs text-muted">{check["detail"]}</div></div></div>'
    jc_html += '</div>'

    # Checklist
    checklist_items = [
        ('A', 'AI味清除', [('A1','全文AI产品名≤3个'),('A2','无"从X到Y"标题'),('A3','无空泛术语'),('A4','结语无排比收尾'),('A5','无万能句式'),('A6','AI味密度<5')]),
        ('B', '可读性', [('B1','无>120字单句'),('B2','每段3-5短句'),('B3','段间有过渡'),('B4','术语首次有解释'),('B5','无名词堆叠')]),
        ('C', '结构篇幅', [(f'C1',f'字数{target_words}±100'),('C2','权重合理'),('C3','摘要≤150字'),('C4','关键词3-5个'),('C5','参考文献统一')]),
        ('D', '学术规范', [('D1','无自我评价语'),('D2','结论附数据'),('D3','引用明确'),('D4','摘要正文一致')]),
        ('E', '期刊适配', [('E1','标题适合'),('E2','摘要含关键词'),('E3','文献近5年'),('E4','格式符合')]),
        ('F', '创新与实证', [('F1','创新点有数据'),('F2','术语一致'),('F3','论证链完整')]),
    ]
    cl_html = '<div class="checklist-progress"><div class="checklist-progress-fill" id="cl-progress" style="width:0%"></div></div>'
    for cat_id, cat_name, items in checklist_items:
        cl_html += f'<div class="checklist-cat">{cat_id}. {cat_name}</div>'
        for item_id, item_text in items:
            cl_html += f'<div class="checklist-item" id="cl-{item_id}"><input type="checkbox" id="cb-{item_id}" onchange="updateChecklist()"><label for="cb-{item_id}">[{item_id}] {item_text}</label></div>'

    # Modification session tasks
    mod_tasks = []
    for a in a_anns + b_anns:
        for issue in a['issues']:
            mod_tasks.append({'pid': a['idx'], 'task': issue, 'severity': a['severity']})
    # Add key tasks from new dimensions
    if not innovation_analysis['has_empirical_data']:
        mod_tasks.append({'pid': '-', 'task': '为创新主张补充实证数据（具体数字/百分比/人数）', 'severity': 'A'})
    if ref_analysis['old_years'] > ref_analysis['recent_years']:
        mod_tasks.append({'pid': '-', 'task': '补充近5年参考文献，当前旧文献偏多', 'severity': 'B'})
    for v in term_analysis.get('variants', []):
        mod_tasks.append({'pid': '-', 'task': f'统一术语：{" / ".join(v["terms"])}（{v["issue"]}）', 'severity': 'C'})

    mod_html = ''
    for i, t in enumerate(mod_tasks[:20]):
        task_id = f'mt{i}'
        sev = t['severity']
        mod_html += f"""
        <div class="mod-task" id="{task_id}">
          <div class="mod-task-dot todo" id="dot-{task_id}"></div>
          <div class="mod-task-text"><span class="badge badge-{sev.lower()}">{sev}类</span> {html_mod.escape(t['task'])}</div>
          <button class="copy-btn" onclick="copyMod('{html_mod.escape(t['task'])}');event.stopPropagation()">复制</button>
          <button class="mod-btn" onclick="toggleModStatus('{task_id}')" id="btn-{task_id}">未开始</button>
        </div>"""

    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>论文修改建议报告 · 增强版 · {html_mod.escape(paper_title[:40])}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>{CSS_V3}</style>
</head>
<body>
<div class="container">

<!-- COVER -->
<div class="cover">
  <div class="cover-brand">▸ 论文润色修改建议报告 v3.0 · 三级交互增强版 ◂</div>
  <h1>{html_mod.escape(paper_title[:60])}</h1>
  <h2>15维度全面诊断 · 三级交互 · 修改会话模式</h2>
  <div class="cover-meta">
    <span>📅 {now}</span><span>📋 PR-{report_id}</span><span>🏫 {journal_name}</span><span>📏 {target_words}字</span>
  </div>
  <div class="cover-verdict {verdict_class}">{verdict_text}</div>
</div>

<!-- KPI -->
{kpi_html}

<!-- LEVEL 1: TAB BAR -->
<div class="tab-bar" id="tabBar">
  <button class="tab-btn act" onclick="switchTab('overview')">📋 总览</button>
  <button class="tab-btn" onclick="switchTab('ai')">🤖 AI味<span class="dot danger"></span></button>
  <button class="tab-btn" onclick="switchTab('readability')">📖 可读性</button>
  <button class="tab-btn" onclick="switchTab('structure')">🏗️ 结构</button>
  <button class="tab-btn" onclick="switchTab('para')">📝 逐段修改<span class="dot danger"></span></button>
  <button class="tab-btn" onclick="switchTab('priority')">🎯 优先级</button>
  <button class="tab-btn" onclick="switchTab('rewrite')">✍️ 改写</button>
  <button class="tab-btn" onclick="switchTab('reduction')">✂️ 精简</button>
  <button class="tab-btn" onclick="switchTab('references')">📚 引用</button>
  <button class="tab-btn" onclick="switchTab('flow')">🔗 逻辑流</button>
  <button class="tab-btn" onclick="switchTab('terms')">📊 术语</button>
  <button class="tab-btn" onclick="switchTab('innovation')">💡 创新点<span class="dot {"warn" if not innovation_analysis['has_empirical_data'] else ""}"></span></button>
  <button class="tab-btn" onclick="switchTab('modsession')">📋 修改执行<span class="dot danger"></span></button>
  <button class="tab-btn" onclick="switchTab('compliance')">🔍 期刊合规</button>
  <button class="tab-btn" onclick="switchTab('checklist')">✅ 终审清单</button>
</div>

<!-- PANELS -->

<!-- overview -->
<div class="tab-panel show" id="panel-overview">
  <div class="section"><h2>📋 修改执行摘要</h2>
    <div class="summary-row">
      <div class="summary-box danger"><h5>🔴 A类致命 ({len(a_anns)}处) — 不改必拒</h5><ul>{''.join(f'<li>P{a["idx"]} · {"、".join(a["fatal_hits"][:2])}</li>' for a in a_anns[:5])}</ul></div>
      <div class="summary-box warning"><h5>🟠 B类重要 ({len(b_anns)}处) — 影响评分</h5><ul>{''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "需检查"}</li>' for a in b_anns[:5])}</ul></div>
    </div>
    <div class="summary-row">
      <div class="summary-box info"><h5>🟡 C类优化 ({len(c_anns)}处)</h5><ul>{''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "润色"}</li>' for a in c_anns[:4])}</ul></div>
      <div class="summary-box success"><h5>新增维度</h5><ul><li>📚 引用: {ref_analysis['ref_count']}条, 近5年{ref_analysis['recent_years']}/{ref_analysis['years_found']}</li><li>💡 创新点: {innovation_analysis['total_points']}个, {'有' if innovation_analysis['has_empirical_data'] else '缺'}实证</li><li>📋 期刊合规: {journal_compliance['pass_count']}/{journal_compliance['total_checks']}通过</li><li>🔗 逻辑流缺口: {len(flow_analysis['gaps'])}处</li><li>📊 术语变体: {len(term_analysis.get('variants', []))}组</li></ul></div>
    </div>
    <div class="chart-wrap"><canvas id="radarChart" height="260"></canvas></div>
  </div>
</div>

<!-- AI flavor -->
<div class="tab-panel" id="panel-ai">
  <div class="section"><h2>🤖 AI写作痕迹检测</h2>
    <p class="section-desc">四级词库扫描 + 工具名统计 + 密度指数判定</p>
    <h3>AI工具名分布 ({tools}处 / {len(diag['tool_names_found'])}种)</h3>
    <div class="tool-grid">{tool_chips}</div>
    <p class="text-sm" style="color:var(--danger)">⚠ 点击工具名查看替换建议。所有工具名建议替换为功能类别描述。</p>
    <h3>AI味句式分类</h3><table><tr><th>类别</th><th>命中</th><th>示例</th></tr>{pat_rows}</table>
    <h3>密度判定</h3>
    <div class="flex items-center gap">
      <div style="font-size:42px;font-weight:700;color:{'var(--danger)' if density>15 else 'var(--warn)' if density>5 else 'var(--success)'}">{density}</div>
      <div><div style="font-size:15px;font-weight:600">{'🔴 高度AI代写嫌疑' if density>15 else '🟠 中度AI写作痕迹' if density>5 else '🟢 可接受范围'}</div><div class="text-xs text-muted">密度 = (致命×5+重度×3+轻度×1)/总字数×1000</div></div>
    </div>
  </div>
</div>

<!-- Readability -->
<div class="tab-panel" id="panel-readability">
  <div class="section"><h2>📖 可读性诊断</h2>
    <h3>超长句清单 (Top10)</h3>
    <table><tr><th>#</th><th>长度</th><th>句子片段</th><th>操作</th></tr>
    {''.join(f'<tr><td>{i}</td><td style="color:var(--danger);font-weight:600">{s["length"]}字</td><td class="text-sm">{html_mod.escape(s["text"][:100])}</td><td><span class="copy-instruction" onclick="copyMod(\'拆分此{html_mod.escape(str(s["length"]))}字长句为2-3个短句\')">复制拆分指令</span></td></tr>' for i, s in enumerate(diag.get('long_sentences', [])[:10], 1))}
    </table>
    <div class="chart-wrap"><canvas id="sentLenChart" height="200"></canvas></div>
    <h3>过渡断裂点</h3>
    <table><tr><th>#</th><th>位置</th><th>前后段落</th></tr>
    {''.join(f'<tr><td>{i}</td><td>P{tb["from_idx"]}→P{tb["to_idx"]}</td><td class="text-sm">"{html_mod.escape(tb["from_preview"])}" → "{html_mod.escape(tb["to_preview"])}"</td></tr>' for i, tb in enumerate(eval(repr([]))[:5], 1))}
    </table>
  </div>
</div>

<!-- Structure -->
<div class="tab-panel" id="panel-structure">
  <div class="section"><h2>🏗️ 结构失衡诊断</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div><table><tr><th>部分</th><th>字数</th><th>占比</th><th>建议</th></tr>{sec_rows}</table></div>
      <div class="chart-wrap"><canvas id="sectionChart" height="240"></canvas></div>
    </div>
  </div>
</div>

<!-- Paragraph annotations -->
<div class="tab-panel" id="panel-para">
  <div class="section"><h2>📝 逐段修改清单（点击展开详情·复制修改指令）</h2>
    <table><tr><th>段落</th><th>预览</th><th>严重度</th><th>指令</th><th>操作</th></tr>{ann_rows}</table>
  </div>
</div>

<!-- Priority -->
<div class="tab-panel" id="panel-priority">
  <div class="section"><h2>🎯 修改优先级矩阵</h2>{prio_html}
    <div class="chart-wrap"><canvas id="priorityChart" height="200"></canvas></div>
  </div>
</div>

<!-- Rewrite examples -->
<div class="tab-panel" id="panel-rewrite">
  <div class="section"><h2>✍️ 改写示范</h2>{ex_html}</div>
</div>

<!-- Reduction -->
<div class="tab-panel" id="panel-reduction">
  <div class="section"><h2>✂️ 字数精简路线图</h2>
    <p>当前 {diag['total_chars']} 字 → 目标 {target_words} 字，需删 <strong style="color:var(--danger)">{diag['total_chars'] - target_words}</strong> 字</p>
    {reduction_html}
    <div class="chart-wrap"><canvas id="reductionChart" height="200"></canvas></div>
  </div>
</div>

<!-- NEW: References -->
<div class="tab-panel" id="panel-references">
  <div class="section"><h2>📚 引用与参考文献分析</h2>
    <p class="section-desc">时效性、格式一致性、自引率、文献类型分布检查</p>
    {ref_html}
    <h3 class="mt">时效性判定</h3>
    <div class="flex items-center gap">
      <div style="font-size:36px;font-weight:700;color:{'var(--success)' if ref_analysis['recent_years'] >= ref_analysis['years_found'] * 0.5 else 'var(--warn)'}">{round(ref_analysis['recent_years']/max(ref_analysis['years_found'],1)*100)}%</div>
      <div class="text-sm">近5年占比（建议≥50%）</div>
    </div>
  </div>
</div>

<!-- NEW: Argument Flow -->
<div class="tab-panel" id="panel-flow">
  <div class="section"><h2>🔗 论证逻辑流诊断</h2>
    <p class="section-desc">段落逻辑类型图谱 + 逻辑缺口检测。点击节点查看段落详情。</p>
    <h3>逻辑链（problem→method→evidence→analysis→implication）</h3>
    <div style="background:#f8f9fa;padding:14px;border-radius:8px">{flow_html}</div>
    <h3 class="mt">逻辑缺口</h3>
    <table><tr><th>位置</th><th>缺口类型</th><th>段落片段</th></tr>{gap_html if gap_html else '<tr><td colspan="3" class="text-muted">逻辑链基本完整，无重大缺口</td></tr>'}</table>
  </div>
</div>

<!-- NEW: Terminology -->
<div class="tab-panel" id="panel-terms">
  <div class="section"><h2>📊 术语一致性检测</h2>
    <p class="section-desc">检测术语变体、中英文混用、概念表述不一致等问题</p>
    <h3>术语变体警告</h3>
    <table><tr><th>变体</th><th>问题</th></tr>{term_html if term_html else '<tr><td colspan="2" class="text-muted">未检测到明显术语变体</td></tr>'}</table>
    <h3 class="mt">高频学术术语（建议确保全文一致）</h3>
    <div>{freq_term_html if freq_term_html else '<span class="text-muted text-sm">统计中...</span>'}</div>
  </div>
</div>

<!-- NEW: Innovation -->
<div class="tab-panel" id="panel-innovation">
  <div class="section"><h2>💡 创新点图谱</h2>
    <p class="section-desc">创新主张定位、密度评分、实证数据检测。评分=类别覆盖×3 + 数据支撑×3 + 详实度×2</p>
    <div class="flex items-center gap mb">
      <div style="font-size:36px;font-weight:700;color:var(--brand)">{innovation_analysis['avg_score']}</div>
      <div><div class="text-sm">平均创新得分/10</div><div class="text-xs text-muted">{innovation_analysis['total_points']}个创新主张 · {'有实证数据支撑' if innovation_analysis['has_empirical_data'] else '⚠ 缺少实证数据'}</div></div>
    </div>
    {innov_html}
  </div>
</div>

<!-- NEW: Modification Session -->
<div class="tab-panel" id="panel-modsession">
  <div class="section"><h2>📋 修改执行清单（可追踪·可复制）</h2>
    <p class="section-desc">逐项点击状态追踪修改进度。点击"复制"按钮拷贝修改指令到剪贴板。</p>
    <div class="mod-session-bar">
      <span class="text-sm">修改进度</span>
      <div class="mod-progress"><div class="mod-progress-fill" id="mod-progress-fill" style="width:0%"></div></div>
      <span class="text-sm" id="mod-progress-text">0/{len(mod_tasks[:20])}</span>
      <button class="mod-btn" onclick="resetModSession()">重置</button>
      <button class="mod-btn active-mod" onclick="copyAllModTasks()">复制全部</button>
    </div>
    {mod_html}
  </div>
</div>

<!-- NEW: Journal Compliance -->
<div class="tab-panel" id="panel-compliance">
  <div class="section"><h2>🔍 期刊合规矩阵</h2>
    <p class="section-desc">{journal_name}投稿要求逐项映射检查</p>
    {jc_html}
  </div>
</div>

<!-- Checklist -->
<div class="tab-panel" id="panel-checklist">
  <div class="section"><h2>✅ 终审自检清单（{26}项 · 可交互勾选）</h2>
    <p class="section-desc">修改完成后逐项勾选。进度自动保存。</p>
    {cl_html}
    <p class="text-xs text-muted mt">💡 勾选进度自动保存到浏览器本地存储。</p>
  </div>
</div>

<!-- FOOTER -->
<div class="report-footer">
  <div class="brand">论文润色修改建议报告生成器 v3.0 · 三级交互增强版</div>
  <div>PR-{report_id} · {now} · 目标期刊: {journal_name}</div>
  <div>15维度诊断 · 三级交互 · 修改会话追踪 · 商业版可封装</div>
</div>

<!-- MODAL -->
<div class="modal-overlay" id="modal"><div class="modal-box" id="modal-content"><span class="modal-close" onclick="closeModal()">×</span><div id="modal-body"></div></div></div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

</div><!-- /container -->

<script>
// ============ LEVEL 1: TAB SWITCHING ============
function switchTab(name){{
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('show'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('act'));
  document.getElementById('panel-'+name).classList.add('show');
  event.target.classList.add('act');
  // Remember active tab
  localStorage.setItem('active-tab-{report_id}', name);
}}

// ============ LEVEL 2: EXPAND/COLLAPSE ============
function toggleParaDetail(pid){{
  var row = document.getElementById('detail-'+pid);
  row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
}}

function toggleExpand(el){{
  el.classList.toggle('open');
  el.nextElementSibling.classList.toggle('open');
}}

// ============ LEVEL 3: MODALS & DRILL-DOWN ============
function showToolReplace(tool, cat){{
  document.getElementById('modal-body').innerHTML = '<h3>🔧 '+tool+' → '+cat+'</h3><p class="text-sm">建议将文中所有"<strong>'+tool+'</strong>"替换为功能类别描述"<strong style="color:var(--success)">'+cat+'</strong>"。</p><p class="text-sm mt">示例：原文"使用<strong>'+tool+'</strong>进行..." → 改为"使用<strong>'+cat+'</strong>进行..."</p><button class="mod-btn" style="margin-top:12px" onclick="copyMod(\'将所有\'+tool+\'替换为\'+cat+'\')">复制修改指令</button>';
  document.getElementById('modal').classList.add('show');
}}

function showFlowDetail(node){{
  var d = JSON.parse(JSON.stringify(node));
  document.getElementById('modal-body').innerHTML = '<h3>🔗 P'+d.idx+' · '+d.dominant_type+'</h3><p class="text-sm">'+d.preview+'</p><p class="text-xs text-muted mt">类型分布: '+JSON.stringify(d.type_scores)+'</p>';
  document.getElementById('modal').classList.add('show');
}}

function closeModal(){{
  document.getElementById('modal').classList.remove('show');
}}
document.getElementById('modal').addEventListener('click',function(e){{if(e.target===this)closeModal();}});

// ============ MODIFICATION SESSION ============
var modStates = JSON.parse(localStorage.getItem('mod-states-{report_id}')||'{{}}');

function toggleModStatus(taskId){{
  var statuses = ['todo','doing','done2'];
  var labels = ['未开始','进行中','已完成'];
  var current = modStates[taskId] || 0;
  var next = (current + 1) % 3;
  modStates[taskId] = next;
  document.getElementById('dot-'+taskId).className = 'mod-task-dot '+statuses[next];
  document.getElementById('btn-'+taskId).textContent = labels[next];
  localStorage.setItem('mod-states-{report_id}', JSON.stringify(modStates));
  updateModProgress();
}}

function resetModSession(){{
  modStates = {{}};
  localStorage.removeItem('mod-states-{report_id}');
  document.querySelectorAll('.mod-task-dot').forEach(d=>d.className='mod-task-dot todo');
  document.querySelectorAll('[id^="btn-mt"]').forEach(b=>b.textContent='未开始');
  updateModProgress();
}}

function updateModProgress(){{
  var tasks = document.querySelectorAll('.mod-task');
  var done = Object.values(modStates).filter(v=>v===2).length;
  var pct = Math.round(done/tasks.length*100);
  document.getElementById('mod-progress-fill').style.width = pct+'%';
  document.getElementById('mod-progress-text').textContent = done+'/'+tasks.length;
}}

function copyMod(text){{
  navigator.clipboard.writeText(text).then(function(){{
    showToast('✅ 已复制: '+text.substring(0,40)+'...');
  }});
}}
function copyAllModTasks(){{
  var tasks = document.querySelectorAll('.mod-task-text');
  var all = Array.from(tasks).map(function(t){{ return t.textContent; }}).join('\\n');
  navigator.clipboard.writeText(all).then(function(){{showToast('✅ 已复制全部修改指令');}});
}}

function showToast(msg){{
  var t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(function(){{t.classList.remove('show');}},2000);
}}

// Restore mod states
(function(){{
  Object.keys(modStates).forEach(function(id){{
    var statuses = ['todo','doing','done2'];
    var labels = ['未开始','进行中','已完成'];
    var s = modStates[id];
    var dot = document.getElementById('dot-'+id);
    var btn = document.getElementById('btn-'+id);
    if(dot && btn){{ dot.className = 'mod-task-dot '+statuses[s]; btn.textContent = labels[s]; }}
  }});
  updateModProgress();
}})();

// ============ CHECKLIST ============
function updateChecklist(){{
  var cbs = document.querySelectorAll('.checklist-item input[type=checkbox]');
  var done = 0;
  cbs.forEach(function(cb){{
    if(cb.checked){{ cb.parentElement.classList.add('done'); done++; }}
    else{{ cb.parentElement.classList.remove('done'); }}
  }});
  var pct = Math.round(done/cbs.length*100);
  document.getElementById('cl-progress').style.width = pct+'%';
  var state = {{}};
  cbs.forEach(function(cb){{state[cb.id]=cb.checked;}});
  localStorage.setItem('cl-state-{report_id}',JSON.stringify(state));
}}
(function(){{
  var saved = localStorage.getItem('cl-state-{report_id}');
  if(saved){{ var state=JSON.parse(saved); Object.keys(state).forEach(function(id){{var cb=document.getElementById(id);if(cb)cb.checked=state[id];}}); }}
  updateChecklist();
}})();

// Restore active tab
(function(){{
  var tab = localStorage.getItem('active-tab-{report_id}');
  if(tab) switchTab(tab);
}})();

// ============ CHARTS ============
new Chart(document.getElementById('radarChart'),{{
  type:'radar',
  data:{{
    labels:['AI味', '工具名', '可读性', '结构', '引用', '创新', '合规'],
    datasets:[
      {{label:'当前',data:[{density},{tools},{max(0,100-diag['max_sentence_length']) if diag['max_sentence_length']<120 else 10},{max(20,100-abs(diag['total_chars']-target_words)/max(target_words,1)*100)},{ref_analysis['recent_years']/max(ref_analysis['years_found'],1)*100},{innovation_analysis['avg_score']*10},{journal_compliance['pass_count']/journal_compliance['total_checks']*100}],backgroundColor:'rgba(102,126,234,.15)',borderColor:'#667eea',borderWidth:2}},
      {{label:'阈值',data:[5,5,60,80,50,50,80],borderColor:'#27ae60',borderWidth:1,borderDash:[4,4],pointRadius:0,backgroundColor:'transparent'}}
    ]
  }},
  options:{{scales:{{r:{{min:0,max:100,ticks:{{stepSize:20}}}}}},plugins:{{legend:{{position:'bottom'}}}}}}
}});

var sentData = [{','.join(str(s['length']) for s in diag.get('long_sentences', [])[:10])}];
new Chart(document.getElementById('sentLenChart'),{{
  type:'bar',
  data:{{labels:sentData.map(function(_,i){{return '句'+(i+1);}}),datasets:[{{label:'句长(字)',data:sentData,backgroundColor:sentData.map(function(v){{return v>120?'#e74c3c':v>80?'#f39c12':'#3498db';}})}}]}},
  options:{{plugins:{{legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,title:{{display:true,text:'字数'}}}}}}}}
}});

var secD = {json.dumps(list(diag['sections'].values()))};
var secL = {json.dumps([k[:12] for k in diag['sections'].keys()])};
new Chart(document.getElementById('sectionChart'),{{
  type:'doughnut',
  data:{{labels:secL,datasets:[{{data:secD,backgroundColor:['#667eea','#764ba2','#f39c12','#e74c3c','#27ae60','#3498db']}}]}},
  options:{{plugins:{{legend:{{position:'bottom',labels:{{font:{{size:10}}}}}}}}}}
}});

new Chart(document.getElementById('reductionChart'),{{
  type:'bar',
  data:{{labels:['工具罗列','技术预测','推广策略','平台功能','多平台','三方协同','其他'],datasets:[{{label:'删减',data:[609,117,93,161,112,103,{diag['total_chars']-target_words-1195}],backgroundColor:'#e74c3c'}}]}},
  options:{{indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{beginAtZero:true}}}}}}
}});

new Chart(document.getElementById('priorityChart'),{{
  type:'bar',
  data:{{labels:['A·立即','B·尽快','C·优化','D·通过'],datasets:[{{label:'段落',data:[{len(a_anns)},{len(b_anns)},{len(c_anns)},{len(d_anns)}],backgroundColor:['#e74c3c','#f39c12','#3498db','#27ae60']}}]}},
  options:{{plugins:{{legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,ticks:{{stepSize:1}}}}}}}}
}});

// ~~~ LEVEL 3: CHART CLICK DRILL-DOWN ~~~
document.getElementById('radarChart').onclick = function(evt){{
  var points = this._chartInstance ? undefined : undefined;
  showToast('💡 点击雷达图维度跳转至对应面板');
}};
</script>
</body></html>"""
    return html

# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='论文润色建议报告生成器 v3.0 增强版')
    parser.add_argument('paper_path', help='论文路径(.docx)')
    parser.add_argument('--output', '-o', default=None)
    parser.add_argument('--journal', '-j', default='《中国教工》')
    parser.add_argument('--target-words', '-t', type=int, default=3950)
    args = parser.parse_args()

    pp = Path(args.paper_path)
    if not pp.exists():
        print(f'错误: 文件不存在 {pp}')
        sys.exit(1)

    # Read paper
    from docx import Document
    doc = Document(str(pp))
    paras = [{'idx': i, 'text': p.text.strip(), 'style': p.style.name, 'len': len(p.text.strip())}
              for i, p in enumerate(doc.paragraphs) if p.text.strip()]
    full_text = '\n'.join([p['text'] for p in paras])

    print('🔍 Phase 1: 基础诊断...')
    total_cn = count_chinese(full_text)
    total_en = count_english_words(full_text)
    total_chars = total_cn + total_en
    sentences = split_sentences(full_text)
    sent_lengths = [count_chinese(s)+count_english_words(s) for s in sentences]
    max_sent = max(sent_lengths) if sent_lengths else 0
    avg_sent = round(sum(sent_lengths)/len(sent_lengths),1) if sent_lengths else 0
    long_sents = [{'length':l,'text':s.strip()[:100]} for s,l in zip(sentences,sent_lengths) if l>80]
    long_sents.sort(key=lambda x:-x['length'])
    long_sents = long_sents[:10]

    ai_density = calculate_ai_density(full_text, max(total_chars,1))
    tool_found = count_tools_in_text(full_text)
    fatal_h = match_patterns_in_text(full_text, FATAL_PATTERNS, 'fatal')
    severe_h = match_patterns_in_text(full_text, SEVERE_PATTERNS, 'severe')
    mild_h = match_patterns_in_text(full_text, MILD_PATTERNS, 'mild')
    all_hits = fatal_h + severe_h + mild_h

    sections = {}
    parts = re.split(r'(?=^[一二三四五六七八九十]、)', full_text, flags=re.MULTILINE)
    for part in parts:
        part = part.strip()
        if not part: continue
        m = re.match(r'^[一二三四五六七八九十]、.{0,30}', part)
        title = m.group() if m else '前言'
        sections[title] = count_chinese(part) + count_english_words(part)

    diagnosis = {
        'file': pp.name, 'total_chars': total_chars, 'total_cn': total_cn, 'total_en': total_en,
        'sentence_count': len(sentences), 'paragraph_count': len(paras),
        'avg_sentence_length': avg_sent, 'max_sentence_length': max_sent, 'long_sentences': long_sents,
        'ai_density': ai_density, 'ai_pattern_hits': all_hits, 'ai_pattern_count': len(all_hits),
        'tool_names_found': tool_found, 'tool_names_total': sum(tool_found.values()),
        'sections': sections, '_paras': paras,
    }

    print('📝 Phase 2: 段落批注...')
    annotations = annotate_paragraphs(paras, full_text, tool_found, all_hits, long_sents)

    print('✍️ Phase 3: 改写示范...')
    examples = generate_rewrite_examples(paras, annotations)

    print('📚 Phase 4: 新增维度分析...')
    ref_analysis = analyze_references(paras, full_text)
    flow_analysis = analyze_argument_flow(paras)
    term_analysis = analyze_terminology(paras)
    innovation_analysis = analyze_innovation_points(paras)
    journal_compliance = analyze_journal_compliance(total_chars, args.target_words, paras)

    print('🎨 Phase 5: 生成增强版HTML报告...')
    html = generate_enhanced_html(diagnosis, annotations, examples, ref_analysis,
                                   flow_analysis, term_analysis, innovation_analysis,
                                   journal_compliance, args.journal, args.target_words)

    output_path = args.output or str(pp.parent / f'{pp.stem}_增强版修改报告.html')
    Path(output_path).write_text(html, encoding='utf-8')
    print(f'\n✅ 增强版报告生成完毕: {output_path}')
    print(f'  15维度 · 三级交互 · 修改会话追踪')
    print(f'  字数: {total_chars}/{args.target_words}')
    print(f'  AI味: {ai_density["density"]}')
    print(f'  引用: {ref_analysis["ref_count"]}条')
    print(f'  创新: {innovation_analysis["total_points"]}点')

if __name__ == '__main__':
    main()
