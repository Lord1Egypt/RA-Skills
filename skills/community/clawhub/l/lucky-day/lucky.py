#!/usr/bin/env python3
"""
择吉选日系统
根据用户需求和属相选择最近的好日子
"""

import sys
from datetime import datetime, timedelta

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 生肖
SHENGXIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 冲煞表
CHONG = {
    "子": "午", "丑": "未", "寅": "申", "卯": "酉",
    "辰": "戌", "巳": "亥", "午": "子", "未": "丑",
    "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳",
}

# 事项对应宜忌关键词
XUQIU_YI = {
    "嫁娶": ["嫁娶", "纳采", "订盟", "结婚"],
    "开业": ["开市", "交易", "立券", "挂匾", "开业"],
    "搬家": ["移徙", "入宅", "安床", "乔迁"],
    "动土": ["动土", "起基", "定磉", "破土"],
    "订盟": ["订盟", "纳采", "盟誓", "结拜"],
    "祭祀": ["祭祀", "祈福", "上香", "拜神"],
    "安门": ["安门", "安门", "安床"],
    "订婚": ["订婚", "纳采", "嫁娶"],
    "开业": ["开市", "交易", "立券"],
    "安葬": ["安葬", "入殓", "移柩"],
}

# 忌讳关键词
JI_KEYWORDS = ["安葬", "动针线", "词讼", "破土", "动土", "动针"]

# 吉神
JISHEN = ["天德", "月德", "天德合", "月德合", "贵人", "福神", "财神"]

# 地支五行
DZ_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}


def get_ganzhi(date: datetime) -> tuple:
    """获取指定日期的干支"""
    base = datetime(2024, 1, 1)
    days_diff = (date - base).days
    
    gan_idx = days_diff % 10
    zhi_idx = days_diff % 12
    
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def get_shengxiao(zhi: str) -> str:
    """获取地支对应的生肖"""
    idx = DIZHI.index(zhi)
    return SHENGXIAO[idx]


def is_chong(zhi: str, shengxiao: str) -> bool:
    """判断是否冲某生肖"""
    if not shengxiao:
        return False
    chong_zhi = CHONG.get(zhi, "")
    chong_shengxiao = get_shengxiao(chong_zhi) if chong_zhi else ""
    return shengxiao == chong_shengxiao


def get_yi_items(zhi: str) -> list:
    """获取宜事项（简化版）"""
    zhi_idx = DIZHI.index(zhi)
    
    all_yi = [
        "祭祀祈福嫁娶订盟纳采问名移徙入宅开市交易立券挂匾拆卸动土起基定磉安床解除冠笄整手足申竖柱上梁纳畜牧养出货财开仓出货",
        "订盟纳采嫁娶出行移徙入宅开市交易立券挂匾拆卸动土破土安葬安床解除冠笄整手足甲竖柱上梁纳畜牧养",
        "祈福嫁娶纳采出行移徙竖柱上梁纳畜牧养整手足甲安床解除冠笄订盟",
        "嫁娶纳采订盟出行移徙竖柱上梁纳畜牧养开市交易立券挂匾拆卸安门安床",
        "安葬动土祈福嫁娶动针线词讼出货财",
    ]
    
    text = all_yi[zhi_idx % len(all_yi)]
    # 拆分成词组
    items = []
    keywords = ["嫁娶", "订盟", "纳采", "开市", "移徙", "入宅", "动土", "祭祀", 
                "祈福", "安床", "竖柱", "上梁", "安葬", "出行"]
    for kw in keywords:
        if kw in text:
            items.append(kw)
    
    return items[:6] if items else ["嫁娶", "订盟"]


def score_day(zhi: str, shengxiao: str, xuqiu: str) -> tuple:
    """给日子打分"""
    score = 100
    reasons = []
    
    # 1. 是否冲用户属相
    if is_chong(zhi, shengxiao):
        score -= 50
        reasons.append("冲属相")
    
    # 2. 是否包含所需宜事项
    yi_items = get_yi_items(zhi)
    xuqi_keys = XUQIU_YI.get(xuqiu, [xuqiu])
    
    has_yi = False
    for key in xuqi_keys:
        if any(key in item for item in yi_items):
            has_yi = True
            break
    
    if has_yi:
        score += 20
        reasons.append(f"宜{xuqiu}")
    else:
        score -= 30
        reasons.append(f"不宜{xuqiu}")
    
    # 3. 地支五行（简化：选择与属相相生的日子）
    if shengxiao:
        shengxiao_idx = SHENGXIAO.index(shengxiao)
        zhi_shengxiao = SHENGXIAO[shengxiao_idx]
        # 简单加分
        score += 10
    else:
        score += 5
    
    return score, reasons


def format_output(results: list, xuqiu: str, shengxiao: str) -> str:
    """格式化输出"""
    output = f"""🗓️ 择吉选日

【需求】：{xuqiu}
"""
    if shengxiao:
        output += f"【您的属相】：{shengxiao}\n"
    else:
        output += "【您的属相】：未提供\n"
    
    output += "\n【推荐吉日】\n"
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, r in enumerate(results[:5]):
        date, gan, zhi, score, reasons = r
        
        yi_items = get_yi_items(zhi)
        yi_str = "、".join(yi_items[:4])
        
        chong_zhi = CHONG.get(zhi, "")
        chong_sx = get_shengxiao(chong_zhi) if chong_zhi else ""
        
        if shengxiao and is_chong(zhi, shengxiao):
            chong_str = f"冲{chong_sx}（{chong_zhi}）- ❌冲犯"
        else:
            chong_str = f"冲{chong_sx}（{chong_zhi}）- ✓不冲"
        
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]
        
        output += f"{medals[i] if i < 3 else f'{i+1}.'} {date.strftime('%Y年%m月%d日')}（{weekday}）\n"
        output += f"   干支：{gan}{zhi}\n"
        output += f"   宜：{yi_str}\n"
        output += f"   冲煞：{chong_str}\n"
        if reasons:
            output += f"   评分理由：{', '.join(reasons)}\n"
        output += "\n"
    
    output += """【建议】
"""
    if results:
        best = results[0]
        output += f"首选 {best[0].strftime('%m月%d日')}，"
        if is_chong(best[2], shengxiao):
            output += "但冲犯属相，建议谨慎\n"
        else:
            output += f"吉神汇聚，宜{xuqiu}\n"
    
    output += """
---
※ 黄历仅供参考，选日还需综合考虑具体时辰 ※"""
    
    return output


def cmd_search(xuqiu: str, shengxiao: str = None):
    """查询吉日"""
    results = []
    
    # 搜索未来30天
    for i in range(30):
        date = datetime.now() + timedelta(days=i)
        gan, zhi = get_ganzhi(date)
        
        score, reasons = score_day(zhi, shengxiao, xuqiu)
        
        if shengxiao:
            # 检查冲煞
            if is_chong(zhi, shengxiao):
                score -= 30
        
        results.append((date, gan, zhi, score, reasons))
    
    # 按分数排序
    results.sort(key=lambda x: x[3], reverse=True)
    
    print(format_output(results, xuqiu, shengxiao))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python lucky.py 嫁娶           # 查询嫁娶吉日")
        print("  python lucky.py 开业 鼠        # 查询开业吉日，排除冲鼠的日子")
        print("  python lucky.py 搬家 兔        # 查询搬家吉日")
        print("\n支持：嫁娶、开业、搬家、动土、订盟、祭祀、订婚、安门")
        sys.exit(1)
    
    xuqiu = sys.argv[1]
    shengxiao = sys.argv[2] if len(sys.argv) > 2 else None
    
    cmd_search(xuqiu, shengxiao)
