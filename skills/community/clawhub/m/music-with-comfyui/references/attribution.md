# Source Attribution (music-with-comfyui)

The workflow in `workflows/` is an **adapted** version of a real ComfyUI
AceStep Audio 1.5 workflow. The workflow JSONs carry only ComfyUI's standard
per-node labels (`_meta` `title`); they do **not** embed provenance or
attribution metadata, so the original source lives here instead, and the file
stays runnable.

| Workflow | Original source | Key modifications applied |
|---|---|---|
| `acestep_audio_api.json` | AceStep Audio 1.5 text-to-audio graph (TextEncodeAceStepAudio1.5 → AceStep-ComfyUI) | API-ready output node (SaveAudioAdvanced) + timestamped output filenames (`amusic_<timestamp>`); exposed tags/lyrics and all text-encode params (bpm, keyscale, language, timesignature, cfg_scale, temperature, top_p, top_k, min_p, duration, seed); VRAM-cleanup nodes (`UnloadModel` 112/113 + `UnloadAllModels` 114), auto-bypassed when absent; the empty-audio latent `seconds` set to match `duration`; default `filename_prefix` kept (`asa`) — the script stamps it per run to `amusic_<timestamp>` |

The workflow is **adapted** (as opposed to) the original; it adds API-ready
output, parameter exposure, and VRAM management on top of the original ComfyUI
graph. The model weights and CLIP/VAE files are the AceStep 1.5 release; see
[`MODEL_URL.txt`](MODEL_URL.txt) for the download locations and the CAVEAT
about filenames.
