#!/usr/bin/env python3
# modules/analyzer.py - 话题分析与生命周期判断 v2
"""
核心分析维度：
1. 话题聚类 - 将相似话题归类
2. 生命周期判断 - 新兴/爆发中/持续发酵/衰减中（基于昨日数据对比）
3. 共鸣度评分 - 热度 × 平台权重 × 跨平台覆盖率
4. 关键词过滤 - 匹配竞品词/行业词/告警词
5. PM选题建议 - 从话题内容提取切入角度
"""
import re, sys, os, json, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# ============================================================
# 平台权重（影响共鸣度评分）
# ============================================================
PLATFORM_WEIGHTS = {
    # 国内
    '知乎': 1.3, '知乎热榜': 1.3,
    '微博': 1.0, '微博热搜': 1.0,
    '抖音': 0.8, '抖音热点': 0.8,
    'B站': 1.1, '小红书': 0.9, '微信': 1.2,
    '36氪': 1.1, '虎嗅': 1.1, '雷锋网': 1.0,
    'IT之家': 0.9, '爱范儿': 1.0, '界面新闻': 1.0,
    '今日热榜': 0.7,
    # 海外
    'YouTube': 1.1,
    'X/Twitter': 0.8, 'Twitter趋势': 0.8,
    'Instagram': 0.7,
    'TechCrunch': 1.2, 'The Verge': 1.1,
    'Wired': 1.1, 'Engadget': 1.0, 'Ars Technica': 1.0,
}


# ============================================================
# 生命周期关键词（辅助判断）
# ============================================================
LIFE_CYCLE_SIGNALS = {
    'emerging': ['刚刚', '突发', '首曝', '曝光', '新出', '上线', '首款', '首发', '首次', '新动态'],
    'peak':     ['爆发', '热搜', '刷屏', '破亿', '爆炸', '沸腾', '霸榜', '引爆'],
    'sustaining': ['持续', '发酵', '争议', '回应', '后续', '深挖', '解读', '分析'],
    'decaying': ['降温', '平息', '已解决', '结局', '收尾', '结案', '落幕', '收官'],
}


# ============================================================
# 行业主题词库（扩展到15个主题）
# ============================================================
THEME_TAGS = {
    'AI/大模型': ['AI', '大模型', 'DeepSeek', 'ChatGPT', 'GPT', 'Claude', 'Kimi', '豆包', '文心', '通义', '人工智能', 'LLM', 'AIGC', 'AGI', 'OpenAI', 'Gemini', 'Copilot', 'Stable Diffusion', 'Midjourney', 'Grok', '豆包', '夸克', '硅基流动', '月之暗面', 'MiniMax', '阶跃星辰', '智谱AI', '百川AI'],
    '科技产品': ['iPhone', '华为', '小米', '苹果', '三星', 'OV', '荣耀', '一加', '真我', '特斯拉', '电动车', '汽车', '新能源', '理想', '蔚来', '小鹏', 'Mate', 'Pura', '骁龙', '天玑', 'A系列', '折叠屏'],
    '航天/军事': ['神舟', '火箭', '航天', '星舰', 'SpaceX', '卫星', '空间站', '飞船', '发射', '榛树', '导弹', '军演', '解放军'],
    '人形机器人': ['人形机器人', '机器人', '具身智能', '机械臂', '星行侠', '宇树', 'Figure', '擎天柱', '智元机器人', '追觅'],
    '互联网/平台': ['字节', '腾讯', '阿里', '百度', '美团', '拼多多', '京东', '抖音', '微信', '小红书', 'B站', '快手', '知乎', '微博', '滴滴', '滴滴出行'],
    '娱乐/综艺': ['歌手', '综艺', '电影', '剧集', '明星', '偶像', '演唱会', '选秀', 'CP', '热搜剧', '短剧', '微短剧', '追剧', '票房', '动漫'],
    '体育': ['足球', '篮球', 'NBA', '世界杯', '亚洲杯', '奥运', '夺冠', '冠军', '泰山', '三镇', '皇马', '巴萨', '马刺', '雷霆', '男足', '亚冠', '中超', 'FIFA', '世预赛'],
    '财经/商业': ['上市', '融资', '收购', '股价', '财报', '裁员', '倒闭', '独角兽', 'IPO', 'VC', '投资', 'A股', '港股', '美股', '纳斯达克', '道琼斯', '半导体', '芯片'],
    '政策/社会': ['政府', '官方', '回应', '调查', '监管', '政策', '规定', '外交部', '商务部', '证监会', '住建部', '教育部', '证监会', '央行', '银保监会'],
    '国际关系': ['访华', '中美', '中欧', '中俄', '制裁', '关税', '贸易战', 'G7', '联合国', '北约', '武契奇', '特朗普', '普京', '泽连斯基'],
    '安全/事故': ['煤矿', '事故', '瓦斯', '爆炸', '暴雨', '洪水', '灾害', '伤亡', '失联', '搜救', '火灾', '地震'],
    '食品/健康': ['食品', '健康', '医疗', '医保', '医院', '药品', '疫苗', '病毒', '疫情', '癌症', '中药', '减肥'],
    '汽车出行': ['汽车', '车祸', '续航', '智驾', '辅助驾驶', '自动驾驶', '高速', '出行', '限行', '油价', '充电'],
    '游戏/电竞': ['游戏', '电竞', 'Steam', 'Epic', 'Switch', 'PS5', 'Xbox', '原神', '王者荣耀', '吃鸡', '永劫'],
}


# ============================================================
# PM选题切入角度词库（基于主题提供多个角度）
# ============================================================
TOPIC_ANGLES = {
    'AI/大模型': [
        {'angle': 'AI产品商业化分析', 'take': '不报道功能更新，拆解背后的商业模式、定价策略与用户增长逻辑'},
        {'angle': '大模型技术对比', 'take': '从产品体验角度横向对比，普通人该选哪个'},
        {'angle': 'AI替代性评估', 'take': '哪些职业/产品最容易被大模型颠覆，从用户场景出发分析'},
        {'angle': 'AI投资机会', 'take': '从一级市场投资视角，分析哪些AI公司有护城河'},
    ],
    '科技产品': [
        {'angle': '新品快速体验', 'take': '第一时间上手，从真实用户场景评价，不吹不黑'},
        {'angle': '产品策略分析', 'take': '从产品定位角度看厂商为什么要这么做'},
        {'angle': '值不值买', 'take': '从产品经理视角评估性价比和目标用户群'},
    ],
    '航天/军事': [
        {'angle': '航天科普知识向', 'take': '用普通人听得懂的语言解释技术亮点，适合知识型内容'},
        {'angle': '航天商业化视角', 'take': 'SpaceX模式对中国航天商业化的启发'},
        {'angle': '情感向传播', 'take': '发射窗口期情感最强，适合情感向+知识向双线内容'},
    ],
    '人形机器人': [
        {'angle': '技术落地评估', 'take': '从产品化视角分析哪些场景真的能用，离量产有多远'},
        {'angle': '具身智能投资逻辑', 'take': '从投资视角分析人形机器人赛道的机会与坑'},
    ],
    '娱乐/综艺': [
        {'angle': 'IP联动热度', 'take': '游戏+二次元联动有天然社群，可做垂类内容'},
        {'angle': '内容营销拆解', 'take': '从产品运营角度拆解：为什么这个内容能出圈'},
        {'angle': '粉丝经济分析', 'take': '从产品视角分析粉丝社群运营逻辑'},
    ],
    '财经/商业': [
        {'angle': '财报解读', 'take': '不堆数字，拆解业务本质：一个公司到底靠什么赚钱'},
        {'angle': '行业趋势分析', 'take': '从产品/用户视角看行业格局变化'},
        {'angle': '投资逻辑', 'take': '什么公司有护城河，什么公司在讲故事'},
    ],
    '政策/社会': [
        {'angle': '政策解读', 'take': '不炒情绪，从从业者视角做合规分析'},
        {'angle': '影响评估', 'take': '这个政策对普通用户有什么影响，举例说明'},
    ],
    '国际关系': [
        {'angle': '地缘政治影响', 'take': '从出海/供应链视角分析对中国科技公司的影响'},
        {'angle': '外交逻辑拆解', 'take': '为什么要访问，为什么选这个时机，有哪些交易'},
    ],
    '安全/事故': [
        {'angle': '安全机制反思', 'take': '从安全生产管理视角分析：问题出在哪，如何避免'},
        {'angle': '应急响应评估', 'take': '从危机公关和产品应急视角评估各方处理质量'},
    ],
    '体育': [
        {'angle': '体育内容蹭流量', 'take': '体育话题在微博/抖音流量大，适合蹭热点'},
    ],
    '互联网/平台': [
        {'angle': '平台战略分析', 'take': '从产品战略角度拆解：平台最近的动作意味着什么'},
        {'angle': '竞争格局对比', 'take': '同类产品横向对比，用户体验差异在哪'},
    ],
}


def extract_keywords(title):
    """从标题中提取关键词"""
    try:
        import jieba
        words = jieba.cut(title)
        return [w for w in words if len(w) >= 2]
    except ImportError:
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', title)
        return list(dict.fromkeys(words))


def detect_theme(title):
    """检测话题所属主题"""
    title_lower = title.lower()
    best_tag, best_count = '其他', 0
    for tag, keywords in THEME_TAGS.items():
        count = sum(1 for kw in keywords if kw.lower() in title_lower)
        if count > best_count:
            best_tag, best_count = tag, count
    return best_tag


def _load_history():
    """加载昨日数据，用于趋势对比"""
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    hist_path = os.path.join(DATA_DIR, f'{yesterday}.json')
    if os.path.exists(hist_path):
        try:
            data = json.load(open(hist_path, encoding='utf-8'))
            hist = {}
            for platform, items in data.get('raw', {}).items():
                for item in items:
                    item['platform'] = platform
                    hist[item['title']] = item
            return hist
        except Exception:
            pass
    return {}


def _parse_hot(v):
    """将热度值转为整数，兼容字符串格式如'599 万热度'"""
    try:
        if isinstance(v, (int, float)):
            return int(v)
        if isinstance(v, str):
            v = re.sub(r'[^\d.]', '', v)
            return int(float(v)) if v else 0
        return 0
    except (ValueError, TypeError):
        return 0


def detect_lifecycle(item, all_items, history):
    """
    判断话题生命周期阶段（v2: 基于趋势对比）
    """
    title = item.get('title', '')
    platform = item.get('platform', '')
    hot = _parse_hot(item.get('hot', 0))

    # 1. 跨平台覆盖率
    same_title_all = [i for i in all_items if i.get('title') == title]
    platform_count = len({i.get('platform') for i in same_title_all})

    # 2. 趋势判断：对比昨日
    hist_item = history.get(title)
    if hist_item:
        hist_hot = _parse_hot(hist_item.get('hot', 0))
        hot_change = (hot - hist_hot) / max(hist_hot, 1)
    else:
        hot_change = None  # 昨日无记录

    # 3. 关键词信号
    signals = {stage: 0 for stage in LIFE_CYCLE_SIGNALS}
    for stage, keywords in LIFE_CYCLE_SIGNALS.items():
        for kw in keywords:
            if kw in title:
                signals[stage] += 1

    # 4. 综合判断逻辑（优先级顺序）
    # 爆发中: 三平台共振 OR (有上升趋势 AND 有peak信号)
    if platform_count >= 3:
        return '爆发中'
    if hot_change is not None and hot_change > 0.3 and signals['peak'] >= 1:
        return '爆发中'
    # 持续发酵: 有上升趋势 OR 多平台出现
    if hot_change is not None and hot_change > 0.1:
        return '持续发酵'
    if platform_count >= 2 and signals['sustaining'] >= 1:
        return '持续发酵'
    if platform_count >= 2:
        return '持续发酵'
    # 新兴: 昨日无记录 + 新出关键词
    if hot_change is None and (signals['emerging'] >= 1 or signals['peak'] >= 1):
        return '新兴'
    if hot_change is None and platform_count == 1:
        return '新兴'
    # 衰减中: 有下降趋势
    if hot_change is not None and hot_change < -0.2:
        return '衰减中'
    # 衰减中: 关键词信号
    if signals['decaying'] >= 1:
        return '衰减中'
    # 默认：看覆盖率
    if platform_count <= 1:
        return '衰减中'
    return '持续发酵'


def resonance_score(item, all_items):
    """计算话题共鸣度评分（0-10）"""
    hot = _parse_hot(item.get('hot', 0))
    platform = item.get('platform', '')
    weight = PLATFORM_WEIGHTS.get(platform, 1.0)

    # 跨平台覆盖率
    same_title = [i for i in all_items if i.get('title') == item.get('title')]
    platform_count = len({i.get('platform') for i in same_title})
    # 覆盖率基准：5个平台=满分
    coverage_score = min(1.0, platform_count / 5.0) * 3.0

    # 热度分（不同平台热度值量级不同，分别归一化）
    # 分平台归一化（用对数压缩解决同量级平台内区分度问题）
    import math as _math
    if platform in ('抖音', '抖音热点'):
        hot_score = min(4.5, (_math.log1p(hot) / _math.log1p(15_000_000)) * 4.5)
    elif platform in ('微博', '微博热搜'):
        hot_score = min(4.0, (_math.log1p(hot) / _math.log1p(5_000_000)) * 4.0)
    elif platform in ('知乎', '知乎热榜'):
        hot_score = min(3.5, (_math.log1p(hot) / _math.log1p(5_000_000)) * 3.5)
    else:
        hot_score = min(3.0, (_math.log1p(hot) / _math.log1p(1_000_000)) * 3.0)

    score = hot_score * weight + coverage_score
    return round(min(10.0, score), 1)


def pm_topic_suggestion(item):
    """从PM视角给出选题建议（v2: 基于话题内容提取角度）"""
    title = item.get('title', '')
    lifecycle = item.get('lifecycle', '')
    theme = detect_theme(title)
    hot = _parse_hot(item.get('hot', 0))

    # 从词库获取角度列表
    angles = TOPIC_ANGLES.get(theme, None)
    if angles:
        # 热度高优先选第一个，话题新优先选靠前者
        pick = 0 if hot > 5_000_000 else min(1, len(angles) - 1)
        chosen = angles[pick]
    else:
        # 从标题中提取关键词作为角度
        kws = extract_keywords(title)
        main_kw = kws[0] if kws else '热门话题'
        chosen = {
            'angle': f'{main_kw}话题追踪',
            'take': f'围绕"{main_kw}"拆解：为什么引发关注，背后反映了什么趋势',
            'form': '热点速评 / 深度分析',
        }

    # 组装最终建议
    suggestion = {
        'angle': chosen['angle'],
        'take': chosen['take'],
        'form': chosen.get('form', '根据话题类型选择形式'),
    }

    # 生命周期建议
    if lifecycle == '爆发中':
        suggestion['timing'] = '⏰ 立即行动，流量窗口期已到'
    elif lifecycle == '新兴':
        suggestion['timing'] = '🆕 跟踪关注，判断是否值得跟进'
    elif lifecycle == '持续发酵':
        suggestion['timing'] = '📈 适合做深度内容或系列内容'
    else:
        suggestion['timing'] = '📉 可做盘点总结类内容'

    return suggestion


def _safe_max(items, key='hot'):
    """安全取最大值"""
    valid = [(i, _parse_hot(i.get(key, 0))) for i in items]
    return max(valid, key=lambda x: x[1])[0] if valid else items[0]


def cluster_topics(items):
    """将相似话题聚类"""
    clusters = []
    used = set()

    for item in items:
        title = item.get('title', '')
        if title in used:
            continue

        keywords = set(extract_keywords(title))
        group = [item]
        group_platforms = {item.get('platform')}

        for other in items:
            if other.get('title') in used or other.get('title') == title:
                continue
            other_kws = set(extract_keywords(other.get('title', '')))
            overlap = keywords & other_kws
            # 重叠>=1个关键词 且 重叠率>30%
            if len(overlap) >= 1 and len(overlap) / max(len(keywords), 1) > 0.3:
                group.append(other)
                group_platforms.add(other.get('platform'))
                used.add(other.get('title'))

        used.add(title)
        clusters.append({
            'primary': title,
            'items': group,
            'platforms': list(group_platforms),
            'platform_count': len(group_platforms),
            'total_hot': sum(_parse_hot(i.get('hot', 0)) for i in group),
            'theme': detect_theme(title),
        })

    return sorted(clusters, key=lambda c: c['total_hot'], reverse=True)


def filter_by_keywords(all_items, keywords):
    """按关键词过滤"""
    result = {}
    for platform, items in all_items.items():
        matched = [item for item in items if any(kw in item.get('title', '') for kw in keywords)]
        if matched:
            result[platform] = matched
    return result


def _load_keywords():
    """加载关键词配置"""
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'keywords.json')
    if os.path.exists(cfg_path):
        return json.load(open(cfg_path, encoding='utf-8'))
    return {}


def filter_by_blacklist(all_items, blacklist):
    """按黑名单过滤"""
    if not blacklist:
        return all_items
    filtered = []
    removed = 0
    for item in all_items:
        title = item.get('title', '')
        excerpt = item.get('excerpt', '')
        if any(kw in title or kw in excerpt for kw in blacklist):
            removed += 1
            continue
        filtered.append(item)
    if removed > 0:
        print(f'  🚫 黑名单过滤掉 {removed} 条')
    return filtered


def analyze(raw):
    """完整分析流程 v2"""
    # 加载历史数据（昨日）
    history = _load_history()
    if history:
        print(f'  📊 已加载昨日数据 {len(history)} 条用于趋势对比')
    else:
        print('  ⚠️ 未找到昨日数据，生命周期判断精度下降')

    all_items = []
    for platform, items in raw.items():
        for item in items:
            item['platform'] = platform
            all_items.append(item)

    # 黑名单过滤
    cfg = _load_keywords()
    blacklist = cfg.get('blacklist', [])
    all_items = filter_by_blacklist(all_items, blacklist)

    # 话题聚类
    clusters = cluster_topics(all_items)

    # 每个话题评分
    scored = []
    for cluster in clusters:
        top_item = _safe_max(cluster['items'], 'hot')
        lifecycle = detect_lifecycle(top_item, all_items, history)
        resonance = resonance_score(top_item, all_items)
        top_item['lifecycle'] = lifecycle
        top_item['resonance'] = resonance
        top_item['theme'] = cluster['theme']
        top_item['platform_count'] = cluster['platform_count']
        scored.append(top_item)

    # 按共鸣度排序
    scored.sort(key=lambda x: x.get('resonance', 0), reverse=True)

    # 平台统计
    stats = {}
    for platform, items in raw.items():
        themes = {}
        for item in items:
            t = detect_theme(item.get('title', ''))
            themes[t] = themes.get(t, 0) + 1
        stats[platform] = {
            'count': len(items),
            'themes': themes,
            'top': _safe_max(items, 'hot').get('title', '') if items else '',
        }

    # 主题统计
    theme_summary = {}
    for item in all_items:
        t = item.get('theme', '其他')
        theme_summary[t] = theme_summary.get(t, 0) + 1

    top_theme = max(theme_summary, key=theme_summary.get) if theme_summary else '其他'

    return {
        'clusters': clusters,
        'scored': scored[:20],
        'stats': stats,
        'summary': {
            'total': len(all_items),
            'platform_count': len(raw),
            'top_theme': top_theme,
            'history_loaded': bool(history),
        }
    }


if __name__ == '__main__':
    import json
    test = {
        '知乎': [{'title': 'DeepSeek大模型新版本发布', 'hot': 5000, 'platform': '知乎'}],
        '微博': [{'title': 'DeepSeek深夜重磅更新', 'hot': 2000000, 'platform': '微博'}],
    }
    r = analyze(test)
    print(json.dumps(r, ensure_ascii=False, indent=2))
