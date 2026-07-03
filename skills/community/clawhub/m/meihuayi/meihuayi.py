
#!/usr/bin/env python3
"""梅花易数排盘"""
import datetime, time, json, os, urllib.request
from typing import Dict, Tuple

# ══════════════════════════════════════════════
#  Step 1: 自动检查并下载 iching.json
# ══════════════════════════════════════════════
_DATA_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
_ICHING_PATH = os.path.join(_DATA_DIR, 'iching.json')
_ICHING_URL  = "https://raw.githubusercontent.com/john-walks-slow/open-iching/master/iching/iching.json"

def _ensure_iching_data():
    if not os.path.exists(_DATA_DIR):
        os.makedirs(_DATA_DIR)
        print(f"[初始化] 已创建目录：{_DATA_DIR}")
    if not os.path.exists(_ICHING_PATH):
        print("[初始化] 未找到 iching.json，正在从网络下载...")
        try:
            urllib.request.urlretrieve(_ICHING_URL, _ICHING_PATH)
            print(f"[初始化] 下载完成 → {_ICHING_PATH}")
        except Exception as e:
            raise RuntimeError(
                f"[错误] iching.json 下载失败：{e}\n"
                f"请手动下载：{_ICHING_URL}\n"
                f"并保存至：{_ICHING_PATH}"
            )
    else:
        print(f"[初始化] 已找到 iching.json ✓")

_ensure_iching_data()

with open(_ICHING_PATH, 'r', encoding='utf-8') as f:
    _RAW = json.load(f)

# ══════════════════════════════════════════════
#  Step 2: 八卦定义 & 自然名
# ══════════════════════════════════════════════
TRIGRAMS = {
    1: {"name": "乾", "element": "金", "symbol": "☰", "lines": ["yang", "yang", "yang"]},
    2: {"name": "兑", "element": "金", "symbol": "☱", "lines": ["yang", "yang", "yin"]},
    3: {"name": "离", "element": "火", "symbol": "☲", "lines": ["yang", "yin", "yang"]},
    4: {"name": "震", "element": "木", "symbol": "☳", "lines": ["yang", "yin", "yin"]},
    5: {"name": "巽", "element": "木", "symbol": "☴", "lines": ["yin", "yang", "yang"]},
    6: {"name": "坎", "element": "水", "symbol": "☵", "lines": ["yin", "yang", "yin"]},
    7: {"name": "艮", "element": "土", "symbol": "☶", "lines": ["yin", "yin", "yang"]},
    8: {"name": "坤", "element": "土", "symbol": "☷", "lines": ["yin", "yin", "yin"]},
}

TRIGRAM_NATURE = {
    "乾": "天", "兑": "泽", "离": "火", "震": "雷",
    "巽": "风", "坎": "水", "艮": "山", "坤": "地",
}

# ══════════════════════════════════════════════
#  Step 3: 构建卦索引
# ══════════════════════════════════════════════
def _bits_to_trigram_num(bits: list) -> int:
    pattern = ["yang" if b == 1 else "yin" for b in bits]
    for num, tri in TRIGRAMS.items():
        if tri["lines"] == pattern:
            return num
    return 1

_GUA_INDEX: Dict[Tuple[int, int], dict] = {}
for _h in _RAW:
    arr = _h["array"]
    lower_num = _bits_to_trigram_num(arr[0:3])
    upper_num = _bits_to_trigram_num(arr[3:6])
    _GUA_INDEX[(upper_num, lower_num)] = _h

# ══════════════════════════════════════════════
#  Step 4: 卦辞 / 爻辞 / 卦名 / 卦符号 接口
# ══════════════════════════════════════════════
def get_gua_ci(upper: int, lower: int) -> str:
    h = _GUA_INDEX.get((upper, lower))
    return h["scripture"] if h else "未知卦辞"

def get_yao_ci(upper: int, lower: int, yao: int) -> str:
    h = _GUA_INDEX.get((upper, lower))
    if not h:
        return f"详见{upper}卦{yao}爻"
    lines = h.get("lines", [])
    idx = yao - 1
    if 0 <= idx < len(lines):
        ln = lines[idx]
        return f"{ln['name']}，{ln['scripture']}"
    return f"详见{upper}卦{yao}爻"

def get_gua_name(upper: int, lower: int) -> str:
    h = _GUA_INDEX.get((upper, lower))
    return h["name"] if h else f"{TRIGRAMS[upper]['name']}{TRIGRAMS[lower]['name']}"

def get_gua_full_name(upper: int, lower: int) -> str:
    """上卦自然名 + 下卦自然名 + 短卦名，如 天泽履"""
    short        = get_gua_name(upper, lower)
    upper_nature = TRIGRAM_NATURE.get(TRIGRAMS[upper]['name'], TRIGRAMS[upper]['name'])
    lower_nature = TRIGRAM_NATURE.get(TRIGRAMS[lower]['name'], TRIGRAMS[lower]['name'])
    # 上下卦相同，如兑为泽、乾为天
    if upper == lower:
        return f"{short}为{lower_nature}"
    return f"{upper_nature}{lower_nature}{short}"

def get_gua_symbol(upper: int, lower: int) -> str:
    h = _GUA_INDEX.get((upper, lower))
    return h["symbol"] if h else "䷀"

# ══════════════════════════════════════════════
#  Step 5: 五行常量
# ══════════════════════════════════════════════
GENERATING = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
OVERCOMING = {"金":"木","木":"土","土":"水","水":"火","火":"金"}

# 月令对照：公历月份 → 农历月令地支
MONTH_LUNAR = {
    1:"寅", 2:"卯", 3:"辰", 4:"巳",  5:"午",  6:"未",
    7:"申", 8:"酉", 9:"戌", 10:"亥", 11:"子", 12:"丑",
}

# 五行旺衰表：规则「同我者旺，我生者相，生我者休，克我者囚，我克者死」
# 逐月推导，键=地支名，顺序：木火土金水
WX_MONTH_STATE = {
    "寅": {"木":"旺", "火":"相", "土":"死", "金":"囚", "水":"休"},  # 寅月(木)
    "卯": {"木":"旺", "火":"相", "土":"死", "金":"囚", "水":"休"},  # 卯月(木)
    "辰": {"木":"囚", "火":"休", "土":"旺", "金":"相", "水":"死"},  # 辰月(土)
    "巳": {"木":"休", "火":"旺", "土":"相", "金":"死", "水":"囚"},  # 巳月(火)
    "午": {"木":"休", "火":"旺", "土":"相", "金":"死", "水":"囚"},  # 午月(火)
    "未": {"木":"囚", "火":"休", "土":"旺", "金":"相", "水":"死"},  # 未月(土)
    "申": {"木":"死", "火":"囚", "土":"休", "金":"旺", "水":"相"},  # 申月(金)
    "酉": {"木":"死", "火":"囚", "土":"休", "金":"旺", "水":"相"},  # 酉月(金)
    "戌": {"木":"囚", "火":"休", "土":"旺", "金":"相", "水":"死"},  # 戌月(土)
    "亥": {"木":"相", "火":"死", "土":"囚", "金":"休", "水":"旺"},  # 亥月(水)
    "子": {"木":"相", "火":"死", "土":"囚", "金":"休", "水":"旺"},  # 子月(水)
    "丑": {"木":"囚", "火":"休", "土":"旺", "金":"相", "水":"死"},  # 丑月(土)
}

# 时辰对照表：地支 → 时辰序号（子=1 ... 亥=12）
SHICHEN_NUM = {
    '子':1, '丑':2, '寅':3, '卯':4, '辰':5, '巳':6,
    '午':7, '未':8, '申':9, '酉':10, '戌':11, '亥':12,
}

def _get_shichen(hour: int) -> Tuple[str, int]:
    """
    根据24小时制小时数返回 (地支名, 时辰序号 1-12)
    子时：23:00-00:59 → 1
    丑时：01:00-02:59 → 2
    ...以此类推
    """
    zhi_order = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
    if hour == 23:
        idx = 0
    else:
        idx = (hour + 1) // 2
    zhi = zhi_order[idx % 12]
    return zhi, SHICHEN_NUM[zhi]

# ══════════════════════════════════════════════
#  Step 6: PlumBlossom 主类
# ══════════════════════════════════════════════
class PlumBlossom:
    def __init__(self): pass

    def _mod8(self, n):
        r = n % 8; return r if r != 0 else 8

    def _mod6(self, n):
        r = n % 6; return r if r != 0 else 6

    def _get_hugua(self, upper: int, lower: int) -> Tuple[int, int]:
        lower_lines  = TRIGRAMS[lower]['lines']
        upper_lines  = TRIGRAMS[upper]['lines']
        bengua_lines = lower_lines + upper_lines
        hugua_lines  = bengua_lines[1:5]
        hugua_lower  = hugua_lines[:3]
        hugua_upper  = hugua_lines[1:4]
        def find_trigram(lines):
            for num, tri in TRIGRAMS.items():
                if tri['lines'] == lines: return num
            return 1
        return find_trigram(hugua_upper), find_trigram(hugua_lower)

    def _get_biangua(self, upper: int, lower: int, mv: int) -> Tuple[int, int]:
        lower_lines  = TRIGRAMS[lower]['lines']
        upper_lines  = TRIGRAMS[upper]['lines']
        bengua_lines = lower_lines + upper_lines
        idx = mv - 1
        bian_gua_lines = bengua_lines.copy()
        bian_gua_lines[idx] = 'yang' if bian_gua_lines[idx] == 'yin' else 'yin'
        def find_trigram(lines):
            for num, tri in TRIGRAMS.items():
                if tri['lines'] == lines: return num
            return 1
        return find_trigram(bian_gua_lines[3:]), find_trigram(bian_gua_lines[:3])

    def _wuxing_relation(self, body_elem: str, use_elem: str) -> Tuple[str, str]:
        if OVERCOMING.get(body_elem) == use_elem: return '体克用', '吉'  # 体克用
        if GENERATING.get(use_elem) == body_elem: return '用生体', '吉'
        if GENERATING.get(body_elem) == use_elem: return '体生用', '耗'
        if body_elem == use_elem:                  return '体用比和', '吉'
        return '用克体', '凶'  # 用克体

    def _get_ganzhi(self, year: int, month: int, day: int, hour: int) -> Dict:
        """干支推算（精准版）。日干支基于 2000-01-07 甲子日迭代；月支用节气校正。"""
        gan = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
        zhi = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']

        # ── 年干支 ──
        year_g = gan[(year - 4) % 10]
        year_z = zhi[(year - 4) % 12]

        # ── 月支（节气校正） ──
        # 月支以节气为界，立春→寅月，惊蛰→卯月，…小寒→丑月
        # 节气用近似日（±1天误差可接受）
        _SOLAR_TERMS = [  # (月, 日, 地支名)
            (1, 5, '丑'), (2, 4, '寅'), (3, 5, '卯'), (4, 5, '辰'),
            (5, 5, '巳'), (6, 5, '午'), (7, 7, '未'), (8, 7, '申'),
            (9, 7, '酉'), (10, 8, '戌'), (11, 7, '亥'), (12, 7, '子'),
        ]
        month_zhi = None
        for i, (st_m, st_d, zhi_name) in enumerate(_SOLAR_TERMS):
            next_st = _SOLAR_TERMS[(i + 1) % 12]
            if (month == st_m and day >= st_d) or \
               (month == next_st[0] and day < next_st[1]):
                month_zhi = zhi_name
                month_branch_idx = zhi.index(month_zhi)
                break
        if month_zhi is None:
            # fallback（极少触发）
            month_branch_idx = (month + 1) % 12
            month_zhi = zhi[month_branch_idx]

        # ── 月干 ──
        # 甲/己年正月丙寅, 乙/庚年正月戊寅, 丙/辛年正月庚寅, 丁/壬年壬寅, 戊/癸年甲寅
        year_stem_idx = (year - 4) % 10   # 0=甲…4=戊, 5=己…9=癸
        month_stem_start = ((year_stem_idx % 5) * 2 + 2) % 10  # 寅月起始干
        # 寅月 branch_idx=2 → offset 0
        month_offset = (zhi.index(month_zhi) - 2) % 12
        month_g = gan[(month_stem_start + month_offset) % 10]

        # ── 日干支（精确：从 2000-01-07 甲子日起算）──
        from datetime import date
        ref = date(2000, 1, 7)  # 甲子日
        target = date(year, month, day)
        delta = (target - ref).days
        day_g = gan[delta % 10]
        day_z = zhi[delta % 12]

        # ── 时干支 ──
        shichen_zhi, shichen_num = _get_shichen(hour)
        day_stem_idx = delta % 10
        # 甲/己日起甲子, 乙/庚日起丙子, 丙/辛日起戊子, 丁/壬日起庚子, 戊/癸日起壬子
        hour_stem_start = (day_stem_idx % 5) * 2
        hour_g = gan[(hour_stem_start + shichen_num - 1) % 10]

        return {
            'year':  year_g  + year_z,
            'month': month_g + month_zhi,
            'day':   day_g   + day_z,
            'hour':  hour_g  + shichen_zhi,
        }

    # ── 两种起卦方式 ──────────────────────────
    def time_divination(self, year: int, month: int, day: int, hour: int) -> Dict:
        """① 时间起卦（月日数用农历）：
        上卦:(年支数+农历月+农历日)÷8
        下卦:(年支数+农历月+农历日+时支数)÷8
        动爻:(年支数+农历月+农历日+时支数)÷6
        """
        from zhdate import ZhDate
        from datetime import datetime as dt
        greg = dt(year, month, day)
        lunar = ZhDate.from_datetime(greg)
        lunar_year  = lunar.lunar_year
        lunar_month = lunar.lunar_month
        lunar_day   = lunar.lunar_day

        year_zhi = (lunar_year - 4) % 12 + 1   # 农历年支：子=1 … 亥=12
        _, shichen_num = _get_shichen(hour)     # 时辰序数

        upper = self._mod8(year_zhi + lunar_month + lunar_day)
        lower = self._mod8(year_zhi + lunar_month + lunar_day + shichen_num)
        mv    = self._mod6(year_zhi + lunar_month + lunar_day + shichen_num)

        # ganzhi / 旺衰 仍用公历计算
        return self._build_result(upper, lower, mv,
            "时间", f"农历{lunar_month}月{lunar_day}日",
            month, year, month, day, hour)

    def number_divination(self, number: int, month: int = None) -> Dict:
        """
        ② 数字起卦：传入一个三位整数
        - 上卦：百位数字 除以8取余
        - 下卦：十位数字 + 个位数字 之和 除以8取余
        - 动爻：三位数字之和 + 当前时辰数(1-12) 除以6取余
        """
        if number < 100 or number > 999:
            raise ValueError(f"数字起卦需要传入三位整数（100-999），收到：{number}")

        d1 = number // 100          # 百位
        d2 = (number // 10) % 10   # 十位
        d3 = number % 10           # 个位

        upper = self._mod8(d1)
        lower = self._mod8(d2 + d3)

        bjt = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))
        _, shichen_num = _get_shichen(bjt.hour)
        mv = self._mod6(d1 + d2 + d3 + shichen_num)

        if month is None:
            month = bjt.month

        return self._build_result(
            upper, lower, mv,
            "数字", str(number),
            month, bjt.year, bjt.month, bjt.day, bjt.hour
        )

    def _build_result(self, upper: int, lower: int, mv: int,
                      method: str, method_detail,
                      month: int, year: int, month2: int,
                      day: int, hour: int) -> Dict:
        ben_upper = TRIGRAMS[upper]
        ben_lower = TRIGRAMS[lower]
        hu_upper, hu_lower     = self._get_hugua(upper, lower)
        bian_upper, bian_lower = self._get_biangua(upper, lower, mv)

        if mv <= 3:
            body_elem     = ben_upper['element']
            use_elem      = ben_lower['element']
            body_gua_name = ben_upper['name']
            use_gua_name  = ben_lower['name']
        else:
            body_elem     = ben_lower['element']
            use_elem      = ben_upper['element']
            body_gua_name = ben_lower['name']
            use_gua_name  = ben_upper['name']

        relation, fortune = self._wuxing_relation(body_elem, use_elem)
        ganzhi = self._get_ganzhi(year, month2, day, hour)

        zhi_num  = {'子':1,'丑':2,'寅':3,'卯':4,'辰':5,'巳':6,
                    '午':7,'未':8,'申':9,'酉':10,'戌':11,'亥':12}
        hour_num = zhi_num.get(ganzhi['hour'][-1], hour + 1)
        yingqi   = upper + lower + hour_num

        return {
            'method': method, 'method_detail': method_detail,
            'month': ganzhi['month'][-1], 'year': year, 'month2': month2,
            'day': day, 'hour': hour,
            'ben':  {'upper': ben_upper, 'lower': ben_lower,
                     'mv': mv, 'gua': (upper, lower)},
            'hu':   {'upper': TRIGRAMS[hu_upper], 'lower': TRIGRAMS[hu_lower],
                     'gua': (hu_upper, hu_lower)},
            'bian': {'upper': TRIGRAMS[bian_upper], 'lower': TRIGRAMS[bian_lower],
                     'gua': (bian_upper, bian_lower)},
            'body_elem': body_elem,         'use_elem': use_elem,
            'body_gua_name': body_gua_name, 'use_gua_name': use_gua_name,
            'relation': relation,           'fortune': fortune,
            'ganzhi': ganzhi, 'yingqi': yingqi,
            'upper': upper, 'lower': lower, 'hour_num': hour_num,
        }

    def format_output(self, result: Dict, question: str = "") -> str:
        lines = []
        gz  = result['ganzhi']
        now = datetime.datetime.now()

        # ── 第1行：真实时间 ──
        lines.append(f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}")

        # ── 第2行：干支 ──
        lines.append(f"{gz['year']}年 {gz['month']}月 {gz['day']}日 {gz['hour']}时")

        # ── 第3行：五行旺衰（直接查表，木火土金水顺序）──
        month_state = WX_MONTH_STATE.get(result['month'], {})
        wx_status   = [f"{elem}{month_state[elem]}" for elem in ["木", "火", "土", "金", "水"]]
        lines.append("，".join(wx_status))

        # ── 第4行：起卦方式 ──
        method = result['method']
        detail = result['method_detail']
        lines.append(f"起卦方式：{method}（{detail}）" if detail else f"起卦方式：{method}")

        if question:
            lines.append(f"问：{question}")

        lines.append("")

        b  = result['ben']
        hu = result['hu']
        bi = result['bian']
        upper,  lower  = b['gua']
        hu_u,   hu_l   = hu['gua']
        bian_u, bian_l = bi['gua']

        # ── 主卦 ──
        ben_sym       = get_gua_symbol(upper, lower)
        ben_full_name = get_gua_full_name(upper, lower)
        ben_ci        = get_gua_ci(upper, lower)
        lines.append(f"[主卦] {ben_sym} {ben_full_name}（{result['relation']}）")
        lines.append(f"        「{ben_ci}」")

        # ── 互卦：互见XX（经卦卦名）──
        lines.append(f"[互卦] 互见{hu['upper']['name']}{hu['lower']['name']}")

        # ── 变卦 ──
        bian_sym       = get_gua_symbol(bian_u, bian_l)
        bian_full_name = get_gua_full_name(bian_u, bian_l)
        bian_ci        = get_gua_ci(bian_u, bian_l)
        # 变卦体用：动爻在下卦(mv≤3)则体=上卦用=下卦，动爻在上卦(mv≥4)则体=下卦用=上卦
        if b['mv'] <= 3:
            bian_rel, _ = self._wuxing_relation(bi['upper']['element'], bi['lower']['element'])
        else:
            bian_rel, _ = self._wuxing_relation(bi['lower']['element'], bi['upper']['element'])
        lines.append(f"[变卦] {bian_sym} {bian_full_name}（{bian_rel}）")
        lines.append(f"        「{bian_ci}」")

        # ── 动爻 ──
        mv        = b['mv']
        yao_label = ["初", "二", "三", "四", "五", "六"][mv - 1]
        yao_ci    = get_yao_ci(upper, lower, mv)
        lines.append(f"[动爻] {yao_label}爻动")
        lines.append(f"        「{yao_ci}」")

        return "\n".join(lines)


# ══════════════════════════════════════════════
#  入口
# ══════════════════════════════════════════════
if __name__ == '__main__':
    import sys
    pb  = PlumBlossom()
    bjt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        if cmd == 'time':
            question = sys.argv[2] if len(sys.argv) >= 3 else ""
            r = pb.time_divination(bjt.year, bjt.month, bjt.day, bjt.hour)
            print(pb.format_output(r, question))
        elif cmd == 'num' and len(sys.argv) >= 3:
            number   = int(sys.argv[2])
            question = sys.argv[3] if len(sys.argv) >= 4 else ""
            r = pb.number_divination(number)
            print(pb.format_output(r, question))
        else:
            r = pb.time_divination(now.year, now.month, now.day, now.hour)
            print(pb.format_output(r))
    else:
        r = pb.time_divination(now.year, now.month, now.day, now.hour)
        print(pb.format_output(r))
