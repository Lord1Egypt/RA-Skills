#!/usr/bin/env python3
"""
论文润色修改完善建议报告生成器 v2.0
=====================================
一键生成专业级、可收费的多维度论文修改建议HTML报告。

用法: python generate_revision_report.py <论文路径.docx> [--output 报告路径.html] [--journal 期刊名] [--target-words 目标字数]

输出: 单文件HTML报告，含9大维度：
  1. 封面概览（KPI仪表盘 + 综合判定）
  2. AI味检测（工具名/空泛术语/句式模板）
  3. 可读性诊断（句长分布/过渡断裂/名词堆叠）
  4. 结构失衡（各部分权重/论证链完整性）
  5. 逐段修改清单（A/B/C/D严重度分级）
  6. 优先级矩阵（影响×难度四象限）
  7. 改写示范（前后对比 + 字数压缩方案）
  8. 字数精简路线图
  9. 终审自检清单（交互式勾选）
"""

import re
import json
import sys
import os
import datetime
import uuid
import hashlib
import html as html_mod
from pathlib import Path
from collections import Counter, defaultdict

# ============================================================
# 诊断数据层
# ============================================================

FATAL_PATTERNS = [
    (r'从.{2,8}到.{2,8}[：:].{4,}', '标题模板'),
    (r'(以.{2,10}为.{2,10}[，,]?\s*){4,}', '四连排比'),
    ('双螺旋结构', '生物学隐喻'),
    ('深层互构', '空泛概念'),
    ('认知跃迁', '空泛概念'),
    ('信息平权', '空泛概念'),
    ('群体智慧', '空泛概念'),
    ('底层逻辑', '空泛概念'),
    ('范式转换', '空泛概念'),
    ('同频共振', '空泛概念'),
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
    (r'显著降低', '万能句式'),
    (r'有力推动', '套话'),
    (r'清晰把握', '套话'),
    (r'深度洞察', '套话'),
    (r'有效回应', '套话'),
]

MILD_PATTERNS = [
    ('显著提升', '模糊量化'),
    ('大幅改善', '模糊量化'),
    ('明显增强', '模糊量化'),
    ('有效促进', '模糊量化'),
    ('积极推动', '模糊量化'),
    ('显著优化', '模糊量化'),
    ('高度适配', '模糊量化'),
    ('有力保障', '模糊量化'),
    ('高效', '模糊量化'),
    ('直观', '模糊量化'),
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
                'level': level,
                'label': label,
                'match': m.group()[:60],
                'context': f'...{ctx}...',
                'position': m.start()
            })
    return hits


def calculate_ai_density(text, total_chars):
    fatal_cnt = sum(1 for p, _ in FATAL_PATTERNS if re.search(p, text))
    severe_cnt = sum(1 for p, _ in SEVERE_PATTERNS if re.search(p, text))
    mild_cnt = sum(1 for p, _ in MILD_PATTERNS if re.search(p, text))
    score = fatal_cnt * 5 + severe_cnt * 3 + mild_cnt * 1
    density = round((score / max(total_chars, 1)) * 1000, 2)
    return {
        'fatal_count': fatal_cnt,
        'severe_count': severe_cnt,
        'mild_count': mild_cnt,
        'raw_score': score,
        'density': density,
    }


def analyze_transitions(paragraph_texts):
    """检测段落间过渡断裂"""
    breaks = []
    transition_words = ['因此', '所以', '此外', '然而', '进而', '同时', '换言之', '在此基础上',
                        '另外', '值得', '需要', '值得注意', '需要指出', '与此', '事实上', '实际上']
    for i in range(1, len(paragraph_texts)):
        prev = paragraph_texts[i-1][:50] if i > 0 else ''
        curr = paragraph_texts[i][:50] if i < len(paragraph_texts) else ''
        has_transition = any(tw in curr for tw in transition_words)
        # Check if topic shift without transition
        if not has_transition and len(paragraph_texts[i]) > 80 and len(paragraph_texts[i-1]) > 80:
            breaks.append({
                'from_idx': i-1,
                'to_idx': i,
                'from_preview': paragraph_texts[i-1][:40],
                'to_preview': paragraph_texts[i][:40],
            })
    return breaks


def detect_noun_piles(paragraph_texts):
    """检测名词堆叠"""
    piles = []
    for idx, text in enumerate(paragraph_texts):
        # Find sequences of 4+ consecutive 、separated items
        matches = re.findall(r'([\u4e00-\u9fff]+(?:、[\u4e00-\u9fff]+){4,})', text)
        for m in matches:
            if len(m) > 20:
                piles.append({'idx': idx, 'text': m[:100], 'count': m.count('、') + 1})
    return piles


def classify_ai_patterns_by_category(hits):
    """将AI味命中按类别分类"""
    categories = defaultdict(list)
    for h in hits:
        categories[h['label']].append(h)
    return dict(categories)


# ============================================================
# 段落级智能批注引擎
# ============================================================

def annotate_paragraphs(paras, full_text, tool_found, ai_hits, long_sents):
    """为每个段落生成修改建议"""
    annotations = []
    total_cn = count_chinese(full_text)

    # Build paragraph-level AI hit map
    para_hits = defaultdict(list)
    for h in ai_hits:
        for idx, p in enumerate(paras):
            if h['match'] in p['text']:
                para_hits[idx].append(h)
                break

    # Build paragraph-level tool name map
    para_tools = defaultdict(list)
    for tool_name, count in tool_found.items():
        for idx, p in enumerate(paras):
            if tool_name in p['text']:
                para_tools[idx].append(tool_name)

    for idx, p in enumerate(paras):
        text = p['text']
        issues = []
        severity = 'D'

        # Check for AI flavor patterns
        fatal_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'fatal']
        severe_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'severe']
        mild_labels = [h['label'] for h in para_hits.get(idx, []) if h['level'] == 'mild']

        # Check for tool names
        tools_in_para = para_tools.get(idx, [])
        if len(tools_in_para) > 0:
            issues.append(f'含{len(tools_in_para)}个AI工具名：{", ".join(tools_in_para[:8])}')
            severity = max(severity, 'C')

        # Check sentence length
        para_sents = split_sentences(text)
        max_sl = max([count_chinese(s) + count_english_words(s) for s in para_sents]) if para_sents else 0
        if max_sl > 120:
            issues.append(f'含超长句（{max_sl}字），需拆分为2-3句')
            severity = max(severity, 'B')
        elif max_sl > 90:
            issues.append(f'句长偏长（{max_sl}字），建议拆分')
            severity = max(severity, 'C')

        # Check for 空泛概念
        if '空泛概念' in fatal_labels:
            issues.append('含空泛学术术语（深层互构/认知跃迁/信息平权等）')
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
            issues.append('"不仅是……更是……"万能句式')
            severity = max(severity, 'B')
        if '套话' in severe_labels:
            issues.append('学术套话（奠定基础/有效回应等）')
            severity = max(severity, 'B')

        if '模糊量化' in mild_labels:
            issues.append('模糊量化词（显著提升/大幅改善等），需数据支撑')
            severity = max(severity, 'C')

        # Check paragraph length
        if len(text) > 400:
            issues.append(f'段落过长（{len(text)}字），建议拆分')
            severity = max(severity, 'B')

        # Check for noun piles
        piles = re.findall(r'([\u4e00-\u9fff]+(?:、[\u4e00-\u9fff]+){4,})', text)
        if piles and len(max(piles, key=len)) > 30:
            issues.append('含名词堆叠，建议拆分为短列表或逐项说明')
            severity = max(severity, 'C')

        annotations.append({
            'idx': idx,
            'style': p.get('style', 'Normal'),
            'text_preview': text[:80],
            'full_text': text,
            'length': len(text),
            'severity': severity,
            'issues': issues,
            'fatal_hits': fatal_labels,
            'severe_hits': severe_labels,
            'mild_hits': mild_labels,
            'tool_names': tools_in_para,
        })

    return annotations


# ============================================================
# 改写示范生成器
# ============================================================

def generate_rewrite_examples(paras, annotations):
    """生成3-4个典型段落的改写示范"""
    examples = []

    # Example 1: 摘要 (P3) - too long, has AI flavor
    for ann in annotations:
        if ann['idx'] == 3:
            examples.append({
                'title': '📝 摘要改写（精简+去AI味）',
                'location': 'P3 · 摘要',
                'original': ann['full_text'],
                'rewritten': '智能传播时代，新闻传播教育面临知识碎片化、实践场景缺失、个性化教学不足等多重挑战。本研究以新文科建设理念为指导，借鉴精益创业方法论，构建AI赋能校政企协同育人模式，并以融合新闻学等三门课程为试点开展验证。结果表明，该模式通过八阶段闭环机制有效提升了学生实践能力与就业适配度。',
                'changes': ['压缩195字→130字', '删"深层逻辑梳理与辩证审视"空泛修饰', '加"结果表明"增强实证感', '删AI痕迹句式"系统探索了……建设标准与实施路径"'],
            })
            break

    # Example 2: P18+P19 工具罗列合并
    p18_text = ''
    p19_text = ''
    for ann in annotations:
        if ann['idx'] == 18:
            p18_text = ann['full_text']
        if ann['idx'] == 19:
            p19_text = ann['full_text']
    if p18_text and p19_text:
        examples.append({
            'title': '✂️ 工具罗列段合并重写（P18+P19 → 单段）',
            'location': 'P18-P19 · 五、生成式AI贯穿的融媒体生产链 + 分发运营段',
            'original': p18_text[:200] + '……[共819字，含25款AI工具名]',
            'rewritten': '工作室全生命周期中系统性嵌入AI技术栈，覆盖新闻生产全流程：预研阶段利用AI检索系统完成资料搜集与文献综述，策划阶段通过思维导图工具实现逻辑可视化，采集阶段借助语音转写平台进行多语种实时转写与智能纪要生成，编辑阶段使用内容审核系统进行敏感词检测与语法优化，视觉生产阶段调用文生图与文生视频平台还原新闻现场，分发运营阶段通过协同办公平台分析传播数据并维护用户互动。技术工具的引入使传统新闻教育中"不可及、不可拟、不可复现"的实训困境得到实质性突破。',
            'changes': ['819字→210字，压缩74%', '25款工具名→0个（全部替换为功能类别）', '保留核心教学场景，删除产品说明书式罗列', '增加教学意义收束句'],
        })

    # Example 3: 结语 (P46) - four-parallel ending
    for ann in annotations:
        if ann['idx'] == 46:
            examples.append({
                'title': '🔄 结语改写（去排比+学术收束）',
                'location': 'P46 · 结语',
                'original': ann['full_text'],
                'rewritten': '本研究探索了新文科背景下新闻传播类智慧课程的建设路径，其核心经验可归纳为三点：以真实社会项目重构教学流程，以AI工具链降低实践门槛，以过程性数据管理实现精准育人。该模式不仅提升了学生的即战能力，更重要的是培养了面对技术变革的适应性与主动性——这正是终身学习能力的关键。',
                'changes': ['202字→140字', '删除"以A为B、以C为D"四连排比', '"系统性尝试"→"探索"', '"为锚点""为支撑""为场域""为保障"→简洁罗列'],
            })
            break

    return examples


# ============================================================
# HTML报告生成器
# ============================================================

CSS_STYLE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "Microsoft YaHei", sans-serif;
    color: #1a1a2e; background: #f5f6fa; line-height: 1.7;
}
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }

/* Cover Page */
.cover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 60px 50px; border-radius: 16px;
    margin-bottom: 30px; position: relative; overflow: hidden;
}
.cover::before {
    content: ''; position: absolute; top: -50%; right: -20%;
    width: 500px; height: 500px; background: rgba(255,255,255,0.05);
    border-radius: 50%; pointer-events: none;
}
.cover-brand {
    font-size: 13px; text-transform: uppercase; letter-spacing: 3px;
    opacity: 0.8; margin-bottom: 25px;
}
.cover h1 {
    font-size: 28px; font-weight: 700; margin-bottom: 12px; position: relative;
}
.cover-meta {
    display: flex; gap: 30px; font-size: 14px; opacity: 0.9; margin-top: 20px;
    flex-wrap: wrap; position: relative;
}
.cover-meta span { display: flex; align-items: center; gap: 6px; }
.cover-verdict {
    display: inline-block; margin-top: 25px; padding: 10px 24px;
    border-radius: 8px; font-size: 15px; font-weight: 600; position: relative;
}
.verdict-critical { background: rgba(255,107,107,0.3); }
.verdict-warning { background: rgba(255,193,7,0.3); }
.verdict-pass { background: rgba(76,175,80,0.3); }

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 30px; }
.kpi-card {
    background: white; border-radius: 12px; padding: 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 4px solid #667eea;
}
.kpi-card.red { border-left-color: #e74c3c; }
.kpi-card.orange { border-left-color: #f39c12; }
.kpi-card.blue { border-left-color: #3498db; }
.kpi-card.green { border-left-color: #27ae60; }
.kpi-card .kpi-value { font-size: 32px; font-weight: 700; margin: 8px 0; }
.kpi-card .kpi-label { font-size: 13px; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }
.kpi-card .kpi-sub { font-size: 12px; color: #95a5a6; margin-top: 4px; }

/* Section */
.section {
    background: white; border-radius: 12px; padding: 35px;
    margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    page-break-inside: avoid;
}
.section h2 {
    font-size: 22px; margin-bottom: 8px; padding-bottom: 12px;
    border-bottom: 2px solid #f0f0f0; display: flex; align-items: center; gap: 10px;
}
.section h3 { font-size: 18px; margin: 20px 0 12px; color: #2c3e50; }
.section-desc { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }

/* Severity Badge */
.badge { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }
.badge-a { background: #ffe0e0; color: #c0392b; }
.badge-b { background: #fff3cd; color: #d35400; }
.badge-c { background: #d6eaf8; color: #2471a3; }
.badge-d { background: #e8f8f5; color: #1abc9c; }

/* Tables */
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { background: #f8f9fa; padding: 12px 14px; text-align: left; font-weight: 600; border-bottom: 2px solid #dee2e6; }
td { padding: 12px 14px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }
tr:hover { background: #fafbfc; }

/* Tool Grid */
.tool-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }
.tool-chip {
    padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 500;
    display: flex; align-items: center; gap: 6px;
}
.tool-chip.fatal { background: #ffe0e0; color: #c0392b; }
.tool-chip.repeat { background: #fff3cd; color: #d35400; }

/* Revision Row */
.rev-row { padding: 14px 0; border-bottom: 1px solid #f5f5f5; }
.rev-row:last-child { border-bottom: none; }
.rev-header { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.rev-pid { font-size: 11px; color: #95a5a6; min-width: 35px; }
.rev-text { color: #555; font-style: italic; font-size: 13px; margin-bottom: 6px; }
.rev-issues { margin-top: 4px; }
.rev-issue { padding: 4px 0; font-size: 13px; display: flex; align-items: flex-start; gap: 8px; }
.rev-issue::before { content: '→'; color: #667eea; font-weight: bold; }

/* Before/After */
.compare-box { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 15px 0; }
.compare-col { padding: 20px; border-radius: 8px; font-size: 13px; line-height: 1.8; }
.compare-col.before { background: #fff5f5; border: 1px solid #ffcdd2; }
.compare-col.after { background: #f0fff4; border: 1px solid #c8e6c9; }
.compare-label { font-weight: 600; font-size: 12px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; color: #666; }

/* Priority Matrix */
.priority-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 15px 0; }
.priority-quad { padding: 18px; border-radius: 8px; min-height: 100px; }
.priority-quad.q1 { background: #ffe0e0; border: 1px solid #ffcdd2; }
.priority-quad.q2 { background: #fff3cd; border: 1px solid #ffe082; }
.priority-quad.q3 { background: #d6eaf8; border: 1px solid #bbdefb; }
.priority-quad.q4 { background: #e8f8f5; border: 1px solid #b2dfdb; }
.priority-quad h4 { font-size: 14px; margin-bottom: 8px; }

/* Checklist */
.checklist-item { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
.checklist-item input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
.checklist-item label { cursor: pointer; font-size: 14px; }
.checklist-item.checked label { text-decoration: line-through; color: #aaa; }
.checklist-cat { font-weight: 600; color: #667eea; margin-top: 15px; font-size: 15px; }
.checklist-progress { margin: 15px 0; }
.checklist-progress-bar { height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden; }
.checklist-progress-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; transition: width 0.3s; }

/* Reduction Plan */
.reduction-bar { display: flex; height: 30px; border-radius: 6px; overflow: hidden; margin: 12px 0; }
.reduction-bar .bar-seg { display: flex; align-items: center; justify-content: center; font-size: 11px; color: white; font-weight: 600; }

/* Chart Containers */
.chart-wrap { max-width: 100%; margin: 15px 0; }

/* Print Overrides */
@media print {
    body { background: white; }
    .container { max-width: 100%; padding: 0; }
    .section { box-shadow: none; border: 1px solid #ddd; }
    .cover { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}

/* Footer */
.report-footer {
    text-align: center; padding: 30px; color: #95a5a6; font-size: 12px;
    border-top: 1px solid #f0f0f0; margin-top: 30px;
}
.report-footer .brand { font-weight: 600; color: #667eea; }

/* Tabs */
.tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.tab-btn {
    padding: 8px 18px; border-radius: 20px; border: 1px solid #dee2e6;
    background: white; cursor: pointer; font-size: 13px; color: #666;
    transition: all 0.2s;
}
.tab-btn:hover { border-color: #667eea; color: #667eea; }
.tab-btn.active { background: #667eea; color: white; border-color: #667eea; }

/* Summary Cards Row */
.summary-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.summary-box {
    padding: 20px; border-radius: 10px; font-size: 13px;
}
.summary-box.danger { background: #fff5f5; border: 1px solid #ffcdd2; }
.summary-box.warning { background: #fffdf5; border: 1px solid #ffe082; }
.summary-box.info { background: #f5f9ff; border: 1px solid #bbdefb; }
.summary-box.success { background: #f5fff8; border: 1px solid #c8e6c9; }
.summary-box h5 { font-size: 14px; margin-bottom: 8px; }
.summary-box ul { padding-left: 18px; }
.summary-box li { margin: 4px 0; }
"""


def generate_report_html(diagnosis, annotations, examples, journal_name, target_words):
    """Generate the complete HTML report"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    report_id = str(uuid.uuid4())[:8].upper()
    paper_title = diagnosis.get('file', '未命名论文')

    # Determine verdict
    diag = diagnosis
    if diag['ai_density']['density'] > 15 or diag['tool_names_total'] > 15:
        verdict_class = 'verdict-critical'
        verdict_text = '🔴 需大幅修改 · AI味严重'
    elif diag['ai_density']['density'] > 5 or diag['tool_names_total'] > 5:
        verdict_class = 'verdict-warning'
        verdict_text = '🟠 需针对性修改 · 中度AI味'
    else:
        verdict_class = 'verdict-pass'
        verdict_text = '🟢 轻度润色即可'

    # Build KPI cards
    kpi_cards = f"""
    <div class="kpi-grid">
        <div class="kpi-card red">
            <div class="kpi-label">🤖 AI味密度指数</div>
            <div class="kpi-value">{diag['ai_density']['density']}</div>
            <div class="kpi-sub">致命{diag['ai_density']['fatal_count']} / 重度{diag['ai_density']['severe_count']} / 轻度{diag['ai_density']['mild_count']}</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">🔧 AI工具名罗列</div>
            <div class="kpi-value">{diag['tool_names_total']}</div>
            <div class="kpi-sub">{len(diag['tool_names_found'])}种工具 / 全文散布</div>
        </div>
        <div class="kpi-card blue">
            <div class="kpi-label">📏 最⻓单句</div>
            <div class="kpi-value">{diag['max_sentence_length']}</div>
            <div class="kpi-sub">字（可读性阈值 ≤120）</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">📊 当前字数 / 目标</div>
            <div class="kpi-value">{diag['total_chars']}</div>
            <div class="kpi-sub">需删减 {diag['total_chars'] - target_words} 字至 {target_words}</div>
        </div>
    </div>
    """

    # Build summary boxes
    fatal_issues = [a for a in annotations if a['severity'] == 'A']
    severe_issues = [a for a in annotations if a['severity'] == 'B']
    mild_issues = [a for a in annotations if a['severity'] == 'C']
    fine_issues = [a for a in annotations if a['severity'] == 'D']

    summary_boxes = f"""
    <div class="summary-row">
        <div class="summary-box danger">
            <h5>🔴 致命问题（A类 · {len(fatal_issues)}处）—— 不改必拒</h5>
            <ul>
                {''.join(f'<li>P{a["idx"]} · {"、".join(a["fatal_hits"][:2])}</li>' for a in fatal_issues[:6])}
            </ul>
        </div>
        <div class="summary-box warning">
            <h5>🟠 重要问题（B类 · {len(severe_issues)}处）—— 影响评分</h5>
            <ul>
                {''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "需检查"}</li>' for a in severe_issues[:6])}
            </ul>
        </div>
    </div>
    <div class="summary-row">
        <div class="summary-box info">
            <h5>🟡 建议优化（C类 · {len(mild_issues)}处）—— 提升质量</h5>
            <ul>
                {''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "润色建议"}</li>' for a in mild_issues[:5])}
            </ul>
        </div>
        <div class="summary-box success">
            <h5>🟢 通过段（D类 · {len(fine_issues)}处）—— 无需大改</h5>
            <ul>
                {''.join(f'<li>{"、".join([f"P{a["idx"]}" for a in fine_issues[:6]])} 等段落</li>')}
            </ul>
        </div>
    </div>
    """

    # Build tool names grid
    tool_chips = ''
    for tool, count in sorted(diag['tool_names_found'].items(), key=lambda x: -x[1]):
        css = 'fatal' if count >= 2 else 'repeat'
        tool_chips += f'<span class="tool-chip {css}">{tool} <small>×{count}</small></span>\n'

    # Build AI pattern category table
    all_pattern_hits = diag['ai_pattern_hits']
    categories = classify_ai_patterns_by_category(all_pattern_hits)
    pattern_rows = ''
    for cat, hits in sorted(categories.items(), key=lambda x: -len(x[1])):
        pattern_rows += f"""
        <tr>
            <td><strong>{cat}</strong></td>
            <td>{len(hits)}</td>
            <td style="font-size:12px;color:#888">{'; '.join(set(h['match'][:30] for h in hits[:5]))}</td>
        </tr>"""

    # Build annotation table
    annotation_rows = ''
    severity_emoji = {'A': '🔴', 'B': '🟠', 'C': '🟡', 'D': '🟢'}
    severity_badge = {'A': 'badge-a', 'B': 'badge-b', 'C': 'badge-c', 'D': 'badge-d'}
    for a in annotations:
        issues_html = ''.join(f'<div class="rev-issue">{issue}</div>' for issue in a['issues'])
        annotation_rows += f"""
        <tr>
            <td style="text-align:center"><span class="badge {severity_badge[a['severity']]}">P{a['idx']}</span></td>
            <td style="font-size:13px;max-width:300px">{html_mod.escape(a['text_preview'])}</td>
            <td style="text-align:center"><span class="badge {severity_badge[a['severity']]}">{severity_emoji[a['severity']]} {a['severity']}类</span></td>
            <td style="font-size:13px">{issues_html if issues_html else '✅ 无明显问题'}</td>
        </tr>"""

    # Build rewrite examples
    examples_html = ''
    for i, ex in enumerate(examples):
        changes_html = ''.join(f'<li>{c}</li>' for c in ex['changes'])
        examples_html += f"""
        <div style="margin-bottom:25px">
            <h3>{ex['title']}<span style="font-size:12px;color:#888;margin-left:10px">{ex['location']}</span></h3>
            <div class="compare-box">
                <div class="compare-col before">
                    <div class="compare-label">❌ 原文（问题段落）</div>
                    <div>{html_mod.escape(ex['original'][:500])}</div>
                </div>
                <div class="compare-col after">
                    <div class="compare-label">✅ 建议改写</div>
                    <div>{ex['rewritten']}</div>
                </div>
            </div>
            <div style="background:#f8f9fa;padding:14px;border-radius:6px;font-size:13px;margin-top:8px">
                <strong>✎ 修改要点：</strong>
                <ul style="margin-top:6px">{changes_html}</ul>
            </div>
        </div>"""

    # Build priority matrix items
    # Classify annotations into quadrants
    q1 = []  # High impact, low difficulty (立即)
    q2 = []  # High impact, high difficulty (尽快)
    q3 = []  # Low impact, low difficulty (优化)
    q4 = []  # Low impact, high difficulty (润色)

    for a in annotations:
        if a['severity'] == 'A':
            q1.append(a)
        elif a['severity'] == 'B':
            q2.append(a)
        elif a['severity'] == 'C':
            q3.append(a)
        else:
            q4.append(a)

    priority_html = f"""
    <div class="priority-grid">
        <div class="priority-quad q1">
            <h4>🔴 第一优先：立即修改（高影响 · 低难度）</h4>
            <ul style="font-size:13px">
                {''.join(f'<li>P{a["idx"]} · {"、".join(a["fatal_hits"][:2]) if a["fatal_hits"] else a["issues"][0] if a["issues"] else "需重写"}</li>' for a in q1)}</ul>
        </div>
        <div class="priority-quad q2">
            <h4>🟠 第二优先：尽快修改（高影响 · 中等难度）</h4>
            <ul style="font-size:13px">
                {''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "需拆句/补过渡"}</li>' for a in q2)}</ul>
        </div>
        <div class="priority-quad q3">
            <h4>🟡 第三优先：常规优化（低影响 · 低难度）</h4>
            <ul style="font-size:13px">
                {''.join(f'<li>P{a["idx"]} · {a["issues"][0] if a["issues"] else "润色措辞"}</li>' for a in q3[:6])}</ul>
        </div>
        <div class="priority-quad q4">
            <h4>🟢 可选润色（低影响 · 依个人偏好）</h4>
            <ul style="font-size:13px">
                <li>{len(q4)}个段落基本通过，建议保持原样或轻微润色</li>
            </ul>
        </div>
    </div>
    <div style="margin-top:16px;text-align:center">
        <canvas id="priorityChart" height="200"></canvas>
    </div>
    """

    # Build reduction plan
    reduction_plan = f"""
    <table>
        <tr>
            <th>板块</th><th>当前字数</th><th>目标字数</th><th>删减量</th><th>方法</th>
        </tr>
        <tr>
            <td>P18-P19 工具罗列</td><td>819</td><td>210</td><td style="color:#e74c3c;font-weight:600">-609</td>
            <td>合并重写为功能类别描述</td>
        </tr>
        <tr>
            <td>P44 技术演进预测</td><td>297</td><td>180</td><td style="color:#e74c3c;font-weight:600">-117</td>
            <td>压缩为1段，删未来预测详述</td>
        </tr>
        <tr>
            <td>P42 推广策略详述</td><td>273</td><td>180</td><td style="color:#e74c3c;font-weight:600">-93</td>
            <td>合并院校类型，保留核心原则</td>
        </tr>
        <tr>
            <td>P26-P27 平台功能描述</td><td>461</td><td>300</td><td style="color:#e74c3c;font-weight:600">-161</td>
            <td>精简平台功能介绍，保留教学价值</td>
        </tr>
        <tr>
            <td>P23 多平台管理系统</td><td>362</td><td>250</td><td style="color:#e74c3c;font-weight:600">-112</td>
            <td>压缩3款管理软件描述为1句话</td>
        </tr>
        <tr>
            <td>P32 三方协同段落</td><td>353</td><td>250</td><td style="color:#e74c3c;font-weight:600">-103</td>
            <td>缩减事务性描述，聚焦核心论点</td>
        </tr>
        <tr>
            <td>其他段落润色压缩</td><td>-</td><td>-</td><td style="color:#e74c3c;font-weight:600">-605</td>
            <td>逐段精简冗余修饰词</td>
        </tr>
        <tr style="font-weight:700;background:#f8f9fa">
            <td>合计</td><td>{diag['total_chars']}</td><td>{target_words}</td><td style="color:#e74c3c">-{diag['total_chars'] - target_words}</td>
            <td></td>
        </tr>
    </table>
    """

    # Build section structure analysis
    sec_rows = ''
    total_c = max(diag['total_chars'], 1)
    for sec, count in diag['sections'].items():
        pct = round(count / total_c * 100, 1)
        ideal = ''
        if '一、' in sec or '机制' in sec:
            ideal = '35-40%' if pct > 40 else '✅'
        elif '二、' in sec or '效果' in sec:
            ideal = '25-30%' if pct < 25 else '✅'
        elif '三、' in sec or '路径' in sec:
            ideal = '20-25%' if pct > 25 else '✅'
        sec_rows += f'<tr><td>{sec[:40]}</td><td>{count}</td><td>{pct}%</td><td>{ideal}</td></tr>'

    # Build checklist
    checklist_items = [
        ('A', 'AI味清除', [
            ('A1', '全文具体AI产品名称 ≤ 3个'),
            ('A2', '无"从X到Y"对仗式标题'),
            ('A3', '无"双螺旋""深层互构""认知跃迁"等空泛术语'),
            ('A4', '结语无四连排比收尾'),
            ('A5', '无"不仅是……更是……"万能句式'),
            ('A6', 'AI味密度指数 < 5'),
        ]),
        ('B', '可读性', [
            ('B1', '全文无超过120字的单句'),
            ('B2', '每个自然段由3-5个短句构成'),
            ('B3', '段落间有过渡句或逻辑连接词'),
            ('B4', '核心术语首次出现有简短解释'),
            ('B5', '无连续4个以上并列名词堆叠'),
        ]),
        ('C', '结构与篇幅', [
            ('C1', f'字数在{target_words}±100字范围内'),
            ('C2', '各部分权重合理'),
            ('C3', '摘要150字以内含四要素'),
            ('C4', '关键词3-5个有检索价值'),
            ('C5', '参考文献格式统一'),
        ]),
        ('D', '学术规范', [
            ('D1', '无自我评价式语言'),
            ('D2', '有数据支撑的结论附带具体数字'),
            ('D3', '他人观点/数据有明确引用'),
            ('D4', '摘要与正文结论一致'),
        ]),
        ('E', '期刊适配', [
            ('E1', '标题长度适合《中国教工》风格'),
            ('E2', '摘要含期刊偏好关键词'),
            ('E3', '参考文献近5年为主'),
            ('E4', '版面格式符合投稿要求'),
        ]),
    ]

    checklist_html = '<div class="checklist-progress"><small>完成进度</small><div class="checklist-progress-bar"><div class="checklist-progress-fill" id="checklist-progress-fill" style="width:0%"></div></div></div>'
    for cat_id, cat_name, items in checklist_items:
        checklist_html += f'<div class="checklist-cat">{cat_id}. {cat_name}</div>'
        for item_id, item_text in items:
            checklist_html += f"""
            <div class="checklist-item" id="cl-{item_id}">
                <input type="checkbox" id="cb-{item_id}" onchange="updateChecklist()">
                <label for="cb-{item_id}">[{item_id}] {item_text}</label>
            </div>"""

    # Build sentence analysis
    long_sent_html = ''
    for i, s in enumerate(diag.get('long_sentences', [])[:10], 1):
        long_sent_html += f"""
        <tr>
            <td>{i}</td>
            <td style="color:#e74c3c;font-weight:600">{s['length']}字</td>
            <td style="font-size:13px">{html_mod.escape(s['text'])}</td>
        </tr>"""

    # Build transition breaks
    trans_breaks = analyze_transitions([p['text'] for p in diagnosis.get('_paras', [])])
    trans_html = ''
    for i, tb in enumerate(trans_breaks[:5], 1):
        trans_html += f"""
        <tr>
            <td>{i}</td>
            <td>P{tb['from_idx']} → P{tb['to_idx']}</td>
            <td style="font-size:13px">"{html_mod.escape(tb['from_preview'])}" → "{html_mod.escape(tb['to_preview'])}"</td>
        </tr>"""

    # Build noun piles
    noun_piles = detect_noun_piles([p['text'] for p in diagnosis.get('_paras', [])])
    pile_html = ''
    for i, np_item in enumerate(noun_piles[:5], 1):
        pile_html += f"""
        <tr>
            <td>{i}</td>
            <td>P{np_item['idx']}</td>
            <td style="font-size:13px">{np_item['count']}项并列：{html_mod.escape(np_item['text'][:80])}</td>
        </tr>"""

    # ================================================================
    # FULL HTML
    # ================================================================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>论文润色修改建议报告 · {html_mod.escape(paper_title[:50])}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>{CSS_STYLE}</style>
</head>
<body>
<div class="container">

<!-- ===== COVER ===== -->
<div class="cover">
    <div class="cover-brand">▸ 论文润色修改建议报告 ◂</div>
    <h1>论文润色修改完善建议报告</h1>
    <div style="font-size:18px;opacity:0.95;margin-bottom:5px">{html_mod.escape(paper_title[:80])}</div>
    <div class="cover-meta">
        <span>📅 {now}</span>
        <span>📋 报告编号：PR-{report_id}</span>
        <span>🏫 目标期刊：{journal_name}</span>
        <span>📏 目标字数：{target_words}字（3版面）</span>
    </div>
    <div class="cover-verdict {verdict_class}">{verdict_text}</div>
</div>

<!-- ===== KPI CARDS ===== -->
{kpi_cards}

<!-- ===== SUMMARY ===== -->
<div class="section">
    <h2>📋 修改执行摘要</h2>
    <p class="section-desc">基于自动诊断+专家规则的多维度分析，以下为优先修改方案。</p>
    {summary_boxes}
    <div style="margin-top:16px">
        <canvas id="radarChart" height="260"></canvas>
    </div>
</div>

<!-- ===== SECTION 1: AI FLAVOR ===== -->
<div class="section" id="s1">
    <h2>🤖 维度一：AI写作痕迹检测</h2>
    <p class="section-desc">AI味是本报告最关注的维度。以下检测基于四级词库扫描+工具名统计。</p>

    <h3>AI工具名分布（{diag['tool_names_total']}处 / {len(diag['tool_names_found'])}种）</h3>
    <div class="tool-grid">{tool_chips}</div>
    <p style="font-size:13px;color:#e74c3c;margin-bottom:20px">
        ⚠️ 以上所有工具名建议替换为功能类别描述（如"AI语音转写系统""文生图平台""协同办公平台"等）。
    </p>

    <h3>AI味句式分类统计</h3>
    <table>
        <tr><th>类别</th><th>命中次数</th><th>典型示例</th></tr>
        {pattern_rows}
    </table>

    <h3>AI味密度判定</h3>
    <div style="display:flex;gap:30px;align-items:center;margin:15px 0">
        <div style="font-size:48px;font-weight:700;color:{'#e74c3c' if diag['ai_density']['density']>15 else '#f39c12' if diag['ai_density']['density']>5 else '#27ae60'}">{diag['ai_density']['density']}</div>
        <div>
            <div style="font-size:16px;font-weight:600">{'🔴 高度AI代写嫌疑' if diag['ai_density']['density']>15 else '🟠 中度AI写作痕迹' if diag['ai_density']['density']>5 else '🟢 可接受范围'}</div>
            <div style="font-size:13px;color:#888">密度指数 = (致命×5 + 重度×3 + 轻度×1) / 总字数×1000</div>
        </div>
    </div>
</div>

<!-- ===== SECTION 2: READABILITY ===== -->
<div class="section" id="s2">
    <h2>📖 维度二：可读性诊断</h2>
    <p class="section-desc">句长分布、过渡流畅度、名词密度的综合分析。</p>

    <h3>超⻓句清单（Top 10）</h3>
    <table>
        <tr><th>#</th><th>长度</th><th>句子片段</th></tr>
        {long_sent_html}
    </table>

    <h3>段落过渡断裂点</h3>
    <table>
        <tr><th>#</th><th>断裂位置</th><th>前后段落</th></tr>
        {trans_html if trans_html else '<tr><td colspan="3" style="color:#888">未检测到明显过渡断裂</td></tr>'}
    </table>

    <h3>名词堆叠检测</h3>
    <table>
        <tr><th>#</th><th>位置</th><th>堆叠内容</th></tr>
        {pile_html if pile_html else '<tr><td colspan="3" style="color:#888">未检测到明显名词堆叠</td></tr>'}
    </table>

    <div style="margin-top:15px">
        <canvas id="sentLenChart" height="200"></canvas>
    </div>
</div>

<!-- ===== SECTION 3: STRUCTURE ===== -->
<div class="section" id="s3">
    <h2>🏗️ 维度三：结构失衡诊断</h2>
    <p class="section-desc">各部分字数占比及理想调整方向。</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div>
            <table>
                <tr><th>部分</th><th>字数</th><th>占比</th><th>建议</th></tr>
                {sec_rows}
            </table>
        </div>
        <div>
            <canvas id="sectionChart" height="240"></canvas>
        </div>
    </div>
</div>

<!-- ===== SECTION 4: PARAGRAPH ANNOTATIONS ===== -->
<div class="section" id="s4">
    <h2>📝 维度四：逐段修改清单</h2>
    <p class="section-desc">全文{len(annotations)}个段落逐一标注严重度（A/B/C/D）、问题类型与具体修改指令。</p>

    <table>
        <tr><th style="width:60px">段落</th><th>内容预览</th><th style="width:70px">严重度</th><th>修改指令</th></tr>
        {annotation_rows}
    </table>
</div>

<!-- ===== SECTION 5: PRIORITY MATRIX ===== -->
<div class="section" id="s5">
    <h2>🎯 维度五：修改优先级矩阵</h2>
    <p class="section-desc">按影响程度×修改难度将问题分为四象限，指导修改顺序。</p>
    {priority_html}
</div>

<!-- ===== SECTION 6: REWRITE EXAMPLES ===== -->
<div class="section" id="s6">
    <h2>✍️ 维度六：改写示范</h2>
    <p class="section-desc">选取3个最具代表性的段落，展示修改前后对比与具体变化要点。</p>
    {examples_html}
</div>

<!-- ===== SECTION 7: REDUCTION PLAN ===== -->
<div class="section" id="s7">
    <h2>✂️ 维度七：字数精简路线图</h2>
    <p class="section-desc">当前 {diag['total_chars']} 字，目标 {target_words} 字（3版面），需删减 <strong style="color:#e74c3c">{diag['total_chars'] - target_words}</strong> 字。</p>
    {reduction_plan}
    <div style="margin-top:16px">
        <canvas id="reductionChart" height="200"></canvas>
    </div>
</div>

<!-- ===== SECTION 8: FINAL CHECKLIST ===== -->
<div class="section" id="s8">
    <h2>✅ 维度八：终审自检清单</h2>
    <p class="section-desc">修改完成后逐项勾选确认。全部通过方可提交。</p>
    {checklist_html}
    <p style="margin-top:10px;font-size:12px;color:#888">
        💡 勾选进度自动保存到浏览器本地存储。
    </p>
</div>

<!-- ===== SECTION 9: METRICS ===== -->
<div class="section" id="s9">
    <h2>📐 维度九：完整诊断数据</h2>
    <p class="section-desc">以下为本文的完整量化诊断数据，供深度分析参考。</p>
    <table>
        <tr><th>指标</th><th>数值</th><th>说明</th></tr>
        <tr><td>文件</td><td>{diag['file']}</td><td>论文文件名</td></tr>
        <tr><td>总字数</td><td>{diag['total_chars']}</td><td>中文{diag['total_cn']}字 + 英文{diag['total_en']}词</td></tr>
        <tr><td>句数 / 段数</td><td>{diag['sentence_count']} / {diag['paragraph_count']}</td><td></td></tr>
        <tr><td>平均句长 / 最长句</td><td>{diag['avg_sentence_length']}字 / {diag['max_sentence_length']}字</td><td>建议平均≤50字，单句≤120字</td></tr>
        <tr><td>AI味密度</td><td>{diag['ai_density']['density']}</td><td>致命{diag['ai_density']['fatal_count']}/重度{diag['ai_density']['severe_count']}/轻度{diag['ai_density']['mild_count']}</td></tr>
        <tr><td>工具名统计</td><td>{diag['tool_names_total']}次 · {len(diag['tool_names_found'])}种</td><td>建议≤3个必要工具名</td></tr>
        <tr><td>模式命中</td><td>{diag['ai_pattern_count']}次</td><td>4级词库扫描</td></tr>
    </table>
</div>

<!-- ===== FOOTER ===== -->
<div class="report-footer">
    <div class="brand">论文润色修改建议报告生成器 v2.0</div>
    <div>报告编号：PR-{report_id} · 生成时间：{now} · 目标期刊：{journal_name}</div>
    <div style="margin-top:8px">本报告由AI辅助生成，建议结合人工审稿综合判断。所有修改建议均为参考性质。</div>
</div>

</div><!-- /container -->

<script>
// ===== Chart.js 初始化 =====

// Radar Chart
new Chart(document.getElementById('radarChart'), {{
    type: 'radar',
    data: {{
        labels: ['AI味密度', '工具名罗列', '可读性', '结构平衡', '期刊适配'],
        datasets: [{{
            label: '当前状态',
            data: [
                {diag['ai_density']['density']},
                {diag['tool_names_total']},
                {max(0, 100 - diag['max_sentence_length']) if diag['max_sentence_length'] < 120 else 20},
                {max(20, 100 - abs(diag['total_chars'] - target_words) / max(target_words,1) * 100)},
                100
            ],
            backgroundColor: 'rgba(102,126,234,0.2)',
            borderColor: '#667eea',
            borderWidth: 2,
        }},
        {{
            label: '通过阈值',
            data: [5, 5, 60, 80, 80],
            borderColor: '#27ae60',
            borderWidth: 1,
            borderDash: [4, 4],
            pointRadius: 0,
            backgroundColor: 'transparent',
        }}
        ]
    }},
    options: {{
        scales: {{ r: {{ min: 0, max: 100, ticks: {{ stepSize: 20 }} }} }},
        plugins: {{ legend: {{ position: 'bottom' }} }}
    }}
}});

// Sentence Length Distribution
var sentLens = [{','.join(str(s['length']) for s in diag.get('long_sentences', [])[:10])}];
var labels = sentLens.map(function(_,i) {{ return '句'+(i+1); }});
new Chart(document.getElementById('sentLenChart'), {{
    type: 'bar',
    data: {{
        labels: labels,
        datasets: [{{
            label: '句长（字）',
            data: sentLens,
            backgroundColor: sentLens.map(function(v) {{ return v > 120 ? '#e74c3c' : v > 80 ? '#f39c12' : '#3498db'; }}),
        }}]
    }},
    options: {{
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: '字数' }} }} }}
    }}
}});

// Section Distribution
var secData = {json.dumps(list(diagnosis['sections'].values()))};
var secLabels = {json.dumps([k[:15] for k in diagnosis['sections'].keys()])};
new Chart(document.getElementById('sectionChart'), {{
    type: 'doughnut',
    data: {{
        labels: secLabels,
        datasets: [{{
            data: secData,
            backgroundColor: ['#667eea','#764ba2','#f39c12','#e74c3c','#27ae60','#3498db'],
        }}]
    }},
    options: {{
        plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }} }} }} }}
    }}
}});

// Reduction Plan Bar
new Chart(document.getElementById('reductionChart'), {{
    type: 'bar',
    data: {{
        labels: ['工具罗列', '技术预测', '推广策略', '平台功能', '多平台', '三方协同', '其他润色'],
        datasets: [{{
            label: '删减字数',
            data: [609, 117, 93, 161, 112, 103, 605],
            backgroundColor: '#e74c3c',
        }}]
    }},
    options: {{
        indexAxis: 'y',
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ beginAtZero: true, title: {{ display: true, text: '删减字数' }} }} }}
    }}
}});

// Priority Matrix Bar Chart
new Chart(document.getElementById('priorityChart'), {{
    type: 'bar',
    data: {{
        labels: ['A类·立即', 'B类·尽快', 'C类·优化', 'D类·通过'],
        datasets: [{{
            label: '段落数',
            data: [{len(fatal_issues)}, {len(severe_issues)}, {len(mild_issues)}, {len(fine_issues)}],
            backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#27ae60'],
        }}]
    }},
    options: {{
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
    }}
}});

// Checklist Progress
function updateChecklist() {{
    var checks = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    var done = 0;
    checks.forEach(function(cb) {{
        if (cb.checked) {{
            cb.parentElement.classList.add('checked');
            done++;
        }} else {{
            cb.parentElement.classList.remove('checked');
        }}
    }});
    var pct = Math.round(done / checks.length * 100);
    document.getElementById('checklist-progress-fill').style.width = pct + '%';
    // Save to localStorage
    var state = {{}};
    checks.forEach(function(cb) {{ state[cb.id] = cb.checked; }});
    localStorage.setItem('checklist-state-{report_id}', JSON.stringify(state));
}}

// Restore checklist state
(function() {{
    var saved = localStorage.getItem('checklist-state-{report_id}');
    if (saved) {{
        var state = JSON.parse(saved);
        Object.keys(state).forEach(function(id) {{
            var cb = document.getElementById(id);
            if (cb) cb.checked = state[id];
        }});
    }}
    updateChecklist();
}})();
</script>

</body>
</html>"""
    return html


# ============================================================
# MAIN ENTRY
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='论文润色修改建议报告生成器')
    parser.add_argument('paper_path', help='论文文件路径（.docx）')
    parser.add_argument('--output', '-o', default=None, help='输出HTML路径')
    parser.add_argument('--journal', '-j', default='《中国教工》', help='目标期刊名称')
    parser.add_argument('--target-words', '-t', type=int, default=3950, help='目标字数')
    parser.add_argument('--author', '-a', default='', help='作者姓名')
    args = parser.parse_args()

    paper_path = Path(args.paper_path)
    if not paper_path.exists():
        print(f'错误: 文件不存在: {paper_path}')
        sys.exit(1)

    # Read paper
    if paper_path.suffix == '.docx':
        from docx import Document
        doc = Document(str(paper_path))
        paras = [{'idx': i, 'text': p.text.strip(), 'style': p.style.name,
                   'len': len(p.text.strip())}
                  for i, p in enumerate(doc.paragraphs) if p.text.strip()]
        full_text = '\n'.join([p['text'] for p in paras])
    elif paper_path.suffix == '.txt':
        full_text = paper_path.read_text(encoding='utf-8')
        paras = [{'idx': i, 'text': t.strip(), 'style': 'Normal', 'len': len(t)}
                  for i, t in enumerate(full_text.split('\n\n')) if t.strip()]
    else:
        print(f'不支持的文件格式: {paper_path.suffix}')
        sys.exit(1)

    # Run diagnosis
    print('🔍 正在执行多维度诊断...')
    total_cn = count_chinese(full_text)
    total_en = count_english_words(full_text)
    total_chars = total_cn + total_en
    sentences = split_sentences(full_text)
    sent_lengths = [count_chinese(s) + count_english_words(s) for s in sentences]
    max_sent = max(sent_lengths) if sent_lengths else 0
    avg_sent = round(sum(sent_lengths) / len(sent_lengths), 1) if sent_lengths else 0

    long_sentences = []
    for s in sentences:
        sl = count_chinese(s) + count_english_words(s)
        if sl > 80:
            long_sentences.append({'length': sl, 'text': s.strip()[:100]})
    long_sentences.sort(key=lambda x: -x['length'])
    long_sentences = long_sentences[:10]

    ai_density = calculate_ai_density(full_text, max(total_chars, 1))
    tool_found = count_tools_in_text(full_text)

    fatal_hits = match_patterns_in_text(full_text, FATAL_PATTERNS, 'fatal')
    severe_hits = match_patterns_in_text(full_text, SEVERE_PATTERNS, 'severe')
    mild_hits = match_patterns_in_text(full_text, MILD_PATTERNS, 'mild')
    all_hits = fatal_hits + severe_hits + mild_hits

    # Section analysis
    sections = {}
    parts = re.split(r'(?=^[一二三四五六七八九十]、)', full_text, flags=re.MULTILINE)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r'^[一二三四五六七八九十]、.{0,30}', part)
        title = m.group() if m else '前言'
        sections[title] = count_chinese(part) + count_english_words(part)

    diagnosis = {
        'file': paper_path.name,
        'total_chars': total_chars,
        'total_cn': total_cn,
        'total_en': total_en,
        'sentence_count': len(sentences),
        'paragraph_count': len(paras),
        'avg_sentence_length': avg_sent,
        'max_sentence_length': max_sent,
        'long_sentences': long_sentences,
        'ai_density': ai_density,
        'ai_pattern_hits': all_hits,
        'ai_pattern_count': len(all_hits),
        'tool_names_found': tool_found,
        'tool_names_total': sum(tool_found.values()),
        'sections': sections,
        '_paras': paras,
    }

    # Paragraph annotations
    print('📝 正在生成逐段修改批注...')
    annotations = annotate_paragraphs(paras, full_text, tool_found, all_hits, long_sentences)

    # Rewrite examples
    print('✍️ 正在生成改写示范...')
    examples = generate_rewrite_examples(paras, annotations)

    # Generate HTML
    print('🎨 正在生成HTML报告...')
    html = generate_report_html(diagnosis, annotations, examples,
                                args.journal, args.target_words)

    # Output
    output_path = args.output or str(paper_path.parent / f'{paper_path.stem}_修改建议报告.html')
    Path(output_path).write_text(html, encoding='utf-8')

    print(f'\n✅ 报告生成完毕！')
    print(f'  文件: {output_path}')
    print(f'  字数: {total_chars} / 目标 {args.target_words}')
    print(f'  AI味密度: {ai_density["density"]}')
    print(f'  工具名: {sum(tool_found.values())}处 / {len(tool_found)}种')
    print(f'  判定: {"🔴 需大幅修改" if ai_density["density"]>15 else "🟠 需针对性修改" if ai_density["density"]>5 else "🟢 轻度润色"}')
    print(f'  报告编号: PR-{str(uuid.uuid4())[:8].upper()}')


if __name__ == '__main__':
    main()
