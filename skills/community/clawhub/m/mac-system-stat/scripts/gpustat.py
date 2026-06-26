#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from _common import bytes_human, clamp_percent, json_dump, machine_meta, run
from _swift_helper import emit_failure, run_helper


SYSTEM_PROFILER = "/usr/sbin/system_profiler"


def system_profiler_gpu() -> List[Dict[str, Any]]:
    out = run([SYSTEM_PROFILER, "SPDisplaysDataType", "-json"], timeout=30)
    try:
        data = json.loads(out)
    except Exception:
        return []
    cards = []
    for item in data.get("SPDisplaysDataType", []):
        cards.append(
            {
                "name": item.get("sppci_model") or item.get("_name"),
                "vendor": item.get("spdisplays_vendor"),
                "cores": int(item["sppci_cores"]) if str(item.get("sppci_cores", "")).isdigit() else None,
                "metal_family": item.get("spdisplays_mtlgpufamilysupport"),
                "bus": item.get("sppci_bus"),
            }
        )
    return cards


def select_card(cards: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not cards:
        return {}
    preferred = [card for card in cards if card.get("performance_statistics")]
    ranked = preferred or cards
    ranked.sort(key=lambda card: (card.get("gpu_core_count") or 0, card.get("registry_id") or 0), reverse=True)
    return ranked[0]


def main() -> int:
    root = Path(__file__).resolve().parent
    profiler_cards = system_profiler_gpu()

    try:
        helper = run_helper(root, "gpustat", timeout=30)
    except Exception as e:
        return emit_failure(
            "gpustat",
            f"Swift IOKit GPU helper failed to build or run: {e}",
            [
                "Verify Command Line Tools / swiftc availability.",
                "If the helper builds but returns no cards, re-check IOAccelerator registry matching on this macOS build.",
            ],
        )

    cards = helper.get("cards", [])
    chosen = select_card(cards)
    perf = chosen.get("performance_statistics", {})

    payload = {
        **machine_meta(),
        "kind": "gpustat",
        "implemented": helper.get("implemented", True),
        "supported": bool(helper.get("supported")) and bool(perf),
        "gpu": {
            "model": chosen.get("model") or (profiler_cards[0]["name"] if profiler_cards else None),
            "accelerator_class": chosen.get("accelerator_class"),
            "core_count": chosen.get("gpu_core_count") or (profiler_cards[0].get("cores") if profiler_cards else None),
            "cards": profiler_cards,
            "registry_cards": cards,
        },
        "utilization_percent": {
            "device": clamp_percent(perf.get("Device Utilization %")) if perf else None,
            "renderer": clamp_percent(perf.get("Renderer Utilization %")) if perf else None,
            "tiler": clamp_percent(perf.get("Tiler Utilization %")) if perf else None,
        },
        "memory": {
            "allocated_system_bytes": perf.get("Alloc system memory"),
            "allocated_system_human": bytes_human(perf.get("Alloc system memory")) if perf else None,
            "in_use_system_bytes": perf.get("In use system memory"),
            "in_use_system_human": bytes_human(perf.get("In use system memory")) if perf else None,
            "driver_in_use_system_bytes": perf.get("In use system memory (driver)"),
            "driver_in_use_system_human": bytes_human(perf.get("In use system memory (driver)")) if perf else None,
        },
        "counters": {
            "recovery_count": perf.get("recoveryCount"),
            "last_recovery_time": perf.get("lastRecoveryTime"),
            "split_scene_count": perf.get("SplitSceneCount"),
            "tiled_scene_bytes": perf.get("TiledSceneBytes"),
            "allocated_parameter_buffer_bytes": perf.get("Allocated PB Size"),
        },
        "source": {
            "system_profiler_cards": profiler_cards,
            "registry_card_count": len(cards),
            "registry_notes": helper.get("notes", []),
        },
        "notes": helper.get("notes", []) if perf else helper.get("notes", []) + ["IOAccelerator PerformanceStatistics not found on this host / OS build."],
    }
    json_dump(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
