---
name: locateanything
description: NVIDIA LocateAnything-3B vision-language grounding model. Covers inference API (detect/ground/point/detect_text/ground_gui), data preparation (JSONL+Recipe 8 tasks), training/fine-tuning, evaluation. For object detection, visual grounding, GUI recognition, OCR, etc.
---

# LocateAnything — Vision-Language Grounding

NVIDIA Eagle family VLM, based on Parallel Box Decoding (PBD) for single-step parallel prediction of complete coordinates. 12.7 BPS (H100) ≈ 10× Qwen3-VL.

Architecture: `MoonViT-SO-400M → MLP → Qwen2.5-3B → PBD`

## Installation

```bash
git clone https://github.com/NVlabs/Eagle eagle && cd eagle/Embodied
pip install -e .
# Optional MagiAttention (Hopper/Blackwell only, long sequences 32K+):
# git clone https://github.com/SandAI-org/MagiAttention.git && cd MagiAttention && git checkout v1.0.5
# git submodule update --init --recursive && pip install --no-build-isolation .
```

## Inference API

```python
from locateanything_worker import LocateAnythingWorker
from PIL import Image

worker = LocateAnythingWorker("nvidia/LocateAnything-3B")
img = Image.open("e.jpg").convert("RGB")

worker.detect(img, ["person", "car"])                    # Object detection
worker.ground_single(img, "the red car")                  # Single-instance grounding
worker.ground_multi(img, "people wearing hats")           # Multi-instance grounding
worker.detect_text(img)                                   # OCR
worker.ground_gui(img, "search button")                   # GUI box
worker.ground_gui(img, "search", output_type="point")     # GUI point
worker.point(img, "the traffic light")                    # Point grounding

# Low-level: worker.predict(image, question, generation_mode="hybrid")
# mode: fast(MTP) | slow(NTP) | hybrid(default)
```

## Output Parsing

```
Box: <ref>label</ref><box><x1><y1><x2><y2></box>
Point: <box><x><y></box>
Empty: <box>none</box>
```

Coordinates `[0,1000]` integers, divide by 1000 for relative coordinates.
```python
boxes = LocateAnythingWorker.parse_boxes(answer, w, h)  # Pixel coordinates
points = LocateAnythingWorker.parse_points(answer, w, h)
```

## Data Preparation

### JSONL (ShareGPT Format)
```jsonl
{"conversations":[{"from":"human","value":"Detect all objects in <image-1>."},{"from":"gpt","value":"<ref>car</ref><box><100><200><400><500></box>"}],"image":"train/00001.jpg"}
```

### Recipe JSON
```json
{"my_data":{"annotation":["a.jsonl","b.jsonl"],"root":"/data/images/","repeat_time":1.0,"data_augment":true}}
```
`repeat_time`: ≥1 oversample, <1 downsample. Coordinates normalized to `[0,1000]`.

### 8 Task Prompts

| Task | Method | Prompt |
|------|--------|--------|
| Detection | `detect(cats)` | `Locate all the instances that matches: cat1</c>cat2.` |
| Single instance | `ground_single(p)` | `Locate a single instance that matches: phrase.` |
| Multi instance | `ground_multi(p)` | `Locate all instances that match: phrase.` |
| OCR | `detect_text()` | `Detect all the text in box format.` |
| Text grounding | `ground_text(p)` | `Please locate the text referred as phrase.` |
| GUI box | `ground_gui(p)` | `Locate the region that matches: element.` |
| GUI point | `ground_gui(p,pt)` | `Point to: element.` |
| Point grounding | `point(p)` | `Point to: target.` |

Plain text: omit `image` field. Multi-image: `image_list` + `<image-1>` `<image-2>`.

## Training

```bash
torchrun --nproc_per_node=8 eaglevl/train/locany_finetune_magi_stream.py \
  --model_name_or_path nvidia/LocateAnything-3B \
  --meta_path "./recipe.json" --output_dir work_dirs/sft \
  --max_steps 25000 --lr 2e-5 --bf16 True --block_size 6 \
  --attn_implementation magi --max_seq_length 16384 --max_num_tokens 25600 \
  --deepspeed deepspeed_configs/zero_stage2_config.json
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `--block_size` | MTP chunk size (default 4), use `--causal_attn False` during training |
| `--attn_implementation` | `magi` (Hopper/Blackwell 32K+) or `sdpa` (any GPU ~4K) |
| `--freeze_llm/backbone/mlp` | Freeze corresponding modules |
| `--max_num_tokens` | Token budget per batch (recommend 2-3× `max_num_tokens_per_sample`) |
| `--packing_buffer_size` | Online packing buffer (default 32, 64-128 for higher efficiency) |

Non-Hopper GPU: `--attn_implementation sdpa --max_seq_length 4096`. OOM: `--grad_checkpoint True` + reduce `--max_num_tokens`.

Streaming Packing: Best-Fit + Big-Rocks-First algorithm, checkpoint resume bit-identical. DeepSpeed recommended `zero_stage2`.

## Evaluation

```bash
# COCO / LVIS
bash evaluation/scripts/eval_coco.sh --model_path ... --test_jsonl ... --coco_json ... --output_dir ...
bash evaluation/scripts/eval_lvis.sh --model_path ... --test_jsonl ... --lvis_json ... --output_dir ...

# General grounding (Dense200/DocLayNet/HumanRef/RefCOCOg/VisDrone etc.)
bash evaluation/scripts/eval_grounding.sh --dataset Dense200 --eval_type box_eval ...

# Point evaluation / ScreenSpot-Pro
bash evaluation/scripts/eval_grounding.sh --dataset COCO --eval_type point_eval ...
bash evaluation/scripts/eval_sspro.sh --model_path ... --test_jsonl ... --output_dir ...
```

Requires Rex-Omni `fastevaluate` + data `Mountchicken/Rex-Omni-EvalData` `likaixin/ScreenSpot-Pro`.

## Key Results

| Benchmark | Score | Comparison |
|-----------|:-----:|-----------|
| LVIS F1@Mean | **50.7** | +3.8 vs Rex-Omni |
| COCO F1@Mean | **54.7** | +1.8 vs Rex-Omni |
| M6Doc F1@Mean | **70.1** | +14.5 vs Rex-Omni |
| ScreenSpot-Pro Avg | **60.3** | SOTA |
| RefCOCOg val F1@Mean | **76.7** | SOTA |
| Pointing (7 benchmarks) | — | Best on all |
| PBD dense scenes | **2-6×** faster vs NTP |

## Model Info

- Name: `nvidia/LocateAnything-3B` | LLM: Qwen2.5-3B | Vision: MoonViT-SO-400M | Length: 25K
- HF: https://huggingface.co/nvidia/LocateAnything-3B
- Demo: https://huggingface.co/spaces/nvidia/LocateAnything
- Paper: arXiv:2605.27365

## License

Code Apache 2.0 | Model NVIDIA License (non-commercial research)

## References

- GitHub: https://github.com/NVlabs/Eagle
- Project page: https://nvlabs.github.io/Eagle/