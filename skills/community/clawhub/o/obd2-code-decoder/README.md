# OBD2 Code Decoder

**Check-engine light → plain English → safe-to-drive verdict → real cost bands.**

## The problem

The check-engine light is the most ignored warning in the world, and the most
mis-diagnosed. A $20 dongle hands you codes like `P0420 P0171 P0300`; a web
search returns 40 causes and a $2,400 worst case, so people either panic at a
shop ("just replace whatever") or ignore a misfire until the catalytic
converter is destroyed. The information gap between "code" and "decision" is
where this skill lives.

## What it does

`scripts/obd2_decoder.py` (stdlib-only, offline):

1. **Decodes 55+ generic codes** — plain-language meaning, subsystem,
   severity ladder: `STOP-DRIVING` / `FIX-SOON` / `MONITOR`.
2. **Pattern engine** — the money-saver. Code COMBINATIONS share root causes:
   - `P0171+P0174` = one vacuum leak, not two O2 sensors
   - `P0300+P0420` = misfire is killing the cat; fix misfire first or the new
     cat dies too
   - `P0440/42/55` evap cluster = usually the gas cap ($0) before a smoke test
3. **Cost bands + DIY difficulty**, always cheapest-cause-first with the
   "mimics" called out (exhaust leak mimics P0420).
4. **Clearing rules** — when clearing is legitimate, why clearing before an
   emissions test fails anyway (readiness monitors), and the flashing-light
   override rule.
5. Honest fallback for manufacturer-specific P1xxx / B / C / U codes instead
   of invented meanings.

## Example

```bash
$ python3 scripts/obd2_decoder.py P0171 P0174 P0300
==================================================================
PATTERN(S) DETECTED — read this before individual codes
==================================================================
  P0171+P0174: BOTH BANKS LEAN — one shared cause
    A single vacuum leak, dirty MAF, or weak fuel pump leans BOTH banks...
  P0300+P0171: LEAN MISFIRE chain
    The lean condition is causing the misfire. Fix mixture first...
...
WHOLE-SET VERDICT: FIX-SOON
```

## Who needs this

Any driver with a $15 OBD2 dongle (hundreds of millions of cars on the road
with generic OBD2 ports), used-car buyers reading a pre-purchase scan, and
anyone deciding "can I drive to work tomorrow" at 8 pm on a Sunday.

## Scope & honesty

Generic P0/P2 codes decode identically across makes; P1/B/C/U codes are
manufacturer-specific and the tool says so instead of guessing. Cost bands
are US independent-shop ranges, 2020s. Not a replacement for a mechanic's
hands — it is the decision layer before you talk to one.

## License

MIT © 2026 Denis Voronin
