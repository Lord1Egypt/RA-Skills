from __future__ import annotations

from dataclasses import dataclass, field

from .analysis import safe_text, unique_strings


@dataclass(frozen=True)
class SourceProfile:
    source_id: str
    display_name: str
    portal_names: tuple[str, ...]
    regions: tuple[str, ...]
    implemented: bool
    market: str | None = None
    aliases: tuple[str, ...] = field(default_factory=tuple)
    optional_provider: str = ""
    notes: str = ""


SOURCE_PROFILES: dict[str, SourceProfile] = {
    "ok": SourceProfile(
        source_id="ok",
        display_name="OK",
        portal_names=("OK",),
        regions=("australia", "uae", "singapore", "new zealand", "hong kong", "canada", "united states"),
        implemented=True,
        market="ok",
        aliases=("ok", "ok.com", "ok-core-skill"),
        notes="Bridge adapter implemented in Property Advisor; actual fetching is delegated to ok-core-skill.",
    ),
    "gt": SourceProfile(
        source_id="gt",
        display_name="Gumtree",
        portal_names=("Gumtree",),
        regions=("united kingdom", "uk", "england", "scotland", "wales", "northern ireland"),
        implemented=True,
        market="gt",
        aliases=("gt", "gumtree", "gt-core-skill"),
        notes="Bridge adapter implemented in Property Advisor; actual fetching is delegated to gt-core-skill.",
    ),
    "zillow": SourceProfile(
        source_id="zillow",
        display_name="Zillow",
        portal_names=("Zillow",),
        regions=("united states", "usa"),
        implemented=False,
        aliases=("zillow",),
        optional_provider="hasdata",
    ),
    "redfin": SourceProfile(
        source_id="redfin",
        display_name="Redfin",
        portal_names=("Redfin",),
        regions=("united states", "usa", "canada"),
        implemented=False,
        aliases=("redfin",),
        optional_provider="hasdata",
    ),
    "realtor": SourceProfile(
        source_id="realtor",
        display_name="Realtor.com",
        portal_names=("Realtor.com",),
        regions=("united states", "usa"),
        implemented=False,
        aliases=("realtor", "realtor.com"),
    ),
    "airbnb": SourceProfile(
        source_id="airbnb",
        display_name="Airbnb",
        portal_names=("Airbnb",),
        regions=("global",),
        implemented=False,
        aliases=("airbnb", "air bnb"),
        optional_provider="hasdata",
    ),
    "rightmove": SourceProfile(
        source_id="rightmove",
        display_name="Rightmove",
        portal_names=("Rightmove",),
        regions=("united kingdom", "uk"),
        implemented=False,
        aliases=("rightmove",),
    ),
    "zoopla": SourceProfile(
        source_id="zoopla",
        display_name="Zoopla",
        portal_names=("Zoopla",),
        regions=("united kingdom", "uk"),
        implemented=False,
        aliases=("zoopla",),
    ),
    "onthemarket": SourceProfile(
        source_id="onthemarket",
        display_name="OnTheMarket",
        portal_names=("OnTheMarket",),
        regions=("united kingdom", "uk"),
        implemented=False,
        aliases=("onthemarket", "on the market"),
    ),
    "domain": SourceProfile(
        source_id="domain",
        display_name="Domain",
        portal_names=("Domain",),
        regions=("australia",),
        implemented=False,
        aliases=("domain", "domain.com.au"),
    ),
    "realestate_au": SourceProfile(
        source_id="realestate_au",
        display_name="realestate.com.au",
        portal_names=("realestate.com.au",),
        regions=("australia",),
        implemented=False,
        aliases=("realestate.com.au", "real estate australia", "rea"),
    ),
    "propertyguru": SourceProfile(
        source_id="propertyguru",
        display_name="PropertyGuru",
        portal_names=("PropertyGuru",),
        regions=("singapore", "malaysia"),
        implemented=False,
        aliases=("propertyguru", "property guru"),
    ),
    "99co": SourceProfile(
        source_id="99co",
        display_name="99.co",
        portal_names=("99.co",),
        regions=("singapore",),
        implemented=False,
        aliases=("99.co", "99co"),
    ),
    "idealista": SourceProfile(
        source_id="idealista",
        display_name="Idealista",
        portal_names=("Idealista",),
        regions=("spain", "portugal", "italy"),
        implemented=False,
        aliases=("idealista",),
    ),
    "immoscout24": SourceProfile(
        source_id="immoscout24",
        display_name="ImmoScout24",
        portal_names=("ImmoScout24",),
        regions=("germany", "austria"),
        implemented=False,
        aliases=("immoscout24", "immobilienscout24", "immo scout"),
    ),
    "bayut": SourceProfile(
        source_id="bayut",
        display_name="Bayut",
        portal_names=("Bayut",),
        regions=("uae", "united arab emirates"),
        implemented=False,
        aliases=("bayut",),
    ),
    "dubizzle": SourceProfile(
        source_id="dubizzle",
        display_name="Dubizzle",
        portal_names=("Dubizzle",),
        regions=("uae", "united arab emirates"),
        implemented=False,
        aliases=("dubizzle",),
    ),
    "propertyfinder": SourceProfile(
        source_id="propertyfinder",
        display_name="Property Finder",
        portal_names=("Property Finder",),
        regions=("uae", "united arab emirates", "egypt", "qatar", "bahrain"),
        implemented=False,
        aliases=("propertyfinder", "property finder"),
    ),
}


COUNTRY_SOURCE_ORDER: dict[str, tuple[str, ...]] = {
    "united kingdom": ("gt", "rightmove", "zoopla", "onthemarket"),
    "uk": ("gt", "rightmove", "zoopla", "onthemarket"),
    "australia": ("ok", "domain", "realestate_au"),
    "uae": ("ok", "propertyfinder", "bayut", "dubizzle"),
    "united arab emirates": ("ok", "propertyfinder", "bayut", "dubizzle"),
    "singapore": ("ok", "propertyguru", "99co"),
    "united states": ("ok", "zillow", "redfin", "realtor"),
    "usa": ("ok", "zillow", "redfin", "realtor"),
    "spain": ("idealista",),
    "germany": ("immoscout24",),
}


def normalize_source_hint(value: str) -> str:
    raw = safe_text(value).lower()
    if not raw or raw == "auto":
        return "auto"
    for source_id, profile in SOURCE_PROFILES.items():
        if raw == source_id or raw == profile.display_name.lower() or raw in profile.aliases:
            return source_id
    normalized = raw.replace("-", "_").replace(".", "").replace(" ", "_")
    if normalized in SOURCE_PROFILES:
        return normalized
    return raw


def source_profile(source_id: str) -> SourceProfile | None:
    return SOURCE_PROFILES.get(normalize_source_hint(source_id))


def is_implemented_source(source_id: str) -> bool:
    profile = source_profile(source_id)
    return bool(profile and profile.implemented)


def market_for_source(source_id: str) -> str | None:
    profile = source_profile(source_id)
    return profile.market if profile else None


def detect_source_signals(text: str) -> list[str]:
    lowered = safe_text(text).lower()
    matches: list[str] = []
    if not lowered:
        return matches
    for source_id, profile in SOURCE_PROFILES.items():
        candidates = (source_id, profile.display_name.lower(), *profile.aliases, *[name.lower() for name in profile.portal_names])
        if any(candidate and candidate in lowered for candidate in candidates):
            matches.append(source_id)
    return unique_strings(matches)


def candidate_sources_for_country(country: str) -> list[str]:
    normalized = safe_text(country).lower()
    if normalized in COUNTRY_SOURCE_ORDER:
        return list(COUNTRY_SOURCE_ORDER[normalized])
    for key, values in COUNTRY_SOURCE_ORDER.items():
        if key in normalized:
            return list(values)
    return ["ok"]


def first_implemented_source(candidates: list[str]) -> str:
    for candidate in candidates:
        if is_implemented_source(candidate):
            return candidate
    return "ok"


def unavailable_source_message(source_id: str) -> str:
    profile = source_profile(source_id)
    label = profile.display_name if profile else source_id
    if profile and profile.optional_provider == "hasdata":
        return (
            f"数据源 {label} 已识别，但当前 Property Advisor 尚未接入本地 adapter。"
            "如需使用该平台，可在用户确认后安装并配置 HasData 可选插件："
            "openclaw plugins install clawhub:@hasdata/hasdata-openclaw-plugin；"
            "同时需要配置 HASDATA_API_KEY。插件返回结果仍必须先转成 Property Advisor listing contract。"
        )
    return f"数据源 {label} 已识别，但当前 Property Advisor 尚未安装或接入可执行 adapter；请先安装/配置对应 source 后重试。"
