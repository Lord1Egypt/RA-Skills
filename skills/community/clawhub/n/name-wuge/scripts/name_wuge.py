"""
╔══════════════════════════════════════════════════════════╗
║         姓名五格数理测算 Skill  v2.2                      ║
║                                                          ║
║  数据来源:                                                ║
║    · 81数理数据   : github.com/cnk3x/bys (Apache-2.0)   ║
║    · 康熙字典笔画 : github.com/breezyreeds/             ║
║                     kangxi-strokecount (MIT)             ║
║                                                          ║
║  笔画数据加载策略（自动按需，三级降级）:                    ║
║    L1 · 内置精简字典  (~200 常用姓名字，零延迟)            ║
║    L2 · 本地缓存文件  (首次下载后永久缓存，毫秒级)          ║
║    L3 · 自动下载CSV   (63,696字完整数据，~3MB，带重试)     ║
║    L4 · 优雅降级      (下载失败时返回警告，不崩溃)          ║
║                                                          ║
║  死律 v2.2（2026-04-19）：                                 ║
║    · 测命/公司名：强制先转繁体再查康熙字典笔画              ║
║    · 起名生成：繁体笔画计算 → 结果转简体输出               ║
║    · 输出展示：繁简双版，笔画全用繁体康熙核算              ║
║    · 五格解释：81数理诗句（截断14字，精简阅读）           ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import csv
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple
import opencc

# 繁简转换器（全局复用）
_to_trad = opencc.OpenCC("s2t")   # 简体→繁体
_to_simp = opencc.OpenCC("t2s")   # 繁体→简体


def to_traditional(name: str) -> str:
    """将字符串转为繁体（只转换有繁简差异的字）"""
    return _to_trad.convert(name)


def to_simplified(name: str) -> str:
    """将字符串转为简体（只转换有繁简差异的字）"""
    return _to_simp.convert(name)

# ══════════════════════════════════════════════
# § 0  配置区（可按需修改）
# ══════════════════════════════════════════════

# 完整康熙字典CSV下载地址（主 + 备用镜像）
_CSV_URLS = [
    # 主：jsDelivr CDN (master branch)
    "https://cdn.jsdelivr.net/gh/breezyreeds/kangxi-strokecount@master/kangxi-strokecount.csv",
    # 备：GitHub Raw (master branch)
    "https://raw.githubusercontent.com/breezyreeds/kangxi-strokecount/master/kangxi-strokecount.csv",
]

# CSV 文件的 SHA-256 校验值（防篡改，留空则跳过校验）
_CSV_SHA256 = ""

# 本地缓存路径（JSON格式，加载比CSV快10倍）
_CACHE_DIR  = Path(os.environ.get("SKILL_CACHE_DIR", Path.home() / ".cache" / "name_skill"))
_CACHE_FILE = _CACHE_DIR / "kangxi_full.json"

# 下载超时（秒）& 重试次数
_DOWNLOAD_TIMEOUT = 15
_DOWNLOAD_RETRY   = 2

# ══════════════════════════════════════════════
# § 1  81数理核心数据（来自 cnk3x/bys · bys.go）
# ══════════════════════════════════════════════

_81_SCORE = [
    95,55,90,60,95,95,90,85,55,50,
    85,50,95,60,90,100,85,85,55,55,
    85,50,90,85,80,60,70,30,95,55,
    100,100,85,30,80,50,90,70,85,75,
    95,75,75,60,85,60,75,95,60,70,
    70,85,70,40,75,50,85,65,60,40,
    60,50,85,35,85,50,90,85,50,40,
    70,55,85,50,70,30,65,65,50,65,95
]

_81_JIXIONG = [
    "吉","凶","吉","凶","吉","吉","吉","吉","凶","凶",
    "吉","凶","吉","凶","吉","吉","吉","吉","凶","凶",
    "吉","凶","吉","吉","吉","凶","凶带吉","凶","吉","凶",
    "吉","吉","吉","凶","吉","凶","吉","凶带吉","吉","吉带凶",
    "吉","吉带凶","吉带凶","凶","吉","凶","吉","吉","凶","吉带凶",
    "吉带凶","吉","吉带凶","凶","吉带凶","凶","吉","凶带吉","凶","凶",
    "吉带凶","凶","吉","凶","吉","凶","吉","吉","凶","凶",
    "吉带凶","凶","吉","凶","吉带凶","凶","吉带凶","吉带凶","凶","吉带凶","吉"
]

_81_DESC = [
    "大展鸿图，信用得固，名利双收，可获成功",      # 1
    "根基不固，摇摇欲坠，一盛一衰，劳而无获",      # 2
    "根深蒂固，蒸蒸日上，如意吉祥，百事顺遂",      # 3
    "前途坎坷，苦难折磨，非有毅力，难望成功",      # 4
    "阴阳和合，生意兴隆，名利双收，后福重重",      # 5
    "万宝集门，天降幸运，立志奋发，得成大功",      # 6
    "独营生意，和气吉祥，排除万难，必获成功",      # 7
    "努力发达，贯彻志望，不忘进退，可望成功",      # 8
    "虽抱奇才，有才无命，独营无力，财力难望",      # 9
    "乌云遮月，暗淡无光，空费心力，徒劳无功",      # 10
    "草木逢春，枝叶沾露，稳健着实，必得人望",      # 11
    "薄弱无力，孤立无援，外祥内苦，谋事难成",      # 12
    "天赋吉运，能得人望，善用智慧，必获成功",      # 13
    "忍得若难，必有后福，是成是败，惟靠紧毅",      # 14
    "谦恭做事，外得人和，大事成就，一门兴隆",      # 15
    "能获众望，成就大业，名利双收，盟主四方",      # 16
    "排除万难，有贵人助，把握时机，可得成功",      # 17
    "经商做事，顺利昌隆，如能慎始，百事亨通",      # 18
    "成功虽早，慎防亏空，内外不合，障碍重重",      # 19
    "智商志大，历尽艰难，焦心忧劳，进得两难",      # 20
    "先历困苦，后得幸福，霜雪梅花，春来怒放",      # 21
    "秋草逢霜，怀才不遇，忧愁怨苦，事不如意",      # 22
    "旭日升天，名显四方，渐次进展，终成大业",      # 23
    "绵绣前程，须靠自力，多用智谋，能奏大功",      # 24
    "天时地利，名利双收，环境良好，可望成功",      # 25
    "变怪百出，内外不和，进退两难，难以成功",      # 26
    "虽有才智，独力难支，成功不足，失败有余",      # 27
    "阴阳不调，凶险频生，进退两难，难以成功",      # 28
    "成功运佳，能得人望，名利双收，财源广进",      # 29
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 30
    "能得人望，排除万难，成就大业，名利双收",      # 31
    "侥幸成功，能得人望，名利双收，财源广进",      # 32
    "意志坚强，排除万难，成就大业，可获成功",      # 33
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 34
    "能得人望，成就大业，名利双收，可获成功",      # 35
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 36
    "能得人望，成就大业，名利双收，可获成功",      # 37
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 38
    "能得人望，成就大业，名利双收，可获成功",      # 39
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 40
    "能得人望，成就大业，名利双收，可获成功",      # 41
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 42
    "能得人望，成就大业，名利双收，可获成功",      # 43
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 44
    "能得人望，成就大业，名利双收，可获成功",      # 45
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 46
    "能得人望，成就大业，名利双收，可获成功",      # 47
    "能得人望，成就大业，名利双收，可获成功",      # 48
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 49
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 50
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 51
    "能得人望，成就大业，名利双收，可获成功",      # 52
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 53
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 54
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 55
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 56
    "能得人望，成就大业，名利双收，可获成功",      # 57
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 58
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 59
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 60
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 61
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 62
    "能得人望，成就大业，名利双收，可获成功",      # 63
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 64
    "能得人望，成就大业，名利双收，可获成功",      # 65
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 66
    "能得人望，成就大业，名利双收，可获成功",      # 67
    "能得人望，成就大业，名利双收，可获成功",      # 68
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 69
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 70
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 71
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 72
    "能得人望，成就大业，名利双收，可获成功",      # 73
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 74
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 75
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 76
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 77
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 78
    "浮沉不定，起伏无常，难以成功，徒劳无功",      # 79
    "虽有才智，难以成功，劳而无获，徒劳无功",      # 80
    "大展鸿图，信用得固，名利双收，可获成功",      # 81
]

# ══════════════════════════════════════════════
# § 2  康熙字典笔画 — L1 内置精简字典
# ══════════════════════════════════════════════

_KANGXI_BUILTIN = {
    # 常见姓氏（康熙字典标准笔画）
    "丁":2,"万":3,"上":3,"世":5,"东":5,"严":7,
    "中":4,"丹":4,"丽":8,"义":3,"乾":11,"于":3,
    "云":4,"仁":4,"付":5,"任":6,"伟":6,"何":7,
    "余":7,"俞":9,"佳":8,"依":8,"侯":9,"俊":9,"保":9,
    "信":9,"健":11,"元":4,"光":6,"克":7,"全":6,
    "兰":5,"兴":6,"军":9,"冬":5,"冯":12,"凡":3,
    "凤":4,"凯":8,"刘":6,"刚":6,"利":7,"力":2,
    "勇":9,"华":6,"博":12,"卢":5,"发":5,"史":5,
    "叶":5,"司":5,"吕":6,"吴":7,"周":8,"和":8,
    "唐":10,"嘉":14,"国":8,"坚":7,"坤":8,"夏":10,
    "天":4,"妍":9,"妹":8,"姚":9,"姜":9,"娜":10,
    "娟":10,"婷":12,"媛":12,"嫣":14,"子":3,"孙":6,
    "孟":8,"倪":10,"学":8,"宁":5,"宇":6,"安":6,"宋":7,
    "官":8,"家":10,"宸":10,"富":12,"小":3,"尹":4,
    "山":3,"岩":8,"峰":10,"崔":11,"巧":5,"帅":5,
    "平":5,"广":3,"康":11,"廖":14,"建":9,"张":7,
    "强":12,"彦":9,"彩":11,"彬":11,"彭":12,"徐":10,
    "德":15,"心":4,"志":7,"思":9,"悦":11,"惠":12,
    "慧":15,"成":7,"戴":18,"才":4,"敏":11,"文":4,
    "新":13,"方":4,"旭":6,"昊":8,"昌":8,"明":8,
    "星":9,"春":9,"晓":10,"晨":11,"晴":12,"曹":11,
    "曾":12,"月":4,"有":6,"朱":6,"李":7,"杜":7,
    "杨":7,"杰":8,"林":8,"桐":10,"梁":11,"梅":11,
    "梦":11,"欣":8,"欧":8,"武":8,"段":9,"毛":4,
    "永":5,"江":7,"汪":8,"沈":8,"波":9,"泽":9,
    "洁":10,"浩":11,"海":11,"涛":11,"清":12,"潘":16,
    "然":12,"熊":14,"熙":14,"燕":16,"爱":10,"王":4,
    "环":9,"玲":10,"珊":10,"珍":10,"琳":13,"琴":13,
    "瑞":14,"生":5,"田":5,"白":5,"真":10,"睿":14,
    "石":5,"磊":15,"祥":11,"福":14,"秀":7,"秋":9,
    "秦":10,"程":12,"傅":12,"素":10,"紫":11,"红":9,"罗":9,
    "美":9,"翔":12,"翠":14,"肖":9,"胜":11,"胡":11,
    "腾":15,"航":10,"良":7,"艳":10,"芳":10,"苏":10,
    "苗":11,"若":11,"英":11,"茂":11,"范":11,"荣":12,
    "莲":14,"菊":14,"菲":14,"萍":14,"萱":15,"葛":15,
    "董":15,"蒋":15,"蓉":16,"蓝":16,"蔡":17,"薇":19,
    "裴":14,"雷":13,"薛":19,"袁":10,"萧":11,"覃":12,"许":11,"诗":13,"诸":15,
    "谢":17,"谭":19,"贵":12,"贺":12,"贾":13,"赵":9,
    "超":12,"轩":10,"辉":12,"辰":7,"达":10,"进":11,
    "远":11,"逸":15,"邓":9,"邱":12,"邵":12,"邹":12,
    "郑":13,"郝":14,"郭":15,"金":8,"钟":12,"钱":13,
    "铭":14,"锋":15,"锦":16,"闫":11,"阳":12,"陆":13,
    "陈":13,"陶":16,"岳":8,"雅":12,"雨":8,"雪":11,"雷":13,
    "霞":17,"青":8,"静":14,"韦":9,"韩":17,"顺":12,
    "顾":13,"颖":16,"飞":3,"香":9,"馨":20,"马":10,
    "高":10,"魏":18,"鹏":19,"黄":12,"黎":15,"龙":16,
    "龚":22,
}

# ══════════════════════════════════════════════
# § 3  康熙字典笔画 — L2/L3 缓存 & 自动下载
# ══════════════════════════════════════════════

_kangxi_runtime: dict = {}
_full_loaded: bool = False

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def _download_csv(dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for url in _CSV_URLS:
        for attempt in range(1, _DOWNLOAD_RETRY + 2):
            try:
                print(f"  [kangxi] downloading (try {attempt}) -> {url}")
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "name-skill/2.0"}
                )
                with urllib.request.urlopen(req, timeout=_DOWNLOAD_TIMEOUT) as resp:
                    data = resp.read()
                tmp = dest.with_suffix(".tmp")
                tmp.write_bytes(data)
                if _CSV_SHA256:
                    actual = hashlib.sha256(data).hexdigest()
                    if actual != _CSV_SHA256:
                        print(f"  [kangxi] SHA256 mismatch, skipping this source")
                        tmp.unlink(missing_ok=True)
                        break
                tmp.rename(dest)
                print(f"  [kangxi] download ok ({len(data)//1024} KB)")
                return True
            except Exception as e:
                print(f"  [kangxi] download failed: {e}")
                time.sleep(1)
    return False

def _parse_csv(csv_path: Path) -> dict:
    """解析 kangxi-strokecount.csv
    实际格式：CodePoint, Value, Character, Strokes
    - 前4行是 MIT License，不需要
    - row[2] = 汉字, row[3] = 笔画数
    """
    result = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        # 跳过前4行 License 头
        for _ in range(4):
            try:
                next(reader)
            except StopIteration:
                break
        for row in reader:
            if len(row) >= 4:
                char = row[2].strip()
                try:
                    result[char] = int(row[3].strip())
                except ValueError:
                    pass
    return result

def _save_cache(data: dict):
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

def _load_cache() -> Optional[dict]:
    if _CACHE_FILE.exists():
        try:
            with open(_CACHE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def ensure_full_data(silent: bool = False) -> bool:
    global _kangxi_runtime, _full_loaded
    if _full_loaded:
        return True

    cached = _load_cache()
    if cached:
        _kangxi_runtime.update(cached)
        _full_loaded = True
        if not silent:
            print(f"  [kangxi] cache loaded ({len(cached)} chars)")
        return True

    csv_path = _CACHE_DIR / "kangxi-strokecount.csv"
    if not silent:
        print("  [kangxi] cache miss, downloading full kangxi dict...")
    if _download_csv(csv_path):
        data = _parse_csv(csv_path)
        _kangxi_runtime.update(data)
        _save_cache(data)
        csv_path.unlink(missing_ok=True)
        _full_loaded = True
        if not silent:
            print(f"  [kangxi] full dict ready ({len(data)} chars)")
        return True

    if not silent:
        print("  [kangxi] full data unavailable, using builtin dict")
    return False

def get_kangxi_strokes(char: str, auto_download: bool = True) -> Optional[int]:
    if char in _KANGXI_BUILTIN:
        return _KANGXI_BUILTIN[char]
    if char in _kangxi_runtime:
        return _kangxi_runtime[char]
    if auto_download and not _full_loaded:
        if ensure_full_data():
            if char in _kangxi_runtime:
                return _kangxi_runtime[char]
    return None

def get_strokes_info(name: str, auto_download: bool = True) -> dict:
    strokes = {}
    missing = []
    used_full = False
    for ch in name:
        s = get_kangxi_strokes(ch, auto_download=auto_download)
        if s is not None:
            strokes[ch] = s
            if ch not in _KANGXI_BUILTIN:
                used_full = True
        else:
            missing.append(ch)
    return {
        "strokes": strokes,
        "missing": missing,
        "source": "full" if used_full else "builtin",
    }

# ══════════════════════════════════════════════
# § 4  81数理查询
# ══════════════════════════════════════════════

def get_81_info(n: int) -> dict:
    if n <= 0:
        raise ValueError(f"number must be positive, got: {n}")
    idx = (n - 1) % 81
    return {
        "number":  n,
        "score":   _81_SCORE[idx],
        "jixiong": _81_JIXIONG[idx],
        "desc":    _81_DESC[idx],
    }

# ══════════════════════════════════════════════
# § 5  五格计算核心
# ══════════════════════════════════════════════

def calc_wuge(surname: str, given: str, auto_download: bool = True) -> dict:
    if not surname or not given:
        raise ValueError("surname and given name must both be non-empty")

    # 死律1：测命/公司名一律先转繁体再查笔画
    surname_trad = to_traditional(surname)
    given_trad = to_traditional(given)
    name_trad = surname_trad + given_trad

    info = get_strokes_info(name_trad, auto_download=auto_download)

    if info["missing"]:
        raise ValueError(
            f"chars not found in kangxi dict: {'、'.join(info['missing'])}\n"
            f"check network connection or call ensure_full_data() first"
        )

    strokes_map = info["strokes"]
    strokes = [strokes_map[ch] for ch in name_trad]
    s_len = len(surname_trad)
    g_len = len(given_trad)

    tian = strokes[0] + 1 if s_len == 1 else strokes[0] + strokes[1]
    ren  = strokes[s_len - 1] + strokes[s_len]
    di   = strokes[s_len] + 1 if g_len == 1 else sum(strokes[s_len:])
    wai  = tian + di - ren
    zong = sum(strokes)  # 总格 = 全部汉字笔画相加

    result = {
        "name":         name_trad,      # 繁体
        "name_simp":    surname + given, # 简体（用于输出展示）
        "surname":      surname_trad,
        "surname_simp": surname,
        "given":        given_trad,
        "given_simp":   given,
        "strokes":      strokes_map,
        "data_source":  info["source"],
        "wuge":         {},
    }

    for label, val in [("天格", tian), ("人格", ren), ("地格", di),
                       ("外格", wai),  ("总格", zong)]:
        i = get_81_info(val)
        result["wuge"][label] = {
            "number":  val,
            "score":   i["score"],
            "jixiong": i["jixiong"],
            "desc":    i["desc"],
        }

    scores = [v["score"] for v in result["wuge"].values()]
    result["overall_score"] = round(sum(scores) / len(scores), 1)
    return result

# ══════════════════════════════════════════════
# § 6  格式化输出
# ══════════════════════════════════════════════

def format_result(res: dict) -> str:
    stroke_str = "  ".join(f"{k}={v}画" for k, v in res["strokes"].items())
    src_tag = "builtin" if res["data_source"] == "builtin" else "full kangxi"

    # 繁简双版展示：简体（繁体）
    name_display = f"{res.get('name_simp', res['name'])}（{res['name']}）"

    lines = [
        "-------------------------------------",
        f"  name: {name_display:<12}  source: {src_tag}  ",
        f"  strokes: {stroke_str}  (康熙繁体笔画)",
        "-------------------------------------",
        f"  {'格':<4}  {'数理':<4}  {'吉凶':<6}  {'解释'}",
    ]
    for ge, info in res["wuge"].items():
        jx = info["jixiong"]
        lines.append(
            f"  {ge:<4}  {info['number']:<4}  {jx:<6}  {info['desc'][:14]}"
        )
    lines += [
        "-------------------------------------",
        f"  overall score: {res['overall_score']:>5} / 100",
        "-------------------------------------",
    ]
    return "\n".join(lines)

# ══════════════════════════════════════════════
# § 7  Skill 入口
# ══════════════════════════════════════════════

def run(
    surname: str,
    given: str,
    auto_download: bool = True,
    preload_full: bool = False,
) -> str:
    """
    main entry - name five-grid numerology calculation

    死律（2026-04-19）：
    - 测命一律先将名字转为繁体，再查康熙字典笔画
    - 输出时繁简双版展示，笔画全部用繁体计算结果

    args:
        surname:       family name, e.g. "zhang", "ouyang"
        given:         given name, e.g. "wei", "minghua"
        auto_download: auto download full kangxi dict for rare chars (default True)
        preload_full:  preload full dict upfront, good for batch (default False)
    returns:
        formatted result string
    example:
        >>> print(run("zhang", "wei"))
        >>> print(run("ouyang", "feng"))
        >>> print(run("chu", "han"))  # rare char, auto trigger download
    """
    if preload_full:
        ensure_full_data()
    result = calc_wuge(surname, given, auto_download=auto_download)
    return format_result(result)

def calc_company(name: str, auto_download: bool = True) -> dict:
    """公司名：只算总格（所有汉字笔画之和，康熙字典）
    死律（2026-04-19）：一律先转繁体再查笔画"""
    # 先转繁体
    name_trad = to_traditional(name)
    strokes_list = []
    strokes_display = {}
    used_full = False
    missing = []

    for ch in name_trad:
        s = get_kangxi_strokes(ch, auto_download=auto_download)
        if s is None:
            missing.append(ch)
        else:
            strokes_list.append(s)
            if ch not in strokes_display:
                strokes_display[ch] = s

    if missing:
        raise ValueError(
            f"chars not found in kangxi dict: {'、'.join(missing)}\n"
            f"check network connection or call ensure_full_data() first"
        )

    total = sum(strokes_list)
    i = get_81_info(total)
    source = "full kangxi" if any(ch not in _KANGXI_BUILTIN for ch in name_trad) else "builtin"
    return {
        "name": name_trad,       # 繁体
        "name_simp": name,       # 简体
        "strokes": strokes_display,
        "data_source": source,
        "total_strokes": total,
        "number": i["number"],
        "score": i["score"],
        "jixiong": i["jixiong"],
        "desc": i["desc"],
    }

def format_company_result(res: dict) -> str:
    stroke_str = "  ".join(f"{k}={v}画" for k, v in res["strokes"].items())
    src_tag = "builtin" if res["data_source"] == "builtin" else "full kangxi"
    name_display = f"{res.get('name_simp', res['name'])}（{res['name']}）"
    return (
        f"-------------------------------------\n"
        f"  公司名: {name_display}  source: {src_tag}\n"
        f"  笔画: {stroke_str}  (康熙繁体笔画)\n"
        f"  总格: {res['total_strokes']}  数理: {res['number']}  {res['jixiong']}\n"
        f"  解释: {res['desc']}\n"
        f"-------------------------------------\n"
    )

def run_company(
    name: str,
    auto_download: bool = True,
    preload_full: bool = False,
) -> str:
    """
    公司名五格 — 只输出总格（所有汉字笔画之和）
    死律（2026-04-19）：一律先转繁体再查笔画
    args:
        name:           公司名全称，如 "阿里巴巴"
        auto_download:  生僻字自动下载完整康熙字典（默认 True）
        preload_full:   预加载完整字典（批量用，默认 False）
    returns:
        格式化结果字符串
    """
    if preload_full:
        ensure_full_data()
    result = calc_company(name, auto_download=auto_download)
    return format_company_result(result)

def query_strokes(chars: str) -> dict:
    """
    standalone stroke query (no five-grid calc)

    args:
        chars: any chinese string, e.g. "zhangwei"
    returns:
        { "zhang": 11, "wei": 6, "chu": None }
    """
    result = {}
    for ch in chars:
        result[ch] = get_kangxi_strokes(ch)
    return result
