# LibreLinkUp Monitor: Gotchas, Failure Modes, and Operational Truths

Hard-won operational knowledge gathered from deploying and running autonomous continuous glucose monitoring (CGM) companion agents. Read this before designing your alert logic.

> **LEGAL & REGULATORY NOTICE:**  
> This documentation is provided for research, education, and personal interoperability purposes only. It is not medical advice. FreeStyle Libre and LibreLinkUp are trademarks of Abbott Laboratories.

---

## 1. The Trend Enum Inversion Trap

In the official Abbott LibreLinkUp cloud protocol (and implemented in `pylibrelinkup/models/data.py` as `class Trend(IntEnum)`):

```
0 = UNKNOWN
1 = DOWN_FAST   (Rapidly falling, > 2 mg/dL/min)
2 = DOWN_SLOW   (Falling, 1-2 mg/dL/min)
3 = STABLE      (Slow change, < 1 mg/dL/min)
4 = UP_SLOW     (Rising, 1-2 mg/dL/min)
5 = UP_FAST     (Rapidly rising, > 2 mg/dL/min)
```

### The Pitfall
Many developers intuitively guess that `4` and `5` represent falling values (associating higher numbers with severity) and write rules like `if trend >= 4: alert_falling()`.
* **The Failure:** That rule fires alerts when blood sugar is **rising**, while remaining completely blind to real, dangerous plummets (`1` and `2`).
* **The Rule:** Always assert `trend in {1, 2}` for falling trajectories.

---

## 2. The Data Path Nesting Trap

When inspecting the raw JSON response from LibreLinkUp:
* The live glucose measurement lives at:  
  `data.connection.glucose_measurement.value_in_mg_per_dl` (or `.value`)
* It does **NOT** live at the flat path:  
  `data.glucose_measurement.value`

### The Pitfall
In Python dict or object navigation, querying the flat path returns `None` rather than raising an exception.
* **The Failure:** A poller written with the flat path reads `None` on every tick, defaults to a quiet state, and reports "all clear" indefinitely—creating a completely silent, broken safety net that can never alarm.
* **The Rule:** Use `client.latest(patient_id)` or verify the full nested structure `data.connection.glucose_measurement`.

---

## 3. The 400.0 mg/dL Sensor Ceiling Trap

FreeStyle Libre sensors have a physical measurement ceiling of 400.0 mg/dL (or ~22.2 mmol/L).
* When glucose exceeds 400, the API returns a flat `400.0` with `is_high: true` and `trend: 0 (UNKNOWN)`.

### The Pitfall
Do not interpret a flat sequence of `400.0` readings as a stable plateau. It is a sensor saturation clamp.
* **The Rule:** Check `client.graph(patient_id)` (which returns ~141 historical data points spanning the last 12 hours). Look at the trajectory *entering* the ceiling (e.g. `250 → 310 → 365 → 400`) to determine if blood sugar is actively climbing or beginning to recover.

---

## 4. The Android / Samsung DND "Modes and Routines" Re-arming Trap

On modern Android devices (especially Samsung Galaxy devices), Do Not Disturb is not a single toggle.

### The Pitfall
A user might manually configure their notification settings to allow LibreLinkUp or Telegram through Do Not Disturb. However, Samsung's **"Modes and Routines"** (specifically the scheduled *Sleep* mode) frequently maintains its own independent DND profile that re-arms every night at bedtime, silently overriding the manual exceptions.
* **The Failure:** The user tests the alert during the day, it works, but overnight when Sleep Mode activates, the alert is muted and the user sleeps through a low.
* **The Rule:** Users must explicitly navigate to `Settings → Modes and Routines → Sleep → Do Not Disturb → Allow Exceptions → Apps` and add their alert channel there directly.

---

## 5. The Two-App Alarm Trap

Many patients use the primary **FreeStyle Libre** sensor app on their phone, while their caregiver or agent connects via **LibreLinkUp**.
* The primary app connects via local Bluetooth Low Energy (BLE) to the sensor.
* The LibreLinkUp client receives data synced through Abbott's cloud servers.
* **The Benefit:** If the patient's phone loses Bluetooth contact with the sensor, or if the primary app crashes, an autonomous agent polling LibreLinkUp provides an independent, redundant cloud telemetry channel.
* **The Rule:** Do not rely on a single channel. An agent companion should supplement, not replace, physical sensor alarms and fingerstick blood glucose meters.

---

## 6. Zero Meter = Zero Ground Truth

Continuous glucose monitors measure **interstitial fluid**, not capillary blood. Interstitial fluid lags blood glucose by 5 to 15 minutes. Furthermore:
* Compression lows (sleeping directly on the sensor) can cause false plunges.
* Sensor detachment or calibration drift can produce erratic readings.

**The Golden Safety Rule:** An agent must always instruct the user to verify a low reading with a physical fingerstick blood glucose meter before administering large emergency carbohydrate loads or making acute clinical adjustments.
