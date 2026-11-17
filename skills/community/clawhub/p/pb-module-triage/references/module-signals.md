# BrainNode PB Module Signals

Use this reference when the issue description is ambiguous or when the PB triage
script flags several modules with similar scores.

## TotalDataCore Buffers

| Buffer | Message | Module | Primary evidence |
|---|---|---|---|
| `data_core_frames_buffer` | `DataCoreFrame` | raw sensors / recording | point cloud, image, H264/rangeframe, IMU, GPS, env, speed, timestamps |
| `perceptor_frames_buffer` | `PerceptorFrame` | lidar perception / odometry | `odom`, `sem_perception.layers`, semantic entities, lidar/gps diagnostic |
| `camera_perceptor_frames_buffer` | `CameraPerceptorFrame` | camera perception | segments, static/moving objects, driving spaces, camera semantic map |
| `contextor_frames_buffer` | `ContextInfo` | localization / map matching | `alignment_valid`, `map_accepted`, confidence, residual, `T_map2odom`, `mf_pose` |
| `tasker_frames_buffer` | `TaskerFrame` | planning / tasker | command, trajectory, global path, CCPP cost map/path, embedded state management |
| `controller_frames_buffer` | `Controller` | control output | `x_spd`, `y_spd`, `eps`, `brake` |
| `data_chassis_frames_buffer` | `DataCahssisFrame` | chassis feedback | actual speed, wheel steering, gear, brake, control mode, emergency/touch status |
| `stormer_frames_buffer` | `DataStormFrame` | task dispatch / route input | `raw_nav_task`, map info, task status, mark point |
| `state_management_buffer` | `StateManagement` | system state | module modes, abnormal state, task type/mode/category |
| `diagnostics_frames_buffer` | `DiagnosticsFrame` | health/diagnostics | lidar/camera/chassis/process/sys diagnostic level and values |

## Symptom Routing

| Symptom words | Start with | Then compare |
|---|---|---|
| 定位飘, 跳变, 丢定位, 重定位失败, map mismatch | `ContextInfo`, `PerceptorFrame.odom`, GPS/IMU in `DataCoreFrame` | If contextor invalid while raw sensors continue, suspect localization/contextor. If IMU/GPS/timestamps break first, suspect DataCore/sensors. |
| 避障异常, 漏检, 误检, 大车/行人/障碍不对 | `PerceptorFrame.sem_perception`, camera perception buffers | If semantic entities/layers are missing before tasker reacts, suspect perception. If perception sees obstacle but trajectory collides/stops oddly, suspect tasker. |
| 路径不走, 到不了, 卡住, 画龙, CCPP/清扫异常 | `TaskerFrame.trajectory_points`, `global_path`, CCPP fields, `StateManagement.state_2` | If tasker trajectory is empty or abnormal while perception/localization are valid, suspect planning/tasker. If controller ignores non-empty trajectory, suspect control. |
| 速度慢, 方向盘异常, 抖动, 横向误差 | `Controller`, chassis actual feedback | If controller command is already wrong/zero, suspect control or upstream planning. If command is correct but chassis speed/steer does not follow, suspect chassis. |
| 急停, 防撞条, 档位, 底盘无响应 | `DataCahssisFrame.chassis_state`, `chassis_info` | Verify controller command vs chassis speed/gear/brake/control mode. Emergency/touch status usually explains planned stop. |
| 任务下发错误, POI/路线错误, 地图版本不一致 | `DataStormFrame.raw_nav_task`, `map_info`, `TaskerFrame.task_id` | If dispatch route/destination is wrong before perceptor/tasker consume it, suspect task dispatch or map/task data. |
| 进程异常, 频率掉线, WARN/ERROR | `DiagnosticsFrame`, buffer rates/gaps | Use diagnostics as supporting evidence, then identify the first module whose data becomes stale or invalid. |

## Evidence Hierarchy

Prefer direct PB evidence over symptom wording.

1. First abnormal timestamp in a downstream module is not enough for root cause.
   Compare upstream modules within the same time window.
2. Root cause is often the earliest upstream break that explains the downstream
   behavior.
3. Distinguish command and execution:
   - `TaskerFrame.trajectory_points` non-empty + `Controller.x_spd` near zero:
     control or control gating.
   - `Controller.x_spd` nonzero + chassis actual speed near zero:
     chassis, brake, gear, emergency stop, or control mode.
   - perception empty/invalid + tasker empty trajectory:
     perception may be the root cause.
4. Distinguish localization and planning:
   - `ContextInfo.alignment_valid=false`, low confidence, high residual, or
     `map_accepted=false` before path failure points to localization/contextor.
   - `ContextInfo` valid but tasker trajectory is empty/unsafe points to tasker.
5. Treat missing buffers carefully:
   - A PB may be DataCore-only. Missing tasker/control buffers means "not
     recorded", not necessarily a module fault.
   - For map-building PB, `semantic_map.pb` and `submap_*.pb` are output artifacts,
     not TotalDataCore logs.

## Useful Existing Project Tools

Run these from the project root when available:

```bash
python3 brainnode_toolkit/pb_view/pb_size_viewer.py FILE.pb --type TotalDataCore --decode-total-buffers
python3 brainstorm_mapper_git/tools/pb_dumper.py INPUT.pb --output OUTPUT_DIR
python3 brainnode_perceptor/tools/split_total_datacore_pb.py INPUT.pb --parts 4 --output-dir OUT
brainnode_tasker-tasker_dr5t_rc0725/run_pb_tasker_rerun.bash INPUT.pb --offline
```

Use `pb_size_viewer.py` for schema/size/field presence checks, `pb_dumper.py` for
raw sensor extraction, `split_total_datacore_pb.py` for narrowing long clips, and
tasker rerun for reproducing planning/control behavior against recorded inputs.

## Output Contract

Final answers should include:

- Problem summary: one sentence using the user's words.
- Primary suspected module: module name plus confidence (`high`, `medium`, or
  `low`).
- Evidence: concrete PB fields, counts, timestamps, anomalies, and upstream /
  downstream comparisons.
- Module analysis table: at least `data_core`, `perception`, `localization`,
  `planning_tasker`, `control`, `chassis`, and any issue-specific modules.
- Next checks: only the smallest checks needed to confirm or disprove the
  attribution.

Avoid claiming root cause when the PB only supports correlation. Say "more
likely" or "needs replay/visual confirmation" when evidence is incomplete.
