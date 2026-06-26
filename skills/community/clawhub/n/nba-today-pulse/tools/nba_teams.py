#!/usr/bin/env python3
"""Team alias helpers for NBA_TR."""

from __future__ import annotations

import re

ENGLISH_TEAM_ALIASES: dict[str, list[str]] = {
    "ATL": ["atl", "hawks", "atlanta", "atlanta hawks"],
    "BOS": ["bos", "celtics", "boston", "boston celtics"],
    "BKN": ["bkn", "nets", "brooklyn", "brooklyn nets"],
    "CHA": ["cha", "hornets", "charlotte", "charlotte hornets"],
    "CHI": ["chi", "bulls", "chicago", "chicago bulls"],
    "CLE": ["cle", "cavaliers", "cavs", "cleveland", "cleveland cavaliers"],
    "DAL": ["dal", "mavericks", "mavs", "dallas", "dallas mavericks"],
    "DEN": ["den", "nuggets", "denver", "denver nuggets"],
    "DET": ["det", "pistons", "detroit", "detroit pistons"],
    "GSW": ["gsw", "warriors", "golden state", "golden state warriors"],
    "HOU": ["hou", "rockets", "houston", "houston rockets"],
    "IND": ["ind", "pacers", "indiana", "indiana pacers"],
    "LAC": ["lac", "clippers", "la clippers", "los angeles clippers"],
    "LAL": ["lal", "lakers", "la lakers", "los angeles lakers"],
    "MEM": ["mem", "grizzlies", "memphis", "memphis grizzlies"],
    "MIA": ["mia", "heat", "miami", "miami heat"],
    "MIL": ["mil", "bucks", "milwaukee", "milwaukee bucks"],
    "MIN": ["min", "timberwolves", "wolves", "minnesota", "minnesota timberwolves"],
    "NOP": ["nop", "pelicans", "new orleans", "new orleans pelicans"],
    "NYK": ["nyk", "knicks", "new york", "new york knicks"],
    "OKC": ["okc", "thunder", "oklahoma city", "oklahoma city thunder"],
    "ORL": ["orl", "magic", "orlando", "orlando magic"],
    "PHI": ["phi", "76ers", "sixers", "philadelphia", "philadelphia 76ers"],
    "PHX": ["phx", "suns", "phoenix", "phoenix suns"],
    "POR": ["por", "trail blazers", "blazers", "portland", "portland trail blazers"],
    "SAC": ["sac", "kings", "sacramento", "sacramento kings"],
    "SAS": ["sas", "spurs", "san antonio", "san antonio spurs"],
    "TOR": ["tor", "raptors", "toronto", "toronto raptors"],
    "UTA": ["uta", "jazz", "utah", "utah jazz"],
    "WAS": ["was", "wsh", "wizards", "washington", "washington wizards"],
}

TEAM_DISPLAY = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "LA Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards",
}

TEAM_DISPLAY_ZH_CN = {
    "ATL": "亚特兰大老鹰",
    "BOS": "波士顿凯尔特人",
    "BKN": "布鲁克林篮网",
    "CHA": "夏洛特黄蜂",
    "CHI": "芝加哥公牛",
    "CLE": "克利夫兰骑士",
    "DAL": "达拉斯独行侠",
    "DEN": "丹佛掘金",
    "DET": "底特律活塞",
    "GSW": "金州勇士",
    "HOU": "休斯顿火箭",
    "IND": "印第安纳步行者",
    "LAC": "洛杉矶快船",
    "LAL": "洛杉矶湖人",
    "MEM": "孟菲斯灰熊",
    "MIA": "迈阿密热火",
    "MIL": "密尔沃基雄鹿",
    "MIN": "明尼苏达森林狼",
    "NOP": "新奥尔良鹈鹕",
    "NYK": "纽约尼克斯",
    "OKC": "俄克拉荷马城雷霆",
    "ORL": "奥兰多魔术",
    "PHI": "费城76人",
    "PHX": "菲尼克斯太阳",
    "POR": "波特兰开拓者",
    "SAC": "萨克拉门托国王",
    "SAS": "圣安东尼奥马刺",
    "TOR": "多伦多猛龙",
    "UTA": "犹他爵士",
    "WAS": "华盛顿奇才",
}

TEAM_DISPLAY_ZH_HK = {
    "ATL": "亞特蘭大鷹隊",
    "BOS": "波士頓塞爾特人",
    "BKN": "布魯克林籃網",
    "CHA": "夏洛特黃蜂",
    "CHI": "芝加哥公牛",
    "CLE": "克里夫蘭騎士",
    "DAL": "達拉斯獨行俠",
    "DEN": "丹佛金塊",
    "DET": "底特律活塞",
    "GSW": "金州勇士",
    "HOU": "休斯頓火箭",
    "IND": "印第安納溜馬",
    "LAC": "洛杉磯快艇",
    "LAL": "洛杉磯湖人",
    "MEM": "孟菲斯灰熊",
    "MIA": "邁阿密熱火",
    "MIL": "密爾沃基公鹿",
    "MIN": "明尼蘇達木狼",
    "NOP": "新奧爾良鵜鶘",
    "NYK": "紐約人",
    "OKC": "奧克拉荷馬城雷霆",
    "ORL": "奧蘭多魔術",
    "PHI": "費城76人",
    "PHX": "鳳凰城太陽",
    "POR": "波特蘭拓荒者",
    "SAC": "沙加緬度帝王",
    "SAS": "聖安東尼奧馬刺",
    "TOR": "多倫多速龍",
    "UTA": "猶他爵士",
    "WAS": "華盛頓巫師",
}

TEAM_DISPLAY_ZH_TW = {
    "ATL": "亞特蘭大老鷹",
    "BOS": "波士頓塞爾提克",
    "BKN": "布魯克林籃網",
    "CHA": "夏洛特黃蜂",
    "CHI": "芝加哥公牛",
    "CLE": "克里夫蘭騎士",
    "DAL": "達拉斯獨行俠",
    "DEN": "丹佛金塊",
    "DET": "底特律活塞",
    "GSW": "金州勇士",
    "HOU": "休士頓火箭",
    "IND": "印第安那溜馬",
    "LAC": "洛杉磯快艇",
    "LAL": "洛杉磯湖人",
    "MEM": "曼菲斯灰熊",
    "MIA": "邁阿密熱火",
    "MIL": "密爾瓦基公鹿",
    "MIN": "明尼蘇達灰狼",
    "NOP": "紐奧良鵜鶘",
    "NYK": "紐約尼克",
    "OKC": "奧克拉荷馬城雷霆",
    "ORL": "奧蘭多魔術",
    "PHI": "費城76人",
    "PHX": "鳳凰城太陽",
    "POR": "波特蘭拓荒者",
    "SAC": "沙加緬度國王",
    "SAS": "聖安東尼奧馬刺",
    "TOR": "多倫多暴龍",
    "UTA": "猶他爵士",
    "WAS": "華盛頓巫師",
}

TEAM_SHORT_ALIASES_ZH = {
    "ATL": ["老鹰", "老鷹", "鹰队", "鷹隊"],
    "BOS": ["凯尔特人", "凱爾特人", "塞尔提克", "塞爾提克", "塞尔特人", "塞爾特人"],
    "BKN": ["篮网", "籃網"],
    "CHA": ["黄蜂", "黃蜂"],
    "CHI": ["公牛"],
    "CLE": ["骑士", "騎士"],
    "DAL": ["独行侠", "獨行俠", "小牛"],
    "DEN": ["掘金", "金塊"],
    "DET": ["活塞"],
    "GSW": ["勇士"],
    "HOU": ["火箭"],
    "IND": ["步行者", "溜馬"],
    "LAC": ["快船", "快艇"],
    "LAL": ["湖人"],
    "MEM": ["灰熊"],
    "MIA": ["热火", "熱火"],
    "MIL": ["雄鹿", "公鹿"],
    "MIN": ["森林狼", "灰狼", "木狼"],
    "NOP": ["鹈鹕", "鵜鶘"],
    "NYK": ["尼克斯", "尼克", "紐約人"],
    "OKC": ["雷霆"],
    "ORL": ["魔术", "魔術"],
    "PHI": ["76人"],
    "PHX": ["太阳", "太陽"],
    "POR": ["开拓者", "開拓者", "拓荒者"],
    "SAC": ["国王", "國王", "帝王"],
    "SAS": ["马刺", "馬刺"],
    "TOR": ["猛龙", "猛龍", "暴龍", "速龍"],
    "UTA": ["爵士"],
    "WAS": ["奇才", "華盛頓奇才", "巫师", "巫師"],
}

ZH_LOCALE_PATTERN_MAP = {
    "cn": ["大陆", "大陸", "内地", "內地", "简中", "簡中", "简体", "簡體", "中国大陆", "中國大陸"],
    "hk": ["香港", "港版", "港區", "港区", "繁中香港", "繁體香港", "港式"],
    "tw": ["台湾", "台灣", "台版", "台區", "台区", "繁中台灣", "繁體台灣", "台式"],
}

PROVIDER_ABBR_MAP = {
    "GS": "GSW",
    "SA": "SAS",
    "NO": "NOP",
    "NY": "NYK",
    "UTAH": "UTA",
    "WSH": "WAS",
}

ESPN_TEAM_IDS = {
    "ATL": "1",
    "BOS": "2",
    "BKN": "17",
    "CHA": "30",
    "CHI": "4",
    "CLE": "5",
    "DAL": "6",
    "DEN": "7",
    "DET": "8",
    "GSW": "9",
    "HOU": "10",
    "IND": "11",
    "LAC": "12",
    "LAL": "13",
    "MEM": "29",
    "MIA": "14",
    "MIL": "15",
    "MIN": "16",
    "NOP": "3",
    "NYK": "18",
    "OKC": "25",
    "ORL": "19",
    "PHI": "20",
    "PHX": "21",
    "POR": "22",
    "SAC": "23",
    "SAS": "24",
    "TOR": "28",
    "UTA": "26",
    "WAS": "27",
}

NBA_TEAM_IDS = {
    "ATL": "1610612737",
    "BOS": "1610612738",
    "BKN": "1610612751",
    "CHA": "1610612766",
    "CHI": "1610612741",
    "CLE": "1610612739",
    "DAL": "1610612742",
    "DEN": "1610612743",
    "DET": "1610612765",
    "GSW": "1610612744",
    "HOU": "1610612745",
    "IND": "1610612754",
    "LAC": "1610612746",
    "LAL": "1610612747",
    "MEM": "1610612763",
    "MIA": "1610612748",
    "MIL": "1610612749",
    "MIN": "1610612750",
    "NOP": "1610612740",
    "NYK": "1610612752",
    "OKC": "1610612760",
    "ORL": "1610612753",
    "PHI": "1610612755",
    "PHX": "1610612756",
    "POR": "1610612757",
    "SAC": "1610612758",
    "SAS": "1610612759",
    "TOR": "1610612761",
    "UTA": "1610612762",
    "WAS": "1610612764",
}


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _build_team_aliases() -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    for abbr in TEAM_DISPLAY:
        merged: list[str] = []
        seen: set[str] = set()
        for candidate in (
            ENGLISH_TEAM_ALIASES.get(abbr, [])
            + TEAM_SHORT_ALIASES_ZH.get(abbr, [])
            + [
                TEAM_DISPLAY_ZH_CN.get(abbr, ""),
                TEAM_DISPLAY_ZH_HK.get(abbr, ""),
                TEAM_DISPLAY_ZH_TW.get(abbr, ""),
            ]
        ):
            normalized = _normalize(candidate)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            merged.append(normalized)
        aliases[abbr] = merged
    return aliases


TEAM_ALIASES = _build_team_aliases()

_SORTED_ALIASES = sorted(
    ((alias, abbr) for abbr, aliases in TEAM_ALIASES.items() for alias in aliases),
    key=lambda item: len(item[0]),
    reverse=True,
)


def normalize_zh_locale(value: str | None) -> str | None:
    normalized = _normalize(value)
    if not normalized:
        return None
    if normalized in {"cn", "zh-cn", "zh_cn", "mainland", "simplified"}:
        return "cn"
    if normalized in {"hk", "zh-hk", "zh_hk", "hong kong", "hongkong"}:
        return "hk"
    if normalized in {"tw", "zh-tw", "zh_tw", "taiwan"}:
        return "tw"
    return None


def detect_zh_locale(text: str | None) -> str | None:
    normalized = _normalize(text)
    if not normalized:
        return None
    for locale, hints in ZH_LOCALE_PATTERN_MAP.items():
        for hint in hints:
            if _normalize(hint) in normalized:
                return locale
    return None


def infer_zh_locale(*, lang: str, tz_name: str | None = None, command_text: str | None = None, explicit_zh_locale: str | None = None) -> str | None:
    if lang != "zh":
        return None
    hinted = detect_zh_locale(command_text)
    if hinted:
        return hinted
    explicit = normalize_zh_locale(explicit_zh_locale)
    if explicit:
        return explicit
    tz_normalized = str(tz_name or "")
    if tz_normalized == "Asia/Hong_Kong":
        return "hk"
    if tz_normalized == "Asia/Taipei":
        return "tw"
    return "cn"


def normalize_team_input(value: str | None) -> str | None:
    if not value:
        return None
    normalized = _normalize(value)
    upper_value = canonicalize_team_abbr(value.strip())
    if upper_value in TEAM_ALIASES:
        return upper_value
    for alias, abbr in _SORTED_ALIASES:
        if normalized == alias:
            return abbr
    return None


def extract_team_from_text(text: str | None) -> str | None:
    teams = extract_teams_from_text(text)
    return teams[0] if teams else None


def _alias_pattern(alias: str) -> str:
    if re.fullmatch(r"[a-z0-9 .'-]+", alias):
        return rf"(?<![a-z]){re.escape(alias)}(?![a-z])"
    return re.escape(alias)


def extract_teams_from_text(text: str | None) -> list[str]:
    normalized_text = _normalize(text or "")
    matches_by_team: dict[str, tuple[int, int, str]] = {}
    for alias, abbr in _SORTED_ALIASES:
        pattern = _alias_pattern(alias)
        for match in re.finditer(pattern, normalized_text):
            candidate = (match.start(), -(match.end() - match.start()), abbr)
            current = matches_by_team.get(abbr)
            if current is None or candidate[:2] < current[:2]:
                matches_by_team[abbr] = candidate
    ordered = sorted(matches_by_team.values())
    return [abbr for _, _, abbr in ordered]


def canonicalize_team_abbr(value: str | None) -> str:
    normalized = (value or "").strip().upper()
    return PROVIDER_ABBR_MAP.get(normalized, normalized)


def provider_team_id(abbr: str | None, provider: str) -> str | None:
    canonical = canonicalize_team_abbr(abbr)
    if provider == "espn":
        return ESPN_TEAM_IDS.get(canonical)
    if provider == "nba":
        return NBA_TEAM_IDS.get(canonical)
    return None


def team_display_name(abbr: str | None, lang: str = "en", zh_locale: str | None = None) -> str:
    canonical = canonicalize_team_abbr(abbr)
    if lang == "zh":
        locale = normalize_zh_locale(zh_locale) or "cn"
        if locale == "hk":
            return TEAM_DISPLAY_ZH_HK.get(canonical, canonical or "")
        if locale == "tw":
            return TEAM_DISPLAY_ZH_TW.get(canonical, canonical or "")
        return TEAM_DISPLAY_ZH_CN.get(canonical, canonical or "")
    return TEAM_DISPLAY.get(canonical, canonical or "")


def format_matchup_display(
    away_abbr: str | None,
    home_abbr: str | None,
    *,
    lang: str = "en",
    zh_locale: str | None = None,
    away_score: object | None = None,
    home_score: object | None = None,
) -> str:
    away = team_display_name(away_abbr, lang, zh_locale=zh_locale) or "AWAY"
    home = team_display_name(home_abbr, lang, zh_locale=zh_locale) or "HOME"
    if away_score is not None or home_score is not None:
        return f"{away} {away_score if away_score is not None else ''} @ {home} {home_score if home_score is not None else ''}".strip()
    return f"{away} @ {home}"
