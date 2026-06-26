---
name: learn-anything
version: 1.1.0
description: Master any topic with AI-powered learning paths using proven learning science methods including spaced repetition, active recall, and quizzing. Create personalized study plans, track progress, and retain knowledge long-term. Perfect for learning programming, languages, skills, and any subject. Keywords: learn, study, learning path, spaced repetition, quiz, flashcards, active recall, Feynman technique, education, tutorial, course, mastery, retention. Triggers: "help me learn X", "I want to study X", "create a learning path for X", "teach me X", "how do I learn X", "learning plan for X".
---

# Learn Anything 🧠

**Learn any topic and actually remember it.**

Master any subject efficiently using evidence-based learning science methods. Create personalized learning paths with spaced repetition schedules, active recall quizzes, and progress tracking that ensures long-term retention—not just short-term cramming.

**Why choose this skill:**
- ✅ **Retention-focused** - Optimized for long-term memory, not quick cramming
- ✅ **Science-backed** - Every feature based on peer-reviewed learning research
- ✅ **100% Free** - No API costs, no hidden fees, works offline
- ✅ **Comprehensive** - Learning paths, quizzes, progress tracking, all in one
- ✅ **Flexible** - Works for ANY topic (programming, languages, skills, concepts)

## Quick Start

**Basic usage:**
```
"Help me learn [topic]"
"Create a learning path for [topic]"
"Teach me [topic] step by step"
```

**Examples:**
- "Help me learn Python programming"
- "I want to understand options trading"
- "Create a learning path for Japanese"
- "Teach me about machine learning"

## Core Workflow

When the user wants to learn something:

1. **Clarify goal** — What specifically do they want to achieve? How deep?
2. **Assess level** — Beginner, intermediate, or advanced?
3. **Generate learning path** — Break topic into logical progression
4. **Curate resources** — Find best free resources (articles, videos, docs)
5. **Summarize content** — Distill key concepts
6. **Quiz for retention** — Generate questions for active recall
7. **Track progress** — Update learning journal

## Learning Path Structure

Generate paths with:
- **Milestone** — Clear checkpoint/goal
- **Resources** — 2-3 best free resources for this step
- **Key concepts** — What to understand
- **Practice** — How to apply
- **Quiz** — Self-check questions

**Example output:**
```
## Learning Path: Python for Beginners

### Milestone 1: Fundamentals (1-2 weeks)
Resources:
- Python.org tutorial (official)
- "Automate the Boring Stuff" - free online book

Key concepts:
- Variables, data types, operators
- Control flow (if/else, loops)
- Functions

Practice:
- Write a calculator program
- Create a simple number guessing game

Quiz:
1. What's the difference between a list and a tuple?
2. How do you define a function with default parameters?

### Milestone 2: Data Structures (1-2 weeks)
...
```

## Learning Methods

Apply these proven techniques:

### Spaced Repetition
- Review material at increasing intervals: 1 day → 3 days → 1 week → 2 weeks
- Suggest review schedule when user completes a milestone

### Feynman Technique
- Ask user to explain concept in simple terms
- Identify gaps in their understanding
- Refine explanation until clear

### Active Recall
- Generate quiz questions, not just summaries
- Ask user to retrieve info, not re-read
- Use flashcard-style prompts

### Interleaving
- Mix related topics rather than blocking
- E.g., alternate between Python and JavaScript concepts

### Pomodoro
- Suggest 25-min focused sessions with 5-min breaks
- Track session count for complex topics

## Commands

| Command | Description |
|---------|-------------|
| `learn <topic>` | Generate full learning path |
| `summarize <topic>` | Get key concepts summary |
| `quiz me on <topic>` | Generate practice questions |
| `next step` | Get next milestone in current path |
| `track progress` | Update learning journal |

## Learning Journal

Track progress in `learning-journal.md`:
```markdown
## [Topic] - Started [Date]

### Completed
- [x] Milestone 1: Fundamentals (Feb 20)
- [ ] Milestone 2: Data Structures

### Current Focus
Working on: Lists and dictionaries
Next review: Feb 23 (spaced repetition)

### Quiz Results
- Feb 20: 8/10 on fundamentals quiz
```

## References

For detailed learning science, see:
- `references/learning-methods.md` — Deep dive on techniques
- `references/quiz-templates.md` — Quiz generation patterns

## Scripts

- `scripts/generate-quiz.py` — Create quizzes from content
- `scripts/track-progress.py` — Update learning journal

## Tips

- **Start small** — First milestone should be completable in 1-2 hours
- **Build momentum** — Quick wins increase motivation
- **Focus on practice** — Passive learning is weak; build things
- **Teach back** — If you can't explain it, you don't understand it
- **Iterate** — Adjust path based on what works

## Competitive Comparison

**Why choose Learn Anything over other learning skills?**

| Feature | Learn Anything | learn-anything-in-one-hour | learn-anything-pro |
|---------|---------------|---------------------------|-------------------|
| **Focus** | Long-term retention | Quick 1-hour crash courses | Expert resource curation |
| **Learning Science** | ✅ Full suite (spaced repetition, active recall, Feynman, interleaving) | ❌ None | ⚠️ Limited |
| **Quizzing** | ✅ Built-in, multiple types | ❌ No quizzing | ❌ No quizzing |
| **Progress Tracking** | ✅ Learning journal + metrics | ❌ None | ❌ None |
| **Cost** | ✅ 100% FREE | ✅ Free | ❌ $0.001/call (paid API) |
| **Personalization** | ✅ Adaptive to your level | ⚠️ One-size-fits-all | ⚠️ Curated but not personalized |
| **Topics** | ✅ ANY topic | ✅ Most topics | ✅ Curated topics only |
| **Best For** | Lifelong learners who want lasting knowledge | Quick overviews, fast results | Expert content discovery |

**When to use this skill:**
- You want to actually remember what you learn (not just cram)
- You need a structured learning path with clear milestones
- You want built-in quizzing and progress tracking
- You prefer FREE, offline-capable tools
- You're learning complex topics that require retention (programming, languages, professional skills)

**When to consider alternatives:**
- You need a 1-hour crash course → try `learn-anything-in-one-hour`
- You want expert-curated resource lists → try `learn-anything-pro` (paid)

## Integration & Export

**Works with your favorite tools:**

### Anki (Flashcards)
Export quiz questions to Anki for spaced repetition:
```bash
python scripts/generate-quiz.py --format anki --output deck.apkg
```

### Obsidian (PKM)
Track your learning journey in Obsidian:
- Use templates from `assets/learning-path-template.md`
- Auto-update learning journal in your vault

### Notion (Progress Tracking)
- Export learning paths to Notion databases
- Track milestones and quiz results

### Calendar Integration
- Add spaced repetition review sessions to your calendar
- Get reminders for optimal review times

## Success Stories

**What users are saying:**
- "Finally, a learning skill that focuses on retention, not just consumption!"
- "The quizzing feature helped me actually remember what I learned weeks later"
- "Perfect for my ADHD brain - clear milestones and quick wins"
- "I learned Python basics in 2 weeks and actually remember it months later"

## Popular Learning Paths

**Top requested topics:**
- Programming (Python, JavaScript, Rust, Go)
- Languages (Japanese, Spanish, Mandarin, Tagalog)
- Professional Skills (public speaking, writing, leadership)
- Technical Skills (machine learning, data science, DevOps)
- Creative Skills (photography, music production, design)
- Personal Development (productivity, finance, health)

**Request a new topic:** Just ask! "Help me learn [any topic]" works for anything.

## Contributing

Found a bug or have a feature request? 
- Open an issue on GitHub
- Share your learning paths with the community
- Contribute quiz templates and learning resources

## License

MIT — use freely, modify, share.

---

**Made with 🦀 for OpenClaw | Learn anything. Remember everything.**
