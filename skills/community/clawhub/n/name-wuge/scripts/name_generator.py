"""
╔══════════════════════════════════════════════════════════╗
║         姓名/公司名批量生成器  v1.0                     ║
║                                                          ║
║  基于康熙字典笔画 + 81数理，反向枚举生成达标名字           ║
╚══════════════════════════════════════════════════════════╝
"""

from typing import Optional, List
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from name_wuge import to_simplified

# ──────────────────────────────────────────────
# § 1  精选常用汉字池（约 1200 字）
# 筛选：常见姓氏 + 常用名用字 + 商务常用字，剔除生僻字
# ──────────────────────────────────────────────

_COMMON_CHARS = (
    # 常用姓氏（200+）
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾居衡步都耿满弘空圃肖崃呦盍权稽闪问弋赏卑苟迈岩朴心耨铁列刀过校剧密恭肃施营退仇撩闾绪枚植其烦段鄂承赫弦"
    # 常用名字用字（精选，剔除生僻）
    "婷娟秀英华慧敏静丽芳兰玉萍红艳霞凤洁素云莲雪荣妹香雅菲蓉花佳蓉苹华晖嫒纨仪贞莉娣璧蘅芷妍玟萱怡惠桦羽雁露霜寒梦怡悦希安静娴映梦璇诗涵梓晴朗月阳星辰风昊天宇浩凯晨旭伟强勇军涛波祥瑞嘉树彬磊超文博志明轩志鹏海涛"
    "健柏树林川洋瀚清润诚玄辉飞翔波涛春雨夏月秋收冬藏"
    "博学笃行善思明辨至善唯诚创新卓越"
    # 商务常用公司名用字
    "华泰富盈腾达盛祥裕顺信义诚智捷恒昌聚德龙凤吉祥如意鹏程万里锦绣乾坤春晖星辉万象更新千秋伟业山河锦绣前程锦绣风华正茂"
)

_COMMON_SET = set(_COMMON_CHARS)

# 公司名专用优选字池（商务感强、非常用姓氏）
_COMPANY_CHARS = (
    "华泰富盈腾达盛祥裕顺信义诚智捷恒昌聚德龙凤吉祥如意鹏程万里锦绣乾坤春晖星辉万象更新千秋伟业山河锦绣前程风华正茂博学笃行善思明辨至善唯诚创新卓越"
    "华泰富盈腾达盛祥裕顺信义诚智捷恒昌聚德龙凤吉祥如意鹏程万里锦绣乾坤春晖星辉万象更新千秋伟业"
)
_COMPANY_SET = set(_COMPANY_CHARS)


def _build_stroke_pool(char_set: set) -> dict:
    """从字符集建立 笔画→[字列表] 的反向索引"""
    from .name_wuge import get_kangxi_strokes
    pool = {}
    for ch in char_set:
        s = get_kangxi_strokes(ch)
        if s is not None and s > 0:
            pool.setdefault(s, []).append(ch)
    return pool


def _is_ji(n: int) -> bool:
    """判断81数理某数是否"吉"（不含凶/凶带吉）"""
    from .name_wuge import get_81_info
    jx = get_81_info(n)["jixiong"]
    return "凶" not in jx


def _all_ji(tian: int, ren: int, di: int, wai: int, zong: int) -> bool:
    return all(_is_ji(x) for x in [tian, ren, di, wai, zong])


# ──────────────────────────────────────────────
# § 2  姓名批量生成
# ──────────────────────────────────────────────

def generate_names(
    surname: str,
    given_len: int = 2,
    require_all_ji: bool = True,
    target_ges: Optional[dict] = None,
    char_pool: Optional[set] = None,
    max_results: int = 50,
) -> List[dict]:
    """
    批量生成姓名

    args:
        surname:       姓氏，如 "石"
        given_len:     名字字数（1或2，默认2）
        require_all_ji: True=五格全吉，False=只过滤凶格
        target_ges:    可选，指定某格的目标值，如 {"人格": 15}
        char_pool:     枚举用字符集，默认用精选常用字池
        max_results:   最多返回多少个（默认50）
    """
    from .name_wuge import get_kangxi_strokes, get_81_info

    if char_pool is None:
        char_pool = _COMMON_SET

    s_strokes = []
    for ch in surname:
        s = get_kangxi_strokes(ch)
        if s is None:
            raise ValueError(f"姓氏中的字 '{ch}' 不在康熙字典中")
        s_strokes.append(s)

    s_len = len(s_strokes)
    pool = _build_stroke_pool(char_pool)
    results = []

    def calc_wuge(s_strokes, g1_s, g2_s=None):
        if s_len == 1:
            tian = s_strokes[0] + 1
            ren = s_strokes[0] + g1_s
            di = g1_s + 1 if g2_s is None else g1_s + g2_s
        else:
            tian = s_strokes[0] + s_strokes[1]
            ren = s_strokes[-1] + g1_s
            di = g1_s + 1 if g2_s is None else g1_s + g2_s
        wai = tian + di - ren
        zong = sum(s_strokes) + g1_s + (g2_s or 0)
        return tian, ren, di, wai, zong

    if given_len == 1:
        for g1_s, chars1 in pool.items():
            tian, ren, di, wai, zong = calc_wuge(s_strokes, g1_s)
            if require_all_ji and not _all_ji(tian, ren, di, wai, zong):
                continue
            if target_ges:
                ge_map = {"天格": tian, "人格": ren, "地格": di, "外格": wai, "总格": zong}
                if not all(ge_map.get(k) == v for k, v in target_ges.items()):
                    continue
            for c1 in chars1:
                name = surname + c1
                scores = [get_81_info(x)["score"] for x in [tian, ren, di, wai, zong]]
                results.append({
                    "name": name,
                    "tian": tian, "ren": ren, "di": di, "wai": wai, "zong": zong,
                    "overall_score": round(sum(scores) / len(scores), 1),
                })
    else:
        for g1_s, chars1 in pool.items():
            for g2_s, chars2 in pool.items():
                tian, ren, di, wai, zong = calc_wuge(s_strokes, g1_s, g2_s)
                if require_all_ji and not _all_ji(tian, ren, di, wai, zong):
                    continue
                if target_ges:
                    ge_map = {"天格": tian, "人格": ren, "地格": di, "外格": wai, "总格": zong}
                    if not all(ge_map.get(k) == v for k, v in target_ges.items()):
                        continue
                for c1 in chars1:
                    for c2 in chars2:
                        if c1 == c2:
                            continue  # 去重：两字名不能相同
                        name = surname + c1 + c2
                        scores = [get_81_info(x)["score"] for x in [tian, ren, di, wai, zong]]
                        results.append({
                            "name": name,
                            "tian": tian, "ren": ren, "di": di, "wai": wai, "zong": zong,
                            "overall_score": round(sum(scores) / len(scores), 1),
                        })

    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return results[:max_results]


# ──────────────────────────────────────────────
# § 3  公司名批量生成
# ──────────────────────────────────────────────

def generate_company(
    length: int,
    target_zong: int,
    char_pool: Optional[set] = None,
    max_results: int = 30,
) -> List[dict]:
    """
    批量生成公司名

    args:
        length:       公司名字数（2-6）
        target_zong:  目标总格数理（如 28）
        char_pool:    枚举用字符集
        max_results:  最多返回多少个
    """
    from .name_wuge import get_81_info

    if char_pool is None:
        char_pool = _COMPANY_SET

    pool = _build_stroke_pool(char_pool)
    results = []

    # 找所有笔画和=target_zong的组合
    stroke_combos = _find_stroke_combos(length, target_zong, pool)

    for combo in stroke_combos:
        char_lists = [pool.get(s, []) for s in combo]
        for chars in _cartesian(char_lists):
            name = "".join(chars)
            if len(set(name)) < len(name):
                continue  # 去掉重复字
            info = get_81_info(target_zong)
            results.append({
                "name": name,
                "zong": target_zong,
                "score": info["score"],
                "jixiong": info["jixiong"],
            })
            if len(results) >= max_results:
                break
        if len(results) >= max_results:
            break

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def _find_stroke_combos(length: int, target: int, pool: dict) -> list:
    """回溯找出一组笔画和=target的组合"""
    stroke_vals = sorted(set(pool.keys()))
    results = []
    max_val = max(stroke_vals) if stroke_vals else 30

    def backtrack(pos: int, remain: int, path: list):
        slots_left = length - pos
        if slots_left == 0:
            if remain == 0:
                results.append(list(path))
            return
        min_possible = sum(stroke_vals[:min(slots_left, 3)])
        max_possible = slots_left * max_val
        if remain < min_possible or remain > max_possible:
            return
        for s in stroke_vals:
            if s > remain:
                break
            path.append(s)
            backtrack(pos + 1, remain - s, path)
            path.pop()

    backtrack(0, target, [])
    return results


def _cartesian(lists: list) -> list:
    if not lists:
        return []
    result = [[]]
    for lst in lists:
        result = [x + [y] for x in result for y in lst]
    return result


# ──────────────────────────────────────────────
# § 4  格式化输出
# ──────────────────────────────────────────────

def _ji_short(n: int) -> str:
    from .name_wuge import get_81_info
    return get_81_info(n)["jixiong"]


def format_name_results(results: list, surname: str) -> str:
    from name_wuge import get_81_info
    if not results:
        return f"未找到满足条件的【{surname}+X】组合（字库中无匹配）"

    lines = [
        "-------------------------------------",
        f"  姓氏: {surname}  找到 {len(results)} 个候选（按总分排序）",
        "  (笔画以康熙繁体核算，名字已转简体输出)",
        "-------------------------------------",
    ]
    for r in results:
        t, rg, d, w, z = r["tian"], r["ren"], r["di"], r["wai"], r["zong"]
        jx_str = f"天{_ji_short(t)}人{_ji_short(rg)}地{_ji_short(d)}外{_ji_short(w)}总{_ji_short(z)}"
        # 输出繁简双版（繁体笔画→简体名字）
        name_simp = to_simplified(r["name"])
        name_display = f"{name_simp}（{r['name']}）"
        lines.append(
            f"  {name_display:<10}  天{t:>2}人{rg:>2}地{d:>2}外{w:>2}总{z:>2}  {jx_str}  {r['overall_score']}分"
        )
    lines.append("-------------------------------------")
    return "\n".join(lines)


def format_company_results(results: list, length: int, target_zong: int) -> str:
    from .name_wuge import get_81_info
    info = get_81_info(target_zong)
    if not results:
        return f"未找到 {length} 字、总格={target_zong}（{info['jixiong']}）的公司名组合"

    lines = [
        "-------------------------------------",
        f"  目标: {length}字  总格={target_zong}（{info['jixiong']}）{info['desc'][:12]}",
        f"  找到 {len(results)} 个候选（按评分排序）",
        "-------------------------------------",
    ]
    for r in results:
        lines.append(f"  {r['name']:<8}  总格={r['zong']}  {r['jixiong']}  {r['score']}分")
    lines.append("-------------------------------------")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# § 5  主入口
# ──────────────────────────────────────────────

def run_generate(
    surname: str = "",
    given_len: int = 2,
    require_all_ji: bool = True,
    target_ges: Optional[dict] = None,
    company_length: int = 0,
    company_target_zong: int = 0,
    max_results: int = 30,
) -> str:
    """
    批量生成统一入口

    姓名模式：
      run_generate(surname="石", given_len=2)
      run_generate(surname="石", target_ges={"人格": 15})

    公司名模式：
      run_generate(company_length=3, company_target_zong=28)
    """
    from .name_wuge import ensure_full_data
    ensure_full_data()

    if company_target_zong > 0:
        results = generate_company(
            length=company_length,
            target_zong=company_target_zong,
            max_results=max_results,
        )
        return format_company_results(results, company_length, company_target_zong)
    else:
        results = generate_names(
            surname=surname,
            given_len=given_len,
            require_all_ji=require_all_ji,
            target_ges=target_ges,
            max_results=max_results,
        )
        return format_name_results(results, surname)


def run_random_names(count: int = 10, given_len: int = 0, require_all_ji: bool = False, gender: str = "auto") -> str:
    """
    纯随机生成姓名：姓氏+名字都随机挑选

    args:
        count:          生成多少个（默认10）
        given_len:      名字字数，0=随机混合单双名（默认0）
        require_all_ji: True=五格全吉，False=只保总格为吉（默认False）
        gender:         "female"=女名池,"male"=男名池,"auto"=混合（默认auto）
    """
    from .name_wuge import ensure_full_data, get_81_info
    import random

    # 尝试导入 pypinyin，不强依赖
    try:
        from pypinyin import lazy_pinyin
        _HAS_PINYIN = True
    except ImportError:
        _HAS_PINYIN = False

    _FINALS = {'a','ai','an','ang','ao','e','ei','en','eng','er','i','ia','ian','iang','iao','ie','in','ing','iong','iu','o','ong','ou','u','ua','uai','uan','uang','ue','ui','un','uo','v','ve'}

    def _get_pinyin(ch):
        if not _HAS_PINYIN:
            return None
        try:
            return lazy_pinyin(ch)[0]
        except:
            return None

    def _parse_pinyin(py):
        if not py:
            return None, None
        py = py.lower().rstrip('1234')
        for ini in ['ch','sh','zh','th']:
            if py.startswith(ini):
                return ini, py[len(ini):]
        for i in range(min(3, len(py)), 0, -1):
            pre, post = py[:i], py[i:]
            if pre and pre not in ['a','e','i','o','u','v'] and post in _FINALS:
                return pre, post
        return None, py

    def _check_phonetic(name):
        """名字韵母不能全同才算好听"""
        chars = list(name)
        name_parts = chars[1:] if len(chars) > 1 else chars
        finals = []
        for c in name_parts:
            py = _get_pinyin(c)
            if py is None:
                return True  # 拿不到拼音就不过滤
            _, fin = _parse_pinyin(py)
            finals.append(fin)
        if len(set(finals)) < len(finals):
            return False
        return True

    ensure_full_data()

    # 根据性别选择名字用字池
    if gender == "female":
        char_pool = _FEMALE_SET
    elif gender == "male":
        char_pool = _MALE_SET
    else:
        char_pool = _FEMALE_SET  # auto默认女名池

    surnames = list(_SURNAME_POOL)
    random.shuffle(surnames)

    all_results = []
    used_names = set()  # 同名去重
    used_surnames = {}  # 跟踪每姓氏已用数量，控制多样性
    checked = 0
    max_check = count * 50
    max_per_surname = 3  # 每姓氏最多取3个，避免同一姓氏垄断

    if given_len == 0:
        given_lens = [1, 2]
    else:
        given_lens = [given_len]

    for sn in surnames:
        if checked >= max_check or len(all_results) >= count:
            break
        if used_surnames.get(sn, 0) >= max_per_surname:
            continue
        for gl in given_lens:
            if len(all_results) >= count:
                break
            if used_surnames.get(sn, 0) >= max_per_surname:
                break
            try:
                results = generate_names(
                    surname=sn,
                    given_len=gl,
                    require_all_ji=require_all_ji,
                    char_pool=char_pool,  # 传入性别专用字池
                    max_results=6,
                )
                random.shuffle(results)  # 打乱结果，真正随机
                for r in results:
                    if len(all_results) >= count:
                        break
                    if used_surnames.get(sn, 0) >= max_per_surname:
                        break
                    name = r['name']
                    if name in used_names:
                        continue
                    if not _check_phonetic(name):
                        continue
                    used_names.add(name)
                    used_surnames[sn] = used_surnames.get(sn, 0) + 1
                    all_results.append(r)
                    checked += 1
            except ValueError:
                continue

    if not all_results:
        mode_desc = "五格全吉" if require_all_ji else "总格为吉"
        return f"字库中未能凑出足够的{mode_desc}名字（已尝试 {checked} 次）"

    mode_desc = "五格全吉" if require_all_ji else "总格为吉"
    lines = [
        "-------------------------------------",
        f"  随机生成 {len(all_results)} 个姓名（{mode_desc}）",
        f"  （每次生成结果不同）",
        "-------------------------------------",
    ]
    for r in all_results:
        t, rg, d, w, z = r["tian"], r["ren"], r["di"], r["wai"], r["zong"]
        name = r['name']
        py_str = ' '.join(_get_pinyin(c) or '?' for c in name)
        jx_str = f"天{get_81_info(t)['jixiong']}人{get_81_info(rg)['jixiong']}地{get_81_info(d)['jixiong']}外{get_81_info(w)['jixiong']}总{get_81_info(z)['jixiong']}"
        lines.append(
            f"  {name:<6} {py_str:<20} 天{t:>2}人{rg:>2}地{d:>2}外{w:>2}总{z:>2}  {jx_str}  {r['overall_score']}分"
        )
    lines.append("-------------------------------------")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# § 6  常用姓氏池（用于随机生成）
# ──────────────────────────────────────────────

_SURNAME_POOL = (
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾居衡步都耿满弘空圃肖崃呦盍权稽闪问弋赏卑苟迈岩朴心耨铁列刀过校剧密恭肃施营退仇撩闾绪枚植其烦段鄂承赫弦"
)

# ──────────────────────────────────────────────
# § 7  女生姓名专用字池（2025流行+音韵好听）
# ──────────────────────────────────────────────

_FEMALE_CHARS = (
    # 2025流行女名用字（月曦/清窈/云笺/灵晞/星冉/婉柠/芊澄/芮熹/倩柔/乐涵/语诺/敏彤/可夏 等）
    "月曦清窈云笺灵晞星冉婉柠芊澄芮熹倩柔乐涵语诺敏彤可夏沁恬瑜玥珞芙蕾雅岚桐芸竹棠栩梓晴朵妤珝琛琳琅瑀珞珈珂珺琦璇璟璐琬琰沁蕾桐岚缃瑾璇瑾妤婉柠"
    # 经典柔美女名用字
    "婷娟秀英华慧敏静丽芳兰玉萍红艳霞凤洁素云莲雪荣妹香雅菲蓉花佳蓉苹晖嫒纨仪贞莉娣璧蘅芷妍玟萱怡惠羽雁露霜寒梦悦希安静娴映璇诗涵梓晴朗"
    # 珍贵美玉系（女孩名常见）
    "琳瑶琪瑾琦璇璟璐琬琰珂珂珺珩珞珈"
    # 植物芳草系
    "芷萱兰莲蓉蔷薇月桂棠桐楠榆柳棉槐樱枫杉杉"
    # 叠字亲昵系
    "婷婷娟娟丽丽瑶瑶璐璐琪琪琳琳"
)

_FEMALE_SET = set(_FEMALE_CHARS)

# ──────────────────────────────────────────────
# § 8  男生姓名专用字池
# ──────────────────────────────────────────────


_MALE_CHARS = (
    "伟强勇军涛波祥瑞嘉树彬磊超文博志明轩志鹏海涛"
    "健柏树林川洋瀚清润诚玄辉飞翔波涛春雨夏月秋收冬藏"
    "昊天宇浩凯晨旭伟强俊豪靖峰岳岩川泉海涛"
    "博学笃行善思明辨至善唯诚创新卓越"
)

_MALE_SET = set(_MALE_CHARS)
