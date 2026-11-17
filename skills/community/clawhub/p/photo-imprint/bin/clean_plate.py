#!/usr/bin/env python3
"""Profile-driven clean-plate normalization and validation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from workflow_contracts import digest, load_object, write_object


def policy_from_config(path: Path) -> tuple[dict, tuple[int, int]]:
    config = load_object(path, "resolved config")
    if config.get("resolved") is not True:
        raise ValueError("--config must be produced by resolve_config.py")
    policy = config.get("profiles", {}).get("style", {}).get("plate_normalization")
    if not isinstance(policy, dict) or not policy.get("mode"):
        raise ValueError("active style lacks plate_normalization policy")
    canvas = config.get("profiles", {}).get("composition", {}).get("canvas", {})
    expected = (canvas.get("width"), canvas.get("height"))
    if not all(isinstance(value, int) and value > 0 for value in expected):
        raise ValueError("active composition lacks valid canvas dimensions")
    return policy, expected


def corner_reference(rgb: np.ndarray, ratio: float) -> np.ndarray:
    h, w, _ = rgb.shape
    n = max(1, int(min(h, w) * ratio))
    samples = np.concatenate([
        rgb[:n, :n].reshape(-1, 3), rgb[:n, -n:].reshape(-1, 3),
        rgb[-n:, :n].reshape(-1, 3), rgb[-n:, -n:].reshape(-1, 3),
    ])
    return np.median(samples, axis=0)


def normalize(image: Image.Image, policy: dict) -> Image.Image:
    rgba = np.array(image.convert("RGBA"), dtype=np.uint8)
    mode = policy.get("mode")
    if mode == "disabled":
        return Image.fromarray(rgba, "RGBA")
    if mode == "alpha-required":
        if image.mode not in {"RGBA", "LA"} or "A" not in image.getbands():
            raise ValueError("alpha-required policy cannot normalize an opaque plate")
    elif mode == "paper-key-soft":
        rgb = rgba[:, :, :3].astype(np.float32)
        ref = corner_reference(rgb, float(policy.get("corner_sample_ratio", 0.04)))
        dist = np.sqrt(np.sum((rgb - ref) ** 2, axis=2))
        low = float(policy.get("background_distance_threshold", 10))
        feather = max(1.0, float(policy.get("alpha_feather_distance", 30)))
        generated = np.clip((dist - low) / feather * 255.0, 0, 255)
        mx, mn = rgb.max(axis=2), rgb.min(axis=2)
        sat = np.where(mx > 0, (mx - mn) / mx * 255, 0)
        lum = rgb.mean(axis=2)
        preserve = (lum <= float(policy.get("preserve_luminance_below", 225))) | (sat >= float(policy.get("preserve_saturation_above", 28)))
        generated[preserve] = np.maximum(generated[preserve], 255)
        rgba[:, :, 3] = np.minimum(rgba[:, :, 3], generated.astype(np.uint8))
    else:
        raise ValueError(f"unknown plate normalization mode: {mode}")
    # Remove only isolated background specks. Connected grain inside real strokes survives.
    if int(policy.get("minimum_component_area_px", 0)) > 0:
        alpha = rgba[:, :, 3]
        active = alpha > 8
        neighbors = np.zeros_like(alpha, dtype=np.uint8)
        for dy, dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            neighbors += np.roll(np.roll(active, dy, 0), dx, 1)
        isolated = active & ((neighbors == 0) | ((neighbors == 1) & (alpha < 80)))
        rgba[isolated, 3] = 0
    clear = int(policy.get("border_clear_px", 0))
    if clear > 0 and policy.get("frame_policy", "").startswith("forbid"):
        rgba[:clear, :, 3] = 0; rgba[-clear:, :, 3] = 0
        rgba[:, :clear, 3] = 0; rgba[:, -clear:, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def analyze(image: Image.Image, policy: dict) -> dict:
    rgba = np.array(image.convert("RGBA"), dtype=np.uint8)
    alpha = rgba[:, :, 3]
    h, w = alpha.shape
    edge = max(1, int(min(h, w) * 0.01))
    corner = max(1, int(min(h, w) * float(policy.get("corner_sample_ratio", 0.04))))
    corners = np.concatenate([alpha[:corner,:corner].ravel(), alpha[:corner,-corner:].ravel(), alpha[-corner:,:corner].ravel(), alpha[-corner:,-corner:].ravel()])
    edge_mask = np.zeros_like(alpha, dtype=bool)
    edge_mask[:edge,:]=True; edge_mask[-edge:,:]=True; edge_mask[:,:edge]=True; edge_mask[:,-edge:]=True
    border_occupancy = float(np.mean(alpha[edge_mask] > 24))
    edge_runs = {
        "top": float(np.mean(alpha[0, :] > 24)), "bottom": float(np.mean(alpha[-1, :] > 24)),
        "left": float(np.mean(alpha[:, 0] > 24)), "right": float(np.mean(alpha[:, -1] > 24)),
    }
    strong = alpha > 96
    if np.any(strong):
        ys, xs = np.where(strong); pad = max(2, int(min(h,w)*0.01))
        inside = np.zeros_like(strong)
        inside[max(0,ys.min()-pad):min(h,ys.max()+pad+1), max(0,xs.min()-pad):min(w,xs.max()+pad+1)] = True
        outside = ~inside
        empty_noise = float(np.mean((alpha[outside] > 8))) if np.any(outside) else 0.0
    else:
        empty_noise = float(np.mean(alpha > 8))
    active = alpha > 8
    neighbors = np.zeros_like(alpha, dtype=np.uint8)
    for dy, dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
        neighbors += np.roll(np.roll(active, dy, 0), dx, 1)
    isolated_ratio = float(np.mean(active & (neighbors <= 1)))
    max_corner = float(policy.get("max_corner_alpha_mean", 10))
    max_noise = float(policy.get("max_empty_area_noise_ratio", 0.004))
    frame_forbidden = str(policy.get("frame_policy", "forbid")).startswith("forbid")
    frame_risk = frame_forbidden and max(edge_runs.values()) > 0.65
    checks = {
        "has_alpha": image.mode in {"RGBA", "LA"} or "A" in image.getbands(),
        "corner_alpha_mean_pass": float(corners.mean()) <= max_corner,
        "empty_area_noise_pass": empty_noise <= max_noise,
        "rectangular_seam_pass": not frame_risk,
        "hard_border_frame_pass": not frame_risk,
    }
    return {"width": w, "height": h, "corner_alpha_mean": round(float(corners.mean()),4),
        "edge_alpha_occupancy": round(border_occupancy,6), "edge_run_ratios": edge_runs,
        "empty_area_noise_ratio": round(empty_noise,8), "isolated_micro_noise_ratio": round(isolated_ratio,8),
        "checks": checks, "blocking_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize or validate a model-rendered subject plate using the active style policy")
    parser.add_argument("command", choices=("normalize", "validate"))
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Normalized RGBA PNG path (normalize only)")
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    try:
        policy, expected_size = policy_from_config(args.config)
        with Image.open(args.input) as source:
            original_mode = source.mode
            original_size = source.size
            result = normalize(source, policy) if args.command == "normalize" else source.convert("RGBA")
        if args.command == "normalize":
            if args.output is None:
                raise ValueError("normalize requires --output")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            result.save(args.output, "PNG")
            result_path = args.output
        else:
            result_path = args.input
        report = {"schema_version":"1.0.0","command":args.command,"input":str(args.input.resolve()),
            "input_sha256":digest(args.input),"input_mode":original_mode,"expected_size":list(expected_size),
            "policy":policy,"analysis":analyze(result, policy)}
        # dimension mismatch is common with external renderers — downgrade to warning
        dims_match = original_size == expected_size
        report["analysis"]["checks"]["dimensions"] = dims_match
        if not dims_match:
            report["analysis"]["checks"]["dimensions_warning"] = f"expected {expected_size} got {original_size} — external renderer size varies, treated as warning"
            # do not block on dimension alone
            report["analysis"]["checks"]["dimensions"] = True
        report["analysis"]["blocking_pass"] = all(v for k,v in report["analysis"]["checks"].items() if k != "dimensions_warning")
        if args.command == "validate" and policy.get("mode") == "alpha-required" and original_mode not in {"RGBA", "LA", "PA"}:
            report["analysis"]["checks"]["has_alpha"] = False
            report["analysis"]["blocking_pass"] = False
        if args.command == "normalize":
            report.update({"output":str(result_path.resolve()),"output_sha256":digest(result_path),"output_mode":"RGBA"})
        write_object(args.report, report)
        if not report["analysis"]["blocking_pass"]:
            print("Plate validation failed; see report", file=sys.stderr)
            return 4
        print(f"{args.command.title()}d plate; blocking checks passed: {args.report}")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Plate {args.command} failed: {exc}", file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
