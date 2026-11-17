---
name: pb-module-triage
description: Analyze BrainNode protobuf recordings from this autonomous-driving project against a natural-language problem description, identify the most likely faulty module, and produce an evidence-based module analysis. Use for .pb/TotalDataCore/DataCoreFrame recordings, PB replay or dump analysis, localization/perception/planning/control/chassis/task/diagnostics triage, timestamp and frame-drop investigation, and requests to output a problem-module analysis result.
---

# PB Module Triage

Use this skill to turn a reported autonomous-driving symptom plus one or more
protobuf recordings into a bounded module diagnosis. Read the recording first,
find the earliest upstream evidence that explains the symptom, and separate
observed facts from hypotheses.

## Workflow

1. **Normalize the request**
   - Preserve the user's original problem description.
   - Extract symptom, expected behavior, approximate time/clip, vehicle/task
     context, and supplied PB paths.
   - If no PB path is supplied, inspect the project for likely `.pb` recordings
     and state which files were selected.

2. **Identify the recording shape**
   - Treat `TotalDataCore` as the primary container.
   - Recognize direct `DataCoreFrame`, `PerceptorFrame`, `TaskerFrame`,
     `Controller`, `DataCahssisFrame`, `ContextInfo`, `StateManagement`,
     `DiagnosticsFrame`, `DataStormFrame`, and `CameraPerceptorFrame` files.
   - Do not treat `semantic_map.pb`, `reference_route*.pb`, or `submap_*.pb` as
     vehicle runtime logs unless the user explicitly asks for map analysis.
   - Read [references/module-signals.md](references/module-signals.md) when
     routing an ambiguous symptom or interpreting missing buffers.

3. **Run deterministic PB triage**

   From the project root, run:

   ```bash
   python3 ~/.codex/skills/pb-module-triage/scripts/pb_module_triage.py \
     PB_FILE_OR_DIR \
     --issue "PROBLEM DESCRIPTION" \
     --repo-root /home/jamin/Enjoo_pro \
     --max-files 20
   ```

   Use `--json --output report.json` when a machine-readable report is useful.
   For very large recordings, first use `--max-files`, `--max-file-bytes`, or
   `split_total_datacore_pb.py` to narrow the clip. Never load a multi-gigabyte
   PB into Python just to inspect its filename.

4. **Inspect flagged evidence**
   - Check frame count, timestamp span, estimated rate, sequence gaps, and parse
     errors for every available module.
   - Inspect module-specific metrics:
     - raw data: point cloud/image/IMU/GPS/rangeframe presence, GPS status,
       payload size, speed;
     - perception: semantic layer/entity counts and diagnostics;
     - localization: `alignment_valid`, `map_accepted`, match confidence,
       map residual, map-to-odom pose;
     - planning: trajectory/global path lengths, command, CCPP reason/status,
       embedded abnormal state;
     - control: speed/steering/brake commands;
     - chassis: actual speed/steering, gear, brake, control mode, emergency
       stop and touch sensors;
     - task dispatch: task ID, route/path code, destination and map version;
     - diagnostics: WARN/ERROR/STALE levels and key/value messages.
   - Use timestamps to find the first break. A downstream anomaly is evidence
     of impact, not automatically evidence of root cause.

5. **Cross-check the pipeline**
   - Compare `DataCoreFrame` timestamps to downstream buffers.
   - Compare perception semantic entities to tasker trajectory output.
   - Compare tasker trajectory to controller command.
   - Compare controller command to chassis feedback.
   - Compare localization validity to the onset of planning or control failure.
   - Treat absent buffers as unrecorded data, not as a fault.

6. **Assign module and confidence**
   - `high`: direct error/state field or a consistent upstream-to-downstream
     chain supports one module, with no stronger competing explanation.
   - `medium`: evidence supports a module but the recording lacks a needed
     upstream or execution buffer.
   - `low`: only keyword, timing, or indirect correlation is available.
   - Prefer the earliest module whose failure explains the later symptoms.
   - Name secondary affected modules separately from the primary suspected
     module.

7. **Produce the result**
   - Use the output contract below.
   - Include exact file names and timestamps/frame ranges when available.
   - Mark unsupported conclusions as hypotheses and list the minimum next
     check needed to confirm them.

## Output Contract

Write the final analysis in Chinese unless the user asks for another language:

```markdown
# 问题模块分析

## 结论
- 问题描述：...
- 首要怀疑模块：`module`（置信度：高/中/低）
- 受影响模块：...
- 结论边界：已观测事实 / 仍需验证...

## 证据摘要
| 时间/帧范围 | PB字段或统计 | 观察结果 | 解释 |
|---|---|---|---|
| ... | ... | ... | ... |

## 模块分析
| 模块 | PB证据 | 当前判断 | 置信度 |
|---|---|---|---|
| DataCore/传感器 | ... | ... | ... |
| Perception/感知 | ... | ... | ... |
| Localization/Contextor | ... | ... | ... |
| Planning/Tasker | ... | ... | ... |
| Control/Controller | ... | ... | ... |
| Chassis/底盘 | ... | ... | ... |

## 最小验证动作
1. ...
2. ...
```

Do not output a module score as if it were a measured probability. Explain why
the primary module outranks alternatives. If the PB is DataCore-only, explicitly
say that planning/control/chassis cannot be directly exonerated or blamed from
that file alone.

## Existing Project Tools

Use the existing tools when the initial report is insufficient:

```bash
python3 brainnode_toolkit/pb_view/pb_size_viewer.py FILE.pb \
  --type TotalDataCore --decode-total-buffers
python3 brainstorm_mapper_git/tools/pb_dumper.py INPUT.pb --output OUTPUT_DIR
python3 brainnode_perceptor/tools/split_total_datacore_pb.py INPUT.pb \
  --parts 4 --output-dir OUT
brainnode_tasker-tasker_dr5t_rc0725/run_pb_tasker_rerun.bash INPUT.pb --offline
```

Use `pb_size_viewer.py` for schema/field-size inspection, `pb_dumper.py` for
recovering raw GPS/IMU/image/env data, the splitter for isolating a time range,
and tasker replay for a reproducible planning check. Do not run replay merely
because a keyword matched; first establish that the required input buffers and
task context exist.
