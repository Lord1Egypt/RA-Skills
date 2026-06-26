---
name: parcel-tracker
description: Erkennt automatisch den Paketdienst (DHL, Hermes, UPS, GLS, Amazon etc.) via Track123-API und ruft Tracking-Informationen ab. Optional PLZ für erweiterte Infos.
version: 1.1.0
---

metadata:
  openclaw:
    emoji: "📦"
    bins: ["python3"]
    env:
      - name: TRACK123_API_SECRET
        required: true
        description: Track123 API-Secret (aus deinem Account: Developer > Webhook/API).[web:34]
      - name: TRACK123_API_BASE
        required: false
        default: "https://api.track123.com/gateway/open-api/tk/v2"
        description: Track123 API-Base-URL.
    os: ["linux", "darwin"]

triggers:
  - match: regex
    pattern: "(?i)(tracke|verfolge|status) (mein|eine|ein|dieses)? paket"
  - match: regex
    pattern: "(?i)(sendungsverfolgung|sendungsstatus|tracking status)"

commands:
  - name: track
    description: Holt Tracking-Status via Track123 (auto-detect Carrier).
    args:
      - name: tracking_number
        type: string
        required: true
      - name: postal_code
        type: string
        required: false
    run:
      bin: python3
      script: track.py
      cwd: "."
      timeout: 30

usage:
  examples:
    - "Tracke Paket 00340434161234567890, PLZ 73614."
    - "Sendungsstatus für 1Z9999W99999999999."
