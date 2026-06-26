#!/usr/bin/env python3
"""
牛妖股评分体系 V1.0 - 
权重重构：题材25 + 股性20 + 开盘15 + 换手15 + 情绪15 + 连板10 = 100分
用法: python3 niu_yao_v1.py [--date YYYYMMDD]
"""

import akshare as ak
import sys
from datetime import datetime, timedelta
from collections import Counter

# ========== V1.0 评分体系（前瞻型）==========

def calc_theme_score(theme_stat):
    """题材强度评分（满分25分）- 方案C：排名+占比混合制
    
    基础分（按排名）:
        Top1: 20分 / Top2: 18分 / Top3: 15分 / Top4-5: 10分 / Top6-10: 5分 / 其他: 0分
    占比加成:
        >10%: +5分 / 5-10%: +2分 / <5%: +0分
    """
    rank = theme_stat.get('rank', 999)
    pct = theme_stat.get('pct', 0)
    
    # 基础分
    if rank == 1:       base = 20
    elif rank == 2:     base = 18
    elif rank == 3:     base = 15
    elif rank <= 5:     base = 10
    elif rank <= 10:    base = 5
    else:               base = 0
    
    # 占比加成
    if pct > 10:        bonus = 5
    elif pct >= 5:      bonus = 2
    else:               bonus = 0
    
    return min(base + bonus, 25)  # 封顶25分

def calc_xing_score(limit_10d):
    """股性评分（近10日涨停次数，满分20分）- 盘前可知"""
    if limit_10d >= 5:    return 20
    elif limit_10d >= 3:  return 15
    elif limit_10d >= 2:  return 10
    elif limit_10d >= 1:  return 5
    else:                 return 0

def calc_open_score(open_pct):
    """开盘涨幅评分（满分15分）- 竞价可知"""
    if open_pct < 0:       return 0
    elif open_pct < 3:     return 5
    elif open_pct < 7:     return 10
    elif open_pct <= 10:   return 15
    else:                  return 8

def calc_turn_score(turn):
    """换手率评分（满分15分）- 当天可知"""
    if turn < 3:     return 0
    elif turn < 8:   return 5
    elif turn < 15:  return 10
    elif turn < 25:  return 13
    else:            return 15

def calc_market_score(limit_up_count):
    """市场情绪评分（满分15分）- 当天可知"""
    if limit_up_count > 100:   return 15
    elif limit_up_count > 80:  return 12
    elif limit_up_count >= 50: return 8
    else:                      return 0

def calc_board_score(board):
    """连板高度评分（满分10分）- 辅助验证"""
    if board >= 5:   return 10
    elif board == 4: return 8
    elif board == 3: return 6
    elif board == 2: return 4
    elif board == 1: return 2
    else:            return 0

def get_grade(score):
    if score >= 80:   return "S级"
    elif score >= 65: return "A级"
    elif score >= 50: return "B级"
    elif score >= 35: return "C级"
    else:             return "D级"

# ========== 准确数据获取 ==========

def get_last_n_trading_days(end_date_str, n=3):
    """获取最近n个交易日"""
    end = datetime.strptime(end_date_str, '%Y%m%d')
    dates = []
    current = end
    attempts = 0
    while len(dates) < n and attempts < 15:
        date_str = current.strftime('%Y%m%d')
        try:
            df = ak.stock_zt_pool_em(date=date_str)
            if len(df) > 0:
                dates.append(date_str)
        except:
            pass
        current -= timedelta(days=1)
        attempts += 1
    return dates

def get_10d_limit_up_count(code, end_date_str):
    """近10个交易日涨停次数（准确值）"""
    end = datetime.strptime(end_date_str, '%Y%m%d')
    count = 0
    checked = 0
    current = end
    
    while checked < 10:
        date_str = current.strftime('%Y%m%d')
        try:
            df = ak.stock_zt_pool_em(date=date_str)
            if len(df) > 0:
                checked += 1
                if len(df[df['代码'] == code]) > 0:
                    count += 1
        except:
            pass
        current -= timedelta(days=1)
    
    return count

def get_open_pct_accurate(code, date_str):
    """准确开盘涨幅（%）"""
    try:
        prefix = 'sh' if code.startswith('6') else 'sz'
        target_date = datetime.strptime(date_str, '%Y%m%d').date()
        
        df = ak.stock_zh_a_daily(
            symbol=f'{prefix}{code}',
            start_date=(datetime.strptime(date_str, '%Y%m%d') - timedelta(days=5)).strftime('%Y%m%d'),
            end_date=date_str
        )
        if len(df) < 2:
            return None
        
        target_idx = None
        for i, row in df.iterrows():
            if row['date'] == target_date:
                target_idx = i
                break
        
        if target_idx is None or target_idx == 0:
            return None
        
        today_open = float(df.iloc[target_idx]['open'])
        prev_close = float(df.iloc[target_idx - 1]['close'])
        
        if prev_close == 0:
            return None
        
        open_pct = (today_open / prev_close - 1) * 100
        return round(open_pct, 2)
    except:
        return None

def get_theme_stats(zt_pools):
    """获取题材统计：排名 + 占比"""
    all_industries = []
    for df in zt_pools:
        if df is not None and len(df) > 0:
            all_industries.extend(df['所属行业'].dropna().tolist())
    
    counter = Counter(all_industries)
    total = len(all_industries)
    
    # 返回 [(industry, count, rank, pct), ...]
    stats = []
    for rank, (name, count) in enumerate(counter.most_common(), 1):
        pct = count / total * 100 if total > 0 else 0
        stats.append({
            'name': name,
            'count': count,
            'rank': rank,
            'pct': round(pct, 1)
        })
    
    return stats

def get_top3_themes(zt_pools):
    """推断最强主线Top3（兼容旧接口）"""
    stats = get_theme_stats(zt_pools)
    return [s['name'] for s in stats[:3]]

def parse_limit_stats(stats_str):
    try:
        if '/' in str(stats_str):
            parts = str(stats_str).split('/')
            return int(parts[0])
    except:
        pass
    return 1

def infer_open_pct(first_seal_time):
    """通过首次封板时间推断开盘涨幅（备用）"""
    t = str(first_seal_time)
    if t <= '092800':
        return 10.0
    elif t <= '094500':
        return 7.0
    elif t <= '103000':
        return 4.0
    else:
        return 2.0

# ========== V1.0 主流程 ==========

def run_v1_score(target_date=None):
    """V1.0评分"""
    if target_date is None:
        target_date = datetime.now().strftime('%Y%m%d')
    
    print(f"🦞 牛妖股评分 V1.0 · 版 · {target_date}")
    print("="*60)
    print("权重: 题材25 + 股性20 + 开盘15 + 换手15 + 情绪15 + 连板10 = 100")
    print("="*60)
    
    # Step 1: 获取最近3个交易日
    trading_days = get_last_n_trading_days(target_date, n=3)
    if len(trading_days) < 3:
        print(f"⚠️ 只获取到 {len(trading_days)} 个交易日")
    
    print(f"\n📅 分析日期: {' / '.join(trading_days)}")
    
    # Step 2: 拉取3日涨停池
    zt_pools = []
    all_candidates = {}
    
    for day in trading_days:
        try:
            df = ak.stock_zt_pool_em(date=day)
            zt_pools.append(df)
            print(f"   {day}: {len(df)}只涨停")
            
            for _, row in df.iterrows():
                code = str(row['代码']).zfill(6)
                name = row['名称']
                industry = row.get('所属行业', '')
                board = int(row.get('连板数', 1))
                turn = float(row.get('换手率', 0))
                market_cap = float(row.get('流通市值', 0)) / 1e8
                limit_stats = row.get('涨停统计', '1/1')
                recent_limit = parse_limit_stats(limit_stats)
                first_seal = str(row.get('首次封板时间', '093000'))
                
                if code not in all_candidates:
                    all_candidates[code] = {
                        'code': code, 'name': name, 'industry': industry,
                        'max_board': board, 'limit_up_days': 1,
                        'latest_date': day, 'latest_turn': turn,
                        'latest_market_cap': market_cap,
                        'latest_first_seal': first_seal,
                        'today_limit_up': (day == target_date)
                    }
                else:
                    cand = all_candidates[code]
                    cand['max_board'] = max(cand['max_board'], board)
                    cand['limit_up_days'] += 1
                    if day > cand['latest_date']:
                        cand['latest_date'] = day
                        cand['latest_turn'] = turn
                        cand['latest_market_cap'] = market_cap
                        cand['latest_first_seal'] = first_seal
                        cand['today_limit_up'] = (day == target_date)
        except Exception as e:
            print(f"   {day}: 拉取失败 ({e})")
            zt_pools.append(None)
    
    total_candidates = len(all_candidates)
    today_limit_count = sum(1 for c in all_candidates.values() if c['today_limit_up'])
    
    print(f"\n📊 3日候选池: {total_candidates}只 (今日涨停{today_limit_count}只)")
    
    # Step 3: 推断主线 + 题材统计
    theme_stats = get_theme_stats([p for p in zt_pools if p is not None])
    top3_themes = [s['name'] for s in theme_stats[:3]]
    
    print(f"🔥 3日最强主线Top3: {' / '.join(top3_themes)}")
    print(f"\n📊 题材分布Top10:")
    for s in theme_stats[:10]:
        print(f"   {s['rank']}. {s['name']}: {s['count']}只 ({s['pct']}%)")
    
    # Step 4: 获取准确数据
    print(f"\n⏳ 获取准确数据中...")
    
    accurate_data = {}
    for i, code in enumerate(all_candidates.keys()):
        if i % 20 == 0:
            print(f"   进度: {i}/{total_candidates}...")
        
        limit_10d = get_10d_limit_up_count(code, target_date)
        open_pct = get_open_pct_accurate(code, target_date)
        
        accurate_data[code] = {
            'limit_10d': limit_10d,
            'open_pct': open_pct
        }
    
    print(f"   完成: {total_candidates}/{total_candidates}")
    
    # Step 5: V1.0 评分
    results = []
    for code, cand in all_candidates.items():
        if cand['latest_market_cap'] >= 100:
            continue
        
        # 查找题材统计
        theme_stat = {'rank': 999, 'pct': 0}
        for s in theme_stats:
            if s['name'] == cand['industry']:
                theme_stat = s
                break
        
        is_top3 = theme_stat['rank'] <= 3
        
        acc = accurate_data.get(code, {})
        open_pct = acc.get('open_pct')
        if open_pct is None:
            open_pct = infer_open_pct(cand['latest_first_seal'])
        
        limit_10d = acc.get('limit_10d', cand['limit_up_days'])
        
        # V1.0 六大指标评分
        details = {}
        details['题材强度'] = calc_theme_score(theme_stat)
        details['股性'] = calc_xing_score(limit_10d)
        details['开盘涨幅'] = calc_open_score(open_pct)
        details['换手率'] = calc_turn_score(cand['latest_turn'])
        details['市场情绪'] = calc_market_score(today_limit_count)
        details['连板高度'] = calc_board_score(cand['max_board'])
        
        total = sum(details.values())
        
        # 今日涨停加分
        if cand['today_limit_up']:
            details['今日涨停'] = 5
            total += 5
        
        results.append({
            'name': cand['name'],
            'code': cand['code'],
            'industry': cand['industry'],
            'is_top3': is_top3,
            'theme_rank': theme_stat['rank'],
            'theme_pct': theme_stat['pct'],
            'max_board': cand['max_board'],
            'limit_up_days': cand['limit_up_days'],
            'limit_10d': limit_10d,
            'today_limit_up': cand['today_limit_up'],
            'turn': cand['latest_turn'],
            'market_cap': round(cand['latest_market_cap'], 1),
            'open_pct': round(open_pct, 1) if open_pct else None,
            'score': total,
            'grade': get_grade(total),
            'details': details
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n📈 通过硬门槛: {len(results)}/{total_candidates}只")
    
    grades = {}
    for r in results:
        g = r['grade']
        grades[g] = grades.get(g, 0) + 1
    if grades:
        print(f"   等级分布: ", end="")
        for g in ['S级', 'A级', 'B级', 'C级', 'D级']:
            if g in grades:
                print(f"{g}:{grades[g]}只 ", end="")
        print()
    
    return results[:20]

def format_v1_top20(results, date_str):
    """格式化V1.0 Top20榜单"""
    lines = []
    lines.append(f"# 🦞 牛妖股Top20榜单 · V1.0前瞻版 · {date_str}")
    lines.append(f"> 权重: 题材25 + 股性20 + 开盘15 + 换手15 + 情绪15 + 连板10 = 100")
    lines.append(f"> 题材评分=排名基础分+占比加成 | 候选池=3日涨停 | 开盘/股性=真实数据")
    lines.append("")
    lines.append("| 排名 | 股票 | 代码 | 等级 | 总分 | 题材分 | 股性 | 开盘 | 换手 | 情绪 | 连板 | 题材排名 | 今日 |")
    lines.append("|------|------|------|------|------|--------|------|------|------|------|------|----------|------|")
    
    for i, r in enumerate(results, 1):
        today_mark = "🔴" if r['today_limit_up'] else "⚪"
        d = r['details']
        
        lines.append(
            f"| {i} | **{r['name']}** | {r['code']} | **{r['grade']}** | {r['score']} | "
            f"{d['题材强度']} | {d['股性']} | {d['开盘涨幅']} | {d['换手率']} | {d['市场情绪']} | {d['连板高度']} | "
            f"Top{r['theme_rank']}({r['theme_pct']}%) | {today_mark} |"
        )
    
    lines.append("")
    lines.append("**图例**: 🔴=今日涨停 / ⚪=今日未涨停")
    lines.append("")
    lines.append("---")
    lines.append("*V1.0前瞻版: 题材评分=排名基础分(Top1=20/Top2=18/Top3=15/Top4-5=10/Top6-10=5)+占比加成(>10%=+5/5-10%=+2)*")
    
    return "\n".join(lines)

def main():
    date_str = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--date' else None
    
    results = run_v1_score(date_str)
    if results:
        date_display = date_str or datetime.now().strftime('%Y%m%d')
        md = format_v1_top20(results, date_display)
        print("\n" + md)
        
        import os
        os.makedirs("/root/.openclaw/workspace/reports", exist_ok=True)
        filename = f"/root/.openclaw/workspace/reports/niu_yao_v1_{date_display}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"\n💾 已保存: {filename}")

if __name__ == "__main__":
    main()
)
