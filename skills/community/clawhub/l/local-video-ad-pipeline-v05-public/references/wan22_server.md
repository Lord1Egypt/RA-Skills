# Wan2.2 Server Tuning

Verified on the Strix Halo local host.

## Servers

| Server | Path | Port | Use |
| --- | --- | --- | --- |
| WSL fp16 | `C:\Users\k0103\Desktop\ComfyUI WSL Wan2.2.bat` | 8192 | Production, dual fp16, AOTriton |
| ZLUDA Q8 | `C:\Users\k0103\Desktop\ComfyUI-Server-Wan22-ROCm7.bat` | 8188 | Single-shot fast tests; unstable for repeated dual-unet runs |

WSL IP can drift. `127.0.0.1:8192` works when WSL2 mirrored networking is active.

## Lifecycle

Never restart WSL ComfyUI between shots unless it is wedged. The first fp16 load is slow. Warm runs are much faster because the models stay resident.

Recommended sequence:

1. Start `ComfyUI WSL Wan2.2.bat`.
2. Run `python scripts/doctor.py --comfy http://127.0.0.1:8192`.
3. Run `python scripts/fire_warmup.py --comfy http://127.0.0.1:8192`.
4. Wait for `fire_warmup_out_00001.mp4` in the WSL output folder.
5. Queue shots with `python scripts/fire_videos.py --project <project>`.
6. Wait by checking files, not HTTP history.
7. Copy outputs with `python scripts/fire_videos.py --project <project> --collect`.

## Do Not Poll During Render

Avoid `/queue` and `/history` loops while Wan2.2 is rendering. Previous experiments showed that polling can coincide with silent ComfyUI crashes. The scripts queue work and exit; output collection happens from the filesystem afterward.

## Resolution Envelope

Strix Halo with a 96 GB UMA allocation:

- Safe: 832x480 / 33 frames, 16 fps, Lightning 4-step, dual fp16.
- Shorts safe: 480x832 / subtitle-planned frames, 16 fps, Lightning 4-step, dual fp16.
- No-slow 5s target: 832x480 / 80-81 frames, 16 fps, Lightning 4-step, dual fp16. This is slower but avoids `setpts` stretching.
- Pushed: 832x480 / 81+ frames can work but has thin memory margin.
- 720p is not recommended for this dual-fp16 path.

Standard clips can be slowed in `compose.py` to hit the target per-shot duration. For motion that must not look slow, render more frames natively and compose with `compose.py --no-slow --target-duration <seconds>`. If the no-slow final is short, add a short native clip or render more frames; do not stretch frames.

## Models

```
diffusion_models/
  wan2.2_i2v_high_noise_14B_fp16.safetensors
  wan2.2_i2v_low_noise_14B_fp16.safetensors
text_encoders/
  umt5_xxl_fp16.safetensors
vae/
  wan_2.1_vae.safetensors
loras/
  wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors
  wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors
```

Required custom nodes:

```
WanVideoWrapper
ComfyUI-GGUF
ComfyUI-KJNodes
ComfyUI-VideoHelperSuite
```
