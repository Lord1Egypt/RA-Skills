#!/usr/bin/env python3
"""
OBD2 Code Decoder — plain-language DTC meanings, safety verdicts,
multi-code pattern detection, cost bands, DIY difficulty.

Usage:
  obd2_decoder.py P0171 P0174
  obd2_decoder.py --short P0300
  obd2_decoder.py --list-system evap
"""
import argparse
import re
import sys

# severity: 3=STOP-DRIVING, 2=FIX-SOON, 1=MONITOR
CODES = {
    # --- fuel/air mixture ---
    "P0171": ("System too lean, bank 1", "fuel", 2,
              [("vacuum leak (intake hose, brake booster, PCV)", "$0-80", "easy"),
               ("dirty MAF sensor", "$10-20 (cleaner)", "easy"),
               ("weak fuel pump / clogged filter", "$80-400", "medium"),
               ("bad O2 sensor (LESS likely than the above)", "$50-150", "medium")]),
    "P0174": ("System too lean, bank 2", "fuel", 2,
              [("same causes as P0171 — bank 2 confirms ONE shared cause", "$0-80", "easy")]),
    "P0172": ("System too rich, bank 1", "fuel", 2,
              [("leaking fuel injector", "$60-300", "hard"),
               ("high fuel pressure / bad regulator", "$50-250", "medium"),
               ("MAF over-reporting (dirty or dying)", "$10-150", "easy"),
               ("bad O2 sensor", "$50-150", "medium")]),
    "P0175": ("System too rich, bank 2", "fuel", 2,
              [("same causes as P0172", "$50-300", "medium")]),
    # --- ignition/misfire ---
    "P0300": ("Random/multiple cylinder misfire", "ignition", 3,
              [("see pattern: with lean codes, fix mixture FIRST", "$0-80", "easy"),
               ("worn spark plugs (60-100k mi)", "$40-160 set", "easy"),
               ("ignition coil (1 cylinder)", "$40-150", "easy"),
               ("vacuum leak leaning mixture", "$0-80", "easy")]),
    "P0301": ("Cylinder 1 misfire", "ignition", 3,
              [("coil or plug on cyl 1 (swap with cyl 2, see if code moves)", "$20-120", "easy"),
               ("injector cyl 1", "$60-250", "hard"),
               ("low compression cyl 1 (worst case)", "$300-2500", "shop")]),
    "P0302": ("Cylinder 2 misfire", "ignition", 3,
              [("coil/plug cyl 2 — swap test", "$20-120", "easy")]),
    "P0303": ("Cylinder 3 misfire", "ignition", 3,
              [("coil/plug cyl 3 — swap test", "$20-120", "easy")]),
    "P0304": ("Cylinder 4 misfire", "ignition", 3,
              [("coil/plug cyl 4 — swap test", "$20-120", "easy")]),
    "P0305": ("Cylinder 5 misfire", "ignition", 3,
              [("coil/plug cyl 5 — swap test", "$20-120", "easy")]),
    "P0306": ("Cylinder 6 misfire", "ignition", 3,
              [("coil/plug cyl 6 — swap test", "$20-120", "easy")]),
    # --- catalyst ---
    "P0420": ("Catalyst efficiency below threshold, bank 1", "emissions", 1,
              [("exhaust leak upstream of rear O2 (sounds like a bad cat)", "$0-150", "easy"),
               ("rear O2 sensor lazy", "$50-150", "medium"),
               ("ENGINE running wrong (misfire/lean/rich) killing cat — fix that first", "$0-300", "varies"),
               ("catalytic converter genuinely dead", "$300-2400", "shop")]),
    "P0430": ("Catalyst efficiency below threshold, bank 2", "emissions", 1,
              [("same logic as P0420", "$0-2400", "varies")]),
    # --- evap ---
    "P0440": ("Evaporative emission system malfunction", "emissions", 1,
              [("loose/worn gas cap", "$0-25", "trivial"),
               ("cracked evap hose", "$10-60", "easy"),
               ("purge valve stuck", "$30-120", "easy"),
               ("vent valve / charcoal canister", "$50-400", "medium")]),
    "P0442": ("Evap small leak (0.040 in)", "emissions", 1,
              [("gas cap seal", "$0-25", "trivial"),
               ("small hose crack — smoke test finds it", "$80-150 test", "shop"),
               ("purge/vent solenoid", "$30-120", "easy")]),
    "P0455": ("Evap large leak (gross)", "emissions", 1,
              [("gas cap loose or missing (#1 cause)", "$0-25", "trivial"),
               ("disconnected evap hose", "$0-60", "easy"),
               ("bad purge valve", "$30-120", "easy")]),
    "P0456": ("Evap very small leak", "emissions", 1,
              [("gas cap", "$0-25", "trivial"),
               ("smoke test to find pinhole", "$80-150", "shop")]),
    # --- EGR ---
    "P0401": ("EGR insufficient flow", "emissions", 1,
              [("clogged EGR ports/valve (carbon)", "$20-250", "medium"),
               ("EGR valve failed", "$80-350", "medium"),
               ("DPFE sensor", "$30-90", "easy")]),
    "P0402": ("EGR excessive flow", "emissions", 1,
              [("EGR valve stuck open", "$80-350", "medium")]),
    # --- sensors ---
    "P0101": ("MAF sensor range/performance", "sensor", 2,
              [("dirty MAF (clean with MAF cleaner ONLY)", "$10", "easy"),
               ("intake leak after MAF", "$0-80", "easy"),
               ("dead MAF", "$80-300", "easy")]),
    "P0102": ("MAF circuit low", "sensor", 2,
              [("wiring/connector", "$0-60", "easy"), ("dead MAF", "$80-300", "easy")]),
    "P0103": ("MAF circuit high", "sensor", 2,
              [("wiring short", "$0-60", "easy"), ("dead MAF", "$80-300", "easy")]),
    "P0113": ("IAT sensor circuit high", "sensor", 1,
              [("wiring/connector", "$0-60", "easy"), ("IAT sensor", "$15-60", "easy")]),
    "P0128": ("Coolant below thermostat regulating temp", "sensor", 1,
              [("thermostat stuck open (classic)", "$20-80", "medium"),
               ("coolant LOW (check level first)", "$0-30", "trivial"),
               ("ECT sensor lying", "$15-60", "easy")]),
    "P0121": ("TPS circuit range/performance", "sensor", 2,
              [("TPS sensor", "$30-120", "easy"), ("wiring/connector", "$0-60", "easy")]),
    "P0131": ("O2 sensor low voltage, bank 1 sensor 1", "sensor", 2,
              [("REAL lean condition (vacuum leak)", "$0-80", "easy"),
               ("wiring/exhaust leak near sensor", "$0-100", "easy"),
               ("dead O2 sensor", "$50-150", "medium")]),
    "P0133": ("O2 slow response, B1S1", "sensor", 2,
              [("aging O2 sensor", "$50-150", "medium"),
               ("small exhaust leak", "$0-150", "easy")]),
    "P0135": ("O2 heater, B1S1", "sensor", 1,
              [("heater circuit fuse/relay", "$5-30", "easy"),
               ("O2 sensor heater element", "$50-150", "medium")]),
    "P0141": ("O2 heater, B1S2 (rear)", "sensor", 1,
              [("O2 sensor heater", "$50-150", "medium")]),
    "P0134": ("O2 no activity, B1S1", "sensor", 2,
              [("dead O2 sensor", "$50-150", "medium")]),
    "P0221": ("TPS B circuit range", "sensor", 2,
              [("TPS / pedal sensor", "$40-200", "medium")]),
    # --- fuel system ---
    "P0087": ("Fuel rail pressure too low", "fuel", 3,
              [("clogged fuel filter", "$20-80", "easy"),
               ("weak fuel pump", "$200-800", "hard"),
               ("fuel pressure regulator", "$50-250", "medium"),
               ("PRESSURIZED SYSTEM — relieve pressure before working", "-", "shop")]),
    "P0088": ("Fuel rail pressure too high", "fuel", 3,
              [("stuck regulator", "$50-250", "medium"),
               ("PRESSURIZED SYSTEM — safety", "-", "shop")]),
    "P0191": ("Fuel rail pressure sensor range", "fuel", 2,
              [("FRP sensor", "$40-150", "medium")]),
    # --- transmission ---
    "P0700": ("Transmission control module fault (info code)", "trans", 2,
              [("this just POINTS at the TCM — read TCM sub-codes", "-", "shop"),
               ("low/atf fluid or valve body", "$150-900", "shop")]),
    "P0730": ("Incorrect gear ratio", "trans", 3,
              [("low fluid / worn clutches / valve body", "$150-3000", "shop")]),
    "P0741": ("Torque converter clutch stuck off", "trans", 2,
              [("valve body solenoid", "$200-700", "shop"),
               ("fluid + filter service first (cheap try)", "$120-250", "medium")]),
    "P0751": ("Shift solenoid A stuck", "trans", 2,
              [("solenoid + fluid", "$200-600", "shop")]),
    # --- charging/electrical ---
    "P0562": ("System voltage low", "electrical", 2,
              [("alternator/belt", "$100-600", "medium"),
               ("battery 5+ years old", "$120-250", "easy"),
               ("corroded grounds", "$0-40", "easy")]),
    "P0563": ("System voltage high", "electrical", 3,
              [("alternator regulator overcharging — WILL cook battery/ECU", "$100-600", "medium")]),
    # --- misc powertrain ---
    "P0011": ("Camshaft timing over-advanced, bank 1", "engine", 2,
              [("dirty oil (VVT solenoids hate it) — oil change first", "$50-100", "easy"),
               ("VVT solenoid", "$60-250", "medium"),
               ("timing chain stretch (worst)", "$500-2000", "shop")]),
    "P0016": ("Crank/cam position correlation", "engine", 3,
              [("stretched timing chain — stop driving, chain can jump", "$500-2000", "shop")]),
    "P0299": ("Turbo underboost", "engine", 2,
              [("charge-pipe/intercooler leak (listen for hiss)", "$20-200", "easy"),
               ("sticking wastegate/boost solenoid", "$50-300", "medium"),
               ("clogged VNT turbo (diesel)", "$300-1200", "shop")]),
    "P0300R": ("reserved", "ignition", 1, []),
    "P0327": ("Knock sensor circuit low", "sensor", 1,
              [("knock sensor / wiring (often no symptom)", "$40-200", "medium")]),
    "P0335": ("Crankshaft position sensor circuit", "sensor", 3,
              [("CKP sensor (car can stall and NOT restart)", "$40-180", "medium")]),
    "P0340": ("Camshaft position sensor circuit", "sensor", 2,
              [("CMP sensor", "$40-180", "easy")]),
    "P0500": ("Vehicle speed sensor", "sensor", 2,
              [("VSS sensor / wiring (ABS shares it)", "$30-200", "easy")]),
    "P0505": ("Idle air control malfunction", "fuel", 1,
              [("dirty throttle body (clean it)", "$10-25", "easy"),
               ("IAC valve", "$60-250", "easy")]),
    "P2096": ("Post-catalyst fuel trim lean, bank 1", "fuel", 1,
              [("small exhaust leak after cat", "$0-150", "easy"),
               ("rear O2 sensor", "$50-150", "medium")]),
    "P2187": ("Idle system too lean, bank 1", "fuel", 2,
              [("vacuum leak at idle (classic)", "$0-80", "easy")]),
    "P2195": ("O2 signal stuck lean, B1S1", "sensor", 2,
              [("real lean or dead sensor", "$0-150", "varies")]),
    "P2196": ("O2 signal stuck rich, B1S1", "sensor", 2,
              [("real rich or dead sensor", "$0-150", "varies")]),
    "U0100": ("Lost communication with ECM/PCM", "electrical", 2,
              [("battery/ground corrosion (check 12V health first)", "$0-40", "easy"),
               ("CAN bus wiring short/open", "$80-400", "hard"),
               ("ECM power relay", "$20-90", "medium")]),
}

PATTERNS = [
    ({"P0171", "P0174"}, "BOTH BANKS LEAN — one shared cause",
     "A single vacuum leak, dirty MAF, or weak fuel pump leans BOTH banks. "
     "Do NOT buy two O2 sensors. Fix intake/fuel side once, all three "
     "possible codes clear together."),
    ({"P0172", "P0175"}, "BOTH BANKS RICH — one shared cause",
     "Over-fueling (injector leak, regulator, MAF over-reporting) hits both "
     "banks together. Rich washes cylinders and kills cats — fix soon."),
    ({"P0300", "P0171"}, "LEAN MISFIRE chain",
     "The lean condition is causing the misfire. Fix mixture first (vacuum "
     "leak / MAF), then plugs if misfire persists. Ignoring it overheats "
     "the catalyst."),
    ({"P0300", "P0174"}, "LEAN MISFIRE chain",
     "Same as P0300+P0171: mixture first, ignition second."),
    ({"P0420", "P0300"}, "MISFIRE → CATALYST chain",
     "Unburned fuel from the misfire is cooking the catalyst. The P0420 is "
     "a SYMPTOM: fix the misfire FIRST, or a new cat dies the same way."),
    ({"P0420", "P0430"}, "BOTH CATS flagged",
     "Both cats rarely die together — look for a shared upstream cause: "
     "exhaust leak, engine running rich/lean, or rear O2 sensors aging."),
    ({"P0440", "P0442"}, "EVAP family cluster",
     "Almost always a leak in the evap system. Gas cap first ($0), then "
     "smoke test. Harmless to drive; fails emissions inspection."),
    ({"P0440", "P0455"}, "EVAP family cluster",
     "Large leak: check the gas cap is tight and sealing, then hoses."),
    ({"P0442", "P0455"}, "EVAP family cluster",
     "Leak sizing disagrees — likely cap + small crack. Smoke test settles it."),
    ({"P0128", "P0171"}, "COLD ENGINE runs lean",
     "Thermostat stuck open keeps engine in warm-up fueling: check running "
     "temp before chasing the lean code."),
]

SEV_LABEL = {3: "STOP-DRIVING", 2: "FIX-SOON", 1: "MONITOR"}
SEV_ACTION = {
    3: "Park the car. Risk of cascading damage (cat fire, chain jump, "
       "stall in traffic). Tow or drive <1 mi at low load, once.",
    2: "OK to drive gently for days, not weeks. Book a shop this week; "
       "damage is progressive (cat, plugs, mileage).",
    1: "Informational / early. Safe to drive. Check cheap causes, watch "
       "for repeat within a week.",
}


def decode(codes, short=False):
    lines = []
    unknown = []
    worst = 0
    emissions = False
    for c in codes:
        c = c.upper().strip()
        entry = CODES.get(c)
        if entry is None:
            kind = c[0] if c else "?"
            if kind == "P" and re.match(r"^P[013][0-9A-F]{3}$", c):
                unknown.append((c, "generic-range P-code not in local DB — "
                                   "meaning is SAE-standard; look up for your "
                                   "make/model, verdict unknown"))
            elif kind == "P" and re.match(r"^P2[0-9A-F]{3}$", c):
                unknown.append((c, "generic-range P2xxx not in local DB "
                                   "(SAE generic, often manufacturer-"
                                   "defined sub-detail); look up for your "
                                   "make/model"))
            elif kind in "BCU":
                unknown.append((c, f"{kind}-code is manufacturer-specific "
                                   "(body/chassis/network) — needs make-"
                                   "specific lookup; U-codes: check battery "
                                   "voltage and grounds first"))
            elif kind == "P":
                unknown.append((c, "manufacturer-specific P1xxx — meaning "
                                   "varies by make; look up for your vehicle"))
            else:
                unknown.append((c, "not a valid OBD2 code format"))
            continue
        name, system, sev, causes = entry
        worst = max(worst, sev)
        if system == "emissions":
            emissions = True
        if short:
            lines.append(f"{c}  {name}  [{SEV_LABEL[sev]}]")
            continue
        lines.append(f"{c} — {name}")
        lines.append(f"  system: {system} | severity: {SEV_LABEL[sev]}")
        if causes:
            lines.append("  likely causes (cheapest first):")
            for cause, cost, diy in causes:
                lines.append(f"    - {cause}  [{cost} | DIY: {diy}]")
        lines.append("")

    return lines, unknown, worst, emissions


def pattern_scan(codes):
    found = []
    cset = {c.upper() for c in codes}
    for need, title, text in PATTERNS:
        if need <= cset:
            found.append((need, title, text))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("codes", nargs="*", help="DTC codes, e.g. P0171 P0174")
    ap.add_argument("--short", action="store_true", help="one line per code")
    ap.add_argument("--list-system", metavar="SYS",
                    help="list codes in system (fuel/ignition/emissions/"
                         "sensor/trans/engine/electrical)")
    args = ap.parse_args(argv)

    if args.list_system:
        sysname = {"evap": "emissions", "evaporative": "emissions",
                   "air": "fuel", "mix": "fuel"}.get(
                       args.list_system.lower(), args.list_system.lower())
        hits = [(c, v[0]) for c, v in sorted(CODES.items())
                if v[1] == sysname and v[0] != "reserved"]
        if not hits:
            print(f"no codes in system '{sysname}' "
                  f"(try: fuel ignition emissions sensor trans engine electrical)")
            return 1
        for c, name in hits:
            print(f"{c}  {name}")
        return 0

    if not args.codes:
        ap.print_help()
        return 1

    # 1. patterns first (root cause before symptoms)
    pats = pattern_scan(args.codes)
    if pats and not args.short:
        print("=" * 66)
        print("PATTERN(S) DETECTED — read this before individual codes")
        print("=" * 66)
        for need, title, text in pats:
            print(f"  {'+'.join(sorted(need))}: {title}")
            print(f"    {text}")
            print()

    lines, unknown, worst, emissions = decode(args.codes, args.short)
    print("\n".join(lines))
    if unknown:
        print("NOT IN LOCAL DB:")
        for c, msg in unknown:
            print(f"  {c}: {msg}")
        print()

    if worst:
        print("=" * 66)
        print(f"WHOLE-SET VERDICT: {SEV_LABEL[worst]}")
        print(SEV_ACTION[worst])
        if emissions:
            print("Emissions-related codes present — clearing to pass an "
                  "inspection resets readiness monitors (rejected as "
                  "'not ready' + fault returns). Clear AFTER fixing.")
        print("Flashing check-engine light overrides everything: active "
              "misfire = park it.")

    # return non-zero if unknown codes only
    return 0 if (lines or not unknown) else 1


if __name__ == "__main__":
    sys.exit(main())
