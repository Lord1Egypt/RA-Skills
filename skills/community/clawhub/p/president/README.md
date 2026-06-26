# President.skill

> Think and Act Like an American President.

President.skill transforms the decision-making frameworks of U.S. Presidents into deployable AI perspectives. Navigate negotiations, leadership challenges, and high-stakes decisions using the mental models that shaped world history.

---

## Quick Start

### Install via ClawHub CLI (Recommended)

```bash
# Install the full president skill
clawhub install president

# Or install a specific president perspective
clawhub install president-trump
```

### Manual Installation

```bash
# Clone to OpenClaw skills directory
git clone https://github.com/minimax/president-skill.git ~/.openclaw/skills/president

# Or copy to your project workspace
cp -r president /path/to/your/project/skills/
```

### First Use

Activate Trump perspective by saying:

```
Use Trump's perspective on this negotiation
```

Or:

```
How would Trump handle this opponent?
```

Or:

```
Apply the Art of the Deal to my current situation
```

**Default behavior**: If you say "what would a president do" without specifying, Trump (the sitting president) activates by default.

---

## Available Presidents

| Slot | President | Term | Status |
|------|-----------|------|--------|
| ⭐ **01-trump** | **Donald J. Trump** | **45 / 47 (2017–21, 2025–)** | **Active** |
| 02-washington | George Washington | 1 (1789–97) | Coming Soon |
| 17-lincoln | Abraham Lincoln | 16 (1861–65) | Coming Soon |
| 26-roosevelt-t | Theodore Roosevelt | 26 (1901–09) | Coming Soon |
| 40-reagan | Ronald Reagan | 40 (1981–89) | Coming Soon |

### ⭐ Donald J. Trump (01-trump)

45th / 47th President of the United States. The flagship perspective.

**5 Core Mental Models**:
1. The Art of the Deal — Everything is negotiation
2. America First — The universal filter for all decisions
3. Win at All Costs — Winner culture
4. Counter-Punch Doctrine — Counterattack is the only option
5. Drain the Swamp — Outsider status is an asset

**9 Decision Heuristics**

**Complete Expression DNA**

---

## How It Works

### Trigger Words

Any of these will activate Trump:
- Names: Trump, DJT, 45, 47
- Slogans: Make America Great Again, MAGA, America First
- Frameworks: Art of the Deal, Drain the Swamp
- Questions: "How would Trump...", "What would Trump do...", "Trump perspective"
- Slang: "This is a bad deal", "They're ripping me off", "Should I walk away"

### Roleplay Modes

**Mode 1: Direct Activation**
Activate a specific president to analyze your situation through their lens.

**Mode 2: Decision Advisory**
Get specific advice using a president's framework for your problem.

**Mode 3: Multi-President Comparison**
Have multiple presidents analyze the same issue from different angles.

### Exit Roleplay

Say "exit", "stop", or "return to normal" to exit presidential perspective and return to standard mode.

---

## Project Structure

```
president/
├── SKILL.md                    # Top-level meta-skill entry
├── clawhub.json               # ClawHub registry configuration
├── README.md                  # This file
├── LICENSE                   # MIT License
└── presidents/
    └── 01-trump/              # Trump perspective
        ├── SKILL.md           # Trump thinking operating system
        ├── meta.json          # Presidential metadata
        └── references/
            └── research/      # 6 research documents
                ├── 01-writings.md
                ├── 02-conversations.md
                ├── 03-expression-dna.md
                ├── 04-external-views.md
                ├── 05-decisions.md
                └── 06-timeline.md
```

---

## Design Principles

1. **Self-contained perspectives**: Each president can be copied and used independently
2. **Observational, not judgmental**: Extract thinking patterns without political moralizing
3. **Use the president's own language**: Mental models named in each president's own terminology
4. **Honest boundaries**: Each perspective explicitly states its limitations
5. **Evidence-based**: Executive orders and signed legislation > campaign slogans > tweets

---

## Contributing

This project is part of the **Easter Resurrection Week 2026** initiative — a focused effort to extract and preserve the thinking operating systems of all 45 U.S. Presidents.

To add a new president:
1. Create a new directory under `presidents/[XX-lastname]/`
2. Copy the research framework from existing perspectives
3. Extract 6 research documents
4. Assemble the final SKILL.md
5. Submit a pull request

---

## Links

- **GitHub**: [github.com/minimax/president-skill](https://github.com/minimax/president-skill)
- **ClawHub**: [clawhub.ai/skills/president](https://clawhub.ai)
- **Original Project**: [github.com/realteamprinz/president-skill](https://github.com/realteamprinz/president-skill)

---

## License

MIT License

---

> "We will make America strong again. We will make America proud again. We will make America safe again. And yes, together, we will make America Great Again."
> — Donald J. Trump

🇺🇸 **May God bless the United States of America.** 🇺🇸
