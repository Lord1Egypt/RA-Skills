# Music Practice Buddy

**Analyze instrumental practice recordings to detect timing, pitch, tempo, and dynamics issues. Get objective feedback and targeted exercises.**

## The Real-World Problem

Every musician has experienced this: you practice a piece for hours, it feels "off," but you can't tell exactly what's wrong. Is your timing off? Your pitch? Your tempo? Without a teacher listening, you're guessing.

Professional musicians have teachers who catch these issues instantly: "You're rushing the bridge," "Your intonation dropped on the high passage," "Your dynamics are flat." Self-taught musicians and students practicing alone have... nothing but their own ears, which are notoriously unreliable at self-assessment.

**Music Practice Buddy** brings objective audio analysis to every practice session. Record yourself, get specific data on timing, pitch, tempo, and dynamics — and a targeted practice plan to fix your weakest area.

## Who Needs This

- **Self-taught musicians** without regular access to a teacher
- **Music students** who want feedback between lessons
- **Amateur musicians** preparing for a performance or audition
- **Singers** working on pitch accuracy
- **Band members** practicing parts individually
- **Music teachers** who want to supplement their feedback with data
- **Anyone preparing for graded music exams** (ABRSM, Trinity, etc.)

## How It Works

1. **Tempo Detection** — Uses onset detection (identifying note starts) and autocorrelation to estimate your BPM
2. **Timing Analysis** — Measures the intervals between note onsets; flags gaps >50ms as timing inconsistencies
3. **Pitch Tracking** — Extracts the fundamental frequency over time using autocorrelation; measures stability
4. **Dynamic Analysis** — Computes RMS energy (volume) over time; identifies imbalances and flat sections
5. **Scoring** — Converts raw measurements into 0–100 scores per dimension
6. **Recommendations** — Matches weaknesses to specific exercises from evidence-based practice methodology

## Quick Start

```bash
# Analyze a recording
python scripts/practice_buddy.py analyze practice.wav

# With a target tempo
python scripts/practice_buddy.py analyze practice.wav --target-bpm 120

# Track improvement
python scripts/practice_buddy.py compare week1.wav week2.wav
```

## Example Scenario

**Mike**, a self-taught guitarist, has been learning a song for 3 weeks. It sounds OK but "something's off." He records himself:

```bash
python scripts/practice_buddy.py analyze solo.wav
```

**Report shows:**
- Timing: 64/100 — several notes are slightly ahead of the beat
- Pitch: 88/100 — solid
- Tempo: 71/100 — drifting faster in the chorus
- Dynamics: 59/100 — volume drops during fast passages

**Diagnosis:** Mike is **rushing** — speeding up and losing timing consistency, especially in technically demanding sections. He doesn't realize this because his ear normalizes the drift.

**Targeted plan:**
```bash
python scripts/practice_buddy.py plan solo.wav --instrument guitar --minutes 30
```

Output: 30-minute plan focused on timing — 10 min metronome at 60% speed, 10 min metronome at 80%, 10 min at full speed. Specific focus on the chorus transitions where drift is worst.

Mike practices the plan for a week, re-records, and compares:
```bash
python scripts/practice_buddy.py compare week3.wav week4.wav
```

**Result:** Timing score jumps from 64 → 82. Tempo consistency from 71 → 89. The objective data confirms what he can now hear: he's improved.

## Why It Works

- **Objective measurement replaces subjective guesswork** — you know exactly what to fix
- **Targeted practice is 3× more effective** than "playing it again" (Ericsson, 1993)
- **Progress tracking motivates** — seeing scores improve over weeks builds confidence
- **Self-assessment bias correction** — musicians consistently misjudge their own timing and tempo

## Installation

```bash
git clone https://github.com/voronindenis5/music-practice-buddy.git
cd music-practice-buddy
pip install numpy
```

## Requirements

- Python 3.8+
- numpy (for signal processing)
- WAV format recordings (convert from other formats with ffmpeg if needed)

## License

MIT — free for personal and educational use.
