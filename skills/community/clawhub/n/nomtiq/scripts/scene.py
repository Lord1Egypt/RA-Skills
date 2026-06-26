#!/usr/bin/env python3
"""
小饭卡 - 场景上下文构建器
职责：把用户画像 + 历史习惯打包成 CoT prompt，供 LLM 做场景理解
不做规则判断，不绑定特定 LLM 或数据源

用法:
  python3 scene.py build "下午和客户吃个饭"
  python3 scene.py record '{"occasion":"商务","area":"三里屯",...}'
  python3 scene.py companion "爸妈" --liked "粤菜,清淡" --disliked "太辣"
  python3 scene.py history
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
PROFILE_PATH = DATA_DIR / 'taste-profile.json'

# 常识提示库 —— 不是规则，是给 LLM 的参考知识
# 只在用户输入包含相关词时注入，避免 prompt 过长
COMMON_SENSE = {
    "辣": "辣味偏好通常对应川菜/湘菜/赣菜，但需结合用户具体辣度偏好（重辣/微辣/有滋味不刺激）",
    "清淡": "清淡偏好通常对应粤菜/江浙菜/云南菜，适合老人或养生场景",
    "商务": "商务场合通常需要：安静环境、包厢或半包厢、有面子、服务好、不太嘈杂",
    "客户": "接待客户通常需要：有档次、服务好、包厢优先、不会让人尴尬",
    "约会": "约会场合通常需要：氛围感、灯光柔和、不太吵、有特色、适合拍照",
    "爸妈": "带父母通常需要：清淡为主、软烂易嚼、不太辣、宽敞、停车方便、不用排队",
    "父母": "带父母通常需要：清淡为主、软烂易嚼、不太辣、宽敞、停车方便、不用排队",
    "朋友": "朋友聚餐通常需要：热闹、可以大声说话、适合分享的菜、不用太正式",
    "宵夜": "宵夜场景通常对应：烧烤/火锅/小龙虾/夜市，营业到深夜",
    "一个人": "独食场景通常需要：快、不尴尬、有一人食选项、不用等位",
}


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_profile(profile: dict):
    profile['updated_at'] = datetime.now().isoformat()
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def extract_habit_patterns(history: list) -> dict:
    """从历史场景中提取用户习惯模式，不做规则判断，只做统计"""
    patterns = {}
    for entry in history[-20:]:
        scene = entry.get('scene', {})
        occasion = scene.get('occasion')
        if not occasion:
            continue
        if occasion not in patterns:
            patterns[occasion] = {'areas': {}, 'cuisines': {}, 'budgets': []}
        area = scene.get('area')
        if area:
            patterns[occasion]['areas'][area] = patterns[occasion]['areas'].get(area, 0) + 1
        for c in scene.get('cuisines', []):
            patterns[occasion]['cuisines'][c] = patterns[occasion]['cuisines'].get(c, 0) + 1
        budget = scene.get('budget')
        if budget:
            patterns[occasion]['budgets'].append(budget)

    summaries = {}
    for occ, data in patterns.items():
        parts = []
        if data['areas']:
            top_area = max(data['areas'], key=data['areas'].get)
            parts.append(f"常去{top_area}")
        if data['cuisines']:
            top = sorted(data['cuisines'], key=data['cuisines'].get, reverse=True)[:2]
            parts.append(f"偏好{'、'.join(top)}")
        if data['budgets']:
            avg = sum(data['budgets']) / len(data['budgets'])
            parts.append(f"人均¥{avg:.0f}左右")
        summaries[occ] = '，'.join(parts)
    return summaries


def build_context(user_input: str) -> str:
    """
    构建 CoT 上下文 prompt
    输出供 LLM 使用的结构化提示，不做任何规则判断
    LLM 拿到这个 prompt 后，结合自身理解输出结构化场景 JSON
    """
    profile = load_profile()
    prefs = profile.get('preferences', {})
    user = profile.get('user', {})
    companions = profile.get('companions', {})
    history = profile.get('scene_history', [])

    lines = []

    # 1. 用户口味画像
    lines.append("## 用户口味画像")
    liked = prefs.get('liked_tags', [])
    disliked = prefs.get('disliked_tags', [])
    price_range = prefs.get('price_range', [])
    top_areas = prefs.get('top_areas', [])
    if liked:
        lines.append(f"- 喜欢：{', '.join(liked)}")
    if disliked:
        lines.append(f"- 不喜欢：{', '.join(disliked)}")
    dislike_reasons = prefs.get('dislike_reasons', [])
    if dislike_reasons:
        lines.append(f"- 踩雷原因（高频）：{', '.join(dislike_reasons)}")
    if price_range and len(price_range) == 2:
        lines.append(f"- 偏好价位：人均¥{price_range[0]}-¥{price_range[1]}")
    if top_areas:
        lines.append(f"- 常去区域：{', '.join(top_areas)}")

    # 2. 同行人画像（如果有）
    if companions:
        lines.append("\n## 同行人偏好")
        for name, data in companions.items():
            parts = []
            if data.get('liked'):
                parts.append(f"喜欢{'、'.join(data['liked'])}")
            if data.get('disliked'):
                parts.append(f"不喜欢{'、'.join(data['disliked'])}")
            if data.get('notes'):
                parts.append(data['notes'])
            lines.append(f"- {name}：{'，'.join(parts) if parts else '暂无记录'}")

    # 3. 历史习惯模式（从行为中学习，不是规则）
    if history:
        patterns = extract_habit_patterns(history)
        if patterns:
            lines.append("\n## 用户历史习惯（从过往推荐中学习）")
            for occ, summary in patterns.items():
                lines.append(f"- {occ}场合：{summary}")

    # 4. 相关常识提示（按需注入，不全量加载）
    relevant_hints = [hint for kw, hint in COMMON_SENSE.items() if kw in user_input]
    if relevant_hints:
        lines.append("\n## 常识参考")
        for hint in relevant_hints:
            lines.append(f"- {hint}")

    # 5. 用户输入
    lines.append(f"\n## 用户输入\n{user_input}")

    # 6. 输出格式（LLM 填写）
    lines.append("""
## 请基于以上上下文输出结构化场景（JSON）
{
  "area": "推荐搜索区域（优先从历史习惯和用户输入推断，无法推断则用常去区域默认值）",
  "occasion": "场合（商务/约会/家庭/朋友/独食，无法判断则 null）",
  "people": "人数（整数，无法判断则 null）",
  "budget": "人均预算（整数，无法判断则 null）",
  "meal_time": "餐次（早餐/午餐/晚餐/宵夜/下午茶，无法判断则 null）",
  "cuisines": ["推断的菜系列表，结合用户画像和同行人偏好"],
  "search_query": "优化后的搜索词，直接用于搜索引擎",
  "reasoning": "一句话说明关键推断逻辑"
}""")

    return '\n'.join(lines)


def record_scene(scene_json: str):
    """记录场景结果，积累用户习惯。推荐完成后调用。"""
    try:
        scene = json.loads(scene_json)
    except json.JSONDecodeError:
        print("⚠️  JSON 格式错误", file=sys.stderr)
        sys.exit(1)

    profile = load_profile()
    if 'scene_history' not in profile:
        profile['scene_history'] = []

    profile['scene_history'].append({
        'input': scene.pop('_input', ''),
        'scene': scene,
        'timestamp': datetime.now().isoformat(),
    })
    # 只保留最近 50 条
    profile['scene_history'] = profile['scene_history'][-50:]
    save_profile(profile)
    print("✅ 场景已记录")


def show_history():
    """查看历史场景模式"""
    profile = load_profile()
    history = profile.get('scene_history', [])
    if not history:
        print("还没有历史记录")
        return

    patterns = extract_habit_patterns(history)
    print(f"📊 场景习惯（基于最近 {min(len(history), 20)} 次）\n")
    if patterns:
        for occ, summary in patterns.items():
            print(f"  {occ}：{summary}")
    else:
        print("  暂无明显规律")

    print(f"\n最近 5 次：")
    for entry in history[-5:]:
        ts = entry.get('timestamp', '')[:10]
        inp = entry.get('input', '')[:30]
        scene = entry.get('scene', {})
        area = scene.get('area', '')
        reasoning = scene.get('reasoning', '')
        print(f"  {ts} | {inp} → {area}  {reasoning}")


def add_companion(name: str, liked: list = None, disliked: list = None, notes: str = None):
    """添加/更新同行人偏好"""
    profile = load_profile()
    if 'companions' not in profile:
        profile['companions'] = {}
    profile['companions'][name] = {
        'liked': liked or [],
        'disliked': disliked or [],
        'notes': notes or '',
        'updated_at': datetime.now().isoformat(),
    }
    save_profile(profile)
    print(f"✅ 已记录同行人：{name}")


def main():
    parser = argparse.ArgumentParser(description='小饭卡 - 场景上下文构建器')
    sub = parser.add_subparsers(dest='command')

    build_p = sub.add_parser('build', help='构建 CoT 上下文 prompt')
    build_p.add_argument('text', help='用户输入')

    rec_p = sub.add_parser('record', help='记录场景结果（推荐后调用）')
    rec_p.add_argument('scene_json', help='场景 JSON 字符串')

    sub.add_parser('history', help='查看历史习惯模式')

    comp_p = sub.add_parser('companion', help='添加同行人偏好')
    comp_p.add_argument('name', help='同行人（如：爸妈、朋友圈、大林）')
    comp_p.add_argument('--liked', default='', help='喜欢，逗号分隔')
    comp_p.add_argument('--disliked', default='', help='不喜欢，逗号分隔')
    comp_p.add_argument('--notes', help='备注')

    args = parser.parse_args()

    if args.command == 'build':
        print(build_context(args.text))
    elif args.command == 'record':
        record_scene(args.scene_json)
    elif args.command == 'history':
        show_history()
    elif args.command == 'companion':
        liked = [x.strip() for x in args.liked.split(',') if x.strip()]
        disliked = [x.strip() for x in args.disliked.split(',') if x.strip()]
        add_companion(args.name, liked, disliked, args.notes)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
