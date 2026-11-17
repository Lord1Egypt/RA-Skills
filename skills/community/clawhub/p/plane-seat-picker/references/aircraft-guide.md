# Plane Seat Picker — Reference

Aircraft family data, seat-letter logic per layout, and the
evidence behind the strategies in `scripts/seat_picker.py`.

## 1. Seat-letter logic by cabin layout

Airlines vary letters, but the standard scheme:

| Layout | Windows | Middles | Aisles | Notes |
|---|---|---|---|---|
| 2-2 (E175/195, biz) | A, C | — | C? no: A C / D F | both seats touch aisle or window |
| 2-3 (A220) | A, plus the 3-block window | the 3-block middle | C (2-side), D, F | couples: A+C pair; avoid the 3-block middle |
| 3-3 (A320/737) | A, F | B, E | C, D | left ABC, right DEF |
| 3-3-3 (787, A350) | A, K (or A, L) | B, E, F(/G), J | C, D, G(/H), J-ish | airline letter drift is real — decode on the map |
| 3-4-3 (777 dense, A380 main) | A, L | middle of each block | varies | middle-of-4 (E,F on 3-4-3) = worst flying seat |

The decode command uses family defaults; ALWAYS cross-check the
letter on the actual airline map — letters drift between airlines
and even subfleets.

## 2. Family quick facts

### A320 / A321 (ceo)
- Layout 3-3, pitch 29-31", width ~18".
- Over-wing exits split around rows 11-15 depending on config:
  row ahead of exit = no recline.
- Loud band: rows ~10-17 (engines). Front (rows 1-8) noticeably
  quieter — the real reason people pay "preferred seating" even
  when pitch is identical.

### A320neo / A321neo
- Same layout; engine noise dramatically lower (geared turbofan /
  LEAP). If you hate noise, neo is a genuine upgrade — worth
  checking the aircraft subtype before booking two options.
- A321neo LR/XLR long-haul: 3-3 at 30" for 8+ hours — pick
  front-third + window for sleep, aisle-adjacent for stretching.

### 737-800 / 737 MAX 8
- Layout 3-3, pitch 29-31".
- Over-wing exits around row 14-16: rows 13-14 may not recline.
- MAX is quieter than -800 at similar weights. Sky-interior bins
  slope: side bins pinch at taller window-seat heads.

### A220-100 / -300
- Layout 2-3, pitch 30-32", width 18.5-18.9" (widest in class).
- No bad seat except the 3-block middle; couples should take the
  2-side (A+C). Windows are large and LOW (great view, cold wall).
- Cabin is small: service reaches everyone fast, deplaning quick.

### E175 / E195
- Layout 2-2, pitch 29-31".
- NO middle seats on the aircraft. A=C windows, aisle next to each.
- Ride is bumpier at the back (short fuselage, wing-forward);
  front rows smoother. Row 1 often has no window (blank panel).

### 787-8 / -9 / -10
- Layout 3-3-3, pitch 30-32", width 17.2-17.5" (narrow for the
  cabin length — the real comfort complaint).
- Electronic window dimming: no shade to pull; crew can lock ALL
  windows dark — light-sensitive sleepers: eyeshade, always.
- Lower cabin altitude (6,000 ft) genuinely reduces fatigue —
  hydration matters more than seat choice on these.

### A350
- Layout 3-3-3, pitch 31-32", width ~18".
- Very quiet up front; noise rises behind the wing.
- Windows misaligned in some rows (frame spacing): the map won't
  tell you — reviews of your specific airline config will.

### 777-300ER / -9
- 3-4-3 dense configs: pitch 31-32" but 17.2" width; middle-of-4
  seats are the worst in economy. 2-5-2 or 3-3-3 (rare now) configs
  are strictly better — a reason to prefer an airline/subfleet.
- The 2-side pairs (A-C) on 3-4-3 are the hidden value.

### A380
- Main deck 3-4-3: boarding wave, bigger cabin feel, more engine
  rumble transfer; upper deck 2-4-2: quieter, smaller, side bins —
  the best economy experience at the back of a plane, anywhere.

## 3. Zone logic that holds across configs

1. Front third: faster deplaning, first meal choice, less
   turbulence perception (nose), usually quieter (ahead of engines
   on wing-mounted aircraft).
2. Over-wing: smoothest ride (near the center of lift) — motion
   sickness and nervous flyers want rows at the wing root; window
   for horizon reference.
3. Back third: louder, later service, more engine vibration, but
   statistically emptier on lightly-booked flights (middle-seat
   lottery odds improve).
4. Lav/galley clusters at doors 2/3: ±1 row noise halo; the aisle
   seat on the lav side takes bumps all night.
5. Last row(s): fixed or heavily limited recline (wall behind),
   full meal-service skip risk on short runs.

## 4. Bassinet and infant specifics

- Bassinets mount on bulkheads (usually row 1 of each cabin
  section); count per aircraft: 2-6. Weight limits ~11-14 kg
  (varies); length limits apply.
- Must reserve: via airline phone/booking remark usually, not
  online at all airlines; do it at booking.
- Lap infants: cannot be in exit rows (whole party); infant fare
  ~10% of adult + taxes.
- Bulkhead with infant: you're prioritized for bassinet bulkheads —
  the "crying baby row" stigma works in your favor: neighbors who
  book bulkheads knowingly accept it.
- Car seat onboard: must be approved (label), usually requires a
  purchased seat, window-position only (can't block others' egress).

## 5. The middle-seat-empty gamble (evidence)

- On flights under ~80% load, middles fill last — window+aisle
  pairs on the 3-block have the best odds of staying split.
- On full flights you've guaranteed a stranger between you; the
  social play: keep the window+aisle, offer the swap when someone
  sits ("we're together, want the window or aisle?") — most take a
  side seat and you end up adjacent anyway.
- Never do the gambit on a red-eye full flight expecting mercy at
  seatAssignment roulette — load factors on red-eyes skew high.

## 6. Timing rules

- Seat maps open at booking for most airlines; good rows go at
  T-48h before the flight (check-in upgrades, elite windows) —
  re-check at T-24h.
- Equipment changes are most common T-7d to T-1d; if your row
  number stops existing, the swap happened — re-pick fast, the
  earlier you re-claim the better rows go.
- Basic economy seat assignment at T-24h/gate: families get some
  protection (US DOT rules require seating kids under 13 with a
  parent at no charge when bought together — claim it, agents
  don't always volunteer it).
