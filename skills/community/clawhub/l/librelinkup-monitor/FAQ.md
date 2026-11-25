# LibreLinkUp Monitor: User Guide, FAQ & Legal Indemnification

A comprehensive operational manual and legal framework for the `librelinkup-monitor` autonomous continuous glucose monitoring skill.

---

## ⚖️ Mandatory Legal Terms, Medical Disclaimer & Indemnification Agreement

### 1. NOT MEDICAL SOFTWARE OR A MEDICAL DEVICE
**THIS SOFTWARE IS FOR INFORMATIONAL, EXPERIMENTAL, AND EDUCATIONAL PURPOSES ONLY.**  
`librelinkup-monitor` is not a medical device, is not diagnostic software, and has not been tested, evaluated, approved, or certified by the United States Food and Drug Administration (FDA), the European Medicines Agency (EMA), or any other regulatory authority. 

Continuous glucose monitoring (CGM) sensors measure **interstitial fluid glucose**, which inherently lags capillary blood glucose by 5 to 15 minutes and is subject to compression artifacts, calibration drift, sensor detachment, and communication interruptions. 

**DO NOT RELY ON THIS SOFTWARE AS A PRIMARY OR SOLE BASIS FOR INSULIN DOSING, MEDICATION ADJUSTMENTS, OR ACUTE MEDICAL DECISIONS.**  
Always verify any anomalous, low, or high reading with an independent, calibrated fingerstick blood glucose meter before administering carbohydrates, fast sugars, or corrective insulin.

### 2. NON-AFFILIATION & TRADEMARK DISCLAIMER
This software is an independent open-source contribution developed by the Nous Research community and Syzygy Studios. It is **not affiliated with, associated with, authorized by, endorsed by, or in any way officially connected with Abbott Laboratories, FreeStyle Libre, LibreView, or any of their subsidiaries or affiliates**. The official Abbott FreeStyle Libre website is located at `https://www.freestyle.abbott`.

The names "FreeStyle", "FreeStyle Libre", "LibreLinkUp", and "LibreView", as well as related names, marks, emblems, and images, are registered trademarks of their respective owners.

### 3. ASSUMPTION OF RISK & INDEMNIFICATION (HOLD HARMLESS)
**BY INSTALLING, RUNNING, OR RELYING UPON THIS SOFTWARE, YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT YOU DO SO ENTIRELY AT YOUR OWN RISK.**

To the maximum extent permitted by applicable law, the authors, maintainers, contributors, and copyright holders of this repository (including Nous Research, Syzygy Studios, and individual developers) **DISCLAIM ALL WARRANTIES OF ANY KIND, WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OPERATIONAL AVAILABILITY, ACCURACY, AND NON-INFRINGEMENT.**

**IN NO EVENT SHALL THE AUTHORS, MAINTAINERS, OR AFFILIATES BE LIABLE FOR ANY CLAIM, DAMAGES, LOSSES, INJURIES, HOSPITALIZATIONS, ADVERSE HEALTH EVENTS, OR LIABILITIES**, WHETHER IN AN ACTION OF CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE, THE USE OF THE SOFTWARE, DELAYED NOTIFICATIONS, FAILED NETWORK REQUESTS, THIRD-PARTY CLOUD OUTAGES, MISINTERPRETED TELEMETRY, OR INACCURATE ALERTS.

**YOU AGREE TO DEFEND, INDEMNIFY, AND HOLD HARMLESS** the authors and distributors against any claims, liabilities, damages, judgments, awards, losses, costs, or legal fees arising out of your deployment, modification, or reliance on this tool.

---

## 📖 Frequently Asked Questions (FAQ)

### Architecture & Account Questions

#### Q: Can I use my main FreeStyle Libre login email and password?
**NO. Never use the patient's primary FreeStyle Libre account credentials.**  
Querying the cloud API using the primary patient account can invalidate active Bluetooth sessions on the patient's mobile scanner or phone, causing communication interruptions with the physical sensor.  
Instead, invite a **secondary caregiver email address** via the *Connected Apps* menu in the FreeStyle Libre mobile app. The poller logs into the LibreLinkUp caregiver endpoint, preserving the patient's local Bluetooth link intact.

#### Q: How do I set up the secondary caregiver account?
1. Open your **FreeStyle Libre** app on your phone.
2. Tap the menu (hamburger icon) → **Connected Apps** → **LibreLinkUp**.
3. Tap **Add Connection** (or invite follower).
4. Enter a secondary email address dedicated to your assistant (e.g. an address you control).
5. Open the invitation email, accept the share, and complete registration with a strong password (≥12 characters).
6. **Age Gate Requirement:** When registering, ensure the caregiver birth year indicates an age of 18 or older. Abbott's API strictly rejects caregiver registrations for accounts under 18 years old.

#### Q: Does this connect directly to my sensor via Bluetooth Low Energy (BLE)?
No. This skill connects to Abbott's cloud service (`lluapi.libreview.io`). Your physical FreeStyle Libre sensor communicates with your smartphone via NFC/BLE, your smartphone synchronizes readings to Abbott's LibreView cloud, and this script polls the authorized cloud endpoint.

---

### Alerting & Reliability Questions

#### Q: Why does this monitor alert on LOWS and RAPID DROPS, but remain quiet on HIGHS overnight?
This is the core clinical safety design of the skill: **Inverted Overnight Asymmetry**.
* An unattended low overnight is an acute medical crisis that can cause seizure, unconsciousness, or worse within 30 to 45 minutes.
* An elevated glucose reading (high) overnight is metabolically undesirable, but manageable and recoverable the next day.
* If an automated monitor wakes a sleeping patient every 20 minutes for an elevated reading of 190 mg/dL, the patient inevitably develops **alarm fatigue**, mutes their phone, or disables the monitor entirely—leaving them completely unprotected against a catastrophic 50 mg/dL plummet.
* This monitor guards the dangerous edge: it alerts urgently on lows and rapid drops, keeping routine overnight highs silent.

#### Q: What if my home Wi-Fi drops or Abbott's cloud has a 30-second glitch? Will it wake me up with an error alarm?
No. The script features **failure smoothing** (`error_after_fails`, default 3). Transient network drops, brief API timeouts, or temporary sensor warmup states collapse to `state=QUIET`. The system will only emit `state=ERROR` if it experiences 3 consecutive failed polls (e.g., 30–45 minutes of complete telemetry blackout).

#### Q: How do I prevent Android or iPhone Do Not Disturb (DND) from silencing alarms?
On Android (especially Samsung devices), scheduled **Sleep Modes** in *Settings → Modes and Routines* will re-arm DND every evening, silently overriding standard app notification exceptions.
* **The Fix:** Go to `Settings → Modes and Routines → Sleep → Do Not Disturb → Allow Exceptions → Apps` and add your notification channel (Telegram/WhatsApp) explicitly to the active Sleep Mode.
* Ensure battery optimization is set to **Unrestricted** for your communication app so the OS background process is not killed during deep sleep.

---

### Configuration & Customization Questions

#### Q: How often does the monitor check my numbers?
The check frequency is governed by your Hermes cron schedule. Common cadences:
* `--interval 15m`: Standard cadence matching sensor cloud upload rhythms.
* `--interval 10m`: Recommended for tighter monitoring during active insulin therapy.
* `--interval 5m`: High-frequency polling.

#### Q: How do I change my alert thresholds?
You can customize thresholds directly in `libre_creds.json`:
```json
{
  "email": "caregiver@example.com",
  "password": "YourPassword123!",
  "low_threshold": 80.0,
  "crit_threshold": 65.0,
  "fall_threshold": 120.0,
  "watch_from_hour": 22,
  "watch_to_hour": 8,
  "error_after_fails": 3
}
```
* `low_threshold`: Soft low alert floor (default 85 mg/dL).
* `crit_threshold`: Critical hypoglycemia alert floor (default 70 mg/dL).
* `fall_threshold`: Ceiling below which rapid drop arrows (Trend 1 or 2) trigger a warning.
* `watch_from_hour` / `watch_to_hour`: Active window (e.g. 22 to 8 for 10 PM to 8 AM). Omit for 24/7 watch.

#### Q: How do I verify that the alerts actually work without dropping my blood sugar?
Run the built-in synthetic test harness:
```bash
python scripts/glucose_watch.py --test
```
This tests all 9 boundary conditions (stable, rising, rapid drop, soft low, critical hypoglycemia, and trend direction assertions) to prove that the state machine triggers correctly.
