#!/usr/bin/env python3
"""
大规模协同验证：18名人婚姻案例 × 5功能模块
测试: Double Transit PAC+D9, Transit LL/7L, 行星聚集, Vivah Saham, Chara Dasha
"""
import sys, json, os
sys.path.insert(0, '/Users/wuyongnaren/WorkBuddy/yinduzhanxing/scripts')
import swisseph as swe
swe.set_ephe_path('')

from jyotish_engine import (
    compute_chart_data, cmd_double_transit_pac, cmd_transit_ll7l,
    cmd_planetary_congregation, cmd_vivah_saham, SIGN_LORDS, SIGNS
)
from jaimini import calc_chara_dasha_with_antardasha

# 18名人案例（来自 v6.1 验证脚本）
CASES = [
    {'name':'Nelson Mandela','birth':(1918,7,18,14.0,-33.32,26.52),'gender':'M',
     'marriage1':(1944,10,5)},
    {'name':'Tom Cruise','birth':(1962,7,3,19.25,43.05,-76.15),'gender':'M',
     'marriage1':(1987,5,9)},
    {'name':'Elon Musk','birth':(1971,6,28,5.0,-25.74,28.19),'gender':'M',
     'marriage1':(2000,1,1)},
    {'name':'Oprah Winfrey','birth':(1954,1,29,11.88,33.51,-88.52),'gender':'F',
     'marriage1':(1986,1,1)},
    {'name':'Prince Harry','birth':(1984,9,15,15.33,51.5,-0.17),'gender':'M',
     'marriage1':(2018,5,19)},
    {'name':'Jeff Bezos','birth':(1964,1,12,9.63,25.78,-80.19),'gender':'M',
     'marriage1':(1993,1,1)},
    {'name':'Priyanka Chopra','birth':(1982,7,18,10.5,23.57,87.19),'gender':'F',
     'marriage1':(2018,12,1)},
    {'name':'Shah Rukh Khan','birth':(1965,11,1,21.25,28.61,77.21),'gender':'M',
     'marriage1':(1991,10,25)},
    {'name':'Britney Spears','birth':(1981,12,2,19.92,31.17,-89.18),'gender':'F',
     'marriage1':(2004,1,3)},
    {'name':'Mark Zuckerberg','birth':(1984,5,14,19.67,40.71,-74.01),'gender':'M',
     'marriage1':(2012,5,19)},
    {'name':'Narendra Modi','birth':(1950,9,17,4.78,23.03,72.58),'gender':'M',
     'marriage1':(1968,1,1)},
    {'name':'Amitabh Bachchan','birth':(1942,10,11,10.5,25.43,81.85),'gender':'M',
     'marriage1':(1973,6,3)},
]

def make_args(y,m,d,h,mi,lat,lon,tz,date_str,house=7):
    """构建 args 对象"""
    return type('Args', (), {
        'year':y,'month':m,'day':d,'hour':h,'minute':mi,
        'lat':lat,'lon':lon,'tz':tz,
        'date':date_str,'house':house,
        'transit_date':date_str,
    })()

def run():
    results = []
    stats = {'dt':0,'p5':0,'p8':0,'pariv':0,'cong':0,'vs':0,'cd':0}
    total = 0
    
    for case in CASES:
        y,m,d,h_utc,lat,lon = case['birth']
        name = case['name']
        my,mm,md_d = case['marriage1']
        date_str = f"{my}-{mm:02d}-{md_d:02d}"
        total += 1
        
        # 转UTC hour (假设 birth 中 h 已经是 UTC)
        hour_int = int(h_utc)
        minute_int = int((h_utc - hour_int) * 60)
        tz = 0  # UTC
        
        print(f"\n{'='*50}")
        print(f"[{total}] {name} | 婚姻: {date_str}")
        print(f"{'='*50}")
        
        signals = []
        
        # 1. Double Transit PAC + D9
        dt_hit = False
        try:
            dt_r = cmd_double_transit_pac(make_args(y,m,d,hour_int,minute_int,lat,lon,tz,date_str))
            dt_hit = len(dt_r.get('double_transit',[])) > 0
            if dt_hit:
                signals.append('DT')
                stats['dt'] += 1
            dt_list = dt_r.get('double_transit',[])
            layer_str = ','.join(set(l['layer'] for l in dt_list)) if dt_list else '-'
            dt_summary = dt_r.get('summary','')
            print(f"  [DT PAC+D9] {'✅' if dt_hit else '❌'} layers={layer_str} {dt_summary}")
        except Exception as e:
            print(f"  [DT PAC+D9] ERROR: {e}")
            dt_hit = False  # ERROR不计为hit
        
        # 2. Transit LL/7L
        try:
            ll7l_r = cmd_transit_ll7l(make_args(y,m,d,hour_int,minute_int,lat,lon,tz,date_str))
            p5 = ll7l_r['p5']['hit']
            p8 = ll7l_r['p8']['hit']
            pariv = ll7l_r['parivartana']['hit']
            if p5: signals.append('P5'); stats['p5'] += 1
            if p8: signals.append('P8'); stats['p8'] += 1
            if pariv: signals.append('Pariv'); stats['pariv'] += 1
            print(f"  [LL/7L] P5={'✅' if p5 else '❌'} P8={'✅' if p8 else '❌'} Pariv={'✅' if pariv else '❌'}")
        except Exception as e:
            print(f"  [LL/7L] ERROR: {e}")
        
        # 3. 行星聚集
        try:
            cong_r = cmd_planetary_congregation(make_args(y,m,d,hour_int,minute_int,lat,lon,tz,date_str,7))
            cong_hit = cong_r.get('hit', False)
            if cong_hit: signals.append('聚集'); stats['cong'] += 1
            print(f"  [聚集] {'✅' if cong_hit else '❌'} {cong_r.get('summary','')}")
        except Exception as e:
            print(f"  [聚集] ERROR: {e}")
        
        # 4. Vivah Saham
        try:
            vs_r = cmd_vivah_saham(make_args(y,m,d,hour_int,minute_int,lat,lon,tz,date_str))
            ta = vs_r.get('transit_activation', {})
            vs_double = ta.get('double_activation', False) if ta else False
            if vs_double: signals.append('VS双星'); stats['vs'] += 1
            jup = [c['type'] for c in ta.get('jupiter',[])] if ta else []
            sat = [c['type'] for c in ta.get('saturn',[])] if ta else []
            vs_s = vs_r.get('vivah_saham',{})
            print(f"  [VivahSaham] {vs_s.get('sign_cn','?')} {vs_s.get('degree_in_sign',0):.1f}° | 双星={'✅' if vs_double else '❌'} Jup={jup} Sat={sat}")
        except Exception as e:
            print(f"  [VivahSaham] ERROR: {e}")
        
        # 5. Chara Dasha (Antardasha)
        try:
            chart, asc_idx, jd, aya = compute_chart_data(y,m,d,hour_int,minute_int,lat,lon,tz)
            if chart:
                p_lons = {pn: pd['degree'] for pn, pd in chart['planets'].items() if 'degree' in pd}
                cd = calc_chara_dasha_with_antardasha(asc_idx, p_lons, y, m)
                m_year, m_month = my, mm
                md_name = ''; ad_name = ''
                for md_d in cd['dasha_sequence']:
                    s_y, s_m = map(int, md_d['start_date'].split('-'))
                    e_y, e_m = map(int, md_d['end_date'].split('-'))
                    if (m_year > s_y or (m_year == s_y and m_month >= s_m)) and \
                       (m_year < e_y or (m_year == e_y and m_month <= e_m)):
                        md_name = f"{md_d['sign']}({md_d['lord']})"
                        for ad in md_d.get('antardashas', []):
                            as_y, as_m = map(int, ad['start_date'].split('-'))
                            ae_y, ae_m = map(int, ad['end_date'].split('-'))
                            if (m_year > as_y or (m_year == as_y and m_month >= as_m)) and \
                               (m_year < ae_y or (m_year == ae_y and m_month <= ae_m)):
                                ad_name = f"{ad['sign']}({ad['lord']})"
                                break
                        break
                # 检查 MD 或 AD 是否涉及 7 宫相关
                seven_sign = SIGNS[(asc_idx + 6) % 12]
                seven_lord = SIGN_LORDS[seven_sign]
                ll = SIGN_LORDS[SIGNS[asc_idx]]
                cd_relevant = seven_lord in md_name or ll in md_name or seven_lord in ad_name or ll in ad_name
                if cd_relevant: signals.append('CD'); stats['cd'] += 1
                print(f"  [CharaDasha] MD={md_name} AD={ad_name} | 7宫相关={'✅' if cd_relevant else '❌'}")
        except Exception as e:
            print(f"  [CharaDasha] ERROR: {e}")
        
        score = len(signals)
        if score >= 3: verdict = '✅强'
        elif score == 2: verdict = '⚠️中'
        elif score == 1: verdict = '⚠️弱'
        else: verdict = '❌无'
        
        print(f"  >>> 综合: {verdict} ({score}/6) 信号={signals}")
        
        results.append({
            'name': name, 'marriage': date_str,
            'signals': signals, 'score': score, 'verdict': verdict,
        })
    
    # 汇总
    print(f"\n{'='*60}")
    print(f"大规模验证汇总 ({total} 案例)")
    print(f"{'='*60}")
    
    strong = sum(1 for r in results if r['score'] >= 3)
    medium = sum(1 for r in results if r['score'] == 2)
    weak = sum(1 for r in results if r['score'] == 1)
    none_c = sum(1 for r in results if r['score'] == 0)
    
    print(f"\n综合评分分布:")
    print(f"  强确认 (≥3信号): {strong}/{total} ({strong/total*100:.0f}%)")
    print(f"  中等确认 (2信号): {medium}/{total} ({medium/total*100:.0f}%)")
    print(f"  弱信号 (1信号):   {weak}/{total} ({weak/total*100:.0f}%)")
    print(f"  无确认 (0信号):   {none_c}/{total} ({none_c/total*100:.0f}%)")
    
    print(f"\n各功能命中率:")
    print(f"  Double Transit PAC+D9:   {stats['dt']}/{total} ({stats['dt']/total*100:.0f}%)")
    print(f"  Transit LL/7L P5:        {stats['p5']}/{total} ({stats['p5']/total*100:.0f}%)")
    print(f"  Transit LL/7L P8:        {stats['p8']}/{total} ({stats['p8']/total*100:.0f}%)")
    print(f"  Parivartana 互换:        {stats['pariv']}/{total} ({stats['pariv']/total*100:.0f}%)")
    print(f"  行星聚集:                {stats['cong']}/{total} ({stats['cong']/total*100:.0f}%)")
    print(f"  Vivah Saham 双星激活:    {stats['vs']}/{total} ({stats['vs']/total*100:.0f}%)")
    print(f"  Chara Dasha 7宫相关:     {stats['cd']}/{total} ({stats['cd']/total*100:.0f}%)")
    
    avg_score = sum(r['score'] for r in results) / total
    at_least_1 = sum(1 for r in results if r['score'] >= 1)
    at_least_2 = sum(1 for r in results if r['score'] >= 2)
    print(f"\n核心指标:")
    print(f"  平均信号数: {avg_score:.1f}/6")
    print(f"  ≥1信号覆盖率: {at_least_1}/{total} ({at_least_1/total*100:.0f}%)")
    print(f"  ≥2信号覆盖率: {at_least_2}/{total} ({at_least_2/total*100:.0f}%)")
    
    # 保存
    out = '/Users/wuyongnaren/WorkBuddy/2026-05-03-task-3/verify-large-scale-results.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({'results': results, 'stats': stats, 'total': total}, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {out}")

if __name__ == '__main__':
    run()
