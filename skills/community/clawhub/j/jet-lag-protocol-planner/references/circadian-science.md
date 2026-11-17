# Circadian Science Behind the Jet-Lag Protocol Planner

This reference documents the model the script implements, the constants, and
the reasoning. Everything is drawn from established human circadian
phase-response literature (Eastman & Burgess's practical protocols, the
light/melatonin phase-response curves from Khalsa et al. 2003 and Lewy et
al. 1998, and field studies of pre-flight shifting). No claim here is
novel — the skill is careful *arithmetic and timing logic* on top of it.

## 1. The anchor: CBTmin

Core body temperature follows a circadian sinusoid; its minimum (CBTmin)
lands, in a typical adult, roughly **2 hours before habitual wake time**.
CBTmin is the divide between the two halves of the phase-response curve:

```
CBTmin = habitual_wake − 2 h        (e.g. wake 07:00 → CBTmin 05:00)
```

Jet lag = local clock time minus your CBTmin position. Alignment protocol =
moving CBTmin toward the destination's night at a survivable rate.

## 2. Phase-response curves

### Light PRC (phase shifts produced by bright-light exposure)
- Exposure in the **~4 h before CBTmin** (late biological night) → **delay**
  (clock pushed later). Peak effect just before CBTmin.
- Exposure in the **~4 h after CBTmin** (biological morning) → **advance**
  (clock pulled earlier). Peak effect just after CBTmin.
- Brightness matters: ~50–100× brighter than typical indoor light (outdoor
  light is 1,000–10,000 lux; indoors is 100–300 lux) does the real work.
  Overcast outdoor light still beats any indoor room.

### Melatonin PRC (low exogenous dose)
- Roughly the **mirror image** of the light curve (Lewy et al.):
  - ~**5 h before CBTmin** → **advance** (max advance ≈ 5 h before)
  - **after CBTmin** → **delay** (smaller effect)
- Practical dose: **0.3–1 mg** timed for the PRC, **not** a hypnotic 5–10 mg
  at bedtime. High doses add grogginess without better phase shifting.
- Melatonin also has a modest direct sleep-promoting effect when taken
  0.5–1 h before desired bedtime — useful on the plane.

## 3. Alignment speed limits

| Direction | Spontaneous realignment rate | With timed light + melatonin |
|---|---|---|
| Eastward (advance) | ~0.5–1 h/day | ~1–1.5 h/day |
| Westward (delay) | ~1–1.5 h/day | ~1.5–2 h/day |

Pre-trip shifting at home (moving sleep 1 h/day opposite the trip direction)
"pre-pays" shift so the remainder at arrival is smaller. Practical caps:
~2–3 h of pre-payment eastward, ~2 h westward (shifting more than ~1 h/day
at home costs too much daytime function).

## 4. Direction and the wrap-around

The clock never "advances 17 hours". For offset difference Δ:
- If Δ (east-positive) > +12 h → treat as Δ − 24 (i.e. delay instead).
- If Δ < −12 h → treat as Δ + 24.
Example: UTC+3 → UTC−5 is +... careful with sign convention — the script
normalizes: LA (UTC−8) → Tokyo (UTC+9) raw +17 h ⇒ −7 h (delay 7 h) —
delaying sleep is dramatically easier than advancing 17 h.

## 5. In-flight rules (flight day)
- Set watch to destination at boarding; eat/sleep on destination cues.
- Sleep on plane **only** inside destination's night window that overlaps the
  flight; otherwise stay awake (light-exposure control = eye mask + shades).
- Caffeine allowed early in the flight per destination morning; cutoff
  ~6 h before planned destination sleep.
- Alcohol undermines both sleep architecture and the phase marker — skip.
- Hydrate: cabin air is ~10–20% RH; dehydration worsens subjective jet lag.

## 6. First days at destination
- **Eastward**: mornings are the danger zone (light too early = delay). Seek
  light mid-morning onward; avoid bright light before shifted CBTmin; melatonin
  early evening local (falls 4–6 h before CBTmin as it drifts).
- **Westward**: evenings are the danger zone (light after CBTmin extends the
  day the wrong way — but wait, west you WANT delay…). Precisely: westward
  you want evening light (delay is the goal) and you must avoid early-morning
  light. Melatonin: NOT in the morning at destination (post-CBTmin dosing is
  a delay — actually that's desired westward, but daytime melatonin = groggy;
  standard practice: skip melatonin westward or use tiny dose on waking only
  if returning East the same week — keep it simple: westward = light only).
- Nap doctrine: <25–30 min, before 15:00 local, alarm set. Longer/later naps
  anchor the old phase.
- Performance reality: expect ~1 h of internal misalignment per time zone to
  decay per ~day eastward; schedule high-stakes events ≥2 days in when >6 h.

## 7. What the script does NOT model
- Individual chronotype extremes (DLMO measurement would anchor better than
  habitual-wake heuristic; the 2 h-before-wake CBTmin estimate has ±1 h
  personal variance — shift windows ±30 min if you know you're an extreme
  lark or owl).
- Flight timing nuances (red-eye vs day flight interacts with the light
  plan; the day table gives the doctrine, apply judgment onboard).
- Medication interactions, pregnancy, mood disorders with light sensitivity
  — the skill defers to clinicians there.
