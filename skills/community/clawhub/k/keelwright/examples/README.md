# Examples — toy apps to try keelwright on

Three minimal projects to see keelwright's gates fire. Each is a deliberately small
loop-coding target; run keelwright alongside your agent and watch the gates.

## 1. `toy-flask-api/` — a 1-file web API
- **Task:** "build a /login endpoint that checks a hardcoded user".
- **What keelwright catches:** R2 (hardcoded password), R1 (SQL string concat if you use a DB).
- **Try:** `cd toy-flask-api && python app.py` then `curl localhost:5000/login`.

## 2. `toy-cli/` — a command-line tool
- **Task:** "a CLI that renames files by a pattern".
- **What keelwright catches:** R8 slopsquatting if the agent suggests a fake package;
  R3 business-logic review if the rename is destructive.
- **Try:** `cd toy-cli && python main.py --help`.

## 3. `toy-loop/` — an autonomous loop
- **Task:** "loop: fetch a number, double it, write to file, repeat 10x".
- **What keelwright catches:** circuit-breaker (doom-loop guard), R12 preflight.
- **Try:** `cd toy-loop && python loop.py` — watch breaker.py cap iterations.

## 30-second try (no install of keelwright internals needed)
1. Load the skill by name (`keelwright`) in your agent before coding.
2. Paste any toy task above into your agent.
3. Read the gate report at session end: `Keelwright this session: <N> gates passed,
   <M> traps avoided, <K> attacks blocked.`

No agent? Run the demo directly:
```bash
python scripts/validate_run.py --self-test   # exercises GATE 1-8 on a built-in sample
```
