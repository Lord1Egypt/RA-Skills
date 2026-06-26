# Character Replace Module

Character Replace from image, video, or reference materials.

## Supported Task Types

| Type | Description | Required Params |
|------|-------------|-----------------|
| `Full_Scene` | **Full Scene Replace** — Use the whole image's person and  background in the video | `--input-image` , `--input-video` |
| `Body_Only` | **Only Body Replace** — Use the image's person in the video, keep the video's background | `--input-image` , `--input-video` |

## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** New request, start to finish | Yes — waits until done |
| `submit` | Batch: fire multiple tasks without waiting | No — exits immediately |
| `query` | Recovery: resume polling a known `taskId` | Yes — waits until done |
| `list-models` | Check models, constraints, and audio support | No |
| `estimate-cost` | Estimate credit cost before running | No |

## Usage

```bash
python {baseDir}/scripts/video_mimic.py <subcommand> --type <Full_Scene|Body_Only> [options]
```

## Examples

### List Models

```bash
python {baseDir}/scripts/video_mimic.py list-models --type Full_Scene
python {baseDir}/scripts/video_mimic.py list-models --type Body_Only --json
```

### Full Scene Replace (Full_Scene)

```bash
python {baseDir}/scripts/video_mimic.py run \
  --type Full_Scene \
  --model "Kling V3.0" \
  --resolution 720 \
  --input-image <fileUrl> \
  --input-video <fileUrl> 
```

### Only Body Replace (Body_Only)

```bash
python {baseDir}/scripts/video_mimic.py run \
  --type Full_Scene \
  --model "Wan 2.2" \
  --resolution 720 \
  --input-image <fileUrl|local_file> \
  --input-video <fileUrl|local_file> 
```

### Cost Estimation

```bash
python {baseDir}/scripts/video_mimic.py estimate-cost \
  --model "Kling V3.0" --resolution 720 --input-video "C:\\video.mp4"
```

### Recovery / Batch

```bash
TASK_ID=$(python {baseDir}/scripts/video_mimic.py submit \
  --type Full_Scene \
  --model "Kling V3.0" \
  --resolution 720 \
  --input-image <fileUrl|local_file> \
  --input-video <fileUrl|local_file> 

python {baseDir}/scripts/video_mimic.py query \
  --task-id <taskId> --timeout 1200
```

## Common Options

| Option | Description                                                                                                                                  |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `--type` | Task type: `Full_Scene`, `Body_Only` (required)                                                                                              |
| `--model` | Model **display name** (`Kling V3.0`, `Seedance 2.0`, `Wan 2.2`)                                                                             |
| `--resolution` | `480`or `720`                                                                                                                                |
| `--input-image` | input image(image url or local path). E.g. image url: `--input-image "https//photo.jpg"` or local file: `--input-image "/path/to/photo.jpg"` |
| `--input-video` | input video(video url or local path). E.g. video url: `--input-video "https//video.mp4"` or local file: `--input-video "/path/to/video.mp4"` |
| `--timeout` | Max polling time (default: 600)                                                                                                              |
| `--interval` | Polling interval (default: 60)                                                                                                               |
| `--output-dir` | Download result videos to directory                                                                                                          |
| `--json` | Output full JSON response (not used by default; only when the user explicitly requests raw JSON output)                                      |
| `-q, --quiet` | Suppress status messages                                                                                                                     |

## Body_Only only

- Only model `Wan 2.2` support `--type Body_Only` — check via `list-models`

## Model Recommendation

> **Note:** `Standard` and `Fast` are top-tier models with industry-leading visual quality, native audio, and up to 15s duration, delivered Seedance 2.0-level capabilities. Available for all three task types (i2v, t2v, omni). Use `Standard` for best quality; use `Fast` for quicker turnaround at similar quality.

**By priority:**

| Priority            | Recommended Models | Why                      |
|---------------------|--------------------|--------------------------|
| **Best quality**    | Kling V3.0 | Top-tier visual fidelity |
| **Fast turnaround** | Seedance 2.0 | Quicker, lower cost      |
| **quality**         | Kling V3.0 | support 720p             |
| **Budget**          | Seedance 2.0 | Lowest cost              |
| **Native audio**    | Kling V3.0 | Ambient sound            |


**Defaults** (when user has no preference):
- Full_Scene → `Kling V3.0` or `Seedance 2.0`
- Body_Only → `Wan 2.2`

