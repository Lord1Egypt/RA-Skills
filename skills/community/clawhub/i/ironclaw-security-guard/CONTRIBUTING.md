# Contributing

Thanks for improving `ironclaw-security-guard`.

## Good contributions

- safer detection rules with low false-positive risk
- better audit messages and operator guidance
- clearer docs for deployment and configuration
- examples that show why a call was blocked or redacted

## Before you open a PR

1. Keep blocking rules explainable and reviewable.
2. Prefer narrow, testable rule changes over giant heuristic jumps.
3. Update both [README.md](./README.md) and [README.zh-CN.md](./README.zh-CN.md) when public behavior changes.
4. Update [CHANGELOG.md](./CHANGELOG.md) for notable user-visible upgrades.
5. Run `npm test` before opening a PR.

## Review expectations

- describe the threat or failure mode
- explain expected operator impact
- mention false-positive tradeoffs if relevant
- include the `npm test` result when rule behavior changed
