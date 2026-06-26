# Performance Notes

This skill demonstrates OpenVINO acceleration through visible switching and compact Ultralytics code, not only raw benchmark tables.

## What to measure

Use two numbers in the overlay:

- Live FPS: end-to-end display pipeline speed, including camera/video reading, postprocessing, drawing, and UI display.
- Inference FPS or latency: Ultralytics-reported model inference time.

The live FPS is what visitors feel. The inference metric is better for comparing devices and precision.

## Suggested comparisons

Run each comparison for several seconds after switching so warmup frames do not dominate the average.

- CPU FP32 vs CPU INT8: usually the clearest INT8 speedup story.
- GPU FP32 vs GPU INT8: may be close on nano models because GPU FP32 is already fast and overhead can dominate.
- NPU INT8: best positioned as efficient dedicated AI execution, especially when the CPU and GPU should stay available.

## Model size tradeoffs

The default `yolo26n.pt` model is optimized for fast setup and responsive live demos. Larger YOLO26 variants such as `yolo26s.pt`, `yolo26m.pt`, and `yolo26l.pt` can improve accuracy but usually increase compile time, memory use, and per-frame latency.

Use this decision rule:

- `nano`: first-run demos, live camera, low latency, battery-friendly AI PC use.
- `small` or `medium`: better accuracy when the scene is harder or objects are smaller.
- `large`: accuracy-focused validation, not the first choice for a lightweight live demo.

## Explain surprising results honestly

If INT8 is not always faster, explain that performance depends on the model size, device plugin, preprocessing, postprocessing, and pipeline overhead. For very small nano models, camera capture and drawing can hide pure inference gains.

Use benchmark mode when the user wants cleaner inference comparison:

```powershell
.\run_ultralytics_demo.ps1 -Mode benchmark -Source 0 -Device CPU -Precision fp32
.\run_ultralytics_demo.ps1 -Mode benchmark -Source 0 -Device CPU -Precision int8
```

OpenVINO `MULTI` can produce very high pure-inference throughput when many async requests are in flight, but it may not improve a single live display stream. For the Ultralytics live path, prefer explicit `CPU`, `GPU`, or `NPU` switching. Use a lower-level OpenVINO async pipeline when the user specifically wants `MULTI:GPU,CPU,NPU` throughput behavior.

## Booth message

Avoid saying `INT8 is always faster`. Prefer:

`OpenVINO lets us choose the best Intel AI PC engine for the workload, and INT8 often improves latency, throughput, or efficiency, especially on CPU and NPU paths.`

## Tuning knobs

Use these only after the basic demo works:

- `-ImageSize 640`: default quality and speed balance.
- `-CameraWidth 1280 -CameraHeight 720`: request a clearer camera feed.
- `-BenchmarkSeconds 8`: stabilize measurements.
- `-Source <video path>`: use a repeatable input for fair comparisons.
