# Getting Started

You need an x402-capable client with a funded wallet. AgentCash is one supported path.

Check wallet balance:

```bash
npx agentcash@latest balance
```

Discover Penny:

```bash
npx agentcash@latest discover https://pennyregwatch.com
```

Inspect the paid search endpoint:

```bash
npx agentcash@latest check https://pennyregwatch.com/v1/search
```

Run a search:

```bash
npx agentcash@latest fetch https://pennyregwatch.com/v1/search -m POST -b '{"query":"current AI agent commerce news","limit":5}'
```

Do not use controlled/self-payments as evidence of unrelated customer demand.
