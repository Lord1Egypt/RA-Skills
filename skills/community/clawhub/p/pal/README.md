# 🔍 Project Analyzer

**An OpenClaw skill that analyzes any project directory and gives you an instant orientation report.**

Never stare at an unfamiliar codebase wondering where to start again. Just message your agent:

> "Analyze this project"  
> "What does ~/projects/my-app do?"  
> `/scout`

And get back a clear, structured breakdown — what the project does, what tech it uses, where to start reading, and how to run it.

---

## What it does

Project Scout scans a directory and produces a report covering:

- **What the project does** — plain English summary
- **Tech stack** — languages, frameworks, and key libraries (auto-detected)
- **Directory structure** — an annotated file tree
- **Entry points** — the files a new developer should read first
- **How to run it** — install, build, and run commands extracted from package.json, Makefile, README, etc.
- **Notes** — anything unusual worth knowing

---

## Usage

After installing, just talk to your agent naturally:

```
Analyze this project
What does ~/projects/my-app do?
I'm new to this codebase, give me an overview
/scout
/scout ~/projects/my-app
/scout .
```

---

## Install

```bash
openclaw skills install project-analyzer
```

Or via ClawHub CLI:

```bash
clawhub install project-analyzer
```

**Requires:** Python 3 on your PATH.

---

## How it works

The skill runs a local Python script (`scout.py`) that:

1. Walks the directory tree (skipping `node_modules`, `.git`, build folders, etc.)
2. Reads key files: `README.md`, `package.json`, `pyproject.toml`, `Dockerfile`, source files, configs
3. Auto-detects languages (by file extension counts) and frameworks (by dependency fingerprinting)
4. Identifies likely entry points (`main.py`, `index.ts`, `cmd/main.go`, etc.)
5. Extracts run commands from `package.json` scripts, Makefiles, and READMEs
6. Returns all of this to the agent, which formats a clear report for your chat channel

Everything runs locally — no data leaves your machine.

---

## Supported tech detection

**Languages:** Python, JavaScript, TypeScript, Go, Rust, Java, Kotlin, C, C++, C#, Ruby, PHP, Swift, Dart, Lua, R, Julia, Elixir, Erlang, Haskell, Shell, SQL, GraphQL, Terraform, and more.

**Frameworks / libraries:** React, Vue, Angular, Svelte, Next.js, Nuxt, Remix, Gatsby, Astro, Express, Fastify, NestJS, Django, Flask, FastAPI, Rails, Laravel, Spring, Electron, Tauri, Docker Compose, Kubernetes, Terraform, Prisma, SQLAlchemy, LangChain, Anthropic SDK, PyTorch, TensorFlow, and more.

---

## Files

```
project-analyzer/
├── SKILL.md      ← OpenClaw skill definition (instructions for the agent)
├── scout.py      ← Python scanner (runs locally via exec tool)
└── README.md     ← This file
```

---

## Contributing

Found a framework that isn't detected? Want to add a new output format? PRs welcome! The detection logic lives in `scout.py` in the `FRAMEWORK_HINTS` and `EXT_LANGUAGE` dictionaries — easy to extend.

---

## License

MIT — free to use, modify, and share.
