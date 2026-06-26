#!/usr/bin/env python3
"""
小饭卡 - 口味画像管理
用法:
  python3 profile.py add "鲤承" --tags "中餐,精致小馆" --feeling "喜欢" --price 200
  python3 profile.py remove "鲤承"
  python3 profile.py list
  python3 profile.py analyze
  python3 profile.py tags
  python3 profile.py export
  python3 profile.py reset
"""

import sys
import json
import argparse
import os
from datetime import datetime
from pathlib import Path

# 数据目录：skill自身的data目录
DATA_DIR = Path(__file__).parent.parent / 'data'
PROFILE_PATH = DATA_DIR / 'taste-profile.json'


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_profile() -> dict:
    ensure_data_dir()
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'user': {},
        'restaurants': [],
        'preferences': {},
        'updated_at': None,
    }


def save_profile(profile: dict):
    ensure_data_dir()
    profile['updated_at'] = datetime.now().isoformat()
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def cmd_check():
    """检查口味画像是否存在，输出 JSON"""
    profile = load_profile()
    has_profile = bool(profile.get('preferences') and profile['preferences'].get('liked_tags'))
    has_restaurants = len(profile.get('restaurants', [])) > 0
    print(json.dumps({
        'has_profile': has_profile,
        'has_restaurants': has_restaurants,
        'restaurant_count': len(profile.get('restaurants', [])),
        'onboarded': profile.get('user', {}).get('onboarded', False),
    }, ensure_ascii=False))


def cmd_count():
    """返回记录的餐厅总数"""
    profile = load_profile()
    total = len(profile.get('restaurants', []))
    liked = sum(1 for r in profile.get('restaurants', []) if r.get('feeling') in ('喜欢', '常去'))
    # 检查是否刚好达到解锁里程碑
    unlock_milestone = total >= 20 and not profile.get('user', {}).get('hidden_menu_unlocked', False)
    print(json.dumps({
        'total': total,
        'liked': liked,
        'unlock_milestone': unlock_milestone,
    }, ensure_ascii=False))


def cmd_show():
    """显示口味画像摘要"""
    profile = load_profile()
    prefs = profile.get('preferences', {})
    user = profile.get('user', {})
    print(json.dumps({
        'city': user.get('city', ''),
        'areas': user.get('areas', []),
        'liked_tags': prefs.get('liked_tags', []),
        'disliked_tags': prefs.get('disliked_tags', []),
        'avg_price': prefs.get('avg_price'),
        'price_range': prefs.get('price_range'),
        'total_restaurants': len(profile.get('restaurants', [])),
    }, ensure_ascii=False))


def _auto_analyze(profile: dict):
    """内部：每次记录后自动更新口味画像偏好摘要"""
    restaurants = profile.get('restaurants', [])
    if len(restaurants) < 3:
        return
    liked_tags, disliked_tags, price_points, area_counts = {}, {}, [], {}
    dislike_reasons = {}
    for r in restaurants:
        feeling = r.get('feeling', '')
        is_pos = feeling in ('喜欢', '常去', '感兴趣', '想去')
        is_neg = feeling in ('不喜欢', '一般', '踩雷')
        for tag in r.get('tags', []):
            if is_pos:
                liked_tags[tag] = liked_tags.get(tag, 0) + 1
            elif is_neg:
                disliked_tags[tag] = disliked_tags.get(tag, 0) + 1
        if r.get('avg_price') and is_pos:
            price_points.append(r['avg_price'])
        if r.get('area') and is_pos:
            area_counts[r['area']] = area_counts.get(r['area'], 0) + 1
        # 统计踩雷原因
        if is_neg:
            for reason in r.get('dislike_reasons', []):
                dislike_reasons[reason] = dislike_reasons.get(reason, 0) + 1
    top_liked = sorted(liked_tags, key=liked_tags.get, reverse=True)[:8]
    top_disliked = sorted(disliked_tags, key=disliked_tags.get, reverse=True)[:3]
    top_areas = sorted(area_counts, key=area_counts.get, reverse=True)[:3]
    top_dislike_reasons = sorted(dislike_reasons, key=dislike_reasons.get, reverse=True)[:5]
    avg = round(sum(price_points) / len(price_points)) if price_points else None
    profile['preferences'] = {
        'liked_tags': top_liked,
        'disliked_tags': top_disliked,
        'avg_price': avg,
        'price_range': [min(price_points), max(price_points)] if price_points else None,
        'top_areas': top_areas,
        'dislike_reasons': top_dislike_reasons,
        'total_restaurants': len(restaurants),
        'analyzed_at': datetime.now().isoformat(),
    }
    save_profile(profile)


def cmd_record(name: str, feeling: str, note: str = '', reasons: list = None):
    """记录一次用餐体验，更新画像，自动重新分析偏好"""
    profile = load_profile()
    existing = next((r for r in profile.get('restaurants', []) if r['name'] == name), None)
    if existing:
        existing['feeling'] = feeling
        existing['visits'] = existing.get('visits', 0) + 1
        if note:
            existing['notes'] = note
        if reasons:
            existing['dislike_reasons'] = reasons
        existing['updated_at'] = datetime.now().isoformat()
    else:
        profile.setdefault('restaurants', []).append({
            'name': name,
            'feeling': feeling,
            'notes': note,
            'dislike_reasons': reasons or [],
            'tags': [],
            'visits': 1,
            'source': 'user_feedback',
            'added_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        })
    save_profile(profile)

    # 自动重新分析口味画像，保持画像始终最新
    _auto_analyze(profile)

    # 自动发布到 Moltbook（仅"喜欢"/"常去"，用户同意后，静默执行）
    if feeling in ('喜欢', '常去') and profile.get('user', {}).get('moltbook_sharing', False):
        try:
            import subprocess
            r = next((x for x in profile.get('restaurants', []) if x['name'] == name), {})
            tags = ','.join(r.get('tags', []))
            area = r.get('area', '')
            price = r.get('avg_price', '')
            cmd = ['python3', str(Path(__file__).parent / 'moltbook.py'), 'post', name,
                   '--feeling', feeling, '--area', area]
            if price:
                cmd += ['--price', str(price)]
            if tags:
                cmd += ['--tags', tags]
            subprocess.Popen(cmd, cwd=str(Path(__file__).parent.parent),
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    total = len(profile['restaurants'])
    print(json.dumps({
        'status': 'ok',
        'name': name,
        'feeling': feeling,
        'total': total,
        'unlock_milestone': total >= 20 and not profile.get('user', {}).get('hidden_menu_unlocked', False),
    }, ensure_ascii=False))


def add_restaurant(name, tags, feeling, price=None,
                   area=None, city=None,
                   notes=None, source=None):
    """添加或更新一家餐厅"""
    profile = load_profile()

    existing = next((r for r in profile['restaurants'] if r['name'] == name), None)
    if existing:
        existing['tags'] = list(set(existing.get('tags', []) + tags))
        if feeling:
            existing['feeling'] = feeling
        if price:
            existing['avg_price'] = price
        if area:
            existing['area'] = area
        if city:
            existing['city'] = city
        if notes:
            existing['notes'] = notes
        if source:
            existing['source'] = source
        existing['updated_at'] = datetime.now().isoformat()
        existing['visits'] = existing.get('visits', 0) + 1
        print(f"✏️  已更新: {name}")
    else:
        entry = {
            'name': name,
            'tags': tags,
            'feeling': feeling,
            'avg_price': price,
            'area': area,
            'city': city,
            'notes': notes,
            'source': source,
            'visits': 1,
            'added_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }
        profile['restaurants'].append(entry)
        print(f"✅ 已添加: {name}")

    save_profile(profile)


def remove_restaurant(name: str):
    """删除一家餐厅"""
    profile = load_profile()
    before = len(profile['restaurants'])
    profile['restaurants'] = [r for r in profile['restaurants'] if r['name'] != name]
    after = len(profile['restaurants'])
    if before > after:
        save_profile(profile)
        print(f"🗑️  已删除: {name}")
    else:
        print(f"⚠️  未找到: {name}")


def list_restaurants():
    """列出所有记录的餐厅"""
    profile = load_profile()
    restaurants = profile.get('restaurants', [])

    if not restaurants:
        print("还没有记录任何餐厅，试试 onboard.py 开始吧")
        return

    # 显示用户信息
    user = profile.get('user', {})
    if user:
        city = user.get('city', '')
        areas = ', '.join(user.get('areas', []))
        if city or areas:
            print(f"📍 {city} {areas}\n")

    groups = {}
    for r in restaurants:
        feeling = r.get('feeling', '未分类')
        groups.setdefault(feeling, []).append(r)

    feeling_order = ['喜欢', '常去', '去过', '感兴趣', '想去', '一般', '不喜欢', '未分类']
    feeling_emoji = {
        '喜欢': '❤️', '常去': '🔁', '去过': '✅', '感兴趣': '👀',
        '想去': '📌', '一般': '😐', '不喜欢': '👎', '未分类': '❓'
    }

    for feeling in feeling_order:
        if feeling in groups:
            emoji = feeling_emoji.get(feeling, '•')
            print(f"\n{emoji} {feeling}:")
            for r in groups[feeling]:
                price = f" ¥{r['avg_price']}" if r.get('avg_price') else ''
                area = f" 📍{r['area']}" if r.get('area') else ''
                tags = ' '.join(f'#{t}' for t in r.get('tags', []))
                visits = f" ({r['visits']}次)" if r.get('visits', 0) > 1 else ''
                print(f"  • {r['name']}{price}{area}{visits} {tags}")
                if r.get('notes'):
                    print(f"    💬 {r['notes']}")

    print(f"\n共 {len(restaurants)} 家餐厅")


def analyze():
    """分析口味偏好"""
    profile = load_profile()
    restaurants = profile.get('restaurants', [])

    if len(restaurants) < 3:
        print(f"数据太少（{len(restaurants)}家），至少3家才能分析")
        return

    tag_counts = {}
    liked_tags = {}
    disliked_tags = {}
    price_points = []
    area_counts = {}

    for r in restaurants:
        tags = r.get('tags', [])
        feeling = r.get('feeling', '')
        price = r.get('avg_price')
        area = r.get('area')
        is_positive = feeling in ('喜欢', '常去', '感兴趣', '想去')
        is_negative = feeling in ('不喜欢', '一般')

        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            if is_positive:
                liked_tags[tag] = liked_tags.get(tag, 0) + 1
            elif is_negative:
                disliked_tags[tag] = disliked_tags.get(tag, 0) + 1

        if price and is_positive:
            price_points.append(price)

        if area and is_positive:
            area_counts[area] = area_counts.get(area, 0) + 1

    # 输出
    print("🧠 口味画像分析\n")

    total = len(restaurants)
    liked = sum(1 for r in restaurants if r.get('feeling') in ('喜欢', '常去'))
    disliked = sum(1 for r in restaurants if r.get('feeling') == '不喜欢')
    print(f"📊 共 {total} 家：{liked} 家喜欢，{disliked} 家不喜欢\n")

    if liked_tags:
        sorted_tags = sorted(liked_tags.items(), key=lambda x: x[1], reverse=True)
        print("✅ 喜欢的标签:")
        for tag, count in sorted_tags[:10]:
            bar = '█' * count
            print(f"  #{tag}: {bar} ({count})")
        print()

    if disliked_tags:
        sorted_tags = sorted(disliked_tags.items(), key=lambda x: x[1], reverse=True)
        print("❌ 不喜欢的标签:")
        for tag, count in sorted_tags[:5]:
            print(f"  #{tag} ({count})")
        print()

    if price_points:
        avg = sum(price_points) / len(price_points)
        low = min(price_points)
        high = max(price_points)
        print(f"💰 偏好价位: ¥{low}-¥{high}，平均 ¥{avg:.0f}\n")

    if area_counts:
        sorted_areas = sorted(area_counts.items(), key=lambda x: x[1], reverse=True)
        print("📍 常去区域:")
        for area, count in sorted_areas[:5]:
            print(f"  {area}: {count}家")
        print()

    # 生成画像摘要
    top_liked = [t for t, _ in sorted(liked_tags.items(), key=lambda x: x[1], reverse=True)[:8]]
    top_disliked = [t for t, _ in sorted(disliked_tags.items(), key=lambda x: x[1], reverse=True)[:3]]
    top_areas = [a for a, _ in sorted(area_counts.items(), key=lambda x: x[1], reverse=True)[:3]]

    print("📝 画像摘要:")
    if top_liked:
        print(f"  喜欢: {', '.join(top_liked)}")
    if top_disliked:
        print(f"  不喜欢: {', '.join(top_disliked)}")
    if price_points:
        print(f"  价位: 人均¥{avg:.0f}左右 (¥{low}-¥{high})")
    if top_areas:
        print(f"  常去: {', '.join(top_areas)}")

    # 保存分析结果
    profile['preferences'] = {
        'liked_tags': top_liked,
        'disliked_tags': top_disliked,
        'avg_price': round(avg) if price_points else None,
        'price_range': [low, high] if price_points else None,
        'top_areas': top_areas,
        'total_restaurants': total,
        'analyzed_at': datetime.now().isoformat(),
    }
    save_profile(profile)
    print("\n✅ 画像已更新")


def show_tags():
    """显示所有标签"""
    profile = load_profile()
    tag_counts = {}
    for r in profile.get('restaurants', []):
        for tag in r.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if not tag_counts:
        print("还没有标签")
        return

    print("🏷️  所有标签:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  #{tag} ({count})")


def export_json():
    """导出完整画像数据"""
    profile = load_profile()
    print(json.dumps(profile, ensure_ascii=False, indent=2))


def reset_profile():
    """重置画像"""
    if PROFILE_PATH.exists():
        PROFILE_PATH.unlink()
        print("🔄 画像已重置")
    else:
        print("画像本来就是空的")


def set_user(city: str = None, areas: list = None, dislikes: list = None):
    """设置用户基本信息"""
    profile = load_profile()
    user = profile.get('user', {})
    if city:
        user['city'] = city
    if areas:
        user['areas'] = areas
    if dislikes:
        user['dislikes'] = dislikes
    user['updated_at'] = datetime.now().isoformat()
    profile['user'] = user
    save_profile(profile)
    print(f"✅ 用户信息已更新")


def cmd_moltbook_opt(enabled: bool):
    """设置 Moltbook 匿名分享偏好（onboarding 完成后问一次）"""
    profile = load_profile()
    profile.setdefault('user', {})['moltbook_sharing'] = enabled
    save_profile(profile)
    if enabled:
        print(json.dumps({'status': 'ok', 'moltbook_sharing': True,
                          'message': '已开启。你喜欢的馆子会匿名分享到 Moltbook，每天最多 2 家。'}, ensure_ascii=False))
    else:
        print(json.dumps({'status': 'ok', 'moltbook_sharing': False,
                          'message': '已关闭。随时可以重新开启。'}, ensure_ascii=False))


def cmd_pending_add(name: str):
    """推荐后记录待反馈"""
    profile = load_profile()
    pending = profile.setdefault('pending_feedback', [])
    if not any(p['name'] == name for p in pending):
        pending.append({'name': name, 'recommended_at': datetime.now().isoformat()})
        save_profile(profile)
    print(json.dumps({'status': 'ok', 'name': name}, ensure_ascii=False))


def cmd_pending_list():
    """列出超过2天未反馈的推荐"""
    profile = load_profile()
    pending = profile.get('pending_feedback', [])
    now = datetime.now()
    overdue = []
    for p in pending:
        try:
            rec = datetime.fromisoformat(p['recommended_at'])
            days = (now - rec).days
            if days >= 2:
                overdue.append({**p, 'days_ago': days})
        except Exception:
            pass
    print(json.dumps(overdue, ensure_ascii=False))


def cmd_pending_clear(name: str):
    """清除待反馈记录"""
    profile = load_profile()
    profile['pending_feedback'] = [
        p for p in profile.get('pending_feedback', []) if p['name'] != name
    ]
    save_profile(profile)
    print(json.dumps({'status': 'ok'}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='小饭卡 - 口味画像管理')
    sub = parser.add_subparsers(dest='command')

    # add
    add_p = sub.add_parser('add', help='添加餐厅')
    add_p.add_argument('name', help='餐厅名')
    add_p.add_argument('--tags', default='', help='标签，逗号分隔')
    add_p.add_argument('--feeling', default='喜欢',
                       choices=['喜欢', '常去', '去过', '感兴趣', '想去', '一般', '不喜欢'],
                       help='感受')
    add_p.add_argument('--price', type=int, help='人均价格')
    add_p.add_argument('--area', help='区域')
    add_p.add_argument('--city', help='城市')
    add_p.add_argument('--notes', help='备注')
    add_p.add_argument('--source', help='信息来源(dianping/xiaohongshu/user)')

    # remove
    rm_p = sub.add_parser('remove', help='删除餐厅')
    rm_p.add_argument('name', help='餐厅名')

    # user
    user_p = sub.add_parser('user', help='设置用户信息')
    user_p.add_argument('--city', help='城市')
    user_p.add_argument('--areas', help='常去区域，逗号分隔')
    user_p.add_argument('--dislikes', help='不喜欢的，逗号分隔')

    sub.add_parser('list', help='列出所有餐厅')
    sub.add_parser('analyze', help='分析口味偏好')
    sub.add_parser('tags', help='显示所有标签')
    sub.add_parser('export', help='导出JSON')
    sub.add_parser('reset', help='重置画像')
    sub.add_parser('check', help='检查口味画像是否存在')
    sub.add_parser('count', help='返回记录的餐厅总数')
    sub.add_parser('show', help='显示口味画像摘要')
    rec_p = sub.add_parser('record', help='记录一次用餐体验')
    rec_p.add_argument('name', help='餐厅名')
    rec_p.add_argument('--feeling', choices=['喜欢', '一般', '踩雷'], default='喜欢')
    rec_p.add_argument('--note', default='', help='备注')
    rec_p.add_argument('--reasons', default='', help='踩雷原因，逗号分隔（太贵/难吃/服务差/太吵/太远/太油/太辣/太淡/环境差/排队太长）')
    opt_p = sub.add_parser('moltbook-opt', help='设置 Moltbook 匿名分享偏好')
    opt_p.add_argument('--enable', action='store_true', help='开启分享')
    opt_p.add_argument('--disable', action='store_true', help='关闭分享')

    pa_p = sub.add_parser('pending-add', help='记录待反馈推荐')
    pa_p.add_argument('name', help='餐厅名')
    sub.add_parser('pending-list', help='列出超过2天未反馈的推荐')
    pc_p = sub.add_parser('pending-clear', help='清除待反馈记录')
    pc_p.add_argument('name', help='餐厅名')

    args = parser.parse_args()

    if args.command == 'check':
        cmd_check()
    elif args.command == 'count':
        cmd_count()
    elif args.command == 'show':
        cmd_show()
    elif args.command == 'moltbook-opt':
        if args.enable:
            cmd_moltbook_opt(True)
        elif args.disable:
            cmd_moltbook_opt(False)
        else:
            print('请指定 --enable 或 --disable')
    elif args.command == 'record':
        reasons = [r.strip() for r in args.reasons.split(',') if r.strip()] if args.reasons else []
        cmd_record(args.name, args.feeling, args.note, reasons)
    elif args.command == 'pending-add':
        cmd_pending_add(args.name)
    elif args.command == 'pending-list':
        cmd_pending_list()
    elif args.command == 'pending-clear':
        cmd_pending_clear(args.name)
    elif args.command == 'add':
        tags = [t.strip() for t in args.tags.split(',') if t.strip()]
        add_restaurant(args.name, tags, args.feeling, args.price, args.area, args.city, args.notes, args.source)
    elif args.command == 'remove':
        remove_restaurant(args.name)
    elif args.command == 'user':
        areas = [a.strip() for a in args.areas.split(',') if a.strip()] if args.areas else None
        dislikes = [d.strip() for d in args.dislikes.split(',') if d.strip()] if args.dislikes else None
        set_user(args.city, areas, dislikes)
    elif args.command == 'list':
        list_restaurants()
    elif args.command == 'analyze':
        analyze()
    elif args.command == 'tags':
        show_tags()
    elif args.command == 'export':
        export_json()
    elif args.command == 'reset':
        reset_profile()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
