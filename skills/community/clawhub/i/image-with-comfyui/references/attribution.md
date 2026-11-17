# Source Attribution (image-with-comfyui)

Every workflow in `workflows/` is an **adapted** version of a real ComfyUI
workflow. Original source + the specific modifications applied by this skill are
documented here. The workflow JSONs carry only ComfyUI's standard per-node
labels (`_meta` `title`); they do **not** embed provenance or attribution
metadata, so the original source is not duplicated inside them — it lives here
instead, and each file stays runnable.

| Workflow | Original source | Key modifications applied |
|---|---|---|
| `qwen_image_2.1_api.json` | [foprc/qwen-image-2.1-comfyui-workflow](https://github.com/foprc/qwen-image-2.1-comfyui-workflow) (ships GGUF Q8_0 + ComfyUI-GGUF) | Replaced GGUF model with standard **safetensors** via `UNETLoader` (`weight_dtype: fp8_e4m3fn_fast`) — removes the ComfyUI-GGUF dependency; added `UnloadModel` (node 18) + `UnloadAllModels` (node 19) VRAM-cleanup; dual-mode reference switch (nodes 12/13/14); `ResolutionSelector` (node 9); API/`timestamp` output |
| `qwen_image-edit_api.json` | Qwen-Image-Edit (Comfy-Org) default edit graph | Prompt auto-routing to the positive `TextEncodeQwenImageEditPlus` node (115:111) by the script |
| `sd3.5-med_t2i_api.json` | Comfy-Org / sd3-medium default graph | Fixed the `.safetensors.safetensors` double-suffix `ckpt_name` bug; `sd3_medium` → `sd3.5_large.safetensors` fallback; `UnloadAllModels` VRAM-cleanup |
| `z-image_t2i_api.json` | Comfy-Org / z-image default graph | `UnloadAllModels` VRAM-cleanup |
| `wan2.2_i2v_api.json` | Comfy-Org / Wan2.2 I2V default graph | Pointed the diffusion model at **4-step Lightspeed** weights; LoRA stack nodes (109/110); `UnloadAllModels` VRAM-cleanup |
| `hunyuan3d-v2.1_i2m_api.json` | Tencent Hunyuan3D-2.1 ComfyUI image→mesh reference graph (user-supplied, [tencent/Hunyuan3D-2.1](https://huggingface.co/tencent/Hunyuan3D-2.1)) | Topology kept 1:1 (including the user's VRAM-unload sink nodes 19/20/21/22); placeholder `image` set to `character.png` (the script always rewrites it to the uploaded filename); default `filename_prefix` kept (`mesh/hy21`) — the script stamps it per run to `mesh/i2m_<timestamp>`; no model/parameter changes — resolution 4096 / 30 steps / CFG 5.0 are the graph's own defaults and stay the skill defaults

All six are **adapted** (as opposed to) the original; they add prompt routing,
resolution selection, dual-mode switches, and VRAM management on top of the
original ComfyUI graphs.
