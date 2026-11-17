# Shopping Comparison

[Simplified Chinese guide](README.zh-CN.md)

Calculate purchase costs, compare saved price snapshots, preserve referral URLs and export reports.

## What it does

Calculate purchase costs, compare saved price snapshots, preserve referral URLs and export reports.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Compare the three washing-machine descriptions I provide by price, capacity, dimensions and warranty, marking missing data.
```

```text
Using my supplied product quotes and shipping costs, compare delivered prices against a CNY 3,000 budget and retain source links.
```

```text
Score these products against my requirements and export a comparison table with reasons.
```

## Exported files

comparison.md / comparison.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace. Current product-page and price research uses the browsing tools available to OpenClaw.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-shopping-compare
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-shopping-compare), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-shopping-compare
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-shopping-compare). Download the repository ZIP and copy `skills/mochi-shopping-compare` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
