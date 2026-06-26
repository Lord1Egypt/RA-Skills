# Downstream Playbooks

Use YOLO detections as local AI PC events, not just boxes. Keep actions reversible and visible so users immediately understand cause and effect.

Core pattern:

- Detect target classes with YOLO26 + OpenVINO.
- Convert stable detections into structured events.
- Debounce events so one object does not trigger repeated actions.
- Keep the action local when privacy, latency, or offline operation matters.

## Person counter

Trigger: count detections where class name is `person`. By default the full frame is counted, but callers can set a custom normalized ROI with `-CountZone x1,y1,x2,y2`.

Best for: entrance counters, queue monitoring, meeting-room occupancy, classroom/lab utilization, retail staffing, and privacy-friendly local analytics.

Action ideas:

- Display current count and peak count in the overlay.
- Change the panel color when the count crosses a threshold.
- Save timestamped counts to CSV for a later chart.

Try it:

```powershell
.\run_downstream_demo.ps1 -Source 0 -Device NPU -Precision int8 -Task person-counter -Target person
```

Count only a queue or doorway region:

```powershell
.\run_downstream_demo.ps1 -Source .\sample_video.mp4 -Device GPU -Precision int8 -Task person-counter -Target person -CountZone "0.35,0.15,0.95,0.95"
```

The window shows current people, peak people, the selected target object, and action cues.

## Inventory and object counting

Trigger: count one or more object classes, such as `bottle`, `cup`, `book`, `laptop`, `cell phone`, `box`, or custom-trained product classes.

Best for: retail shelf checks, warehouse workbench counting, tool availability, cafeteria object flow, classroom device checkout, or local inventory snapshots.

Action ideas:

- Display current count, peak count, and low-stock or over-capacity status.
- Save timestamped counts to CSV for local reporting.
- Trigger a restock or inspection cue when count drops below a threshold.
- Use a custom YOLO26 model for product SKUs or domain-specific objects.

Example:

```powershell
.\run_downstream_demo.ps1 -Source 0 -Device NPU -Precision int8 -Task inventory-count -Target bottle
```

Implementation note: use stable object tracking or N-frame confirmation when the camera sees the same shelf or workbench for long periods.

## Safety zone and compliance alert

Trigger: a `person` enters a configured danger zone. The bundled demo defaults to the top-right one-third of the frame, `-DangerZone "0.667,0,1,0.333"`. Callers can set any normalized ROI with `-DangerZone x1,y1,x2,y2`. With a custom YOLO26 model, the same pattern can detect PPE such as helmet, vest, gloves, or mask.

Best for: lab benches, factory cells, robotics demos, restricted areas, device test stations, loading zones, and local safety assistants.

Action ideas:

- Draw a red danger zone in the overlay.
- Alert when a person enters a restricted zone for more than N frames.
- Alert when a required safety item is missing.
- Save local event logs without streaming video to the cloud.

Example:

```powershell
.\run_downstream_demo.ps1 -Source 0 -Device NPU -Precision int8 -Task safety-zone -Target person
```

Use a custom danger area:

```powershell
.\run_downstream_demo.ps1 -Source .\people.mp4 -Device GPU -Precision int8 -Task safety-zone -Target person -DangerZone "0.667,0,1,0.333"
```

Guardrails:

- Require stable detection over multiple frames.
- Add a cooldown, for example one action per 2 seconds.
- Keep the overlay simple: show whether the danger zone is clear or alerting, plus the number of people in the danger zone.

## Object trigger

Trigger: a target class appears with confidence above a threshold for N consecutive frames.

Good starter classes: `bottle`, `cell phone`, `laptop`, `cup`, `book`, `person`.

Action ideas:

- Play a sound or show a full-screen visual cue.
- Launch a local app or write a local event log.
- Show a message such as `Bottle detected: INT8 NPU path active`.

## Gesture-style control

Use YOLO detections as a simple proxy for gestures when a pose model is not needed.

Examples:

- Detect `cell phone` raised into the top-right zone to switch device.
- Detect `bottle` in the center zone to switch precision.
- Detect two people to trigger a side-by-side benchmark view.

## Implementation pattern

Add a small event layer after each prediction result:

```python
for box in result.boxes:
    cls_id = int(box.cls[0])
    name = result.names.get(cls_id, str(cls_id))
    conf = float(box.conf[0])
    if name == "bottle" and conf > 0.5:
        trigger_bottle_event()
```

For real applications, use debouncing:

```python
if event_is_active and time.perf_counter() - last_trigger > cooldown_seconds:
    run_action()
    last_trigger = time.perf_counter()
```

Validate the event layer without loading a model:

```powershell
.\run_downstream_demo.ps1 -SelfTest
```
