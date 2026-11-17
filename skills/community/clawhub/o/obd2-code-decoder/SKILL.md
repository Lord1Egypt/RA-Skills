---
name: obd2-code-decoder
description: Use when a check-engine light is on, an OBD2 scan returns P0xxx/P2xxx/B/C/U codes, or you need to know if the car is safe to drive, what the code means in plain language, likely causes with fix cost bands, and DIY difficulty. Decodes 70+ generic codes, detects multi-code patterns (lean-both-banks, misfire+catalyst chains), and gives a STOP-DRIVING / SOON / MONITOR verdict per code.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [car, obd2, check-engine, dtc, diagnostics, automotive]
---

# OBD2 Code Decoder

## Overview

A check-engine light turns a $15 Bluetooth OBD2 dongle into a panic machine:
you get "P0420" and Google gives you 40 possible causes from "loose gas cap"
to "$2,400 catalytic converter". `scripts/obd2_decoder.py` converts codes into
plain-language meaning, a safety verdict (STOP-DRIVING / FIX-SOON / MONITOR),
ranked likely causes with realistic fix cost bands, DIY difficulty, and — the
part Google never gives you — **multi-code pattern detection** that collapses
several scary codes into one root cause.

## When to Use

- Check-engine light is on (steady or flashing) and you have scanned codes.
- Buying/selling a used car and want to interpret the scan report.
- A code returned after a repair — is it the same fault or a new one?
- Deciding: drive to work tomorrow, drive to the shop, or tow it?

**Don't use for:** airbag/SRS crash data (B-code module dumps need
manufacturer tools), hybrid/EV high-voltage faults, or anything involving the
flashing light + burning smell + gauge-in-red combination — that is a
shut-down-now situation regardless of codes.

## How It Works

1. **Decode** each code against a 70+ entry generic-Powertrain database:
   plain-language meaning, system (fuel/air/ignition/emissions/sensor/
   transmission), severity.
2. **Pattern engine**: known code COMBINATIONS that have a single root cause —
    - P0171 + P0174 (both banks lean) → vacuum leak / dirty MAF, not two O2
      sensors
    - P0300..P0308 with P0171/P0174 → lean misfire; fix the lean condition
    - Misfire codes + P0420/P0430 → unburned fuel killed the cat; fix
      misfire FIRST or the new cat dies too
    - P0440-family together → evaporative system (often just a loose gas cap)
3. **Verdict** per code and for the whole set: worst severity wins, with the
   one-line reason. Flashing-CEI rule is always stated: flashing = active
   misfire dumping raw fuel = park it.
4. **Cost bands & DIY** per typical fix: e.g. P0420 — check exhaust leaks and
   rear O2 sensor ($20–150) before condemning the cat ($300–2,400); P0455 —
   try the gas cap ($0) before a smoke test ($80–150).
5. **Clearing rules**: when clearing is safe (after fixing), when it's illegal
   (emissions test fraud / masking an unfixed fault), and the drive-cycle note
   (monitors reset; codes often return within days if unfixed).

## Using the Script

```bash
# Decode a set of codes (the realistic case)
python3 scripts/obd2_decoder.py P0171 P0174

# Single code, full detail
python3 scripts/obd2_decoder.py P0420

# Verdict-only quick check
python3 scripts/obd2_decoder.py --short P0300

# List codes in one system, e.g. all evap codes we know
python3 scripts/obd2_decoder.py --list-system evap
```

## Worked Example

Input `P0171 P0174 P0300` outputs: both-banks-lean pattern detected → most
likely vacuum leak or dirty MAF sensor (one cause, three codes), fix-first
order = lean condition before plugs/coils, verdict FIX-SOON (safe to drive
gently; long-term risk is catalytic converter damage), cost bands
$0–20 (MAF clean), $20–80 (vacuum hoses), $150+ (intake gasket).

## Common Pitfalls

1. **Replacing the sensor the code names.** O2 sensor codes are usually the
   sensor REPORTING a real mixture problem, not a broken sensor.
2. **Clearing codes to pass inspection.** Readiness monitors reset to
   "incomplete"; most inspection regimes reject a car with incomplete
   monitors, and the underlying fault returns.
3. **Treating P0420 as an automatic cat replacement.** Exhaust leaks, rear
   O2 sensors, and misfires all mimic it — the cheap causes first.
4. **One code = one problem.** The pattern engine exists because three codes
   are often ONE $15 vacuum hose.
5. **Driving on a flashing CEL.** Steady = diagnose soon; flashing = active
   misfire destroying the catalyst — stop driving.
6. **Pending vs confirmed.** A pending code (seen once) is information; a
   confirmed/stored code with the light on is a decision.

## Verification Checklist

- [ ] Every input code got a decode or an explicit "manufacturer-specific —
      look up for your make" fallback, never silence.
- [ ] Pattern matches are shown BEFORE individual codes (root cause first).
- [ ] Whole-set verdict = worst severity among codes, with reason.
- [ ] Cost bands are ranges, never single promises.
- [ ] Clearing-rules block present when any emissions-related code appears.
