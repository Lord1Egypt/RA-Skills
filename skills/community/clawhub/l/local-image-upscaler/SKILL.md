---
name: image-upscaler
description: Upscale, inspect, or compress JPG, PNG, or WebP images locally on macOS or Windows, including automatic or user-selected photo, portrait, digital-art, sharp-detail, balanced, and fast profiles; 1K/2K/4K/8K output; custom long edges; strict target file sizes; batch folders; aspect-ratio preservation; offline reuse; and verified download fallbacks. Use when the user asks to make an image clearer, enlarge AI-generated art, compare enhancement algorithms, inspect image resolution, upscale without stretching, or reduce a larger image to a target such as 200KB.
---

# Image Upscaler

Use the bundled Python scripts to run Upscayl's Vulkan-based NCNN engine locally. Download models only when selected. Preserve the source aspect ratio by default and never overwrite an input file.

## Workflow

1. Inspect the input path, file type, dimensions, and available disk space.
2. Inspect the image visually and recommend one profile. If the choice materially affects the result, give the user a compact choice with the advantage, disadvantage, and additional download size. Do not block if the user does not choose; use `default`.
3. Choose a profile:
   - `default`: balanced and conservative; use when content is mixed or uncertain. Model download: about 32 MB.
   - `fast`: smallest and fastest; weaker fine-detail reconstruction. Model download: about 2.5 MB.
   - `photo`: natural photographic texture; less crisp on text and architecture. Model download: about 32 MB.
   - `portrait`: use for compressed, noisy, or rough natural portraits that benefit from smoother rendering. It avoids face replacement but can remove fine skin texture. Use `default` for already-clean AI portraits and sharp studio headshots. Model download: about 32 MB, shared with `photo`.
   - `digital-art`: clean anime, illustration, and icon edges; may oversimplify photographic texture. Model download: about 8.6 MB.
   - `sharp`: strongest apparent edge detail; may exaggerate noise, halos, skin, or text artifacts. Model download: about 32 MB.
4. If the selected runtime or model is not cached, explain the download and disk cost, then run setup. Read [platforms.md](references/platforms.md) for compatibility and cache sizes.
5. Run the upscaler or compressor. Prefer PNG for maximum upscale quality; use JPEG for strict file-size targets.
6. Verify that the output exists, has the requested dimensions, and keeps the source ratio. Report the selected profile, output path, dimensions, and file size.

The agent performs the meaningful automatic selection after visually inspecting the image. CLI `--profile auto` uses filename hints only and otherwise falls back conservatively to `default`; it does not claim reliable face or scene classification without an extra vision package. Read [algorithms.md](references/algorithms.md) when comparing profiles or discussing heavier optional algorithms.

For portraits, inspect source quality before selecting by subject alone: choose `default` for clean AI-generated or studio portraits; choose `portrait` only when a natural portrait is noisy, compressed, or visually rough. This rule is based on same-size comparison testing, where `portrait` produced smoother skin but removed detail from an already-clean AI portrait.

## Prepare the Runtime

Run from this skill directory:

```bash
python scripts/setup.py --model high-fidelity
```

List choices, trade-offs, cache status, and incremental downloads without installing anything:

```bash
python scripts/setup.py --list-models
```

Prepare only the selected profile:

```bash
python scripts/setup.py --profile photo
python scripts/setup.py --profile digital-art
python scripts/setup.py --profile sharp
```

The downloader tries the local cache, configured mirrors, a verified GitHub acceleration endpoint, and the official source. Every downloaded artifact must match the pinned SHA-256 digest. The upscaler re-verifies the cached executable and selected model before every execution, including when `IMAGE_UPSCALER_CACHE` overrides the cache directory. To use an organization or domestic mirror, set `IMAGE_UPSCALER_MIRRORS` to one or more comma-separated URL prefixes before setup. Each prefix is prepended to the official URL. Example:

```bash
IMAGE_UPSCALER_MIRRORS="https://mirror.example/proxy/" python scripts/setup.py
```

Use `--offline` to forbid all network access. Use `--platform windows-x64 --download-only` to prefetch Windows files from another machine.

## Upscale Images

Create a 4K image whose long edge is 3840 pixels while preserving the original ratio:

```bash
python scripts/upscale.py INPUT --output OUTPUT.png --target 4k
```

Useful variants:

```bash
python scripts/upscale.py INPUT --target 1k
python scripts/upscale.py INPUT --target 2k --profile fast
python scripts/upscale.py INPUT --target 4k --profile portrait
python scripts/upscale.py INPUT --target 4k --profile digital-art
python scripts/upscale.py INPUT --target 4k --profile sharp
python scripts/upscale.py INPUT --target 8k --profile photo --tile 256
python scripts/upscale.py INPUT --target scale4 --format png
python scripts/upscale.py INPUT_FOLDER --output OUTPUT_FOLDER --target 4k
python scripts/upscale.py INPUT --target 4k --format jpg --compression 92
```

The screen-oriented presets use long edges: `1k=1920`, `2k=2560`, `4k=3840`, and `8k=7680`. A 16:9 4K landscape becomes 3840×2160; portraits and squares retain their own ratios. `scale4` keeps the model's native 4× output. Use `--max-edge N` for an exact custom long edge. Current local models are native 4× models; an 8K preset beyond the native result uses exact high-quality resizing and must not be described as recovered factual detail. For 8K, expect high memory and temporary-disk use; start with `--tile 256` if automatic tiling fails.

Exact 2K/4K output supports PNG and JPEG without extra dependencies. WebP is supported with `--target scale4`; use PNG when an exact target and transparency both matter.

## Compress to a Target Size

Compress a roughly 1MB image to no more than 200KiB:

```bash
python scripts/compress.py INPUT --output OUTPUT.jpg --target-kb 200
python scripts/compress.py INPUT --target-mb 1.5 --keep-dimensions
python scripts/compress.py INPUT_FOLDER --output OUTPUT_FOLDER --target-kb 200 --recursive
```

The compressor first finds the highest JPEG quality that fits. If quality alone is insufficient, it reduces dimensions proportionally while respecting `--min-edge` (default 640px). It never stretches or overwrites the source. JPEG does not preserve transparency; convert the background explicitly before compression when its color matters.

Use `--keep-dimensions` when reducing resolution is forbidden. Existing output files receive a `-v2`, `-v3`, and so on suffix unless `--overwrite` is explicitly supplied. Use `--dry-run` before a large folder job.

## Inspect Before Processing

Inspect one file or a folder before choosing an upscale or compression target:

```bash
python scripts/inspect.py INPUT
python scripts/inspect.py INPUT_FOLDER --recursive --json
```

The report includes dimensions, simplified aspect ratio, megapixels, and file size.

## Safety and Quality Rules

- Never delete or replace source images.
- Do not install GPU drivers, package managers, or system dependencies automatically.
- Do not bypass SHA-256 verification, even when using a mirror.
- Treat `IMAGE_UPSCALER_CACHE` and `IMAGE_UPSCALER_MIRRORS` as trusted configuration; execution-time hashes still reject modified runtime or model files.
- Do not upload user images; processing must stay local.
- Avoid TTA unless the user explicitly accepts a roughly 8× processing slowdown.
- On GPU-memory errors, retry with `--tile 256`, then `--tile 128`.
- If Vulkan is unavailable, stop and explain the platform limitation; do not silently switch to an unrelated cloud service.
- Treat visual enhancement as reconstruction, not recovery of factual detail. Do not claim that invented texture is original information.

## References

- Read [platforms.md](references/platforms.md) for supported systems, storage, cache, mirror, and troubleshooting details.
- Read [algorithms.md](references/algorithms.md) for profile selection, benefits, limitations, and optional heavy algorithms.
- Read [licenses.md](references/licenses.md) before redistributing the engine or model files.
