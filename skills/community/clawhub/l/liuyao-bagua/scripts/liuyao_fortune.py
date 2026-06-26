#!/usr/bin/env python3
"""
六爻八卦算命脚本
输入: 出生年月日，输出: 四柱八字、五行分析、今年卦象解读
"""

import sys
import json
from datetime import datetime

# 天干
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
# 地支
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# 地支对应生肖
ZODIAC_ANIMALS = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
# 五行
FIVE_ELEMENTS = ['木', '火', '土', '金', '水']
# 天干对应五行 (甲乙木, 丙丁火, 戊己土, 庚辛金, 壬癸水)
STEM_ELEMENTS = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # 0=木, 1=火, 2=土, 3=金, 4=水
# 地支对应五行 (寅卯木, 巳午火, 申酉金, 亥子水, 辰戌丑未土)
BRANCH_ELEMENTS = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]

# 八卦
BAGUA = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']
BAGUA_TRIGRAMS = {
    '乾': (1, 1, 1), '兑': (0, 1, 1), '离': (1, 0, 1), '震': (0, 0, 1),
    '巽': (1, 1, 0), '坎': (0, 1, 0), '艮': (1, 0, 0), '坤': (0, 0, 0)
}
BAGUA_MEANING = {
    '乾': '天，象征权威、创造、刚健',
    '兑': '泽，象征喜悦、交流、口舌',
    '离': '火，象征光明、美丽、依附',
    '震': '雷，象征震动、行动、惊恐',
    '巽': '风，象征进入、谦逊、渗透',
    '坎': '水，象征危险、困难、智慧',
    '艮': '山，象征停止、稳定、客观',
    '坤': '地，象征柔顺、包容、厚重'
}

# 六十四卦表（简化版，键为 (下卦, 上卦)）
HEXAGRAMS = {
    (0, 0): ('乾', '乾为天', '大吉', '卦象纯阳，刚健有力。主事业兴旺、贵人相助、名利双收。但需防过于刚硬而招忌。'),
    (0, 1): ('履', '天泽履', '小吉', '如履薄冰，谨慎行事。虽有风险若能谦卑待人、恪守正道，可获成功。'),
    (0, 2): ('同人', '天火同人', '中吉', '与人和同，人际关系顺畅。利于合作、社交、团队行动。'),
    (0, 3): ('无妄', '天雷无妄', '下吉', '无妄之灾，不可期待意外收获。宜守本分，不可投机。'),
    (0, 4): ('垢', '天风垢', '平', '意外邂逅，有隐藏的机遇或挑战。需要细心把握。'),
    (0, 5): ('讼', '天水讼', '下凶', '争讼是非，防官非口舌。诸事有阻碍，忌冒险。'),
    (0, 6): ('遁', '天山遁', '平', '隐遁退避，宜休息调整。不宜冒进，积蓄力量。'),
    (0, 7): ('否', '天地否', '凶', '闭塞不通，事事不顺。需守静待变。'),
    (1, 0): ('夬', '泽天夬', '小凶', '决断去除，防小人口舌。吉中藏凶，谨慎言行。'),
    (1, 1): ('兑', '兑为泽', '中吉', '喜悦和谐，人际顺遂。利合作、谈判、社交。'),
    (1, 2): ('睽', '火泽睽', '平', '违背乖离，防外人伤害。诸事有违原意。'),
    (1, 3): ('归妹', '雷泽归妹', '下平', '以妹从人，防婚姻感情波动。诸事延迟。'),
    (1, 4): ('中孚', '风泽中孚', '中吉', '诚信之卦，人际信用第一。利考试、合作。'),
    (1, 5): ('节', '水泽节', '小吉', '节制节约，资源有限需谨慎。困难终将化解。'),
    (1, 6): ('损', '山泽损', '平', '有所损失，先损后益。宜低调行事。'),
    (1, 7): ('临', '地泽临', '中吉', '临近指导，有贵人上司赏识。诸事进展顺利。'),
    (2, 0): ('大有', '火天大有', '大吉', '大获所有，事业财运亨通。贵人扶持，名利双收。'),
    (2, 1): ('睽', '火泽睽', '下平', '乖离分散，人际有矛盾。诸事窒碍，耐心化解。'),
    (2, 2): ('离', '离为火', '中吉', '光明照耀，名声地位提升。利文化、艺术、学术。'),
    (2, 3): ('噬嗑', '火雷噬嗑', '中平', '咬合障碍，需努力突破。转运需要时间。'),
    (2, 4): ('鼎', '风火鼎', '中吉', '革故鼎新，改革创新之象。利创业、转型。'),
    (2, 5): ('未济', '火水未济', '下凶', '事未成，物不可成。诸事难成，耐心等待。'),
    (2, 6): ('旅', '火山旅', '下平', '旅途奔波，防失盗口舌。诸事不稳。'),
    (2, 7): ('晋', '地火晋', '中吉', '前进晋升，名声日隆。利考试、晋升、出行。'),
    (3, 0): ('大壮', '雷天大壮', '中吉', '声势壮大，行动有力。忌冲动，守规矩。'),
    (3, 1): ('归妹', '雷泽归妹', '下平', '婚姻延迟，防他人夺爱。诸事有阻碍。'),
    (3, 2): ('噬嗑', '雷火噬嗑', '中平', '障碍咬合，需强力资源突破。'),
    (3, 3): ('震', '震为雷', '中平', '变动震惊，意外扰动。诸事突然，保守为上。'),
    (3, 4): ('恒', '雷风恒', '中吉', '恒久持久，稳定的收获。人际关系稳固。'),
    (3, 5): ('解', '雷水解', '中吉', '解除困难，灾难消散。利于纠纷解决。'),
    (3, 6): ('小过', '雷山小过', '下平', '小有过失，防意外小灾。凡事低调。'),
    (3, 7): ('豫', '雷地豫', '中吉', '喜悦豫乐，人际社交顺利。利合作与出行。'),
    (4, 0): ('小畜', '风天小畜', '下吉', '小有积蓄，进展缓慢。耐心积累。'),
    (4, 1): ('中孚', '风泽中孚', '中吉', '诚信之卦，得人信任。利合作、谈判。'),
    (4, 2): ('鼎', '风火鼎', '中吉', '革故鼎新，转变新象。利改革、创业。'),
    (4, 3): ('恒', '雷风恒', '中吉', '恒心持久，感情事业稳定。'),
    (4, 4): ('巽', '巽为风', '下平', '顺从渗入，宜随风行事。利调整变革。'),
    (4, 5): ('涣', '风水涣', '中平', '涣散分离，人心浮动。防团队散乱。'),
    (4, 6): ('蛊', '山风蛊', '下凶', '腐败迷惑，防桃色陷阱。感情需谨慎。'),
    (4, 7): ('观', '风地观', '中平', '观察等待，有贵人来访。诸事需耐心。'),
    (5, 0): ('需', '水天需', '小吉', '耐心等待，有志者事竟成。财运小有。'),
    (5, 1): ('节', '水泽节', '小吉', '节制节约，财务紧张。诸事保守。'),
    (5, 2): ('既济', '水火既济', '中吉', '事已成，吉祥安稳。财运小进，防人生波折。'),
    (5, 3): ('解', '雷水解', '中吉', '解除困难，轻装上阵。利出行、变动。'),
    (5, 4): ('涣', '风水涣', '中平', '人力分散，防团队分裂。诸事拖延。'),
    (5, 5): ('坎', '坎为水', '下凶', '重重险阻，困难重重。诸事遇压，保守为上。'),
    (5, 6): ('蒙', '山水蒙', '凶', '蒙昧迷惑，防小人作祟。学业受阻。'),
    (5, 7): ('比', '水地比', '中吉', '相亲相比，人际和谐。利结交权贵。'),
    (6, 0): ('大畜', '山天大畜', '中吉', '大量积蓄，贵人相助。利学业、积累。'),
    (6, 1): ('损', '山泽损', '下平', '先损后益，减少欲望。保守积累。'),
    (6, 2): ('旅', '火山旅', '下平', '旅途在外，漂泊不定。诸事延迟。'),
    (6, 3): ('小过', '雷山小过', '下平', '小有过失，防意外。诸事小心。'),
    (6, 4): ('蛊', '山风蛊', '下凶', '蛊惑之象，防桃色是非。感情纠纷。'),
    (6, 5): ('蒙', '山水蒙', '凶', '蒙昧无知，学业受阻。需虚心求教。'),
    (6, 6): ('艮', '艮为山', '平', '停止静止，诸事停顿。静待时机。'),
    (6, 7): ('剥', '山地剥', '凶', '剥削脱落，运势衰落。不宜大动作。'),
    (7, 0): ('泰', '地天泰', '大吉', '天地交泰，万事大吉。人际和合，财运亨通。'),
    (7, 1): ('谦', '地泽谦', '大吉', '谦逊有德，贵人扶持。诸事顺遂。'),
    (7, 2): ('明夷', '地火明夷', '下凶', '光明受伤，防小人暗算。注意口舌是非。'),
    (7, 3): ('复', '地雷复', '中吉', '复归本心，运气回复。财运开始转好。'),
    (7, 4): ('升', '地风升', '中吉', '上升发展，职位晋升。一步一脚印。'),
    (7, 5): ('师', '地水师', '中平', '师众之象，团队力量。利组织行动。'),
    (7, 6): ('谦', '山地谦', '大吉', '谦逊有福，得人和之象。诸事吉利。'),
    (7, 7): ('坤', '坤为地', '中吉', '地势柔顺，包容承载。诸事稳重，财运平稳。'),
}

# 五行颜色
ELEMENT_COLORS = {
    '木': '🌿 青绿',
    '火': '🔥 红',
    '土': '🟤 黄褐',
    '金': '⚪ 白',
    '水': '💧 黑蓝'
}

# 五行相生相克说明
ELEMENT_INTERACTIONS = {
    '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
    '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
    '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
    '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
    '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'},
}


def calc_year_stem_branch(year):
    """计算年柱天干地支"""
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def days_since_2000_01_01(date):
    """计算距离2000年1月1日的天数"""
    ref = datetime(2000, 1, 1)
    return (date - ref).days


def calc_day_stem_branch(date):
    """计算日柱天干地支（基于2000年1月1日=癸亥日）"""
    # 2000年1月1日 = 日柱第9天干(癸) + 第12地支(亥) = index 8, 11
    days = days_since_2000_01_01(date)
    stem_idx = (8 + days) % 10
    branch_idx = (11 + days) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def get_year_zodiac(year):
    """计算生肖"""
    branch_idx = (year - 4) % 12
    return ZODIAC_ANIMALS[branch_idx]


def calc_element_strength(stems_branches):
    """计算五行强度得分"""
    scores = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    for stem, branch in stems_branches:
        scores[FIVE_ELEMENTS[STEM_ELEMENTS[HEAVENLY_STEMS.index(stem)]]] += 1
        scores[FIVE_ELEMENTS[BRANCH_ELEMENTS[EARTHLY_BRANCHES.index(branch)]]] += 1
    return scores


def get_trigram(stem1_idx, stem2_idx):
    """根据两个天干索引计算三爻卦"""
    # 三爻：上爻用 (stem1 + branch) % 8，中爻用 stem2 % 8，下爻用 (stem1 * 2 + stem2) % 8
    a = (stem1_idx * 3 + stem2_idx) % 8
    b = (stem2_idx * 5 + stem1_idx + 3) % 8
    c = (stem1_idx + stem2_idx + 7) % 8
    return (a, b, c)


def trigram_to_bagua(tri):
    """三爻转为对应卦名"""
    for name, pattern in BAGUA_TRIGRAMS.items():
        if pattern == tri:
            return name
    return '乾'


def get_hexagram_data(year_stem, year_branch, month_stem, month_branch, day_stem, day_branch, target_year):
    """计算今年卦象"""
    ys_idx = HEAVENLY_STEMS.index(year_stem)
    ms_idx = HEAVENLY_STEMS.index(month_stem)
    ds_idx = HEAVENLY_STEMS.index(day_stem)
    
    lower_tri = get_trigram(ys_idx, ms_idx)
    upper_tri = get_trigram(ds_idx, ys_idx)
    
    lower_name = trigram_to_bagua(lower_tri)
    upper_name = trigram_to_bagua(upper_tri)
    
    hex_key = (list(BAGUA_TRIGRAMS.keys()).index(lower_name) if lower_name in BAGUA_TRIGRAMS else 0,
               list(BAGUA_TRIGRAMS.keys()).index(upper_name) if upper_name in BAGUA_TRIGRAMS else 0)
    
    if hex_key in HEXAGRAMS:
        bagua_lower = lower_name
        bagua_upper = upper_name
        hex_name = f"{bagua_lower}{bagua_upper}"
        hex_full = HEXAGRAMS[hex_key][1]
        luck = HEXAGRAMS[hex_key][2]
        meaning = HEXAGRAMS[hex_key][3]
    else:
        bagua_lower = lower_name
        bagua_upper = upper_name
        hex_name = f"{bagua_lower}{bagua_upper}"
        hex_full = f"【{hex_name}】"
        luck = '平'
        meaning = '今年运势平稳，无大起大落，宜稳扎稳打。'
    
    return {
        'hex_name': hex_name,
        'hex_full': hex_full,
        'lower': bagua_lower,
        'upper': bagua_upper,
        'lower_meaning': BAGUA_MEANING.get(bagua_lower, ''),
        'upper_meaning': BAGUA_MEANING.get(bagua_upper, ''),
        'luck': luck,
        'meaning': meaning,
        'lower_tri': lower_tri,
        'upper_tri': upper_tri
    }


def generate_fortune_report(birth_year, birth_month, birth_day, target_year=2026):
    """生成完整算命报告"""
    date = datetime(birth_year, birth_month, birth_day)
    
    # 计算四柱
    year_stem, year_branch = calc_year_stem_branch(birth_year)
    day_stem, day_branch = calc_day_stem_branch(date)
    
    # 月柱计算（简化：使用月支地支，再推算月天干）
    month_branch_idx = (birth_month + 2) % 12
    month_branch_name = EARTHLY_BRANCHES[month_branch_idx]
    # 月干口诀：甲己之年丙作首
    year_stem_idx = HEAVENLY_STEMS.index(year_stem)
    month_stem_idx = (year_stem_idx * 2 + birth_month) % 10
    month_stem_name = HEAVENLY_STEMS[month_stem_idx]
    
    # 生肖
    zodiac = get_year_zodiac(birth_year)
    
    # 五行分析
    pillars = [
        (year_stem, year_branch),
        (month_stem_name, month_branch_name),
        (day_stem, day_branch),
    ]
    # 时柱（简化：以日干推算时干，日上起时）
    hour_branch_idx = 0  # 默认子时
    hour_stem_idx = (HEAVENLY_STEMS.index(day_stem) * 2 + hour_branch_idx) % 10
    hour_stem_name = HEAVENLY_STEMS[hour_stem_idx]
    hour_branch_name = EARTHLY_BRANCHES[hour_branch_idx]
    pillars.append((hour_stem_name, hour_branch_name))
    
    element_scores = calc_element_strength(pillars)
    
    # 今年卦象
    hex_data = get_hexagram_data(year_stem, year_branch, month_stem_name, month_branch_name, day_stem, day_branch, target_year)
    
    # 日干性情（简析）
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    day_elem = FIVE_ELEMENTS[STEM_ELEMENTS[day_stem_idx]]
    stem_nature = {
        '甲': '刚毅、有领导力、慷慨', '乙': '温柔、善于变通、包容',
        '丙': '热情、积极、冲动', '丁': '细腻、礼貌、内敛',
        '戊': '稳重、诚实、固执', '己': '细腻、圆滑、务实',
        '庚': '刚强、义气、急躁', '辛': '清高、坚韧、敏感',
        '壬': '聪明、圆通、野心', '癸': '柔和、敏感、幻想'
    }
    day_nature = stem_nature.get(day_stem, '')
    
    # 排盘结果
    report = f"""
╔══════════════════════════════════════╗
║     🧧 六爻八卦 · {target_year}年算命报告     ║
╚══════════════════════════════════════╝

📋 基本信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  出生：{birth_year}年{birth_month}月{birth_day}日
  生肖：{zodiac} 🐉
  日主：{day_stem}{day_branch}（{day_nature}）

🌟 四柱八字
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  年柱：{year_stem}{year_branch}
  月柱：{month_stem_name}{month_branch_name}
  日柱：{day_stem}{day_branch}
  时柱：{hour_stem_name}{hour_branch_name}（起卦参考）

🔮 {target_year}年卦象
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  卦名：{hex_data['hex_name']}卦
  全称：{hex_data['hex_full']}
  运势：{hex_data['luck']}
  
  卦象解释：
  {hex_data['meaning']}
  
  内卦（下卦）：{hex_data['lower']} — {hex_data['lower_meaning']}
  外卦（上卦）：{hex_data['upper']} — {hex_data['upper_meaning']}

⚖️ 五行分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    for elem, score in element_scores.items():
        bar = '█' * score + '░' * (4 - score)
        color = ELEMENT_COLORS.get(elem, '')
        report += f"\n  {elem} {color}：{bar}（{score}分）"
    
    # 找出最旺和最弱
    max_elem = max(element_scores, key=element_scores.get)
    min_elem = min(element_scores, key=element_scores.get)
    dominant = [e for e, s in element_scores.items() if s == element_scores[max_elem]]
    
    report += f"\n\n  ✅ 最旺：{'/'.join(dominant)}（{element_scores[max_elem]}分）"
    report += f"\n  ⚠️ 最弱：{min_elem}（{element_scores[min_elem]}分）"
    
    # 五行养生建议
    report += f"""

🍃 命理建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  你的日主为 {day_stem}（{day_nature}），
  五行最旺为 {''.join(dominant)}，需注意补足 {min_elem}。

  {target_year}年事业：{hex_data['luck']}
  {target_year}年人际：宜低调行事，防小人是非
  {target_year}年财运：稳中求进，忌冒险投机

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  本结果为AI辅助分析，仅供娱乐参考！
  命运掌握在自己手中，努力奋斗才是正道 💪
"""
    return report


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python liuyao_fortune.py <年> <月> <日> [目标年]")
        sys.exit(1)
    
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    target_year = int(sys.argv[4]) if len(sys.argv) > 4 else 2026
    
    report = generate_fortune_report(year, month, day, target_year)
    print(report)
