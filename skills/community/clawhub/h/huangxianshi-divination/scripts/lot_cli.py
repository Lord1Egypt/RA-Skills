#!/usr/bin/env python3
import argparse
import json
import os
import random
import sys
import time

# 签数据已内置在同目录的 signs_data.py 中
import sys
sys.path.insert(0, os.path.dirname(__file__))
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LAST_DRAW_PATH = os.path.join(DATA_DIR, 'last_draw.json')

# 导入内置签数据
try:
    from signs_data import SIGNS
except ImportError:
    # 兼容旧版本：从JSON读取
    CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'signs_cache.json')
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        SIGNS = json.load(f).get('signs', [])

ASPECT_MAP = {
    '流年': 'yearly', '全年': 'yearly', 'yearly': 'yearly',
    '事业': 'career', '工作': 'career', 'career': 'career',
    '财运': 'wealth', '财富': 'wealth', 'wealth': 'wealth',
    '自身': 'self', '自己': 'self', 'self': 'self',
    '家庭': 'family', '家宅': 'family', 'family': 'family',
    '姻缘': 'relationship', '感情': 'relationship', '恋爱': 'relationship', 'relationship': 'relationship',
    '迁居': 'moving', '搬家': 'moving', 'moving': 'moving',
    '名誉': 'reputation', '口碑': 'reputation', 'reputation': 'reputation',
    '健康': 'health', '身体': 'health', 'health': 'health',
    '友情': 'friendship', '朋友': 'friendship', 'friendship': 'friendship',
    '典故': 'story', '看典故': 'story', '故事': 'story', 'story': 'story',
    '全部': 'all', 'all': 'all'
}

ASPECT_CN = {
    'yearly': '流年', 'career': '事业', 'wealth': '财运', 'self': '自身', 'family': '家庭',
    'relationship': '姻缘', 'moving': '迁居', 'reputation': '名誉', 'health': '健康', 'friendship': '友情'
}

DRAW_FRAMES = ['🪄 正在净手焚香……', '🎋 签筒摇动中……', '🧧 灵签已落，请接签。']


def fetch_signs(force=False):
    """从内置数据读取签"""
    return SIGNS


def format_poem(sign):
    # poem 现在直接是字符串
    poem = sign.get('poem', '')
    if isinstance(poem, dict):
        lines = [poem.get('first', ''), poem.get('second', ''), poem.get('third', ''), poem.get('fourth', '')]
        lines = [x.strip() for x in lines if str(x).strip()]
        return '\n'.join(lines) if lines else ''
    return str(poem) if poem else ''


def save_last_draw(sign):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LAST_DRAW_PATH, 'w', encoding='utf-8') as f:
        json.dump({'no': sign.get('number'), 'ts': time.time()}, f, ensure_ascii=False)


def load_last_draw_no():
    if not os.path.exists(LAST_DRAW_PATH):
        return None
    try:
        with open(LAST_DRAW_PATH, 'r', encoding='utf-8') as f:
            return int(json.load(f).get('no'))
    except Exception:
        return None


def find_sign_by_no(signs, no):
    return next((x for x in signs if int(x.get('number', -1)) == int(no)), None)


def render_draw_card(sign):
    story = sign.get('story', '') or '（暂无典故）'
    return (
        '━━━━━━━━━━\n'
        '🎴 黄仙师灵签\n'
        f'⚖️ 吉凶：{sign.get("grade", "")}\n'
        f'🔢 签号：{sign.get("no", "")}\n'
        f'🏷️ 签题：{sign.get("title", "")}\n'
        '📝 签诗：\n'
        f'{format_poem(sign)}\n\n'
        f'📚 典故：\n{story}\n'
        '━━━━━━━━━━\n'
        '可继续：解签 / 解事业 / 解财运 / 解姻缘 / 解健康 / 解流年 / 全部解签\n'
        '（可说：再求一签）'
    )


def render_explain_card(sign, aspect, content, all_mode=False):
    head = (
        '━━━━━━━━━━\n'
        '🧾 解签结果\n'
        f'🔢 签号：{sign.get("no")}\n'
        f'🏷️ 签题：{sign.get("title", "")}\n'
        f'⚖️ 吉凶：{sign.get("grade", "")}\n'
    )
    if all_mode:
        story = sign.get('story', '')
        lines = [head, '📚 全部解签：']
        if story:
            lines.append(f'\n【典故】\n{story}')
        lines.append('\n━━━━━━━━━━')
        return '\n'.join(lines)
    return head + f'🧭 方向：{ASPECT_CN.get(aspect, aspect)}\n\n{content}\n━━━━━━━━━━'


def cmd_draw(args):
    signs = fetch_signs(force=args.refresh)
    sign = random.SystemRandom().choice(signs)
    save_last_draw(sign)

    if args.animation_only:
        for f in DRAW_FRAMES:
            print(f)
        return

    if args.format == 'card':
        if args.animate:
            for f in DRAW_FRAMES:
                print(f)
                time.sleep(0.25)
        print(render_draw_card(sign))
        return

    print(json.dumps({'no': sign.get('number'), 'title': sign.get('title'), 'grade': sign.get('grade'), 'poem': format_poem(sign)}, ensure_ascii=False, indent=2))


def cmd_draw_ritual(args):
    signs = fetch_signs(force=args.refresh)
    sign = random.SystemRandom().choice(signs)
    save_last_draw(sign)
    for f in DRAW_FRAMES:
        print(f)
        time.sleep(args.delay)
    print(render_draw_card(sign))


def cmd_explain(args):
    signs = fetch_signs(force=args.refresh)
    no = args.no if args.no is not None else load_last_draw_no()
    if no is None:
        print(json.dumps({'error': '还没有上一签，请先抽签。'}, ensure_ascii=False))
        sys.exit(1)

    sign = find_sign_by_no(signs, no)
    if not sign:
        print(json.dumps({'error': f'签号不存在: {no}'}, ensure_ascii=False))
        sys.exit(1)

    aspect = ASPECT_MAP.get(args.aspect, args.aspect)
    inter = sign.get('interpretations') or {}

    if aspect == 'all':
        if args.format == 'card':
            print(render_explain_card(sign, aspect, '', all_mode=True))
        else:
            print(json.dumps({'no': sign.get('number'), 'title': sign.get('title'), 'grade': sign.get('grade'), 'poem': format_poem(sign), 'story': (sign.get('explanation') or {}).get('story', ''), 'interpretations': inter}, ensure_ascii=False, indent=2))
        return

    if aspect == 'story':
        story = (sign.get('explanation') or {}).get('story', '')
        if args.format == 'card':
            print('━━━━━━━━━━\n📚 典故详解\n' + f'🔢 签号：{sign.get("number")}\n🏷️ 签题：{sign.get("title", "")}\n⚖️ 吉凶：{sign.get("grade", "")}\n\n' + (story or '（暂无典故）') + '\n━━━━━━━━━━')
        else:
            print(json.dumps({'no': sign.get('number'), 'title': sign.get('title'), 'grade': sign.get('grade'), 'story': story}, ensure_ascii=False, indent=2))
        return

    if aspect not in inter:
        print(json.dumps({'error': f'不支持的解签方向: {args.aspect}'}, ensure_ascii=False))
        sys.exit(1)

    if args.format == 'card':
        print(render_explain_card(sign, aspect, inter.get(aspect, ''), all_mode=False))
    else:
        print(json.dumps({'no': sign.get('number'), 'title': sign.get('title'), 'grade': sign.get('grade'), 'aspect': aspect, 'aspect_cn': ASPECT_CN.get(aspect, aspect), 'content': inter.get(aspect, '')}, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description='黄仙师灵签抽签与解签')
    sp = p.add_subparsers(dest='cmd', required=True)

    p_draw = sp.add_parser('draw', help='随机抽签')
    p_draw.add_argument('--refresh', action='store_true')
    p_draw.add_argument('--format', choices=['json', 'card'], default='json')
    p_draw.add_argument('--animate', action='store_true')
    p_draw.add_argument('--animation-only', action='store_true')
    p_draw.set_defaults(func=cmd_draw)

    p_rit = sp.add_parser('draw-ritual', help='三段仪式动画 + 结果卡（单次输出）')
    p_rit.add_argument('--refresh', action='store_true')
    p_rit.add_argument('--delay', type=float, default=0.18)
    p_rit.set_defaults(func=cmd_draw_ritual)

    p_ex = sp.add_parser('explain', help='按签号解签')
    p_ex.add_argument('--no', type=int, required=False)
    p_ex.add_argument('--aspect', default='all')
    p_ex.add_argument('--refresh', action='store_true')
    p_ex.add_argument('--format', choices=['json', 'card'], default='json')
    p_ex.set_defaults(func=cmd_explain)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
