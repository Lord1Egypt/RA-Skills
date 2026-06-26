#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爽点/毒点分析工具
检测章节中的爽点模式和毒点模式，评估读者的"爽感"体验
"""

import re
import sys
from pathlib import Path

try:
    from chapter_text import extract_content_from_chapter, is_chapter_file
except ModuleNotFoundError:
    from scripts.chapter_text import extract_content_from_chapter, is_chapter_file

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


THRILL_PATTERNS = {
    '打脸反转': {
        'keywords': [
            '没想到', '竟然是', '居然是', '竟是', '打死也想不到', '不敢相信',
            '瞬间傻眼', '面色大变', '瞳孔收缩', '难以置信', '这不可能',
            '怎么可能', '原来是你', '身份暴露', '真相揭开', '反转'
        ],
        'weight': 3,
        'description': '主角或反派被打脸、身份暴露、真相揭开',
        'scope': 'full'
    },
    '越级战斗': {
        'keywords': [
            '越级', '跨境界', '以弱胜强', '逆袭', '反杀',
            '秒杀', '碾压', '完虐', '吊打', '不堪一击',
            '越阶', '跨境', '弱者', '蝼蚁', '不自量力'
        ],
        'weight': 3,
        'description': '主角跨越等级/境界战胜强敌',
        'scope': 'full'
    },
    '宝物获得': {
        'keywords': [
            '获得', '得到', '收获', '意外获得', '偶然得到',
            '传承', '法宝', '神器', '灵宝', '仙草', '灵丹',
            '功法', '秘籍', '传承', '血脉', '天赋'
        ],
        'weight': 2,
        'description': '主角获得珍稀宝物、功法、传承',
        'scope': 'full'
    },
    '境界突破': {
        'keywords': [
            '突破', '进阶', '晋升', '升级', '突破瓶颈',
            '筑基', '金丹', '元婴', '化神', '渡劫',
            '境界提升', '实力大增', '修为暴涨', '顿悟'
        ],
        'weight': 3,
        'description': '主角修为/实力突破',
        'scope': 'full'
    },
    '英雄救美': {
        'keywords': [
            '英雄救美', '英雄', '救人', '拯救', '保护',
            '危机', '危险', '刺杀', '偷袭', '围攻',
            '轻薄', '侮辱', '欺凌', '仗势欺人'
        ],
        'weight': 2,
        'description': '主角拯救他人于危难',
        'scope': 'full'
    },
    '身份揭露': {
        'keywords': [
            '身份', '真实身份', '隐藏身份', '暴露', '揭穿',
            '伪装', '面具', '真面目', '王爷', '太子',
            '少主', '长老', '掌门', '背后身份'
        ],
        'weight': 2,
        'description': '隐藏身份被揭露或反转',
        'scope': 'full'
    },
    '复仇成功': {
        'keywords': [
            '复仇', '报复', '血债血偿', '十倍奉还', '新仇旧恨',
            '灭族', '灭门', '杀害', '仇恨', '不共戴天',
            '报仇', '雪恨', '清偿', '了断'
        ],
        'weight': 3,
        'description': '主角成功报复仇人',
        'scope': 'full'
    },
    '势力打脸': {
        'keywords': [
            '门派', '家族', '势力', '宗门', '长老', '掌门',
            '轻视', '嘲讽', '讥笑', '不屑', '狗眼看人低',
            '有眼不识泰山', '不长眼', '瞎了狗眼'
        ],
        'weight': 2,
        'description': '势力/家族被打脸',
        'scope': 'full'
    },
    '神秘伏笔': {
        'keywords': [
            '神秘', '诡异', '奇怪', '不对劲', '有问题',
            '阴谋', '陷阱', '算计', '背后', '真相',
            '隐藏', '秘密', '不可告人', '惊人'
        ],
        'weight': 1,
        'description': '设置悬念/伏笔',
        'scope': 'full'
    },
    '承诺兑现': {
        'keywords': [
            '承诺', '保证', '誓言', '一定会', '必然',
            '一定会', '说到做到', '言出必行', '实现'
        ],
        'weight': 2,
        'description': '之前的承诺/伏笔被兑现',
        'scope': 'full'
    }
}


POISON_PATTERNS = {
    'AI常用词': {
        'keywords': [
            '众所周知', '不言而喻', '须弥芥子', '璀璨', '瑰丽',
            '绚烂', '夺目', '耀眼', '绝美', '俊美无俦',
            '令人窒息', '无法言喻', '言语无法形容'
        ],
        'weight': 2,
        'description': 'AI常用的华丽但空洞的词汇',
        'scope': 'full'
    },
    '高风险感官套语': {
        'keywords': [
            '血腥味', '铁锈味', '金属的甜腥味',
            '周遭的空气仿佛凝固了', '令人疯狂的窒息感', '呼吸如破风箱'
        ],
        'weight': 2,
        'description': '高频 AI 感官套语，若反复出现建议改写为更具体的场面',
        'scope': 'full'
    },
    '高风险微表情套语': {
        'keywords': [
            '瞳孔骤缩', '倒吸一口凉气', '嘴角勾起了一抹弧度',
            '修长的手指', '深邃的眼眸', '眉头微蹙',
            '呢喃', '叹息声空气中回荡'
        ],
        'weight': 2,
        'description': '常见 AI 微表情或人物描写套语，重复时容易失真',
        'scope': 'full'
    },
    '高风险抽象形容': {
        'keywords': [
            '宛如实质的杀气', '恐怖如斯', '不可名状'
        ],
        'weight': 2,
        'description': '抽象压迫形容过重，容易替代具体场面',
        'scope': 'full'
    },
    '感悟式结尾': {
        'keywords': [
            '他明白了', '她明白了', '他懂了', '她懂了',
            '他意识到', '她意识到', '他终于明白', '她终于懂得',
            '此刻他才明白', '此刻她才明白'
        ],
        'weight': 3,
        'description': '直接陈述主角顿悟',
        'scope': 'ending'
    },
    '感叹式结尾': {
        'keywords': [
            '真是太', '多么', '竟然如此',
            '令人', '实在', '简直'
        ],
        'weight': 2,
        'description': '使用感叹句直接表达情绪',
        'scope': 'ending'
    },
    '上帝视角': {
        'keywords': [
            '所有人没想到', '全书', '所有人都在',
            '所有人都是', '众人', '所有人'
        ],
        'weight': 3,
        'description': '使用上帝视角叙述',
        'scope': 'full'
    },
    '套路堆砌': {
        'keywords': [
            '莫欺少年穷', '三十年河东', '废物利用',
            '退婚', '悔婚', '天材地宝', '应有尽有'
        ],
        'weight': 1,
        'description': '使用网文老套路',
        'scope': 'full'
    },
    '抽象心理': {
        'keywords': [
            '他感到很', '她感到很', '他觉得', '她觉得',
            '他感到', '她感到', '内心充满'
        ],
        'weight': 2,
        'description': '使用抽象的心理描述而非具体动作',
        'scope': 'full'
    },
    '过度解释': {
        'keywords': [
            '这是因为', '原因在于',
            '也就是说', '换言之', '换句话说',
            '归根结底', '说到底', '总而言之'
        ],
        'weight': 1,
        'description': '过度解释角色行为动机',
        'scope': 'full'
    },
    '无意义修饰': {
        'keywords': [
            '美丽的', '英俊的', '可爱的', '迷人的',
            '绚丽的', '灿烂的', '辉煌的', '宏伟的'
        ],
        'weight': 1,
        'description': '无意义的属性修饰词',
        'scope': 'full'
    }
}


def get_scope_text(text: str, scope: str) -> str:
    if not text:
        return text
    if scope == 'ending':
        start = int(len(text) * 0.8)
        return text[start:]
    if scope == 'opening':
        end = max(1, int(len(text) * 0.2))
        return text[:end]
    return text


def count_occurrences(text: str, keyword: str) -> int:
    return text.count(keyword)


def detect_patterns(text: str, pattern_dict: dict) -> list:
    """检测文本中匹配的模式"""
    matches = []

    for pattern_name, pattern_info in pattern_dict.items():
        scope_text = get_scope_text(text, pattern_info.get('scope', 'full'))
        found_keywords = []
        total_count = 0
        for keyword in pattern_info['keywords']:
            count = count_occurrences(scope_text, keyword)
            if count:
                total_count += count
                found_keywords.append((keyword, count))

        if total_count:
            matches.append({
                'pattern': pattern_name,
                'keywords': [f'{keyword}×{count}' for keyword, count in found_keywords[:5]],
                'count': total_count,
                'weight': pattern_info['weight'],
                'description': pattern_info['description'],
                'scope': pattern_info.get('scope', 'full'),
            })

    return matches


def analyze_thrills_and_poisons(file_path: str) -> dict:
    """分析章节中的爽点和毒点"""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'error': f'文件不存在: {file_path}'
        }

    content = extract_content_from_chapter(path)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))

    thrill_matches = detect_patterns(content, THRILL_PATTERNS)
    poison_matches = detect_patterns(content, POISON_PATTERNS)

    thrill_score = sum(m['weight'] * m['count'] for m in thrill_matches)
    poison_score = sum(m['weight'] * m['count'] for m in poison_matches)

    thrill_density = thrill_score / max(chinese_chars / 500, 1)
    poison_density = poison_score / max(chinese_chars / 500, 1)

    if thrill_score >= 10 and thrill_density >= 0.5 and poison_score <= 5:
        overall = 'positive'
    elif poison_score > thrill_score or poison_score > 5:
        overall = 'negative'
    else:
        overall = 'neutral'

    return {
        'file': str(path),
        'exists': True,
        'content_length': len(content),
        'chinese_char_count': chinese_chars,
        'thrills': thrill_matches,
        'poisons': poison_matches,
        'thrill_score': thrill_score,
        'poison_score': poison_score,
        'thrill_density': round(thrill_density, 2),
        'poison_density': round(poison_density, 2),
        'overall': overall
    }


def print_thrill_poison_analysis(result: dict):
    """打印爽点/毒点分析结果"""
    if not result.get('exists'):
        print(f"\n❌ {result.get('error', '未知错误')}")
        return

    print('\n' + '=' * 60)
    print(f'🎯 爽点/毒点分析: {Path(result["file"]).name}')
    print('=' * 60)

    print(f'\n📊 基础数据:')
    print(f'   内容长度: {result["content_length"]} 字符')
    print(f'   中文字数: {result["chinese_char_count"]}')

    print(f'\n🔥 爽点得分: {result["thrill_score"]} (密度: {result["thrill_density"]})')
    if result['thrills']:
        print(f'   发现 {len(result["thrills"])} 种爽点模式:')
        for item in sorted(result['thrills'], key=lambda x: -x['weight'] * x['count'])[:5]:
            print(f'   • {item["pattern"]}: {item["count"]}次 - {item["description"]}')
            print(f'     关键词: {", ".join(item["keywords"][:3])}')
    else:
        print('   ⚠️ 未检测到明显爽点')

    print(f'\n💀 毒点得分: {result["poison_score"]} (密度: {result["poison_density"]})')
    if result['poisons']:
        print(f'   发现 {len(result["poisons"])} 种毒点模式:')
        for item in sorted(result['poisons'], key=lambda x: -x['weight'] * x['count'])[:5]:
            scope_label = '（结尾段）' if item.get('scope') == 'ending' else ''
            print(f'   • {item["pattern"]}{scope_label}: {item["count"]}次 - {item["description"]}')
            print(f'     关键词: {", ".join(item["keywords"][:3])}')
    else:
        print('   ✅ 未检测到明显毒点')

    print(f'\n📈 综合评估: ', end='')
    if result['overall'] == 'positive':
        print('✅ 爽感充足')
    elif result['overall'] == 'negative':
        print('⚠️ 毒点较多，建议修改')
    else:
        print('➖ 需要结合正文人工判断')

    print('\n💡 优化建议:')
    if result['thrill_score'] < 10:
        print('   • 建议增加爽点：打脸反转、境界突破、宝物获得')
    if result['poison_score'] > 5:
        print('   • 建议减少毒点：避免AI常用词、感悟式结尾和过度解释')
    poison_names = {item['pattern'] for item in result['poisons']}
    if poison_names & {'高风险感官套语', '高风险微表情套语', '高风险抽象形容'}:
        print('   • 高风险套语偏多时，不要只删词，优先改写成具体动作、环境、物件或后果')
    if result['thrill_density'] < 0.5:
        print('   • 爽点密度偏低，每500字应有1个以上爽点')


def analyze_multiple_chapters(directory: str, pattern: str = '*.md') -> list:
    """分析目录下所有章节的爽点/毒点"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误: 目录不存在 - {directory}')
        return []

    chapter_files = [path for path in sorted(dir_path.glob(pattern)) if is_chapter_file(path)]
    results = []

    for chapter_file in chapter_files:
        result = analyze_thrills_and_poisons(str(chapter_file))
        results.append(result)

    return results


def print_summary(results: list):
    """打印汇总报告"""
    if not results:
        return

    print('\n' + '=' * 60)
    print('📋 多章汇总报告')
    print('=' * 60)

    total_thrill = sum(r['thrill_score'] for r in results if r.get('exists'))
    total_poison = sum(r['poison_score'] for r in results if r.get('exists'))
    avg_thrill = total_thrill / len(results)
    avg_poison = total_poison / len(results)

    print(f'\n📊 总体数据:')
    print(f'   章节数: {len(results)}')
    print(f'   平均爽点得分: {avg_thrill:.1f}')
    print(f'   平均毒点得分: {avg_poison:.1f}')

    print(f'\n🔥 爽点排行榜:')
    sorted_thrills = sorted(results, key=lambda x: x.get('thrill_score', 0), reverse=True)[:5]
    for i, r in enumerate(sorted_thrills, 1):
        if r.get('exists'):
            print(f'   {i}. {Path(r["file"]).name}: {r["thrill_score"]}分')

    print(f'\n💀 毒点排行榜:')
    sorted_poisons = sorted(results, key=lambda x: x.get('poison_score', 0), reverse=True)[:5]
    for i, r in enumerate(sorted_poisons, 1):
        if r.get('exists') and r['poison_score'] > 0:
            print(f'   {i}. {Path(r["file"]).name}: {r["poison_score"]}分')


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法:')
        print('  分析单章: python extract_thrills.py <章节文件路径>')
        print('  分析所有章节: python extract_thrills.py --all <目录路径>')
        return

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误: 使用 --all 时需要指定目录路径')
            return
        directory = sys.argv[2]
        results = analyze_multiple_chapters(directory)

        for result in results:
            print_thrill_poison_analysis(result)

        print_summary(results)
    else:
        file_path = sys.argv[1]
        result = analyze_thrills_and_poisons(file_path)
        print_thrill_poison_analysis(result)


if __name__ == '__main__':
    main()
