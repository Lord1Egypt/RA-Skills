# LibreLinkUp Cloud API Reference

Technical reference for integrating with Abbott's FreeStyle Libre cloud infrastructure via the LibreLinkUp caregiver sharing service.

> **LEGAL & REGULATORY NOTICE:**  
> This specification is documented for educational, interoperability, and personal companioning research purposes only. This tool is not affiliated with, endorsed by, or sponsored by Abbott Laboratories. FreeStyle Libre and LibreLinkUp are registered trademarks of Abbott Laboratories. This is not medical advice or an approved medical device.

---

## 1. Architecture & Telemetry Pipeline

FreeStyle Libre sensors stream or scan glucose values to the patient's mobile app (FreeStyle Libre 2 or 3). The patient app synchronizes readings to Abbott's cloud backend (LibreView). The LibreLinkUp service enables authorized caregivers and followers to receive real-time readings and historical logs via cloud API without accessing or disrupting the primary patient account.

```
Patient Sensor (NFC/BLE) 
    → Patient Mobile App (FreeStyle Libre 2/3) 
    → Abbott Cloud (LibreView / api-us.libreview.io) 
    → Caregiver API (LibreLinkUp / lluapi.libreview.io) 
    → Autonomous Poller (pylibrelinkup / Hermes Cron)
```

---

## 2. Cloud Endpoints & Protocol

### Regional Routing & Discovery
- **Endpoint:** `GET https://api-us.libreview.io/llu/config/country?country=US`
- **Headers:**
  - `product`: `llu.android`
  - `version`: `5.0.0.0`
- **Returns:** Regional server routing table, terms of service URLs, minimum caregiver age (18 for US), and password requirements.

### Email Verification Token Redemption (Automated Signup Verification)
When a new caregiver account registers, Abbott emails a verification link containing a `tokenID`. The verification can be redeemed headlessly:
- **Endpoint:** `PUT https://lluapi.libreview.io/v1/verifications/email`
- **Headers:**
  - `Content-Type`: `application/json`
  - `X-User-Agent`: `<app>;<appVersion>;<osType>;<osVersion>` (e.g. `llu;5.0.0.0;Android;14`)
    *CRITICAL:* The `X-User-Agent` header is mandatory and must follow this 4-element semi-colon format. Missing or standard browser user agents trigger HTTP 400 `{"code":1,"errors":[{"error":"invalid user agent format","key":"X-User-Agent"}]}`.
- **Body:**
  ```json
  {
    "tokenID": "<tokenID>"
  }
  ```

### Caregiver Authentication & Token Issuance
- **Endpoint:** `POST https://api-us.libreview.io/llu/auth/login`
- **Headers:**
  - `Content-Type`: `application/json`
  - `product`: `llu.android`
  - `version`: `5.0.0.0`
- **Body:**
  ```json
  {
    "email": "caregiver@example.com",
    "password": "<password>"
  }
  ```
- **Response:**
  - `data.authTicket.token`: Bearer JWT token required for subsequent API requests.
  - `data.user.id`: User ID, which is SHA-256 hashed and passed in the `account-id` header for authenticated patient requests.

---

## 3. Python Client Implementation (`pylibrelinkup`)

Install the client:
```bash
python -m pip install pylibrelinkup
```

### Basic Authentication & Telemetry Read
```python
import json
from pylibrelinkup import PyLibreLinkUp

with open("libre_creds.json", "r", encoding="utf-8") as f:
    creds = json.load(f)

client = PyLibreLinkUp(email=creds["email"], password=creds["password"])
client.authenticate()

# get_patients() returns a list of Pydantic Patient objects
patients = client.get_patients()
if not patients:
    raise RuntimeError("No connected patients found. Has the sharing invitation been accepted?")

patient_id = patients[0].patient_id

# 1. Real-time glucose reading
latest = client.latest(patient_id)
print(f"Glucose: {latest.value} mg/dL | Trend: {latest.trend} | Timestamp: {latest.timestamp}")

# 2. 12-hour historical trajectory graph (~141 readings at 5-minute intervals)
history = client.graph(patient_id)
# history is a list of entries with .timestamp, .value_in_mg_per_dl, .is_high, .is_low
```

---

## 4. Trend Velocity Mapping
The LibreLinkUp API maps trend arrows to the following integer values:

| Enum Value | Identifier | Rate of Change | Clinical Meaning |
|---|---|---|---|
| `0` | `UNKNOWN` | N/A | Sensor warming up, calibrating, or signal gap |
| `1` | `DOWN_FAST` | > 2.0 mg/dL per min | Rapidly dropping (urgent intervention priority) |
| `2` | `DOWN_SLOW` | 1.0 – 2.0 mg/dL per min | Falling steadily |
| `3` | `STABLE` | < 1.0 mg/dL per min | Flat, stable trajectory |
| `4` | `UP_SLOW` | 1.0 – 2.0 mg/dL per min | Rising steadily |
| `5` | `UP_FAST` | > 2.0 mg/dL per min | Rapidly rising |

> **WARNING:** Many community implementations mistakenly assume `4` and `5` represent falling values. In Abbott's cloud specification, `1` and `2` are the only falling states.
