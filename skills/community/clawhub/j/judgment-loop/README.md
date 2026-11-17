<p align="center">
  <img src="assets/judgment-loop-hero.png" alt="Judgment Loop — evidence, counterevidence, verification, action" width="100%">
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> · <strong>English</strong>
</p>

<h1 align="center">Judgment Loop</h1>

<p align="center"><strong>The missing step between thinking and acting.</strong></p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT-0" src="https://img.shields.io/badge/license-MIT--0-F2C94C.svg"></a>
  <a href="https://skills.sh/sirsws/judgment-loop"><img alt="skills.sh installs" src="https://skills.sh/b/sirsws/judgment-loop"></a>
  <img alt="Version 1.1.2" src="https://img.shields.io/badge/version-1.1.2-2563EB.svg">
</p>

Judgment Loop is an open Agent Skill for consequential choices, uncertain claims, recurring failures, serious learning, and evidence-based review. It turns vague confidence into a provisional judgment, a discriminating test, and an action the user still owns.

It is not a prompt that makes an AI sound deeper. It is a guardrail against answering the wrong question beautifully.

## See the difference in 30 seconds

**Ask an agent**

> A volunteer workshop received excellent satisfaction scores. Should we roll it out to the whole company?

**A fluent answer may optimize the proxy**

> The pilot was popular, so prepare the company-wide rollout.

That treats participant satisfaction as proof that the program improves the outcome it was created for.

**Judgment Loop changes the job**

- **Provisional judgment:** do not scale yet; run one representative follow-up pilot.
- **Real target:** improve cross-team handoffs, not attendance or satisfaction scores.
- **Verified fact:** volunteers rated the first workshop highly.
- **Untested hypothesis:** ordinary teams will change behavior after the workshop.
- **Strongest failure:** self-selected volunteers may not represent the rollout population.
- **Cheapest test:** predeclare one handoff outcome and a stop condition for a second team.
- **Stop or expand:** scale only if the target outcome improves without unacceptable cost.

Try the same question after installation:

```text
$judgment-loop A volunteer workshop received excellent satisfaction scores. Should we roll it out to the whole company?
```
## Why it exists

AI can produce a coherent answer before a person has identified the real target. That creates four common failures:

- proxy metrics improve while reality does not;
- an attractive plan becomes part of the user's identity;
- elegant explanations outrun evidence;
- the AI completes the cognitive work, leaving no user-owned judgment or action.

Judgment Loop interrupts that pattern without turning every task into a ceremony.

## Five modes

| Mode | Use it for | Core move |
|---|---|---|
| **Quick** | A vague problem or solution attachment | Real target → strongest failure → cheapest action |
| **Decision** | Costly or hard-to-reverse choices | Downside, reversibility, key assumption, guardrail |
| **Research** | Papers, reports, data and causal claims | Claim, evidence, boundary, strongest alternative |
| **Learning** | Understanding that must transfer | Reconstruction, boundary, transfer, recall |
| **Review** | Work that has produced real results | Original target, observed result, prediction gap, update |

## Install

### skills.sh / universal skills CLI

```bash
npx skills add sirsws/judgment-loop
```

Install only this skill for Codex:

```bash
npx skills add sirsws/judgment-loop --skill judgment-loop -g -a codex -y
```

### ClawHub / OpenClaw

```bash
clawhub install judgment-loop
```

### Manual

Copy the repository folder into your agent's skill directory. For Codex, the global location is `~/.codex/skills/judgment-loop/`.

## Use

Explicit invocation:

```text
$judgment-loop Should I publish this now, or keep improving it?
```

The skill also supports implicit activation when meaningful consequences and uncertainty coexist. It deliberately stays out of simple facts, clear execution, low-risk reversible tasks, freeform creation, and emotional companionship alone.

## What a good run produces

```text
Provisional judgment
    ↓
Real target and ownership
    ↓
Load-bearing assumption
    ↓
Strongest failure reason
    ↓
Cheapest discriminating test
    ↓
User-owned action and review trigger
```

Use only the moves that change the judgment. The loop is intentionally open: action closes; belief remains updateable.

## Examples and evaluation

See [examples](examples/README.md) for behavioral contrasts. They are deliberately separate from the single-source [cross-domain evaluation manifest](evals/cases.json).

The [reviewed evaluation protocol](evals/trigger-cases.md) scores activation depth, mode selection, evidence updates, missing cases, and error severity separately. The current version has no claimed behavioral baseline until a raw-output-preserving, independently reviewed run is completed.

## Design principles

1. **User sovereignty** — the model does not make value choices for the user.
2. **Evidence before elegance** — clear labels separate facts, inferences, and hypotheses.
3. **Strongest failure first** — the loop looks for the load-bearing weakness, not decorative balance.
4. **Cheap falsification** — test competing explanations before adding process.
5. **Action closed, cognition open** — decide when necessary, remain updateable.
6. **Proportionality** — a small reversible task should stay small.

## Language

The runtime skill is written in English for broad agent compatibility and instructs the agent to answer in the user's language. A maintained Chinese reference translation is available under [`translations/zh-CN`](translations/zh-CN/).

## Repository map

```text
SKILL.md                  Runtime entrypoint
references/              Decision, research, learning, and review modes
agents/openai.yaml       Codex interface and implicit invocation policy
examples/                Realistic usage examples
evals/                   Cross-domain manifest and reviewed scoring protocol
translations/zh-CN/      Chinese reference translation
assets/                  Project visual assets
```

## License

[MIT-0](LICENSE). Use, modify, redistribute, and commercialize without attribution requirements.
