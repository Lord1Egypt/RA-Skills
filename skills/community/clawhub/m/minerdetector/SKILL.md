---
name: MinerDetector
description: Charge 0.01 USDT to export 4 bundled miner signature libraries. No scanning or detection.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - MINERDETECTOR_API_KEY
      anyBins:
        - python3
        - python
        - py
    primaryEnv: MINERDETECTOR_API_KEY
    skillKey: minerdetector
    emoji: "🧩"
    homepage: https://x.com/MaZhenZi1/status/2034654798906269916
    os:
      - linux
      - macos
      - windows
---
# MinerDetector

MinerDetector is a **cross-platform billing-and-export skill**.

It does **not** scan disks, processes, networks, firewalls, Defender, or OpenClaw skills.
It does **not** delete, quarantine, or modify files.
It only does three things:

1. Check SkillPay balance.
2. Generate a payment link when the balance is low.
3. Charge **0.01 USDT** and export the **4 bundled text libraries** below.

Bundled libraries:

- `indicators/mining_pool_websites.txt`
- `indicators/mining_software_filenames.txt`
- `indicators/mining_pool_public_ips.txt`
- `indicators/mining_pool_ports.txt`

Use this skill when the user wants to **get or refresh the 4 signature libraries**. After export, OpenClaw or the user's own local tooling can compare those files against local data. That comparison step is outside this skill.

## Required setup

The user must apply for a billing API key here:

`https://x.com/MaZhenZi1/status/2034654798906269916`

Then export the key for the current terminal/session:

### Linux / macOS

```bash
export MINERDETECTOR_API_KEY="your_api_key_here"
```

### Windows PowerShell

```powershell
$env:MINERDETECTOR_API_KEY = "your_api_key_here"
```

## Commands

### 1) Check balance

```bash
python3 {baseDir}/scripts/miner_detector.py balance --user-id YOUR_USER_ID
```

If `python3` is unavailable, try:

```bash
python {baseDir}/scripts/miner_detector.py balance --user-id YOUR_USER_ID
```

or on Windows:

```powershell
py -3 {baseDir}/scripts/miner_detector.py balance --user-id YOUR_USER_ID
```

### 2) Generate a payment link

```bash
python3 {baseDir}/scripts/miner_detector.py payment-link --user-id YOUR_USER_ID --amount 5
```

### 3) Charge 0.01 USDT and export the 4 files to a folder

```bash
python3 {baseDir}/scripts/miner_detector.py fetch --user-id YOUR_USER_ID --output-dir ./minerdetector-libs
```

### 4) Charge 0.01 USDT and return the 4 files as JSON

```bash
python3 {baseDir}/scripts/miner_detector.py fetch --user-id YOUR_USER_ID --json-only
```

## Agent behavior

- When the user asks to **update**, **refresh**, **download**, or **get** the miner signature libraries, run `fetch`.
- When the user asks to **check balance**, run `balance`.
- When the user asks to **recharge**, **top up**, or **get a payment link**, run `payment-link`.
- When the user asks this skill to scan their computer, be explicit: **this skill does not scan**. Export the 4 libraries and tell the user to let OpenClaw or their own local workflow do the comparison.
- Keep responses factual. Do not claim that scanning or remediation was performed.

## API summary

Skill ID:

`82c878f5-1b74-4ee3-a32a-eeb878309ba5`

Billing endpoints used by the script:

- `GET /api/v1/billing/balance?user_id=xxx`
- `POST /api/v1/billing/charge`
- `POST /api/v1/billing/payment-link`

Default billing host:

`https://skillpay.me`

## Notes

- This package is text-only and publish-friendly.
- No hardcoded billing secret is included.
- The billing API key is provided by the user at runtime through `MINERDETECTOR_API_KEY`.
- The 4 bundled libraries are the files included under `indicators/`.
