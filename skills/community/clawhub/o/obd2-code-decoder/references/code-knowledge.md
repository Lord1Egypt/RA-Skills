# OBD2 Code Decoder — Reference

## 1. Code architecture

```
P 0 3 0 1
│ │ │ └┴─ specific fault number
│ │ └───── subsystem digit
│ └─────── 0 = SAE generic, 1 = manufacturer-specific, 2 = both,
│          3 = reserved (hybrid common)
└───────── P powertrain, B body, C chassis, U network/communication
```

P0xxx and P2xxx are generic (same meaning on every car). P1xxx is
manufacturer-specific. B/C/U codes are heavily manufacturer-specific — the
decoder flags them with the honest fallback instead of inventing meanings.

## 2. Severity ladder

| Verdict | Meaning | Action |
|---|---|---|
| STOP-DRIVING | Active risk of damage or danger | Park it / tow; do not "limp it" far |
| FIX-SOON (days) | Progressive damage or efficiency loss | Drive gently, book shop this week |
| MONITOR | Informational or early warning | Watch for repeat, check cheap causes |

Flashing check-engine light ALWAYS overrides: it marks active misfire dumping
raw fuel into the catalyst (cat overheats and can start a fire).

## 3. The pattern engine (the part that saves money)

Multi-code sets usually share one root cause:

| Pattern | Root cause | Fix-first |
|---|---|---|
| P0171 + P0174 | Both banks lean → vacuum leak, dirty MAF, low fuel pressure | ONE intake-side fix, not two O2 sensors |
| P0172 + P0175 | Both banks rich → leaky injector, high fuel pressure, bad MAF over-reporting | Fuel delivery side |
| P030x + P0171/74 | Lean misfire | Mixture first, plugs second |
| P0300 + P0420/P0430 | Misfire damaged cat / cat code is a SYMPTOM | Misfire first or new cat dies too |
| P0420 + P0430 | Both cats "inefficient" → common cause: exhaust leak upstream, rear O2, or an engine running wrong | Exhaust leak check first |
| P0440/P0442/P0455 family | Evap leak — loose gas cap is the #1 real cause | Re-tighten cap, re-scan after 3 trips |
| P0128 + low MPG | Thermostat stuck open | Thermostat ($20–80 DIY-easy) |
| Multiple U-codes | Bus/network issue, often battery/ground corrosion | Check 12V health and grounds first |

## 4. Cost-band doctrine

Any estimate is a RANGE. Generic bands used (US, independent shop, 2020s):

- $0–25: gas cap, vacuum hose, MAF cleaning, fuse, loose connector
- $25–150: sensors (O2, ECT, MAF replacement), thermostat, PCV valve, coils
  (1 cyl), purge valve
- $150–600: catalytic converter (aftermarket, 1 unit, incl. welding) at the
  LOW end; ignition set (plugs+coils all cylinders), injectors, EGR valve
- $300–2,400: OEM cat, timing components, transmission solenoids, intake
  gasket labor

A code never mandates the top of its band. The decoder always lists cheap
mimics first ("exhaust leak sounds exactly like P0420").

## 5. Clearing codes — the rules

- Clear AFTER the fix, to confirm the fault stays away (if it returns within
  a week, the fix was a mimic).
- Clearing resets readiness monitors: typically 50–100 miles of mixed driving
  before an emissions test will even run.
- Clearing to mask a fault before a sale or test is fraud in most
  jurisdictions and the code usually returns in days.
- "Pending" (single-sighting) codes clear themselves after 3 good trips;
  confirmed codes need 40 warm-up cycles without the fault.

## 6. Live-data PID quick math (mode 01)

For dongle apps showing raw/live values:

- STFT + LTFT combined beyond ±10% → mixture problem is REAL (confirming
  P0171/72); +25% both = serious lean.
- MAF at idle (g/s) ≈ engine displacement in litres (2.0 L ≈ 2–4 g/s idle,
  ~80–100 g/s at WOT per 2 L). Way low + lean codes = dirty MAF.
- O2 sensor should oscillate 0.1–0.9 V ~1–2 times/sec at 2500 rpm; stuck
  low = lean reality, stuck mid = dead sensor.
- Coolant must reach 88–95 °C; P0128 with 70 °C running temp = thermostat.

## 7. Safety notes

Never work under a car on the factory jack. Cat replacement = 4+ hours
soak-cool (500 °C surfaces). Fuel-system work (P0087/P0088) releases
pressurized fuel — relieve pressure per service manual first.
