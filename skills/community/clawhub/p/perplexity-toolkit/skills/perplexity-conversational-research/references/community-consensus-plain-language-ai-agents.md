# Community Consensus: Plain-Language AI-Agent Communication

Captured from a Perplexity multi-model research pass on 2026-09-01. This reference is a reusable evidence bank and workflow, not a permanent ranking. GitHub counts, product behavior, model names, licenses, and URLs are time-sensitive; re-check them before making current claims.

## Trigger

Use when the user asks for:

- a particularly influential person who makes ChatGPT/Claude Code/Codex speak plainly;
- a community-endorsed prompt, CLAUDE.md, skill, hook, or output style;
- the “best” anti-jargon, conclusion-first, low-narration setup.

## Evidence ladder

Separate three objects before ranking anything:

1. **Person** — identifiable author with a primary artifact or repeatable public practice.
2. **Project** — a maintained repository, plugin, skill, or workflow with adoption signals.
3. **Mechanism** — a product feature or configuration layer that reliably changes behavior.

Use these evidence tiers:

- **Strong:** first-party product mechanism, or an active public project with substantial adoption signals and a directly inspectable artifact. Adoption is not proof of output quality.
- **Medium:** concrete public artifact plus repeated discussion, forks, or limited adoption signals, but no independent behavior evaluation.
- **Anecdotal:** one post, one template, or self-reported improvement without reproducible measurements. Useful for hypotheses, not for calling something a consensus.

Always distinguish “community attention/adoption” from “behavioral effectiveness.” Stars, forks, installs, and reposts are signals of reach, not controlled evidence that an agent communicates better.

## Findings from the 2026-09-01 pass

### Julius Brussee / Caveman — strongest community phenomenon for compression

Primary source: https://github.com/JuliusBrussee/caveman

The repository page showed roughly 100k stars and 5.8k forks at capture time, supports 30+ agents, and exposes both an output skill and an input-compression proxy. Its README showed a 69-token normal-agent example versus a 19-token Caveman example. The project reported 33.2% fewer provider-reported input tokens in a pinned 54-run Claude Code benchmark while passing 18 exact-answer checks.

Interpretation:

- Strong adoption/visibility signal for the “remove narration and repetition” direction.
- The benchmark is project-authored, so it is not independent scientific validation.
- Caveman deliberately produces terse, sometimes telegraphic output. It is not automatically natural, friendly, or easy Chinese.
- Borrow the principles (no routine narration, preserve code/commands/errors, answer first), not the literal caveman voice.
- The repository distinguishes MIT-licensed skill/CLI surfaces from BSL-1.1 engine-linked runtime components; inspect the current license map before installation.

### Anthropic / Claude Code Output Styles — strongest practical mechanism

Primary sources:

- https://code.claude.com/docs/en/output-styles
- https://code.claude.com/docs/en/best-practices

The official Output Styles documentation says the built-in Concise style leads with the result, skips preamble and narration, and keeps replies short while retaining full engineering work. A custom output style can change role, tone, and format; `keep-coding-instructions: true` preserves the built-in software-engineering guidance when only the communication layer is being changed.

The official feature comparison separates responsibilities:

- Output Style: persistent role, tone, and response format.
- CLAUDE.md: project conventions and codebase context.
- Skills: reusable task-specific workflows.
- Hooks/Stop hooks: deterministic checks and stop-boundary enforcement.

The best-practice guide also says to supply tests/builds/screenshots or other checks and have the agent show the evidence. It warns that an over-specified CLAUDE.md gets diluted as context fills. This is the most defensible default for Claude Code, but it is an official mechanism rather than proof of a community A/B win.

### Affaan Mushtaq / Everything Claude Code (ECC) — strong harness architecture, not a plain-language solution

Primary source: https://github.com/affaan-m/ECC

The repository page showed roughly 242k stars and 36.6k forks at capture time, with 68 agents, 286 skills, 94 legacy command shims, hooks, rules, memory, and adapters for several agent harnesses including Codex.

Interpretation:

- Strong evidence that a layered agent harness (agents/skills/rules/hooks/memory) has broad community attention.
- It does not prove that ECC’s default wording is the best way to speak plainly.
- Do not recommend installing the full pack merely to fix verbosity. Borrow the separation of concerns and select only relevant components.

### Galaxy-Dawn / claude-scholar — closest inspectable communication template

Primary source: https://github.com/Galaxy-Dawn/claude-scholar/blob/main/CLAUDE.md

The inspected CLAUDE.md explicitly uses direct answer or executable path, then evidence/verification, then limits/assumptions/next steps. It asks for concrete wording and rejects vague phrases such as “optimize the workflow” unless the concrete action is named. The repository page showed roughly 5.2k stars at capture time.

Interpretation:

- A useful template specimen for conclusion-first, evidence-bearing responses.
- It is project-specific, longer than a minimal style adapter, and lacks independent proof that the full file improves behavior.
- Extract a small communication subset; do not copy the entire research-assistant operating contract into every coding project.

### DenisSergeevitch / chatgpt-custom-instructions — visible ChatGPT prompt, weak quality evidence

Primary source: https://github.com/DenisSergeevitch/chatgpt-custom-instructions

The repository page showed roughly 2.8k stars and 137 forks at capture time, and includes TL;DR-first and language-matching instructions. It also contains role/importance/reward-style prompt language and self-reported MMLU results with an acknowledged evaluation bug.

Interpretation:

- The repository is a real adoption/attention signal, not an empty gist.
- Do not treat its benchmark numbers as independently established.
- Extract only useful structural rules (answer first, match the user’s language, no unsolicited tables/follow-ups); avoid prompt theatre and claims of guaranteed performance.

### Community discussions — recurring pain, not a standard

Primary sources:

- https://news.ycombinator.com/item?id=49298159
- https://news.ycombinator.com/item?id=38765375

The discussions contain repeated complaints about jargon, formal/AI-flavored filler, overlong caveats, and unwanted follow-up offers. Some users report that short TL;DR/Outstanding rules or Custom Instructions helped. These are valuable experience reports, but they do not establish a universal template, author, or controlled improvement.

## Reusable recommendation

When the user wants one answer rather than a catalog, recommend this layered combination:

1. **Global expression layer:** built-in Concise or a short custom Output Style.
2. **Project layer:** a short CLAUDE.md/AGENTS.md containing project facts, commands, safety boundaries, and only a few communication rules.
3. **Delivery layer:** `Result / Changed / Verified / Remaining`, omitting empty sections.
4. **Task layer:** a Skill for rewriting technical content for a non-specialist or a specific stakeholder.
5. **Enforcement layer:** tests, lint, screenshots, Stop hooks, or other deterministic checks; do not use hooks as a semantic judge of whether prose “sounds human.”

For cross-agent use, keep the semantic contract tool-agnostic and put provider-specific adapters in each harness’s native layer. “Plain language” must not mean “omit caveats”: retain risks, errors, security warnings, and conditions that change the decision.

## Search and synthesis procedure

1. Start with a broad Perplexity Search query that explicitly asks for people, projects, mechanisms, adoption signals, original URLs, limitations, and a “not found” result when evidence is weak.
2. Use a same-thread WebBridge follow-up requesting a community-only delta; do not let the first official-doc answer silently stand in for community coverage.
3. Use `model_council`, `step_by_step`, or `deep_research` for model variety when the UI model selector is unreliable; label the mode as perspective diversity, not independent proof.
4. Inspect the original GitHub/official/HN/Reddit pages. A Perplexity answer score or source count is not source verification.
5. Record access date and snapshot metrics. Re-check volatile star/fork/install counts before reporting them.
6. State explicitly when no single person or ChatGPT-specific standard emerged. Absence of a canonical winner is a valid result.

## Pitfalls

- Do not equate “viral” with “good prose.” Caveman is the clearest counterexample: high adoption and strong compression focus, but potentially poor natural-language readability.
- Do not rank a person above a mechanism just because the person is famous in adjacent agent work.
- Do not call a repository “community consensus” from stars alone.
- Do not claim that a self-reported benchmark, install badge, or third-party directory count is an independent evaluation.
- Do not turn one Reddit/Hacker News experience into a guaranteed rule for all models, languages, or task types.
- Do not recommend a giant CLAUDE.md, Custom Instructions file, or all-in-one pack when a short layer-specific adapter solves the request.
