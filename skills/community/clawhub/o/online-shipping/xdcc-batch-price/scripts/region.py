#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
region.py — 省市区解析与规范化（快递运费试算前置模块）

作用：把用户口语化的地址输入解析成小递查查接口要求的**规范省市区全称**。

支持的输入形态（发件/收件都一样）：
  "广东省深圳市南山区"        —— 连写
  "广东省 深圳市 南山区"      —— 空格分隔
  "广东,深圳,南山"            —— 逗号分隔（中英文逗号/顿号/斜杠/竖线/分号均可）
  "深圳南山"                  —— 省略省份，自动反查
  "北京朝阳"                  —— 直辖市，自动补市/区
  "东莞南城"                  —— 直筒子市（镇街道级区域）
  "广东省深圳市南山区科技园路1号" —— 尾部多余内容自动识别为详细地址

设计取舍：
  · 基础数据来自 xdccy.com 官方页面同款城市库（/dist/js/city.json.js），
    已精简为纯名称三层结构随包分发（scripts/regions.json），运行时**零网络依赖**；
  · 匹配采用「精确 → 去行政后缀比对 → 前缀 → 包含 → 模糊」五级降级，
    尽量让客户少输字也能命中，命不中时给出候选而不是直接报错中断；
  · 区级缺失时按 "市辖区 → 首个区" 兜底并显式告警，绝不静默猜错。
"""

import difflib
import json
import os
import re

REGIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regions.json")
CACHE_FILE = os.path.expanduser("~/.workbuddy/xdcc-regions.json")
SOURCE_URL = "https://xdccy.com/dist/js/city.json.js?v=12"

# 行政后缀（越长越优先剥离）。用于把「深圳市」还原为「深圳」做核心名比对。
_ADMIN_SUFFIX_RE = re.compile(
    # 「新区/开发区/工业区」必须排在单字「区」之前，否则「浦东新区」会被剥成「浦东新」，
    # 导致用户写「上海浦东」时匹配不上（实测踩过）。
    r"(维吾尔自治区|壮族自治区|回族自治区|特别行政区|自治区|自治州|"
    r"新区|开发区|工业区|地区|盟|省|市|区|县|旗)$"
)
# 分隔符：空格、逗号、顿号、斜杠、竖线、分号、制表符
_DELIM_RE = re.compile(r"[\s,，、/\\|;；\t]+")

# 区级缺失时的兜底优先名
_FALLBACK_AREA_NAMES = ("市辖区", "城区", "市中心区")


class RegionError(ValueError):
    """地址解析失败。suggestions 用于给客户返回「你是不是想找…」。"""

    def __init__(self, message, suggestions=None):
        super().__init__(message)
        self.suggestions = suggestions or []


def _core(name):
    """去掉行政后缀取核心名：'深圳市' -> '深圳'，'内蒙古自治区' -> '内蒙古'。"""
    if not name:
        return ""
    prev = None
    cur = name
    # 最多剥两层，避免把「市辖区」剥成空串之类
    for _ in range(2):
        prev = cur
        cur = _ADMIN_SUFFIX_RE.sub("", cur)
        if cur == prev or not cur:
            break
    return cur or name


# --------------------------------------------------------------------------- #
# 数据加载
# --------------------------------------------------------------------------- #
def load_regions(path=None):
    """加载省市区数据。优先随包 regions.json，其次本地缓存。"""
    for p in (path, REGIONS_FILE, CACHE_FILE):
        if p and os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and data.get("provinces"):
                    return data
            except (OSError, ValueError):
                continue
    raise RegionError(
        "省市区基础数据不可用（未找到 scripts/regions.json，也没有本地缓存）。"
    )


def refresh_regions(path=None):
    """从官方页面同款城市库重新拉取并缓存（GBK 编码的 `var province = [...]`）。

    仅在网络可用且需要更新数据时调用；日常查询走随包数据，不依赖网络。
    """
    import urllib.request

    dst = path or CACHE_FILE
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("gb18030", errors="replace")
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        raise RegionError("城市库格式异常，未找到 JSON 数组。")
    data = json.loads(text[start:end + 1])
    provinces = [
        {
            "name": p["name"],
            "cities": [
                {"name": c["name"], "areas": [a["name"] for a in c.get("areaList", [])]}
                for c in p.get("cityList", [])
            ],
        }
        for p in data
    ]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump({"source": SOURCE_URL, "provinces": provinces}, f,
                  ensure_ascii=False, separators=(",", ":"))
    return {"source": SOURCE_URL, "provinces": provinces}


# --------------------------------------------------------------------------- #
# 匹配
# --------------------------------------------------------------------------- #
def _match_one(query, candidates):
    """在候选名里匹配一个。返回规范名或 None。

    降级顺序：精确 → 核心名相等 → 候选以查询开头 → 候选包含查询 → 模糊(0.6)。
    """
    if not query or not candidates:
        return None
    q = query.strip()
    if not q:
        return None
    if q in candidates:
        return q
    qc = _core(q)
    for c in candidates:
        if _core(c) == qc:
            return c
    pre = [c for c in candidates if c.startswith(q) or (qc and c.startswith(qc))]
    if pre:
        return min(pre, key=len)
    sub = [c for c in candidates if q in c or (qc and qc in c)]
    if sub:
        return min(sub, key=len)
    close = difflib.get_close_matches(q, candidates, n=1, cutoff=0.6)
    return close[0] if close else None


def _suggest(text, pool, n=5):
    """给出最相近的候选名，用于报错时引导客户。"""
    if not text or not pool:
        return []
    hits = difflib.get_close_matches(text, pool, n=n, cutoff=0.4)
    if not hits:
        hits = [c for c in pool if text and text in c][:n]
    return hits


def _best_prefix(names, text):
    """在 text 开头做最长匹配。

    返回 (规范名, 已消费字符数, 匹配类型)。匹配类型：
      2 = text 以该名的全称或核心名开头（强匹配，可放心截断）
      1 = 该名以 text 开头（弱匹配，输入只是名字的前缀）
    无匹配返回 None。
    """
    best = None
    for n in names:
        c = _core(n)
        if text.startswith(n):
            cand = (n, len(n), 2)
        elif c and text.startswith(c):
            cand = (n, len(c), 2)
        elif n.startswith(text) or (c and c.startswith(text)):
            cand = (n, len(n), 1)
        else:
            continue
        if best is None:
            best = cand
            continue
        # 先比匹配类型；同类型下，强匹配取更长（吃得更准），弱匹配取更短（更保守）
        if cand[2] > best[2]:
            best = cand
        elif cand[2] == best[2]:
            if cand[2] == 2 and cand[1] > best[1]:
                best = cand
            elif cand[2] == 1 and cand[1] < best[1]:
                best = cand
    return best


class RegionDB:
    """省市区索引：province -> city -> area 三级查询。"""

    def __init__(self, data=None):
        data = data or load_regions()
        self.provinces = data.get("provinces", [])
        self.province_names = [p["name"] for p in self.provinces]
        self._cities = {}   # province -> [city names]
        self._areas = {}    # (province, city) -> [area names]
        self._city_parent = {}
        self._area_parent = {}
        for p in self.provinces:
            pn = p["name"]
            cn = [c["name"] for c in p.get("cities", [])]
            self._cities[pn] = cn
            for c in p.get("cities", []):
                self._city_parent[c["name"]] = pn
                key = (pn, c["name"])
                an = [a for a in c.get("areas", [])]
                self._areas[key] = an
                for a in an:
                    self._area_parent[(pn, c["name"], a)] = key
        self._prov_aliases = self._build_province_aliases()

    def _build_province_aliases(self):
        """省份可接受前缀表：[(前缀, 规范省名), ...]。

        常见中文省份简称基本等于「去掉行政后缀」后的核心名（广东/浙江/新疆…），
        但有一类例外：自治区名去掉后缀后仍是三字，口语会再缩一次——
        「内蒙古」常说成「内蒙」。这里为核心名长度 >= 3 的省份补一个两字简称，
        且仅在全省范围内唯一时才启用（「内蒙」只有内蒙古一家，安全）。
        """
        short_owners = {}
        for p in self.province_names:
            c = _core(p)
            if len(c) >= 3:
                short_owners.setdefault(c[:2], []).append(p)

        items = []
        for p in self.province_names:
            c = _core(p)
            items.append((p, p))            # 全称：广东省
            if c != p:
                items.append((c, p))        # 核心名：广东
            short = c[:2] if len(c) >= 3 else ""
            if short and short != c and len(short_owners.get(short, [])) == 1:
                items.append((short, p))    # 两字简称：内蒙
        return items

    # ---- 基础查询 ----
    def cities(self, province):
        return self._cities.get(province, [])

    def areas(self, province, city):
        return self._areas.get((province, city), [])

    def all_city_names(self):
        return list(self._city_parent.keys())

    def resolve_province(self, query):
        return _match_one(query, self.province_names)

    def match_province_prefix(self, text):
        """在 text 开头匹配省份，返回 (规范省名, 已消费字符数) 或 None。

        比通用前缀匹配多支持一类：核心名的**两字简称**（如「内蒙」→ 内蒙古自治区）。
        连写场景（「内蒙呼和浩特」）必须靠这个才能识别——只比全称和核心名会漏。
        简称只在全局唯一时才启用，避免歧义。
        """
        best = None
        for prefix, name in self._prov_aliases:
            if text.startswith(prefix):
                if best is None or len(prefix) > best[1]:
                    best = (name, len(prefix))
        return best

    def resolve_city(self, query, province=None):
        pool = self.cities(province) if province else self.all_city_names()
        hit = _match_one(query, pool)
        if hit and province:
            return hit
        if hit and not province:
            return hit, self._city_parent.get(hit)
        return None

    def resolve_area(self, query, province, city):
        return _match_one(query, self.areas(province, city))

    def parent_of_city(self, city):
        return self._city_parent.get(city)


# --------------------------------------------------------------------------- #
# 解析入口
# --------------------------------------------------------------------------- #
def resolve(text, db=None):
    """解析一段地址为规范的 省/市/区（+ 详细地址）。

    返回 dict：
      {"province", "city", "area", "address", "warnings": [...]}

    无法解析出省份/城市时抛 RegionError（带 suggestions）。
    """
    db = db or RegionDB()
    warnings = []
    raw = (text or "").strip()
    if not raw:
        raise RegionError("地址为空，请提供「省 市 区」，例如：广东 深圳 南山。")

    tokens = [t for t in _DELIM_RE.split(raw) if t]
    province = city = area = None
    address = ""

    # ---- 路径 A：已明确切成三段（及以上），逐段匹配，多余部分当详细地址 ----
    if len(tokens) >= 3:
        p = db.resolve_province(tokens[0])
        c = db.resolve_city(tokens[1], p) if p else None
        a = db.resolve_area(tokens[2], p, c) if (p and c) else None
        if p and c and a:
            province, city, area = p, c, a
            address = "".join(tokens[3:])

    # ---- 路径 B：连写/缺段，按「省→市→区」贪心最长匹配 ----
    if not (province and city and area):
        s = "".join(tokens)
        rest = s
        pm = db.match_province_prefix(rest)
        if pm:
            province, consumed = pm
            rest = rest[consumed:]
        else:
            # 省份没写：先按城市反查
            cm = _best_prefix(db.all_city_names(), rest)
            if cm:
                city, consumed, _ = cm
                province = db.parent_of_city(city)
                rest = rest[consumed:]
            else:
                raise RegionError(
                    f"无法识别「{raw}」所属省市。",
                    _suggest(s[:4], db.province_names, 5)
                    or db.province_names[:5],
                )

        if not city:
            cm = _best_prefix(db.cities(province), rest)
            if cm:
                city, consumed, _ = cm
                rest = rest[consumed:]
            elif len(db.cities(province)) == 1:
                # 直辖市：只有「北京市」这类唯一城市
                city = db.cities(province)[0]
            else:
                # 城市没写：用区名反查城市
                found = None
                for cn in db.cities(province):
                    am = _best_prefix(db.areas(province, cn), rest)
                    if am:
                        found = (cn, am[0], am[1])
                        break
                if found:
                    city, area, consumed = found[0], found[1], found[2]
                    rest = rest[consumed:]
                else:
                    raise RegionError(
                        f"无法识别「{raw}」所属城市。",
                        _suggest(rest[:4], db.cities(province), 5),
                    )

        if not area:
            am = _best_prefix(db.areas(province, city), rest) if rest else None
            if am:
                area, consumed, _ = am
                rest = rest[consumed:]
            elif rest:
                # 剩下的更像详细地址，区级按兜底补
                area = _fallback_area(db, province, city)
                if area:
                    warnings.append(
                        f"未识别到区县，已按「{area}」兜底估算；"
                        f"「{rest}」当作详细地址。如需精确报价请补上区县。"
                    )
                address = rest
            else:
                area = _fallback_area(db, province, city)
                if area:
                    warnings.append(f"未提供区县，已按「{area}」兜底估算。")

        address = address or rest

    if not area:
        area = _fallback_area(db, province, city)
        if area:
            warnings.append(f"未提供区县，已按「{area}」兜底估算。")
    if not area:
        raise RegionError(
            f"「{province}{city}」下没有可用的区县数据，无法估算运费。",
            _suggest("", db.cities(province), 5),
        )

    return {
        "province": province,
        "city": city,
        "area": area,
        "address": address.strip(),
        "warnings": warnings,
    }


def _fallback_area(db, province, city):
    """区级兜底：优先「市辖区」等通用名，否则取第一个区。"""
    areas = db.areas(province, city)
    if not areas:
        return None
    for fav in _FALLBACK_AREA_NAMES:
        if fav in areas:
            return fav
    return areas[0]


def fmt_region(r):
    """格式化为可读的「省 市 区」。"""
    return f"{r['province']} {r['city']} {r['area']}"


if __name__ == "__main__":
    import sys

    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass

    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("用法: python region.py <地址文本> [...]")
        print("示例: python region.py 广东深圳南山  \"浙江省,杭州市,西湖区\"  北京朝阳")
        sys.exit(0)
    if args[0] == "--refresh":
        refresh_regions()
        print("已刷新缓存:", CACHE_FILE)
        sys.exit(0)

    _db = RegionDB()
    for a in args:
        try:
            r = resolve(a, _db)
            print(f"{a}  ->  {fmt_region(r)}" + (f"   详细地址: {r['address']}" if r["address"] else ""))
            for w in r["warnings"]:
                print("     ⚠️", w)
        except RegionError as e:
            print(f"{a}  ->  ❌ {e}")
            if e.suggestions:
                print("     候选:", " / ".join(e.suggestions))
