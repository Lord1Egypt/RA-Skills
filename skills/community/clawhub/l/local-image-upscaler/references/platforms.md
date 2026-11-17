# Platform and Storage Reference

## Supported systems

- macOS 12 or newer on Apple Silicon or Intel. The runtime is a universal binary and uses Metal through MoltenVK.
- Windows 10/11 x64 with a Vulkan-capable GPU and current graphics driver.
- Windows ARM is not supported by the pinned runtime. x64 emulation does not guarantee Vulkan compatibility.
- Linux is intentionally omitted from version 1.0 to keep the tested support surface focused.

## Approximate storage

The Skill itself is under 1 MB. Cached components use approximately:

- macOS runtime: 9 MB download plus 28 MB extracted.
- Windows runtime: 2.5 MB download plus 8 MB extracted.
- High-fidelity model: 34 MB.
- Lite model: 2.5 MB.
- Digital-art model: 8.6 MB.
- Natural photo/portrait model: 32 MB (one shared model for both profiles).
- Sharp-detail model: 32 MB.
- Installing every bundled model adds about 100 MB of model data; models are downloaded individually by default.
- Output images: varies; lossless 4K PNG files are commonly 5–30 MB each.

The cache is stored in `~/.cache/image-upscaler` on macOS and `%LOCALAPPDATA%\image-upscaler` on Windows. Override it with `IMAGE_UPSCALER_CACHE`.

## Download order

1. Existing verified cache.
2. Prefixes in `IMAGE_UPSCALER_MIRRORS`, in the supplied order.
3. The bundled GitHub acceleration prefix.
4. Official GitHub or raw GitHub URL.

All paths use the same pinned SHA-256 digests. Setup verifies downloads and extracted executables; every upscale re-verifies the cached executable and selected model before execution. A mirror or replaced cache file cannot substitute a modified binary or model without being rejected.

For a private mirror, mirror the exact upstream URL hierarchy and set a prefix, or use a prefix containing `{url}`. Example: `https://mirror.example/fetch?url={url}`.

## Troubleshooting

- `Unsupported platform`: use macOS or Windows x64.
- `All download sources failed`: set `IMAGE_UPSCALER_MIRRORS` to a reachable internal/domestic proxy, or prefill the cache on a connected machine.
- `SHA-256 mismatch`: do not continue. Remove only the named `.part` or cached artifact and retry from another source.
- Vulkan or GPU error: update the graphics driver and verify Vulkan support. Virtual machines often lack sufficient Vulkan passthrough.
- Out of GPU memory: retry `upscale.py` with `--tile 256`, then `--tile 128`.
- Slow processing: use `--model lite`, avoid `--tta`, and process files one at a time.
- Unsure which model is cached or how large it is: run `python scripts/setup.py --list-models` before downloading.
- Exact WebP resizing is intentionally not performed through platform APIs. Use PNG/JPEG for exact 2K/4K dimensions, or WebP with `--target scale4`.
