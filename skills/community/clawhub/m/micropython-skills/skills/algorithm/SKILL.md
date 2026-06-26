---
name: micropython-skills/algorithm
description: MicroPython on-device algorithms — PID controller, moving average, Kalman filter, state machine, task scheduler, data logger.
---

# On-Device Algorithms

Pure MicroPython algorithm implementations that run on the device.
These are **Safe tier** — no direct hardware side effects.

These algorithms are typically combined with sensor reads (input) and actuator control (output).
Upload as `.py` files via `mpremote fs cp algorithm.py :` for reuse.

## PID Controller

Classic PID with anti-windup for control loops (e.g., temperature regulation):

```python
import time, json

class PID:
    def __init__(self, kp, ki, kd, setpoint=0, output_min=-100, output_max=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_min = output_min
        self.output_max = output_max
        self._integral = 0
        self._last_error = 0
        self._last_time = time.ticks_ms()

    def compute(self, measurement):
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self._last_time) / 1000.0
        if dt <= 0:
            dt = 0.001
        self._last_time = now

        error = self.setpoint - measurement
        self._integral += error * dt
        derivative = (error - self._last_error) / dt
        self._last_error = error

        output = self.kp * error + self.ki * self._integral + self.kd * derivative

        # Anti-windup: clamp output and freeze integral if saturated
        if output > self.output_max:
            output = self.output_max
            self._integral -= error * dt
        elif output < self.output_min:
            output = self.output_min
            self._integral -= error * dt

        return output

# Example usage: temperature control
try:
    pid = PID(kp=2.0, ki=0.5, kd=0.1, setpoint=25.0, output_min=0, output_max=100)
    # Simulate 5 steps
    temps = [22.0, 23.1, 24.0, 24.8, 25.1]
    results = []
    for t in temps:
        out = pid.compute(t)
        results.append({"temp": t, "output": round(out, 2)})
        time.sleep_ms(100)
    print("RESULT:" + json.dumps({"pid_steps": results}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Moving Average Filter

Smooths noisy sensor readings using a ring buffer:

```python
import json

class MovingAverage:
    def __init__(self, window_size=10):
        self._buf = [0.0] * window_size
        self._idx = 0
        self._count = 0
        self._sum = 0.0
        self._size = window_size

    def add(self, value):
        old = self._buf[self._idx]
        self._buf[self._idx] = value
        self._sum += value - old
        self._idx = (self._idx + 1) % self._size
        if self._count < self._size:
            self._count += 1
        return self._sum / self._count

# Example: smooth noisy ADC readings
try:
    filt = MovingAverage(window_size=5)
    raw = [512, 498, 525, 510, 503, 515, 508, 520, 502, 511]
    smoothed = []
    for v in raw:
        s = filt.add(v)
        smoothed.append(round(s, 1))
    print("RESULT:" + json.dumps({"raw": raw, "smoothed": smoothed}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Kalman Filter (1D)

Better noise rejection than moving average, adapts to signal dynamics:

```python
import json

class KalmanFilter:
    def __init__(self, process_variance=0.01, measurement_variance=0.1, initial_estimate=0):
        self.q = process_variance      # Process noise
        self.r = measurement_variance  # Measurement noise
        self.x = initial_estimate      # Current estimate
        self.p = 1.0                   # Estimation error

    def update(self, measurement):
        # Prediction
        self.p += self.q
        # Update
        k = self.p / (self.p + self.r)  # Kalman gain
        self.x += k * (measurement - self.x)
        self.p *= (1 - k)
        return self.x

# Example: filter noisy temperature readings
try:
    kf = KalmanFilter(process_variance=0.01, measurement_variance=0.5, initial_estimate=23.0)
    readings = [23.2, 22.8, 23.5, 23.1, 24.0, 23.3, 22.9, 23.4, 23.0, 23.2]
    filtered = []
    for r in readings:
        f = kf.update(r)
        filtered.append(round(f, 2))
    print("RESULT:" + json.dumps({"raw": readings, "filtered": filtered}))
except Exception as e:
    print("ERROR:" + str(e))
```

## State Machine

Event-driven finite state machine for device behavior control:

```python
import json

class StateMachine:
    def __init__(self, initial_state, transitions):
        """
        transitions: dict mapping (state, event) -> (new_state, action_fn)
        action_fn receives (old_state, event, new_state) and returns optional data.
        """
        self.state = initial_state
        self.transitions = transitions
        self.history = []

    def handle(self, event):
        key = (self.state, event)
        if key not in self.transitions:
            return None
        old = self.state
        new_state, action = self.transitions[key]
        result = action(old, event, new_state) if action else None
        self.history.append({"from": old, "event": event, "to": new_state})
        self.state = new_state
        return result

# Example: simple thermostat (IDLE -> HEATING -> IDLE)
try:
    def start_heat(old, ev, new):
        return "heater ON"

    def stop_heat(old, ev, new):
        return "heater OFF"

    sm = StateMachine("IDLE", {
        ("IDLE", "too_cold"):    ("HEATING", start_heat),
        ("HEATING", "reached"):  ("IDLE", stop_heat),
        ("IDLE", "too_hot"):     ("COOLING", lambda o,e,n: "cooler ON"),
        ("COOLING", "reached"):  ("IDLE", lambda o,e,n: "cooler OFF"),
    })

    events = ["too_cold", "reached", "too_hot", "reached"]
    actions = []
    for ev in events:
        a = sm.handle(ev)
        actions.append({"event": ev, "action": a, "state": sm.state})

    print("RESULT:" + json.dumps({"transitions": actions}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Cooperative Task Scheduler

Run multiple periodic tasks without threads (uses Timer or manual scheduling):

```python
import time, json

class Scheduler:
    def __init__(self):
        self.tasks = []

    def add(self, name, interval_ms, callback):
        self.tasks.append({
            "name": name,
            "interval": interval_ms,
            "callback": callback,
            "last_run": 0,
        })

    def run(self, duration_ms=5000):
        """Run all tasks cooperatively for a fixed duration."""
        start = time.ticks_ms()
        log = []
        while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
            now = time.ticks_ms()
            for task in self.tasks:
                if time.ticks_diff(now, task["last_run"]) >= task["interval"]:
                    result = task["callback"]()
                    log.append({"task": task["name"], "time_ms": time.ticks_diff(now, start), "result": result})
                    task["last_run"] = now
            time.sleep_ms(10)
        return log

# Example: read sensor every 500ms, log every 2000ms
try:
    counter = {"reads": 0}

    def read_sensor():
        counter["reads"] += 1
        return counter["reads"]

    def log_status():
        return "reads=" + str(counter["reads"])

    sched = Scheduler()
    sched.add("sensor", 500, read_sensor)
    sched.add("log", 2000, log_status)

    events = sched.run(duration_ms=3000)
    print("RESULT:" + json.dumps({"events": events}))
except Exception as e:
    print("ERROR:" + str(e))
```

## Data Logger

Write sensor data to CSV on the device filesystem with size rotation:

```python
import os, time, json

class DataLogger:
    def __init__(self, filename="data.csv", max_size_kb=100):
        self.filename = filename
        self.max_bytes = max_size_kb * 1024
        self._ensure_header()

    def _ensure_header(self):
        try:
            os.stat(self.filename)
        except OSError:
            with open(self.filename, "w") as f:
                f.write("timestamp,value\n")

    def _check_rotation(self):
        try:
            size = os.stat(self.filename)[6]
            if size > self.max_bytes:
                try:
                    os.remove(self.filename + ".old")
                except:
                    pass
                os.rename(self.filename, self.filename + ".old")
                self._ensure_header()
                return True
        except:
            pass
        return False

    def log(self, value):
        self._check_rotation()
        with open(self.filename, "a") as f:
            f.write("{},{}\n".format(time.time(), value))

    def read_last(self, n=5):
        lines = []
        with open(self.filename, "r") as f:
            for line in f:
                lines.append(line.strip())
        return lines[-(n+1):]  # Include header

# Example
try:
    logger = DataLogger("sensor_log.csv", max_size_kb=50)
    for i in range(5):
        logger.log(22.5 + i * 0.3)
    last = logger.read_last(5)
    print("RESULT:" + json.dumps({"log_file": "sensor_log.csv", "last_entries": last}))
except Exception as e:
    print("ERROR:" + str(e))
```
