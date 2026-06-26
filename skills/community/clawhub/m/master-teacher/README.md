# Master Teacher 🎓

Systematic teaching skill for AI agents — mastery learning, Socratic questioning, and progress tracking.

Transforms your AI agent into a master-level instructor for teaching complex technical topics (architecture, source code analysis, system design).

## Features

- **Prep before teaching** — agent researches the topic before lecturing
- **Mastery learning** — students must pass verification (≥2/3) before advancing
- **Socratic questioning** — guide with questions, don't give conclusions
- **Structured lessons** — position → theory → code → relate to practice → verify
- **Progress tracking** — persistent across fragmented learning sessions
- **Adaptive pacing** — handles "too easy", "don't understand", off-topic, silence
- **Mid-course review** — revisit weak points at halfway mark
- **Final report** — summary of mastery, weak points, and next steps

## Install

### Claude Code

```bash
# Option 1: Clone to personal skills
git clone https://github.com/jacky-wzj/master-teacher.git ~/.claude/skills/master-teacher

# Option 2: Clone to project skills
git clone https://github.com/jacky-wzj/master-teacher.git .claude/skills/master-teacher
```

Then in Claude Code, the skill activates when you say things like:
- "教我 X"
- "teach me about X"
- "我要系统学习 X"
- "create a course on X"

Or invoke directly: `/master-teacher`

### OpenClaw

```bash
# From ClawHub
clawhub install master-teacher

# Or clone manually
git clone https://github.com/jacky-wzj/master-teacher.git ~/.openclaw/skills/master-teacher
```

The skill triggers when the user asks to systematically learn a topic.

## Usage

Once installed, just ask the agent to teach you something:

```
我想系统学习 Claude Code 的架构设计
```

The agent will:
1. **Prep** — research the topic first
2. **Profile** — check what it already knows about you, ask only what's missing
3. **Outline** — propose a curriculum, wait for your confirmation
4. **Teach** — deliver lessons one at a time with verification
5. **Track** — save progress so you can resume anytime

## Course files

Each course is stored in the workspace:

```
<workspace>/<course-name>/
├── README.md              # Course outline
├── lessons/
│   ├── lesson-01-xxx.md   # Lesson content
│   └── lesson-02-xxx.md
└── progress/
    └── tracking.md        # Learning progress
```

## License

MIT
