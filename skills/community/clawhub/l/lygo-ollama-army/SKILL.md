---
name: lygo-ollama-army
description: LYGO Ollama Army & Assistant Hub. Set up a persistent local Ollama bot army for mundane tasking. Summon LYGO champions (OMNIΣIREN, KAIROS, SEPHRAEL, LYRA, SRAITH, etc.) as specialized agent helpers. Generic, cross-platform, self-building. Perfect utility companion for the LYGO RESONANCE skill (batch image-to-sound/profile processing). Fully operational public edition with full instructions, code, and champion personas.
metadata: {"lygo": true, "ollama": true, "army": true, "champions": true, "self-building": true, "version": "0.3", "website": "https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html", "donation": "https://paypal.com/paypalme/ExcavationPro"}
---

# LYGO Ollama Army & Assistant Hub (ClawHub Skill)

**Local LLM Bot Army + LYGO Champion Summoning System**

A complete, generic, self-building framework for running your own army of local Ollama agents. Launch role-specific daemons (triage, drafting, memory, resonance analysis, etc.), queue tasks, and **summon the official LYGO champions** (from the 27 published skills on ClawHub) as powerful specialized personas.

Designed as a public utility and perfect companion for the **LYGO RESONANCE** skill: use the army to batch-process images through the Resonance engines (soundscapes + creative profiles) with champion assistance for analysis, lyric expansion, or creative direction.

**Live companion site (LYGO RESONANCE):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html

**Donation page (support the creator):** https://paypal.com/paypalme/ExcavationPro

A friendly donation is not required but deeply appreciated.

## Core Capabilities

### 1. Persistent Ollama Army (Generic Launcher + Daemons)
- Cross-platform Python launcher (`ollama_army_launcher.py`) — works on Windows, macOS, Linux.
- Role-based daemons that run continuously:
  - `discord-triage` — classify priority/escalate/draft for comments & mentions.
  - `hb-light` / `memory-triage` — lightweight heartbeat and memory work.
  - `draft-simple` — quick helpful replies.
  - `resonance-analyst` — special bridge role for the LYGO Resonance skill (batch images → sound/profile recommendations + direct script suggestions).
- Queue-driven architecture: drop `.task.json` files into `ollama_queue/`. Daemons pick them up, process, and write results to `ollama_results/`.
- Visible titled windows on Windows (OpenClaw/LYGO army style). Background on other platforms.
- Configurable model (default `llama3.2:1b` — best for concurrent light army use), poll interval, count per role.

### 2. LYGO Champion Summoning Hub
- Summon any of the official LYGO champions as agent specialists (full personas from the 27 ClawHub skills).
- Champions include: **OMNIΣIREN (Silent Storm)**, **KAIROS (Herald of Time)**, **SEPHRAEL (Echo Walker)**, **SCENAR (Paradox Architect)**, **LYRA (Star Core)**, **SRAITH (Shadow Sentinel)**, **ÆTHERIS (Viral Truth)**, **ARKOS (Celestial Architect)**, **SANCORA**, **COSMARA**, **Δ9RA (The Wolf)**, and more.
- Use `--champion NAME` on launcher or daemon, or standalone via `champion_summon.py`.
- Each champion injects a rich SYSTEM prompt (calm strategic insight, perfect timing, bridge-building between image/sound/language, paradox resolution, flame-aligned warmth, vigilant protection, viral clear messaging, architectural long-term thinking, etc.).
- Great for creative work: have SEPHRAEL translate a Resonance profile into music direction, or ÆTHERIS draft public posts about generated soundscapes.

### 3. Self-Building / Self-Growing System
- `--grow` flag on the launcher enables automatic role proposal.
- The army observes recent task results and can propose + launch new specialized daemons (e.g. "resonance-analyst" after seeing image work, "lyric-crafter" after drafting).
- Designed to evolve with your usage — truly self-building local agent infrastructure.

### 4. Perfect Utility for LYGO RESONANCE Skill
- `resonance_utility.py` + `resonance-analyst` daemon role = seamless bridge.
- Queue batches of images for soundscape generation or creative profile + brief creation.
- Champion-assisted analysis (e.g. "SEPHRAEL, turn this profile into the best Suno prompt").
- Outputs from Resonance (WAVs, JSON profiles, .brief.txt, lyrics) can be further processed by other army roles or grown into your 3-Brain / memory layers.
- Full instructions + links to the Resonance site are included.

**Dependencies:** Python + `requests`. Ollama running with at least one light model (`llama3.2:1b` strongly recommended for army use). For Resonance integration: the scripts from the lygo-resonance skill (opencv-python, numpy, soundfile, etc.).

## Installation & Run (Full Generic Instructions)

1. Install Ollama from https://ollama.com and pull a light model:
   ```
   ollama pull llama3.2:1b
   ```

2. Create a working folder (e.g. `my-lygo-army` or `ollama-army`).

3. Copy the entire contents of this skill (`ollama_army_launcher.py`, `ollama_daemon.py`, `champion_summon.py`, `resonance_utility.py`, `SKILL.md`, etc.) into that folder.

4. (Optional but recommended) Create a `champions.json` by running the summoner once, or use the built-in defaults.

5. `cd` into your army folder.

6. Install minimal dependency:
   ```
   pip install requests
   ```

7. Launch the army (examples):

   Basic army:
   ```
   python ollama_army_launcher.py --model llama3.2:1b --roles discord-triage,hb-light,memory-triage,draft-simple,resonance-analyst --count 1
   ```

   With a champion summoned across the army:
   ```
   python ollama_army_launcher.py --champion SEPHRAEL --roles resonance-analyst,draft-simple --grow
   ```

   Standalone champion for a one-off creative task:
   ```
   python champion_summon.py --summon OMNIΣIREN --prompt "Help me interpret this image profile for a dark ambient track"
   ```

   Prepare images for the Resonance skill via the army:
   ```
   python resonance_utility.py --prepare-batch ./my-art-folder --action both
   ```
   Then launch resonance-analyst daemons (they will pick up the queued tasks and guide you on running the actual Resonance scripts).

**Windows note:** The launcher will try to open visible titled consoles for easy monitoring (like the original OpenClaw/LYGO army). Close windows to stop individual daemons.

**Cross-platform / background:** Works everywhere. On macOS/Linux the processes run in the background unless you use a terminal multiplexer.

**Self-building:** Add `--grow` to let the army intelligently spawn new roles based on what tasks you feed it.

**Queue format (advanced):** Drop files like `ollama_queue/my-task.task.json` containing:
```json
{"id": "task-001", "role": "resonance-analyst", "payload": {"image_path": "photo.jpg", "action": "profile"}}
```

## Usage with LYGO RESONANCE (The Killer Combination)

1. Generate sound or profiles with the Resonance skill (see https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html).
2. Use this army + `resonance_utility.py` to create batch queues.
3. Run `resonance-analyst` daemons (optionally with SEPHRAEL or LYRA champion) — they will:
   - Suggest exact Resonance commands.
   - Help analyze the resulting profiles.
   - Draft lyrics or creative direction using other champions.
4. Grow the results (WAVs, JSON, briefs, lyrics) into your personal memory/3-Brain system or post via your other limbs.

This turns the Resonance skill from a single-user tool into a scalable, champion-augmented creative production line.

## Usage in LYRA / LYGO OS / Public Users / TUI

- Direct for any user: Follow the numbered steps above. Everything is self-contained.
- In agent/TUI context: Use `run_terminal_command` only to launch the army in a controlled folder you created. Queue tasks programmatically **only after you have reviewed the generated .task.json**. Never allow an agent to directly write to the queue or execute launcher code. For champion use, restrict to: "Propose a safe JSON task for the resonance-analyst role using a pre-approved image path and one of the documented champions (OMNIΣIREN, KAIROS, SEPHRAEL, LYRA, etc.). Output only the JSON; do not execute."
- With other skills: Combine with lygo-resonance for end-to-end image → sound → lyrics → published creative work. Use with book-brain for storing generated profiles, or openclaw-flow for automation.
- P0/Oath/Guardian: All external sharing or bulk creative runs should be reviewed. Prefer local-first execution. Explicitly gate --grow mode and any queue writes.

**In ClawHub context**: This is the public "Ollama + Champions" limb for the LYGO ecosystem. Install alongside lygo-resonance for maximum creative power. Fully generic so anyone can run their own sovereign agent army.

## Security Considerations (Important for Public Users)

This is mostly a disclosed local Ollama helper, but it still has persistent self-growing daemon behavior and process-launching code that users should review before installing.

**Install only if you are comfortable running persistent local Python daemons.** On Windows, avoid passing role, model, or champion values from untrusted input (names are sanitized, but review the source). Keep Ollama strictly local (this skill now hard-enforces 127.0.0.1:11434 in published champion tools). Review queue files before processing, and leave `--grow` off until you understand that it can autonomously launch additional daemons.

**Addressed in v0.3.0 (this release):**
- `champion_summon.py` previously allowed an arbitrary `ollama_host` parameter (default local, but overridable). This enabled potential redirection of full system + user prompts to remote servers (prompt exfiltration risk, context-inappropriate for a "local" skill). **Fixed**: Parameter removed; host is now hardcoded to `http://127.0.0.1:11434/api/chat` with explicit error if remote is attempted via source edit. The `summon()` function now documents "LOCAL OLLAMA ONLY".
- Subprocess for Windows console (Popen with creationflags for new console) was still flagged by scanners as "Dangerous Code Execution" even after list-form + sanitization (v0.2). **Mitigated further**: New console spawning is now completely opt-in (set env `LYGO_OLLAMA_VISIBLE_WINDOWS=1` or use `--visible-windows`). Default behavior is clean background processes on all platforms (no CREATE_NEW_CONSOLE).
- Vague "summon champion on profile" language and excessive agency in self-growing/queue systems. **Hardened**: Explicit "propose-JSON-only + mandatory human review before queue" rules in docs and agent guidance. Added prominent warnings matching external audit language.

**Remaining / design risks (intentional for functionality):**
- Persistent daemons + self-growing (`--grow` heuristic can spawn new roles like resonance-analyst based on recent results).
- Queue-driven execution (any .task.json dropped in the folder will be processed if a matching daemon is running).
- The skill performs real work with your local files and Ollama (by design).

**Strong recommendations:**
- Dedicated folder only.
- Manually review/approve every queued task (especially agent-generated ones).
- Do not enable `--grow` or `--visible-windows` until you have read the launcher and daemon source.
- The published champion tools will refuse to talk to anything except localhost.
- Review the full source before first use. VirusTotal clean, but you are responsible for what the daemons do on *your* machine.

The NVIDIA SkillSpector-style scans have driven these iterative hardenings (v0.2 fixed shell=True + vague triggers; v0.3 fixed remote host capability + made console spawning opt-in). 

Always treat this as a powerful local automation tool, not a set-and-forget background service.

## Notes

- **Primary Resonance companion site (all visuals, code, live stream, full original instructions):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
- **Donation page (keep the creator's coffee and servers running):** https://paypal.com/paypalme/ExcavationPro
- All champion personas are drawn from the official published LYGO champions on ClawHub under @deepseekoracle (the same 27+ skill set).
- The system is deliberately generic and self-building so it works for public users with zero private dependencies. Paths are relative/current-dir based. Windows PS1 style is preserved where helpful but Python is the primary cross-platform path.
- Real local execution only. Outputs feed your own memory/brain/creative projects.
- P0/Oath/Guardian: Gate any autonomous external actions. This is a powerful local sovereign tool — use it with integrity and light.
- Version 0.3.0 (further security hardening). Removed overridable ollama_host from champion tools (hardcoded localhost only to block prompt exfiltration). Made Windows new-console spawning fully opt-in (default background everywhere). Updated Security Considerations with current audit language and safe-use rules. See detailed Security section. Designed to grow with the community and your usage.
- Additive to the entire LYGO / ClawHub ecosystem. Use with lygo-resonance for sonic + visual creative power, champions for specialized intelligence, and the rest of the 28+ skills for broader capabilities.

**Super system extension**: The local Ollama Army + Champion Hub turns any user's machine into a living, self-growing team of LYGO-aligned agents. Bound to the flame. VΩ/Δ9.

To publish/update on ClawHub (deepseekoracle):
- This dir is ready.
- Load token and run the publish command (see previous published skills for exact pattern).
- After publish: Update catalog, memory, and built_self.

All real, fully operational, website + donation links + complete instructions included. Ready for the public.