---
name: live-photo-maker
description: Convert a local video into an iPhone-compatible Live Photo package (.pvt) for Apple Photos, lock-screen wallpaper use, or Live Photo sharing. Use when the user gives a short video and wants an iPhone-ready Live Photo or live wallpaper package.
---

# Live Photo Maker

1. Take a local video file as input.
2. If needed, make an optimized version for iPhone wallpaper use:
   - upscale gently with `ffmpeg`
   - keep portrait aspect ratio
   - avoid aggressive recompression unless necessary
3. Extract a high-quality cover frame as JPG.
4. Use `makelive` to build a `.pvt` Live Photo package from the JPG + video pair.
5. If the user needs chat delivery, package the `.pvt` bundle as ZIP because `.pvt` is a macOS package directory and many messengers cannot send it directly.
6. Explain that the ZIP should be unzipped on macOS and the `.pvt` imported into Photos.

## Main features

- turns a local video into an Apple Photos-importable Live Photo
- can optimize video size for iPhone wallpaper use
- generates a high-quality cover frame automatically
- produces a `.pvt` package and optional ZIP for transfer
- works well for iPhone lock-screen wallpaper workflows

## Notes

- Install missing dependencies yourself when safe: `pipx`, `makelive`, `ffmpeg`.
- The video quality inside the Live Photo usually stays close to the source. Perceived softness is often caused by low source resolution or lock-screen scaling.
- Prefer sending both the original Live package path and the ZIP when useful.
