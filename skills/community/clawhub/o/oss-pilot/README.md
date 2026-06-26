# OSS Pilot

I'm a PM, not an engineer.

My first PR on [OpenClaw](https://github.com/openclaw/openclaw) (329K+ stars) started the same way -- I hit a bug that affected me, fixed it with Claude Code, and submitted a PR. It got merged. Then I did it again. And again.

After the third one I thought: can this whole process be automated?

Inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch), I built this -- a set of skills that handle the entire open-source contribution lifecycle. It finds issues, implements fixes, opens PRs, handles bot reviews, learns from each contribution, and gets better over time.

Every feature exists because I hit a real wall doing it manually.

Built by [@Cypherm](https://github.com/Cypherm)

---

## What It Does

```
discover ---> auto ---> pr ---> check ---> retrospective
   ^                   ^       |              |
   |                   +-------+              v
   |              (review loop)          profile grows
   |                                    (lessons, patterns)
   +---- learns from history ---------------+
```

| Skill | What it does | When to use |
|-------|-------------|-------------|
| **discover** | Find high-value issues with highest merge probability | "What should I work on?" |
| **auto** | Issue -> implemented, reviewed, bot-responded, maintainer-pinged PR | "Fix this issue end-to-end" |
| **pr** | Quality gate: root cause analysis, description, bot strategy | "Is this PR ready?" |
| **check** | Monitor CI, bot comments, stale status, take action | "What needs attention today?" |

## Results

**OpenClaw** (329K+ stars) -- 3 merged PRs:

| PR | What | Shipped |
|----|------|---------|
| [#35474](https://github.com/openclaw/openclaw/pull/35474) | Show status reaction during context compaction | v3.13 |
| [#48842](https://github.com/openclaw/openclaw/pull/48842) | Support custom apiRoot for Telegram alternative API endpoints | v3.22 |
| [#55922](https://github.com/openclaw/openclaw/pull/55922) | Fix anthropic service_tier injection for OAuth auth | v3.29 |

## Install

```bash
# Via ClawHub (recommended)
npx clawhub@latest install oss-pilot

# Or manually
git clone https://github.com/Cypherm/oss-pilot.git ~/.claude/skills/oss-pilot
```

## Quick Start

```bash
# 0. Make sure gh CLI is authenticated
gh auth status

# 1. Find something to work on
> oss discover https://github.com/some-org/some-repo
# (First run auto-creates a profile and forks the repo for you)

# 2. Fix an issue end-to-end
> oss auto some-repo #12345

# 3. Check your pending PRs next morning
> oss check
```

On first run, the system creates a **profile** for each repo -- a living document that captures build commands, maintainer styles, bot behavior, and lessons learned. See `_template.md` for the schema and `example.md` for what a mature profile looks like after weeks of contributions.

## How It Works

### The Learning Loop

Every PR goes through this cycle:

1. **Discover** finds issues by scanning 8 sources (bounty labels -> bugs -> CI failures -> codebase cleanup), checking repo openness, issue velocity, and competition
2. **Auto** implements the fix: reads code, traces root cause, writes tests, opens PR, responds to bots, pings maintainer
3. **PR** validates quality: root cause at the right layer? Description matches diff? Bot comments all answered?
4. **Check** monitors daily: CI status, new reviews, stale pings. When a PR is merged or closed, runs a **retrospective** -- writes the outcome and lessons back to the profile
5. Next time **Discover** runs, it uses the profile to make better choices and checks archived PRs to avoid past mistakes

### What Makes It Different

- **Profile system**: Each repo builds institutional knowledge over time. Your 10th PR is informed by lessons from your 1st
- **Competition check**: Two-level (issue + code) to avoid wasting time on crowded issues
- **Repo openness check**: Measures external contributor merge rate before you invest hours
- **Velocity check**: Detects fast-moving repos where issues get claimed in hours
- **Version/comment intelligence**: Reads issue comments and release notes to avoid working on already-fixed bugs
- **Maintenance**: Auto-prunes stale lessons and old context files

## Security Model

This skill instructs the agent to run build, lint, and test commands (e.g., `pnpm install`, `make`, `cargo test`) from the target repository. This is inherent to contribution automation -- you cannot validate a fix without running the repo's toolchain.

**Threat surface**: If the target repo contains malicious build scripts (e.g., postinstall hooks), those commands execute on your machine. This is the same risk as manually cloning a repo and running `npm install`.

**How risk is managed**:
- **User trust boundary**: You choose which repo to target. The skill never picks repos autonomously.
- **Runtime gating**: OpenClaw's exec approval system prompts before executing shell commands. The skill issues instructions; the runtime decides whether to run them.
- **Scope checkpoint**: The skill stops and asks before committing to changes >5 files or >200 lines.

**Recommended hardening**:
- Run inside a container (`openclaw --container <name>`) or VM when targeting unfamiliar repos.
- Review the repo's `package.json` scripts / `Makefile` targets before first run.
- Use a dedicated GitHub account for automation if you prefer isolation.

## File Structure

```
oss-pilot/
+-- SKILL.md          # Entry point -- routing + quick start
+-- discover.md       # Issue discovery (8 sources + scoring + verification)
+-- auto.md           # End-to-end PR automation (orchestrator)
+-- pr.md             # PR quality validation (root cause + description + bot strategy)
+-- check.md          # Daily monitoring + retrospective + maintenance
+-- _template.md      # Profile template for new repos
+-- example.md        # Real profile from 2+ months of contributions (anonymized)
```

## Built From Real Contributions

Every feature exists because I hit a real problem:

- **Velocity check** -> Added after issues got claimed within hours
- **Version check** -> Added after investigating an issue already fixed in a newer release
- **Comment intelligence** -> Added after missing a comment that said "likely fixed in next version"
- **First PR rules** -> Added after attempting a core infrastructure fix on first contribution
- **Repo openness check** -> Added after investing time on a repo that merges <10% external PRs
- **Staleness decay** -> Added after chasing a maintainer-filed issue that was 30+ days stale
- **Scope checkpoint** -> Added after wasting effort on a PR that got rejected for touching too many files

## Prerequisites

- [OpenClaw](https://openclaw.ai) or [Claude Code](https://claude.ai/code) installed
- `gh` CLI authenticated (`gh auth status`)
- A GitHub account

## Language Support

Tested on TypeScript, Python, and Go repos.

## License

[MIT](LICENSE)
