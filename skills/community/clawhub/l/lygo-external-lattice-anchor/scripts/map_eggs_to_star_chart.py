#!/usr/bin/env python3
"""
Map classic + sovereign eggs into Haven Star Chart *proposal* nodes (does not live-write chart).

Output JSON for steward ingest via lygo-haven-star-chart (consent + gate).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

SIG = "Delta9Phi963-EXTERNAL-LATTICE-ANCHOR-v1.0"


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
            return p
    return Path.cwd()


def load(p: Path):
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def egg_nodes_from_sovereign(reg: dict) -> list[dict]:
    nodes = []
    eggs = reg.get("eggs") or {}
    if isinstance(eggs, dict):
        items = eggs.items()
    else:
        items = []
    for eid, meta in items:
        leaf = meta.get("leaf_hash") or meta.get("content_sha256") or ""
        nodes.append(
            {
                "proposal_id": f"egg-sov-{eid}",
                "kind": "kernel_egg",
                "layer": "B_sovereign",
                "egg_id": eid,
                "label": f"Sovereign egg: {eid}",
                "star_role": "kernel_egg",
                "content_sha256": meta.get("content_sha256"),
                "leaf_hash": leaf,
                "version": meta.get("version"),
                "egg_kind": meta.get("kind"),
                "registry_merkle_root": reg.get("registry_merkle_root"),
                "links": {
                    "snapshot": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/sovereign_seeds_snapshot/registry.json",
                    "seeder_skill": "https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder",
                },
                "protection": {
                    "verify_before_load": True,
                    "quarantine_on_mismatch": True,
                },
            }
        )
    return nodes


def egg_nodes_from_classic(reg: dict) -> list[dict]:
    nodes = []
    eggs = reg.get("eggs") or []
    if isinstance(eggs, list):
        for e in eggs:
            if not isinstance(e, dict):
                continue
            eid = e.get("egg_id") or e.get("id")
            transport = e.get("transport") or {}
            nodes.append(
                {
                    "proposal_id": f"egg-cls-{eid}",
                    "kind": "kernel_egg",
                    "layer": "A_classic",
                    "egg_id": eid,
                    "label": f"Classic egg: {eid}",
                    "star_role": "kernel_egg",
                    "content_sha256": transport.get("content_sha256") or e.get("content_sha256"),
                    "merkle_root": e.get("merkle_root"),
                    "registry_merkle_root": reg.get("registry_merkle_root"),
                    "links": {
                        "retrieval": "https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html",
                        "planter_skill": "https://clawhub.ai/deepseekoracle/skills/lygo-kernel-egg-planter",
                    },
                    "protection": {
                        "verify_before_load": True,
                        "four_pillars": True,
                    },
                }
            )
    elif isinstance(eggs, dict):
        for eid, e in eggs.items():
            nodes.append(
                {
                    "proposal_id": f"egg-cls-{eid}",
                    "kind": "kernel_egg",
                    "layer": "A_classic",
                    "egg_id": eid,
                    "label": f"Classic egg: {eid}",
                    "star_role": "kernel_egg",
                    "content_sha256": (e or {}).get("content_sha256"),
                    "registry_merkle_root": reg.get("registry_merkle_root"),
                }
            )
    return nodes


def surface_nodes() -> list[dict]:
    """Fixed world-network surfaces as star nodes."""
    surfaces = [
        ("surface-pages-stack", "GitHub Pages stack mirror", "https://deepseekoracle.github.io/lygo-protocol-stack/", "public_mirror"),
        ("surface-anchors", "Immutable Anchors ledger", "https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/network_builder/IMMUTABLE_ANCHORS.json", "ledger"),
        ("surface-star-chart", "Haven Star Chart LIVE", "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html", "world_map"),
        ("surface-hf-stack", "HF stack dataset", "https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack", "free_server"),
        ("surface-hf-music", "HF music stream CAS", "https://huggingface.co/datasets/DeepSeekOracle/excavationpro-music-stream", "free_server"),
        ("surface-clawhub", "ClawHub publisher", "https://clawhub.ai/deepseekoracle", "skill_registry"),
        ("surface-eternalhaven", "Eternal Haven hub", "https://eternalhaven.ca/", "public_hub"),
        ("surface-music-license", "LYGO Music License", "https://eternalhaven.ca/lygo-music-license.html", "rights"),
    ]
    out = []
    for pid, label, url, role in surfaces:
        out.append(
            {
                "proposal_id": pid,
                "kind": "lattice_surface",
                "layer": "C_external",
                "label": label,
                "star_role": role,
                "url": url,
                "protection": {"public_verify": True, "user_facing": True},
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-root", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    stack = Path(args.stack_root).resolve() if args.stack_root else stack_root()

    classic = load(stack / "data" / "kernel_eggs" / "registry.json") or load(
        stack / "docs" / "KernelEggRegistry.json"
    ) or {}
    sovereign = load(stack / "data" / "sovereign_seeds" / "registry.json") or load(
        stack / "docs" / "sovereign_seeds_snapshot" / "registry.json"
    ) or {}

    proposals = []
    if isinstance(classic, dict):
        proposals.extend(egg_nodes_from_classic(classic))
    if isinstance(sovereign, dict):
        proposals.extend(egg_nodes_from_sovereign(sovereign))
    proposals.extend(surface_nodes())

    bundle = {
        "signature": SIG,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "purpose": "Haven Star Chart proposals — steward gate + consent before LIVE ingest",
        "chart_live": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "portal": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html",
        "skill_gate": "lygo-haven-star-chart",
        "count": len(proposals),
        "proposals": proposals,
        "sync_note": "Do NOT auto-ingest. Human runs haven star chart gate with --i-consent.",
    }
    raw = json.dumps(bundle, sort_keys=True, separators=(",", ":")).encode("utf-8")
    bundle["bundle_sha256"] = hashlib.sha256(raw).hexdigest()

    out = Path(args.out) if args.out else stack / "docs" / "star_chart_egg_map_proposals.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "STAR_MAP_OK", "out": str(out), "proposals": len(proposals)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
