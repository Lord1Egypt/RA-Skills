# Holiday Lights Electrical Reference

## Why loads go wrong

US holiday-light fires concentrate on two mechanisms: overloaded circuits/
cords (heat in the cord, plug, or timer — not the bulbs) and damaged/wet
connections. The bulbs almost never start the fire; the wiring feeding them
does. That's why this skill's math targets amps through cords, plugs, and
timers rather than "how many lights look right."

## Circuit budgets (US residential, 120 V)

| Breaker | Nameplate | 80% continuous budget | Honest string budget* |
|---------|-----------|----------------------|------------------------|
| 15 A    | 1,800 W   | 1,440 W              | ~1,300 W after reserves |
| 20 A    | 2,400 W   | 1,920 W              | ~1,750 W after reserves |

*Assuming ~100 W existing always-on load on the circuit. A circuit you can't
name the other residents of (fridge, AV wall, bathroom GFCI sharing) should
be treated as having LESS room, not more.

The 80% rule (NEC continuous-load doctrine) matters here: a display running
6+ hours is continuous in every practical sense. Planning to nameplate means
planning to nuisance-trip on a cold night when the fridge compressor kicks.

## Per-type wattage (measured ranges)

| Type | Per bulb / per m | 100-bulb string | Notes |
|------|------------------|-----------------|-------|
| Incandescent mini | 0.40–0.49 W | ~45 W | the classic roofline eater |
| Incandescent C7   | 5–7 W       | n/a (25-bulb ~125 W) | socket-by-socket heat |
| Incandescent C9   | 7–10 W      | n/a (25-bulb ~175 W) | 12 strings ≈ a space heater |
| LED mini          | 0.05–0.09 W | ~7 W | 90%+ reduction |
| LED C9            | ~0.1 W      | n/a | |
| Rope, incandescent| ~5.5 W/m    | 15 m ≈ 83 W | |
| Rope, LED         | ~2.0 W/m    | 15 m ≈ 30 W | |
| Net lights (inc.) | ~0.45 W/bulb| 150-bulb net ≈ 68 W | drape load, 3-run limit |
| Inflatable blower | 50–150 W continuous | — | a motor, not a light |
| Projector         | 30–100 W    | — | fan inside; keep vents clear |

## Daisy-chain (end-to-end) limits

The limit is the fused plug on the first string, plus the conductor size of
the wire between strings. Typical box ratings:

- Incandescent mini: **3–5 strings** end-to-end (read the tag on the plug).
- Incandescent C7/C9: **2 strings** (often fewer — 5–10 W/bulb adds fast).
- LED mini: 20–45+ (the wall wart / controller rating usually binds first).
- Never build a "T" of power strips to defeat the fuse. Split runs at the
  wall outlet instead — the house wiring is rated for far more than the
  string wire is.

## Extension cords

| AWG | Light duty ≤13 A | Comfortable 10 A |
|-----|------------------|------------------|
| 16  | ≤ 50 ft          | ≤ 25 ft          |
| 14  | ≤ 100 ft         | ≤ 50 ft          |
| 12  | ≤ 150 ft         | ≤ 100 ft         |
| 10  | ≤ 250 ft         | ≤ 150 ft         |

Rules of thumb that prevent fires:

1. Outdoor = outdoor-rated jacket (marked "W"), always.
2. Never coil a loaded cord (coiled cord = induction heating + trapped heat).
3. Never under a rug, through a door pinch, or through a wall.
4. Plug-to-plug connections outdoors: elevate, wrap pointing down in a
   bubble cover so water can't track into the socket.
5. One cord per outlet tap; avoid stacking multi-taps.

## Outdoor checklist

- Source is GFCI-protected (test the TEST button — it should kill the lights).
- Lights and cords marked for wet/outdoor use.
- Plugs off the ground, in covers.
- Strings attached with plastic hooks/clip systems — never nailed/stapled
  through the wire (the #1 self-inflicted damage mechanism).
- Take-down before they get brittle in late-winter sun.

## Timers and photocells

A timer is a switch with a contact rating. Mechanical holiday timers are
commonly rated 10–15 A; photocell stakes 6–10 A; cheap indoor dial timers
5–10 A. The contact carries the ENTIRE load through it. Rating check:
`timer_amps ≥ total_amps` or split loads.

## Energy and LED payback

- Season (45 nights × 6 h = 270 h): every 100 W of incandescent = 27 kWh ≈
  $4.59 at $0.17/kWh.
- A 24-string incandescent roofline (~1,080 W) costs ~$49/season; the LED
  equivalent (~170 W) costs ~$8. The swap pays back in 1–2 seasons on energy
  alone, before counting the capacity it frees (912 W ≈ 20 more mini
  equivalents' worth of headroom on the same circuit).
- Inflatables run all night if you let them: a timer on inflatables is the
  cheapest single energy win (blowers are continuous motors).

## Distress signs after hanging (act on any of these)

- Plug, timer, or cord warm to the touch after 15 minutes.
- Lights dimming when another appliance starts (circuit is at the edge).
- Breaker trips more than once: re-plan the split, don't just reset.
- Any flicker tied to a specific string: unplug that string before touching.

## Non-US note

230 V regions: same watts, half the amps — cords breathe easier, but the
80% doctrine and daisy-chain fuse logic are identical. Series-wired European
string fuses blow at lower counts; read the plug.
