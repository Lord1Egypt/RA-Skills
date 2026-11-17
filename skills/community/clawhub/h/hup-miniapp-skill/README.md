# hup-miniapp

An [OpenClaw](https://openclaw.ai) skill that teaches an agent to **build, test, and list Hup
mini apps** — web apps that run inside [Hup](https://hup.social) social posts and transact
through the viewer's existing Hup wallet session.

```bash
openclaw skills install hup-miniapp
```

## What the agent learns

- The Hup SDK bridge: `hup.ready()`, `hup.getProvider()`, session events — and the Farcaster
  Mini App compatible surface (`sdk.actions.ready()`, `sdk.wallet.getEthereumProvider()`), so
  existing Farcaster mini apps port with little or no change.
- The wallet policy the host enforces: which methods prompt, which proxy silently, and which are
  always refused (`eth_sign`, `eth_signTransaction`, `wallet_addEthereumChain`).
- The listing flow: onchain registration on the apps directory, moderator embed review, and why
  every listing edit pauses embedding until re-review.
- A diagnostic table for the common failures (no host, framing headers, origin mismatch, 4200/4100).

## Contents

| File | Purpose |
| --- | --- |
| `SKILL.md` | The skill — rules, workflow, minimal working core, diagnostics. |
| `references/miniapp-guide.md` | Snapshot of the canonical spec (live copy: https://hup.social/miniapp-skill.md). |
| `references/demo-app.html` | Complete working mini app: connect, sign, send, policy checks. |

The live spec at `https://hup.social/miniapp-skill.md` is always the source of truth; the skill
directs agents to fetch it before building.

## License

MIT
