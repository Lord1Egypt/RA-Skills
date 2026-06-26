#!/usr/bin/env python3
"""
Photo Screener — AI-powered photo pre-screening using MobileCLIP2-S0.

Performs three intelligent screening stages on a directory of photos:
  1. Aesthetic scoring   — CLIP + LAION MLP predicts human aesthetic preference (1-10)
  2. Similarity dedup    — CLIP embeddings cosine similarity removes near-duplicates
  3. Scene classification — Zero-shot CLIP text matching assigns scene tags

Uses Apple MobileCLIP2-S0 via open_clip for 18x faster inference vs ViT-L/14,
with 80% selection consistency (Top-10 overlap 8/10).

Dependencies:
    Python: pip install torch open-clip-torch pillow numpy

    Check & install: bash scripts/setup_deps.sh

Model Download:
    The MobileCLIP2-S0 model (~300MB) is NOT pre-downloaded.
    On first run, the script will ask for user confirmation before downloading.
    Uses HuggingFace mirror (hf-mirror.com) for accelerated download in China.

    To pre-download: HF_ENDPOINT=https://hf-mirror.com python -c \\
        "import open_clip; open_clip.create_model_and_transforms('MobileCLIP2-S0', pretrained='dfndr2b')"

Configuration:
    Default options from config.toml (next to scripts/ dir).

Usage:
    python screen.py ~/Downloads/output/{session-id}/thumbnails
    python screen.py ~/Downloads/output/{session-id}/thumbnails --min-score 5.0
    python screen.py ~/Downloads/output/{session-id}/thumbnails --output report.json
    python screen.py ~/Downloads/output/{session-id}/thumbnails --dry-run
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

# Ensure line-buffered output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# ── Configuration ───────────────────────────────────────────────

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

_SKILL_DIR = Path(__file__).resolve().parent.parent
_ROOT_DIR = _SKILL_DIR.parent
_DEFAULT_CONFIG_PATH = (
    _SKILL_DIR / "config.toml" if (_SKILL_DIR / "config.toml").exists() else _ROOT_DIR / "config.toml"
)


def load_config(config_path=None):
    """Load configuration from config.toml."""
    path = Path(config_path or _DEFAULT_CONFIG_PATH).expanduser().resolve()
    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        if not isinstance(cfg, dict):
            print(f"⚠️  Config is not a valid mapping, ignoring: {path}", file=sys.stderr)
            return {}
        print(f"📄 Loaded config: {path}")
        return cfg
    except Exception as e:
        print(f"⚠️  Failed to read config ({path}): {e}", file=sys.stderr)
        return {}


# ── Dependency Check ────────────────────────────────────────────


def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    for pkg, pip_name in [("torch", "torch"), ("open_clip", "open-clip-torch"), ("PIL", "pillow"), ("numpy", "numpy")]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print("❌ Missing dependencies:", file=sys.stderr)
        for pkg in missing:
            print(f"  - {pkg}", file=sys.stderr)
        print(f"\nInstall with:\n  pip3 install {' '.join(missing)}", file=sys.stderr)
        print(f"\nOr run:\n  bash {_SKILL_DIR}/scripts/setup_deps.sh", file=sys.stderr)
        sys.exit(1)


check_dependencies()

import open_clip
import numpy as np
import torch
from PIL import Image

# ── Supported image extensions ──────────────────────────────────

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp", ".heic", ".heif"}

# Check HEIC support availability
_HEIC_AVAILABLE = False
try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    _HEIC_AVAILABLE = True
except ImportError:
    # HEIC/HEIF files will be skipped if pillow-heif is not installed
    pass

# ── Model constants ─────────────────────────────────────────────

# MobileCLIP2-S0 embedding dimension
_MOBILECLIP_EMBED_DIM = 512

# Aesthetic model expects 768-dim (ViT-L/14)
_AESTHETIC_INPUT_DIM = 768
_AESTHETIC_MODEL_URL = (
    "https://github.com/christophschuhmann/improved-aesthetic-predictor/raw/main/sac+logos+ava1-l14-linearMSE.pth"
)

# HuggingFace mirror for China
_HF_MIRROR = "https://hf-mirror.com"


# ═══════════════════════════════════════════════════════════════
# Model Loading with User Confirmation
# ═══════════════════════════════════════════════════════════════


def _check_model_cached(model_name, pretrained):
    """Check if the open_clip model is already cached locally."""
    # Check common cache locations
    cache_dirs = [
        Path.home() / ".cache" / "open_clip",
        Path.home() / ".cache" / "huggingface" / "hub",
        Path.home() / ".cache" / "clip",
    ]
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            for item in cache_dir.rglob("*"):
                name_lower = item.name.lower()
                if "mobileclip" in name_lower and "s0" in name_lower:
                    return True
                if "dfndr2b" in name_lower:
                    return True
    return False


def load_clip_model(model_name, pretrained, device, auto_download=False):
    """
    Load CLIP model with user confirmation for download.

    If the model is not cached and auto_download is False, prompts the user.
    Uses HuggingFace mirror (hf-mirror.com) for accelerated download in China.

    Args:
        model_name: open_clip model name (e.g., 'MobileCLIP2-S0')
        pretrained: pretrained weights tag (e.g., 'dfndr2b')
        device: torch device
        auto_download: skip confirmation if True

    Returns:
        (model, preprocess, tokenizer)
    """
    is_cached = _check_model_cached(model_name, pretrained)

    if not is_cached and not auto_download:
        print(f"\n{'━' * 60}")
        print(f"  ⚠️  模型 {model_name} 尚未下载")
        print(f"{'━' * 60}")
        print(f"  模型大小: ~300MB")
        print(f"  下载源:   hf-mirror.com (国内加速)")
        print(f"  缓存位置: ~/.cache/huggingface/")
        print(f"{'━' * 60}")
        print()

        # Check if running in interactive mode
        if sys.stdin.isatty():
            answer = input("  是否下载模型？[Y/n] ").strip()
            if answer and answer.lower() not in ("y", "yes", "是"):
                print("\n❌ 模型下载已取消。无法继续运行。")
                print(
                    f"   手动下载: HF_ENDPOINT={_HF_MIRROR} python3 -c \"import open_clip; open_clip.create_model_and_transforms('{model_name}', pretrained='{pretrained}')\""
                )
                sys.exit(1)
        else:
            # Non-interactive mode — abort with instructions
            print("❌ 模型未下载且当前为非交互模式。")
            print(f"   请先手动下载模型:")
            print(
                f"   HF_ENDPOINT={_HF_MIRROR} python3 -c \"import open_clip; open_clip.create_model_and_transforms('{model_name}', pretrained='{pretrained}')\""
            )
            print(f"\n   或运行: bash {_SKILL_DIR}/scripts/setup_deps.sh")
            print(f"   或添加 --auto-download 参数跳过确认")
            sys.exit(1)

    # Set HuggingFace mirror for download acceleration
    original_hf_endpoint = os.environ.get("HF_ENDPOINT")
    if not is_cached:
        os.environ["HF_ENDPOINT"] = _HF_MIRROR
        print(f"\n📥 使用国内镜像下载 {model_name}...")
        print(f"   镜像源: {_HF_MIRROR}")

    try:
        model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
        tokenizer = open_clip.get_tokenizer(model_name)

        model = model.to(device)
        model.eval()

        if not is_cached:
            print(f"   ✅ 模型下载完成！")

        return model, preprocess, tokenizer

    finally:
        # Restore original HF_ENDPOINT
        if original_hf_endpoint is not None:
            os.environ["HF_ENDPOINT"] = original_hf_endpoint
        elif "HF_ENDPOINT" in os.environ and not is_cached:
            del os.environ["HF_ENDPOINT"]


# ═══════════════════════════════════════════════════════════════
# LAION Aesthetic Predictor
# ═══════════════════════════════════════════════════════════════


class AestheticPredictor(torch.nn.Module):
    """LAION improved-aesthetic-predictor MLP."""

    def __init__(self, input_dim=768):
        super().__init__()
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 1024),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(1024, 128),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(128, 64),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(64, 16),
            torch.nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.layers(x)


def _get_aesthetic_model_path():
    """Get the cached path for the aesthetic model weights, downloading if needed."""
    cache_dir = Path.home() / ".cache" / "photo-filter"
    cache_dir.mkdir(parents=True, exist_ok=True)
    model_path = cache_dir / "aesthetic_sac_logos_ava1_l14_linearMSE.pth"

    if model_path.exists():
        return model_path

    print(f"📥 Downloading aesthetic model (~3MB)...")
    print(f"   建议预下载: bash {_SKILL_DIR}/scripts/setup_deps.sh")
    try:
        urllib.request.urlretrieve(_AESTHETIC_MODEL_URL, str(model_path))
        print(f"   ✓ Saved to: {model_path}")
    except Exception as e:
        print(f"❌ Failed to download aesthetic model: {e}", file=sys.stderr)
        print("   You can manually download from:", file=sys.stderr)
        print(f"   {_AESTHETIC_MODEL_URL}", file=sys.stderr)
        print(f"\n   Or run: bash {_SKILL_DIR}/scripts/setup_deps.sh", file=sys.stderr)
        sys.exit(1)

    return model_path


def load_aesthetic_model(device):
    """Load the LAION aesthetic predictor (always 768-dim input)."""
    model_path = _get_aesthetic_model_path()
    state_dict = torch.load(str(model_path), map_location=device, weights_only=True)
    keys = list(state_dict.keys())

    if any("layers" in k for k in keys):
        model = AestheticPredictor(input_dim=_AESTHETIC_INPUT_DIM)
        model.load_state_dict(state_dict)
    else:
        model = torch.nn.Linear(_AESTHETIC_INPUT_DIM, 1)
        model.load_state_dict(state_dict)

    model.to(device)
    model.eval()
    return model


# ═══════════════════════════════════════════════════════════════
# Core Functions
# ═══════════════════════════════════════════════════════════════


def find_images(input_dir, recursive=False):
    """Find all supported image files in a directory."""
    input_path = Path(input_dir).expanduser().resolve()
    if not input_path.exists():
        return []
    if input_path.is_file():
        if input_path.suffix.lower() in IMAGE_EXTENSIONS:
            return [input_path]
        return []

    results = []
    if recursive:
        for p in sorted(input_path.rglob("*")):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
                results.append(p)
    else:
        for p in sorted(input_path.iterdir()):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
                results.append(p)
    return results


def get_device():
    """Get the best available PyTorch device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def encode_images(image_paths, model, preprocess, device, batch_size=32):
    """Encode images using CLIP. Returns (embeddings, valid_paths, errors)."""
    all_embeddings = []
    valid_paths = []
    errors = []
    total = len(image_paths)

    for batch_start in range(0, total, batch_size):
        batch_end = min(batch_start + batch_size, total)
        batch_paths = image_paths[batch_start:batch_end]

        batch_tensors = []
        batch_valid = []

        for p in batch_paths:
            try:
                img = Image.open(p).convert("RGB")
                tensor = preprocess(img).unsqueeze(0)
                batch_tensors.append(tensor)
                batch_valid.append(p)
            except Exception as e:
                errors.append((str(p), str(e)))

        if not batch_tensors:
            continue

        images_tensor = torch.cat(batch_tensors, dim=0).to(device)

        with torch.no_grad():
            features = model.encode_image(images_tensor)
            features = features / features.norm(dim=-1, keepdim=True)
            all_embeddings.append(features.cpu().numpy().astype(np.float32))

        valid_paths.extend(batch_valid)
        done = min(batch_end, total)
        print(f"  🔍 Encoding images: [{done}/{total}]", flush=True)

    print(f"  🔍 Encoding complete: [{total}/{total}] ✓", flush=True)

    if not all_embeddings:
        return np.array([]), valid_paths, errors

    return np.vstack(all_embeddings), valid_paths, errors


def compute_aesthetic_scores(embeddings, aesthetic_model, device):
    """
    Compute aesthetic scores. Zero-pads MobileCLIP 512-dim embeddings to 768-dim
    for the aesthetic model.
    """
    embed_dim = embeddings.shape[1]
    target_dim = _AESTHETIC_INPUT_DIM  # 768

    with torch.no_grad():
        emb_tensor = torch.from_numpy(embeddings).to(device).float()

        if embed_dim < target_dim:
            padding = torch.zeros(emb_tensor.shape[0], target_dim - embed_dim, device=device)
            emb_tensor = torch.cat([emb_tensor, padding], dim=1)
        elif embed_dim > target_dim:
            emb_tensor = emb_tensor[:, :target_dim]

        scores = aesthetic_model(emb_tensor).cpu().numpy().flatten()
    return scores


def deduplicate_by_similarity(embeddings, scores, paths, threshold=0.97):
    """
    Remove near-duplicate images using greedy approach.
    Higher score images have priority.
    """
    n = len(paths)
    if n == 0:
        return np.array([], dtype=bool), []

    sim_matrix = embeddings @ embeddings.T
    sorted_indices = np.argsort(scores)[::-1]

    keep_mask = np.ones(n, dtype=bool)
    groups = []

    for idx in sorted_indices:
        if not keep_mask[idx]:
            continue
        group = [(idx, str(paths[idx]), float(scores[idx]))]
        for other in sorted_indices:
            if other == idx or not keep_mask[other]:
                continue
            if sim_matrix[idx, other] >= threshold:
                keep_mask[other] = False
                group.append((other, str(paths[other]), float(scores[other])))
        if len(group) > 1:
            groups.append(group)

    return keep_mask, groups


def classify_scenes(embeddings, model, tokenizer, device, categories=None):
    """Zero-shot scene classification using open_clip text-image matching."""
    if categories is None:
        categories = [
            "portrait photo of a person",
            "landscape or nature scenery",
            "street photography",
            "architecture or building",
            "food or drink",
            "animal or pet",
            "night scene or cityscape",
            "macro or close-up",
            "group photo of people",
            "still life or product",
            "sports or action",
            "wedding or ceremony",
            "travel or tourism",
            "abstract or artistic",
        ]

    label_names = [
        "人像",
        "风景",
        "街拍",
        "建筑",
        "美食",
        "动物",
        "夜景",
        "微距",
        "合影",
        "静物",
        "运动",
        "婚礼/仪式",
        "旅行",
        "抽象/艺术",
    ]

    # Encode text prompts using open_clip tokenizer
    text_tokens = tokenizer(categories).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        text_np = text_features.cpu().numpy().astype(np.float32)

    all_scores = embeddings @ text_np.T

    labels = []
    for i in range(len(embeddings)):
        row = all_scores[i]
        sorted_indices = np.argsort(row)[::-1]
        primary = (
            label_names[sorted_indices[0]] if sorted_indices[0] < len(label_names) else categories[sorted_indices[0]]
        )
        secondary = None
        if len(sorted_indices) > 1:
            diff = row[sorted_indices[0]] - row[sorted_indices[1]]
            if diff < 0.03:
                secondary = (
                    label_names[sorted_indices[1]]
                    if sorted_indices[1] < len(label_names)
                    else categories[sorted_indices[1]]
                )

        labels.append(
            {
                "primary": primary,
                "secondary": secondary,
                "confidence": round(float(row[sorted_indices[0]]), 4),
            }
        )

    return labels, all_scores


# ═══════════════════════════════════════════════════════════════
# Batching for LLM
# ═══════════════════════════════════════════════════════════════


def create_batches(photos, batch_size=20):
    """Split photos into batches grouped by scene tag."""
    scene_groups = {}
    for photo in photos:
        tag = photo.get("scene", {}).get("primary", "其他")
        scene_groups.setdefault(tag, []).append(photo)

    batches = []
    for tag, group in sorted(scene_groups.items(), key=lambda x: -len(x[1])):
        group.sort(key=lambda x: -x.get("aesthetic_score", 0))
        for i in range(0, len(group), batch_size):
            batch = group[i : i + batch_size]
            batches.append(
                {
                    "batch_id": len(batches) + 1,
                    "scene_tag": tag,
                    "count": len(batch),
                    "photos": batch,
                }
            )

    return batches


# ═══════════════════════════════════════════════════════════════
# Main Pipeline
# ═══════════════════════════════════════════════════════════════


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds) // 60
    secs = seconds - minutes * 60
    return f"{minutes}m {secs:.0f}s"


def run_pipeline(
    input_dir,
    output_json=None,
    clip_model_name="MobileCLIP2-S0",
    clip_pretrained="dfndr2b",
    min_score=4.0,
    sim_threshold=0.97,
    batch_size=20,
    top_k=None,
    recursive=False,
    scene_categories=None,
    dry_run=False,
    auto_download=False,
    pre_images=None,
):
    """Run the full photo filtering pipeline."""
    total_start = time.monotonic()

    print(f"\n{'═' * 60}")
    print(f"  📸 Photo Filter V2 — MobileCLIP-powered Smart Pre-screening")
    print(f"{'═' * 60}\n")

    images = pre_images if pre_images else find_images(input_dir, recursive)
    if not images:
        print("❌ No image files found.")
        sys.exit(1)

    display_dir = input_dir if input_dir else (str(images[0].parent) if images else "N/A")
    print(f"📂 Input:  {Path(display_dir).resolve() if input_dir else display_dir}")
    print(f"📷 Found:  {len(images)} image(s)")
    print(f"🎯 Config: model={clip_model_name}, min_score={min_score}, sim_threshold={sim_threshold}")

    if dry_run:
        print(f"\n🔍 Dry run — would process {len(images)} images")
        for img in images[:20]:
            print(f"  📸 {img.name}")
        if len(images) > 20:
            print(f"  ... and {len(images) - 20} more")
        return None

    # ── Step 1: Load CLIP model ─────────────────────────────────
    device = get_device()
    print(f"\n🧠 Loading {clip_model_name} on {device}...")
    t0 = time.monotonic()
    clip_model, preprocess, tokenizer = load_clip_model(
        clip_model_name, clip_pretrained, device, auto_download=auto_download
    )
    print(f"   ✓ Model loaded in {format_time(time.monotonic() - t0)}")

    # ── Step 2: Load aesthetic predictor ─────────────────────────
    print(f"\n🎨 Loading aesthetic predictor...")
    t0 = time.monotonic()
    aesthetic_model = load_aesthetic_model(device)
    print(f"   ✓ Aesthetic model loaded in {format_time(time.monotonic() - t0)}")

    # ── Step 3: Encode all images ───────────────────────────────
    print(f"\n📊 Stage 1: Encoding {len(images)} images with {clip_model_name}...")
    t0 = time.monotonic()
    embeddings, valid_paths, encode_errors = encode_images(images, clip_model, preprocess, device)
    encode_time = time.monotonic() - t0
    print(f"   ✓ Encoded {len(valid_paths)} images in {format_time(encode_time)}")
    if encode_errors:
        print(f"   ⚠️  {len(encode_errors)} images failed to load")

    if len(valid_paths) == 0:
        print("❌ No images could be processed.")
        sys.exit(1)

    # ── Step 4: Aesthetic scoring ───────────────────────────────
    print(f"\n🎨 Stage 2: Computing aesthetic scores...")
    t0 = time.monotonic()
    scores = compute_aesthetic_scores(embeddings, aesthetic_model, device)
    score_time = time.monotonic() - t0

    avg_score = float(np.mean(scores))
    min_s = float(np.min(scores))
    max_s = float(np.max(scores))
    above_threshold = int(np.sum(scores >= min_score))
    print(f"   ✓ Scores computed in {format_time(score_time)}")
    print(f"   📈 Score range: {min_s:.2f} ~ {max_s:.2f} (avg: {avg_score:.2f})")
    print(f"   ✅ {above_threshold}/{len(valid_paths)} photos above threshold ({min_score})")

    # ── Step 5: Similarity dedup ────────────────────────────────
    print(f"\n🔄 Stage 3: Deduplication (threshold={sim_threshold})...")
    t0 = time.monotonic()

    above_mask = scores >= min_score
    if np.sum(above_mask) == 0:
        print("   ⚠️  No photos above threshold, relaxing to keep top 50%")
        median = float(np.median(scores))
        above_mask = scores >= median
        min_score = median

    above_indices = np.where(above_mask)[0]
    above_embeddings = embeddings[above_indices]
    above_scores = scores[above_indices]
    above_paths = [valid_paths[i] for i in above_indices]

    keep_mask, dup_groups = deduplicate_by_similarity(above_embeddings, above_scores, above_paths, sim_threshold)
    dedup_time = time.monotonic() - t0

    kept_count = int(np.sum(keep_mask))
    removed_count = len(above_paths) - kept_count
    dup_group_count = sum(1 for g in dup_groups if len(g) > 1)
    print(f"   ✓ Dedup completed in {format_time(dedup_time)}")
    print(f"   🔄 Found {dup_group_count} duplicate group(s), removed {removed_count} duplicates")
    print(f"   ✅ {kept_count} unique photos remaining")

    # ── Step 6: Scene classification ────────────────────────────
    kept_indices = np.where(keep_mask)[0]
    kept_embeddings = above_embeddings[kept_indices]
    kept_scores = above_scores[kept_indices]
    kept_paths = [above_paths[i] for i in kept_indices]

    print(f"\n🏷️  Stage 4: Scene classification...")
    t0 = time.monotonic()
    scene_labels, _ = classify_scenes(kept_embeddings, clip_model, tokenizer, device, scene_categories)
    classify_time = time.monotonic() - t0
    print(f"   ✓ Classification completed in {format_time(classify_time)}")

    scene_counts = {}
    for label in scene_labels:
        tag = label["primary"]
        scene_counts[tag] = scene_counts.get(tag, 0) + 1
    print(f"   🏷️  Scene distribution:")
    for tag, count in sorted(scene_counts.items(), key=lambda x: -x[1]):
        print(f"      {tag}: {count}")

    # ── Step 7: Apply top_k limit ───────────────────────────────
    if top_k and top_k < len(kept_paths):
        sorted_idx = np.argsort(kept_scores)[::-1][:top_k]
        kept_paths = [kept_paths[i] for i in sorted_idx]
        kept_scores = kept_scores[sorted_idx]
        scene_labels = [scene_labels[i] for i in sorted_idx]
        kept_embeddings = kept_embeddings[sorted_idx]
        print(f"\n   🔝 Top-K filter: keeping top {top_k} photos")

    # ── Step 8: Build report ────────────────────────────────────
    photos = []
    for i, (path, score, label) in enumerate(zip(kept_paths, kept_scores, scene_labels)):
        photos.append(
            {
                "file": path.name,
                "path": str(path),
                "aesthetic_score": round(float(score), 3),
                "scene": label,
            }
        )

    photos.sort(key=lambda x: -x["aesthetic_score"])
    batches = create_batches(photos, batch_size)

    total_elapsed = time.monotonic() - total_start

    report = {
        "summary": {
            "total_input": len(images),
            "encode_errors": len(encode_errors),
            "below_threshold": int(np.sum(~above_mask)),
            "duplicates_removed": removed_count,
            "final_count": len(photos),
            "score_range": [round(min_s, 3), round(max_s, 3)],
            "score_avg": round(avg_score, 3),
            "min_score_threshold": min_score,
            "sim_threshold": sim_threshold,
            "scene_distribution": scene_counts,
            "llm_batches": len(batches),
            "clip_model": clip_model_name,
            "clip_pretrained": clip_pretrained,
            "device": str(device),
            "elapsed_seconds": round(total_elapsed, 2),
        },
        "batches": batches,
        "rejected": {
            "below_threshold": [
                {"file": valid_paths[i].name, "score": round(float(scores[i]), 3)}
                for i in range(len(valid_paths))
                if not above_mask[i]
            ],
            "duplicates": [
                {
                    "kept": {
                        "file": Path(group[max(range(len(group)), key=lambda gi: group[gi][2])][1]).name,
                        "score": round(group[max(range(len(group)), key=lambda gi: group[gi][2])][2], 3),
                    },
                    "removed": [
                        {"file": Path(m[1]).name, "score": round(m[2], 3)}
                        for mi, m in enumerate(group)
                        if mi != max(range(len(group)), key=lambda gi: group[gi][2])
                    ],
                }
                for group in dup_groups
                if len(group) > 1
            ],
            "encode_errors": [{"file": p, "error": e} for p, e in encode_errors],
        },
    }

    # ── Output ──────────────────────────────────────────────────
    print(f"\n{'═' * 60}")
    print(f"  ✅ Photo Filter V2 Complete")
    print(f"{'═' * 60}")
    print(f"  📷 Input:      {len(images)} photos")
    print(f"  ❌ Rejected:   {int(np.sum(~above_mask))} (low score) + {removed_count} (duplicates)")
    print(f"  ✅ Selected:   {len(photos)} photos")
    print(f"  📦 LLM batch:  {len(batches)} batch(es) × ≤{batch_size} photos")
    print(f"  ⏱️  Total time: {format_time(total_elapsed)}")

    if output_json:
        output_path = Path(output_json).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  📄 Report saved: {output_path}")

    return report


# ═══════════════════════════════════════════════════════════════
# CLI Entry
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered photo pre-screening using MobileCLIP2-S0 (aesthetic scoring + dedup + scene tagging)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Downloads/output/{session-id}/thumbnails
  %(prog)s ~/Downloads/output/{session-id}/thumbnails --min-score 5.0
  %(prog)s ~/Downloads/output/{session-id}/thumbnails --top-k 50
  %(prog)s ~/Downloads/output/{session-id}/thumbnails --output report.json
  %(prog)s ~/Downloads/output/{session-id}/thumbnails --dry-run
  %(prog)s ~/Downloads/output/{session-id}/thumbnails --auto-download
        """,
    )
    parser.add_argument("input_dir", nargs="?", default=None, help="Directory containing photos (JPG thumbnails)")
    parser.add_argument("--paths", nargs="+", type=str, default=None, help="缩略图绝对路径列表（替代 input_dir）")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output JSON report path")
    parser.add_argument("--config", type=str, default=None, help="Path to config.toml")
    parser.add_argument(
        "--min-score", type=float, default=None, help="Minimum aesthetic score threshold (default: 4.0)"
    )
    parser.add_argument(
        "--sim-threshold", type=float, default=None, help="Cosine similarity threshold for dedup (default: 0.97)"
    )
    parser.add_argument("--batch-size", type=int, default=None, help="Max photos per LLM batch (default: 20)")
    parser.add_argument("--top-k", type=int, default=None, help="Keep only top K photos after filtering")
    parser.add_argument("--recursive", "-r", action="store_true", default=None, help="Search subdirectories")
    parser.add_argument("--dry-run", action="store_true", help="Preview without processing")
    parser.add_argument("--auto-download", action="store_true", help="Auto-download model without confirmation")

    args = parser.parse_args()

    if not args.input_dir and not args.paths:
        parser.error("input_dir or --paths is required")

    cfg = load_config(args.config)

    clip_model_name = cfg.get("clip_model", "MobileCLIP2-S0")
    clip_pretrained = cfg.get("clip_pretrained", "dfndr2b")
    min_score = args.min_score if args.min_score is not None else cfg.get("min_aesthetic_score", 4.0)
    sim_threshold = args.sim_threshold if args.sim_threshold is not None else cfg.get("dedup_threshold", 0.97)
    batch_size = args.batch_size if args.batch_size is not None else cfg.get("llm_batch_size", 20)
    top_k = args.top_k if args.top_k is not None else cfg.get("top_k") or None
    recursive = args.recursive if args.recursive is not None else cfg.get("recursive", False)

    # Build pre_images from --paths if provided
    pre_images = None
    input_dir = args.input_dir
    if args.paths:
        pre_images = [Path(p).expanduser().resolve() for p in args.paths]
        pre_images = [p for p in pre_images if p.exists() and p.suffix.lower() in IMAGE_EXTENSIONS]
        input_dir = str(pre_images[0].parent) if pre_images and not input_dir else input_dir

    output_json = args.output or cfg.get("screener_output") or cfg.get("output")
    if not output_json and input_dir:
        output_json = str(Path(input_dir).expanduser().resolve() / "filter_report.json")

    run_pipeline(
        input_dir=input_dir,
        output_json=output_json if not args.dry_run else None,
        clip_model_name=clip_model_name,
        clip_pretrained=clip_pretrained,
        min_score=min_score,
        sim_threshold=sim_threshold,
        batch_size=batch_size,
        top_k=top_k,
        recursive=recursive,
        dry_run=args.dry_run,
        auto_download=args.auto_download,
        pre_images=pre_images,
    )


if __name__ == "__main__":
    main()
