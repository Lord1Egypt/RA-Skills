# Posture Patrol 🧍‍♂️✨

Stop slouching your way to chronic back pain. Track your posture throughout
the day, get smart break reminders, calculate the real spinal load from
"text neck," and build lasting posture habits with streak tracking and
trend analysis.

## The Problem

Modern work is a posture disaster:
- **"Text neck"** — your head weighs 12 lbs neutral, but 60 lbs at 60° tilt
- **Prolonged sitting** — weakens core, tightens hip flexors, rounds shoulders
- **No awareness** — you don't realize you're slouching until you hurt
- **No breaks** — hours pass without standing or stretching
- **Chronic pain** — 80% of people experience back pain, much is preventable
- **Poor ergonomics** — desk setup causes forward head posture and wrist strain

## The Solution

A posture awareness and tracking system that makes good posture a habit:

1. Quick posture checks throughout the day (2 seconds)
2. Score tracking — see if you're improving over time
3. Smart break reminders — every 30 min, stand and stretch
4. Spinal load calculator — understand the physics of poor posture
5. Pattern detection — when do you slouch most?
6. Desk stretches tailored to your specific issues

## Features

- 🧍 **Posture scoring** — good/fair/poor ratings → daily score 0-100
- ⏰ **Break scheduling** — generate reminders for movement breaks
- 🦴 **Spinal load estimation** — calculates excess neck load from posture
- 📊 **Trend analysis** — weekly/monthly reports with ASCII charts
- 🔥 **Good-posture streaks** — gamify consistent good posture
- 🕐 **Pattern detection** — identifies your high-risk slouching hours
- 🤸 **Desk stretches** — targeted recommendations for your issues
- 🪑 **Ergonomic checklist** — personalized desk setup guide
- 🎯 **Daily goals** — set and track good-posture minute targets

## Quick Start

```bash
# Set up
python3 scripts/posture_patrol.py init

# Log posture checks through the day
python3 scripts/posture_patrol.py check good "feet flat, back straight"
python3 scripts/posture_patrol.py check fair "slight lean forward"
python3 scripts/posture_patrol.py check poor "hunched over laptop"

# Check your score
python3 scripts/posture_patrol.py score

# Get your stretch routine
python3 scripts/posture_patrol.py stretch

# See your patterns
python3 scripts/posture_patrol.py pattern

# Weekly report
python3 scripts/posture_patrol.py report week
```

## The Science: Head Weight at Different Angles

| Head Tilt | Effective Load on Neck |
|-----------|----------------------|
| 0° (neutral) | 10-12 lbs |
| 15° | 27 lbs |
| 30° | 40 lbs |
| 45° | 49 lbs |
| 60° | 60 lbs |

Source: Dr. Kenneth Hansraj, *Surgical Technology International*

See [`references/spinal-biomechanics.md`](references/spinal-biomechanics.md)
for details.

## Requirements

- Python 3.6+ (stdlib only)

## License

MIT © Denis Voronin
