# Prompt Hardening — Research Sources

## Primary Sources

1. **asgeirtj/system_prompts_leaks** — Leaked system prompts from Claude Code, ChatGPT Agent Mode, Codex CLI, Gemini CLI, Warp Agent, Google Jules
2. **Anthropic: Building Effective Agents** — Tool design > prompt rules, poka-yoke patterns
3. **Anthropic: Prompting Best Practices** — WHY-based constraints, XML structure, anti-overengineering
4. **OpenAI GPT-5 Prompting Guide** — Agentic eagerness control, tool-call budgets, scoped XML blocks

## Empirical Data

5. **sinc-LLM Framework** (275 production agents) — Constraints account for 42.7% of output quality; task description only 2.8%
6. **Liu et al. 2023 "Lost in the Middle"** — LLMs attend most to beginning and end of context; middle instructions 20% less likely followed
7. **Reddit r/PromptEngineering Echo-Check** (500+ upvotes) — Pre-execution constraint restatement improves compliance 40-60%

## Agent Framework Patterns

8. **CrewAI** — Closed-world tool declaration, existential stakes, self-attributed error correction
9. **SWE-agent** — Single-action-per-turn constraint with parser backup
10. **Devin 2.0** — Prohibition + positive replacement, mandatory think-before-act checkpoints
11. **Factory DROID** — State machine with Boolean pre-condition gates
12. **Instructor (jxnl)** — Validate-reject-retry loop for near-100% compliance
13. **Claude Code** — Primacy/recency bracketing, IMPORTANT prefix, Use X (NOT Y) pattern
