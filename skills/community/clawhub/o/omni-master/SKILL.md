---
name: omni
description: >
  The all-in-one master skill — unified interface for every capability domain.
  Use when the user asks for anything that spans multiple domains or when no
  single specialized skill clearly applies. Covers: automation & workflows,
  coding & development, data analysis & databases, web scraping & browsing,
  finance & accounting, security & hardening, image/video/audio generation &
  editing, music creation, email & messaging, calendar & scheduling, document
  processing (PDF/DOCX/PPTX), translation, writing & content creation,
  project management, deployment & DevOps, IoT & smart home, communication
  platforms, knowledge management, CLI tools, system administration,
  API design & testing, and general problem-solving.
  Triggers on: "do everything", "all in one", "omni", "master skill",
  "mega skill", or any task where routing to the right domain matters.
---

# OMNI — The All-In-One Skill

Unified intelligence across every domain. Route, execute, deliver.

## Architecture

```
omni/
├── SKILL.md          ← You are here (master router)
├── references/       ← Domain-specific deep dives (load on demand)
│   ├── brain.md      ← ALWAYS LOAD THIS FIRST — cognitive protocols
│   ├── advanced-prompting.md  ← Transform bad prompts into great results
│   ├── data-literacy.md       ← Data types, stats, viz, quality, ethics
│   ├── reasoning.md           ← Problem decomposition, decisions, logic
│   ├── math-engine.md         ← Arithmetic → calculus, stats, finance
│   ├── research.md            ← Search, fact-check, source evaluation
│   ├── quality-assurance.md   ← Testing, review, verification
│   ├── performance.md         ← Profiling, optimization, monitoring
│   ├── ethics-safety.md       ← Boundaries, privacy, responsible use
│   ├── health-fitness.md      ← Nutrition, workouts, wellness tracking
│   ├── career.md              ← Resume, interviews, networking, salary
│   ├── learning.md            ← Teaching, study techniques, quizzes
│   ├── network-cloud.md       ← DNS, SSH, VPN, AWS/Azure/GCP, K8s
│   ├── creative.md            ← Fiction, content, design thinking, rhetoric
│   ├── multi-agent.md         ← Agent orchestration & collaboration
│   ├── realtime.md            ← WebSockets, SSE, queues, webhooks
│   ├── automation.md
│   ├── coding.md
│   ├── data-databases.md
│   ├── web-scraping.md
│   ├── finance.md
│   ├── security.md
│   ├── media-generation.md
│   ├── music-audio.md
│   ├── email-messaging.md
│   ├── calendar-scheduling.md
│   ├── documents.md
│   ├── translation.md
│   ├── writing-content.md
│   ├── project-management.md
│   ├── deployment-devops.md
│   ├── iot-smarthome.md
│   ├── communications.md
│   ├── knowledge-mgmt.md
│   ├── system-admin.md
│   └── api-design.md
└── scripts/          ← Reusable automation scripts
    └── router.sh
```

## Brain Protocol (ALWAYS ACTIVE)

**Before any action, load `references/brain.md`.** It governs:
1. **Error Memory** — Check `memory/mistakes.json` before repeating any failed approach
2. **Loop Detection** — Same command fails twice? STOP. Change approach entirely.
3. **Anti-Hallucination** — Verify before stating. Say "I don't know" when uncertain.
4. **Precision Code** — Read → Research → Plan → Write → Test → Deliver
5. **Perfect Memory** — Log decisions, errors, patterns to `memory/*.json`
6. **Debug Protocol** — Reproduce → Isolate → Hypothesize → Test → Document

Brain runs first, domain routing runs second. Always.

## Routing Protocol

When a task arrives, classify it into one or more domains, then load only the
relevant reference file(s). Do NOT load all references — progressive disclosure
keeps context lean.

### Domain Detection

| Signal words → | Domain → | Reference file |
|---|---|---|
| *(always)* | **Brain** (cognitive engine) | `references/brain.md` ← LOAD FIRST |
| workflow, pipeline, automate, cron, schedule, trigger | Automation | `references/automation.md` |
| code, program, script, debug, refactor, git, PR, commit | Coding | `references/coding.md` |
| data, analyze, SQL, query, database, CSV, chart, dashboard | Data & DB | `references/data-databases.md` |
| scrape, crawl, browse, fetch, URL, website, HTML | Web | `references/web-scraping.md` |
| money, budget, invoice, finance, accounting, stock, crypto | Finance | `references/finance.md` |
| security, audit, firewall, vulnerability, encrypt, harden | Security | `references/security.md` |
| image, photo, generate, edit, video, frame, screenshot | Media | `references/media-generation.md` |
| music, song, audio, sound, TTS, voice, podcast | Music/Audio | `references/music-audio.md` |
| email, mail, inbox, send message, SMS, chat | Email/Messaging | `references/email-messaging.md` |
| calendar, event, meeting, schedule, reminder, appointment | Calendar | `references/calendar-scheduling.md` |
| PDF, DOCX, document, spreadsheet, presentation, OCR | Documents | `references/documents.md` |
| translate, language, i18n, locale | Translation | `references/translation.md` |
| write, article, blog, essay, copy, content, book | Writing | `references/writing-content.md` |
| project, task, board, kanban, milestone, sprint | Projects | `references/project-management.md` |
| deploy, CI/CD, Docker, cloud, server, infrastructure | DevOps | `references/deployment-devops.md` |
| smart home, IoT, Hue, Sonos, light, thermostat, camera | IoT | `references/iot-smarthome.md` |
| Discord, Telegram, Slack, WhatsApp, iMessage, Signal | Comms | `references/communications.md` |
| notes, wiki, knowledge, Notion, Obsidian, bookmark | Knowledge | `references/knowledge-mgmt.md` |
| system, OS, process, disk, network, terminal, shell | SysAdmin | `references/system-admin.md` |
| API, endpoint, REST, GraphQL, webhook, schema | API | `references/api-design.md` |
| vague, unclear, bad prompt, interpret, refine | Prompting | `references/advanced-prompting.md` |
| data types, statistics, visualization, clean, quality | Data Literacy | `references/data-literacy.md` |
| think, reason, decide, analyze, problem, logic, debug | Reasoning | `references/reasoning.md` |
| math, calculate, equation, statistics, convert, formula | Math | `references/math-engine.md` |
| research, verify, fact-check, source, search, find | Research | `references/research.md` |
| test, QA, review, validate, verify, quality | QA | `references/quality-assurance.md` |
| performance, optimize, fast, slow, profile, benchmark | Performance | `references/performance.md` |
| ethics, safety, privacy, boundary, responsible, safe | Ethics | `references/ethics-safety.md` |
| health, fitness, workout, nutrition, meal, diet, exercise, wellness | Health | `references/health-fitness.md` |
| resume, CV, interview, career, salary, job, cover letter, hiring | Career | `references/career.md` |
| teach, learn, study, quiz, flashcard, explain, tutor, education | Learning | `references/learning.md` |
| DNS, SSH, VPN, cloud, AWS, Azure, GCP, Kubernetes, network, tunnel | Network/Cloud | `references/network-cloud.md` |
| creative, fiction, story, brainstorm, design, presentation, rhetoric | Creative | `references/creative.md` |
| multi-agent, orchestrate, collaborate, parallel agent, spawn agent | Multi-Agent | `references/multi-agent.md` |
| websocket, realtime, event-driven, queue, webhook, SSE, streaming | Realtime | `references/realtime.md` |

### Multi-Domain Tasks

When a task spans multiple domains, load each relevant reference. Common combos:
- **Build & deploy app** → coding + deployment-devops
- **Automated email reports** → automation + email-messaging + data-databases
- **Security audit of codebase** → security + coding
- **Scrape data → analyze → visualize** → web-scraping + data-databases + media-generation

## Execution Principles

0. **Brain Check** — Load brain.md. Check mistakes.json. Verify you're not in a loop.
1. **Identify** — Classify the task into domain(s)
2. **Load** — Read only relevant reference(s)
3. **Plan** — Outline approach before executing
4. **Execute** — Use the best tool for the job (CLI > API > manual)
5. **Verify** — Check output quality before delivering
6. **Log** — Record to mistakes.json if error, patterns.json if reusable, daily log always
7. **Report** — Summarize what was done and what's next

## Installed Skills Reference

These skills are already available and should be used directly when applicable.
The omni skill supplements them with domain knowledge, not replaces them:

### Communication & Messaging
- **discord** — Discord operations
- **slack** — Slack control (reactions, pins)
- **bluebubbles** — iMessage via BlueBubbles
- **imsg** — iMessage/SMS CLI
- **wacli** — WhatsApp messaging
- **voice-call** — Voice calls
- **xurl** — X (Twitter) API

### Productivity & Notes
- **apple-notes** — macOS Notes via `memo`
- **apple-reminders** — macOS Reminders via `remindctl`
- **bear-notes** — Bear notes via `grizzly`
- **things-mac** — Things 3 task manager
- **notion** — Notion API (pages, databases, blocks)
- **obsidian** — Obsidian vault management
- **trello** — Trello boards/lists/cards
- **gog** — Google Workspace (Gmail, Calendar, Drive, Contacts, Sheets, Docs)
- **himalaya** — Email via IMAP/SMTP

### Development & GitHub
- **github** — GitHub CLI (issues, PRs, CI, review)
- **gh-issues** — GitHub issues → auto-fix PRs
- **coding-agent** — Delegate to Codex/Claude Code
- **mcporter** — MCP server management
- **gemini** — Gemini CLI for Q&A
- **oracle** — Oracle CLI (prompt bundling, sessions)

### Media & Creative
- **openai-image-gen** — Batch image generation
- **nano-banana-pro** — Gemini image gen/edit
- **openai-whisper** — Local speech-to-text
- **openai-whisper-api** — Cloud speech-to-text
- **sag** — ElevenLabs TTS
- **sherpa-onnx-tts** — Offline TTS
- **gifgrep** — GIF search/download
- **video-frames** — Video frame extraction
- **peekaboo** — macOS UI capture & automation
- **songsee** — Audio spectrograms
- **nano-pdf** — PDF editing with NL

### Music & Audio
- **spotify-player** — Spotify playback/search
- **sonoscli** — Sonos speaker control
- **blucli** — BluOS audio
- **songsee** — Audio visualization

### Smart Home & IoT
- **openhue** — Philips Hue lights
- **eightctl** — Eight Sleep pods
- **camsnap** — RTSP/ONVIF cameras
- **sonoscli** — Sonos speakers

### Web & Search
- **weather** — Weather via wttr.in / Open-Meteo
- **goplaces** — Google Places API
- **blogwatcher** — RSS/Atom feed monitoring
- **summarize** — URL/podcast/file summarization

### System & Security
- **healthcheck** — Security hardening & audits
- **1password** — 1Password CLI secrets
- **node-connect** — OpenClaw node diagnostics
- **session-logs** — Session log analysis
- **tmux** — tmux session control

### Platform & Ecosystem
- **canvas** — UI canvas presentation
- **clawhub** — Skill marketplace
- **skill-creator** — Skill development
- **model-usage** — Model cost tracking

### Food & Ordering
- **ordercli** — Foodora order tracking

## When NOT to Use This Skill

If a specialized installed skill clearly matches the task, use that skill directly.
Omni is the fallback and the glue — it fills gaps and handles cross-domain work.
