#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
吠陀占星分盘计算模块 v1.0
BPHS Shodasavarga（十六分盘体系）
支持: D2/D3/D4/D7/D9/D10/D12/D16/D20/D24/D27/D30/D40/D45/D60
每个分盘输出精确度数，支持进一步分析。
"""
from typing import Dict, List, Optional

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGNS_CN = {s: f"{cn}" for s, cn in zip(SIGNS,
    ['白羊座','金牛座','双子座','巨蟹座','狮子座','处女座',
     '天秤座','天蝎座','射手座','摩羯座','水瓶座','双鱼座'])}
SIGN_LORDS = {'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury','Cancer':'Moon',
    'Leo':'Sun','Virgo':'Mercury','Libra':'Venus','Scorpio':'Mars',
    'Sagittarius':'Jupiter','Capricorn':'Saturn','Aquarius':'Saturn','Pisces':'Jupiter'}
EXALT_SIGN = {'Sun':0,'Moon':1,'Mars':9,'Mercury':5,'Jupiter':3,'Venus':11,'Saturn':6}
DEBIL_SIGN = {'Sun':6,'Moon':7,'Mars':3,'Mercury':11,'Jupiter':9,'Venus':5,'Saturn':0}
OWN_SIGNS = {'Sun':[4],'Moon':[3],'Mars':[0,7],'Mercury':[2,5],
    'Jupiter':[8,11],'Venus':[1,6],'Saturn':[9,10]}
VARGA_META = {
    2:{'name':'Hora','cn':'财富','area':'财富资源'},3:{'name':'Drekkana','cn':'兄弟','area':'兄弟姐妹'},
    4:{'name':'Turyamsa','cn':'财产','area':'财产住所'},7:{'name':'Saptamsa','cn':'子女','area':'子女后代'},
    9:{'name':'Navamsa','cn':'婚姻','area':'婚姻伴侣灵魂'},10:{'name':'Dasamsa','cn':'事业','area':'事业公众形象'},
    12:{'name':'Dwadashamsa','cn':'父母','area':'父母祖先'},16:{'name':'Shodasamsa','cn':'享受','area':'车辆物质'},
    20:{'name':'Vimsamsa','cn':'修行','area':'精神修行'},24:{'name':'Siddhamsa','cn':'学识','area':'教育学识'},
    27:{'name':'Bhamsa','cn':'力量','area':'力量弱点'},30:{'name':'Trimsamsa','cn':'苦难','area':'灾难苦难'},
    40:{'name':'Khavedamsa','cn':'运势','area':'吉凶运势'},45:{'name':'Akshavedamsa','cn':'格局','area':'整体格局'},
    60:{'name':'Shashtyamsa','cn':'业力','area':'前世业力同盘区分'}}

def _si(lon): return int(lon/30)%12
def _sn(i): return SIGNS[i%12]
def _odd(si): return si%2==0  # Aries(0)=odd

def _d30_map(si, pi):
    if _odd(si):
        if pi<5: return 0
        if pi<10: return 10
        if pi<18: return 8
        if pi<25: return 2
        return 6
    else:
        if pi<5: return 1
        if pi<12: return 5
        if pi<20: return 9
        if pi<25: return 7
        return 11

def varga_map(si, pi, div):
    """BPHS分盘映射：星座索引si的第pi份→目标星座索引"""
    o = _odd(si)
    if div==2: return (4 if o else 3) if pi==0 else (3 if o else 4)
    if div==3: return (si+pi*4)%12 if o else (si+8+pi*4)%12
    if div==4: return (si+pi)%12 if o else (si+8+pi)%12
    if div==7: return (si+pi)%12 if o else (si+6+pi)%12
    if div==9:
        el={0:0,1:9,2:6,3:3}; return (el[si%4]+pi)%12
    if div==10: return (si+pi)%12 if o else (si+9+pi)%12  # D10: even signs start from 9th (2026-05-03 fix: was +8)
    if div==12: return (si+pi)%12
    if div==16: return ((0 if o else 4)+pi)%12  # D16: movable=+0, fixed=+4; dual needs separate (2026-05-03 fix: was +1)
    if div==20: return ((0 if o else 8)+pi)%12
    if div==24: return ((4 if o else 3)+pi)%12
    if div==27: return ((0 if o else 6)+pi)%12
    if div==30: return _d30_map(si,pi)
    if div==40: return ((0 if o else 6)+pi)%12
    if div==45: return ((0 if o else 6)+pi)%12
    if div==60: return (si+pi)%12 if o else (si+1+pi)%12
    raise ValueError(f"不支持的D{div}")

def calc_varga(lon, div):
    """计算行星在指定分盘的位置（星座+精确度数+尊贵状态）"""
    # 2026-05-03修正：D9 Navamsa使用Harmonic(×9)法而非BPHS映射法
    # 原因：Harmonic法与主流Jyotish软件(Jagannatha Hora等)结果一致
    # 且在Einstein等名人案例中与人生事件吻合度更高
    # BPHS映射法(el={0:0,1:9,2:6,3:3})仍保留在varga_map中作为备选
    if div == 9:
        nav_lon = (lon * 9) % 360
        vsi = int(nav_lon / 30) % 12
        dp = nav_lon - vsi * 30
        pi = int(dp / (30.0/9))  # approximate pada from harmonic degree
        r = {'sign': _sn(vsi), 'sign_idx': vsi, 'degree_in_sign': round(dp, 4),
             'part_index': pi, 'lord': SIGN_LORDS.get(_sn(vsi), ''), 'pada': pi + 1}
        return r
    si=_si(lon); d=lon-si*30; ps=30.0/div; pi=int(d/ps); dp=d-pi*ps
    vsi=varga_map(si,pi,div)
    r={'sign':_sn(vsi),'sign_idx':vsi,'degree_in_sign':round(dp,4),
       'part_index':pi,'lord':SIGN_LORDS.get(_sn(vsi),'')}
    if div==9: r['pada']=pi+1
    return r

def dignity(planet, sign_idx):
    if planet in EXALT_SIGN and sign_idx==EXALT_SIGN[planet]: return 'Exalted'
    if planet in DEBIL_SIGN and sign_idx==DEBIL_SIGN[planet]: return 'Debilitated'
    if planet in OWN_SIGNS and sign_idx in OWN_SIGNS[planet]: return 'Own Sign'
    return 'Neutral'

def calc_all_vargas(planet_lons, asc_lon, divisions=None):
    """批量计算所有指定分盘"""
    if divisions is None:
        divisions=[2,3,4,7,9,10,12,16,20,24,27,30,40,45,60]
    results={}
    for div in divisions:
        m=VARGA_META.get(div,{})
        key=f"D{div}_{m.get('name',f'D{div}')}"
        vd={'_meta':{'div':div,'name':m.get('name',''),'cn':m.get('cn',''),
                      'area':m.get('area',''),'part_size':30.0/div}}
        vd['Ascendant']=calc_varga(asc_lon,div)
        for pn,lon in planet_lons.items():
            vd[pn]=calc_varga(lon,div)
        # 尊贵状态
        vd['_dignity']={pn:dignity(pn,pd['sign_idx'])
            for pn,pd in vd.items() if pn not in ('Ascendant','_meta') and isinstance(pd,dict) and 'sign_idx' in pd}
        # D9专项
        if div==9:
            ai=vd['Ascendant']['sign_idx']
            s7=(ai+6)%12
            p7=[pn for pn,pd in vd.items() if isinstance(pd,dict) and pd.get('sign_idx')==s7]
            vd['_d9_analysis']={
                'navamsa_7th_sign':_sn(s7),'navamsa_7th_lord':SIGN_LORDS.get(_sn(s7),''),
                'planets_in_d9_7th':p7,
                'venus_d9':f"{vd.get('Venus',{}).get('sign','?')} {vd.get('Venus',{}).get('degree_in_sign',0):.2f}°",
                'jupiter_d9':f"{vd.get('Jupiter',{}).get('sign','?')} {vd.get('Jupiter',{}).get('degree_in_sign',0):.2f}°",
                'venus_dignity':dignity('Venus',vd.get('Venus',{}).get('sign_idx',-1)),
                'jupiter_dignity':dignity('Jupiter',vd.get('Jupiter',{}).get('sign_idx',-1)),
            }
        # D60专项
        if div==60:
            ai=vd['Ascendant']['sign_idx']
            ben,mal=[],[]
            for pn,pd in vd.items():
                if not isinstance(pd,dict) or 'sign_idx' not in pd: continue
                h=((pd['sign_idx']-ai)%12)+1
                if h in (1,4,7,10):
                    if pn in ('Jupiter','Venus','Moon'): ben.append(f"{pn}({h}宫)")
                    elif pn in ('Saturn','Mars','Sun','Rahu','Ketu'): mal.append(f"{pn}({h}宫)")
            vd['_d60_analysis']={'benefics_in_kendras':ben,'malefics_in_kendras':mal,
                'karma_hint':'前世善业较重' if len(ben)>len(mal) else '前世有业力课题' if len(mal)>len(ben) else '善恶交织'}
        results[key]=vd
    return results
