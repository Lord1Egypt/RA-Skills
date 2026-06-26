#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪曲线分析工具
分析章节文本的情绪变化，检测章节内部和章节之间的情绪连贯性
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    from chapter_text import extract_content_from_chapter, is_chapter_file
except ModuleNotFoundError:
    from scripts.chapter_text import extract_content_from_chapter, is_chapter_file

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


EMOTION_KEYWORDS = {
    '紧张': [
        '紧张', '担忧', '焦虑', '恐惧', '害怕', '惊慌', '恐慌', '不安', '忐忑',
        '凝重', '严肃', '危险', '致命', '生死', '死亡', '威胁', '压迫',
        '心跳加速', '掌心出汗', '眉头紧锁', '咬紧牙关', '攥紧拳头',
        '剑拔弩张', '一触即发', '步步紧逼', '命悬一线', '千钧一发'
    ],
    '愤怒': [
        '愤怒', '恼怒', '怒火', '愤恨', '怨恨', '恼火', '气恼', '暴怒',
        '怒吼', '咆哮', '嘶吼', '冷笑', '讥笑', '嘲笑', '轻蔑', '不屑',
        '拳头紧握', '青筋暴起', '面色铁青', '双眼喷火', '怒火中烧',
        '杀意', '必杀', '灭口', '让你后悔', '不会放过'
    ],
    '悲伤': [
        '悲伤', '悲痛', '哀伤', '伤心', '难过', '痛苦', '绝望', '沮丧',
        '泪流满面', '热泪盈眶', '泣不成声', '掩面而泣', '失声痛哭',
        '心碎', '心酸', '苦涩', '酸楚', '无奈', '叹息', '黯然',
        '苍老', '消沉', '萎靡', '颓废', '生无可恋'
    ],
    '喜悦': [
        '喜悦', '高兴', '开心', '快乐', '兴奋', '激动', '欣喜', '狂喜',
        '大笑', '欢笑', '轻笑', '微笑', '会心一笑', '笑逐颜开', '眉开眼笑',
        '喜上眉梢', '喜形于色', '欣喜若狂', '手舞足蹈', '欢呼', '雀跃',
        '畅快', '痛快', '酣畅', '舒畅', '舒坦'
    ],
    '惊讶': [
        '惊讶', '震惊', '吃惊', '错愕', '惊愕', '意外', '惊讶', '惊叹',
        '目瞪口呆', '瞠目结舌', '难以置信', '不敢相信', '做梦也没想到',
        '什么', '怎么可能', '竟然', '居然', '居然是', '竟然是他'
    ],
    '平静': [
        '平静', '平静', '安宁', '宁静', '静谧', '安详', '祥和',
        '淡淡', '悠然', '从容', '淡定', '镇定', '冷静', '沉稳',
        '品茶', '喝茶', '闭目', '养神', '沉思', '冥想'
    ],
    '温暖': [
        '温暖', '温馨', '温情', '柔和', '柔软', '温柔', '温和',
        '心疼', '怜惜', '关爱', '关怀', '呵护', '珍惜', '珍视',
        '依偎', '拥抱', '牵手', '相视而笑', '心意相通'
    ]
}


def extract_paragraphs(text: str) -> list:
    """将文本分割成段落"""
    paragraphs = []
    current_para = []

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        elif not line.startswith('#') and not line.startswith('```'):
            current_para.append(line)

    if current_para:
        paragraphs.append(' '.join(current_para))

    return paragraphs


def analyze_paragraph_emotions(paragraph: str) -> dict:
    """分析单个段落的情绪倾向"""
    scores = defaultdict(int)

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in paragraph:
                scores[emotion] += 1

    if not scores:
        return {'dominant': 'neutral', 'scores': {}, 'intensity': 0}

    dominant = max(scores, key=scores.get)
    total_intensity = sum(scores.values())

    return {
        'dominant': dominant,
        'scores': dict(scores),
        'intensity': total_intensity
    }


def analyze_chapter_emotion_curve(file_path: str) -> dict:
    """分析单章的情绪曲线"""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'error': f'文件不存在: {file_path}'
        }

    main_content = extract_content_from_chapter(path)
    paragraphs = extract_paragraphs(main_content)

    if len(paragraphs) < 3:
        paragraphs = main_content.split('。')[:10]

    curve = []
    emotion_distribution = defaultdict(int)

    for i, para in enumerate(paragraphs):
        analysis = analyze_paragraph_emotions(para)
        position = '开头' if i < len(paragraphs) * 0.3 else ('结尾' if i > len(paragraphs) * 0.7 else '中段')

        curve.append({
            'position': position,
            'para_index': i,
            'dominant': analysis['dominant'],
            'intensity': analysis['intensity']
        })

        if analysis['dominant'] != 'neutral':
            emotion_distribution[analysis['dominant']] += 1

    opening_emotion = curve[0]['dominant'] if curve else 'neutral'
    ending_emotion = curve[-1]['dominant'] if curve else 'neutral'

    transition = f"{opening_emotion} → {ending_emotion}"

    return {
        'file': str(path),
        'exists': True,
        'paragraph_count': len(paragraphs),
        'curve': curve,
        'emotion_distribution': dict(emotion_distribution),
        'opening_emotion': opening_emotion,
        'ending_emotion': ending_emotion,
        'transition': transition
    }


def detect_emotion_jump(chapter_a: dict, chapter_b: dict) -> dict:
    """检测两章之间的情绪跳跃"""
    if not chapter_a.get('exists') or not chapter_b.get('exists'):
        return {'has_jump': False, 'reason': '章节不存在'}

    end_a = chapter_a['ending_emotion']
    start_b = chapter_b['opening_emotion']

    conflict_pairs = [
        ('喜悦', '悲伤'),
        ('喜悦', '愤怒'),
        ('平静', '紧张'),
        ('平静', '愤怒'),
        ('温暖', '愤怒'),
        ('悲伤', '喜悦'),
    ]

    has_jump = any((end_a == p[0] and start_b == p[1]) for p in conflict_pairs)

    return {
        'has_jump': has_jump,
        'from': end_a,
        'to': start_b,
        'transition': f"{end_a} → {start_b}"
    }


def print_emotion_curve(result: dict):
    """打印情绪曲线分析结果"""
    if not result.get('exists'):
        print(f"\n❌ {result.get('error', '未知错误')}")
        return

    print('\n' + '=' * 60)
    print(f'📊 情绪曲线分析: {Path(result["file"]).name}')
    print('=' * 60)

    print(f'\n📈 段落数量: {result["paragraph_count"]}')
    print(f'\n🎭 情绪分布:')
    for emotion, count in sorted(result['emotion_distribution'].items(), key=lambda x: -x[1]):
        bar = '█' * count
        print(f'   {emotion}: {bar} ({count})')

    print(f'\n🔄 情绪走向: {result["transition"]}')
    print(f'   开头: {result["opening_emotion"]} | 结尾: {result["ending_emotion"]}')

    print('\n📉 段落情绪明细:')
    for item in result['curve'][:8]:
        intensity_indicator = '●' * min(item['intensity'], 5)
        print(f'   [{item["position"]}] {item["dominant"]} {intensity_indicator}')

    if len(result['curve']) > 8:
        print('   ...')


def print_jump_warning(jump: dict):
    """打印情绪跳跃警告"""
    if jump.get('has_jump'):
        print('\n⚠️  情绪跳跃警告:')
        print(f'   检测到情绪突变: {jump["transition"]}')
        print('   建议: 添加过渡段落，使情绪变化更自然')
    else:
        print(f'\n✅ 情绪连贯: {jump["transition"]}')


def analyze_multiple_chapters(directory: str, pattern: str = '*.md') -> list:
    """分析目录下所有章节的情绪曲线"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误: 目录不存在 - {directory}')
        return []

    chapter_files = [path for path in sorted(dir_path.glob(pattern)) if is_chapter_file(path)]
    results = []

    for chapter_file in chapter_files:
        result = analyze_chapter_emotion_curve(str(chapter_file))
        results.append(result)

    return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法:')
        print('  分析单章情绪: python check_emotion_curve.py <章节文件路径>')
        print('  分析所有章节: python check_emotion_curve.py --all <目录路径>')
        return

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误: 使用 --all 时需要指定目录路径')
            return
        directory = sys.argv[2]
        results = analyze_multiple_chapters(directory)

        for result in results:
            print_emotion_curve(result)

        if len(results) >= 2:
            for i in range(len(results) - 1):
                jump = detect_emotion_jump(results[i], results[i + 1])
                print(f'\n--- {Path(results[i]["file"]).name} → {Path(results[i+1]["file"]).name} ---')
                print_jump_warning(jump)
    else:
        file_path = sys.argv[1]
        result = analyze_chapter_emotion_curve(file_path)
        print_emotion_curve(result)


if __name__ == '__main__':
    main()
