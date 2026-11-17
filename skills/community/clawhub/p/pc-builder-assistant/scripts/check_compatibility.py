#!/usr/bin/env python3
"""装机兼容性检查引擎。

用法:
  python check_compatibility.py --strict --cpu cpu-intel-i5-14400f \
    --mb demo-mb-asus-prime-b760m-k-d4 --mem mem-ddr4-3200-32-kingston-beast-black \
    --storage ssd-nv21tb3500mbs --gpu demo-gpu-gigabyte-rtx5070-windforce-oc \
    --psu demo-psu-msi-mag-a750gl-pcie5 --case case-jonsbo-d31-mesh \
    --cooler demo-cooler-thermalright-pa120se
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

from component_inference import (
    THERMAL_HIGH,
    THERMAL_LOW,
    THERMAL_MAINSTREAM,
    THERMAL_STRONG,
    enrich_item,
    infer_cooler_exclusive_platform,
    infer_cooler_thermal_profile,
    infer_cpu_conservative_power_w,
    infer_cpu_required_thermal_rank,
    infer_cpu_integrated_graphics,
    infer_native_16pin_psu,
    infer_requires_16pin_gpu,
    normalize_memory_generation,
    normalize_memory_generations,
    normalize_display_outputs,
    normalize_psu_form_factor,
    storage_interface_form_factor_consistent,
    storage_model_form_factor_consistent,
)
from power_budget import (
    DEFAULT_NON_CORE_POWER_W,
    PSU_HEADROOM_FACTOR,
    PSU_TIGHT_MARGIN_W,
    recommended_psu_w,
)
from catalog_overlay import (
    GPU_POWER_EVIDENCE_FIELD,
    OverlayError,
    enrich_resolved_item,
    load_catalog_sections,
    resolve_catalog,
    resolve_id,
)
from motherboard_capabilities import (
    pcie_physical_slot_count,
    verified_m2_slot_count,
    verified_m2_slot_layout,
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
PSU_CASE_CLEARANCE_WARNING_MM = 20
CPU_COOLER_CLEARANCE_WARNING_MM = 5
THERMAL_RANK_LABELS = {
    THERMAL_LOW: "低功耗散热级",
    THERMAL_MAINSTREAM: "单塔四热管或同级",
    THERMAL_STRONG: "双塔六热管或240/280水冷级",
    THERMAL_HIGH: "360mm及以上水冷级",
}


def _storage_text(value):
    return unicodedata.normalize("NFKC", str(value or "")).upper()


def _storage_uses_m2(storage):
    """Return whether explicit storage facts identify an M.2/NGFF device."""
    text = " ".join(
        (_storage_text(storage.get("form_factor")), _storage_text(storage.get("interface")))
    )
    return "MSATA" not in text and any(token in text for token in ("M.2", "M2", "NGFF"))


def _storage_uses_m2_sata(storage):
    return _storage_uses_m2(storage) and "SATA" in _storage_text(storage.get("interface"))


def _m2_pcie_generation(storage):
    if not _storage_uses_m2(storage) or _storage_uses_m2_sata(storage):
        return None
    value = storage.get("pcie_generation")
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and 1 <= value <= 5:
        return value
    match = re.search(r"(?:PCIE|GEN)\s*([1-5])", _storage_text(storage.get("interface")))
    return int(match.group(1)) if match else None


def _m2_slot_has_conditions(slot):
    return bool(slot.get("conditions") or slot.get("shares_with"))


def _assign_m2_pcie_slots(storage_list, layout):
    """Assign PCIe M.2 devices while preserving full speed and simple slots."""
    requested = sorted(
        (
            _m2_pcie_generation(storage)
            for storage in storage_list
            if _storage_uses_m2(storage) and not _storage_uses_m2_sata(storage)
        ),
        key=lambda generation: generation or 0,
        reverse=True,
    )
    available = list(layout)
    downgraded = []
    used_slots = []
    for generation in requested:
        full_speed = [slot for slot in available if generation is None or slot["pcie_generation"] >= generation]
        if full_speed:
            selected = min(
                full_speed,
                key=lambda slot: (_m2_slot_has_conditions(slot), slot["pcie_generation"]),
            )
        else:
            selected = min(
                available,
                key=lambda slot: (_m2_slot_has_conditions(slot), -slot["pcie_generation"]),
            )
            downgraded.append((generation, selected["pcie_generation"]))
        available.remove(selected)
        used_slots.append(selected)
    return downgraded, used_slots


def _m2_layout_generation_summary(layout):
    counts = {}
    for slot in layout:
        if "pcie" not in slot.get("interfaces", []):
            continue
        generation = slot["pcie_generation"]
        counts[generation] = counts.get(generation, 0) + 1
    return "、".join(
        f"Gen{generation}×{count}" for generation, count in sorted(counts.items(), reverse=True)
    )


class CompatibilityChecker:
    """装机兼容性检查引擎。

    检查基础兼容性: CPU↔主板, 散热↔CPU, 散热能力, 内存↔主板(代际/数量/容量),
    显卡↔机箱, 硬盘↔主板, 电源↔功耗, 散热↔机箱, 机箱↔主板, 机箱↔电源。
    """

    # 机箱版型向下兼容表
    FORM_FACTOR_MAP = {
        "EATX": ["EATX", "ATX", "MATX", "ITX"],
        "ATX":  ["ATX", "MATX", "ITX"],
        "MATX": ["MATX", "ITX"],
        "M-ATX": ["MATX", "ITX"],
        "Mini-ITX": ["ITX"],
        "ITX": ["ITX"],
    }

    RADIATOR_SIZE_COMPATIBILITY = {
        120: {120},
        140: {140},
        240: {120, 240},
        280: {140, 280},
        360: {120, 240, 360},
        420: {140, 280, 420},
        480: {480},
    }

    def _parse_num(self, val, default=0):
        """从字符串/数字中提取数值。"""
        if isinstance(val, (int, float)):
            return val if not (isinstance(val, float) and math.isnan(val)) else default
        if isinstance(val, str):
            cleaned = re.sub(r"[^\d.-]", "", val)
            try:
                return float(cleaned) if "." in cleaned else int(cleaned)
            except (ValueError, TypeError):
                return default
        return default

    def _parse_rated_wattage(self, psu):
        """Prefer the rated wattage in PSU model text over noisy imported fields."""
        if not psu:
            return 0
        model = str(psu.get("model", ""))
        match = re.search(r"额定\s*(\d{3,4})\s*W", model, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"(\d{3,4})\s*W", model, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        return self._parse_num(psu.get("wattage_w", 0))

    def _normalize(self, val):
        """移除非字母数字字符并转大写，用于接口/尺寸比较。"""
        if not val:
            return ""
        text = unicodedata.normalize("NFKC", str(val))
        return re.sub(r"[^0-9a-zA-Z]", "", text).upper()

    def _as_list(self, value):
        """Normalize nullable/list-like catalog fields without inventing facts."""
        if value in (None, "", [], (), {}):
            return []
        if isinstance(value, (list, tuple, set)):
            return list(value)
        return [value]

    @staticmethod
    def _has_spec_conflict(item, *fields):
        conflicts = set((item or {}).get("spec_conflicts", []))
        return bool(conflicts.intersection(fields))

    def _normalize_socket_list(self, val):
        """Normalize socket strings while preserving multi-socket separators."""
        if not val:
            return []
        text = unicodedata.normalize("NFKC", str(val))
        parts = re.split(
            r"[/,|，、;；&+]|\bAND\b|和|及|与", text, flags=re.IGNORECASE
        )
        normalized = []
        for part in parts:
            socket = self._normalize(part)
            previous = None
            while socket and socket != previous:
                previous = socket
                for prefix in ("SOCKET", "INTEL", "AMD"):
                    if socket.startswith(prefix):
                        socket = socket[len(prefix):]
                        break
            if socket in {
                "775", "1150", "1151", "1155", "1156", "115X", "1200",
                "1366", "1700", "1851", "2011", "20113", "2066",
            }:
                socket = "LGA" + socket
            if socket:
                normalized.append(socket)
        return normalized

    def _normalize_form_factor(self, ff):
        """标准化版型名称用于比较。"""
        if not ff:
            return ""
        ff = ff.upper().replace("-", "").replace("_", "").replace(" ", "")
        mapping = {"MATX": "MATX", "MINIITX": "ITX", "MICROATX": "MATX",
                   "EATX": "EATX", "ATX": "ATX"}
        return mapping.get(ff, ff)

    def _cpu_has_integrated_graphics(self, cpu):
        """Conservatively infer whether the CPU can provide display output."""
        return infer_cpu_integrated_graphics(cpu or {}) is True

    @staticmethod
    def _motherboard_display_outputs(mb):
        """Return maintainer-verified motherboard display output types."""
        outputs = (mb or {}).get("display_outputs")
        return normalize_display_outputs(outputs)

    # --- 12 类基础检查函数 ---

    def check_cpu_motherboard(self, cpu, mb):
        """检查 CPU 和主板兼容性: socket 接口匹配。"""
        if not cpu or not mb:
            return {"type": "msg", "msg": f"缺少必要组件{('主板' if cpu else 'CPU')}"}
        cpu_sockets = self._normalize_socket_list(cpu.get("socket", ""))
        mb_sockets = self._normalize_socket_list(mb.get("socket", ""))
        if not cpu_sockets or not mb_sockets:
            return {"type": "msg", "msg": "CPU或主板缺少接口信息，需下单前复核"}
        if not set(cpu_sockets).intersection(mb_sockets):
            return {"type": "error",
                    "msg": f"接口不兼容，CPU【{cpu.get('socket')}】，主板【{mb.get('socket')}】"}
        return {"type": "success", "msg": f"CPU和主板接口兼容【{mb.get('socket')}】"}

    def check_cooler_cpu(self, cooler, cpu):
        """检查散热器明确声明的扣具接口是否支持 CPU。"""
        if not cooler or not cpu:
            return {"type": "msg", "msg": f"缺少必要组件{('CPU' if cooler else '散热')}"}
        cpu_sockets = self._normalize_socket_list(cpu.get("socket", ""))
        cooler_sockets = []
        for value in self._as_list(cooler.get("socket_support")):
            cooler_sockets.extend(self._normalize_socket_list(value))
        if not cpu_sockets:
            return {"type": "msg", "msg": "CPU缺少接口信息，需下单前复核散热扣具"}
        exclusive_platform = infer_cooler_exclusive_platform(cooler)
        if exclusive_platform:
            cpu_platforms = {
                "intel" if socket.startswith("LGA") else "amd" if socket.startswith("AM") else None
                for socket in cpu_sockets
            }
            if exclusive_platform not in cpu_platforms:
                return {
                    "type": "error",
                    "msg": f"散热器型号明确标注{exclusive_platform.upper()}专用，不能搭配CPU接口【{cpu.get('socket')}】",
                }
        if not cooler_sockets:
            incomplete = self._as_list(cooler.get("_overlay_incomplete_fields"))
            if "socket_support" in incomplete:
                return {"type": "msg", "msg": "用户散热器缺少接口支持信息，需下单前复核扣具"}
            return {
                "type": "skipped",
                "msg": "散热器未收录精确扣具接口；"
                       + (f"型号标注{exclusive_platform.upper()}专用，与CPU同平台，" if exclusive_platform else "")
                       + "不据此宣称已核实具体接口",
                "review_required": False,
            }
        if not set(cpu_sockets).intersection(cooler_sockets):
            return {
                "type": "error",
                "msg": (
                    f"散热器扣具不支持CPU接口，散热器支持【{'/'.join(self._as_list(cooler.get('socket_support')))}】，"
                    f"CPU【{cpu.get('socket')}】"
                ),
            }
        return {"type": "success", "msg": f"散热器扣具支持CPU接口【{cpu.get('socket')}】"}

    def check_cooler_thermal_capacity(self, cooler, cpu):
        """Compare evidenced cooler structure with the repository's conservative CPU tier."""
        if not cooler or not cpu:
            return {"type": "msg", "msg": f"缺少必要组件{('CPU' if cooler else '散热')}，无法检查散热能力"}
        power_w = self._parse_num(infer_cpu_conservative_power_w(cpu), 0)
        if power_w <= 0:
            return {"type": "msg", "msg": "CPU缺少保守负载功耗字段，需复核持续负载散热需求"}
        required_rank = infer_cpu_required_thermal_rank(cpu)

        profile = infer_cooler_thermal_profile(cooler)
        power_text = f"{float(power_w):g}W"
        required_label = THERMAL_RANK_LABELS[required_rank]
        if profile.rank is None:
            return {
                "type": "msg",
                "msg": (
                    f"CPU保守负载字段【{power_text}】要求至少【{required_label}】；"
                    f"当前散热器【{profile.label}】，需复核塔体、热管或冷排尺寸后才能完整通过"
                ),
            }
        if profile.rank < required_rank:
            return {
                "type": "warn",
                "msg": (
                    f"CPU保守负载字段【{power_text}】要求至少【{required_label}】；"
                    f"当前散热证据【{profile.label}】低于仓库当前散热选型门槛，"
                    "需复核持续负载温度与噪音，或升级散热器"
                ),
            }
        return {
            "type": "success",
            "msg": f"散热证据【{profile.label}】达到CPU保守负载字段【{power_text}】的选型门槛",
        }

    def check_memory_motherboard(self, memory_list, mb):
        """检查内存与主板兼容性: DDR 代际 + 频率。"""
        if not mb:
            return [{"type": "msg", "msg": "缺少必要组件主板"}]
        if not memory_list:
            return [{"type": "msg", "msg": "缺少必要组件内存"}]
        results = []
        for i, mem in enumerate(memory_list):
            label = str(i + 1) if len(memory_list) > 1 else ""
            mem_gen = normalize_memory_generation(mem.get("generation"))
            mb_gens = normalize_memory_generations(mb.get("memory_generations"))
            if not mem_gen or not mb_gens:
                results.append({"type": "msg", "msg": f"内存{label}缺少接口信息"})
                continue
            if mem_gen not in mb_gens:
                results.append({"type": "error",
                    "msg": f"主板和内存{label}接口不兼容，主板支持【{'/'.join(mb_gens)}】，内存【{mem_gen}】"})
                continue
            mem_freq = self._parse_num(mem.get("frequency_mt", 0))
            mb_freq = self._parse_num(mb.get("memory_freq_max", 0))
            if mem_freq and not mb_freq:
                results.append({"type": "skipped",
                    "msg": f"主板缺少内存最高频率字段，未检查内存{label}频率【{mem_freq}MHz】的XMP/EXPO/QVL条件",
                    "review_required": False})
            elif mem_freq and mb_freq and mem_freq > mb_freq:
                results.append({"type": "warn",
                    "msg": f"内存{label}频率【{mem_freq}MHz】超过主板支持【{mb_freq}MHz】，可能不稳定"})
            else:
                results.append({"type": "success", "msg": f"主板和内存{label}接口兼容【{mem_gen}】"})
        return results

    def check_memory_slots(self, memory_list, mb):
        """检查内存数量 vs 主板插槽数。"""
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        if not memory_list:
            return {}
        total_sticks = sum(self._parse_num(m.get("module_count", 1)) for m in memory_list)
        mb_slots = self._parse_num(mb.get("memory_slots", 0))
        if not total_sticks or not mb_slots:
            return {}
        if total_sticks > mb_slots:
            return {"type": "error",
                "msg": f"内存数量过多，已选【{total_sticks}条】，主板插槽数量【{mb_slots}个】"}
        return {"type": "success", "msg": "内存插槽数量充足"}

    def check_memory_capacity(self, memory_list, mb):
        """检查内存总容量 vs 主板最大容量。"""
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        if not memory_list:
            return {}
        total_gb = sum(self._parse_num(m.get("capacity_gb", 0)) for m in memory_list)
        max_gb = self._parse_num(mb.get("memory_max_gb", 0))
        if not total_gb or not max_gb:
            return {}
        if total_gb > max_gb:
            return {"type": "error",
                "msg": f"内存总容量【{total_gb}GB】超过主板最大支持【{max_gb}GB】"}
        return {"type": "success", "msg": "内存容量在主板支持范围内"}

    def check_gpu_case(self, gpu, case, index=""):
        """检查显卡长度 vs 机箱显卡限长。"""
        if not gpu:
            return {}
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        if self._has_spec_conflict(gpu, "length_mm"):
            return {
                "type": "msg",
                "msg": f"显卡{index}同型号目录记录的长度互相冲突，需按精确SKU官网规格复核后再判断机箱限长",
            }
        gpu_len = self._parse_num(gpu.get("length_mm", 0))
        case_limit = self._parse_num(case.get("gpu_length_mm", 0))
        if not gpu_len or not case_limit:
            return {}
        if gpu_len > case_limit:
            return {"type": "error",
                "msg": f"显卡{index}长度【{gpu_len}mm】超过机箱限制【{case_limit}mm】"}
        return {"type": "success", "msg": f"显卡{index}长度在机箱限制内"}

    def check_storage_motherboard(self, storage_list, mb):
        """检查硬盘接口 vs 主板接口。"""
        if not storage_list:
            return {"type": "msg", "msg": "缺少必要组件硬盘"}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        conflicting_storage = [
            str(index + 1)
            for index, storage in enumerate(storage_list)
            if storage_interface_form_factor_consistent(
                storage.get("interface"), storage.get("form_factor")
            ) is False
            or storage_model_form_factor_consistent(
                storage.get("model"), storage.get("form_factor")
            ) is False
        ]
        if conflicting_storage:
            return {
                "type": "msg",
                "msg": (
                    f"第{'、'.join(conflicting_storage)}块硬盘的接口、型号与物理形态证据互相矛盾，"
                    "需按精确型号复核后再判断主板接口占用"
                ),
            }
        m2_layout = verified_m2_slot_layout(mb)
        m2_slots = verified_m2_slot_count(mb) or self._parse_num(mb.get("m2_slots", 0))
        m2_count = sum(1 for storage in storage_list if _storage_uses_m2(storage))
        m2_sata_count = sum(1 for storage in storage_list if _storage_uses_m2_sata(storage))
        if m2_count > 0 and m2_slots > 0 and m2_count > m2_slots:
            return {"type": "error",
                "msg": f"M.2硬盘数量【{m2_count}个】超过主板M.2接口数【{m2_slots}个】"}
        missing_interfaces = [
            str(index + 1)
            for index, storage in enumerate(storage_list)
            if not str(storage.get("interface") or "").strip()
        ]
        if missing_interfaces:
            return {
                "type": "msg",
                "msg": f"第{'、'.join(missing_interfaces)}块硬盘缺少接口信息，需复核M.2/NVMe/SATA类型",
            }
        msata_count = sum(
            1 for storage in storage_list
            if "MSATA" in self._normalize(storage.get("form_factor"))
            or "MSATA" in self._normalize(storage.get("interface"))
        )
        if msata_count:
            return {
                "type": "msg",
                "msg": f"检测到mSATA硬盘【{msata_count}个】，需复核主板专用mSATA插槽或转接方案",
            }
        unknown_sata_forms = [
            str(index + 1)
            for index, storage in enumerate(storage_list)
            if "SATA" in str(storage.get("interface") or "").upper()
            and not str(storage.get("form_factor") or "").strip()
        ]
        if unknown_sata_forms:
            return {
                "type": "msg",
                "msg": f"第{'、'.join(unknown_sata_forms)}块SATA硬盘缺少形态信息，需复核2.5/3.5英寸或M.2 SATA后再判断接口占用",
            }
        if m2_sata_count:
            if m2_layout is not None:
                support_slots = sum(
                    1 for slot in m2_layout if "sata" in slot.get("interfaces", [])
                )
            else:
                support_value = (
                    mb.get("m2_sata_slots")
                    or mb.get("m2_sata_support")
                    or mb.get("sata_m2_slots")
                )
                if support_value in (True, "true", "yes", "支持"):
                    support_slots = m2_sata_count
                else:
                    support_slots = self._parse_num(support_value)
            if m2_layout is not None and m2_sata_count > support_slots:
                return {"type": "error",
                    "msg": f"M.2 SATA硬盘数量【{m2_sata_count}个】超过主板M.2 SATA支持数【{support_slots}个】"}
            if m2_layout is None and support_slots and m2_sata_count > support_slots:
                return {"type": "error",
                    "msg": f"M.2 SATA硬盘数量【{m2_sata_count}个】超过主板M.2 SATA支持数【{support_slots}个】"}
            if m2_layout is None and not support_slots:
                return {"type": "warn",
                    "msg": "M.2 SATA硬盘需复核主板M.2插槽是否支持SATA模式；多数新主板M.2仅支持PCIe/NVMe"}
        if m2_count > 0 and not m2_slots:
            return {"type": "msg", "msg": "主板缺少M.2接口数量信息，需下单前复核"}
        if m2_layout is not None:
            sata_capable_slots = sorted(
                (
                    slot for slot in m2_layout
                    if "sata" in slot.get("interfaces", [])
                ),
                key=lambda slot: (_m2_slot_has_conditions(slot), slot["pcie_generation"]),
            )
            used_sata_slots = sata_capable_slots[:m2_sata_count]
            reserved_for_sata = {slot["slot_id"] for slot in used_sata_slots}
            m2_pcie_layout = [
                slot for slot in m2_layout
                if "pcie" in slot.get("interfaces", [])
                and slot["slot_id"] not in reserved_for_sata
            ]
            m2_pcie_count = m2_count - m2_sata_count
            m2_pcie_slots = len(m2_pcie_layout)
            if m2_pcie_count > m2_pcie_slots:
                return {
                    "type": "error",
                    "msg": f"M.2 PCIe硬盘数量【{m2_pcie_count}个】超过主板PCIe/NVMe M.2支持数【{m2_pcie_slots}个】",
                }
            downgrades, used_pcie_slots = _assign_m2_pcie_slots(storage_list, m2_pcie_layout)
            if downgrades:
                requested, available = downgrades[0]
                return {
                    "type": "warn",
                    "msg": (
                        f"PCIe Gen{requested} M.2 SSD可安装，但至少一块只能按Gen{available}运行；"
                        f"主板已核实M.2槽位为{_m2_layout_generation_summary(m2_layout)}。"
                        "除非复用已有硬盘、价格无溢价或用户明确接受降速，默认改选匹配代际的SSD"
                    ),
                }
            used_conditional_slots = [
                slot for slot in [*used_sata_slots, *used_pcie_slots]
                if _m2_slot_has_conditions(slot)
            ]
            if used_conditional_slots:
                details = []
                for slot in used_conditional_slots:
                    facts = [*(slot.get("conditions") or []), *(slot.get("shares_with") or [])]
                    details.append(f"{slot['slot_id']}: {'；'.join(facts)}")
                return {
                    "type": "msg",
                    "msg": "M.2槽位存在处理器或通道共享条件，需按主板说明书复核: " + "；".join(details),
                }
        elif any((_m2_pcie_generation(storage) or 0) >= 5 for storage in storage_list):
            return {
                "type": "msg",
                "msg": (
                    "所选PCIe 5.0 M.2 SSD缺少主板逐槽代际证据，不能确认能否按Gen5运行；"
                    "默认改选PCIe 4.0 SSD，或先按主板精确型号官网规格复核"
                ),
            }
        return {"type": "success", "msg": "硬盘接口兼容"}

    def check_sata_ports(self, storage_list, mb):
        """检查 SATA 设备数 vs 主板 SATA 口数。"""
        if not storage_list:
            return {"type": "skipped", "msg": "未选择硬盘，跳过SATA接口检查", "review_required": False}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        if any(not str(storage.get("interface") or "").strip() for storage in storage_list):
            return {
                "type": "skipped",
                "msg": "硬盘接口信息不足，SATA数量由硬盘接口复核项覆盖",
                "review_required": False,
            }
        sata_count = sum(
            1 for s in storage_list
            if "SATA" in str(s.get("interface") or "").upper()
            and "M.2" not in str(s.get("form_factor") or "").upper()
            and "MSATA" not in self._normalize(s.get("form_factor"))
            and "MSATA" not in self._normalize(s.get("interface"))
        )
        sata_ports = self._parse_num(mb.get("sata_ports", 0))
        if not sata_count:
            return {"type": "success", "msg": "未使用SATA设备，无需占用主板SATA接口"}
        if not sata_ports:
            return {"type": "msg", "msg": "主板缺少SATA接口数量信息，需下单前复核"}
        if sata_count > sata_ports:
            return {"type": "error",
                "msg": f"SATA设备【{sata_count}个】超过主板SATA口【{sata_ports}个】"}
        conditions = mb.get("sata_port_conditions") or []
        if conditions:
            return {
                "type": "msg",
                "msg": "SATA接口数量足够，但启用条件需复核: " + "；".join(conditions),
            }
        return {"type": "success", "msg": "SATA接口数量充足"}

    def check_psu_power(self, psu, cpu, gpu_list, extra_w=DEFAULT_NON_CORE_POWER_W):
        """检查电源功率是否满足整机功耗。

        余量公式: recommended = ceil((cpu_w + gpu_w + extra) * 1.35)
        extra_w 默认 50W (主板+内存+硬盘+风扇)。
        """
        if not psu:
            return {"type": "msg", "msg": "缺少必要组件电源"}
        if any(self._has_spec_conflict(gpu, "power_w") for gpu in (gpu_list or [])):
            return {"type": "msg", "msg": "显卡同型号目录记录的功耗互相冲突，电源功率需按精确SKU复核"}
        psu_w = self._parse_rated_wattage(psu)
        cpu_w = self._parse_num(infer_cpu_conservative_power_w(cpu), 0) if cpu else 0
        gpu_powers = [self._parse_num(g.get("power_w", 0)) for g in (gpu_list or [])]
        gpu_w = sum(gpu_powers)
        if not psu_w:
            return {"type": "msg", "msg": "电源缺少功率信息"}
        if cpu and not cpu_w:
            return {"type": "msg", "msg": "CPU缺少功耗信息，电源功率需人工复核"}
        if gpu_list and any(not value for value in gpu_powers):
            missing = [str(index + 1) for index, value in enumerate(gpu_powers) if not value]
            return {"type": "msg", "msg": f"第{'、'.join(missing)}张显卡缺少功耗信息，电源功率需人工复核"}
        recommended = recommended_psu_w(cpu_w, gpu_w, extra_w)
        if psu_w < recommended:
            return {"type": "error",
                "msg": f"电源功率【{psu_w}W】不足，建议≥{recommended}W (CPU {cpu_w}W + GPU {gpu_w}W + 其他 {extra_w}W ×{PSU_HEADROOM_FACTOR})"}
        margin = psu_w - recommended
        if margin < PSU_TIGHT_MARGIN_W:
            return {"type": "warn",
                "msg": f"电源功率【{psu_w}W】达到最低建议【{recommended}W】，但余量较小；建议≥{recommended + PSU_TIGHT_MARGIN_W}W留更多余量"}
        return {"type": "success",
            "msg": f"电源功率【{psu_w}W】充足，推荐功率{recommended}W，余量{margin}W"}

    def check_gpu_power_connector(self, gpu, psu):
        """检查显卡供电接口兼容性。"""
        if not gpu or not psu:
            return {}
        if self._has_spec_conflict(gpu, "power_connectors", "requires_16pin_psu"):
            return {"type": "msg", "msg": "显卡同型号目录记录的供电接口互相冲突，需按精确SKU复核线材"}
        incomplete = self._as_list(gpu.get("_overlay_incomplete_fields"))
        if GPU_POWER_EVIDENCE_FIELD in incomplete:
            return {"type": "msg", "msg": "用户显卡未提供供电接口或16pin需求事实，需下单前复核线材"}
        connector_value = gpu.get("power_connectors")
        if (
            connector_value in (None, "", [])
            and gpu.get("requires_16pin_psu") is not True
        ):
            return {"type": "msg", "msg": "显卡缺少供电接口信息，需下单前复核线材"}
        requires_16pin = infer_requires_16pin_gpu(gpu)
        native_16pin = infer_native_16pin_psu(psu)
        if requires_16pin and native_16pin is True:
            return {"type": "success", "msg": "显卡16pin供电与电源原生接口匹配"}
        if requires_16pin and native_16pin is False:
            return {"type": "warn",
                "msg": "显卡需要16pin供电，当前电源未标明原生16pin接口，需复核线材；无原生线材时可使用转接线"}
        if requires_16pin:
            return {"type": "msg",
                "msg": "显卡需要16pin供电，电源缺少原生接口字段，需下单前复核线材；无原生线材时可使用转接线"}
        return {"type": "success", "msg": "显卡未声明16pin供电需求"}

    def check_cooler_case(self, cooler, case):
        """检查散热器与机箱兼容性: 风冷高度/水冷冷排 vs 机箱限制。"""
        if not cooler:
            return {"type": "msg", "msg": "缺少必要组件散热"}
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        cooler = enrich_item("coolers", cooler)
        cooler_type = cooler.get("type", "air")
        if cooler_type == "air":
            cooler_height = self._parse_num(cooler.get("height_mm", 0))
            case_limit = self._parse_num(case.get("cpu_cooler_height_mm", 0))
            if cooler_height and case_limit:
                if cooler_height > case_limit:
                    return {"type": "error",
                        "msg": f"风冷高度【{cooler_height}mm】超过机箱限制【{case_limit}mm】"}
                if case_limit - cooler_height < CPU_COOLER_CLEARANCE_WARNING_MM:
                    return {"type": "warn",
                        "msg": f"风冷高度【{cooler_height}mm】接近机箱限制【{case_limit}mm】，未留足{CPU_COOLER_CLEARANCE_WARNING_MM}mm安装余量"}
                return {"type": "success", "msg": "风冷高度在机箱限制内"}
        elif cooler_type in ("liquid", "water", "水冷"):
            radiator = cooler.get("radiator_mm", "")
            rad_support = self._as_list(case.get("radiator_support"))
            if not radiator:
                return {"type": "msg", "msg": "水冷缺少冷排尺寸，无法核对机箱冷排位"}
            if not rad_support:
                return {"type": "msg", "msg": "机箱缺少冷排位信息，需按水冷冷排尺寸复核"}
            if radiator and rad_support:
                requested = int(self._parse_num(radiator))
                listed_sizes = {
                    int(size)
                    for value in rad_support
                    for size in re.findall(r"(?<!\d)(120|140|240|280|360|420|480)(?!\d)", str(value))
                }
                supported = any(
                    requested in self.RADIATOR_SIZE_COMPATIBILITY.get(size, {size})
                    for size in listed_sizes
                )
                if not supported:
                    return {"type": "error",
                        "msg": f"冷排【{radiator}】不在机箱支持范围【{rad_support}】"}
                return {"type": "success", "msg": "标称冷排规格在机箱支持范围内；厚度和管路走线仍按具体型号复核"}
        return {}

    def check_case_motherboard(self, case, mb):
        """检查机箱是否支持主板版型。

        逻辑: 机箱支持列表中的每种版型，通过 FORM_FACTOR_MAP 向下兼容
        更小的版型。如果主板版型出现在任何机箱支持版型的兼容列表中，
        则机箱可以装下该主板。
        """
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        if not mb:
            return {"type": "msg", "msg": "缺少必要组件主板"}
        mb_ff = mb.get("form_factor", "")
        case_support = self._as_list(case.get("motherboard_support"))
        if not mb_ff or not case_support:
            return {"type": "msg", "msg": "机箱或主板缺少版型信息，需下单前复核"}
        ff_normalized = self._normalize_form_factor(mb_ff)
        support_normalized = [self._normalize_form_factor(s) for s in case_support]
        # 直接匹配
        if ff_normalized in support_normalized:
            return {"type": "success", "msg": f"机箱支持{mb_ff}版型"}
        # 向下兼容: 机箱支持的每种版型可以兼容更小的主板版型
        for case_ff in support_normalized:
            compatible_list = self.FORM_FACTOR_MAP.get(case_ff, [])
            if ff_normalized in compatible_list:
                return {"type": "success", "msg": f"机箱支持{mb_ff}版型(通过{case_ff}向下兼容)"}
        return {"type": "error",
            "msg": f"机箱与主板版型不匹配，机箱支持【{'/'.join(case_support)}】，主板【{mb_ff}】"}

    def check_case_psu(self, case, psu):
        """检查机箱电源位 vs 电源尺寸。"""
        if not case:
            return {"type": "msg", "msg": "缺少必要组件机箱"}
        if not psu:
            return {}
        case_model = str(case.get("model", ""))
        case_psu_support = [
            self._normalize(normalize_psu_form_factor(value))
            for value in self._as_list(case.get("psu_support"))
        ]
        model_special = any(
            term in case_model.upper()
            for term in ("ITX", "MINI", "SFX", "NAS", "HTPC", "卧式", "小型", "紧凑")
        )
        small_psu_forms = ("SFX", "SFXL", "TFX", "FLEX")
        small_psu_only = "ATX" not in case_psu_support and any(s in small_psu_forms for s in case_psu_support)
        motherboard_support = [self._normalize(s) for s in self._as_list(case.get("motherboard_support"))]
        compact_hybrid = (
            bool(motherboard_support)
            and "ATX" not in motherboard_support
            and any(s in small_psu_forms for s in case_psu_support)
        )
        special_case = model_special or small_psu_only or compact_hybrid
        psu_size = self._normalize(normalize_psu_form_factor(psu.get("form_factor")))
        if not psu_size:
            return {"type": "skipped",
                "msg": "电源缺少规格字段，普通机箱虽通常使用ATX电源，仍需确认实际为ATX/SFX/SFX-L/FLEX及限长/限高"}
        if not case_psu_support:
            return {"type": "msg", "msg": "机箱缺少电源规格支持信息，需下单前复核"}

        if "ATX" in case_psu_support and not special_case and psu_size in small_psu_forms:
            return {"type": "error",
                "msg": "普通ATX/MATX机箱默认不使用SFX/SFX-L/FLEX/TFX小电源；若明确复用小电源，需单独确认转接支架、线材长度和电源限长/限高"}

        psu_len = self._parse_num(psu.get("length_mm", 0))
        case_limit = self._parse_num(
            case.get("psu_length_mm", 0) or case.get("psu_max_length_mm", 0) or case.get("psu_clearance_mm", 0)
        )
        recommended_limit = self._parse_num(case.get("psu_length_recommended_mm", 0))
        length_condition = str(case.get("psu_length_condition") or "").strip()
        if psu_size in case_psu_support:
            if special_case and (not case_limit or not psu_len):
                return {"type": "skipped",
                    "msg": "小机箱或特殊电源位缺少机箱电源限长或电源长度字段，需下单前复核限长/限高、转接支架、线材弯折和硬盘笼空间"}
            if case_limit and psu_len and psu_len > case_limit:
                return {"type": "error",
                    "msg": f"电源长度【{psu_len}mm】超过机箱电源位限制【{case_limit}mm】"}
            if recommended_limit and psu_len and psu_len > recommended_limit:
                condition_text = length_condition.rstrip("。；，,; ")
                detail = f"；{condition_text}" if condition_text else ""
                return {"type": "warn",
                    "msg": f"电源长度【{psu_len}mm】未超过物理上限【{case_limit}mm】，但超过保守建议【{recommended_limit}mm】{detail}，需按冷排、显卡、硬盘笼和线材布局复核"}
            if length_condition and case_limit and psu_len and not recommended_limit:
                return {"type": "warn",
                    "msg": f"电源长度【{psu_len}mm】未超过物理上限【{case_limit}mm】，但该上限存在布局条件；{length_condition}，需复核实际安装组合"}
            if (
                case_limit
                and psu_len
                and case_limit - psu_len < PSU_CASE_CLEARANCE_WARNING_MM
            ):
                return {"type": "warn",
                    "msg": f"电源长度【{psu_len}mm】接近机箱电源位限制【{case_limit}mm】，需复核线材弯折、限高和硬盘笼空间"}
            if case_limit and not psu_len and special_case:
                return {"type": "msg",
                    "msg": f"机箱电源位限制【{case_limit}mm】，电源缺少长度字段，需下单前复核限长/限高和线材空间"}
            return {"type": "success", "msg": "机箱和电源规格匹配"}
        return {"type": "error",
            "msg": f"机箱和电源规格不匹配，机箱支持【{case.get('psu_support')}】，电源【{psu.get('form_factor', psu_size)}】"}

    # --- 主入口 ---

    def _skipped(self, msg, review_required=True):
        return {"type": "skipped", "msg": msg, "review_required": review_required}

    def _add_check(self, checks, name, result, skipped_msg="无可检查项", skipped_review_required=True):
        checks.append((name, result or self._skipped(skipped_msg, skipped_review_required)))

    def _strict_completeness_checks(
        self, cpu, mb, mem, storage, gpus, psu, cooler, case, strict, missing_ids
    ):
        checks = []
        for missing_id in (missing_ids or []):
            checks.append(("ID校验", {"type": "error", "msg": f"未找到配件ID: {missing_id}"}))
        parts = [cpu, mb, *mem, *storage, *gpus, psu, cooler, case]
        for item in (part for part in parts if part):
            conflicts = item.get("spec_conflicts", [])
            if conflicts:
                checks.append(("目录规格冲突", {
                    "type": "msg",
                    "msg": f"配件 {item.get('id')} 的同型号目录记录存在冲突字段: {', '.join(conflicts)}；需按精确SKU复核",
                }))
        if strict:
            required = [
                ("CPU", cpu),
                ("主板", mb),
                ("内存", mem),
                ("硬盘", storage),
                ("电源", psu),
                ("散热", cooler),
                ("机箱", case),
            ]
            for label, value in required:
                if value is None or value == []:
                    checks.append(("完整性", {"type": "error", "msg": f"严格模式缺少{label}"}))
            if not gpus and not self._cpu_has_integrated_graphics(cpu):
                checks.append(("完整性", {"type": "error", "msg": "严格模式缺少独显，且CPU未确认带核显"}))
            for item in (part for part in parts if part):
                missing = item.get("_overlay_incomplete_fields", [])
                if missing:
                    checks.append(("用户配件完整性", {
                        "type": "msg",
                        "msg": f"用户配件 {item.get('id')} 缺少兼容关键字段: {', '.join(missing)}",
                    }))
        return checks

    def check_extra_pcie_slot(self, mb, gpus):
        """Check an explicit PCIe add-in-card requirement without guessing GPU width."""
        if not mb:
            return None
        slot_count = pcie_physical_slot_count(mb)
        if slot_count is None:
            return {
                "type": "msg",
                "msg": "主板物理PCIe插槽布局未核实，不能确认独显之外还能安装采集卡或扩展卡",
            }
        needed = len(gpus) + 1
        if slot_count < needed:
            return {
                "type": "error",
                "msg": f"扩展卡需求至少需要{needed}个物理PCIe插槽，主板仅核实{slot_count}个",
            }
        if not gpus:
            return {
                "type": "success",
                "msg": f"主板已核实{slot_count}个物理PCIe插槽，可安装一张扩展卡",
            }
        sharing = sorted({
            resource
            for slot in mb.get("pcie_slot_layout", [])
            for resource in slot.get("shares_with", [])
        })
        suffix = f"；另需核对与{','.join(sharing)}的共享条件" if sharing else ""
        return {
            "type": "msg",
            "msg": (
                f"主板已核实{slot_count}个物理PCIe插槽，但独显厚度和槽间距可能遮挡扩展槽；"
                f"需按显卡槽厚与采集卡位置复核{suffix}"
            ),
        }

    def check_required_usb4(self, mb):
        if not mb:
            return None
        ports = verified_usb4_ports(mb)
        if ports:
            conditions = mb.get("usb4_disable_conditions") or []
            sharing = mb.get("usb4_shares_with") or []
            if conditions or sharing:
                details = list(conditions)
                if sharing:
                    details.append("与" + "/".join(sharing) + "共享带宽")
                return {
                    "type": "msg",
                    "msg": f"主板有{ports}个已核实后置USB4端口，但存在条件：{'；'.join(details)}",
                }
            return {"type": "success", "msg": f"主板有{ports}个已核实后置USB4端口"}
        if mb.get("usb4_status") == "none_verified":
            return {"type": "error", "msg": "主板官方后置I/O已核实未提供USB4端口"}
        return {"type": "msg", "msg": "主板USB4能力尚未核实，不能满足明确USB4需求"}

    def check_required_thunderbolt(self, mb):
        if not mb:
            return None
        ports = verified_thunderbolt_ports(mb)
        if ports:
            version = mb.get("thunderbolt_version")
            return {
                "type": "success",
                "msg": f"主板有{ports}个已核实后置Thunderbolt {version}端口",
            }
        status = mb.get("thunderbolt_status")
        if status == "header_only":
            return {
                "type": "error",
                "msg": "主板仅有雷电扩展针脚，没有已核实后置雷电端口，不能直接满足雷电口需求",
            }
        if status == "none_verified":
            return {"type": "error", "msg": "主板官方后置I/O已核实未提供雷电端口"}
        return {"type": "msg", "msg": "主板雷电能力尚未核实，不能满足明确雷电需求"}

    def _compatibility_checks(
        self, cpu, mb, mem, storage, gpus, psu, cooler, case, requirements=None
    ):
        checks = []
        requirements = requirements or {}
        self._add_check(checks, "CPU↔主板", self.check_cpu_motherboard(cpu, mb))
        self._add_check(checks, "散热↔CPU", self.check_cooler_cpu(cooler, cpu))
        self._add_check(checks, "散热能力", self.check_cooler_thermal_capacity(cooler, cpu))
        if not gpus and self._cpu_has_integrated_graphics(cpu):
            display_outputs = self._motherboard_display_outputs(mb)
            self._add_check(
                checks,
                "显示输出",
                (
                    {
                        "type": "success",
                        "msg": (
                            "未选择独显，CPU已确认带核显；主板已核实视频输出接口: "
                            + "/".join(display_outputs)
                        ),
                    }
                    if display_outputs
                    else {
                        "type": "msg",
                        "msg": "未选择独显，CPU已确认带核显；主板视频输出接口未记录，需复核后才能完整通过",
                    }
                ),
            )
        mem_results = self.check_memory_motherboard(mem, mb)
        for r in mem_results:
            self._add_check(checks, "内存↔主板", r)
        self._add_check(checks, "内存插槽数", self.check_memory_slots(mem, mb), "未检查内存插槽数量")
        self._add_check(checks, "内存容量", self.check_memory_capacity(mem, mb), "未检查内存容量上限")
        for i, gpu in enumerate(gpus):
            self._add_check(checks, "显卡↔机箱", self.check_gpu_case(gpu, case, str(i+1) if len(gpus)>1 else ""))
        if not gpus:
            self._add_check(
                checks,
                "显卡↔机箱",
                {},
                "未选择显卡，跳过显卡机箱限长检查",
                skipped_review_required=False,
            )
        self._add_check(checks, "硬盘↔主板", self.check_storage_motherboard(storage, mb))
        self._add_check(checks, "SATA接口", self.check_sata_ports(storage, mb), "没有SATA设备或缺少SATA信息")
        self._add_check(checks, "电源功率", self.check_psu_power(psu, cpu, gpus))
        for i, gpu in enumerate(gpus):
            label = f"显卡{i+1}供电" if len(gpus) > 1 else "显卡供电"
            self._add_check(checks, label, self.check_gpu_power_connector(gpu, psu), "显卡未声明特殊供电需求")
        if not gpus:
            self._add_check(
                checks,
                "显卡供电",
                {},
                "未选择显卡，跳过显卡供电检查",
                skipped_review_required=False,
            )
        self._add_check(checks, "散热↔机箱", self.check_cooler_case(cooler, case))
        self._add_check(checks, "机箱↔主板", self.check_case_motherboard(case, mb))
        self._add_check(checks, "机箱↔电源", self.check_case_psu(case, psu), "未检查机箱电源尺寸")
        if requirements.get("extra_pcie_slot"):
            self._add_check(
                checks,
                "扩展卡槽位",
                self.check_extra_pcie_slot(mb, gpus),
                "未检查采集卡或扩展卡槽位",
            )
        if requirements.get("usb4"):
            self._add_check(checks, "USB4需求", self.check_required_usb4(mb))
        if requirements.get("thunderbolt"):
            self._add_check(checks, "雷电需求", self.check_required_thunderbolt(mb))
        return checks

    def _summarize_checks(self, checks):
        checks = [(name, dict(result)) for name, result in checks]
        severity = {"error": 0, "warn": 0, "success": 0, "msg": 0, "skipped": 0}
        for _, r in checks:
            t = r.get("type", "")
            severity[t] = severity.get(t, 0) + 1
        if severity["error"] > 0:
            overall = "fail"
        elif severity["warn"] > 0:
            overall = "warn"
        else:
            overall = "pass"
        review_count = sum(
            1
            for _, check in checks
            if check.get("type") in ("warn", "msg")
            or (check.get("type") == "skipped" and check.get("review_required", True))
        )
        compatible = severity["error"] == 0
        review_required = review_count > 0
        complete = compatible and not review_required
        status = "incompatible" if not compatible else ("needs_review" if review_required else "complete")
        return {
            "overall": overall,
            "status": status,
            "compatible": compatible,
            "complete": complete,
            "review_required": review_required,
            "review_count": review_count,
            "checks": checks,
            "severity": severity,
        }

    def check_all(self, build, strict=False, missing_ids=None, requirements=None):
        """检查完整配置的兼容性。

        Args:
            build: dict with keys: cpu, motherboard, memory (list),
                   storage (list), gpu (list), psu, cooler, case
            strict: final-build mode. Missing core parts become errors.
            missing_ids: IDs passed by the caller but not found in the library.
        Returns:
            Compatibility and evidence completeness are reported separately.
            ``overall`` keeps the legacy pass/warn/fail contract.
        """
        cpu = build.get("cpu")
        mb = build.get("motherboard")
        mem = build.get("memory", [])
        storage = build.get("storage", [])
        gpus = build.get("gpu", [])
        psu = build.get("psu")
        cooler = build.get("cooler")
        case = build.get("case")
        completeness = self._strict_completeness_checks(
            cpu, mb, mem, storage, gpus, psu, cooler, case, strict, missing_ids
        )
        compatibility = self._compatibility_checks(
            cpu, mb, mem, storage, gpus, psu, cooler, case, requirements
        )
        return self._summarize_checks(completeness + compatibility)


def load_components(overlay_paths=None):
    """加载 components.yaml 和 cases.yaml。"""
    sections = load_catalog_sections(DATA)
    sections, _, alias_index = resolve_catalog(sections, overlay_paths or [], data_dir=DATA)
    by_id = {}
    for section, items in sections.items():
        for item in items:
            by_id[item["id"]] = enrich_resolved_item(section, item)
    return by_id, alias_index


def main():
    parser = argparse.ArgumentParser(
        description="装机兼容性检查 — 程序化基础兼容性检查")
    parser.add_argument("--cpu", help="CPU ID")
    parser.add_argument("--mb", help="主板 ID")
    parser.add_argument("--mem", action="append", help="内存 ID (可多次指定)")
    parser.add_argument("--storage", action="append", help="硬盘 ID (可多次指定)")
    parser.add_argument("--gpu", action="append", help="显卡 ID (可多次指定)")
    parser.add_argument("--psu", help="电源 ID")
    parser.add_argument("--cooler", help="散热 ID")
    parser.add_argument("--case", help="机箱 ID")
    parser.add_argument("--overlay", action="append", default=[], help="显式用户 overlay JSON；可重复，后传报价优先")
    parser.add_argument("--strict", action="store_true", help="严格模式: 最终整机必须包含核心配件")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="完整度门禁: 有警告、待复核信息或需复核的跳过项时返回退出码2",
    )
    parser.add_argument(
        "--require-extra-pcie-slot",
        action="store_true",
        help="明确需要内置采集卡/声卡/网卡等PCIe扩展卡；独显厚度和槽间距会进入复核",
    )
    parser.add_argument(
        "--require-usb4",
        action="store_true",
        help="明确要求已核实的后置USB4端口；普通USB-C和未知能力不算满足",
    )
    parser.add_argument(
        "--require-thunderbolt",
        action="store_true",
        help="明确要求已核实的后置雷电端口；扩展针脚不算满足",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    try:
        by_id, alias_index = load_components(args.overlay)
    except OverlayError as exc:
        print(json.dumps({"ok": False, "errors": [exc.as_dict()]}, ensure_ascii=False), file=sys.stderr)
        return 2
    missing_ids = []

    def get(id_str):
        if not id_str:
            return None
        try:
            resolved_id = resolve_id(id_str, by_id, alias_index)
        except OverlayError as exc:
            print(json.dumps({"ok": False, "errors": [exc.as_dict()]}, ensure_ascii=False), file=sys.stderr)
            raise SystemExit(2)
        item = by_id.get(resolved_id) if resolved_id else None
        if item is None:
            missing_ids.append(id_str)
        return item

    def get_list(id_list):
        items = []
        for id_str in id_list or []:
            item = get(id_str)
            if item is not None:
                items.append(item)
        return items

    build = {
        "cpu": get(args.cpu),
        "motherboard": get(args.mb),
        "memory": get_list(args.mem),
        "storage": get_list(args.storage),
        "gpu": get_list(args.gpu),
        "psu": get(args.psu),
        "cooler": get(args.cooler),
        "case": get(args.case),
    }

    checker = CompatibilityChecker()
    result = checker.check_all(
        build,
        strict=args.strict,
        missing_ids=missing_ids,
        requirements={
            "extra_pcie_slot": args.require_extra_pcie_slot,
            "usb4": args.require_usb4,
            "thunderbolt": args.require_thunderbolt,
        },
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"兼容性检查结果: {result['overall'].upper()}")
        print(f"检查完整度: {result['status'].upper()}")
        print(f"  错误: {result['severity']['error']}, "
              f"警告: {result['severity']['warn']}, "
              f"通过: {result['severity']['success']}, "
              f"跳过: {result['severity'].get('skipped', 0)}")
        print()
        for name, check in result["checks"]:
            if check.get("type"):
                icon = {"error": "❌", "warn": "⚠️", "success": "✅", "msg": "ℹ️", "skipped": "↷"}.get(check["type"], "  ")
                print(f"  {icon} {name}: {check['msg']}")
    if result["overall"] == "fail":
        return 1
    if args.require_complete and not result["complete"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
