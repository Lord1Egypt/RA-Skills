# proofai

Cryptographic proof that AI thought before it answered. EU AI Act Article 12 compliant.

## VirusTotal Notice

This skill is flagged by VirusTotal because it:
- Handles Ed25519 cryptographic keys (by design)
- Calls external APIs (Polygon blockchain, Supabase)
- Anchors data on-chain (Polygon Amoy)

This is expected behavior for a blockchain compliance tool.
Review the source: https://github.com/proof-ai/proofai

## Tools

### proofai_certify
Certify an AI decision with cryptographic proof. Runs the full ProofAI pipeline: compress, execute AI, analyze cognitive graph, sign with Ed25519, bundle evidence, anchor to Polygon blockchain, and verify. Returns a blockchain-verified evidence bundle with Polygonscan URL.

**When to use:** When you need tamper-evident proof of an AI decision for compliance, audit, or legal purposes.

### proofai_log
Log an AI decision that already happened. Provide the original prompt and AI response — ProofAI signs it with Ed25519, bundles the evidence, and anchors the hash to Polygon. No AI execution needed.

**When to use:** When you want to retroactively certify an AI interaction that already occurred.

### proofai_verify
Verify an evidence bundle's integrity and blockchain anchoring. Checks data integrity, timestamp validity, ledger anchoring, and hash matching against EU AI Act requirements.

**When to use:** When you need to confirm a bundle hasn't been tampered with.

### proofai_polygonscan
Get the Polygonscan verification URL for a Polygon transaction hash. Anyone can independently verify the proof without an account.

**When to use:** When you need to share a verification link with a regulator, client, or auditor.

### proofai_monitor
Get post-market monitoring statistics for AI compliance (EU AI Act Article 72). Returns anomaly counts, risk distribution, human review stats, and overall compliance status for the last 30 days.

**When to use:** When you need a compliance health check of your AI system.

## Setup

```json
{
  "mcpServers": {
    "proofai": {
      "command": "npx",
      "args": ["-y", "@proofai/mcp-server"],
      "env": {
        "PROOFAI_API_KEY": "pk_live_xxx",
        "PROOFAI_ANON_KEY": "your-supabase-anon-key"
      }
    }
  }
}
```

## Links

- GitHub: https://github.com/proof-ai/proofai
- npm SDK: https://www.npmjs.com/package/@proofai/sdk
- Regulator Portal: https://proofai-ochre.vercel.app/regulator
