#!/usr/bin/env python3
"""
论文全息诊断脚本 —— paper-revision-sop Phase 1
用法: python diagnose_paper.py <论文路径> [--format json|text]

输出指标:
  - 总字数、句数、段数
  - 平均句长 / 最长句
  - AI味密度指数
  - 工具名罗列次数
  - 各部分字数占比
  - 致命级模式匹配详情
"""

import re
import json
import sys
import os
from pathlib import Path

# ============ AI味检测词库 ============

FATAL_PATTERNS = [
    # 标题模板
    (r'从.{2,8}到.{2,8}[：:].{4,}', '标题模板'),
    # 排比收尾
    (r'(以.{2,10}为.{2,10}[，,]?\s*){4,}', '四连排比'),
    # 概念拔高
    (r'双螺旋结构', '生物学隐喻'),
    (r'深层互构', '空泛概念'),
    (r'认知跃迁', '空泛概念'),
    (r'信息平权', '空泛概念'),
    (r'群体智慧', '空泛概念'),
    (r'底层逻辑', '空泛概念'),
    (r'范式转换', '空泛概念'),
    # 空泛收尾
    (r'为.+提供理论参照与实践镜鉴', '空泛收尾'),
    (r'有待进一步深化与拓展', '空泛收尾'),
]

SEVERE_PATTERNS = [
    (r'不仅是.+更是', '万能句式'),
    (r'从.+层面.+从.+维度.+从.+视角', '多维度排比'),
    (r'实现了.+的有机统一', '套话'),
    (r'为.+奠定了坚实基础', '套话'),
    (r'推动.+从.+向.+转变', '套话'),
]

MILD_PATTERNS = [
    (r'显著提升', '模糊量化'),
    (r'大幅改善', '模糊量化'),
    (r'明显增强', '模糊量化'),
    (r'有效促进', '模糊量化'),
    (r'积极推动', '模糊量化'),
]

# 🔵 需替换的工具名（检测并统计）
TOOL_NAMES = [
    '秘塔', 'Kimi', '豆包', 'DeepSeek', '天工', '橙篇',
    '通义听悟', '新华妙笔', 'Grammarly', '即梦', '海螺',
    '可灵', 'Vidu', '腾讯混元', '飞书多维表格', '扣子',
    'ChatExcel', '办公小浣熊', 'Perplexity', 'Claude', 'Gemini',
    '高赛通', '智慧无形', '文香', '校友邦', '超星学习通',
    '汇雅', '豆包人工智能播客', '秘塔今天学点啥',
]

# ============ 诊断函数 ============

def count_chinese(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def count_english_words(text):
    return len(re.findall(r'[a-zA-Z]+', text))

def split_sentences(text):
    """按中文句号、问号、感叹号分句"""
    return [s.strip() for s in re.split(r'[。！？!?]', text) if s.strip()]

def count_tools(text):
    """统计工具名出现次数"""
    found = {}
    for tool in TOOL_NAMES:
        count = len(re.findall(re.escape(tool), text))
        if count > 0:
            found[tool] = count
    return found

def match_patterns(text, patterns, level):
    """匹配模式并返回命中详情"""
    hits = []
    for pattern, label in patterns:
        for m in re.finditer(pattern, text):
            start = max(0, m.start() - 10)
            end = min(len(text), m.end() + 10)
            context = text[start:end].replace('\n', ' ')
            hits.append({
                'level': level,
                'label': label,
                'match': m.group(),
                'context': f'...{context}...',
                'position': m.start()
            })
    return hits

def calculate_ai_density(text, total_chars):
    """计算AI味密度指数"""
    fatal_count = sum(1 for p, _ in FATAL_PATTERNS if re.search(p, text))
    severe_count = sum(1 for p, _ in SEVERE_PATTERNS if re.search(p, text))
    mild_count = sum(1 for p, _ in MILD_PATTERNS if re.search(p, text))
    score = fatal_count * 5 + severe_count * 3 + mild_count * 1
    density = (score / total_chars * 1000) if total_chars > 0 else 0
    return {
        'fatal_count': fatal_count,
        'severe_count': severe_count,
        'mild_count': mild_count,
        'raw_score': score,
        'density': round(density, 2)
    }

def section_word_count(text):
    """分析各部分字数"""
    sections = {}
    # 匹配一级标题: 一、二、三、... 或 (一)(二)(三)
    parts = re.split(r'(?=^[一二三四五六七八九十]、)', text, flags=re.MULTILINE)
    if len(parts) <= 1:
        parts = re.split(r'(?=^（[一二三四五六七八九十]）)', text, flags=re.MULTILINE)

    for part in parts:
        part = part.strip()
        if not part:
            continue
        # 提取标题
        title_match = re.match(r'^[一二三四五六七八九十]、|^（[一二三四五六七八九十]）', part)
        if title_match:
            title = part[:part.find('\n')].strip() if '\n' in part else part[:30]
        else:
            title = '前言'
        cn = count_chinese(part)
        en = count_english_words(part)
        sections[title] = cn + en

    return sections

def diagnose(filepath):
    """主诊断函数"""
    # 读取文件
    path = Path(filepath)
    if path.suffix == '.docx':
        try:
            from docx import Document
            doc = Document(filepath)
            text = '\n'.join([p.text for p in doc.paragraphs])
        except ImportError:
            # Fallback: 尝试转txt
            text = "ERROR: python-docx not available for DOCX parsing"
    elif path.suffix == '.txt':
        text = path.read_text(encoding='utf-8')
    elif path.suffix == '.md':
        text = path.read_text(encoding='utf-8')
    else:
        text = path.read_text(encoding='utf-8')

    total_cn = count_chinese(text)
    total_en = count_english_words(text)
    total_chars = total_cn + total_en
    sentences = split_sentences(text)
    sent_lengths = [count_chinese(s) + count_english_words(s) for s in sentences]
    max_sent = max(sent_lengths) if sent_lengths else 0
    avg_sent = round(sum(sent_lengths) / len(sent_lengths), 1) if sent_lengths else 0
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    para_count = len(paragraphs)

    # AI味检测
    fatal_hits = match_patterns(text, FATAL_PATTERNS, 'fatal')
    severe_hits = match_patterns(text, SEVERE_PATTERNS, 'severe')
    mild_hits = match_patterns(text, MILD_PATTERNS, 'mild')
    ai_density = calculate_ai_density(text, max(total_chars, 1))
    tools = count_tools(text)

    # 结构分析
    sections = section_word_count(text)

    # 超长句列表 (top 5)
    long_sents = []
    for s in sentences:
        sl = count_chinese(s) + count_english_words(s)
        if sl > 100:
            long_sents.append({'length': sl, 'text': s.strip()[:80] + ('...' if len(s) > 80 else '')})
    long_sents.sort(key=lambda x: -x['length'])
    long_sents = long_sents[:5]

    result = {
        'file': str(path.name),
        'total_chars': total_chars,
        'total_cn': total_cn,
        'total_en': total_en,
        'sentence_count': len(sentences),
        'paragraph_count': para_count,
        'avg_sentence_length': avg_sent,
        'max_sentence_length': max_sent,
        'long_sentences': long_sents,
        'ai_density': ai_density,
        'ai_pattern_hits': fatal_hits + severe_hits + mild_hits,
        'ai_pattern_count': len(fatal_hits) + len(severe_hits) + len(mild_hits),
        'tool_names_found': tools,
        'tool_names_total': sum(tools.values()),
        'sections': sections,
    }

    # 判定
    if ai_density['density'] > 15 or result['tool_names_total'] > 15:
        result['verdict'] = '🔴 高度AI代写嫌疑，建议大幅重写'
    elif ai_density['density'] > 5 or result['tool_names_total'] > 5:
        result['verdict'] = '🟠 中度AI味，需针对性修改'
    elif result['max_sentence_length'] > 120:
        result['verdict'] = '🔵 可读性不足，需拆句润色'
    else:
        result['verdict'] = '🟢 基本通过，进行润色即可'

    return result


def format_text(result):
    """人类可读输出"""
    lines = []
    lines.append(f"═══════════════════════════════════════")
    lines.append(f"  论文全息诊断报告: {result['file']}")
    lines.append(f"═══════════════════════════════════════")
    lines.append(f"")
    lines.append(f"📊 基础指标")
    lines.append(f"  总字数: {result['total_chars']} (中文{result['total_cn']} + 英文词{result['total_en']})")
    lines.append(f"  句数: {result['sentence_count']} | 段数: {result['paragraph_count']}")
    lines.append(f"  平均句长: {result['avg_sentence_length']}字 | 最长句: {result['max_sentence_length']}字")
    lines.append(f"")
    lines.append(f"🤖 AI味诊断")
    lines.append(f"  密度指数: {result['ai_density']['density']} (致命{result['ai_density']['fatal_count']}/重度{result['ai_density']['severe_count']}/轻度{result['ai_density']['mild_count']})")
    lines.append(f"  工具名罗列: {result['tool_names_total']}个/{len(result['tool_names_found'])}种")
    if result['tool_names_found']:
        tool_list = ', '.join(f'{k}×{v}' for k, v in sorted(result['tool_names_found'].items(), key=lambda x: -x[1]))
        lines.append(f"  详情: {tool_list}")
    lines.append(f"  模式命中: {result['ai_pattern_count']}次")
    lines.append(f"")
    lines.append(f"📐 结构分析")
    for sec, count in result['sections'].items():
        pct = round(count / max(result['total_chars'], 1) * 100, 1)
        lines.append(f"  {sec}: {count}字 ({pct}%)")
    lines.append(f"")
    if result.get('long_sentences'):
        lines.append(f"⚠️ 超长句 Top 5:")
        for i, s in enumerate(result['long_sentences'], 1):
            lines.append(f"  {i}. [{s['length']}字] {s['text']}")
    lines.append(f"")
    lines.append(f"📋 判定: {result['verdict']}")
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python diagnose_paper.py <论文路径.docx/.txt/.md> [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    fmt = 'text'
    if '--json' in sys.argv:
        fmt = 'json'

    result = diagnose(filepath)

    if fmt == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))
