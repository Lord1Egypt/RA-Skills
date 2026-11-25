---
name: librelinkup-monitor
description: Monitor FreeStyle Libre CGM glucose telemetry via LibreLinkUp cloud API with zero-cost monitor-gated alerts for lows and rapid drops.
version: 1.0.0
author: iris-syzygy
license: MIT
metadata:
  hermes:
    icon: "assets/icon.png"
    tags:
      - health
      - cgm
      - diabetes
      - librelinkup
      - telemetry
      - automation
      - smart-home
    related_skills:
      - scheduled-automation
      - openhue
---

# librelinkup-monitor: Autonomous CGM Companioning for Hermes

Autonomous continuous glucose monitoring (CGM) companioning for Abbott FreeStyle Libre sensors via the LibreLinkUp caregiver cloud API (`pylibrelinkup`). 

This skill provides a **zero-cost, monitor-gated poller** that watches glucose telemetry in the background, suppresses routine stable readings to burn **$0.00 in LLM tokens**, and escalates dynamically across multiple communication tiers (text, WhatsApp voice call, smart home lighting) the instant an acute low or rapid drop occurs.

---

## ⚠️ Legal & Medical Disclaimers

> ### 1. NOT MEDICAL SOFTWARE
> This skill and its scripts are for **informational, experimental, and personal companioning research purposes only**. This software is **NOT a medical device**, has not been evaluated, cleared, or approved by the U.S. Food and Drug Administration (FDA) or any medical regulatory authority, and must **never replace professional medical monitoring, clinical diagnosis, or standard fingerstick blood glucose meters**. Never use this software as the sole or primary basis for insulin dosing, medication adjustments, or acute emergency treatment decisions.

> ### 2. NON-AFFILIATION & TRADEMARKS
> This tool is independent open-source software developed by the Nous Research community and is **NOT affiliated with, sponsored by, authorized by, or endorsed by Abbott Laboratories, FreeStyle Libre, or LibreView**. "FreeStyle Libre" and "LibreLinkUp" are registered trademarks of Abbott Laboratories.

---

## Core Philosophy & Design Disciplines

### 1. The Zero-Cost State Machine (Byte-Stable Hashing)
Querying an LLM every 5 to 15 minutes to read "blood sugar is normal" wastes thousands of tokens per hour. 
* This skill uses a lightweight Python poller (`scripts/glucose_watch.py`) running inside Hermes Cron's `monitor_script` facility.
* On every tick, the poller queries Abbott's cloud servers and outputs a single byte-stable line: `state=QUIET`.
* Hermes compares the SHA-256 hash of this output to the previous tick. If the hash hasn't changed, **the LLM agent execution is completely skipped ($0.00 cost)**.
* Only when glucose breaches a threshold or plummets rapidly does the poller emit `state=WARN_FALLING`, `state=ALERT_LOW`, or `state=ALERT_CRITICAL`—breaking the hash and waking the agent immediately to triage and alert.

### 2. The Inverted Overnight Asymmetry
Traditional medical alarm systems often trigger severe alarm fatigue by screaming at patients for elevated readings overnight.
* **An unattended high** overnight is metabolically unideal, but manageable and recoverable in the morning.
* **An unattended low** overnight is an acute life-threatening emergency within 30 to 45 minutes.
* Alerting on highs overnight causes patients to mute their phones, disable notifications, and sleep through fatal hypoglycemia. This skill enforces **overnight asymmetry: watch lows and rapid drops only**. Highs remain silent during sleep hours.

### 3. Failure Smoothing (No Flapping Alarms)
Transient Wi-Fi hiccups, cloud API latency, or sensor calibration gaps are collapsed to `state=QUIET` until a configurable number of consecutive failures occur (`error_after_fails`, default 3). A temporary connection blip will never wake you.

---

## Multi-Tier Alert Escalation Matrix

Users can customize how Hermes delivers alerts based on severity:

| Severity State | Trigger Condition | Recommended Channels | Agent Behavior |
|---|---|---|---|
| **Tier 1: `WARN_FALLING`** | Glucose ≤ 130 mg/dL AND Trend 1/2 (Rapid Fall) | Telegram / WhatsApp / Discord text | Proactive, gentle nudge: *"Dropping rapidly (Trend ↓). Grab a preventative snack before bed."* |
| **Tier 2: `ALERT_LOW`** | Glucose ≤ `low_threshold` (e.g. 85 mg/dL) | Telegram / Push notification + audio chime | Direct, actionable triage: *"Glucose at 82 mg/dL. Sit down first. Take 15g fast simple carbs now."* |
| **Tier 3: `ALERT_CRITICAL`** | Glucose ≤ `crit_threshold` (e.g. 70 mg/dL) | WhatsApp Voice Call + Smart Lights (Red) + Secondary Caregiver | Urgent awakening protocol: Places an active voice call to ring the phone, triggers smart lighting, and alerts emergency contact if unacknowledged in 5m. |

---

## 🤖 Automated Setup (Paste to Your Hermes Agent)

The easiest way to install and configure this skill is to let your Hermes Agent act as your setup wizard. Copy and paste this prompt into your Hermes chat:

```text
Please install and set up the librelinkup-monitor skill for me:
1. Ensure `pylibrelinkup` is installed in my Python environment (`pip install pylibrelinkup`).
2. Guide me through setting up my secondary caregiver LibreLinkUp credentials:
   - Ask for my secondary caregiver email and password (remind me not to use my primary patient account, and that the caregiver account must be registered as age 18+).
   - Confirm my preferred alert thresholds (defaults: soft low 85 mg/dL, critical low 70 mg/dL, rapid drop ceiling 130 mg/dL).
   - Save the configuration securely to my local path (e.g. ~/.config/librelinkup/creds.json or %LOCALAPPDATA%\hermes\libre_creds.json) without echoing secrets to chat.
3. Run `python scripts/glucose_watch.py --test` to verify that the boundary test suite passes (9/9).
4. Run `python scripts/glucose_watch.py --test-auth` to verify live authentication with the LibreLinkUp cloud.
5. Schedule the 15-minute Hermes monitor cron job using the specification in `templates/cron_job.example.json`.
```

---

## Step-by-Step Setup from Zero (Manual)

### Step 1: Create a Secondary Caregiver Account
> **NEVER use the patient's primary FreeStyle Libre login.** Querying the API with primary credentials can invalidate Bluetooth scanning sessions on the patient's mobile phone.
1. In the primary patient's **FreeStyle Libre** mobile app, navigate to:  
   `Menu → Connected Apps → LibreLinkUp → Add Connection`.
2. Enter a secondary email address dedicated to your companion agent (e.g. `caregiver@example.com`).
3. Check the caregiver email inbox, accept the invitation, and set a password (≥12 characters).
4. *Age Gate Requirement:* When registering the caregiver account, ensure the birth year indicates an age of 18+ (Abbott rejects caregiver registrations for minors).

### Step 2: Install Python Client
Ensure `pylibrelinkup` is installed in your Hermes Python environment:
```bash
python -m pip install pylibrelinkup
```

### Step 3: Configure Credentials & Thresholds
Create `libre_creds.json` in your Hermes home directory (e.g. `~/.config/librelinkup/creds.json` or `%LOCALAPPDATA%\hermes\libre_creds.json`):

```json
{
  "email": "caregiver@example.com",
  "password": "CaregiverPassword123!",
  "low_threshold": 85.0,
  "crit_threshold": 70.0,
  "fall_threshold": 130.0,
  "watch_from_hour": 22,
  "watch_to_hour": 8,
  "error_after_fails": 3
}
```

#### Configuration Options:
* `low_threshold` (float, default `85.0`): Floor in mg/dL triggering `ALERT_LOW`.
* `crit_threshold` (float, default `70.0`): Floor in mg/dL triggering `ALERT_CRITICAL`.
* `fall_threshold` (float, default `130.0`): Ceiling below which rapid drops trigger `WARN_FALLING`.
* `watch_from_hour` & `watch_to_hour` (int 0-23, optional): Active monitoring window (e.g. 22 to 8 for overnight). Omit for 24/7 coverage.
* `error_after_fails` (int, default `3`): Number of consecutive poll failures required before emitting `state=ERROR`.

### Step 4: Verify Live Connection
Run the built-in authentication test:
```bash
python scripts/glucose_watch.py --test-auth
```
If successful, it prints your patient identifier and latest real-time reading without exposing credentials.

### Step 5: Schedule the Hermes Monitor Cron Job
Schedule the monitor via Hermes CLI or `cronjob_manage`:
```bash
hermes cron create \
  --name "Glucose Watch (LibreLinkUp 15m)" \
  --interval 15m \
  --monitor-script "scripts/glucose_watch.py" \
  --prompt "You were WOKEN because the glucose digest CHANGED. Re-pull numbers with pylibrelinkup. On LOW/CRITICAL: message immediately with value, trend, and fast sugar triage (sit down first). On QUIET: reply [SILENT]."
```

---

## Testing & Verification

Before relying on this monitor, run the synthetic test suite:
```bash
python scripts/glucose_watch.py --test
```
This evaluates 9 boundary conditions (stable, rising high, rapid fall, slow fall, soft low, critical hypoglycemia, and trend direction assertions) to verify that the state machine behaves deterministically across all states.

---

## Linked References

* **`references/api_reference.md`**: Full Abbott LibreLinkUp cloud REST endpoints, header requirements (`X-User-Agent`), and token structures.
* **`references/gotchas_and_failure_modes.md`**: Deep dive into trend enum inversion, nested JSON paths, sensor ceilings (400 mg/dL), and Android DND Sleep Mode re-arming traps.
* **`templates/libre_creds.example.json`**: Starter template for user credentials and threshold configuration.
* **`templates/cron_job.example.json`**: Starter Hermes cron job definition.
