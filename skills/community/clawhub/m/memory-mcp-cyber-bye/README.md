# Memory MCP OpenClaw Skill

This directory contains the instruction skill manual for the OpenClaw agent. It guides the LLM on how to use the graph-based memory system with persona tracking, emotional memory, adaptive learning, and knowledge graph entities.

---

## File Contents

- [SKILL.md](file:///agent-resources/memory-mcp-sql/skill/SKILL.md): Declares the OpenClaw skill manifest header, YAML metadata, and core instruction prompts.

---

## Usage

When OpenClaw loads this skill, the guidelines in `SKILL.md` are appended to the agent's system prompt or tool-usage instructions. It teaches the agent:
1. To use 9 consolidated tools (`memory`, `entity`, `relation`, `short_term`, `project`, `context`, `extract`, `share`, `search`) via the `op` parameter.
2. How to leverage the 8-phase auto-linking system for cross-session memory continuity.
3. How to track user persona, mood, and learning patterns for personalized interactions.
4. How to create proactive reminders and surface smart suggestions based on memory health.