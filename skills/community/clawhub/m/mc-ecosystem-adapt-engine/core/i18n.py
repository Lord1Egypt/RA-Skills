"""国际化模块 (i18n)

支持 11 种语言：简体中文、繁体中文、英文、日语、韩语、俄语、
西班牙语、意大利语、希腊语、泰语、印地语。

三级语言检测降级策略：
    1. IP 地理定位（优先）- 通过公开 API 查询设备所在国家/地区
    2. 系统 Locale 检测 - 读取操作系统的默认语言设置
    3. 英文（默认）- 以上均失败时回退到英文

用法：
    from core.i18n import t, set_language, get_current_language, init_language
    # 启动时自动检测位置并选择语言
    init_language(auto_detect=True)
    # 手动切换
    set_language("zh_cn")
    print(t("banner.title"))
"""

import json
import os
import sys
import time
import locale as sys_locale
from pathlib import Path
from typing import Optional, Tuple

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# 语言文件目录
_LOCALES_DIR = _PROJECT_ROOT / "locales"

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    "zh_cn": "简体中文",
    "zh_tw": "繁體中文",
    "en_us": "English",
    "ja_jp": "日本語",
    "ko_kr": "한국어",
    "ru_ru": "Русский",
    "es_es": "Español",
    "it_it": "Italiano",
    "el_gr": "Ελληνικά",
    "th_th": "ภาษาไทย",
    "hi_in": "हिन्दी",
    "ar_sa": "العربية",
}

# 默认语言（fallback）— 英文为主语言
_DEFAULT_LANGUAGE = "en_us"

# 当前语言
_current_language = _DEFAULT_LANGUAGE

# 翻译缓存：{lang_code: {key: value}}
_translations: dict = {}

# fallback 翻译（英文）
_fallback_translations: dict = {}

# ============================================================================
# 国家/地区 → 语言代码 映射表
# ISO 3166-1 alpha-2 国家代码 → 我们支持的语言代码
# ============================================================================
_COUNTRY_TO_LANG = {
    # 中文区
    "CN": "zh_cn",  # 中国
    "HK": "zh_tw",  # 香港
    "MO": "zh_tw",  # 澳门
    "TW": "zh_tw",  # 台湾
    "SG": "zh_cn",  # 新加坡（多数用简体中文）
    # 日语区
    "JP": "ja_jp",  # 日本
    # 韩语区
    "KR": "ko_kr",  # 韩国
    "KP": "ko_kr",  # 朝鲜
    # 俄语区
    "RU": "ru_ru",  # 俄罗斯
    "BY": "ru_ru",  # 白俄罗斯
    "KZ": "ru_ru",  # 哈萨克斯坦
    "UA": "ru_ru",  # 乌克兰（俄语仍广泛使用）
    # 西班牙语区
    "ES": "es_es",  # 西班牙
    "MX": "es_es",  # 墨西哥
    "AR": "es_es",  # 阿根廷
    "CL": "es_es",  # 智利
    "CO": "es_es",  # 哥伦比亚
    "PE": "es_es",  # 秘鲁
    "VE": "es_es",  # 委内瑞拉
    "EC": "es_es",  # 厄瓜多尔
    "GT": "es_es",  # 危地马拉
    "CU": "es_es",  # 古巴
    "BO": "es_es",  # 玻利维亚
    "DO": "es_es",  # 多米尼加
    "HN": "es_es",  # 洪都拉斯
    "PA": "es_es",  # 巴拿马
    "UY": "es_es",  # 乌拉圭
    "PR": "es_es",  # 波多黎各
    "CR": "es_es",  # 哥斯达黎加
    "PY": "es_es",  # 巴拉圭
    "SV": "es_es",  # 萨尔瓦多
    "NI": "es_es",  # 尼加拉瓜
    # 意大利语区
    "IT": "it_it",  # 意大利
    "VA": "it_it",  # 梵蒂冈
    "SM": "it_it",  # 圣马力诺
    "CH": "it_it",  # 瑞士（意语区之一， fallback 到意语）
    # 希腊语区
    "GR": "el_gr",  # 希腊
    "CY": "el_gr",  # 塞浦路斯
    # 泰语区
    "TH": "th_th",  # 泰国
    # 印地语区
    "IN": "hi_in",  # 印度
    "NP": "hi_in",  # 尼泊尔（印地语可通）
    # 英语区（其他国家默认英文，不列全）
    # 以下列表仅标注部分主要英语国家作为显式映射
    "US": "en_us",  # 美国
    "GB": "en_us",  # 英国
    "CA": "en_us",  # 加拿大
    "AU": "en_us",  # 澳大利亚
    "NZ": "en_us",  # 新西兰
    "IE": "en_us",  # 爱尔兰
    "ZA": "en_us",  # 南非
    "PH": "en_us",  # 菲律宾
    "MY": "en_us",  # 马来西亚
    "ID": "en_us",  # 印度尼西亚（fallback英文）
    "BR": "en_us",  # 巴西（暂不支持葡语，fallback英文）
    "FR": "en_us",  # 法国（暂不支持法语，fallback英文）
    "DE": "en_us",  # 德国（暂不支持德语，fallback英文）
    "PT": "en_us",  # 葡萄牙
    "NL": "en_us",  # 荷兰
    "BE": "en_us",  # 比利时
    "AT": "en_us",  # 奥地利
    "SE": "en_us",  # 瑞典
    "NO": "en_us",  # 挪威
    "DK": "en_us",  # 丹麦
    "FI": "en_us",  # 芬兰
    "PL": "en_us",  # 波兰
    "CZ": "en_us",  # 捷克
    "SK": "en_us",  # 斯洛伐克
    "HU": "en_us",  # 匈牙利
    "RO": "en_us",  # 罗马尼亚
    "BG": "en_us",  # 保加利亚
    "HR": "en_us",  # 克罗地亚
    "RS": "en_us",  # 塞尔维亚
    "TR": "en_us",  # 土耳其
    # 阿拉伯语区（通用阿拉伯语）
    "SA": "ar_sa",  # 沙特阿拉伯
    "AE": "ar_sa",  # 阿联酋
    "EG": "ar_sa",  # 埃及
    "QA": "ar_sa",  # 卡塔尔
    "KW": "ar_sa",  # 科威特
    "BH": "ar_sa",  # 巴林
    "OM": "ar_sa",  # 阿曼
    "YE": "ar_sa",  # 也门
    "SY": "ar_sa",  # 叙利亚
    "JO": "ar_sa",  # 约旦
    "LB": "ar_sa",  # 黎巴嫩
    "IQ": "ar_sa",  # 伊拉克
    "SD": "ar_sa",  # 苏丹
    "MA": "ar_sa",  # 摩洛哥
    "TN": "ar_sa",  # 突尼斯
    "DZ": "ar_sa",  # 阿尔及利亚
    "LY": "ar_sa",  # 利比亚
    "MR": "ar_sa",  # 毛里塔尼亚
    "IL": "en_us",  # 以色列
    "NG": "en_us",  # 尼日利亚
    "KE": "en_us",  # 肯尼亚
    "PK": "en_us",  # 巴基斯坦
    "BD": "en_us",  # 孟加拉国
    "VN": "en_us",  # 越南
}

# ============================================================================
# IP 地理定位 API 列表（按优先级排序，前一个失败自动尝试下一个）
# 每个 API 都返回国家代码字段，我们统一提取为 ISO 3166-1 alpha-2
# ============================================================================
_IP_GEO_APIS = [
    # 免费、无需注册、支持中文
    {
        "url": "http://ip-api.com/json/?fields=status,countryCode,country,regionName,city",
        "timeout": 5,
        "parse": lambda r: (r.get("countryCode") or "").upper()
            if r.get("status") == "success" else "",
    },
    # 免费、全球覆盖
    {
        "url": "https://ipinfo.io/json",
        "timeout": 5,
        "parse": lambda r: (r.get("country") or "").upper(),
    },
    # 免费、无速率限制
    {
        "url": "https://api.myip.com",
        "timeout": 5,
        "parse": lambda r: (r.get("cc") or "").upper(),
    },
    # 备选：免费 JSON API
    {
        "url": "https://freegeoip.app/json/",
        "timeout": 8,
        "parse": lambda r: (r.get("country_code") or r.get("countryCode") or "").upper(),
    },
]

# IP 定位结果缓存（避免重复请求）
_ip_geo_cache: dict = {
    "country_code": None,
    "country_name": None,
    "timestamp": 0,
    "lang_detected": None,
}
_IP_CACHE_TTL = 86400  # 缓存有效期：24 小时（秒）


def _load_language_file(lang_code: str) -> dict:
    """加载指定语言的 JSON 翻译文件"""
    file_path = _LOCALES_DIR / f"{lang_code}.json"
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _country_to_language(country_code: str) -> Optional[str]:
    """根据 ISO 国家代码映射到支持的语言代码

    参数:
        country_code: ISO 3166-1 alpha-2 两位国家代码（大写），如 "CN", "JP", "KR"

    返回:
        对应的语言代码，如 "zh_cn"；若未映射则返回 None
    """
    if not country_code:
        return None
    cc = country_code.upper().strip()
    return _COUNTRY_TO_LANG.get(cc)


def _detect_ip_geolocation() -> Tuple[Optional[str], Optional[str]]:
    """通过公开 IP 地理定位 API 查询设备所在国家

    使用多级 API 容错机制：依次尝试 ip-api.com → ipinfo.io →
    api.myip.com → freegeoip.app，任一成功即返回。

    返回:
        (country_code, country_name) 元组，均为 None 表示全部失败
        country_code 为 ISO 3166-1 alpha-2 大写两位代码
    """
    # 先看缓存
    now = time.time()
    if (_ip_geo_cache["country_code"] is not None
            and now - _ip_geo_cache["timestamp"] < _IP_CACHE_TTL):
        return (_ip_geo_cache["country_code"], _ip_geo_cache["country_name"])

    # 尝试导入 requests
    try:
        import requests
    except ImportError:
        return (None, None)

    last_country_name = None
    for api_cfg in _IP_GEO_APIS:
        try:
            resp = requests.get(
                api_cfg["url"],
                timeout=api_cfg.get("timeout", 5),
                headers={
                    "User-Agent": "MC-Skill-V1/1.0 (i18n geo detection)",
                    "Accept": "application/json",
                },
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            cc = api_cfg["parse"](data)
            if not cc or len(cc) != 2:
                continue
            # 提取国家名（不同 API 字段名不同）
            for name_key in ("country", "country_name", "Country"):
                if data.get(name_key):
                    last_country_name = data[name_key]
                    break
            # 更新缓存
            _ip_geo_cache["country_code"] = cc
            _ip_geo_cache["country_name"] = last_country_name
            _ip_geo_cache["timestamp"] = now
            # 同时写入磁盘缓存，下次启动无需再请求
            _persist_ip_cache(cc, last_country_name)
            return (cc, last_country_name)
        except Exception:
            continue

    # 所有 API 失败，尝试读取磁盘缓存
    cached = _load_persisted_ip_cache()
    if cached and cached["country_code"]:
        _ip_geo_cache.update(cached)
        return (cached["country_code"], cached.get("country_name"))

    return (None, None)


def _persist_ip_cache(country_code: str, country_name: Optional[str]) -> None:
    """将 IP 定位结果持久化到磁盘缓存文件"""
    cache_file = _PROJECT_ROOT / "data" / "ip_geo_cache.json"
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "country_code": country_code,
                "country_name": country_name,
                "timestamp": int(time.time()),
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_persisted_ip_cache() -> Optional[dict]:
    """从磁盘加载 IP 定位缓存，若过期或不存在返回 None"""
    cache_file = _PROJECT_ROOT / "data" / "ip_geo_cache.json"
    if not cache_file.exists():
        return None
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cached = json.load(f)
        ts = cached.get("timestamp", 0)
        if time.time() - ts < _IP_CACHE_TTL * 7:  # 磁盘缓存保留 7 天
            return cached
    except Exception:
        pass
    return None


def _detect_language_by_ip() -> Optional[str]:
    """基于 IP 地理定位检测语言

    返回:
        检测到的语言代码（如 "zh_cn"），无法检测则返回 None
    """
    try:
        cc, _cn = _detect_ip_geolocation()
        if cc:
            lang = _country_to_language(cc)
            if lang and lang in SUPPORTED_LANGUAGES:
                _ip_geo_cache["lang_detected"] = lang
                return lang
    except Exception:
        pass
    return None


def _detect_system_language() -> str:
    """检测系统语言，返回最接近的支持语言代码"""
    try:
        loc = sys_locale.getdefaultlocale()[0] or ""
        loc = loc.lower().replace("-", "_")
        # 精确匹配
        if loc in SUPPORTED_LANGUAGES:
            return loc
        # 模糊匹配（语言部分）
        lang_part = loc.split("_")[0]
        for code in SUPPORTED_LANGUAGES:
            if code.startswith(lang_part):
                return code
    except Exception:
        pass
    # 默认回退到英文
    return _DEFAULT_LANGUAGE


def set_language(lang_code: str) -> bool:
    """设置当前语言

    参数:
        lang_code: 语言代码，如 "zh_cn", "en_us", "ja_jp" 等

    返回:
        True 如果语言加载成功，False 如果回退到默认语言
    """
    global _current_language, _translations, _fallback_translations

    # 加载 fallback（英文）
    if not _fallback_translations:
        _fallback_translations = _load_language_file(_DEFAULT_LANGUAGE)

    # 加载目标语言
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = _DEFAULT_LANGUAGE

    if lang_code == _DEFAULT_LANGUAGE:
        _translations = _fallback_translations.copy()
        _current_language = lang_code
        return True

    _translations = _load_language_file(lang_code)
    _current_language = lang_code
    return len(_translations) > 0


def t(key: str, **kwargs) -> str:
    """翻译函数

    参数:
        key: 翻译键，如 "banner.title"
        **kwargs: 模板变量，如 t("welcome", name="Steve") 替换 {name}

    返回:
        翻译后的字符串，如果 key 不存在则返回 key 本身
    """
    # 先从当前语言查找
    text = _translations.get(key)
    # 回退到英文（主语言）
    if text is None:
        text = _fallback_translations.get(key)
    # 都没有，返回 key
    if text is None:
        return key

    # 模板变量替换
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass

    return text


def get_current_language() -> str:
    """获取当前语言代码"""
    return _current_language


def get_language_name(lang_code: str = None) -> str:
    """获取语言的显示名称"""
    if lang_code is None:
        lang_code = _current_language
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code)


def get_supported_languages() -> dict:
    """获取所有支持的语言"""
    return SUPPORTED_LANGUAGES.copy()


def get_location_info() -> dict:
    """获取当前检测到的地理位置信息

    返回:
        包含 country_code, country_name, detected_language, source 的字典
    """
    return {
        "country_code": _ip_geo_cache.get("country_code"),
        "country_name": _ip_geo_cache.get("country_name"),
        "detected_language": _ip_geo_cache.get("lang_detected"),
    }


def init_language(lang_code: str = None, auto_detect: bool = True) -> str:
    """初始化语言设置（三级降级策略）

    优先级（当 lang_code 未指定时）：
        1. 用户配置文件中的 language 偏好（最高优先级，尊重用户选择）
        2. IP 地理定位检测（仅当 auto_detect=True）
        3. 操作系统 Locale 检测
        4. 英文（默认 fallback）

    参数:
        lang_code: 显式指定语言代码，如 "zh_cn"。
                   若指定且有效，跳过所有自动检测。
        auto_detect: 是否启用 IP 地理定位自动检测。
                     True = 启用三级降级（位置 → locale → 英文）
                     False = 仅用配置文件 + 系统 locale

    返回:
        实际加载的语言代码
    """
    # 1) 显式指定优先
    if lang_code and lang_code in SUPPORTED_LANGUAGES:
        set_language(lang_code)
        return _current_language

    # 2) 用户配置文件偏好（尊重用户已保存的选择）
    config_lang = _read_config_language()
    if config_lang and config_lang in SUPPORTED_LANGUAGES:
        set_language(config_lang)
        return _current_language

    # 3) IP 地理定位自动检测（如果允许）
    detected_lang = None
    if auto_detect:
        try:
            detected_lang = _detect_language_by_ip()
        except Exception:
            detected_lang = None
        if detected_lang:
            set_language(detected_lang)
            return _current_language

    # 4) 系统 Locale 检测
    sys_lang = _detect_system_language()
    set_language(sys_lang)
    return _current_language


def auto_detect_and_set_language() -> Tuple[str, dict]:
    """执行一次完整的自动检测并切换语言

    与 init_language 不同，本函数会强制重新进行 IP 定位检测，
    并返回详细的检测信息，便于调试和 UI 展示。

    返回:
        (language_code, info_dict)
        info_dict 包含: source（检测来源）、country_code、country_name
    """
    # 先清除内存缓存，强制重新检测
    _ip_geo_cache["country_code"] = None
    _ip_geo_cache["timestamp"] = 0

    info = {"source": "default", "country_code": None, "country_name": None}

    # 1. IP 定位检测
    try:
        cc, cn = _detect_ip_geolocation()
        if cc:
            info["country_code"] = cc
            info["country_name"] = cn
            lang = _country_to_language(cc)
            if lang and lang in SUPPORTED_LANGUAGES:
                set_language(lang)
                info["source"] = "ip_geolocation"
                return (_current_language, info)
    except Exception:
        pass

    # 2. 系统 Locale
    try:
        sys_lang = _detect_system_language()
        set_language(sys_lang)
        info["source"] = "system_locale"
        return (_current_language, info)
    except Exception:
        pass

    # 3. 英文默认
    set_language(_DEFAULT_LANGUAGE)
    info["source"] = "default_fallback"
    return (_current_language, info)


def _read_config_language() -> str:
    """从用户配置文件读取语言设置"""
    config_file = _PROJECT_ROOT / "data" / "user_config.json"
    if not config_file.exists():
        return None
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get("language")
    except Exception:
        return None


def save_language_preference(lang_code: str) -> bool:
    """保存语言偏好到用户配置文件"""
    config_file = _PROJECT_ROOT / "data" / "user_config.json"
    config = {}
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {}
    config["language"] = lang_code
    try:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# 模块加载时初始化默认语言（启用自动检测）
init_language(auto_detect=True)
