#!/usr/bin/env python3
"""配件查询工具 — 按品类、预算、平台、颜色筛选配件。

渐进式披露: 默认只返回 summary (id+model+price)，用 --detail 看完整属性。

用法:
  python query_components.py --category gpu --budget 5000
  python query_components.py --category cpu --platform intel --limit 5
  python query_components.py --category case --color white --summary
  python query_components.py --category all --budget 8000 --json
"""

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from statistics import median
from pathlib import Path

import yaml

from component_inference import (
    THERMAL_HIGH,
    THERMAL_LOW,
    THERMAL_MAINSTREAM,
    THERMAL_STRONG,
    USER_CONFIRMED_SPEC_FIELDS,
    infer_cooler_thermal_profile,
    infer_cooler_exclusive_platform,
    infer_cpu_integrated_graphics,
    infer_gpu_cooling,
    infer_gpu_vram,
    normalize_memory_generation,
    normalize_memory_generations,
    normalize_display_output,
    normalize_display_outputs,
    normalize_psu_form_factor,
)
from catalog_overlay import (
    CATEGORY_SECTIONS,
    GPU_CATALOG_CONFLICT_FIELDS,
    OverlayError,
    enrich_resolved_item,
    load_catalog_sections,
    resolve_catalog,
    resolve_id,
)
from motherboard_capabilities import (
    pcie_physical_slot_count,
    verified_thunderbolt_ports,
    verified_usb4_ports,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CATEGORIES = {
    "cpu": "cpus",
    "mb": "motherboards",
    "memory": "memory",
    "storage": "storage",
    "gpu": "gpus",
    "cooler": "coolers",
    "psu": "psus",
    "case": "cases",  # from cases.yaml
    "display": "displays",  # from displays.yaml, explicit only
    "monitor": "displays",  # alias for display
    "fan": "fans",  # explicit only, not part of all
}

CORE_CATEGORIES = ("cpu", "mb", "memory", "storage", "gpu", "cooler", "psu", "case")
DISPLAY_CATEGORIES = {"display", "monitor"}
FAN_CATEGORIES = {"fan"}
DEFAULT_QUERY_LIMIT = 20
PRICE_STALE_AFTER_DAYS = 14
PRICE_FLOOR_SPARSE_ABOVE_COUNT = 3
PRICE_FLOOR_VERIFY_WARNING = "价格变化大，数据更新可能不及时，请及时核对现价。"


@dataclass(frozen=True)
class QuerySpec:
    category: str | None = None
    budget: int | None = None
    platform: str | None = None
    color: str | None = None
    rgb: bool | None = None
    limit: int = DEFAULT_QUERY_LIMIT
    has_price_only: bool = True
    showcase: bool | None = None
    include_legacy: bool = False
    sort: str = "asc"
    socket: str | None = None
    chipset: str | None = None
    memory_gen: str | None = None
    form_factor: str | None = None
    max_length: int | None = None
    max_cooler_height: int | None = None
    gpu_cooling: str | None = "air"
    gpu_chip: str | None = None
    min_vram: int | None = None
    min_capacity: int | None = None
    include_workstation_gpu: bool = False
    resolution: str | None = None
    min_refresh: int | None = None
    air_flow: str | None = None
    dust_filter: bool | None = None
    fan_size: int | None = None
    blade_direction: str | None = None
    linkable: bool | None = None
    screen: bool | None = None
    radiator_bundle: int | None = None
    fan_type: str | None = None
    model: str | None = None
    item_id: str | None = None
    max_capacity: int | None = None
    pcie_generation: int | None = None
    dram_cache: bool | None = None
    integrated_graphics: bool | None = None
    display_output: str | None = None
    min_pcie_slots: int | None = None
    require_usb4: bool = False
    require_thunderbolt: bool = False

DEDUPE_SPEC_FIELDS = {
    "cpu": ("socket", "power_w", "integrated_graphics"),
    "mb": (
        "socket", "memory_generations", "form_factor", "memory_slots",
        "memory_max_gb", "memory_freq_max", "m2_slots", "sata_ports", "display_outputs",
        "pcie_slot_layout", "m2_slot_layout", "usb4_status", "usb4_rear_ports", "usb4_speed_gbps",
        "usb4_shares_with", "usb4_disable_conditions", "thunderbolt_status",
        "thunderbolt_rear_ports", "thunderbolt_version", "thunderbolt_header",
        "sata_port_conditions",
    ),
    "memory": ("generation", "capacity_gb", "module_count", "frequency_mt", "timing", "color", "rgb"),
    "storage": ("capacity_gb", "capacity_tb", "interface", "pcie_generation", "form_factor", "dram_cache"),
    "gpu": (
        "chip", "vram_gb", "memory_type", "gpu_cooling", "color",
        "length_mm", "power_w", "power_connectors", "requires_16pin_psu",
    ),
    "cooler": (
        "type", "radiator_mm", "height_mm", "air_cooler_layout", "heatpipe_count", "color",
    ),
    "psu": ("wattage_w", "form_factor", "length_mm", "native_16pin_gpu_power", "color"),
    "case": (
        "colors", "motherboard_support", "gpu_length_mm", "cpu_cooler_height_mm",
        "psu_support", "psu_length_mm", "psu_length_recommended_mm",
    ),
    "display": ("resolution", "size_inch", "refresh_rate_hz"),
    "fan": ("size_mm", "pack_count", "blade_direction", "color", "fan_type"),
}

GPU_CONFLICT_FIELDS = GPU_CATALOG_CONFLICT_FIELDS

DISPLAY_NAMES = {
    "cpu": "CPU",
    "mb": "主板",
    "memory": "内存",
    "storage": "硬盘",
    "gpu": "显卡",
    "cooler": "散热",
    "psu": "电源",
    "case": "机箱",
    "display": "显示器",
    "monitor": "显示器",
    "fan": "风扇",
}

# Summary fields per category — minimal fields needed for first-pass narrowing.
SUMMARY_BASE_FIELDS = [
    "id", "brand", "model", "brand_en", "model_en", "normalization_status",
    "price", "price_currency", "price_cny", "base_price_cny", "price_status", "price_date", "price_note",
    "price_age_days", "price_stale", "price_floor_cny", "price_floor_status",
    "price_floor_gap_percent", "price_floor_bottom_decile_cutoff_cny",
    "price_floor_policy", "price_floor_above_candidate_count",
    "price_floor_warning", "spec_conflicts",
]
SUMMARY_FIELDS_BY_CATEGORY = {
    "cpu": SUMMARY_BASE_FIELDS + [
        "platform", "socket", "cores_threads", "cores", "threads", "power_w", "integrated_graphics",
    ],
    "mb": SUMMARY_BASE_FIELDS + [
        "platform", "socket", "chipset", "memory_generations", "memory_slots",
        "memory_max_gb", "memory_freq_max", "m2_slots", "sata_ports", "sata_port_conditions",
        "m2_slot_layout", "display_outputs", "form_factor", "color",
        "usb4_status", "usb4_rear_ports", "usb4_speed_gbps",
        "usb4_shares_with", "usb4_disable_conditions",
        "thunderbolt_status", "thunderbolt_rear_ports", "thunderbolt_version",
        "thunderbolt_header",
    ],
    "memory": SUMMARY_BASE_FIELDS + [
        "generation", "capacity_gb", "module_count", "frequency_mt", "timing", "color", "rgb",
    ],
    "storage": SUMMARY_BASE_FIELDS + [
        "capacity_tb", "capacity_gb", "form_factor", "interface", "pcie_generation", "storage_type",
        "dram_cache", "dram_cache_mb", "series",
    ],
    "gpu": SUMMARY_BASE_FIELDS + [
        "chip", "gpu_vendor", "vram_gb", "memory_type", "memory_bus_bit",
        "memory_bandwidth_gbps", "gpu_cooling", "gpu_radiator_required",
        "length_mm", "power_w", "power_connectors", "requires_16pin_psu", "color", "rgb",
    ],
    "cooler": SUMMARY_BASE_FIELDS + [
        "type", "height_mm", "radiator_mm", "air_cooler_layout", "heatpipe_count", "color", "rgb",
    ],
    "psu": SUMMARY_BASE_FIELDS + [
        "wattage_w", "form_factor", "length_mm", "efficiency", "modular", "native_16pin_gpu_power", "color",
    ],
    "case": SUMMARY_BASE_FIELDS + [
        "colors", "motherboard_support", "gpu_length_mm", "cpu_cooler_height_mm",
        "radiator_support", "fan_mounts", "fan_slots_count", "psu_support", "psu_length_mm",
        "psu_length_recommended_mm", "psu_length_condition",
        "air_flow_type", "has_dust_filter", "is_showcase",
    ],
    "display": SUMMARY_BASE_FIELDS + ["resolution", "size_inch", "refresh_rate_hz"],
    "monitor": SUMMARY_BASE_FIELDS + ["resolution", "size_inch", "refresh_rate_hz"],
    "fan": SUMMARY_BASE_FIELDS + [
        "size_mm", "pack_count", "color", "rgb", "blade_direction",
        "is_linkable", "has_screen", "radiator_fan_bundle_mm",
        "fan_type", "default_recommend",
    ],
}

COLOR_ALIASES = {
    "white": {"white", "白", "白色"},
    "black": {"black", "黑", "黑色"},
}

RGB_TERMS = ("ARGB", "RGB", "幻彩", "炫彩", "彩色", "彩光", "灯效", "灯光", "发光")
NO_RGB_TERMS = ("无光", "不发光")
FAN_ACCESSORY_RE = re.compile(r"(?:控制器|集线器|遥控器|HUB)\s*$", re.IGNORECASE)

# 以下排序只按芯片/芯片组定位辅助筛选，不包含品牌优劣判断。
# 若后续加入品牌/系列候选池权重，应仅基于公开电商销量、装机采用率、
# 渠道覆盖和规格完整度等可观察信号，并保持非品牌倾向、非品牌贬损。
GPU_TIERS = (
    ("RTXPRO6000", 10.0),
    ("RTX5090DV2", 7.8), ("RTX5090D", 8.0), ("RTX5090", 8.2),
    ("RTX5080", 7),
    ("RTX5070TI", 6),
    ("RTX5070", 5), ("RX9070XT", 5),
    ("RTX5060TI", 4),
    ("RX9070GRE", 3), ("RX9070", 3),
    ("RTX5060", 2), ("ARCB580", 2), ("A770", 2), ("RX9060XT", 2), ("RTX3060TI", 2),
    ("RTX5050", 1), ("ARCB570", 1), ("A750", 1),
)

MOTHERBOARD_TIERS = (
    ("Z890", 70), ("X870", 70),
    ("Z790", 65), ("X670", 65),
    ("B860", 55), ("B850", 55),
    ("B760", 50), ("B650", 50),
    ("B550", 45),
    ("H810", 10), ("H610", 10), ("A820", 10), ("A620", 10), ("A520", 5),
)

# Positive candidate-pool signals derived from public adoption, channel coverage,
# visible specifications and common DIY usage. This is not a brand endorsement
# or a negative judgment against brands outside the list.
MOTHERBOARD_PRIMARY_SIGNALS = (
    "华硕", "ASUS", "技嘉", "GIGABYTE", "微星", "MSI",
)

MOTHERBOARD_SERIES_SIGNALS = (
    "AYW", "TUF", "PRIME", "AORUS", "GAMINGX", "GAMING X",
    "迫击炮", "MORTAR", "MAG", "GAMINGPRO", "GAMING PRO", "小雕",
)

MOTHERBOARD_COMMON_SIGNALS = (
    "华擎", "ASROCK", "七彩虹", "COLORFUL", "BATTLEAX",
)

STORAGE_PRIMARY_SIGNALS = (
    "SAMSUNG", "三星", "致态", "TIPLUS", "TIPLUS", "ZHITAI",
    "宏碁掠夺者", "PREDATOR", "ACER",
    "WD", "西数", "SN850", "SN770", "BLACK",
    "KIOXIA", "铠侠", "SOLIDIGM", "海力士", "HYNIX",
    "LEXAR", "雷克沙", "CRUCIAL", "英睿达",
    "ADATA", "威刚", "XPG",
)

STORAGE_COMMON_SIGNALS = (
    "金百达", "KINGBANK", "梵想", "光威",
)

MEMORY_ADOPTION_SIGNALS = (
    "芝奇", "GSKILL", "G.SKILL", "TRIDENT", "幻锋",
    "金百达", "KINGBANK", "阿斯加特", "ASGARD",
    "ADATA", "威刚", "XPG", "光威", "GLOWAY", "玖合",
    "宏碁掠夺者", "PREDATOR", "ACER", "KINGSTON", "金士顿",
    "CORSAIR", "海盗船", "CRUCIAL", "英睿达",
)

COOLER_ADOPTION_SIGNALS = (
    "利民", "THERMALRIGHT", "九州风神", "DEEPCOOL", "酷冷至尊", "COOLERMASTER",
    "雅浚", "乔思伯", "JONSBO", "瓦尔基里", "VALKYRIE", "华硕", "ASUS",
)

PSU_PRIMARY_SIGNALS = (
    "海韵", "SEASONIC", "振华", "SUPERFLOWER", "SUPER FLOWER",
    "海盗船", "CORSAIR", "全汉", "FSP",
)

PSU_COMMON_SIGNALS = (
    "微星", "MSI", "酷冷至尊", "COOLERMASTER", "长城", "GREATWALL",
    "安钛克", "ANTEC", "鑫谷", "SEGOTEP", "华硕", "ASUS",
)


_OVERLAY_PATHS = ()
_QUERY_CURRENCY = "CNY"
_RESOLVED_BY_ID = {}
_ALIAS_INDEX = {}


@lru_cache(maxsize=1)
def _resolved_sections():
    """Load the immutable base catalog and apply only explicitly supplied overlays."""
    global _RESOLVED_BY_ID, _ALIAS_INDEX
    sections = load_catalog_sections(DATA)
    sections, _RESOLVED_BY_ID, _ALIAS_INDEX = resolve_catalog(sections, _OVERLAY_PATHS, data_dir=DATA)
    for section, items in list(sections.items()):
        sections[section] = [enrich_resolved_item(section, item) for item in items]
    return sections


def configure_overlays(paths, currency):
    global _OVERLAY_PATHS, _QUERY_CURRENCY
    _OVERLAY_PATHS = tuple(paths or ())
    _QUERY_CURRENCY = currency
    _resolved_sections.cache_clear()


def load_components():
    return _resolved_sections()


def load_cases():
    return {"cases": _resolved_sections().get("cases", [])}


def load_displays():
    return {"displays": _resolved_sections().get("displays", [])}


_PRICE_FLOORS = None


def load_price_floors():
    """Load optional lower-bound market reference floors."""
    global _PRICE_FLOORS
    if _PRICE_FLOORS is not None:
        return _PRICE_FLOORS
    path = DATA / "price_floors.yaml"
    if not path.exists():
        _PRICE_FLOORS = {}
        return _PRICE_FLOORS
    with path.open("r", encoding="utf-8") as f:
        _PRICE_FLOORS = yaml.safe_load(f) or {}
    return _PRICE_FLOORS


def normalize_color(value):
    """Normalize common Chinese/English color names."""
    if value is None:
        return ""
    text = str(value).strip().lower()
    for normalized, aliases in COLOR_ALIASES.items():
        if text in aliases:
            return normalized
    return text


def normalize_resolution(value):
    """Normalize common display resolution aliases for filtering."""
    text = compact_text(value)
    if not text:
        return ""
    if "2160" in text or "4K" in text:
        return "2160P"
    if "1440" in text or "2K" in text or "QHD" in text:
        return "1440P"
    if "1080" in text or "1K" in text or "FHD" in text:
        return "1080P"
    return text


def compact_text(value):
    """Normalize model/spec text for simple scope checks."""
    text = unicodedata.normalize("NFKC", str(value or ""))
    return "".join(ch for ch in text.upper() if ch.isalnum())


GPU_MODEL_QUERY_CHIP_PATTERN = re.compile(
    r"(?:RTX\d{4}(?:DV2|TISUPER|SUPER|TI|V2|D)?|"
    r"RX\d{4}(?:GRE|XT)?|ARC[AB]\d{3})"
)
GPU_BARE_NVIDIA_MODEL_QUERY_PATTERN = re.compile(
    r"^(?:NVIDIA)?(?:GEFORCE)?(20|30|40|50)(\d{2})(TISUPER|SUPER|TI|D)?$"
)


def _gpu_chip_from_model_query(value):
    """Extract a chip token so a model query cannot cross GPU SKU suffixes."""
    compact = compact_text(value)
    match = GPU_MODEL_QUERY_CHIP_PATTERN.search(compact)
    if match:
        return match.group(0)
    bare = GPU_BARE_NVIDIA_MODEL_QUERY_PATTERN.fullmatch(compact)
    if bare:
        return "RTX" + "".join(part or "" for part in bare.groups())
    return None


def _gpu_chip_only_model_query(value):
    """Return a chip only when the whole model query is a chip shorthand."""
    compact = compact_text(value)
    direct = GPU_MODEL_QUERY_CHIP_PATTERN.fullmatch(compact)
    if direct:
        return direct.group(0)
    bare = GPU_BARE_NVIDIA_MODEL_QUERY_PATTERN.fullmatch(compact)
    if bare:
        return "RTX" + "".join(part or "" for part in bare.groups())
    return None


def is_fan_accessory(item):
    """Identify accessory-only variants that must not enter fan recommendations."""
    return bool(FAN_ACCESSORY_RE.search(str(item.get("model") or "").strip()))


def _dedupe_key(category, item):
    """Build a display-level key for duplicate channel quotes of one SKU."""
    model = compact_text(item.get("model"))
    if not model:
        return (category, compact_text(item.get("id")))
    brand = compact_text(item.get("brand"))
    if brand and model.startswith(brand):
        model = model[len(brand):]
    specs = tuple(
        compact_text(item.get(field))
        for field in DEDUPE_SPEC_FIELDS.get(category, ())
    )
    return (category, brand, model, specs)


def _model_identity_key(item):
    model = compact_text(item.get("model"))
    brand = compact_text(item.get("brand"))
    if brand and model.startswith(brand):
        model = model[len(brand):]
    return brand, model


def filter_ambiguous_gpu_skus(results, catalog):
    """Hide exact model identities whose compatibility-sensitive facts conflict."""
    marked_identities = {
        _model_identity_key(item)
        for item in catalog
        if item.get("spec_conflicts") or item.get("_catalog_conflict_fields")
    }
    if marked_identities:
        return [
            item for item in results
            if not (
                _model_identity_key(item) in marked_identities
                and (item.get("spec_conflicts") or item.get("_catalog_conflict_fields"))
            )
        ]
    grouped = {}
    for item in catalog:
        key = _model_identity_key(item)
        if not all(key):
            continue
        facts = grouped.setdefault(key, {field: set() for field in GPU_CONFLICT_FIELDS})
        for field in GPU_CONFLICT_FIELDS:
            value = item.get(field)
            if value not in (None, "", []):
                facts[field].add(compact_text(value))
    ambiguous = {
        key for key, fields in grouped.items()
        if any(len(values) > 1 for values in fields.values())
    }
    return [item for item in results if _model_identity_key(item) not in ambiguous]


def dedupe_results(category, results):
    """Keep one quote per displayed SKU, preferring a fresh quote when possible."""
    seen = {}
    unique = []
    for item in results:
        key = _dedupe_key(category, item)
        if key in seen:
            index = seen[key]
            current = unique[index]
            if (
                _price_freshness(current).get("price_stale", False)
                and not _price_freshness(item).get("price_stale", False)
            ):
                unique[index] = item
            continue
        seen[key] = len(unique)
        unique.append(item)
    return unique


def _finalize_sorted_results(results, sort, category):
    """Deduplicate display rows and restore the requested order afterward."""
    deduped = dedupe_results(category, results)
    _sort_results(deduped, sort, category)
    return deduped


def _matches_identity(item, model=None, item_id=None):
    """Match a user-supplied model token or an exact library ID."""
    if item_id and str(item.get("id", "")) != str(item_id):
        return False
    if model:
        wanted = compact_text(model)
        is_gpu = str(item.get("id", "")).startswith(("gpu-", "user-gpu-"))
        identity_fields = ["brand", "model", "brand_en", "model_en", "id"]
        if is_gpu:
            identity_fields.append("chip")
        haystack = compact_text(" ".join(str(item.get(k, "")) for k in identity_fields))
        chip_only = _gpu_chip_only_model_query(model) if is_gpu else None
        if wanted not in haystack and chip_only is None:
            return False
        if is_gpu:
            requested_chip = _gpu_chip_from_model_query(model)
            if requested_chip and not _matches_gpu_chip(item, requested_chip):
                return False
    return True


GPU_FAMILY_ONLY_MODEL_QUERY_PATTERN = re.compile(
    r"^(?:(?:NVIDIA)?(?:GEFORCE)?RTX(?:20|30|40|50)?|"
    r"(?:AMD)?(?:RADEON)?RX(?:5000|6000|7000|9000)?|"
    r"(?:INTEL)?ARC(?:A|B)?)$"
)
GPU_GENERIC_MODEL_QUERY_PATTERN = re.compile(
    r"^(?:"
    r"NVIDIA|GEFORCE|RTX(?:20|30|40|50)?|AMD|RADEON|RX(?:5000|6000|7000|9000)?|"
    r"INTEL|ARC(?:A|B)?|GPU|GRAPHICSCARD|显卡|独立显卡|"
    r"OC|O|TI|SUPER|XT|GRE|V2|D|GAMING|PRO|DUAL|TRIO|AIR|WATER|LIQUID|"
    r"WHITE|BLACK|PINK|SILVER|RGB|ARGB|白|黑|白色|黑色|粉色|银色|水冷|风冷|"
    r"VRAM|显存|FAN|风扇|SINGLEFAN|DUALFAN|TRIPLEFAN|"
    r"单风扇|双风扇|三风扇|四风扇|"
    r"\d{1,3}|\d+(?:GB|G)|\d+FAN"
    r")+$"
)


def _strip_catalog_gpu_brand_prefix(compact, catalog_brands):
    """Remove an explicit brand prefix before classifying the remaining tokens."""
    for brand in sorted(catalog_brands, key=len, reverse=True):
        if compact.startswith(brand):
            return compact[len(brand):]
    return compact


def _is_specific_gpu_model_query(value, catalog):
    """Allow scope bypass for a concrete chip/model/series, not a broad family term."""
    compact = compact_text(value)
    catalog_brands = {
        compact_text(item.get(field))
        for item in catalog
        for field in ("brand", "brand_en", "gpu_vendor")
        if compact_text(item.get(field))
    }
    if not compact or compact in catalog_brands:
        return False
    without_brand = _strip_catalog_gpu_brand_prefix(compact, catalog_brands)
    if not without_brand or GPU_FAMILY_ONLY_MODEL_QUERY_PATTERN.fullmatch(without_brand):
        return False
    if _gpu_chip_only_model_query(value):
        return True
    if _gpu_chip_from_model_query(value):
        return any(_matches_identity(item, model=value) for item in catalog)
    if GPU_GENERIC_MODEL_QUERY_PATTERN.fullmatch(without_brand):
        return False
    return any(
        _matches_identity(item, model=value)
        or (
            without_brand != compact
            and _matches_identity(item, model=without_brand)
        )
        for item in catalog
    )


def _parse_num(value, default=0):
    """Parse imported numeric fields that may carry units or noisy text."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        cleaned = re.sub(r"[^\d.-]", "", value)
        if cleaned in ("", "-", ".", "-."):
            return default
        try:
            return float(cleaned) if "." in cleaned else int(cleaned)
        except ValueError:
            return default
    return default


def _parse_int(value, default=0):
    return int(_parse_num(value, default) or default)


def _capacity_upper_bound(section, value):
    """Map common marketed SSD capacities to their binary GB representation."""
    parsed = _parse_int(value)
    if section == "storage":
        return {500: 512, 1000: 1024, 2000: 2048, 4000: 4096, 8000: 8192}.get(parsed, parsed)
    return parsed


def item_text(item):
    """Join searchable fields for positive candidate-pool scoring."""
    return " ".join(str(item.get(k, "")) for k in ("brand", "model", "series", "id"))


def infer_display_brand(item):
    """Best-effort brand display for monitor rows whose model already starts with the brand."""
    if item.get("brand"):
        return item.get("brand")
    model = str(item.get("model") or "").strip()
    if model:
        token = re.split(r"\s+", model, maxsplit=1)[0].strip()
        if token and not re.match(r"^\d", token):
            return token
    item_id = str(item.get("id") or "")
    match = re.match(r"display-([^-]+)-", item_id)
    return match.group(1) if match else ""


def has_candidate_signal(item, signals):
    """Return whether an item matches a positive public-adoption signal."""
    text = compact_text(item_text(item))
    return any(compact_text(signal) in text for signal in signals)


def candidate_signal_score(item, primary=(), secondary=(), common=()):
    """Score visible public-adoption signals without using negative brand labels."""
    score = 0
    if primary and has_candidate_signal(item, primary):
        score += 12
    if secondary and has_candidate_signal(item, secondary):
        score += 6
    if common and has_candidate_signal(item, common):
        score += 4
    return score


def parse_rated_wattage(item):
    """Prefer rated wattage in the model text over noisy imported fields."""
    text = " ".join(str(item.get(k, "")) for k in ("model", "id", "series"))
    match = re.search(r"额定\s*(\d{3,4})\s*W", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d{3,4})\s*W", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    candidates = [
        int(m.group(1))
        for m in re.finditer(r"(?<![0-9.])([3-9]\d{2}|1\d{3}|2000)(?![0-9.])", text)
    ]
    plausible = [value for value in candidates if 300 <= value <= 2000]
    if plausible:
        return plausible[0]
    return _parse_int(item.get("wattage_w"))


def _extract_cpu_model_token(item):
    text = compact_text(item_text(item))
    ultra = re.search(r"ULTRA[579](?:2[235678]\d)(?:K|KF|F)?(?:PLUS)?", text)
    if ultra:
        return ultra.group(0)
    core = re.search(r"I[3579](?:12|13|14)\d{3}(?:KF|K|F)?", text)
    if core:
        return core.group(0)
    for token in (
        "9950X3D", "9900X3D", "9800X3D", "7800X3D",
        "9950X", "9900X", "9700X", "9600X", "7500F",
    ):
        if token in text:
            return token
    return ""


def _cpu_price_floor_tokens(value):
    """Return compact aliases used by public daily CPU price-floor rows."""
    text = compact_text(value)
    tokens = {text} if text else set()
    ultra = re.fullmatch(r"U([579])(\d{3})(K|KF|F)?(PLUS)?", text)
    if ultra:
        suffix = ultra.group(3) or ""
        plus = ultra.group(4) or ""
        tokens.add(f"ULTRA{ultra.group(1)}{ultra.group(2)}{suffix}{plus}")
        tokens.add(f"COREULTRA{ultra.group(1)}{ultra.group(2)}{suffix}{plus}")
    ryzen = re.fullmatch(r"R([579])(\d{4}(?:X3D|X|F)?)", text)
    if ryzen:
        tokens.add(f"RYZEN{ryzen.group(1)}{ryzen.group(2)}")
        tokens.add(f"AMDRYZEN{ryzen.group(1)}{ryzen.group(2)}")
    return tokens


def _outlier_group_key(category, item):
    """Group near-identical specs so default tier sort can ignore low-price outliers."""
    if category == "gpu":
        chip = compact_text(item.get("chip") or "")
        if not chip:
            chip = compact_text(item.get("model") or "")
            for key, _ in GPU_TIERS:
                if key in chip:
                    chip = key
                    break
        vram = _parse_int(infer_gpu_vram(item))
        return ("gpu", chip, vram) if chip and vram else None
    if category == "storage":
        capacity = _parse_int(item.get("capacity_gb"))
        gen = _parse_int(item.get("pcie_generation"))
        speed = _storage_read_speed(item)
        speed_bucket = (speed // 1000) if speed else 0
        return ("storage", capacity, gen, speed_bucket) if capacity and gen else None
    if category == "memory":
        generation = normalize_memory_generation(item.get("generation"))
        capacity = _parse_int(item.get("capacity_gb"))
        freq = _parse_int(item.get("frequency_mt"))
        timing = _memory_timing_value(item)
        modules = _parse_int(item.get("module_count"))
        return ("memory", generation, capacity, freq, timing, modules) if generation and capacity and freq else None
    return None


def _near_capacity(value, target):
    if not value or not target:
        return False
    value = _parse_int(value)
    target = _parse_int(target)
    return abs(value - target) <= 96


def _same_capacity(value, target):
    if not value or not target:
        return False
    return _parse_int(value) == _parse_int(target)


def _storage_trusted_price_floor(rows, item):
    """Return a storage floor without letting unknown M.2 generations bypass it."""
    generation = _parse_int(item.get("pcie_generation"))
    capacity = _parse_int(item.get("capacity_gb"))
    if not capacity and item.get("capacity_tb"):
        capacity = int(_parse_num(item.get("capacity_tb")) * 1000)
    same_capacity_rows = [
        row for row in rows
        if _near_capacity(capacity, row.get("capacity_gb"))
    ]
    if not same_capacity_rows:
        return None
    if generation:
        for row in same_capacity_rows:
            if generation == _parse_int(row.get("pcie_generation")):
                return _parse_int(row.get("floor_cny")) or None
        lower_generation_rows = [
            row for row in same_capacity_rows
            if (row_generation := _parse_int(row.get("pcie_generation"))) and row_generation <= generation
        ]
        if lower_generation_rows:
            best_floor = max(
                lower_generation_rows,
                key=lambda row: _parse_int(row.get("pcie_generation")),
            )
            return _parse_int(best_floor.get("floor_cny")) or None
        return None

    # M.2 rows with an unknown PCIe generation still need the lowest known
    # same-capacity PCIe floor; SATA rows have a different market baseline.
    interface = compact_text(item.get("interface") or item.get("form_factor"))
    if "M2" not in interface:
        return None
    known_generation_rows = [
        row for row in same_capacity_rows
        if _parse_int(row.get("pcie_generation"))
    ]
    if not known_generation_rows:
        return None
    conservative_floor = min(
        known_generation_rows,
        key=lambda row: _parse_int(row.get("pcie_generation")),
    )
    return _parse_int(conservative_floor.get("floor_cny")) or None


def _trusted_price_floor(category, item):
    """Return a trusted lower price bound for categories with market floor data."""
    floors = load_price_floors()
    if category == "cpu":
        text = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "id")))
        rows = sorted(floors.get("cpus", []), key=lambda row: len(compact_text(row.get("model"))), reverse=True)
        for row in rows:
            tokens = _cpu_price_floor_tokens(row.get("model"))
            if tokens and any(token in text for token in tokens):
                return _parse_int(row.get("floor_cny")) or None
    if category == "gpu":
        chip_text = compact_text(" ".join(str(item.get(k, "")) for k in ("chip", "model", "id")))
        vram = _parse_int(infer_gpu_vram(item))
        rows = sorted(floors.get("gpus", []), key=lambda row: len(compact_text(row.get("chip"))), reverse=True)
        for row in rows:
            target = compact_text(row.get("chip"))
            if not target or target not in chip_text:
                continue
            min_vram = _parse_int(row.get("min_vram_gb"))
            max_vram = _parse_int(row.get("max_vram_gb"))
            if min_vram and vram and vram < min_vram:
                continue
            if max_vram and vram and vram > max_vram:
                continue
            return _parse_int(row.get("floor_cny")) or None
    if category == "memory":
        generation = normalize_memory_generation(item.get("generation"))
        capacity = _parse_int(item.get("capacity_gb"))
        modules = _parse_int(item.get("module_count"))
        for row in floors.get("memory", []):
            if generation != normalize_memory_generation(row.get("generation")):
                continue
            if not _same_capacity(capacity, row.get("capacity_gb")):
                continue
            row_modules = _parse_int(row.get("module_count"))
            if row_modules and modules and modules != row_modules:
                continue
            return _parse_int(row.get("floor_cny")) or None
    if category == "storage":
        return _storage_trusted_price_floor(floors.get("storage", []), item)
    return None


def _low_price_floor(category, group_key, group_prices):
    """Return a conservative lower bound for default candidate ranking."""
    if len(group_prices) < 4:
        return None
    mid = median(group_prices)
    if category == "memory":
        ratio = 0.65
    elif category == "gpu":
        chip = str(group_key[1]) if len(group_key) > 1 else ""
        if "RTX5090" in chip:
            ratio = 0.90
        elif "RTX5080" in chip:
            ratio = 0.85
        else:
            ratio = 0.80
    else:
        ratio = 0.60
    return mid * ratio


def _price_floor_group_key(category, item, floor_cny):
    """Group candidates covered by the same trusted floor policy."""
    if category == "cpu":
        text = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "id")))
        rows = sorted(
            load_price_floors().get("cpus", []),
            key=lambda row: len(compact_text(row.get("model"))),
            reverse=True,
        )
        for row in rows:
            tokens = _cpu_price_floor_tokens(row.get("model"))
            if tokens and any(token in text for token in tokens):
                return ("cpu", compact_text(row.get("model")))
    if category == "gpu":
        key = _outlier_group_key(category, item)
        if key:
            return key
    if category == "memory":
        return (
            "memory",
            normalize_memory_generation(item.get("generation")),
            _parse_int(item.get("capacity_gb")),
            _parse_int(item.get("module_count")),
        )
    if category == "storage":
        capacity = _parse_int(item.get("capacity_gb"))
        if not capacity and item.get("capacity_tb"):
            capacity = int(_parse_num(item.get("capacity_tb")) * 1000)
        capacity_bucket = int(round(capacity / 1000.0) * 1000) if capacity else 0
        return ("storage", capacity_bucket, _parse_int(item.get("pcie_generation")), floor_cny)
    return (category, floor_cny)


def _price_floor_brand_key(item):
    """Return a neutral brand key for channel-coverage based popularity checks."""
    brand = compact_text(item.get("brand"))
    if brand:
        return brand
    model = str(item.get("model") or "").strip()
    return compact_text(re.split(r"\s+", model, maxsplit=1)[0]) if model else ""


def _is_floorless_volatile_gpu(item):
    chip = compact_text(" ".join(str(item.get(k, "")) for k in ("chip", "model", "id")))
    return "RTX5090" in chip


def _current_market_quotes(items):
    """Return only dated, non-stale quotes for current-market distribution."""
    return [
        item for item in items
        if _query_price_date(item) and not _price_freshness(item).get("price_stale", False)
    ]


def _popular_brand_market_shift(items, floor_cny):
    """Detect a broad below-floor move using high-coverage brands in this candidate set."""
    brand_prices = {}
    for item in _current_market_quotes(items):
        if _is_selected_user_quote(item):
            continue
        brand = _price_floor_brand_key(item)
        price = float(_query_price(item))
        if brand and price > 0:
            brand_prices.setdefault(brand, []).append(price)
    if len(brand_prices) < 2:
        return False, len(brand_prices), 0
    max_listings = max(len(prices) for prices in brand_prices.values())
    coverage_floor = max(2, (max_listings + 1) // 2)
    popular = sorted(
        (
            (brand, prices)
            for brand, prices in brand_prices.items()
            if len(prices) >= coverage_floor
        ),
        key=lambda pair: (-len(pair[1]), pair[0]),
    )[:6]
    if len(popular) < 2:
        return False, len(popular), 0
    below = sum(1 for _, prices in popular if median(prices) < floor_cny)
    return below * 2 > len(popular), len(popular), below


def _clear_price_floor_annotations(item):
    for field in (
        "price_floor_cny", "price_floor_status", "price_floor_gap_percent",
        "price_floor_bottom_decile_cutoff_cny", "price_floor_policy",
        "price_floor_above_candidate_count", "price_floor_warning",
        "_price_floor_rank",
    ):
        item.pop(field, None)


def filter_low_price_outliers(category, results, budget=None, explicit_identity=False):
    """Annotate and downrank low prices; never remove a usable candidate."""
    if _QUERY_CURRENCY != "CNY":
        return results
    if category not in {"cpu", "gpu", "storage", "memory"}:
        return results

    floor_groups = {}
    for item in results:
        _clear_price_floor_annotations(item)
        trusted_floor = _trusted_price_floor(category, item)
        if not trusted_floor:
            if category == "gpu" and _is_floorless_volatile_gpu(item):
                item.update({
                    "price_floor_status": "not_set_volatile",
                    "price_floor_policy": "verify_current_price",
                    "price_floor_warning": "当前不设可信价格地板；" + PRICE_FLOOR_VERIFY_WARNING,
                    "_price_floor_rank": 0,
                })
            continue
        key = _price_floor_group_key(category, item, trusted_floor)
        floor_groups.setdefault(key, []).append(item)
        item["price_floor_cny"] = trusted_floor

    for items in floor_groups.values():
        floor_cny = int(items[0]["price_floor_cny"])
        channel_items = [
            item for item in items
            if not _is_selected_user_quote(item) and _query_price(item) > 0
        ]
        current_market_items = _current_market_quotes(channel_items)
        channel_prices = sorted(float(_query_price(item)) for item in current_market_items)
        bottom_decile_count = max(1, (len(channel_prices) + 9) // 10) if channel_prices else 0
        bottom_decile_cutoff = (
            channel_prices[bottom_decile_count - 1] if bottom_decile_count else None
        )
        above_count = sum(_query_price(item) >= floor_cny for item in current_market_items)
        market_shift, popular_count, popular_below = _popular_brand_market_shift(
            current_market_items, floor_cny
        )
        sparse_above = above_count < PRICE_FLOOR_SPARSE_ABOVE_COUNT
        for item in items:
            price = float(_query_price(item))
            below_floor = bool(price and price < floor_cny)
            stale_below_floor = bool(
                below_floor and _price_freshness(item).get("price_stale", False)
            )
            gap_percent = round(max(0.0, (floor_cny - price) / floor_cny * 100), 1) if price else 0.0
            deep_below_floor = bool(
                below_floor and bottom_decile_cutoff is not None
                and price <= bottom_decile_cutoff
            )
            item["price_floor_above_candidate_count"] = above_count
            item["price_floor_status"] = (
                "deep_below" if deep_below_floor else "below" if below_floor else "at_or_above"
            )
            if below_floor:
                item["price_floor_gap_percent"] = gap_percent
            if bottom_decile_cutoff is not None:
                item["price_floor_bottom_decile_cutoff_cny"] = bottom_decile_cutoff
            item["_price_floor_rank"] = 0
            warnings = []

            if deep_below_floor:
                warnings.append(
                    f"该候选低于可信价格地板，且位于同品类当前报价最低 10% 区间"
                    f"（分界约 CNY {bottom_decile_cutoff:g}）。"
                )
                if explicit_identity:
                    item["price_floor_policy"] = "named_request_exception"
                    warnings.append("仅因用户点名保留为可选项。")
                else:
                    item["price_floor_policy"] = "deep_below_floor_not_recommended"
                    item["_price_floor_rank"] = 2
                    warnings.append("默认装机不推荐。")
            elif below_floor:
                warnings.append("该候选低于可信价格地板。")
                if explicit_identity:
                    item["price_floor_policy"] = "named_request_exception"
                    warnings.append("因用户点名保留为可选项。")
                elif _is_selected_user_quote(item):
                    item["price_floor_policy"] = "user_quote"
                elif stale_below_floor:
                    item["price_floor_policy"] = "stale_below_floor_not_current"
                    item["_price_floor_rank"] = 2
                    warnings.append(
                        "报价已超过14天且低于可信地板，只能作为历史备选，不能用于当前市场下移判断或预算补齐。"
                    )
                elif market_shift:
                    item["price_floor_policy"] = "popular_market_fallback"
                    warnings.append(
                        f"同组高覆盖品牌中有 {popular_below}/{popular_count} 个品牌的中位报价低于地板，允许回退选择。"
                    )
                elif above_count == 0:
                    item["price_floor_policy"] = (
                        "budget_fallback" if budget is not None else "available_candidate_fallback"
                    )
                    warnings.append("当前筛选范围内没有地板之上的可用候选，允许回退选择。")
                else:
                    item["price_floor_policy"] = "prefer_above_floor"
                    item["_price_floor_rank"] = 1
            else:
                item["price_floor_policy"] = "preferred_above_floor"

            if sparse_above:
                warnings.append(f"同组地板之上仅有 {above_count} 个可用商品，样本较少。")
            if below_floor or sparse_above:
                warnings.append(PRICE_FLOOR_VERIFY_WARNING)
            if warnings:
                item["price_floor_warning"] = "".join(warnings)
    return results


def _is_selected_user_quote(item):
    """Return whether the active quote is explicit user evidence in this currency."""
    currency = item.get("user_price_currency", item.get("price_currency"))
    return item.get("price_status") == "user_quote" and currency == _QUERY_CURRENCY


def keep_identity_matches_without_untrusted_prices(category, results, budget=None):
    """Keep exact matches and expose low-price risk instead of suppressing their quote."""
    return filter_low_price_outliers(
        category, results, budget=budget, explicit_identity=True
    )


def color_matches(item, requested):
    """Return whether an item matches the requested color."""
    requested = normalize_color(requested)
    raw_colors = item.get("colors")
    if raw_colors is None:
        raw_colors = item.get("color", "")
    if not isinstance(raw_colors, list):
        raw_colors = [raw_colors]
    normalized = {normalize_color(c) for c in raw_colors if c}
    model_text = str(item.get("model", "")).lower()
    if normalized:
        if (requested == "white" and requested in normalized
                and ("白牌" in model_text or "白金牌" in model_text)
                and not actual_white_in_model(model_text)):
            return False
        return requested in normalized
    if requested == "white":
        model_text = model_text.replace("白牌", "")
    aliases = COLOR_ALIASES.get(requested, {requested})
    return any(alias.lower() in model_text for alias in aliases)


def actual_white_in_model(model_text):
    """Treat PSU efficiency words like 白牌/白金牌 as not being chassis color."""
    cleaned = str(model_text or "").lower().replace("白金牌", "").replace("白牌", "")
    return "white" in cleaned or "白" in cleaned or "雪" in cleaned


def rgb_matches(item, requested):
    """Return whether an item matches the requested RGB preference."""
    if requested is None:
        return True
    model_text = str(item.get("model", "")).upper()
    explicit = item.get("rgb")
    has_no_rgb_text = any(term.upper() in model_text for term in NO_RGB_TERMS)
    has_rgb_text = any(term.upper() in model_text for term in RGB_TERMS)
    if requested is True:
        return bool(explicit) or (has_rgb_text and not has_no_rgb_text)
    if explicit or (has_rgb_text and not has_no_rgb_text):
        return False
    return True


def _matches_max_cooler_height(item, max_height):
    """Match a known total height for air coolers, never AIO pump/radiator thickness."""
    if max_height is None:
        return True
    if str(item.get("type") or "").strip().lower() != "air":
        return False
    if _parse_int(item.get("radiator_mm")) > 0:
        return False
    height = _parse_num(item.get("height_mm"))
    return bool(height and 0 < float(height) <= float(max_height))


def in_current_scope(section, item, include_workstation_gpu=False, max_cooler_height=None):
    """Filter out legacy/irrelevant parts unless caller explicitly opts in."""
    model = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "chip", "gpu_vendor")))
    socket = compact_text(item.get("socket"))

    if section == "cpus":
        if "CELERON" in model or "PENTIUM" in model or "XEON" in model or "至强" in str(item.get("model", "")):
            return False
        if "RYZEN" in model:
            return socket in {"AM5", "SOCKETAM5"}
        if "COREULTRA" in model or "ULTRA" in model:
            return socket in {"LGA1851", "1851"} or any(term in model for term in ("245", "250", "265", "270", "285"))
        return any(f"COREI{tier}1{gen}" in model or f"I{tier}1{gen}" in model
                   for tier in "3579" for gen in "234")

    if section == "motherboards":
        memory = " ".join(str(v) for v in item.get("memory_generations", []))
        return socket in {"LGA1700", "1700", "LGA1851", "1851", "AM5", "SOCKETAM5"} and "DDR3" not in memory.upper()

    if section == "memory":
        # Keep low-budget fallback candidates visible; recommendation rules still prefer 16GB+.
        return normalize_memory_generation(item.get("generation")) in {"DDR4", "DDR5"} and _parse_int(item.get("capacity_gb")) >= 8

    if section == "storage":
        form = str(item.get("form_factor", "")).upper()
        interface = str(item.get("interface", "")).upper()
        generation = _parse_int(item.get("pcie_generation"))
        capacity_tb = _parse_num(item.get("capacity_tb"))
        capacity_gb = _parse_int(item.get("capacity_gb"))
        return (
            "M.2" in form
            and ("PCIE" in interface or "NVME" in interface or generation >= 4)
            and generation >= 4
            and (capacity_tb >= 0.48 or capacity_gb >= 480)
        )

    if section == "gpus":
        if "RTXPRO" in model:
            return bool(include_workstation_gpu and "RTXPRO6000" in model)
        return any(term in model for term in (
            "RTX50", "RTX5050", "RTX5060", "RTX5070", "RTX5080", "RTX5090",
            "RTX3060TI", "RX9060", "RX9070", "ARCB570", "ARCB580",
        ))

    if section == "coolers":
        height = _parse_num(item.get("height_mm"))
        radiator = _parse_int(item.get("radiator_mm"))
        price_is_plausible = _QUERY_CURRENCY != "CNY" or _query_price(item) >= 50
        if max_cooler_height is not None:
            return _matches_max_cooler_height(item, max_cooler_height) and price_is_plausible
        return (bool(radiator) or float(height or 0) >= 120) and price_is_plausible

    if section == "psus":
        return parse_rated_wattage(item) >= 450

    return True


def _matches_explicit_legacy_scope(section, item, requested_socket):
    """Expose only the supported AM4 exception when the caller asks for it."""
    wanted = compact_text(requested_socket)
    if wanted not in {"AM4", "SOCKETAM4"}:
        return False
    model = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model")))
    if section == "cpus":
        return "RYZEN" in model and "X3D" in model
    if section == "motherboards":
        return compact_text(item.get("chipset")) == "B550"
    return False


def _matches_socket(item, requested):
    item_socket = compact_text(item.get("socket"))
    wanted = compact_text(requested)
    return not wanted or bool(item_socket and (wanted in item_socket or item_socket in wanted))


def _matches_memory_gen(section, item, requested):
    wanted = normalize_memory_generation(requested)
    if not wanted:
        return True
    if section == "motherboards":
        return wanted in normalize_memory_generations(item.get("memory_generations"))
    if section == "memory":
        return wanted == normalize_memory_generation(item.get("generation"))
    return True


def _matches_display_output(item, requested):
    """Match verified motherboard display output types for iGPU builds."""
    outputs = normalize_display_outputs(item.get("display_outputs"))
    if compact_text(requested) == "ANY":
        return bool(outputs)
    wanted = normalize_display_output(requested)
    return bool(wanted and wanted in outputs)


def _matches_motherboard_capabilities(item, spec):
    """Fail closed for explicit motherboard capability requirements."""
    if spec.min_pcie_slots is not None:
        count = pcie_physical_slot_count(item)
        if count is None or count < spec.min_pcie_slots:
            return False
    if spec.require_usb4 and verified_usb4_ports(item) <= 0:
        return False
    if spec.require_thunderbolt and verified_thunderbolt_ports(item) <= 0:
        return False
    return True


def _normalize_form_factor(ff):
    text = compact_text(ff)
    mapping = {"MICROATX": "MATX", "M-ATX": "MATX", "MINIITX": "ITX"}
    return mapping.get(text, text)


def _matches_form_factor(section, item, requested):
    wanted = _normalize_form_factor(requested)
    if not wanted:
        return True
    if section == "motherboards":
        return _normalize_form_factor(item.get("form_factor")) == wanted
    if section == "cases":
        supported = [_normalize_form_factor(v) for v in item.get("motherboard_support", [])]
        if wanted == "ITX":
            # ITX requests mean a compact chassis, not any tower that can mount an ITX board.
            return bool(supported) and set(supported).issubset({"ITX", "MINIDTX"})
        compatible = {
            "EATX": {"EATX", "ATX", "MATX", "ITX"},
            "ATX": {"ATX", "MATX", "ITX"},
            "MATX": {"MATX", "ITX"},
            "ITX": {"ITX"},
        }
        return any(wanted in compatible.get(value, {value}) for value in supported)
    if section == "psus":
        psu_form = normalize_psu_form_factor(item.get("form_factor"))
        requested_form = normalize_psu_form_factor(requested)
        return (
            _normalize_form_factor(psu_form)
            == _normalize_form_factor(requested_form)
        )
    return True


def _has_usable_price(item):
    return (
        _query_price_status(item) != "needs_market_quote"
        and _query_price(item) > 0
    )


def _selected_price_view(item):
    """Project one coherent amount/status/date quote in the requested currency."""
    if _QUERY_CURRENCY == "CNY" and item.get("_cny_price_suppressed"):
        return {
            "price": 0,
            "price_currency": "CNY",
            "price_status": "needs_market_quote",
            "price_date": None,
            "price_note": None,
        }
    user_currency = item.get("user_price_currency", item.get("price_currency"))
    user_price = item.get("user_price", item.get("active_price"))
    if user_currency == _QUERY_CURRENCY and item.get("price_status") == "user_quote":
        return {
            "price": _parse_num(user_price),
            "price_currency": _QUERY_CURRENCY,
            "price_status": "user_quote",
            "price_date": item.get("user_price_date", item.get("price_date")),
            "price_note": item.get("user_quote_note"),
        }
    if _QUERY_CURRENCY == "CNY":
        price = _parse_num(item.get("base_price_cny", item.get("price_cny")))
        status = item.get("base_price_status")
        quoted_on = item.get("base_price_date")
        if status is None and item.get("price_status") != "user_quote":
            status = item.get("price_status")
        if quoted_on is None and item.get("price_status") != "user_quote":
            quoted_on = item.get("price_date")
        selected_status = status or ("channel_quote" if price > 0 else "needs_market_quote")
        return {
            "price": 0 if selected_status == "needs_market_quote" else price,
            "price_currency": "CNY",
            "price_status": selected_status,
            "price_date": quoted_on,
            "price_note": None,
        }
    return {
        "price": 0,
        "price_currency": _QUERY_CURRENCY,
        "price_status": "needs_market_quote",
        "price_date": None,
        "price_note": None,
    }


def _query_price(item):
    """Return a price only in the explicitly selected currency; never convert."""
    return _selected_price_view(item)["price"]


def _query_price_status(item):
    return _selected_price_view(item)["price_status"]


def _query_price_date(item):
    return _selected_price_view(item)["price_date"]


def _project_selected_price(item):
    projected = dict(item)
    view = _selected_price_view(item)
    for internal_field in (
        "active_price", "user_price", "user_price_currency", "user_price_date",
        "base_price_status", "base_price_date", "user_quote_note", "_cny_price_suppressed",
        "_catalog_conflict_fields", "_price_floor_rank", USER_CONFIRMED_SPEC_FIELDS,
    ):
        projected.pop(internal_field, None)
    projected.update({
        "price": view["price"] or None,
        "price_currency": view["price_currency"],
        "price_status": view["price_status"],
        "price_date": view["price_date"],
    })
    if view["price_currency"] == "CNY":
        projected["price_cny"] = view["price"] or None
    else:
        projected.pop("price_cny", None)
    if view["price_note"] is not None:
        projected["price_note"] = view["price_note"]
    return projected


def _matches_max_length(section, item, max_length):
    if not max_length:
        return True
    if section == "gpus":
        if "length_mm" in item.get("spec_conflicts", []):
            return False
        length = _parse_num(item.get("length_mm"))
        return bool(length) and length <= _parse_num(max_length)
    if section == "cases":
        limit = _parse_num(item.get("gpu_length_mm"))
        return bool(limit) and limit >= _parse_num(max_length)
    return True


def _matches_resolution(item, requested):
    wanted = normalize_resolution(requested)
    if not wanted:
        return True
    item_resolution = normalize_resolution(item.get("resolution") or item.get("model") or item.get("id"))
    return wanted == item_resolution or wanted in item_resolution


def _matches_min_refresh(item, min_refresh):
    if not min_refresh:
        return True
    refresh = _parse_num(item.get("refresh_rate_hz"))
    return bool(refresh) and refresh >= _parse_num(min_refresh)


def _matches_air_flow(item, requested):
    wanted = compact_text(requested)
    if not wanted or wanted == "ANY":
        return True
    if wanted == "SHOWCASE":
        return _effective_showcase(item)
    item_type = compact_text(item.get("air_flow_type"))
    return wanted == item_type


def _effective_showcase(item):
    """Unify legacy is_showcase and the newer air_flow_type classification."""
    explicit = item.get("is_showcase")
    explicit_true = explicit is True or str(explicit).strip().lower() in ("true", "yes", "1")
    return explicit_true or compact_text(item.get("air_flow_type")) == "SHOWCASE"


def _dust_filter_status(item):
    """Distinguish a searchable hint from a maintainer-verified dust-filter spec."""
    has_filter = item.get("has_dust_filter")
    verified = item.get("dust_filter_verified")
    if has_filter is True:
        return "verified" if verified is True else "needs_verification"
    if has_filter is False:
        return "not_listed"
    return "unknown"


def _matches_optional_bool(item, field, requested):
    if requested is None:
        return True
    value = item.get(field)
    if isinstance(value, bool):
        return value == bool(requested)
    normalized = str(value or "").strip().lower()
    if normalized in ("true", "yes", "1"):
        return bool(requested) is True
    if normalized in ("false", "no", "0"):
        return bool(requested) is False
    return False


def _matches_fan_size(item, fan_size):
    if not fan_size:
        return True
    return _parse_int(item.get("size_mm")) == _parse_int(fan_size)


def _matches_radiator_bundle(item, radiator_bundle):
    if not radiator_bundle:
        return True
    return _parse_int(item.get("radiator_fan_bundle_mm")) == _parse_int(radiator_bundle)


def _matches_fan_type(item, fan_type):
    if not fan_type or fan_type == "any":
        return True
    return str(item.get("fan_type") or "") == fan_type


def _fan_tier(item):
    """Score fans by presentation features and visible planning fields."""
    score = 0
    if item.get("has_screen"):
        score += 10
    if item.get("is_linkable"):
        score += 8
    if item.get("is_radiator_fan_bundle"):
        score += 5
    if item.get("rgb"):
        score += 3
    if _parse_int(item.get("size_mm")) in (120, 140):
        score += 2
    if _parse_int(item.get("pack_count")) >= 3:
        score += 2
    if item.get("fan_type") == "aio_frame":
        score -= 30
    if _query_price(item) and _query_price_date(item):
        score += 1
    return score


def parse_fan_slots_count(value):
    """Best-effort total fan slot count from compact case fan_mounts text."""
    if value in (None, "", [], {}):
        return None
    if isinstance(value, (int, float)):
        number = int(value)
        return number if 1 <= number <= 20 else None
    text = str(value).upper().replace("×", "X")
    if re.fullmatch(r"\s*\d{1,2}\s*", text):
        number = int(text)
        return number if 1 <= number <= 20 else None
    if re.fullmatch(r"\s*\d{2,3}(?:\.\d+)?\s*(?:MM|CM)\s*", text):
        return None
    match = re.search(r"(\d{1,2})\s*个(?:以上)?\s*(?:E-?ATX|ATX|M-?ATX|MATX|ITX|≤|<|$)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d{1,2})\s*(?:风扇位|风扇安装位)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(?:风扇位|风扇安装位)\s*(\d{1,2})", text)
    if match:
        return int(match.group(1))
    total = 0
    found = False
    for segment in re.split(r"[;；。]\s*", text):
        counts = []
        counts.extend(int(m.group(1)) for m in re.finditer(r"(\d{1,2})\s*X\s*(?:120|140|200)", segment))
        counts.extend(int(m.group(1)) for m in re.finditer(r"(?:120|140|200)\s*MM?\s*FAN\s*X\s*(\d{1,2})", segment))
        counts.extend(int(m.group(1)) for m in re.finditer(r"(?:120|140|200)\s*风扇\s*X\s*(\d{1,2})", segment))
        if counts:
            total += max(counts)
            found = True
    return total if found else None


def should_display_fan_mounts(value):
    """Only show raw fan_mounts when it looks like fan placement text, not dimensions."""
    if value in (None, "", [], {}):
        return False
    text = str(value).upper().replace("×", "X")
    if parse_fan_slots_count(text):
        return True
    if re.fullmatch(r"\s*\d{2,3}(?:\.\d+)?\s*(?:MM|CM)\s*", text):
        return False
    return bool(re.search(r"风扇|FAN|TOP|FRONT|REAR|BOTTOM|SIDE|前|顶|后|底|侧", text))


def radiator_fan_slots(radiator_mm):
    """Common AIO radiator fan occupancy by nominal radiator class."""
    try:
        size = int(radiator_mm or 0)
    except (TypeError, ValueError):
        return None
    if size == 480:
        return 4
    if size in (360, 420):
        return 3
    if size in (240, 280):
        return 2
    if size in (120, 140):
        return 1
    return None


GPU_CHIP_SUFFIXES = ("DV2", "V2", "SUPER", "GRE", "TI", "XT", "D")


def _gpu_chip_suffix_conflicts(wanted, rest):
    """Avoid fuzzy chip matches such as RTX5070 matching RTX5070Ti."""
    for suffix in GPU_CHIP_SUFFIXES:
        if rest.startswith(suffix) and not wanted.endswith(suffix):
            return True
    return False


def _matches_gpu_chip(item, requested):
    """Match GPU chip tokens while preserving Ti/D/V2/XT/GRE distinctions."""
    wanted = compact_text(requested)
    if not wanted:
        return True
    structured_chip = compact_text(item.get("chip"))
    if structured_chip == wanted:
        return True
    # Prefer the structured chip fact. Imported IDs may end in a random
    # hexadecimal suffix whose digits can accidentally satisfy broad filters
    # such as ``--gpu-chip 50``.
    candidate_texts = (structured_chip,) if structured_chip else (
        compact_text(item.get("model")),
    )
    for text in candidate_texts:
        start = 0
        while True:
            pos = text.find(wanted, start)
            if pos < 0:
                break
            rest = text[pos + len(wanted):]
            if not _gpu_chip_suffix_conflicts(wanted, rest):
                return True
            start = pos + 1
    return False


def _sort_results(results, sort, category=None):
    """Sort with missing prices last and keep case sorting consistent."""
    for item in results:
        item.update(_price_freshness(item))
    if sort == "tier":
        results.sort(key=lambda x: _tier_sort_key(category, x))
    elif sort in ("desc", "price-desc"):
        results.sort(key=lambda x: (
            x.get("_price_floor_rank", 0), _query_price(x) <= 0,
            -_query_price(x), x.get("id", ""),
        ))
    else:
        results.sort(key=lambda x: (
            x.get("_price_floor_rank", 0), _query_price(x) <= 0,
            _query_price(x), x.get("id", ""),
        ))


def _price_freshness(item, as_of=None):
    """Return a non-blocking 14-day freshness annotation for a priced row."""
    raw_date = _query_price_date(item)
    if not _query_price(item) or not raw_date:
        return {}
    try:
        quoted_on = date.fromisoformat(str(raw_date))
    except ValueError:
        return {}
    reference = as_of or date.today()
    age_days = max(0, (reference - quoted_on).days)
    return {
        "price_age_days": age_days,
        "price_stale": age_days > PRICE_STALE_AFTER_DAYS,
    }


def _matches_common_candidate(item, spec):
    if not _matches_identity(item, model=spec.model, item_id=spec.item_id):
        return False
    if spec.has_price_only and not _has_usable_price(item) and not (spec.model or spec.item_id):
        return False
    if spec.budget and _query_price(item) and _query_price(item) > spec.budget:
        return False
    return True


def _query_cases(spec):
    results = []
    for item in load_cases().get("cases", []):
        if not _matches_common_candidate(item, spec):
            continue
        if not spec.include_legacy and not item.get("motherboard_support") and not (spec.model or spec.item_id):
            continue
        if not _matches_form_factor("cases", item, spec.form_factor):
            continue
        if not _matches_max_length("cases", item, spec.max_length):
            continue
        if spec.color and not color_matches(item, spec.color):
            continue
        if spec.showcase is True and not _effective_showcase(item):
            continue
        if spec.air_flow and not _matches_air_flow(item, spec.air_flow):
            continue
        if not _matches_optional_bool(item, "has_dust_filter", spec.dust_filter):
            continue
        results.append(item)
    _sort_results(results, spec.sort, "case")
    return [
        _summarize_case(item)
        for item in _finalize_sorted_results(results, spec.sort, "case")[:spec.limit]
    ]


def _query_displays(spec):
    results = []
    for item in load_displays().get("displays", []):
        if not _matches_common_candidate(item, spec):
            continue
        if not _matches_resolution(item, spec.resolution):
            continue
        if not _matches_min_refresh(item, spec.min_refresh):
            continue
        if spec.color and not color_matches(item, spec.color):
            continue
        result = dict(item)
        if not result.get("brand"):
            result["brand"] = infer_display_brand(result)
        results.append(result)
    _sort_results(results, spec.sort, "display")
    return _finalize_sorted_results(results, spec.sort, "display")[:spec.limit]


def _query_fans(spec):
    results = []
    for item in load_components().get("fans", []):
        if not _matches_common_candidate(item, spec):
            continue
        if is_fan_accessory(item) and spec.fan_type != "accessory":
            continue
        explicit_aio_frame = spec.fan_type == "aio_frame"
        if (
            not spec.include_legacy
            and item.get("default_recommend") is False
            and not explicit_aio_frame
            and not (spec.model or spec.item_id)
        ):
            continue
        if spec.color and not color_matches(item, spec.color):
            continue
        if not rgb_matches(item, spec.rgb):
            continue
        if not _matches_fan_size(item, spec.fan_size):
            continue
        if spec.blade_direction and spec.blade_direction != "any" and item.get("blade_direction") != spec.blade_direction:
            continue
        if not _matches_optional_bool(item, "is_linkable", spec.linkable):
            continue
        if not _matches_optional_bool(item, "has_screen", spec.screen):
            continue
        if not _matches_radiator_bundle(item, spec.radiator_bundle):
            continue
        if not _matches_fan_type(item, spec.fan_type):
            continue
        results.append(item)
    _sort_results(results, spec.sort, "fan")
    return _finalize_sorted_results(results, spec.sort, "fan")[:spec.limit]


def _query_core_components(spec):
    lib = load_components()
    categories_to_search = [CATEGORIES[spec.category]] if spec.category and spec.category in CORE_CATEGORIES \
        else [CATEGORIES[k] for k in CORE_CATEGORIES if k != "case"]
    results = []
    for sec in categories_to_search:
        specific_gpu_model = sec == "gpus" and _is_specific_gpu_model_query(
            spec.model, lib.get(sec, [])
        )
        for item in lib.get(sec, []):
            if not _matches_common_candidate(item, spec):
                continue
            explicit_gpu_chip = sec == "gpus" and bool(
                _gpu_chip_only_model_query(spec.gpu_chip)
            )
            explicit_scope_bypass = bool(
                spec.item_id
                or explicit_gpu_chip
                or (specific_gpu_model if sec == "gpus" else spec.model)
            )
            if not spec.include_legacy and not explicit_scope_bypass:
                in_scope = in_current_scope(
                    sec,
                    item,
                    include_workstation_gpu=spec.include_workstation_gpu,
                    max_cooler_height=spec.max_cooler_height,
                )
                if not in_scope and not _matches_explicit_legacy_scope(sec, item, spec.socket):
                    continue
            if spec.platform:
                item_platform = item.get("platform", "").lower()
                if item_platform and spec.platform.lower() not in item_platform:
                    continue
                if sec == "coolers":
                    exclusive_platform = infer_cooler_exclusive_platform(item)
                    if exclusive_platform and exclusive_platform != spec.platform.lower():
                        continue
            if spec.socket and sec in ("cpus", "motherboards") and not _matches_socket(item, spec.socket):
                continue
            if (
                sec == "cpus"
                and spec.integrated_graphics is not None
                and infer_cpu_integrated_graphics(item) is not spec.integrated_graphics
            ):
                continue
            if spec.chipset and sec == "motherboards" and compact_text(spec.chipset) not in compact_text(item.get("chipset")):
                continue
            if sec == "motherboards" and spec.display_output and not _matches_display_output(item, spec.display_output):
                continue
            if sec == "motherboards" and not _matches_motherboard_capabilities(item, spec):
                continue
            if spec.memory_gen and not _matches_memory_gen(sec, item, spec.memory_gen):
                continue
            if spec.form_factor and not _matches_form_factor(sec, item, spec.form_factor):
                continue
            if not _matches_max_length(sec, item, spec.max_length):
                continue
            if sec == "coolers" and not _matches_max_cooler_height(item, spec.max_cooler_height):
                continue
            if sec == "gpus":
                if spec.gpu_chip and not _matches_gpu_chip(item, spec.gpu_chip):
                    continue
                if spec.min_vram and _parse_int(infer_gpu_vram(item)) < _parse_int(spec.min_vram):
                    continue
                if spec.gpu_cooling and not (spec.model or spec.item_id) and infer_gpu_cooling(item) != spec.gpu_cooling:
                    continue
            if sec == "memory" and spec.min_capacity and _parse_int(item.get("capacity_gb")) < _parse_int(spec.min_capacity):
                continue
            if sec == "storage" and spec.min_capacity and _parse_int(item.get("capacity_gb")) < _parse_int(spec.min_capacity):
                continue
            if (
                sec == "storage"
                and not (spec.model or spec.item_id or spec.pcie_generation)
                and _parse_int(item.get("pcie_generation")) >= 5
            ):
                continue
            if sec == "storage" and spec.pcie_generation and _parse_int(item.get("pcie_generation")) != _parse_int(spec.pcie_generation):
                continue
            if sec == "storage" and not _matches_optional_bool(item, "dram_cache", spec.dram_cache):
                continue
            if (sec in ("memory", "storage") and spec.max_capacity
                    and _parse_int(item.get("capacity_gb")) > _capacity_upper_bound(sec, spec.max_capacity)):
                continue
            if spec.color and not color_matches(item, spec.color):
                continue
            if not rgb_matches(item, spec.rgb):
                continue
            results.append(item)

    if spec.category:
        if spec.model or spec.item_id:
            results = keep_identity_matches_without_untrusted_prices(
                spec.category, results, budget=spec.budget
            )
        else:
            results = filter_low_price_outliers(spec.category, results, budget=spec.budget)
            if spec.category == "gpu":
                results = filter_ambiguous_gpu_skus(results, lib.get("gpus", []))
    _sort_results(results, spec.sort, spec.category)
    return _finalize_sorted_results(results, spec.sort, spec.category)[:spec.limit]


def query(category=None, budget=None, platform=None, color=None,
          rgb=None, limit=DEFAULT_QUERY_LIMIT, has_price_only=True, showcase=None,
          include_legacy=False, sort="asc", socket=None, chipset=None,
          memory_gen=None, form_factor=None, max_length=None, max_cooler_height=None,
          gpu_cooling="air",
          gpu_chip=None, min_vram=None, min_capacity=None, include_workstation_gpu=False,
          resolution=None, min_refresh=None, air_flow=None, dust_filter=None,
          fan_size=None, blade_direction=None, linkable=None, screen=None,
          radiator_bundle=None, fan_type=None, model=None, item_id=None,
          max_capacity=None, pcie_generation=None, dram_cache=None,
          integrated_graphics=None, display_output=None, min_pcie_slots=None,
          require_usb4=False, require_thunderbolt=False):
    """查询配件。返回匹配的配件列表。"""
    spec = QuerySpec(
        category=category,
        budget=budget,
        platform=platform,
        color=color,
        rgb=rgb,
        limit=limit,
        has_price_only=has_price_only,
        showcase=showcase,
        include_legacy=include_legacy,
        sort=sort,
        socket=socket,
        chipset=chipset,
        memory_gen=memory_gen,
        form_factor=form_factor,
        max_length=max_length,
        max_cooler_height=max_cooler_height,
        gpu_cooling=None if gpu_cooling == "any" else gpu_cooling,
        gpu_chip=gpu_chip,
        min_vram=min_vram,
        min_capacity=min_capacity,
        include_workstation_gpu=include_workstation_gpu,
        resolution=resolution,
        min_refresh=min_refresh,
        air_flow=air_flow,
        dust_filter=dust_filter,
        fan_size=fan_size,
        blade_direction=blade_direction,
        linkable=linkable,
        screen=screen,
        radiator_bundle=radiator_bundle,
        fan_type=fan_type,
        model=model,
        item_id=item_id,
        max_capacity=max_capacity,
        pcie_generation=pcie_generation,
        dram_cache=dram_cache,
        integrated_graphics=integrated_graphics,
        display_output=display_output,
        min_pcie_slots=min_pcie_slots,
        require_usb4=require_usb4,
        require_thunderbolt=require_thunderbolt,
    )
    if category == "case":
        return _query_cases(spec)
    if category in DISPLAY_CATEGORIES:
        return _query_displays(spec)
    if category in FAN_CATEGORIES:
        return _query_fans(spec)
    return _query_core_components(spec)


def _gpu_tier(item):
    """Return GPU chip tier rank (higher = better). 0 for non-GPU or unknown."""
    chip = compact_text(" ".join(str(item.get(k, "")) for k in ("chip", "model", "id")))
    for key, tier in GPU_TIERS:
        if key in chip:
            return tier
    return 0


def _cpu_tier(item):
    """Return CPU tier rank for budget-near choices. Higher is better."""
    text = compact_text(" ".join(str(item.get(k, "")) for k in ("brand", "model", "id")))
    if "ULTRA9270" in text:
        return 820
    if "ULTRA9285" in text:
        return 810
    if "ULTRA7270" in text:
        return 830
    if "ULTRA7265" in text:
        return 780
    if "ULTRA5250" in text:
        return 735
    if "ULTRA5245" in text:
        return 700
    if "ULTRA5235" in text:
        return 680
    if "ULTRA5230" in text or "ULTRA5225" in text:
        return 610

    amd_scores = (
        ("9950X3D2", 920), ("9950X3D", 900), ("9850X3D", 890),
        ("9800X3D", 880), ("7950X3D", 800), ("7800X3D", 760),
        ("9950X", 830), ("9700X", 760), ("9900X", 730),
        ("5800X3D", 735), ("5700X3D", 710), ("9600X", 660),
        ("5500X3D", 620), ("7500F", 450),
    )
    for key, score in amd_scores:
        if key in text:
            return score

    intel_scores = (
        ("I914900", 900), ("I914700", 860), ("I714700K", 835),
        ("I714700", 820), ("I714900", 820),
        ("I514600", 760), ("I512600K", 725), ("I512600", 710),
        ("I514490", 705), ("I514400", 690),
        ("I513490", 680), ("I513400", 670),
        ("I512490", 625), ("I512400", 600),
        ("I314100", 420), ("I313100", 380), ("I312100", 320),
    )
    for key, score in intel_scores:
        if key in text:
            return score
    return 0


def _motherboard_tier(item):
    """Return motherboard chipset tier rank (higher = better)."""
    text = compact_text(" ".join(str(item.get(k, "")) for k in ("chipset", "model", "id")))
    score = candidate_signal_score(
        item,
        primary=MOTHERBOARD_PRIMARY_SIGNALS,
        secondary=MOTHERBOARD_SERIES_SIGNALS,
        common=MOTHERBOARD_COMMON_SIGNALS,
    )
    for key, tier in MOTHERBOARD_TIERS:
        if key in text:
            return tier * 100 + score
    return score


def _storage_read_speed(item):
    """Infer advertised sequential read speed from common model text."""
    text = str(item.get("model", "")).upper()
    patterns = (
        r"读速\s*(\d{3,5})\s*MB",
        r"读取\s*(\d{3,5})\s*MB",
        r"(\d{3,5})\s*MB/S",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return 0


def _storage_tier(item):
    """Score SSDs by positive adoption and visible specification signals."""
    score = 0
    score += candidate_signal_score(
        item,
        primary=STORAGE_PRIMARY_SIGNALS,
        common=STORAGE_COMMON_SIGNALS,
    )
    generation = _parse_int(item.get("pcie_generation"))
    if generation >= 5:
        score += 5
    elif generation >= 4:
        score += 3
    speed = _storage_read_speed(item)
    if speed >= 7000:
        score += 4
    elif speed >= 5000:
        score += 2
    elif speed >= 3500:
        score += 1
    if "TLC" in compact_text(item_text(item)):
        score += 3
    capacity_gb = _parse_int(item.get("capacity_gb"))
    if capacity_gb >= 4000:
        score += 2
    elif capacity_gb >= 2000:
        score += 1
    if _query_price(item) and _query_price_date(item):
        score += 1
    return score


def _memory_timing_value(item):
    """Infer CL/timing headline value from structured timing or model text."""
    text = str(item.get("timing") or item.get("model", "")).upper()
    match = re.search(r"(?:CL|C)\s*(\d{2})", text)
    return int(match.group(1)) if match else 0


def _memory_tier(item):
    """Score memory by positive adoption and balanced DDR4/DDR5 parameters."""
    score = 0
    if has_candidate_signal(item, MEMORY_ADOPTION_SIGNALS):
        score += 8
    freq = _parse_int(item.get("frequency_mt"))
    if 6000 <= freq <= 6400:
        score += 4
    elif freq >= 6800:
        score += 3
    elif freq >= 5600:
        score += 2
    elif freq >= 3200:
        score += 1
    timing = _memory_timing_value(item)
    if timing and timing <= 30:
        score += 3
    elif timing and timing <= 36:
        score += 2
    module_count = _parse_int(item.get("module_count"))
    if module_count == 2:
        score += 4
    elif module_count > 2:
        score -= 3
    price = _parse_int(_query_price(item)) if _QUERY_CURRENCY == "CNY" else 0
    generation = normalize_memory_generation(item.get("generation"))
    capacity_gb = _parse_int(item.get("capacity_gb"))
    if generation == "DDR5" and freq >= 5600 and capacity_gb >= 32 and 0 < price < 1300:
        score -= 8
    if generation == "DDR5" and freq >= 5600 and capacity_gb >= 64 and 0 < price < 2500:
        score -= 8
    if _query_price(item) and _query_price_date(item):
        score += 1
    return score


def _cooler_tier(item):
    """Score coolers by heat capacity and visible adoption signals."""
    score = candidate_signal_score(item, primary=COOLER_ADOPTION_SIGNALS)
    profile = infer_cooler_thermal_profile(item)
    radiator = _parse_int(item.get("radiator_mm"))
    if profile.rank == THERMAL_HIGH:
        score += 22
        if radiator >= 420:
            score += 2
    elif profile.rank == THERMAL_STRONG:
        score += 14
    elif profile.rank == THERMAL_MAINSTREAM:
        score += 5
    elif profile.rank == THERMAL_LOW:
        score -= 3
    text = compact_text(item_text(item))
    height = float(_parse_num(item.get("height_mm")))
    if 145 <= height <= 165:
        score += 2
    if any(token in text for token in ("LCD", "数显", "屏")):
        score += 2
    if _query_price(item) and _query_price_date(item):
        score += 1
    return score


def _psu_tier(item):
    """Score PSUs by platform, wattage, efficiency and visible adoption signals."""
    score = candidate_signal_score(
        item,
        primary=PSU_PRIMARY_SIGNALS,
        common=PSU_COMMON_SIGNALS,
    )
    wattage = parse_rated_wattage(item)
    if wattage >= 1200:
        score += 8
    elif wattage >= 1000:
        score += 7
    elif wattage >= 850:
        score += 6
    elif wattage >= 750:
        score += 4
    elif wattage >= 650:
        score += 2
    text = compact_text(item_text(item))
    if any(token in text for token in ("ATX31", "ATX30", "PCIE5", "PCIE50", "12V2X6", "12VHPWR")):
        score += 5
    if item.get("native_16pin_gpu_power"):
        score += 4
    if any(token in text for token in ("钛金", "TITANIUM")):
        score += 4
    elif any(token in text for token in ("白金", "PLATINUM")):
        score += 3
    elif any(token in text for token in ("金牌", "GOLD")):
        score += 2
    if any(token in text for token in ("全模", "全模组", "FULLMODULAR")):
        score += 2
    if any(token in text for token in ("白牌", "WHITE牌".upper())):
        score -= 4
    if _query_price(item) and _query_price_date(item):
        score += 1
    return score


def _tier_sort_key(category, item):
    """Category-aware tier sort used by the progressive query helper."""
    price = _query_price(item)
    price_key = (item.get("_price_floor_rank", 0), price <= 0, price, item.get("id", ""))
    if category == "cpu":
        return (-_cpu_tier(item), *price_key)
    if category == "gpu":
        return (-_gpu_tier(item), *price_key)
    if category == "mb":
        return (-_motherboard_tier(item), *price_key)
    if category == "storage":
        return (-_storage_tier(item), *price_key)
    if category == "memory":
        return (-_memory_tier(item), *price_key)
    if category == "cooler":
        return (-_cooler_tier(item), *price_key)
    if category == "psu":
        return (-_psu_tier(item), *price_key)
    if category == "fan":
        return (-_fan_tier(item), *price_key)
    return (0, *price_key)


def query_all(budget=None, platform=None, color=None, rgb=None, limit=5,
              has_price_only=True, include_legacy=False, sort="asc", socket=None,
              chipset=None, memory_gen=None, form_factor=None, max_length=None,
              gpu_cooling="air", gpu_chip=None, min_vram=None, min_capacity=None,
              include_workstation_gpu=False, showcase=None, air_flow=None, dust_filter=None,
              model=None, item_id=None, max_capacity=None, integrated_graphics=None,
              display_output=None, min_pcie_slots=None, require_usb4=False,
              require_thunderbolt=False):
    """Return core PC candidates grouped by category for smoke/progressive disclosure."""
    grouped = {}
    for category in CORE_CATEGORIES:
        grouped[category] = query(
            category=category,
            budget=budget,
            platform=platform,
            color=color,
            rgb=rgb,
            limit=limit,
            has_price_only=has_price_only,
            include_legacy=include_legacy,
            sort=sort,
            socket=socket,
            chipset=chipset,
            memory_gen=memory_gen,
            form_factor=form_factor,
            max_length=max_length,
            gpu_cooling=gpu_cooling,
            gpu_chip=gpu_chip,
            min_vram=min_vram,
            min_capacity=min_capacity,
            max_capacity=max_capacity,
            model=model,
            item_id=item_id,
            include_workstation_gpu=include_workstation_gpu,
            integrated_graphics=integrated_graphics if category == "cpu" else None,
            display_output=display_output if category == "mb" else None,
            min_pcie_slots=min_pcie_slots if category == "mb" else None,
            require_usb4=require_usb4 if category == "mb" else False,
            require_thunderbolt=require_thunderbolt if category == "mb" else False,
            showcase=showcase if category == "case" else None,
            air_flow=air_flow if category == "case" else None,
            dust_filter=dust_filter if category == "case" else None,
        )
    return grouped


def _summarize_case(case):
    """Extract summary fields from a case record."""
    fan_mounts = case.get("fan_mounts")
    price_view = _selected_price_view(case)
    return {
        "id": case.get("id", ""),
        "brand": case.get("brand", ""),
        "model": case.get("model", ""),
        "price": price_view["price"] or None,
        "price_currency": _QUERY_CURRENCY,
        "price_cny": (price_view["price"] or None) if _QUERY_CURRENCY == "CNY" else None,
        "base_price_cny": case.get("base_price_cny"),
        "price_status": price_view["price_status"],
        "price_date": price_view["price_date"],
        "price_note": price_view["price_note"],
        **_price_freshness(case),
        "colors": case.get("colors", case.get("color", "")),
        "motherboard_support": case.get("motherboard_support", []),
        "gpu_length_mm": case.get("gpu_length_mm"),
        "cpu_cooler_height_mm": case.get("cpu_cooler_height_mm"),
        "radiator_support": case.get("radiator_support", []),
        "fan_mounts": fan_mounts,
        "fan_slots_count": parse_fan_slots_count(fan_mounts),
        "psu_support": case.get("psu_support", ["ATX"]),
        "psu_length_mm": case.get("psu_length_mm"),
        "psu_length_recommended_mm": case.get("psu_length_recommended_mm"),
        "psu_length_condition": case.get("psu_length_condition"),
        "air_flow_type": case.get("air_flow_type", ""),
        "has_dust_filter": case.get("has_dust_filter"),
        "dust_filter_status": _dust_filter_status(case),
        "is_showcase": _effective_showcase(case),
    }


def summarize(item, category=None):
    """Extract only summary fields for progressive disclosure."""
    item = _project_selected_price(item)
    fields = SUMMARY_FIELDS_BY_CATEGORY.get(category, SUMMARY_BASE_FIELDS)
    summary = {k: item.get(k) for k in fields if item.get(k) is not None}
    if category == "gpu" and infer_gpu_cooling(item) == "liquid":
        summary["gpu_cooling"] = "liquid"
        summary["gpu_radiator_required"] = True
    if category == "mb":
        slot_count = pcie_physical_slot_count(item)
        if slot_count is not None:
            summary["pcie_physical_slots"] = slot_count
    return summary


def display_extra(category, item):
    """Keep plain-text summaries compact while exposing the key routing field."""
    if category == "cpu":
        integrated_graphics = infer_cpu_integrated_graphics(item)
        if integrated_graphics is True:
            return "iGPU=yes"
        if integrated_graphics is False:
            return "iGPU=no"
    if category == "mb" and item.get("chipset"):
        parts = [f"chipset={item.get('chipset')}"]
        if item.get("display_outputs"):
            parts.append("display=" + "/".join(str(value) for value in item.get("display_outputs")))
        slot_count = pcie_physical_slot_count(item)
        if slot_count is not None:
            parts.append(f"PCIe-slots={slot_count}")
        if verified_usb4_ports(item):
            parts.append(f"USB4={verified_usb4_ports(item)}")
        if verified_thunderbolt_ports(item):
            parts.append(f"TB{item.get('thunderbolt_version')}={verified_thunderbolt_ports(item)}")
        return " ".join(parts)
    if category == "gpu" and item.get("chip"):
        parts = [f"chip={item.get('chip')}"]
        if item.get("vram_gb"):
            parts.append(f"{item.get('vram_gb')}GB")
        if item.get("memory_bus_bit"):
            parts.append(f"{item.get('memory_bus_bit')}-bit")
        if infer_gpu_cooling(item) == "liquid":
            parts.append("liquid-gpu")
        return " ".join(parts)
    if category == "psu" and item.get("wattage_w"):
        connector = " native16pin" if item.get("native_16pin_gpu_power") else ""
        form = f" {item.get('form_factor')}" if item.get("form_factor") else ""
        length = f" {item.get('length_mm')}mm" if item.get("length_mm") else ""
        return f"{item.get('wattage_w')}W{form}{length}{connector}"
    if category == "memory" and item.get("frequency_mt"):
        timing = f" {item.get('timing')}" if item.get("timing") else ""
        return f"{item.get('generation','')} {item.get('frequency_mt')}MT/s{timing}"
    if category == "storage" and item.get("capacity_tb"):
        return f"{item.get('capacity_tb')}TB {item.get('interface','')}"
    if category == "cooler":
        if item.get("type") == "liquid" and item.get("radiator_mm"):
            return f"liquid {item.get('radiator_mm')}mm"
        if item.get("height_mm"):
            return f"{item.get('type','air')} {item.get('height_mm')}mm"
    if category == "case":
        parts = []
        if item.get("gpu_length_mm"):
            parts.append(f"GPU≤{item.get('gpu_length_mm')}mm")
        if item.get("cpu_cooler_height_mm"):
            parts.append(f"CPU≤{item.get('cpu_cooler_height_mm')}mm")
        if item.get("radiator_support"):
            parts.append("rad=" + "/".join(str(x) for x in item.get("radiator_support")))
        if item.get("fan_slots_count"):
            parts.append(f"fans={item.get('fan_slots_count')}")
        elif should_display_fan_mounts(item.get("fan_mounts")):
            parts.append(f"fans={item.get('fan_mounts')}")
        if item.get("psu_support"):
            parts.append("PSU=" + "/".join(str(x) for x in item.get("psu_support")))
        if item.get("psu_length_mm"):
            parts.append(f"PSU≤{item.get('psu_length_mm')}mm")
        if item.get("air_flow_type"):
            parts.append(f"airflow={item.get('air_flow_type')}")
        dust_status = item.get("dust_filter_status") or _dust_filter_status(item)
        if dust_status == "verified":
            parts.append("dust_filter=verified")
        elif dust_status == "needs_verification":
            parts.append("dust_filter=verify")
        elif dust_status == "not_listed":
            parts.append("dust_filter=not-listed")
        return " ".join(parts)
    if category == "fan":
        parts = []
        if item.get("size_mm"):
            parts.append(f"{item.get('size_mm')}mm")
        if item.get("pack_count"):
            parts.append(f"x{item.get('pack_count')}")
        if item.get("blade_direction"):
            direction = "反页" if item.get("blade_direction") == "reverse" else "正页"
            parts.append(direction)
        parts.append("RGB" if item.get("rgb") else "无光")
        if item.get("is_linkable"):
            parts.append("积木/串联")
        if item.get("has_screen"):
            parts.append("带屏")
        if item.get("radiator_fan_bundle_mm"):
            parts.append(f"{item.get('radiator_fan_bundle_mm')}一体式风扇")
        if item.get("fan_type") == "aio_frame":
            parts.append("无风扇水冷框架")
        return " ".join(parts)
    if category in DISPLAY_CATEGORIES:
        parts = []
        if item.get("resolution"):
            parts.append(str(item.get("resolution")))
        if item.get("size_inch"):
            parts.append(f"{item.get('size_inch')}英寸")
        if item.get("refresh_rate_hz"):
            parts.append(f"{item.get('refresh_rate_hz')}Hz")
        return " ".join(parts)
    return ""


def _build_parser():
    parser = argparse.ArgumentParser(description="配件查询工具 (渐进式披露)", allow_abbrev=False)
    parser.add_argument("--category", choices=list(CATEGORIES.keys()) + ["all"],
                        default="all", help="配件品类")
    parser.add_argument("--budget", type=int, help="单品价格上限 (元)，不是整机预算")
    parser.add_argument("--overlay", action="append", default=[], help="显式用户 overlay JSON；可重复，后传报价优先")
    parser.add_argument("--currency", choices=["CNY", "USD", "EUR", "GBP", "JPY", "TWD"], default="CNY",
                        help="价格筛选/预算/排序币种，不换算、不混算；默认 CNY")
    parser.add_argument("--model", help="型号关键词过滤，用于定位用户给出的现有配件")
    parser.add_argument("--id", dest="item_id", help="精确库内 ID 过滤")
    parser.add_argument("--platform", help="平台过滤 (intel/amd)")
    parser.add_argument(
        "--integrated-graphics",
        "--igpu",
        choices=["yes", "no"],
        help="CPU 核显过滤；无独显整机使用 yes，未知核显状态不会进入结果",
    )
    parser.add_argument(
        "--display-output",
        "--video-output",
        choices=["any", "HDMI", "DisplayPort", "DP", "VGA", "D-Sub", "DVI", "USB-C", "Thunderbolt"],
        help="主板已核实视频输出过滤（any/HDMI/DisplayPort/VGA）；无独显整机至少使用 any",
    )
    parser.add_argument(
        "--min-pcie-slots",
        type=int,
        help="主板已核实物理 PCIe 插槽下限；独显加采集卡/扩展卡时通常至少为 2",
    )
    parser.add_argument(
        "--require-usb4",
        action="store_true",
        help="只返回已核实具有后置 USB4 能力的主板；普通 USB-C 不会命中",
    )
    parser.add_argument(
        "--require-thunderbolt",
        action="store_true",
        help="只返回已核实具有后置雷电端口的主板；扩展针脚不会命中",
    )
    parser.add_argument("--socket", help="CPU/主板 socket 过滤 (LGA1700/AM5/LGA1851)")
    parser.add_argument("--chipset", help="主板芯片组过滤 (B760/B850/X870/Z890 等)")
    parser.add_argument("--memory-gen", help="内存代际过滤 (DDR4/DDR5)，作用于主板和内存")
    parser.add_argument(
        "--form-factor",
        help="主板/机箱/电源规格过滤；case+ITX 只返回紧凑机箱，PSU 按 ATX/SFX/SFX-L 精确匹配",
    )
    parser.add_argument("--max-length", type=int,
                        help="显卡长度上限；查询机箱时表示需要容纳的显卡长度 (mm)")
    parser.add_argument(
        "--max-cooler-height",
        type=int,
        help="CPU 风冷散热器总高度上限 (mm)；ITX/小机箱明确限高时使用",
    )
    parser.add_argument("--gpu-cooling", choices=["air", "liquid", "any"], default="air",
                        help="显卡散热形态过滤；默认 air，用户明确要水冷显卡时使用 liquid，排查全量候选时使用 any")
    parser.add_argument("--gpu-chip", "--chip", dest="gpu_chip",
                        help="显卡芯片过滤 (RTX5060Ti/RTX5080/RTX5090D V2 等)；--chip 是兼容别名")
    parser.add_argument("--min-vram", type=int,
                        help="显卡最低显存容量 (GB)，例如明确要 RTX 5060 Ti 16GB 时用 --min-vram 16")
    parser.add_argument("--min-capacity", type=int,
                        help="内存最低总容量或 SSD 最低容量 (GB)；64GB 内存用 64，2TB SSD 用 2000")
    parser.add_argument("--max-capacity", type=int,
                        help="内存或 SSD 最高容量 (GB)；明确要 1TB SSD 时与 --min-capacity 1000 同用")
    parser.add_argument("--pcie-generation", type=int, choices=[3, 4, 5],
                        help="SSD PCIe 代际过滤；Gen5 默认不进入普通候选，明确需要时用 5")
    parser.add_argument("--dram-cache", choices=["yes", "no"],
                        help="SSD 是否已确认独立 DRAM 缓存；yes 不包含字段未知条目")
    parser.add_argument("--color", help="颜色过滤 (black/white)")
    parser.add_argument("--rgb", choices=["yes", "no"], help="RGB 过滤")
    parser.add_argument("--showcase", action="store_true", help="只返回海景房机箱")
    parser.add_argument("--air-flow", choices=["airflow", "mesh", "showcase", "standard", "any"],
                        help="机箱风道类型过滤；养宠/风道优先可用 airflow 或 mesh")
    parser.add_argument(
        "--dust-filter",
        choices=["yes", "no"],
        help="机箱防尘/防毛候选过滤；yes 仍需按 dust_filter_status 复核具体滤网规格",
    )
    parser.add_argument("--fan-size", type=int, help="风扇尺寸过滤 (120/140 等 mm)")
    parser.add_argument("--blade-direction", choices=["normal", "reverse", "any"],
                        help="风扇正反页过滤: normal=正页/正叶, reverse=反页/反叶")
    parser.add_argument("--linkable", choices=["yes", "no"], help="风扇是否积木/串联/磁吸")
    parser.add_argument("--screen", choices=["yes", "no"], help="风扇是否带屏幕/数显")
    parser.add_argument("--radiator-bundle", type=int, help="一体式/冷排风扇套装尺寸 (240/360/420/480)")
    parser.add_argument("--fan-type", choices=["case_fan", "radiator_fan_pack", "aio_frame", "any"],
                        help="风扇类型过滤；aio_frame 为无风扇水冷框架，默认不推荐")
    parser.add_argument("--resolution", help="显示器分辨率过滤 (1080p/1K/1440p/2K/2160p/4K)")
    parser.add_argument("--min-refresh", type=int, help="显示器最低刷新率 (Hz)")
    parser.add_argument("--sort", choices=["asc", "desc", "tier"], default="asc",
                        help="排序: asc=价格升序(默认), desc=价格降序, tier=按品类性能/采用率/规格完整度优先")
    parser.add_argument("--limit", type=int, default=DEFAULT_QUERY_LIMIT, help="最大返回数")
    parser.add_argument("--detail", action="store_true", help="返回完整属性 (默认只返回摘要)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--include-legacy", action="store_true", help="包含旧平台/非当前推荐范围条目")
    parser.add_argument("--include-workstation-gpu", action="store_true",
                        help="包含 RTX PRO 6000 等工作站显卡；仅本地大模型/工作站超高预算场景使用")
    return parser


def _validate_cli_args(parser, args):
    for name in (
        "budget", "max_length", "max_cooler_height", "min_vram", "min_capacity", "max_capacity",
        "fan_size", "radiator_bundle", "min_refresh", "min_pcie_slots", "limit",
    ):
        value = getattr(args, name)
        if value is not None and value <= 0:
            parser.error(f"--{name.replace('_', '-')} must be greater than 0")
    if (
        args.min_capacity is not None
        and args.max_capacity is not None
        and args.min_capacity > args.max_capacity
    ):
        parser.error("--min-capacity cannot exceed --max-capacity")
    if args.max_cooler_height is not None and args.category != "cooler":
        parser.error("--max-cooler-height requires --category cooler")
    if (
        args.min_pcie_slots is not None
        or args.require_usb4
        or args.require_thunderbolt
    ) and args.category not in ("mb", "all"):
        parser.error("motherboard capability filters require --category mb or all")


def _optional_bool(value):
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


def _run_grouped_query(args):
    return query_all(
        budget=args.budget,
        platform=args.platform,
        color=args.color,
        rgb=_optional_bool(args.rgb),
        limit=args.limit,
        include_legacy=args.include_legacy,
        sort=args.sort,
        socket=args.socket,
        chipset=args.chipset,
        memory_gen=args.memory_gen,
        form_factor=args.form_factor,
        max_length=args.max_length,
        gpu_cooling=args.gpu_cooling,
        gpu_chip=args.gpu_chip,
        min_vram=args.min_vram,
        min_capacity=args.min_capacity,
        max_capacity=args.max_capacity,
        model=args.model,
        item_id=args.item_id,
        include_workstation_gpu=args.include_workstation_gpu,
        showcase=args.showcase,
        air_flow=args.air_flow,
        dust_filter=_optional_bool(args.dust_filter),
        integrated_graphics=_optional_bool(args.integrated_graphics),
        display_output=args.display_output,
        min_pcie_slots=args.min_pcie_slots,
        require_usb4=args.require_usb4,
        require_thunderbolt=args.require_thunderbolt,
    )


def _run_single_query(args):
    return query(
        category=args.category,
        budget=args.budget,
        platform=args.platform,
        color=args.color,
        rgb=_optional_bool(args.rgb),
        limit=args.limit,
        showcase=args.showcase if args.category == "case" else None,
        include_legacy=args.include_legacy,
        sort=args.sort,
        socket=args.socket,
        chipset=args.chipset,
        memory_gen=args.memory_gen,
        form_factor=args.form_factor,
        max_length=args.max_length,
        max_cooler_height=args.max_cooler_height if args.category == "cooler" else None,
        gpu_cooling=args.gpu_cooling,
        gpu_chip=args.gpu_chip,
        min_vram=args.min_vram,
        min_capacity=args.min_capacity,
        max_capacity=args.max_capacity,
        pcie_generation=args.pcie_generation,
        dram_cache=_optional_bool(args.dram_cache),
        model=args.model,
        item_id=args.item_id,
        include_workstation_gpu=args.include_workstation_gpu,
        resolution=args.resolution,
        min_refresh=args.min_refresh,
        air_flow=args.air_flow if args.category == "case" else None,
        dust_filter=_optional_bool(args.dust_filter),
        fan_size=args.fan_size if args.category == "fan" else None,
        blade_direction=args.blade_direction if args.category == "fan" else None,
        linkable=_optional_bool(args.linkable) if args.category == "fan" else None,
        screen=_optional_bool(args.screen) if args.category == "fan" else None,
        radiator_bundle=args.radiator_bundle if args.category == "fan" else None,
        fan_type=args.fan_type if args.category == "fan" else None,
        integrated_graphics=_optional_bool(args.integrated_graphics) if args.category == "cpu" else None,
        display_output=args.display_output if args.category == "mb" else None,
        min_pcie_slots=args.min_pcie_slots if args.category == "mb" else None,
        require_usb4=args.require_usb4 if args.category == "mb" else False,
        require_thunderbolt=args.require_thunderbolt if args.category == "mb" else False,
    )


def _grouped_output(grouped, detail):
    if detail:
        return {
            category: items if category == "case" else [_project_selected_price(item) for item in items]
            for category, items in grouped.items()
        }
    return {
        category: (items if category == "case" else [summarize(item, category) for item in items])
        for category, items in grouped.items()
    }


def _single_output(results, category, detail):
    if category == "case":
        return results
    if detail:
        return [_project_selected_price(item) for item in results]
    return [summarize(item, category) for item in results]


def _price_note_tag(item):
    note = re.sub(r"\s+", " ", str(item.get("price_note") or "")).strip()
    if not note:
        return ""
    display = note if len(note) <= 160 else note[:157] + "..."
    return f" [报价备注: {display}]"


def _print_result_row(category, item, *, detail=False):
    selected_price = item.get("price") or _query_price(item)
    currency = item.get("price_currency", _QUERY_CURRENCY)
    if category == "case" or not detail:
        price = f"{currency} {selected_price}" if selected_price else "待补价"
        color = item.get("colors", item.get("color", ""))
        showcase_tag = " [海景房]" if item.get("is_showcase") else ""
        extra = display_extra(category, item)
        stale_tag = " [价格超过14天]" if item.get("price_stale") else ""
        note_tag = _price_note_tag(item)
        if item.get("price_floor_status") == "deep_below":
            floor_tag = " [低于地板且处同品类最低10%，默认不推荐]"
        elif item.get("price_floor_status") == "below":
            floor_tag = " [低于价格地板，请核实现价]"
        elif item.get("price_floor_status") == "not_set_volatile":
            floor_tag = " [价格波动大，请核实现价]"
        elif item.get("price_floor_warning"):
            floor_tag = " [地板上样本少，请核实现价]"
        else:
            floor_tag = ""
        print(
            f"  {item.get('id',''):45s} {item.get('brand',''):10s} "
            f"{item.get('model',''):35s} {price:>8s} {color} {extra} "
            f"{showcase_tag}{stale_tag}{floor_tag}{note_tag}"
        )
        return
    price = f"{currency} {selected_price}" if selected_price else "待补价"
    stale_tag = " [价格超过14天]" if item.get("price_stale") else ""
    note_tag = _price_note_tag(item)
    if item.get("price_floor_status") == "deep_below":
        floor_tag = " [低于地板且处同品类最低10%，默认不推荐]"
    elif item.get("price_floor_status") == "below":
        floor_tag = " [低于价格地板，请核实现价]"
    elif item.get("price_floor_status") == "not_set_volatile":
        floor_tag = " [价格波动大，请核实现价]"
    elif item.get("price_floor_warning"):
        floor_tag = " [地板上样本少，请核实现价]"
    else:
        floor_tag = ""
    print(
        f"  {item['id']:45s} {item.get('brand',''):12s} "
        f"{item.get('model',''):40s} {price:>8s}{stale_tag}{floor_tag}{note_tag}"
    )


def _emit_grouped_output(output, args):
    total = sum(len(items) for items in output.values())
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return total
    suffix = " (摘要模式, 用 --detail 看完整属性)" if not args.detail else ""
    print(f"查询结果: {total} 条，按品类分组{suffix}")
    for category, items in output.items():
        print(f"[{DISPLAY_NAMES.get(category, category)}] {len(items)} 条")
        for item in items:
            _print_result_row(category, item, detail=args.detail)
    return total


def _emit_single_output(output, args):
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return len(output)
    suffix = " (摘要模式, 用 --detail 看完整属性)" if not args.detail else ""
    print(f"查询结果: {len(output)} 条{suffix}")
    for item in output:
        _print_result_row(args.category, item, detail=args.detail)
    return len(output)


def main():
    parser = _build_parser()
    args = parser.parse_args()
    _validate_cli_args(parser, args)
    try:
        configure_overlays(args.overlay, args.currency)
        _resolved_sections()
        if args.item_id:
            resolved = resolve_id(args.item_id, _RESOLVED_BY_ID, _ALIAS_INDEX)
            args.item_id = resolved or args.item_id
    except OverlayError as exc:
        print(json.dumps({"ok": False, "errors": [exc.as_dict()]}, ensure_ascii=False), file=sys.stderr)
        return 2

    if args.category == "all":
        output = _grouped_output(_run_grouped_query(args), args.detail)
        return 0 if _emit_grouped_output(output, args) else 2

    results = _run_single_query(args)
    output = _single_output(results, args.category, args.detail)
    return 0 if _emit_single_output(output, args) else 2


if __name__ == "__main__":
    raise SystemExit(main())
