# Penny Web Search Skill

Portable agent skill for using PennyAPI as a paid real-time web-search provider over x402.

## Install

Replace `ayoubsalem-spec` with your GitHub username after you publish this repository:

```bash
npx skills add ayoubsalem-spec/penny-web-search-skill --all --yes
```

## What it does

The skill teaches an agent to use:

`https://pennyregwatch.com/v1/search`

for current web research and verification.

Current advertised search price: **$0.004 USDC per call** on **Base** via **x402**.

## AgentCash

```bash
npx agentcash@latest check https://pennyregwatch.com/v1/search
npx agentcash@latest fetch https://pennyregwatch.com/v1/search -m POST -b '{"query":"latest x402 news","limit":5}'
```

To persist Penny in AgentCash:

```bash
npx agentcash@latest add https://pennyregwatch.com
```

## Important

This repository is only a distribution artifact. It does **not** modify the PennyAPI production runtime.
