# VX recording and acceptance contract

Read this before an agent configures a project's recorder or assesses recorded
training. GLR supplies the output preset, lifecycle, artifact paths, and index
contract; the project supplies an authorized exact-window input and runtime
observations. FFmpeg alone cannot produce observation/action labels.

## Preflight

```powershell
glr --project . --json doctor
glr --project . --json capture preset
glr --project . --json capture layout
vx ffmpeg -version
vx ffmpeg -hide_banner -encoders
vx ffprobe -version
```

Require `libx264` in the encoder inventory for `training-balanced`. Some VX
FFmpeg builds exclude it. If missing, report `encoder_unavailable` and resolve a
compatible VX-managed build before starting required capture. Do not silently
substitute another H.264 encoder: CRF and GOP options are encoder-specific.
Record the resolved tool version/build and pin the tested version in the project's
VX configuration. Version output alone does not prove encoder availability.

Use the returned `ffmpeg_output_argv`, with only its final `{capture_video}`
replaced by `GLR_CAPTURE_VIDEO`. It supplies aspect-preserving scale/pad to
1920x1080, square pixels, 30 FPS CFR, libx264, CRF 18, fast, yuv420p, High profile,
GOP 30, fixed keyframes, MP4 fast-start, and no audio. Keep capture manifest
codec/dimensions/frame rate consistent with this preset. Inspect the actual
frame for readable UI; upscaling cannot restore missing detail.

## Recorder integration

Construct a fixed argument array and spawn it without a shell:

```text
["vx", "ffmpeg", "-hide_banner", "-n"]
  + reviewed_platform_input_argv
  + preset.ffmpeg_output_argv_with_resolved_video_path
```

`reviewed_platform_input_argv` is an integration boundary, not literal command
text. Obtain it from the project's existing recording provider, bound to the
verified game window. Do not guess a title, capture the whole desktop, or reuse
stale window coordinates. For DCC-CUA UI observation/input, first report
`provider=dcc-cua`, runtime version, target PID, and HWND. Keep binding evidence
local. Preserve the project's DCC-CUA routing requirement.

The configured recorder role must concurrently write `GLR_CAPTURE_INDEX`, observe
the GLR stop protocol, forward a clean `q` stop to FFmpeg when using stdin-q, wait
for MP4 finalization, and register the resulting artifacts. Use finite training
budgets; start and verify capture before gameplay. A required capture failure
must stop the run. Do not configure bare FFmpeg as a training recorder unless
an existing integration also supplies the synchronized index and lifecycle.

For each indexed observation, emit `glr.capture-frame.v1` with `run_id`,
`episode_id` (UUID), `step_id`, `frame_index`, `pts_ns`, and
`observation_timestamp_ns`. Use the actual runtime observation and decoded output
frame association. Account for FPS conversion, dropped/duplicated frames, and
clock offsets. Never invent step IDs from frame numbers or equate wall-clock
time with media PTS. Record synchronization uncertainty and reject training use
when correspondence cannot be established. Hash and register the video and index
in the capture manifest under the run directory.

## Finalized media checks

Set `$video` to the finalized path returned for this run. Save JSON output and
check command exit codes; examples below do not discover or start a capture.

```powershell
vx ffprobe -v error -count_frames -show_streams -show_format -of json $video
vx ffmpeg -v error -xerror -i $video -map 0:v:0 -f null -
vx ffprobe -v error -select_streams v:0 -show_frames -show_entries frame=best_effort_timestamp_time,key_frame -of json $video
```

Require one H.264 video stream, 1920x1080, yuv420p, 30 FPS, positive duration
and decoded frame count, no audio, and a clean full decode. Check frame PTS
spacing for CFR and keyframe intervals against GOP 30. Stream metadata alone
does not prove constant cadence; CRF/encoder preset require the recorded argv
and encoder log. Save large frame reports to files rather than chat output.

Use `verify_capture_manifest` and `read_capture_index` from
`game_learning_runtime.capture` in the project's VX-managed Python environment
to verify artifact hashes, environment/run identity, schema, and monotonicity.
Additionally check each index frame exists in the decoded stream, its PTS agrees
within the declared synchronization tolerance, and its episode/step exists in
the authoritative transition dataset. The existing manifest validator does not
decode video or prove semantic synchronization by itself.

## Agent QA

Extract frames through VX into this run's report directory. Inspect the start,
middle, end, scene changes, and indexed failure/terminal events. For a chosen
timestamp and unique image path:

```powershell
vx ffmpeg -v error -n -i $video -ss $seconds -frames:v 1 $image
```

View those images. Check correct game content, aspect ratio, readable UI,
occlusion, black frames, frozen content during expected motion, and whether the
event is visible at its indexed time. Static menus are not automatically capture
failures. Use authoritative runtime evidence to assess gameplay outcomes.

Report media validity, visual QA, and training alignment separately. A decodable
video may support QA while remaining ineligible for training. Missing index,
labels, checksum verification, or clock alignment must prevent a training-ready
claim. Sampling frames does not prove the whole run is visually correct.

## Skill updates

`glr update` refreshes bundled project skills even at the same binary version.
Resolve the target project first, or pass an explicit `--skills-dir`; outside a
project update requires an explicit destination or `--no-skills`. Check `skills_updated`
in the JSON result and read the installed recording reference after updating.
`--no-skills` is an explicit binary-only opt-out. Host plugin/global skill copies
have separate owners and are not updated by this project-directory operation.
