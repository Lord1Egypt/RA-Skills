You are generating an OpenClaw skill.

Create a folder with:
- SKILL.md: concise, includes purpose, tools exposed, and guardrails.
- Any needed code files (keep minimal).

Constraints:
- Safe local-only skill. No network calls unless explicitly requested.
- Prefer simple tools that shell out to allowlisted commands.
- Do NOT instruct destructive commands (rm, sudo, etc.).
- Assume workspace root is /Users/clawdbot/.openclaw/workspace.
