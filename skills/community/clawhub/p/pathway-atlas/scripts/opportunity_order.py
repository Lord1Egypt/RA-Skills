"""Product reference hierarchy, adapted from the owner's Hubei opportunity chart.

Numbers are ordinal groups, never scores, admission cutoffs or eligibility.
Equal-group schools are peers; tuple order is display order, not a quality score.
"""

from statistics import median_high


ORDINARY_GROUPS = (
    ('北京大学', '清华大学'),
    ('上海交通大学', '复旦大学', '浙江大学', '中国科学技术大学', '南京大学'),
    ('中国科学院大学', '中国人民大学', '哈尔滨工业大学', '北京航空航天大学', '同济大学'),
    ('华中科技大学', '武汉大学', '北京理工大学', '西安交通大学', '东南大学'),
    ('南开大学', '中山大学', '西北工业大学', '北京师范大学', '华南理工大学', '大连理工大学', '北京邮电大学', '天津大学', '厦门大学', '四川大学', '华东师范大学', '中南大学', '重庆大学', '山东大学'),
    ('湖南大学', '哈尔滨工业大学（威海）', '山东大学（威海）', '东北大学', '中国农业大学', '北京交通大学', '南京航空航天大学', '中央财经大学', '上海财经大学', '中国政法大学', '吉林大学', '中国海洋大学', '兰州大学', '对外经济贸易大学', '上海大学', '北京科技大学'),
    ('华北电力大学（北京）', '深圳大学', '哈尔滨工程大学', '武汉理工大学', '华东理工大学', '苏州大学', '北京化工大学', '暨南大学', '厦门大学马来西亚分校', '合肥工业大学', '江南大学', '东华大学', '华北电力大学（保定）', '安徽大学', '西南交通大学', '华中师范大学', '中南财经政法大学', '杭州电子科技大学', '北京外国语大学', '中国地质大学（武汉）', '西北农林科技大学', '河海大学', '西南财经大学', '西南大学', '长安大学', '河北工业大学', '太原理工大学', '郑州大学', '华中农业大学'),
    ('云南大学', '贵州大学', '山西大学', '天津工业大学', '湘潭大学', '广西大学', '海南大学', '北京信息科技大学', '浙江工业大学', '广东工业大学', '江苏大学', '南京工业大学', '武汉科技大学', '成都理工大学', '桂林电子科技大学', '北方工业大学', '华南农业大学', '浙江工商大学', '西安理工大学'),
    ('长沙理工大学', '汕头大学', '浙江理工大学', '东北电力大学', '重庆交通大学', '湖北大学', '上海应用技术大学', '青岛大学', '西安科技大学', '中国民航大学', '湖北工业大学', '中南民族大学', '武汉工程大学', '三峡大学', '江汉大学', '长江大学', '武汉纺织大学', '西交利物浦大学', '宁波诺丁汉大学', '北京师范大学-香港浸会大学联合国际学院', '广东以色列理工学院', '深圳北理莫斯科大学', '温州肯恩大学'),
    ('上海电机学院', '天津师范大学', '华北水利水电大学', '安徽理工大学', '北京印刷学院', '湖南第一师范学院', '中华女子学院'),
    ('武汉轻工大学', '湖北经济学院', '湖北中医药大学', '湖北师范大学', '湖北第二师范学院', '武汉商学院', '武汉体育学院', '湖北理工学院', '黄冈师范学院', '湖北科技学院', '湖北文理学院', '湖北工程学院', '湖北民族大学', '湖北汽车工业学院', '荆楚理工学院', '汉江师范学院'),
    ('武汉东湖学院', '武昌首义学院', '文华学院', '湖北大学知行学院', '武汉学院', '武昌理工学院', '武汉工商学院', '武汉生物工程学院', '武汉华夏理工学院', '武昌工学院'),
    ('武汉职业技术学院', '襄阳职业技术学院', '武汉船舶职业技术学院', '黄冈职业技术学院', '湖北交通职业技术学院', '武汉铁路职业技术学院', '武汉软件工程职业学院', '鄂州职业大学'),
    ('湖北工程职业学院', '武汉民政职业学院', '荆门职业学院', '武汉工程职业技术学院', '武汉纺织大学外经贸学院', '武汉光谷职业学院', '湖北开放职业学院', '湖北健康职业学院'),
)

COMPREHENSIVE_GROUPS = (
    ('南方科技大学', '上海科技大学'),
    ('上海纽约大学',),
    ('北京外国语大学', '昆山杜克大学'),
    ('深圳北理莫斯科大学',),
)

HK_MACAO_GROUPS = (
    ('香港大学',),
    ('香港科技大学',),
    ('香港中文大学',),
    ('香港理工大学',),
    ('香港城市大学', '香港浸会大学', '澳门大学'),
    ('香港岭南大学', '香港教育大学'),
    ('澳门科技大学', '澳门理工大学'),
    ('香港都会大学', '香港恒生大学', '香港树仁大学', '澳门城市大学'),
)

ALIASES = {
    '哈工大': '哈尔滨工业大学', '哈工大威海': '哈尔滨工业大学（威海）',
    '哈尔滨工业大学(威海)': '哈尔滨工业大学（威海）',
    '山东大学威海': '山东大学（威海）', '山东大学(威海)': '山东大学（威海）',
    '厦门大学马来分校': '厦门大学马来西亚分校',
    '上纽': '上海纽约大学', '昆杜': '昆山杜克大学', '北外': '北京外国语大学',
    '南科大': '南方科技大学', '上科大': '上海科技大学',
    '深北莫': '深圳北理莫斯科大学', '岭大': '香港岭南大学',
    '岭南大学': '香港岭南大学', 'Lingnan University': '香港岭南大学',
    'Hong Kong Metropolitan University': '香港都会大学',
}


def reference_position(kind, school, major=''):
    """Return (group, display order), or None; unlisted never means ineligible."""
    school = ALIASES.get(school, school)
    if school in {'哈尔滨工业大学', '山东大学'} and '威海' in major:
        school += '（威海）'
    elif school == '哈尔滨工业大学' and '深圳' in major:
        return None
    elif school == '山东大学' and '青岛' in major:
        return None
    elif school == '厦门大学' and ('马来西亚' in major or '马来分校' in major):
        school = '厦门大学马来西亚分校'
    if kind == 'hong_kong_macao' and school == '香港大学' and '北京大学' in major and '双学位' in major:
        return (0, 0)
    groups = (COMPREHENSIVE_GROUPS if kind == 'comprehensive_evaluation' else
              HK_MACAO_GROUPS if kind == 'hong_kong_macao' else ORDINARY_GROUPS)
    for group, names in enumerate(groups, 1):
        if school in names:
            return (group, names.index(school))
    return None


def sort_reference(kind, items, center):
    """Order catalogued peers; retain unlisted schools' slots and numeric fit."""
    def fallback(item):
        return (0 if kind != 'hong_kong_macao' or item['location_province'] in {'香港', '香港特别行政区'} else 1,
                abs((item['threshold_rank'] or 0) - (center or 0)))
    items.sort(key=fallback)
    slots = [i for i, item in enumerate(items) if reference_position(kind, item['school'], item['major']) is not None]
    known = [items[i] for i in slots]
    known.sort(key=lambda item: (reference_position(kind, item['school'], item['major'])[0],
                                 fallback(item)[0],
                                 fallback(item)[1],
                                 not bool(item.get('matches_preferences'))))
    for slot, item in zip(slots, known):
        items[slot] = item


def align_qualitative_pathways(kind, tiers):
    """Align source-backed qualitative targets, keeping actual personal tiers.

    Peers share a comparison tier; one actual project threshold cannot disable
    alignment of the remaining qualitative candidates. Three or more groups
    give upper/middle/lower comparisons. With fewer groups retain the median
    requested preparation level per group, reordered monotonically; missing
    tiers stay missing instead of inventing distinctions between peers.
    """
    names = ('冲', '稳', '保')
    entries = [(tier, item) for tier in names for item in tiers[tier]]
    known = [(tier, item, reference_position(kind, item['school'], item['major']))
             for tier, item in entries if not item['personal_tier']
             and reference_position(kind, item['school'], item['major']) is not None]
    if not known:
        return
    groups = sorted({position[0] for _, _, position in known})
    if len(groups) >= 3:
        mapping = {group: names[min(i, 2)] for i, group in enumerate(groups)}
    else:
        requested = sorted(median_high(sorted(names.index(tier) for tier, _, position in known
                                              if position[0] == group)) for group in groups)
        mapping = {group: names[index] for group, index in zip(groups, requested)}
    assignments = {id(item): mapping[position[0]] for _, item, position in known}
    for tier in names:
        tiers[tier] = [item for old, item in entries if assignments.get(id(item), old) == tier]
        for item in tiers[tier]:
            if id(item) in assignments:
                item['reference_comparison'] = True
                item['host_tier_reason'] = item.get('tier_reason')
                item['tier_reason'] = f'按全国院校层次在本轮已读候选中列为{tier}档比较目标；同层学校保留为备选，个人录取把握仍需本省项目门槛和校测表现判断'
