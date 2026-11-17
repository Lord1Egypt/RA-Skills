#!/usr/bin/env python3
"""主库结构校验 — 验证配件、机箱和辅助数据的基本完整性。

用法:
  python validate_library.py
"""

import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from component_inference import (
    enrich_item,
    infer_cooler_type,
    infer_cpu_conservative_power_w,
    infer_explicit_cooler_height_mm,
    infer_explicit_gpu_chip,
    infer_explicit_memory_frequency_mt,
    infer_capacity_gb,
    infer_gpu_vram,
    infer_memory_capacity_gb,
    infer_memory_module_count,
    infer_storage_form_factor,
    normalize_display_outputs,
)
from motherboard_capabilities import validate_motherboard_capabilities

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
YAML_SUFFIX = "." + "yaml"


def _data_path(stem):
    yaml_path = DATA / f"{stem}{YAML_SUFFIX}"
    return yaml_path if yaml_path.exists() else DATA / f"{stem}.txt"

REQUIRED_SECTIONS = ["cpus", "motherboards", "memory", "storage", "gpus", "coolers", "psus", "fans"]

REQUIRED_FIELDS = {
    "cpus": {"id", "brand", "model", "platform", "socket"},
    "motherboards": {"id", "brand", "model", "socket", "memory_generations", "form_factor"},
    "memory": {"id", "brand", "model", "generation", "capacity_gb"},
    "storage": {"id", "brand", "model", "capacity_tb", "form_factor"},
    "gpus": {"id", "brand", "model"},
    "coolers": {"id", "brand", "model", "type"},
    "psus": {"id", "brand", "model", "wattage_w"},
    "fans": {"id", "brand", "model", "fan_type", "default_recommend"},
}

# Fields that trigger warning (not error) when missing.
# Motherboard M.2/SATA omissions are tracked separately as non-blocking notes:
# current mainstream boards usually have at least one M.2 slot, and SATA is
# only critical for multi-drive / editing / workstation workflows.
WARN_FIELDS = {
    "cpus": {"power_w"},
    "gpus": {"power_w", "length_mm"},
    "motherboards": {"color", "memory_freq_max"},
    "psus": {"length_mm"},
}

NOTE_FIELDS = {
    "motherboards": {"m2_slots", "sata_ports"},
}

VALID_PRICE_STATUSES = {"scraped", "verified_manual", "channel_quote", "needs_market_quote"}
SOURCE_BACKED_PRICE_STATUSES = {"scraped", "verified_manual", "channel_quote"}
SOURCE_ID_PATTERN = re.compile(
    r"(^|-)mhc(-|$)|-(?:cpu|主板|显卡|内存|硬盘|电源|散热|机箱)-\d+-\d+-",
    re.IGNORECASE,
)
VALID_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9\u4e00-\u9fff]+)+$")
FAN_ACCESSORY_RE = re.compile(r"(?:控制器|集线器|遥控器|HUB)\s*$", re.IGNORECASE)
BLACK_VARIANT_RE = re.compile(r"黑(?:色|款|版|\s|$)", re.IGNORECASE)
WHITE_VARIANT_RE = re.compile(r"白(?:色|款|版|\s|$)", re.IGNORECASE)
OBVIOUS_MODEL_TYPO_RE = re.compile(
    r"\b(?:RYZWN|RYWEN)(?=\s*\d)|\bINTE\s+CORE\b",
    re.IGNORECASE,
)

COVERAGE_FIELDS = {
    "gpus": ["length_mm", "requires_16pin_psu"],
    "motherboards": [
        "m2_slots", "sata_ports", "memory_freq_max", "display_outputs",
        "pcie_slot_layout", "m2_slot_layout", "usb4_status", "thunderbolt_status",
    ],
    "memory": ["timing"],
    "storage": ["pcie_generation", "dram_cache", "dram_cache_mb"],
    "coolers": [
        "type", "radiator_mm", "rgb", "socket_support", "air_cooler_layout", "heatpipe_count",
    ],
    "psus": ["wattage_w", "form_factor", "length_mm", "modular", "native_16pin_gpu_power"],
    "fans": [
        "size_mm", "color", "rgb", "blade_direction", "is_linkable",
        "has_screen", "fan_type", "default_recommend", "pack_count",
    ],
    "cases": [
        "gpu_length_mm", "cpu_cooler_height_mm", "radiator_support", "fan_mounts",
        "psu_length_mm", "psu_length_recommended_mm",
    ],
    "displays": ["resolution", "size_inch", "refresh_rate_hz"],
}

CPU_AIR_COOLER_RE = re.compile(
    r"(热管|单塔|双塔|下压|CPU\s*散热|CPU风冷|内存散热器|阿萨辛|大霜塔|冰立方|玄冰)",
    re.IGNORECASE,
)
AIO_FRAME_FORBIDDEN_RE = re.compile(
    r"(热管|单塔|双塔|下压|CPU风冷|内存散热器|阿萨辛|大霜塔|冰立方|玄冰)",
    re.IGNORECASE,
)
AIO_FRAME_FANLESS_RE = re.compile(r"无风扇|不含风扇|不带风扇|WITHOUT\s+FANS?", re.IGNORECASE)
AIO_FRAME_POSITIVE_RE = re.compile(r"水冷|冷排|AIO|一体式", re.IGNORECASE)
VALID_FAN_TYPES = {"case_fan", "radiator_fan_pack", "aio_frame", "accessory"}
VALID_BLADE_DIRECTIONS = {"normal", "reverse"}
VALID_GPU_MEMORY_TYPES = {
    "GDDR5", "GDDR5X", "GDDR6", "GDDR6X", "GDDR7", "GDDR7 ECC",
    "HBM2", "HBM2E", "HBM3", "HBM3E",
}
VALID_AIR_COOLER_LAYOUTS = {"low_profile", "down_draft", "single_tower", "dual_tower"}
MODEL_FIT_QUANTIZATIONS = {"q4", "q5", "q8", "bf16"}


def _parse_int(value, default=0):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[^\d.-]", "", value)
        if cleaned in ("", "-", ".", "-."):
            return default
        try:
            return int(float(cleaned))
        except ValueError:
            return default
    return default


def _explicit_display_size_inch(item):
    """Read an explicit Chinese inch token without guessing from model codes."""
    match = re.search(r"(?<!\d)(\d{2}(?:\.\d+)?)\s*(?:英寸|寸)", str(item.get("model", "")))
    return float(match.group(1)) if match else None


def _explicit_display_refresh_hz(item):
    """Read the native-resolution refresh token without merging dual-mode rates."""
    values = [
        int(value)
        for value in re.findall(r"(?<!\d)(\d{2,4})\s*HZ", str(item.get("model", "")), re.IGNORECASE)
        if 20 <= int(value) <= 1000
    ]
    model = str(item.get("model", ""))
    if ("双模" in model or len(set(values)) > 1) and values:
        return values[0]
    return max(values) if values else None


MOTHERBOARD_CHIPSET_TOKENS = (
    "X870E", "X670E", "B650E", "B850", "X870", "X670", "B650", "A620", "A820",
    "Z890", "Z790", "Z690", "B860", "B760", "B660", "H810", "H610",
)


def _explicit_motherboard_chipset(item):
    """Infer the longest chipset token explicitly present in model or id."""
    text = str(item.get("model") or item.get("id") or "").upper()
    return next((token for token in MOTHERBOARD_CHIPSET_TOKENS if token in text), None)


def _canonical_motherboard_chipset(value):
    chipset = str(value or "").upper().replace(" ", "")
    if chipset.endswith("M") and chipset[:-1] in MOTHERBOARD_CHIPSET_TOKENS:
        return chipset[:-1]
    return chipset


def _valid_fan_mounts(value):
    if value in (None, "", [], {}):
        return True
    text = str(value).upper().strip().replace("×", "X")
    if re.fullmatch(r"\d{1,2}", text):
        return 1 <= int(text) <= 20
    if re.fullmatch(r"\d{2,3}(?:\.\d+)?\s*(?:MM|CM)", text):
        return False
    if re.search(r"\d{1,2}\s*个(?:以上)?", text):
        return True
    if re.search(r"\d{1,2}\s*X\s*(?:120|140|200)", text):
        return True
    if re.search(r"(?:120|140|160|200)\s*MM?\s*(?:风扇|FAN)", text):
        return True
    if re.search(r"风扇|FAN|TOP|FRONT|REAR|BOTTOM|SIDE|前|顶|后|底|侧", text):
        return True
    return not bool(re.fullmatch(r"\d+(?:\.\d+)?\s*(?:MM|CM)?", text))


def _id_not_normalized(item_id):
    text = str(item_id)
    return text.startswith("cat-") or "--" in text or bool(SOURCE_ID_PATTERN.search(text))


def _check_cpu_vendor_consistency(item):
    item_id = str(item.get("id", ""))
    brand = str(item.get("brand", "")).upper()
    model = str(item.get("model", "")).upper()
    platform = str(item.get("platform", "")).upper()
    socket = str(item.get("socket", "")).upper()
    text = f"{brand} {model} {platform} {socket} {item_id.upper()}"
    if "RYZEN" in text or "AMD" in model or socket.startswith("AM"):
        valid_id = item_id.startswith("cpu-amd-") or item_id.startswith("demo-cpu-amd-")
        if brand != "AMD" or platform != "AMD" or not socket.startswith("AM") or not valid_id:
            return "AMD/Ryzen CPU must use AMD brand/platform/socket/id prefix"
    intel_tokens = ("INTEL", "CORE I", "CORE ULTRA", "PENTIUM", "CELERON")
    if any(token in text for token in intel_tokens) or socket.startswith("LGA"):
        valid_id = item_id.startswith("cpu-intel-") or item_id.startswith("demo-cpu-intel-")
        if brand != "INTEL" or platform != "INTEL" or not socket.startswith("LGA") or not valid_id:
            return "Intel CPU must use Intel brand/platform/socket/id prefix"
    return None


def _valid_iso_date(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed <= date.today()


def _validate_price(section, item, errors, warnings):
    item_id = item.get("id", "<no-id>")
    price_status = item.get("price_status", "")
    price_cny = item.get("price_cny")
    price_date = item.get("price_date")
    if price_status and price_status not in VALID_PRICE_STATUSES:
        errors.append(f"{section}.{item_id}: invalid price_status '{price_status}'")
    if price_cny is not None and (
        isinstance(price_cny, bool)
        or not isinstance(price_cny, (int, float))
        or price_cny <= 0
    ):
        errors.append(f"{section}.{item_id}: price_cny must be a positive number")
    if price_status == "needs_market_quote" and price_cny is not None:
        errors.append(f"{section}.{item_id}: needs_market_quote must not have price_cny")
    if price_status in SOURCE_BACKED_PRICE_STATUSES and price_cny is None:
        errors.append(f"{section}.{item_id}: source-backed price_status requires price_cny")
    if price_cny is not None and not _valid_iso_date(price_date):
        errors.append(f"{section}.{item_id}: invalid or missing price_date={price_date}")
    elif price_date and not _valid_iso_date(price_date):
        warnings.append(f"{section}.{item_id}: invalid price_date={price_date}")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    coverage_rows: list[str] = field(default_factory=list)
    id_entries: list[tuple[str, str]] = field(default_factory=list)


def _validate_component_item(section, item, required):
    state = ValidationResult()
    item_id = item.get("id", "<no-id>")
    state.id_entries.append((section, item_id))
    if _id_not_normalized(item_id):
        state.errors.append(f"{section}.{item_id}: imported id was not normalized")
    missing = required - set(item.keys())
    if missing:
        state.errors.append(f"{section}.{item_id}: missing fields {missing}")

    _validate_price(section, item, state.errors, state.warnings)
    if OBVIOUS_MODEL_TYPO_RE.search(str(item.get("model") or "")):
        state.errors.append(f"{section}.{item_id}: obvious model-family spelling error")
    if section == "cpus":
        consistency_error = _check_cpu_vendor_consistency(item)
        if consistency_error:
            state.errors.append(f"{section}.{item_id}: {consistency_error}")
    if section == "motherboards":
        explicit_chipset = _explicit_motherboard_chipset(item)
        chipset = _canonical_motherboard_chipset(item.get("chipset"))
        if explicit_chipset and chipset and explicit_chipset != chipset:
            state.errors.append(
                f"{section}.{item_id}: chipset={chipset} conflicts with model token {explicit_chipset}"
            )
        memory_freq_max = item.get("memory_freq_max")
        if memory_freq_max not in (None, ""):
            if isinstance(memory_freq_max, bool) or not isinstance(memory_freq_max, int) or not 1600 <= memory_freq_max <= 12000:
                state.errors.append(f"{section}.{item_id}: invalid memory_freq_max={memory_freq_max}")
    if section == "gpus" and item.get("length_mm"):
        try:
            gpu_length = int(item.get("length_mm"))
            if gpu_length > 450 or gpu_length < 120:
                state.errors.append(f"{section}.{item_id}: impossible length_mm={item.get('length_mm')}")
        except (TypeError, ValueError):
            state.errors.append(f"{section}.{item_id}: invalid length_mm={item.get('length_mm')}")
    if section == "cpus":
        conservative_power_w = infer_cpu_conservative_power_w(item)
        if conservative_power_w is not None and item.get("power_w") != conservative_power_w:
            state.errors.append(
                f"{section}.{item_id}: power_w={item.get('power_w')} is below controlled unlocked-SKU floor {conservative_power_w}"
            )
    if section == "gpus":
        inferred_chip = infer_explicit_gpu_chip(item)
        current_chip = re.sub(r"[^A-Z0-9]", "", str(item.get("chip") or "").upper())
        if inferred_chip and current_chip != re.sub(r"[^A-Z0-9]", "", inferred_chip.upper()):
            state.errors.append(
                f"{section}.{item_id}: chip={item.get('chip')} conflicts with explicit model token {inferred_chip}"
            )
        memory_type = str(item.get("memory_type") or "").strip().upper()
        if memory_type and memory_type not in VALID_GPU_MEMORY_TYPES:
            state.errors.append(f"{section}.{item_id}: invalid memory_type={item.get('memory_type')}")
        inferred_vram = infer_gpu_vram(item)
        current_vram = item.get("vram_gb")
        if inferred_vram and current_vram:
            try:
                if int(current_vram) != int(inferred_vram):
                    state.errors.append(
                        f"{section}.{item_id}: vram_gb={current_vram} conflicts with model token {inferred_vram}GB"
                    )
            except (TypeError, ValueError):
                state.errors.append(f"{section}.{item_id}: invalid vram_gb={current_vram}")
        connectors = item.get("power_connectors") or []
        if "16pin" in connectors and "6pin" in connectors:
            state.errors.append(f"{section}.{item_id}: impossible mixed 16pin and 6pin connector data")
    if section == "memory":
        inferred_capacity = infer_memory_capacity_gb(item)
        inferred_modules = infer_memory_module_count(item)
        inferred_frequency = infer_explicit_memory_frequency_mt(item)
        if inferred_capacity and item.get("capacity_gb") != inferred_capacity:
            state.errors.append(
                f"{section}.{item_id}: capacity_gb={item.get('capacity_gb')} "
                f"conflicts with model-inferred {inferred_capacity}GB"
            )
        if inferred_modules and item.get("module_count") not in (None, inferred_modules):
            state.errors.append(
                f"{section}.{item_id}: module_count={item.get('module_count')} "
                f"conflicts with model-inferred {inferred_modules}"
            )
        if inferred_frequency is not None and item.get("frequency_mt") not in (None, "", inferred_frequency):
            state.errors.append(
                f"{section}.{item_id}: frequency_mt={item.get('frequency_mt')} "
                f"conflicts with explicit model token {inferred_frequency}"
            )
        timing = item.get("timing")
        if timing and not re.fullmatch(r"C(?:1[0-9]|[2-7][0-9]|80)", str(timing).upper()):
            state.errors.append(f"{section}.{item_id}: invalid timing={timing}")
    if section == "storage":
        inferred_capacity = infer_capacity_gb(item)
        raw_capacity_tb = item.get("capacity_tb")
        if inferred_capacity and raw_capacity_tb:
            try:
                raw_capacity_gb = float(raw_capacity_tb) * 1024
            except (TypeError, ValueError):
                state.errors.append(f"{section}.{item_id}: invalid capacity_tb={raw_capacity_tb}")
                raw_capacity_gb = float(inferred_capacity)
            tolerance_gb = max(32.0, float(inferred_capacity) * 0.10)
            if abs(raw_capacity_gb - float(inferred_capacity)) > tolerance_gb:
                state.errors.append(
                    f"{section}.{item_id}: capacity_tb={raw_capacity_tb} "
                    f"conflicts with model-inferred {inferred_capacity}GB"
                )
        if "dram_cache" in item and not isinstance(item.get("dram_cache"), bool):
            state.errors.append(f"{section}.{item_id}: invalid dram_cache={item.get('dram_cache')}")
        if item.get("dram_cache_mb") not in (None, ""):
            dram_cache_mb = item.get("dram_cache_mb")
            if isinstance(dram_cache_mb, bool) or not isinstance(dram_cache_mb, int) or not 1 <= dram_cache_mb <= 32768:
                state.errors.append(f"{section}.{item_id}: invalid dram_cache_mb={dram_cache_mb}")
            if item.get("dram_cache") is not True:
                state.errors.append(f"{section}.{item_id}: dram_cache_mb requires dram_cache=true")
        inferred_form_factor = infer_storage_form_factor(item)
        if inferred_form_factor and item.get("form_factor") != inferred_form_factor:
            state.errors.append(
                f"{section}.{item_id}: form_factor={item.get('form_factor')} "
                f"conflicts with model/catalog-inferred {inferred_form_factor}"
            )
        if (
            "SATA" in str(item.get("interface") or "").upper()
            and "M.2" in str(item.get("form_factor") or "").upper()
            and not str(inferred_form_factor or "").upper().startswith("M.2")
        ):
            state.errors.append(
                f"{section}.{item_id}: SATA drive is marked M.2 without explicit M.2 model evidence"
            )
    if section == "coolers":
        inferred_type = infer_cooler_type(item)
        raw_type = str(item.get("type") or "").lower()
        if inferred_type == "liquid" and raw_type not in {"liquid", "water", "水冷"}:
            state.errors.append(f"{section}.{item_id}: type={item.get('type')} conflicts with model-inferred liquid cooler")
        explicit_height = infer_explicit_cooler_height_mm(item)
        if explicit_height and item.get("height_mm") != explicit_height:
            state.errors.append(
                f"{section}.{item_id}: height_mm={item.get('height_mm')} conflicts with installed AXP90-X height {explicit_height}"
            )
        layout = item.get("air_cooler_layout")
        if layout not in (None, "") and layout not in VALID_AIR_COOLER_LAYOUTS:
            state.errors.append(f"{section}.{item_id}: invalid air_cooler_layout={layout}")
        heatpipes = item.get("heatpipe_count")
        if heatpipes not in (None, "") and (
            isinstance(heatpipes, bool) or not isinstance(heatpipes, int) or not 1 <= heatpipes <= 16
        ):
            state.errors.append(f"{section}.{item_id}: invalid heatpipe_count={heatpipes}")
        sockets = item.get("socket_support")
        if sockets is not None and (
            not isinstance(sockets, list)
            or not sockets
            or not all(isinstance(value, str) and value.strip() for value in sockets)
        ):
            state.errors.append(f"{section}.{item_id}: invalid socket_support={sockets}")
    if section == "motherboards" and item.get("display_outputs") is not None:
        outputs = item.get("display_outputs")
        if not normalize_display_outputs(outputs):
            state.errors.append(f"{section}.{item_id}: invalid display_outputs={outputs}")
    if section == "motherboards":
        for error in validate_motherboard_capabilities(item):
            state.errors.append(f"{section}.{item_id}: {error}")
    if section == "psus" and item.get("length_mm") not in (None, ""):
        length_mm = item.get("length_mm")
        if isinstance(length_mm, bool) or not isinstance(length_mm, int) or not 80 <= length_mm <= 300:
            state.errors.append(f"{section}.{item_id}: invalid length_mm={length_mm}")
    if section == "psus" and item.get("form_factor") not in (None, ""):
        if item.get("form_factor") not in {"ATX", "SFX", "SFX-L", "FLEX", "TFX"}:
            state.errors.append(f"{section}.{item_id}: invalid form_factor={item.get('form_factor')}")
    if section == "fans":
        model = str(item.get("model", ""))
        if item.get("fan_type") == "aio_frame":
            radiator_mm = item.get("radiator_fan_bundle_mm")
            positive_aio_evidence = bool(AIO_FRAME_POSITIVE_RE.search(model)) or radiator_mm in {240, 280, 360, 420, 480}
            if (
                not AIO_FRAME_FANLESS_RE.search(model)
                or AIO_FRAME_FORBIDDEN_RE.search(model)
                or not positive_aio_evidence
            ):
                state.errors.append(
                    f"{section}.{item_id}: aio_frame must describe a fanless AIO frame, not an air/memory cooler"
                )
        elif CPU_AIR_COOLER_RE.search(model):
            state.errors.append(f"{section}.{item_id}: CPU/memory cooler classified as fan")
        if item.get("fan_type") not in VALID_FAN_TYPES:
            state.errors.append(f"{section}.{item_id}: invalid fan_type={item.get('fan_type')}")
        if item.get("blade_direction") and item.get("blade_direction") not in VALID_BLADE_DIRECTIONS:
            state.errors.append(f"{section}.{item_id}: invalid blade_direction={item.get('blade_direction')}")
        if item.get("has_screen") and item.get("rgb") is not True:
            state.errors.append(f"{section}.{item_id}: screen fan must be rgb=true")
        if item.get("fan_type") == "aio_frame" and item.get("default_recommend") is not False:
            state.errors.append(f"{section}.{item_id}: aio_frame must not be default_recommend")
        accessory = bool(FAN_ACCESSORY_RE.search(str(item.get("model", "")).strip()))
        if accessory and item.get("fan_type") != "accessory":
            state.errors.append(f"{section}.{item_id}: accessory-only variant classified as fan")
        if item.get("fan_type") == "accessory" and item.get("default_recommend") is not False:
            state.errors.append(f"{section}.{item_id}: accessory must not be default_recommend")
        model = str(item.get("model", ""))
        explicit_black = bool(BLACK_VARIANT_RE.search(model))
        explicit_white = bool(WHITE_VARIANT_RE.search(model))
        mixed_color_label = "黑白" in model or "白黑" in model
        if not mixed_color_label and explicit_black != explicit_white:
            expected_color = "black" if explicit_black else "white"
            if str(item.get("color") or "").lower() != expected_color:
                state.errors.append(
                    f"{section}.{item_id}: color={item.get('color')} "
                    f"conflicts with explicit {expected_color} model token"
                )
        if item.get("size_mm"):
            size_mm = _parse_int(item.get("size_mm"))
            if size_mm < 80 or size_mm > 220:
                state.errors.append(f"{section}.{item_id}: invalid size_mm={item.get('size_mm')}")
    return state


def _missing_field_messages(section, items, fields):
    messages = []
    for field in sorted(fields.get(section, set())):
        missing_items = [item.get("id", "<no-id>") for item in items if not item.get(field)]
        if not missing_items:
            continue
        sample = ", ".join(missing_items[:5])
        messages.append(
            f"{section}: {len(missing_items)}/{len(items)} missing or empty {field}"
            + (f" (sample: {sample})" if sample else "")
        )
    return messages


def _validate_component_sections(lib):
    state = ValidationResult()
    metadata_date = (lib.get("metadata") or {}).get("price_date")
    if metadata_date and not _valid_iso_date(str(metadata_date)):
        state.errors.append(f"components.metadata.price_date invalid: {metadata_date}")

    for section in REQUIRED_SECTIONS:
        raw_items = lib.get(section)
        if not isinstance(raw_items, list) or not raw_items:
            state.errors.append(f"{section}: missing or empty section")
        items = raw_items if isinstance(raw_items, list) else []
        state.counts[section] = len(items)
        required = REQUIRED_FIELDS.get(section, set())

        for item in items:
            item_result = _validate_component_item(section, item, required)
            state.errors.extend(item_result.errors)
            state.warnings.extend(item_result.warnings)
            state.notes.extend(item_result.notes)
            state.id_entries.extend(item_result.id_entries)

        state.warnings.extend(_missing_field_messages(section, items, WARN_FIELDS))
        state.notes.extend(_missing_field_messages(section, items, NOTE_FIELDS))
        state.coverage_rows.extend(_coverage_rows(section, items))
    return state


def _validate_cases(cases):
    state = ValidationResult()
    case_items = cases.get("cases", [])
    if not isinstance(case_items, list) or not case_items:
        state.errors.append("cases: missing or empty section")
        case_items = []
    state.counts["cases"] = len(case_items)

    case_metadata_date = (cases.get("metadata") or {}).get("cutoff_date")
    if case_metadata_date and not _valid_iso_date(str(case_metadata_date)):
        state.errors.append(f"cases.metadata.cutoff_date invalid: {case_metadata_date}")

    for case in case_items:
        case_id = case.get("id", "<no-id>")
        state.id_entries.append(("cases", case_id))
        if _id_not_normalized(case_id):
            state.errors.append(f"cases.{case_id}: imported id was not normalized")
        _validate_price("cases", case, state.errors, state.warnings)
        if not case.get("brand"):
            state.errors.append(f"cases.{case_id}: missing brand")
        if not case.get("motherboard_support"):
            state.warnings.append(f"cases.{case_id}: no motherboard_support")
        if not case.get("gpu_length_mm"):
            state.warnings.append(f"cases.{case_id}: no gpu_length_mm")
        if not _valid_fan_mounts(case.get("fan_mounts")):
            state.errors.append(f"cases.{case_id}: invalid fan_mounts={case.get('fan_mounts')}")
        if case.get("psu_length_mm") not in (None, ""):
            psu_length_mm = case.get("psu_length_mm")
            if isinstance(psu_length_mm, bool) or not isinstance(psu_length_mm, int) or not 80 <= psu_length_mm <= 500:
                state.errors.append(f"cases.{case_id}: invalid psu_length_mm={psu_length_mm}")
        if case.get("psu_length_recommended_mm") not in (None, ""):
            recommended_mm = case.get("psu_length_recommended_mm")
            if isinstance(recommended_mm, bool) or not isinstance(recommended_mm, int) or not 80 <= recommended_mm <= 500:
                state.errors.append(f"cases.{case_id}: invalid psu_length_recommended_mm={recommended_mm}")
            elif case.get("psu_length_mm") and recommended_mm > case.get("psu_length_mm"):
                state.errors.append(
                    f"cases.{case_id}: psu_length_recommended_mm={recommended_mm} "
                    f"exceeds psu_length_mm={case.get('psu_length_mm')}"
                )
        if "psu_length_condition" in case and not str(case.get("psu_length_condition") or "").strip():
            state.errors.append(f"cases.{case_id}: empty psu_length_condition")

    missing_case_prices = [
        case.get("id", "<no-id>") for case in case_items if case.get("price_cny") is None
    ]
    if missing_case_prices:
        sample = ", ".join(missing_case_prices[:5])
        state.warnings.append(
            f"cases: {len(missing_case_prices)}/{len(case_items)} missing price_cny"
            + (f" (sample: {sample})" if sample else "")
        )
    state.coverage_rows.extend(_coverage_rows("cases", case_items))
    return case_items, state


def _optional_dataset_warning(label, field, missing_items, total):
    if not missing_items:
        return None
    sample = ", ".join(missing_items[:5])
    return (
        f"{label}: {len(missing_items)}/{total} missing {field}"
        + (f" (sample: {sample})" if sample else "")
    )


def _validate_displays():
    state = ValidationResult()
    displays_path = _data_path("displays")
    if not displays_path.exists():
        state.notes.append("display catalog: optional explicit monitor database missing")
        return state

    with displays_path.open("r", encoding="utf-8") as file:
        displays = yaml.safe_load(file) or {}
    display_items = displays.get("displays", [])
    state.counts["displays"] = len(display_items)
    missing_display_prices = []
    missing_display_refresh = []
    missing_display_brand = []
    display_metadata_date = (displays.get("metadata") or {}).get("price_date")
    if display_metadata_date and not _valid_iso_date(str(display_metadata_date)):
        state.errors.append(f"displays.metadata.price_date invalid: {display_metadata_date}")

    for item in display_items:
        item_id = item.get("id", "<no-id>")
        state.id_entries.append(("displays", item_id))
        missing = {"id", "model", "resolution"} - set(item.keys())
        if missing:
            state.errors.append(f"displays.{item_id}: missing fields {missing}")
        if not item.get("brand"):
            missing_display_brand.append(item_id)
        _validate_price("displays", item, state.errors, state.warnings)
        price_status = item.get("price_status", "")
        if price_status != "needs_market_quote" and item.get("price_cny") is None:
            missing_display_prices.append(item_id)
        if not item.get("refresh_rate_hz"):
            missing_display_refresh.append(item_id)
        refresh_hz = _parse_int(item.get("refresh_rate_hz"))
        if refresh_hz and (refresh_hz < 30 or refresh_hz > 1000):
            state.errors.append(f"displays.{item_id}: implausible refresh_rate_hz={refresh_hz}")
        explicit_refresh = _explicit_display_refresh_hz(item)
        if explicit_refresh and refresh_hz and explicit_refresh != refresh_hz:
            state.errors.append(
                f"displays.{item_id}: refresh_rate_hz={refresh_hz} "
                f"conflicts with explicit model token {explicit_refresh}"
            )
        explicit_size = _explicit_display_size_inch(item)
        if explicit_size and item.get("size_inch"):
            if abs(float(item.get("size_inch")) - explicit_size) > 0.6:
                state.errors.append(
                    f"displays.{item_id}: size_inch={item.get('size_inch')} "
                    f"conflicts with explicit model token {explicit_size}"
                )

    total = len(display_items)
    for warning in (
        _optional_dataset_warning("displays", "price_cny", missing_display_prices, total),
        _optional_dataset_warning(
            "displays", "refresh_rate_hz", missing_display_refresh, total
        ),
        _optional_dataset_warning("displays", "brand", missing_display_brand, total),
    ):
        if warning:
            state.warnings.append(warning)
    state.coverage_rows.extend(_coverage_rows("displays", display_items))
    return state


def _valid_fps_range(value):
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, (int, float)) for item in value)
        and value[0] > 0
        and value[1] >= value[0]
    )


def _validate_game_fps():
    state = ValidationResult()
    game_fps_path = _data_path("game_fps")
    if not game_fps_path.exists():
        state.errors.append("game FPS catalog: missing game FPS reference table")
        return state

    with game_fps_path.open("r", encoding="utf-8") as file:
        game_fps = yaml.safe_load(file) or {}
    game_ids = {game.get("id") for game in game_fps.get("games", []) if game.get("id")}
    if not game_ids:
        state.errors.append("game FPS catalog: no games")
    required_fps_fields = {
        "game", "resolution", "preset", "cpu", "gpu", "avg_fps",
        "confidence", "source_title", "source_date", "source_type",
    }
    for index, row in enumerate(game_fps.get("benchmarks", []), start=1):
        prefix = f"game_fps.benchmarks[{index}]"
        missing = required_fps_fields - set(row)
        if missing:
            state.errors.append(f"{prefix}: missing fields {missing}")
        if row.get("game") not in game_ids:
            state.errors.append(f"{prefix}: unknown game {row.get('game')}")
        if row.get("source_type") == "public_fps_prediction" and row.get("confidence") == "high":
            state.errors.append(f"{prefix}: public prediction confidence must not be high")
        if not row.get("p1_low_fps") and not row.get("fps_range"):
            state.errors.append(f"{prefix}: missing either p1_low_fps or fps_range")
        for field_name in ("avg_fps", "p1_low_fps", "fps_range", "base_fps"):
            if field_name in row and not _valid_fps_range(row.get(field_name)):
                state.errors.append(f"{prefix}: invalid {field_name}={row.get(field_name)}")
    state.counts["game_fps_samples"] = len(game_fps.get("benchmarks", []))
    return state


def _validate_model_fit():
    state = ValidationResult()
    model_fit_path = _data_path("model_fit")
    if not model_fit_path.exists():
        state.errors.append("model-fit catalog: missing local LLM hardware-fit policy")
        return state
    try:
        with model_fit_path.open("r", encoding="utf-8") as file:
            document = yaml.safe_load(file) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        state.errors.append(f"model-fit catalog: cannot load: {exc}")
        return state
    policy = document.get("policy")
    models = document.get("models")
    if not isinstance(policy, dict) or not isinstance(models, list) or not models:
        state.errors.append("model-fit catalog: policy and non-empty models are required")
        return state
    weight_factors = policy.get("weight_gib_per_billion_params")
    if not isinstance(weight_factors, dict) or set(weight_factors) != MODEL_FIT_QUANTIZATIONS:
        state.errors.append("model-fit catalog: weight factors must be q4/q5/q8/bf16")
    elif any(not isinstance(value, (int, float)) or value <= 0 for value in weight_factors.values()):
        state.errors.append("model-fit catalog: weight factors must be positive numbers")
    vram_tiers = policy.get("vram_tiers_gib")
    if not isinstance(vram_tiers, list) or vram_tiers != sorted(set(vram_tiers)) or any(value <= 0 for value in vram_tiers):
        state.errors.append("model-fit catalog: vram tiers must be unique ascending positive numbers")
    for ratio_field in ("recommended_vram_utilization", "conditional_vram_utilization"):
        value = policy.get(ratio_field)
        if not isinstance(value, (int, float)) or not 0 < value < 1:
            state.errors.append(f"model-fit catalog: invalid {ratio_field}")
    if (
        isinstance(policy.get("recommended_vram_utilization"), (int, float))
        and isinstance(policy.get("conditional_vram_utilization"), (int, float))
        and policy["recommended_vram_utilization"] >= policy["conditional_vram_utilization"]
    ):
        state.errors.append("model-fit catalog: recommended utilization must be below conditional utilization")
    seen = set()
    required = {"id", "name", "params_b", "hf_repo", "default_quantization", "default_context_tokens"}
    for index, model in enumerate(models, start=1):
        prefix = f"model_fit.models[{index}]"
        if not isinstance(model, dict):
            state.errors.append(f"{prefix}: must be mapping")
            continue
        missing = required - set(model)
        if missing:
            state.errors.append(f"{prefix}: missing fields {missing}")
        model_id = model.get("id")
        if model_id in seen:
            state.errors.append(f"{prefix}: duplicate id {model_id}")
        seen.add(model_id)
        if not isinstance(model.get("params_b"), (int, float)) or model.get("params_b", 0) <= 0:
            state.errors.append(f"{prefix}: params_b must be positive")
        if model.get("default_quantization") not in MODEL_FIT_QUANTIZATIONS:
            state.errors.append(f"{prefix}: invalid default_quantization")
        if not isinstance(model.get("default_context_tokens"), int) or model.get("default_context_tokens", 0) <= 0:
            state.errors.append(f"{prefix}: default_context_tokens must be positive integer")
        if model.get("active_params_b") is not None and model.get("active_params_b", 0) >= model.get("params_b", 0):
            state.errors.append(f"{prefix}: active_params_b must be below total params_b")
    state.counts["model_fit_samples"] = len(models)
    return state


def _validate_ids(id_entries):
    errors = []
    seen_ids = {}
    for section, item_id in id_entries:
        if not item_id or item_id == "<no-id>":
            errors.append(f"{section}: missing id")
            continue
        if not VALID_ID_PATTERN.fullmatch(str(item_id)):
            errors.append(f"{section}.{item_id}: invalid id shape; use a stable category-model id")
        previous = seen_ids.get(item_id)
        if previous:
            errors.append(f"duplicate id {item_id}: {previous} and {section}")
        else:
            seen_ids[item_id] = section
    return ValidationResult(errors=errors)


def _combine_validation_results(*results):
    id_entries = [
        entry
        for result in results
        for entry in result.id_entries
    ]
    id_result = _validate_ids(id_entries)
    counts = {
        key: value
        for result in results
        for key, value in result.counts.items()
    }
    return ValidationResult(
        errors=[
            *id_result.errors,
            *(error for result in results for error in result.errors),
        ],
        warnings=[warning for result in results for warning in result.warnings],
        notes=[note for result in results for note in result.notes],
        counts=counts,
        coverage_rows=[row for result in results for row in result.coverage_rows],
        id_entries=id_entries,
    )


def _report_validation(lib, case_items, state):
    if state.errors:
        print("VALIDATION FAILED")
        for error in state.errors:
            print(f"  ❌ {error}")
        for warning in state.warnings:
            print(f"  ⚠️ {warning}")
        return 1

    print("component library validation OK")
    print(f"sections: {', '.join(REQUIRED_SECTIONS)} + cases")
    for section, count in state.counts.items():
        print(f"  {section}: {count} items")

    status_counts = {}
    for section in REQUIRED_SECTIONS:
        for item in lib.get(section, []):
            status = item.get("price_status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
    for item in case_items:
        status = item.get("price_status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    print(f"price status counts: {status_counts}")

    if state.coverage_rows:
        print("\nfield coverage (raw/effective):")
        for row in state.coverage_rows:
            print(f"  {row}")
    if state.warnings:
        print(f"\nwarnings ({len(state.warnings)}):")
        for warning in state.warnings:
            print(f"  ⚠️ {warning}")
    if state.notes:
        print(f"\nnon-blocking notes ({len(state.notes)}):")
        for note in state.notes:
            print(f"  ℹ️ {note}")
    return 0


def main():
    comp_path = _data_path("components")
    if not comp_path.exists():
        print(f"FAIL: {comp_path} not found")
        return 1

    with comp_path.open("r", encoding="utf-8") as f:
        lib = yaml.safe_load(f) or {}

    component_result = _validate_component_sections(lib)

    cases_path = _data_path("cases")
    if not cases_path.exists():
        print(f"FAIL: {cases_path} not found")
        return 1

    with cases_path.open("r", encoding="utf-8") as f:
        cases = yaml.safe_load(f) or {}

    case_items, case_result = _validate_cases(cases)
    display_result = _validate_displays()
    fps_result = _validate_game_fps()
    model_fit_result = _validate_model_fit()
    state = _combine_validation_results(
        component_result,
        case_result,
        display_result,
        fps_result,
        model_fit_result,
    )
    return _report_validation(lib, case_items, state)


def _has_value(item, field):
    value = item.get(field)
    if field in {"length_mm", "gpu_length_mm", "cpu_cooler_height_mm", "height_mm"} and value == 0:
        return False
    if field == "fan_mounts" and not _valid_fan_mounts(value):
        return False
    return value not in (None, "", [], {})


def _coverage_rows(section, items):
    rows = []
    fields = COVERAGE_FIELDS.get(section, [])
    if not fields:
        return rows
    enriched_items = [enrich_item(section, item) for item in items]
    total = len(items) or 1
    for field in fields:
        raw = sum(1 for item in items if _has_value(item, field))
        effective = sum(1 for item in enriched_items if _has_value(item, field))
        if raw != total or effective != total:
            rows.append(f"{section}.{field}: raw {raw}/{total}, effective {effective}/{total}")
    return rows


if __name__ == "__main__":
    sys.exit(main())
