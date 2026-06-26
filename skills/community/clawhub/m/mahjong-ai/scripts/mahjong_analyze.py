#!/usr/bin/env python3
"""
麻将 AI 分析器 v2.0 - 川麻（血战到底）
新增：定缺建议、换三张策略、对手出牌模式推测

用法:
  分析: python3 mahjong_analyze.py --hand "1m,2m,..." --discard "3m,..." --meld "5m,5m,5m,..."
  定缺: python3 mahjong_analyze.py --hand "1m,2m,..." --mode dingque
  换三张: python3 mahjong_analyze.py --hand "1m,2m,..." --mode swap3
  推测: python3 mahjong_analyze.py --discard "1m,2m,..." --mode predict --player "上家"
"""

import sys
import argparse
from collections import Counter
from itertools import combinations

SUITS = {'m': '万', 'p': '筒', 's': '条'}
TILE_NAMES = {}
for sc, sn in SUITS.items():
    for n in range(1, 10):
        TILE_NAMES[f"{n}{sc}"] = f"{n}{sn}"
ALL_TILES = list(TILE_NAMES.keys())
MAX_PER_TILE = 4


def parse_tiles(s):
    if not s or not s.strip(): return []
    tiles = [t.strip() for t in s.split(',') if t.strip()]
    for t in tiles:
        if t not in TILE_NAMES:
            print(f"❌ 无效: {t}"); sys.exit(1)
    return tiles


def get_remaining(hand, discards, melds):
    seen = Counter(hand + discards + melds)
    return {t: MAX_PER_TILE - seen.get(t, 0) for t in ALL_TILES}


def is_complete(c):
    tiles = []
    for t, n in c.items(): tiles.extend([t]*n)
    if len(tiles) != 14: return False
    if is_seven_pairs(c): return True
    for t in set(tiles):
        if c[t] >= 2:
            r = c.copy(); r[t] -= 2
            if r[t] == 0: del r[t]
            if can_form_melds(r): return True
    return False


def is_seven_pairs(c):
    if sum(c.values()) != 14: return False
    return all(v in (2,4) for v in c.values()) and sum(min(v//2,2) for v in c.values()) == 7


def can_form_melds(c):
    if sum(c.values()) == 0: return True
    tiles = sorted(c.keys(), key=lambda t: (t[1], int(t[0])))
    f = tiles[0]
    if c[f] >= 3:
        nc = c.copy(); nc[f] -= 3
        if nc[f] == 0: del nc[f]
        if can_form_melds(nc): return True
    num, suit = int(f[0]), f[1]
    if num <= 7:
        n1, n2 = f"{num+1}{suit}", f"{num+2}{suit}"
        if c.get(n1,0) > 0 and c.get(n2,0) > 0:
            nc = c.copy()
            for t in [f,n1,n2]:
                nc[t] -= 1
                if nc[t] == 0: del nc[t]
            if can_form_melds(nc): return True
    return False


def find_waiting(c, rc):
    waits = []
    for t in ALL_TILES:
        if rc.get(t,0) <= 0: continue
        tc = c.copy(); tc[t] = tc.get(t,0)+1
        if tc[t] <= 4 and is_complete(tc):
            waits.append((t, rc[t]))
    return waits


def calc_shanten(c, rc=None):
    total = sum(c.values())
    if total == 14 and is_complete(c): return -1
    if total == 13:
        _rc = rc or {t:4 for t in ALL_TILES}
        for t in ALL_TILES:
            if _rc.get(t,0) <= 0: continue
            tc = c.copy(); tc[t] = tc.get(t,0)+1
            if tc[t] <= 4 and is_complete(tc): return 0
    best = 8
    for t in set(c.keys()):
        if c[t] >= 2:
            r = c.copy(); r[t] -= 2
            if r[t]==0: del r[t]
            m,ta = count_mt(r)
            best = min(best, 4-m-min(ta,4-m))
    m,ta = count_mt(c.copy())
    best = min(best, 5-m-min(ta,4-m))
    pairs = sum(1 for v in c.values() if v>=2)
    best = min(best, 6-pairs)
    if best == 0 and total == 13:
        _rc = rc or {t:4 for t in ALL_TILES}
        found = any(_rc.get(t,0)>0 and is_complete({**c, t:c.get(t,0)+1}) for t in ALL_TILES)
        if not found: best = 1
    return max(best, -1)


def count_mt(c):
    mentsu, taatsu = 0, 0
    c = c.copy()
    for t in sorted(c.keys(), key=lambda t:(t[1],int(t[0]))):
        while c.get(t,0)>=3: c[t]-=3; mentsu+=1
        if c.get(t,0)==0 and t in c: del c[t]
    for s in 'mps':
        for n in range(1,8):
            t1,t2,t3 = f"{n}{s}",f"{n+1}{s}",f"{n+2}{s}"
            while c.get(t1,0)>0 and c.get(t2,0)>0 and c.get(t3,0)>0:
                for t in [t1,t2,t3]:
                    c[t]-=1
                    if c[t]==0: del c[t]
                mentsu+=1
    for t in sorted(c.keys(), key=lambda t:(t[1],int(t[0]))):
        if c.get(t,0)>=2: c[t]-=2; taatsu+=1
        if c.get(t,0)==0 and t in c: del c[t]
    for s in 'mps':
        for n in range(1,9):
            t1,t2 = f"{n}{s}",f"{n+1}{s}"
            if c.get(t1,0)>0 and c.get(t2,0)>0:
                c[t1]-=1; c[t2]-=1; taatsu+=1
                for t in [t1,t2]:
                    if c.get(t,0)==0 and t in c: del c[t]
        for n in range(1,8):
            t1,t3 = f"{n}{s}",f"{n+2}{s}"
            if c.get(t1,0)>0 and c.get(t3,0)>0:
                c[t1]-=1; c[t3]-=1; taatsu+=1
                for t in [t1,t3]:
                    if c.get(t,0)==0 and t in c: del c[t]
    return mentsu, taatsu


def safety_score(tile, disc_c, rc):
    score = 50
    score += disc_c.get(tile,0) * 15
    if rc[tile] == 0: return 100
    num = int(tile[0])
    if num in (1,9): score += 10
    if 4 <= num <= 6: score -= 10
    return min(100, max(0, score))


def check_specials(c):
    sp = {}
    suits = set(t[1] for t in c.keys())
    sp['清一色'] = len(suits)==1
    sp['接近清一色'] = len(suits)==2 and not sp['清一色']
    sp['七对'] = sum(1 for v in c.values() if v>=2) >= 5
    sp['对对胡'] = sum(1 for v in c.values() if v>=3) >= 3
    sp['龙七对'] = is_seven_pairs(c) and any(v==4 for v in c.values())
    return sp


# ============================================================
# 新功能1: 定缺建议
# ============================================================
def analyze_dingque(hand):
    """分析定缺：选哪门花色最合适"""
    c = Counter(hand)
    suit_info = {}
    
    for s in 'mps':
        tiles_in_suit = [t for t in hand if t[1] == s]
        count = len(tiles_in_suit)
        
        # 计算该花色的"价值"（搭子、对子、刻子越多价值越高）
        value = 0
        sc = Counter(tiles_in_suit)
        
        # 对子/刻子价值
        for t, n in sc.items():
            if n >= 3: value += 6  # 刻子高价值
            elif n >= 2: value += 3  # 对子
        
        # 顺子搭子价值
        for n in range(1, 9):
            t1, t2 = f"{n}{s}", f"{n+1}{s}"
            if sc.get(t1,0) > 0 and sc.get(t2,0) > 0:
                value += 2  # 两面搭子
        for n in range(1, 8):
            t1, t3 = f"{n}{s}", f"{n+2}{s}"
            if sc.get(t1,0) > 0 and sc.get(t3,0) > 0:
                value += 1  # 嵌张搭子
        
        # 清一色潜力
        qingyise_potential = count >= 7
        
        suit_info[s] = {
            'name': SUITS[s],
            'count': count,
            'value': value,
            'tiles': tiles_in_suit,
            'qingyise': qingyise_potential,
        }
    
    # 按价值排序，价值最低的定缺
    ranked = sorted(suit_info.items(), key=lambda x: (x[1]['value'], x[1]['count']))
    
    print("🎯 *定缺建议*")
    print("=" * 50)
    
    for i, (s, info) in enumerate(ranked):
        marker = "⭐ 定缺" if i == 0 else "  保留"
        print(f"{marker} [{info['name']}] {info['count']}张 价值{info['value']}分")
        if info['tiles']:
            print(f"       {' '.join(TILE_NAMES[t] for t in sorted(info['tiles'], key=lambda t:int(t[0])))}")
        if info['qingyise']:
            print(f"       ⚠️ 有清一色潜力，不建议定缺！")
    
    best = ranked[0]
    print(f"\n💡 *建议定缺 [{best[1]['name']}]*")
    reason = []
    if best[1]['count'] <= 2:
        reason.append(f"只有{best[1]['count']}张，最少")
    if best[1]['value'] <= 2:
        reason.append("几乎没有搭子")
    if not reason:
        reason.append(f"价值最低({best[1]['value']}分)")
    print(f"   原因：{'，'.join(reason)}")
    
    # 检查是否有清一色机会
    best_suit = ranked[-1]
    if best_suit[1]['qingyise']:
        print(f"\n🔥 [{best_suit[1]['name']}] 有 {best_suit[1]['count']} 张，可以考虑做清一色！")
    
    return best[0]


# ============================================================
# 新功能2: 换三张策略
# ============================================================
def analyze_swap3(hand, dingque_suit=None):
    """分析换三张：选哪3张换出去"""
    c = Counter(hand)
    
    # 如果没指定定缺，先计算
    if not dingque_suit:
        # 静默计算定缺
        suit_values = {}
        for s in 'mps':
            tiles = [t for t in hand if t[1] == s]
            value = len(tiles)
            sc = Counter(tiles)
            for t, n in sc.items():
                if n >= 3: value += 3
                elif n >= 2: value += 1
            suit_values[s] = value
        dingque_suit = min(suit_values, key=suit_values.get)
    
    dq_tiles = [t for t in hand if t[1] == dingque_suit]
    other_tiles = [t for t in hand if t[1] != dingque_suit]
    
    print(f"🔄 *换三张策略*（定缺：{SUITS[dingque_suit]}）")
    print("=" * 50)
    
    # 必须换同花色的3张
    # 优先换定缺花色的牌
    swap_candidates = []
    
    if len(dq_tiles) >= 3:
        # 定缺花色够3张，全换掉
        # 选价值最低的3张
        sorted_dq = sorted(dq_tiles, key=lambda t: _tile_keep_value(t, c))
        swap = sorted_dq[:3]
        swap_candidates.append(('换定缺牌', swap, '直接清掉定缺花色'))
    
    if len(dq_tiles) < 3:
        print(f"   ⚠️ 定缺[{SUITS[dingque_suit]}]只有{len(dq_tiles)}张，不够3张")
        print(f"   需要从其他花色补{3-len(dq_tiles)}张")
        
        # 从其他花色选最没用的补上
        # 但换三张必须是同花色！
        print(f"   ❗ 注意：换三张必须是同一花色的3张")
        print(f"   如果定缺花色不够3张，只能换另一门花色的3张")
        
        # 找另一门花色中最没用的3张
        for s in 'mps':
            if s == dingque_suit: continue
            s_tiles = [t for t in hand if t[1] == s]
            if len(s_tiles) >= 3:
                sorted_s = sorted(s_tiles, key=lambda t: _tile_keep_value(t, c))
                swap = sorted_s[:3]
                swap_candidates.append((f'换[{SUITS[s]}]', swap, f'{SUITS[s]}中最没用的3张'))
    
    for name, swap, reason in swap_candidates:
        print(f"\n   📤 {name}：{' '.join(TILE_NAMES[t] for t in swap)}")
        print(f"      理由：{reason}")
    
    if swap_candidates:
        best = swap_candidates[0]
        print(f"\n💡 *建议：{best[0]}  →  {' '.join(TILE_NAMES[t] for t in best[1])}*")
    
    # 换回来想要什么
    print(f"\n   📥 希望换回：", end="")
    wanted = []
    for s in 'mps':
        if s == dingque_suit: continue
        s_tiles = [t for t in hand if t[1] == s]
        sc = Counter(s_tiles)
        # 找搭子缺的牌
        for n in range(1, 9):
            t1, t2 = f"{n}{s}", f"{n+1}{s}"
            if sc.get(t1,0) > 0 and sc.get(t2,0) == 0:
                wanted.append(t2)
            if sc.get(t2,0) > 0 and sc.get(t1,0) == 0:
                wanted.append(t1)
        # 找对子缺的
        for t, n in sc.items():
            if n == 1:
                wanted.append(t)  # 凑对
    
    if wanted:
        print(' '.join(TILE_NAMES[t] for t in wanted[:5]))
    else:
        print("任意保留花色的牌")


def _tile_keep_value(tile, counter):
    """计算一张牌的保留价值（越高越不该换掉）"""
    value = 0
    num, suit = int(tile[0]), tile[1]
    
    # 对子/刻子价值
    if counter[tile] >= 3: value += 10
    elif counter[tile] >= 2: value += 5
    
    # 连张价值
    if num > 1 and counter.get(f"{num-1}{suit}", 0) > 0: value += 3
    if num < 9 and counter.get(f"{num+1}{suit}", 0) > 0: value += 3
    if num > 2 and counter.get(f"{num-2}{suit}", 0) > 0: value += 1
    if num < 8 and counter.get(f"{num+2}{suit}", 0) > 0: value += 1
    
    # 边张降低价值
    if num in (1, 9): value -= 1
    
    return value


# ============================================================
# 新功能3: 对手出牌模式推测
# ============================================================
def predict_opponent(discards, player_name="对手"):
    """根据出牌推测对手的策略"""
    if not discards:
        print("⚠️ 没有出牌记录")
        return
    
    c = Counter(discards)
    total = len(discards)
    
    print(f"🔍 *{player_name}出牌分析*（共{total}张）")
    print("=" * 50)
    
    # 统计各花色出牌
    suit_counts = {}
    for s in 'mps':
        st = [t for t in discards if t[1] == s]
        suit_counts[s] = len(st)
    
    print(f"   出牌分布：万{suit_counts['m']}张 / 筒{suit_counts['p']}张 / 条{suit_counts['s']}张")
    
    # 推测定缺
    most_discarded = max(suit_counts, key=suit_counts.get)
    least_discarded = min(suit_counts, key=suit_counts.get)
    
    if suit_counts[most_discarded] >= total * 0.5 and total >= 4:
        print(f"\n   🎯 推测定缺：*[{SUITS[most_discarded]}]*")
        print(f"      理由：{SUITS[most_discarded]}出了{suit_counts[most_discarded]}张（占{suit_counts[most_discarded]*100//total}%），大量清缺门")
    elif total >= 6:
        # 看前3张出的是什么花色
        early = discards[:3]
        early_suits = Counter(t[1] for t in early)
        most_early = max(early_suits, key=early_suits.get)
        if early_suits[most_early] >= 2:
            print(f"\n   🎯 推测定缺：*[{SUITS[most_early]}]*")
            print(f"      理由：前3张就出了{early_suits[most_early]}张{SUITS[most_early]}")
    
    # 推测保留的花色（可能在做什么）
    if suit_counts[least_discarded] == 0 and total >= 5:
        print(f"\n   🔥 *注意*：{player_name}一张{SUITS[least_discarded]}都没出！")
        print(f"      可能在做{SUITS[least_discarded]}的清一色！")
    elif suit_counts[least_discarded] <= 1 and total >= 6:
        print(f"\n   ⚠️ {player_name}很少出{SUITS[least_discarded]}（只出了{suit_counts[least_discarded]}张）")
        print(f"      小心{SUITS[least_discarded]}方向的牌！")
    
    # 分析出牌顺序推测听牌方向
    if total >= 6:
        late = discards[-(total//2):]  # 后半段出的牌
        late_suits = Counter(t[1] for t in late)
        late_nums = [int(t[0]) for t in late]
        
        # 后期出中张 = 可能在做大牌或已经听牌
        mid_count = sum(1 for n in late_nums if 3 <= n <= 7)
        edge_count = sum(1 for n in late_nums if n in (1,2,8,9))
        
        if mid_count > edge_count and total >= 8:
            print(f"\n   🚨 后期出中张偏多 — 可能已听牌或在拆搭子做大牌")
        
        # 推测安全牌
        safe_tiles = []
        for t, cnt in c.items():
            if cnt >= 2:
                safe_tiles.append(t)
        
        if safe_tiles:
            print(f"\n   🟢 相对安全的牌（{player_name}出过2张+）：")
            print(f"      {' '.join(TILE_NAMES[t] for t in safe_tiles)}")
    
    # 推测危险牌
    danger_suits = [s for s in 'mps' if suit_counts[s] <= 1]
    if danger_suits:
        print(f"\n   🔴 危险方向：", end="")
        for s in danger_suits:
            print(f" [{SUITS[s]}]", end="")
        print(f"\n      这些花色的中张（3-7）打出去容易放炮！")


# ============================================================
# 出牌分析（保留原有功能）
# ============================================================
def analyze_discard(hc, rc, dc):
    results = []
    for t in sorted(set(hc.keys()), key=lambda t:(t[1],int(t[0]))):
        tc = hc.copy(); tc[t]-=1
        if tc[t]==0: del tc[t]
        sh = calc_shanten(tc, rc)
        wc, wt = 0, []
        if sh == 0:
            waits = find_waiting(tc, rc)
            wc = sum(w[1] for w in waits); wt = waits
        sf = safety_score(t, dc, rc)
        results.append({'tile':t,'name':TILE_NAMES[t],'shanten':sh,'wait_count':wc,'waits':wt,'safety':sf})
    return results


def main():
    parser = argparse.ArgumentParser(description='川麻AI分析器 v2.0')
    parser.add_argument('--hand', '-H', default='', help='手牌')
    parser.add_argument('--discard', '-d', default='', help='已出的牌')
    parser.add_argument('--meld', '-m', default='', help='碰/杠的牌')
    parser.add_argument('--mode', default='analyze', choices=['analyze','dingque','swap3','predict'],
                        help='模式: analyze=出牌分析, dingque=定缺, swap3=换三张, predict=推测对手')
    parser.add_argument('--player', default='对手', help='对手名称（推测模式用）')
    parser.add_argument('--dingque-suit', '-q', default='', help='已定缺的花色(m/p/s)')
    
    args = parser.parse_args()
    hand = parse_tiles(args.hand)
    discards = parse_tiles(args.discard)
    melds = parse_tiles(args.meld)
    
    # ===== 定缺模式 =====
    if args.mode == 'dingque':
        if not hand:
            print("用法: --hand '1m,2m,...' --mode dingque"); sys.exit(1)
        analyze_dingque(hand)
        return
    
    # ===== 换三张模式 =====
    if args.mode == 'swap3':
        if not hand:
            print("用法: --hand '1m,2m,...' --mode swap3 [--dingque-suit m]"); sys.exit(1)
        dq = args.dingque_suit if args.dingque_suit in 'mps' else None
        analyze_swap3(hand, dq)
        return
    
    # ===== 推测对手模式 =====
    if args.mode == 'predict':
        if not discards:
            print("用法: --discard '1m,2m,...' --mode predict [--player 上家]"); sys.exit(1)
        predict_opponent(discards, args.player)
        return
    
    # ===== 标准分析模式 =====
    if not hand:
        print("用法: python3 mahjong_analyze.py --hand '1m,2m,...' [--discard '...'] [--meld '...']")
        print("模式: --mode analyze|dingque|swap3|predict")
        sys.exit(0)
    
    hc = Counter(hand)
    dc = Counter(discards)
    rc = get_remaining(hand, discards, melds)
    total = len(hand)
    
    # 显示手牌
    sh = sorted(hand, key=lambda t:(t[1],int(t[0])))
    print(f"🀄 手牌（{total}张）：", end="")
    for s in 'mps':
        st = [t for t in sh if t[1]==s]
        if st: print(f" [{SUITS[s]}] {' '.join(TILE_NAMES[t] for t in st)}", end="")
    print()
    
    if discards:
        print(f"🗑️ 场上已出（{len(discards)}张）")
    if melds:
        print(f"🔶 碰/杠（{len(melds)}张）")
    print()
    
    if total == 13:
        shanten = calc_shanten(hc, rc)
        if shanten == 0:
            waits = find_waiting(hc, rc)
            tw = sum(w[1] for w in waits)
            print(f"🎯 *听牌！*")
            for t, r in waits:
                print(f"   听 {TILE_NAMES[t]}（剩{r}张）")
            print(f"   共{len(waits)}种{tw}张")
        else:
            print(f"📊 向听数：{shanten}（距听牌{shanten}步）")
        sp = check_specials(hc)
        active = [n for n,v in sp.items() if v]
        if active: print(f"💡 牌型：{'、'.join(active)}")
    
    elif total == 14:
        if is_complete(hc):
            print("🎉🎉🎉 胡了！")
            sp = check_specials(hc)
            for n,v in sp.items():
                if v: print(f"  🏆 {n}")
        else:
            results = analyze_discard(hc, rc, dc)
            results.sort(key=lambda x:(x['shanten'],-x['wait_count'],-x['safety']))
            best_sh = results[0]['shanten']
            
            print("🎯 出牌建议：")
            print("=" * 55)
            for r in results:
                if r['shanten'] > best_sh + 1: break
                mk = "⭐" if r['shanten']==best_sh else "  "
                si = "🟢" if r['safety']>=70 else "🟡" if r['safety']>=40 else "🔴"
                info = f"{mk} 打 {r['name']:4s} {si}{r['safety']:2d}"
                if r['shanten']==0 and r['wait_count']>0:
                    ws = " ".join(f"{TILE_NAMES[w[0]]}({w[1]})" for w in r['waits'])
                    info += f"  → 听 {ws} ({r['wait_count']}张)"
                elif r['shanten']==0:
                    info += "  → 听牌"
                else:
                    info += f"  → {r['shanten']}向听"
                print(info)
            
            best = [r for r in results if r['shanten']==best_sh][0]
            print(f"\n💡 *建议打 {best['name']}*", end="")
            if best['wait_count']>0: print(f" — 听{best['wait_count']}张")
            elif best['safety']>=70: print(" — 安全")
            else: print()
            
            sp = check_specials(hc)
            active = [n for n,v in sp.items() if v]
            if active: print(f"   牌型：{'、'.join(active)}")
    else:
        print(f"⚠️ 牌数异常：{total}张")


if __name__ == "__main__":
    main()
