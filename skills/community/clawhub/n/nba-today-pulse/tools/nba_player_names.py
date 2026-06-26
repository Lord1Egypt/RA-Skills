#!/usr/bin/env python3
"""Controlled player-name identity and localization helpers for NBA_TR."""

from __future__ import annotations

import re

PLAYER_DISPLAY_ZH = {
    "Alperen Sengun": "阿尔佩伦·申京",
    "Anthony Davis": "安东尼·戴维斯",
    "Anthony Edwards": "安东尼·爱德华兹",
    "Austin Reaves": "Austin Reaves",
    "Ausar Thompson": "奥萨尔·汤普森",
    "Brandin Podziemski": "Brandin Podziemski",
    "Brandon Miller": "布兰登·米勒",
    "Cade Cunningham": "凯德·坎宁安",
    "De'Aaron Fox": "达龙·福克斯",
    "DeMar DeRozan": "德玛尔·德罗赞",
    "Devin Vassell": "德文·瓦塞尔",
    "Domantas Sabonis": "多曼塔斯·萨博尼斯",
    "Donte DiVincenzo": "唐特·迪文琴佐",
    "Draymond Green": "德雷蒙德·格林",
    "Duncan Robinson": "邓肯·罗宾逊",
    "Fred VanVleet": "Fred VanVleet",
    "Giannis Antetokounmpo": "扬尼斯·阿德托昆博",
    "James Harden": "詹姆斯·哈登",
    "Jalen Brunson": "杰伦·布伦森",
    "Jalen Duren": "杰伦·杜伦",
    "Jaxson Hayes": "Jaxson Hayes",
    "Jaylen Brown": "杰伦·布朗",
    "Jayson Tatum": "杰森·塔图姆",
    "Jimmy Butler III": "Jimmy Butler III",
    "Joel Embiid": "乔尔·恩比德",
    "Julius Randle": "朱利叶斯·兰德尔",
    "Kawhi Leonard": "科怀·伦纳德",
    "Karl-Anthony Towns": "卡尔-安东尼·唐斯",
    "Kevin Durant": "凯文·杜兰特",
    "Kyrie Irving": "凯里·欧文",
    "LaMelo Ball": "拉梅洛·鲍尔",
    "LeBron James": "勒布朗·詹姆斯",
    "Luka Doncic": "卢卡·东契奇",
    "Damian Lillard": "达米安·利拉德",
    "Devin Booker": "德文·布克",
    "Donovan Mitchell": "多诺万·米切尔",
    "Malik Monk": "马利克·蒙克",
    "Mark Williams": "马克·威廉姆斯",
    "Miles Bridges": "迈尔斯·布里奇斯",
    "Mike Conley": "迈克·康利",
    "Nikola Jokic": "尼古拉·约基奇",
    "Moses Moody": "Moses Moody",
    "OG Anunoby": "OG·阿奴诺比",
    "Paul George": "保罗·乔治",
    "Rudy Gobert": "鲁迪·戈贝尔",
    "Rui Hachimura": "Rui Hachimura",
    "Shai Gilgeous-Alexander": "谢伊·吉尔杰斯-亚历山大",
    "Stephen Curry": "斯蒂芬·库里",
    "Stephon Castle": "斯蒂芬·卡斯尔",
    "Tobias Harris": "托拜厄斯·哈里斯",
    "Trae Young": "特雷·杨",
    "Tyrese Haliburton": "泰瑞斯·哈利伯顿",
    "Tyrese Maxey": "泰瑞斯·马克西",
    "Victor Wembanyama": "维克托·文班亚马",
    "Zion Williamson": "蔡恩·威廉森",
}

PLAYER_ALIAS_VARIANTS = {
    "Alperen Sengun": ["申京", "阿尔佩伦申京", "a. sengun", "sengun"],
    "Anthony Davis": ["安东尼戴维斯", "浓眉", "ad", "a. davis"],
    "Anthony Edwards": ["爱德华兹", "安东尼爱德华兹", "ant", "a. edwards"],
    "Austin Reaves": ["里夫斯", "a. reaves"],
    "Ausar Thompson": ["奥萨尔", "奥萨尔汤普森", "a. thompson"],
    "Brandin Podziemski": ["podziemski", "b. podziemski"],
    "Cade Cunningham": ["坎宁安", "凯德", "凯德坎宁安", "c. cunningham"],
    "De'Aaron Fox": ["福克斯", "达龙", "deaaron fox", "d. fox"],
    "DeMar DeRozan": ["德罗赞", "德玛尔德罗赞", "d. derozan"],
    "Devin Vassell": ["瓦塞尔", "德文瓦塞尔", "d. vassell"],
    "Domantas Sabonis": ["小萨", "萨博尼斯", "多曼塔斯萨博尼斯", "d. sabonis"],
    "Draymond Green": ["追梦", "追梦格林", "d. green"],
    "Duncan Robinson": ["邓罗", "d. robinson"],
    "Fred VanVleet": ["范弗利特", "fred", "f. vanvleet"],
    "Giannis Antetokounmpo": ["字母哥", "扬尼斯", "阿德托昆博", "giannis", "g. antetokounmpo"],
    "James Harden": ["哈登", "james harden", "j. harden"],
    "Jalen Brunson": ["布伦森", "杰伦布伦森", "j. brunson"],
    "Jalen Duren": ["杜伦", "杰伦杜伦", "j. duren"],
    "Jaxson Hayes": ["海斯", "j. hayes"],
    "Jaylen Brown": ["杰伦布朗", "j. brown"],
    "Jayson Tatum": ["塔图姆", "杰森塔图姆", "jt", "j. tatum"],
    "Jimmy Butler III": ["巴特勒", "吉米巴特勒", "jimmy butler", "j. butler"],
    "Joel Embiid": ["恩比德", "大帝", "joel embiid", "j. embiid"],
    "Karl-Anthony Towns": ["唐斯", "卡尔安东尼唐斯", "kat", "k. towns"],
    "Kawhi Leonard": ["伦纳德", "小卡", "kawhi", "k. leonard"],
    "Kevin Durant": ["杜兰特", "kd", "k. durant"],
    "Kyrie Irving": ["欧文", "凯里欧文", "kyrie", "k. irving"],
    "LaMelo Ball": ["拉梅洛", "拉梅洛鲍尔", "lamelo", "l. ball"],
    "LeBron James": ["勒布朗", "勒布朗詹姆斯", "lbj", "lebron", "l. james"],
    "Luka Doncic": ["东契奇", "卢卡", "卢卡东契奇", "luka", "l. doncic"],
    "Damian Lillard": ["利拉德", "表哥", "damian", "dame", "d. lillard"],
    "Devin Booker": ["布克", "德文布克", "booker", "d. booker"],
    "Donovan Mitchell": ["米切尔", "多诺万米切尔", "spida", "d. mitchell"],
    "Malik Monk": ["蒙克", "m. monk"],
    "Mark Williams": ["马克威廉姆斯", "m. williams"],
    "Miles Bridges": ["布里奇斯", "迈尔斯布里奇斯", "m. bridges"],
    "Mike Conley": ["康利", "m. conley"],
    "Nikola Jokic": ["约基奇", "尼古拉约基奇", "joker", "jokic", "n. jokic"],
    "OG Anunoby": ["阿奴诺比", "anunoby", "o.g. anunoby"],
    "Rudy Gobert": ["戈贝尔", "gobert", "r. gobert"],
    "Rui Hachimura": ["八村塁", "rui", "r. hachimura"],
    "Shai Gilgeous-Alexander": ["亚历山大", "谢伊", "谢伊亚历山大", "sga", "shai", "s. gilgeous-alexander"],
    "Stephen Curry": ["库里", "斯蒂芬库里", "steph", "steph curry", "s. curry"],
    "Stephon Castle": ["卡斯尔", "斯蒂芬卡斯尔", "s. castle"],
    "Tobias Harris": ["哈里斯", "托拜厄斯哈里斯", "t. harris"],
    "Trae Young": ["特雷杨", "吹杨", "trae", "t. young"],
    "Tyrese Haliburton": ["哈利伯顿", "泰瑞斯哈利伯顿", "haliburton", "t. haliburton"],
    "Victor Wembanyama": ["文班", "文班亚马", "维克托文班亚马", "wemby", "wembanyama"],
    "Zion Williamson": ["锡安", "蔡恩", "蔡恩威廉森", "zion", "z. williamson"],
}

PLAYER_SEPARATORS = (" - ", " | ", " (", ": ")


def _normalize_alias_key(value: str | None) -> str:
    text = str(value or "").strip().casefold()
    text = text.replace("’", "'").replace("·", "")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[.'-]", "", text)
    return text


def _alias_pattern(alias: str) -> str:
    if re.fullmatch(r"[a-z0-9 .'-]+", alias):
        return rf"(?<![a-z]){re.escape(alias)}(?![a-z])"
    return re.escape(alias)


def _build_alias_map() -> tuple[dict[str, str], list[tuple[re.Pattern[str], str]]]:
    alias_map: dict[str, str] = {}
    patterns: list[tuple[re.Pattern[str], str]] = []
    for canonical, zh_display in PLAYER_DISPLAY_ZH.items():
        aliases = [canonical, zh_display, *PLAYER_ALIAS_VARIANTS.get(canonical, [])]
        seen: set[str] = set()
        for alias in aliases:
            normalized = _normalize_alias_key(alias)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            alias_map[normalized] = canonical
        for alias in sorted({alias for alias in aliases if str(alias or "").strip()}, key=len, reverse=True):
            patterns.append((re.compile(_alias_pattern(alias), flags=re.IGNORECASE), canonical))
    patterns.sort(key=lambda item: len(item[0].pattern), reverse=True)
    return alias_map, patterns


PLAYER_ALIAS_TO_CANONICAL, PLAYER_ALIAS_PATTERNS = _build_alias_map()


def extract_primary_player_name(text: str | None) -> str:
    value = str(text or "").strip()
    for separator in PLAYER_SEPARATORS:
        if separator in value:
            return value.split(separator, 1)[0].strip()
    return value


def resolve_player_alias_to_canonical(name: str | None) -> str | None:
    primary = extract_primary_player_name(name)
    if not primary:
        return None
    return PLAYER_ALIAS_TO_CANONICAL.get(_normalize_alias_key(primary))


def normalize_player_identity(name: str | None) -> str:
    canonical = resolve_player_alias_to_canonical(name)
    return _normalize_alias_key(canonical or extract_primary_player_name(name))


def extract_player_mentions_from_text(text: str | None, *, limit: int = 4) -> list[str]:
    raw = str(text or "")
    mentions: list[str] = []
    for pattern, canonical in PLAYER_ALIAS_PATTERNS:
        if pattern.search(raw) and canonical not in mentions:
            mentions.append(canonical)
        if len(mentions) >= limit:
            break
    return mentions


def display_player_name(name: str | None, lang: str = "en") -> str:
    if not name:
        return ""
    canonical = resolve_player_alias_to_canonical(name)
    text = canonical or str(name).strip()
    if lang != "zh":
        return text
    return PLAYER_DISPLAY_ZH.get(text, text)


def localize_player_list(names: list[str] | None, lang: str = "en") -> list[str]:
    return [display_player_name(name, lang) for name in (names or [])]


def localize_player_line(text: str | None, lang: str = "en") -> str:
    if not text:
        return ""
    raw = str(text)
    split_at = len(raw)
    for token in PLAYER_SEPARATORS:
        position = raw.find(token)
        if position > 0:
            split_at = min(split_at, position)
    name = raw[:split_at].strip()
    localized = display_player_name(name, lang)
    if not localized:
        return raw
    if localized == name:
        canonical = resolve_player_alias_to_canonical(name)
        if lang != "zh" and canonical and canonical != name:
            return f"{canonical}{raw[split_at:]}"
        return raw
    return f"{localized}{raw[split_at:]}"
