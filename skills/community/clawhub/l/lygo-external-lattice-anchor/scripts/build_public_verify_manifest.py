#!/usr/bin/env python3
"""
Build a Public Verify Manifest that links Layer A/B local roots to worldwide public surfaces.

Does NOT publish. Consent not required for dry manifest build.
Signature: Delta9Phi963-EXTERNAL-LATTICE-ANCHOR-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

SIG = "Delta9Phi963-EXTERNAL-LATTICE-ANCHOR-v1.1"


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    # skill -> docs/skills/X or .grok/skills/X
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
            return p
        if (p / "tools").is_dir() and (p / "docs").is_dir():
            return p
    return Path.cwd()


def sha_file(p: Path) -> str | None:
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path) -> dict | list | None:
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-root", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    stack = Path(args.stack_root).resolve() if args.stack_root else stack_root()

    classic_reg = stack / "data" / "kernel_eggs" / "registry.json"
    classic_docs = stack / "docs" / "KernelEggRegistry.json"
    sovereign_reg = stack / "data" / "sovereign_seeds" / "registry.json"
    sovereign_snap = stack / "docs" / "sovereign_seeds_snapshot" / "registry.json"
    anchors = stack / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json"
    star_data = stack / "docs" / "haven_star_chart_data.json"
    if not star_data.is_file():
        star_data = stack / "docs" / "haven_star_chart" / "haven_star_chart_data.json"
    star_feed = stack / "docs" / "haven_star_chart" / "haven_star_chart_feed.json"
    layers_run = stack / "tests" / "kernel_layers_last_run.json"

    classic = load_json(classic_reg) or load_json(classic_docs) or {}
    sovereign = load_json(sovereign_reg) or load_json(sovereign_snap) or {}
    anchor_doc = load_json(anchors) or {}

    public_endpoints = [
        {
            "id": "immutable_anchors",
            "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/network_builder/IMMUTABLE_ANCHORS.json",
            "role": "ledger",
            "verify": "http_required",
            "mirror": "https://cdn.jsdelivr.net/gh/DeepSeekOracle/lygo-protocol-stack@main/docs/network_builder/IMMUTABLE_ANCHORS.json",
        },
        {
            "id": "kernel_egg_registry_pages",
            "url": "https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRegistry.json",
            "role": "classic_egg_registry_public",
            "verify": "http_soft",
            "source": "docs/KernelEggRegistry.json after user git push",
        },
        {
            "id": "kernel_egg_retrieval",
            "url": "https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html",
            "role": "public_verify_ui",
            "verify": "http_required",
        },
        {
            "id": "haven_star_chart",
            "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
            "role": "world_map",
            "verify": "http_required",
        },
        {
            "id": "haven_star_chart_portal",
            "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html",
            "role": "agent_submit_portal",
            "verify": "http_required",
        },
        {
            "id": "sovereign_seeds_snapshot",
            "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/sovereign_seeds_snapshot/registry.json",
            "role": "sovereign_registry_public_mirror",
            "verify": "http_soft",
        },
        {
            "id": "hf_music_stream",
            "url": "https://huggingface.co/datasets/DeepSeekOracle/excavationpro-music-stream",
            "role": "free_public_media_cas",
            "verify": "http_soft",
        },
        {
            "id": "hf_stack_dataset",
            "url": "https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack",
            "role": "stack_dataset_mirror",
            "verify": "http_soft",
        },
        {
            "id": "pages_stack",
            "url": "https://deepseekoracle.github.io/lygo-protocol-stack/",
            "role": "public_http_mirror",
            "verify": "http_required",
        },
        {
            "id": "clawhub_publisher",
            "url": "https://clawhub.ai/deepseekoracle",
            "role": "skill_registry",
            "verify": "http_soft",
        },
        {
            "id": "clawhub_living_mesh",
            "url": "https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh",
            "role": "layer_d_skill",
            "verify": "http_soft",
        },
        {
            "id": "living_mesh_layer_doc",
            "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/LIVING_MESH_LAYER.md",
            "role": "layer_d_docs",
            "verify": "http_soft",
        },
        {
            "id": "eternalhaven_hub",
            "url": "https://eternalhaven.ca/",
            "role": "public_hub",
            "verify": "http_required",
        },
        {
            "id": "world_lattice_doc",
            "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/WORLD_LATTICE_LAYER.md",
            "role": "docs",
            "verify": "http_soft",
        },
    ]

    def layer_summary(reg: dict, name: str) -> dict:
        if not reg:
            return {"name": name, "present": False}
        eggs = reg.get("eggs") or []
        if isinstance(eggs, dict):
            count = len(eggs)
            sample = list(eggs.keys())[:12]
        elif isinstance(eggs, list):
            count = len(eggs)
            sample = [e.get("egg_id") for e in eggs[:12] if isinstance(e, dict)]
        else:
            count = 0
            sample = []
        return {
            "name": name,
            "present": True,
            "registry_merkle_root": reg.get("registry_merkle_root"),
            "egg_count": count,
            "sample_egg_ids": sample,
            "signature": reg.get("signature") or reg.get("seeder"),
        }

    star = load_json(star_data)
    star_meta = {"present": bool(star)}
    if isinstance(star, dict):
        # try common shapes
        nodes = star.get("nodes") or star.get("stars") or star.get("bodies") or []
        if isinstance(nodes, dict):
            star_meta["node_count"] = len(nodes)
        elif isinstance(nodes, list):
            star_meta["node_count"] = len(nodes)
        star_meta["keys"] = list(star.keys())[:20]

    manifest = {
        "signature": SIG,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stack_root": str(stack),
        "user_protection": {
            "local_is_source_of_truth": True,
            "external_is_mirror": True,
            "consent_required_for_publish": True,
            "no_auto_git_push": True,
            "no_auto_hf_upload": True,
            "quarantine_on_hash_mismatch": True,
            "p0_before_destructive": True,
            "license": "LYGO Sovereign License v2.0 (code) · Music License v1.0 (music)",
        },
        "layers": {
            "A_classic": {
                **layer_summary(classic if isinstance(classic, dict) else {}, "classic_kernel_eggs"),
                "local_path": "data/kernel_eggs/registry.json",
                "skill": "lygo-kernel-egg-planter",
                "public_mirror": "KernelEggRegistry.json / KernelEggRetrieval.html",
            },
            "B_sovereign": {
                **layer_summary(sovereign if isinstance(sovereign, dict) else {}, "sovereign_seeds"),
                "local_path": "data/sovereign_seeds/registry.json",
                "skill": "lygo-sovereign-kernel-seeder",
                "public_mirror": "docs/sovereign_seeds_snapshot/registry.json",
            },
            "C_external": {
                "name": "world_network",
                "skill": "lygo-external-lattice-anchor",
                "role": "public_verify + star_chart_map + free_surface_sync",
                "endpoint_count": len(public_endpoints),
            },
            "D_living_mesh": {
                "name": "living_mesh",
                "skill": "lygo-living-mesh",
                "role": "multi_node_root_digest_gossip + sentinel",
                "docs": "docs/LIVING_MESH_LAYER.md",
                "tools": [
                    "tools/collect_living_mesh_badge.py",
                    "tools/verify_living_mesh.py",
                    "tools/living_mesh_sentinel.py",
                ],
                "clawhub": "https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh",
                "local_path": "data/living_mesh/",
            },
        },
        "public_endpoints": public_endpoints,
        "star_chart": {
            **star_meta,
            "live_url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
            "portal_url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html",
            "local_data_sha256": sha_file(star_data),
            "feed_sha256": sha_file(star_feed) if star_feed.is_file() else None,
        },
        "immutable_anchors": {
            "version": anchor_doc.get("version") if isinstance(anchor_doc, dict) else None,
            "signature": anchor_doc.get("signature") if isinstance(anchor_doc, dict) else None,
            "local_sha256": sha_file(anchors),
        },
        "last_unified_verify": load_json(layers_run),
        "sync_order": [
            "1_local_verify_A_B",
            "2_build_this_manifest",
            "3_map_eggs_to_star_chart_proposals",
            "4_human_consent",
            "5_external_plant_planter_surfaces",
            "6_snapshot_sovereign_to_docs",
            "7_optional_git_push_pages",
            "8_optional_hf_push",
            "9_public_verify_http",
            "10_star_chart_steward_ingest",
        ],
    }

    out = Path(args.out) if args.out else stack / "docs" / "public_verify_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "MANIFEST_OK", "out": str(out), "endpoints": len(public_endpoints)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
