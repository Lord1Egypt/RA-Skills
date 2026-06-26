---
name: openvino-yolo-aipc
description: Turbocharge YOLO26 on Intel AI PCs with Ultralytics + OpenVINO. Use this skill to export compressed FP32/INT8 OpenVINO models, deploy live camera or video inference with compact scripts, switch execution across CPU/GPU/NPU, benchmark acceleration, and build local AI PC vision workflows such as people counting, inventory/object counting, and safety-zone alerts.
---

# YOLO26 OpenVINO Turbo for AI PCs

Turn a YOLO26 model into a local AI PC vision app: export it to OpenVINO, shrink it with INT8 quantization, run it on Intel CPU/GPU/NPU, and compare acceleration without writing a heavyweight inference stack.

The skill focuses on fast deployment: a short Ultralytics-integrated script handles OpenVINO export and inference, while wrappers let an agent choose device, precision, model size, benchmark mode, and downstream task behavior.

The default example uses `yolo26n.pt` because the nano model is quick to download, export, and run live. Users can choose other YOLO26 model sizes such as `yolo26s.pt`, `yolo26m.pt`, or `yolo26l.pt` when they need more accuracy and can afford higher latency or memory use.

The preferred implementation path is the official Ultralytics + OpenVINO integration: export with `YOLO(...).export(format="openvino")`, then load the exported OpenVINO model folder with `YOLO(...)` and run inference using Intel device strings such as `intel:cpu`, `intel:gpu`, or `intel:npu`. This keeps the public demo code short while still using OpenVINO acceleration and device targeting.

## Best use cases

Use this skill for:

- Live object detection from a laptop camera or video file.
- Compressing YOLO26 nano, small, medium, or large models into OpenVINO FP32 and INT8 exports.
- Accelerating YOLO26 inference on Intel CPU, GPU, and NPU from one compact workflow.
- Switching device and precision quickly for benchmark or live comparison.
- Building downstream interactions from detections, such as people counting, inventory/object counting, safety-zone alerts, and object-based UI events.

## 30-second start

Open PowerShell in the skill scripts folder:

```powershell
cd "{baseDir}\scripts"
.\setup_env.ps1
```

Run the live camera demo with the built-in camera:

```powershell
.\run_ultralytics_demo.ps1 -Mode live -Source 0 -Device GPU -Model yolo26n.pt -Precision fp32
```

Export or prepare INT8, then run it:

```powershell
.\run_ultralytics_demo.ps1 -Mode export -Precision int8
.\run_ultralytics_demo.ps1 -Mode live -Source 0 -Device NPU -Precision int8
```

Use a larger YOLO26 variant when accuracy matters more than speed:

```powershell
.\run_ultralytics_demo.ps1 -Mode export -Model yolo26s.pt -Precision int8
.\run_ultralytics_demo.ps1 -Mode live -Source 0 -Device GPU -Model yolo26s.pt -Precision int8
```

Run a repeatable benchmark from a video or camera frame:

```powershell
.\run_ultralytics_demo.ps1 -Mode benchmark -Source 0 -Device CPU -Precision int8 -BenchmarkSeconds 8
```

Run the downstream action demo:

```powershell
.\run_downstream_demo.ps1 -Source 0 -Device NPU -Precision int8 -Task inventory-count -Target bottle
```

The main YOLO demo overlay shows device, precision, live FPS, inference latency, and detection count. Normal skill usage should prefer command parameters so an agent can choose device, precision, model size, benchmark mode, and downstream task directly.

## Recommended AI PC Flow

Start with a visible contrast:

1. Export `yolo26n.pt` to OpenVINO FP32, then INT8.
2. Run the same video or camera input on GPU, NPU, and CPU.
3. Compare overlay metrics or benchmark mode to explain acceleration and quantization.
4. Switch from raw detection to an AI PC task: people counting, object counting, or safety-zone alerting.
5. Use `-CountZone` and `-DangerZone` to adapt the task to the user's real scene.

## Script entrypoints

Use these files from `{baseDir}\scripts`:

- `setup_env.ps1`: create `.venv` and install Python dependencies.
- `run_ultralytics_demo.ps1`: PowerShell wrapper for live, export, and benchmark modes. It exposes `-Model`, `-Precision`, `-Device`, OpenVINO performance hint, and async request controls.
- `run_ultralytics_openvino_demo.py`: Ultralytics + OpenVINO implementation with runtime device and precision switching.
- `run_downstream_demo.ps1`: PowerShell wrapper for person counting, object counting, and safety-zone alerts.
- `run_downstream_demo.py`: downstream action layer on top of Ultralytics + OpenVINO detections.
- `requirements.txt`: Python dependency list.
- `demo_utils.py`: lightweight overlay helper.

## Model and network behavior

Setup and first export require network access for Python packages, YOLO model weights, and INT8 calibration data if they are not already cached. After the OpenVINO model folders exist, live inference can run locally.

The default model is `yolo26n.pt`. The exported OpenVINO models are saved under `{baseDir}\scripts\integrated_models` using the model stem and precision, for example `yolo26n_int8_openvino_model` or `yolo26s_fp32_openvino_model`.

If the user already has an exported OpenVINO model folder, pass it with `-OpenVinoModelDir`.

## Region-Based Downstream Tasks

Downstream tasks can use normalized regions of interest:

- `-CountZone "x1,y1,x2,y2"`: count people only in a custom area, such as a queue, doorway, or meeting-room zone. Empty means full frame.
- `-DangerZone "x1,y1,x2,y2"`: trigger safety-zone alerts only when a person enters the configured danger area. The default is the top-right third: `0.667,0,1,0.333`.

## Choosing the right demo path

Use the Ultralytics-integrated path when the user values short, readable code and quick onboarding. It is the cleanest public skill path.

Use a lower-level OpenVINO AsyncInferQueue implementation outside this skill only when the user specifically needs maximum pipeline control, custom preprocessing, custom async scheduling, OpenVINO `MULTI` throughput pipelines, or deeper performance tuning. The live Ultralytics path intentionally focuses on readable code and CPU/GPU/NPU switching.

## References

Read these only when needed:

- `{baseDir}\references\downstream_playbooks.md`: downstream interaction ideas and implementation patterns.
- `{baseDir}\references\performance_notes.md`: how to explain and benchmark CPU/GPU/NPU and FP32/INT8 differences.
