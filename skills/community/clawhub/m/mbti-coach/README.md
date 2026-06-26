# MBTI Coach ✨

> *You can become anyone you want to be. Personality is not fixed — it's a skill.*

An OpenClaw skill that turns MBTI from a personality label into a personal development system. Your AI coach tracks your cognitive functions, designs your daily schedule, and helps you grow into the person you're trying to become.

---

## The Idea

Most people treat MBTI as a fixed identity: "I'm an INFP, that's just who I am."

This skill treats it differently: **MBTI is a map of cognitive functions, and cognitive functions can be trained.**

Want to think more strategically like an ENTJ? Build stronger Te.
Want to connect more deeply with people like an INFJ? Develop Fe.
Want to stop second-guessing everything? Train your dominant function until it's effortless.

Your personality isn't a cage. It's a starting point.

---

## What It Does

### 🧠 Deep Personality Profiling
- Assesses your current MBTI type AND your actual cognitive function scores
- Maps historical types to understand your development trajectory
- Uses 5 situational questions to calibrate beyond self-reported labels
- Validates with stress response patterns (your inferior function doesn't lie)

### 📊 Cognitive Function Tracking
Tracks 8 cognitive functions with real scores:
- **Te** — Strategic execution, external systems thinking
- **Ti** — Internal logic, framework building
- **Fe** — Group harmony, emotional attunement
- **Fi** — Personal values, authentic self-expression
- **Se** — Present-moment awareness, action
- **Si** — Experience-based wisdom, reliability
- **Ne** — Possibility-seeking, pattern connection
- **Ni** — Long-range vision, convergent insight

### 📅 Personalized Growth Schedule
- Designs daily exercises targeting your weakest functions
- Integrates with Feishu/Lark calendar for real scheduling
- Adapts based on your progress and feedback

### 🎭 Multi-Perspective Coaching
Ask Hikaru to respond as any MBTI type:
- "Give me feedback as an ENTJ"
- "How would an INFJ handle this situation?"
- "Challenge my thinking like an ENTP"

### 📈 Progress Visualization
- Radar charts showing your cognitive function development
- Milestone tracking
- Honest assessment of where you're growing vs. stagnating

---

## Quick Start

### Installation

```bash
# Copy to your OpenClaw workspace
cp -r mbti-coach ~/.openclaw/workspace/skills/

# Configure environment
cp mbti-coach/.env.example mbti-coach/.env
# Edit .env with your Feishu/Lark credentials (optional)
```

### First Session

Just tell your OpenClaw agent:
> "MBTI coach, let's start"

Or trigger with keywords: `MBTI` / `人格教练` / `我想变成` / `安排日程` / `查看进度`

### First Run Flow

1. **Current type assessment** — What type are you now?
2. **Historical types** — How have you changed over time?
3. **Cognitive function calibration** — 5 situational questions
4. **Stress response validation** — Your inferior function reveals the truth
5. **Goal setting** — Who do you want to become?
6. **First week schedule** — Concrete daily exercises

---

## How Personality Development Actually Works

The MBTI Manual (Myers, Briggs, et al.) describes personality development as the **gradual differentiation and integration of cognitive functions** over a lifetime.

You're not changing *who* you are. You're expanding *what you can do*.

An INFP who develops Te doesn't stop being an INFP. They become an INFP who can also execute decisively, lead teams, and build systems — while still having that deep Fi authenticity that makes them who they are.

**The goal is integration, not replacement.**

This skill operationalizes that process:
- Identify your current function stack
- Choose functions to develop
- Get targeted daily practice
- Track progress over time
- Watch your radar chart expand

---

## File Structure

```
mbti-coach/
├── SKILL.md              # Full skill definition and coaching system
├── README.md             # This file
├── .env.example          # Environment variables template
├── data/
│   └── profile.json      # Your personality profile (local, private)
└── scripts/
    ├── feishu_calendar.sh # Feishu/Lark calendar integration
    └── radar_chart.py     # Cognitive function visualization
```

---

## Contributing

This is an early-stage skill. The coaching system works, but there's a lot to build:

**High-priority contributions:**
- Google Calendar integration (Feishu works, Google is next)
- More sophisticated progress tracking algorithms
- Community-sourced cognitive function exercises
- Type-specific development roadmaps
- Integration with habit tracking apps

**How to contribute:**
- Share your own cognitive function exercises that worked
- Add type-specific coaching scenarios to SKILL.md
- Improve the radar chart visualization
- Build integrations with other calendar/habit systems

The more people build this, the better the coaching gets for everyone.

---

## Privacy

Your profile is stored locally in `data/profile.json`. Nothing is shared externally. This is your personal development data — it stays on your machine.

---

## Philosophy

MBTI has a reputation problem. It's been oversimplified into Buzzfeed quizzes and Twitter personality wars.

The original work — Isabel Briggs Myers, her mother Katharine Cook Briggs, and Carl Jung before them — was about something more serious: **helping people understand themselves deeply enough to grow deliberately.**

That's what this skill is trying to recover.

Not "what's your type?" as an identity label.
But "what are your cognitive strengths and weaknesses, and how do you develop the ones you need?"

---

## License

MIT. Build something meaningful with it.

---

*"You can become anyone you want to be. Start by understanding who you are."*
