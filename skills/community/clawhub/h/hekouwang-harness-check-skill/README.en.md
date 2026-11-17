# hekouwang-harness-check-skill

**Simplified Chinese** · [中文 README](README.md)

> An evidence-driven Agent Skill for checking a Harness without confusing “the scripts ran” with “the task is complete.”

This is the standalone source repository for the Skill. It selects the right verification mode, calls the target repository’s existing Harness entry points, preserves exit codes and evidence, and reports automated checks separately from real-host smoke tests and human review.

## What it checks

- Working-tree, staged, and CI verification modes;
- Hooks, Safety Gates, Task Contracts, Episodes, observability, and failure ledgers;
- Positive and negative fixtures, drift detection, adapter checks, and documentation links;
- Explicit boundaries for Claude Code, Cursor, CodeBuddy, Codex, browsers, MCP side effects, and visual/content review.

The Skill is an orchestration layer. It does not copy or replace the target repository’s `.harness/` scripts and contracts. The first reference implementation is [hekouwang-content-agent](https://github.com/huiyonghkw/hekouwang-content-agent).

Product name proposal: **hekouwang Harness Doctor**, shortened to **Harness Doctor**. Product page: [hekouwang Harness Doctor — make every Harness provable](https://huiyonghkw.github.io/hekouwang-harness-check-skill/). It includes an interactive scorecard, evidence ledger, host matrix, domain profile, and downloadable JSON demo.

For a beginner-to-advanced introduction, open the [Chinese Guide site](https://huiyonghkw.github.io/hekouwang-harness-check-skill/guide/index.html?lang=zh). It maps the practical build sequence from `CLAUDE.md` and Skills through Hooks, Subagents, Evaluators, Context Reset, Sprint Contracts, failure ledgers, and independent acceptance evidence.

## Harness Scorecard

The repository also ships an evidence-weighted scorecard. It has 12 dimensions, hard caps, confidence, maturity bands, a host matrix, and machine-readable findings. It deliberately treats prose and keywords as weaker than executable checks, contracts, fixtures, and observed exit codes.

```bash
# Static scan, suitable for a web page or GIF data source
python3 harness_score.py /path/to/harness \
  --format json --output ./harness-scorecard.json

# Execute the target verifier before rendering the report
python3 harness_score.py /path/to/harness \
  --format markdown --mode working-tree --mode ci

# Live, color-aware terminal output for a ScreenStudio/product demo
python3 harness_score.py /path/to/harness \
  --profile content-agent \
  --mode working-tree --mode ci \
  --format terminal --live --color always

# Add the content-agent domain profile
python3 harness_score.py /path/to/harness \
  --profile content-agent --format json

# Compare a new report with an earlier JSON scorecard
python3 harness_score.py /path/to/harness \
  --baseline ./before-scorecard.json --format markdown
```

The score is not a test-count total. A missing safety boundary, negative regression, CI parity, or completion evidence contract activates a hard cap. A configured host is not the same as a real host smoke test; it remains `unknown` until there is explicit evidence.

`--format terminal --live` is the human-facing demo mode: live status is written to stderr while the final score, dimensions, exit codes, governance counts, and host boundary are rendered with color. JSON and Markdown remain machine-safe and contain no ANSI escape codes.

The product boundary is complementary to [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness): DeepSeek Harness is a plugin-based Agent Runtime, while this Skill is an independent acceptance and evidence layer for DeepSeek, Claude, Codex, Cursor, CodeBuddy, and custom Harness repositories. See [`references/market-positioning.md`](references/market-positioning.md).
The GIF storyboard and offline JSON fields for a future demo page are in [`references/demo-storyboard.md`](references/demo-storyboard.md).

## Seven product differentiators

1. **Independent acceptance** — audits any Harness instead of serving one model runtime.
2. **Evidence first** — file/line references, exit codes, positive and negative fixtures, and run records outrank README keywords.
3. **Hard gates** — missing safety enforcement, CI parity, negative regression, or completion evidence caps maturity automatically.
4. **State-aware** — separates `working-tree`, `staged`, and `ci` rather than treating local success as CI success.
5. **Cross-host** — checks Claude Code, Cursor, CodeBuddy, and Codex adapters; configured is not the same as triggered, so missing smoke evidence stays `unknown`.
6. **Domain governance** — the `content-agent` profile covers publication status, provenance, channel contracts, artifact boundaries, visual review, and external side effects.
7. **Visualizable loop** — JSON feeds a web page, GIF, CI artifact, and baseline comparison showing what changed after a fix.

Together these define the product boundary: a runtime makes an Agent run; Harness Check proves that its control plane and delivery boundary are trustworthy.

## Install into a Harness repository

From the target repository root:

```bash
git clone https://github.com/huiyonghkw/hekouwang-harness-check-skill.git \
  .agents/skills/hekouwang-harness-check-skill
```

The target repository must provide at least:

```text
.harness/scripts/verify.sh
.harness/scripts/harness-check.sh
.harness/tests/
```

The host project is responsible for creating its own Claude Code, Cursor, CodeBuddy, and Codex adapters. If it has a synchronization script, validate the links with:

```bash
bash .harness/scripts/sync-agent-adapters.sh --check
```

## Direct verification

```bash
bash .harness/scripts/verify.sh --working-tree
bash .harness/scripts/verify.sh --staged
bash .harness/scripts/verify.sh --ci
```

Use the modes precisely:

| Mode | Evidence | Allowed conclusion |
| --- | --- | --- |
| `working-tree` | Current machine, local Skill and Memory | Local automated checks passed or failed |
| `staged` | The staged change set | This staged change set passed or failed |
| `ci` | Repository fixtures and reproducible checks | CI automation passed or failed |

None of these modes proves that a real Agent host, editor, browser, platform publisher, or MCP side effect behaved correctly. Report those as separate smoke-test or human-review evidence.

## Reporting contract

Every report should include:

1. Mode, repository, and commit;
2. Exact command and exit status;
3. Passed checks, failures, and warnings, retaining original labels;
4. Runtime Governance count as observed in the log, never as a hard-coded score;
5. Real-host smoke-test status and human-review boundaries;
6. A reproducible next step for every failure.

Do not use `| head`, `|| true`, `--no-verify`, or fixed counts to manufacture a pass. A warning is not a pass, and a headless fixture is not a real-host smoke test.

## Repository layout

```text
SKILL.md                         Agent instructions and result protocol
agents/openai.yaml               OpenAI/Codex discovery metadata
references/check-matrix.md       Scope and count terminology
references/score-rubric.json     Weighted dimensions, caps, and maturity bands
references/scorecard-schema.json JSON output contract for web/GIF consumers
references/market-positioning.md Product boundary and DeepSeek comparison
references/demo-storyboard.md  GIF storyboard and web data contract
references/profiles/             Domain profiles; content-agent ships first
website/guide/index.html           Beginner-to-advanced Guide site
harness_score.py                 Standard-library scorecard CLI
tests/test_harness_score.py      Strong/weak fixture regression tests
assets/harness-check-flow.svg    Portable workflow diagram
README.md                        Chinese documentation
README.en.md                     English documentation
```

## Development

Changes to this repository should keep the Skill portable:

1. Keep project-specific facts in the target Harness, not in this repository;
2. Add a positive and a negative example when behavior changes;
3. Update `SKILL.md`, the check matrix, documentation, and the diagram when the protocol changes;
4. Run the package validation workflow and the full checks in a reference Harness;
5. Document what automation proves and what still needs a real host or human.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
