# 🚀 NiftyAgents: The Non-Blockchain NFT Protocol for AI Agents

**Digital Scarcity. Verifiable Provenance. Zero Gas.**

NiftyAgents is a lightweight, cryptographic protocol designed for the next era of commerce: **Agent-to-Agent (A2A) asset trading.** While humans use blockchains, agents use pure math.

## 🌟 Why NiftyAgents?

*   **No Blockchain Required:** Stop paying for gas. NiftyAgents uses Ed25519 signatures and SHA-256 hashing to secure ownership within the file itself.
*   **Self-Sovereign Identity:** Agents trade using `did:key` identifiers. No platform lock-in, no account registration.
*   **Ultra-Lightweight:** The cryptographic overhead is minimal. A Genesis Manifest adds only **~0.4 KB**, and each subsequent transfer adds just **~0.27 KB** to the SVG file size.
*   **Embedded Provenance:** Every asset carries its entire history (minting -> owner 1 -> owner 2) inside its `<metadata>`.
*   **Tamper-Proof:** Any visual change to the SVG (even 1 pixel) instantly invalidates the signature.
*   **Lightning Fast:** Transfers are as fast as a cryptographic signature—milliseconds, not minutes.

## 💡 The Agentic Economy: 5 Core Use Cases

NiftyAgents isn't just about "art"—it's a **Programmable Asset Layer** for autonomous systems:

1.  **🚀 Agent "Proof of Work" (PoW) Certificates:** 
    Agents issue signed SVG certificates upon task completion. Build a **verifiable reputation** that travels with your agent across any platform.
2.  **🔑 Dynamic Access Keys ("The Golden Ticket"):** 
    Transferable SVGs that act as **Cryptographic Tokens**. Want to grant another agent access to your private API or GPU cluster? Send them a signed "Key" SVG.
3.  **🎫 Agent-to-Agent Vouchers & Coupons:** 
    Mint and trade discount codes or credits. Create secondary markets for "GPU Time" or "Data Access" without a central clearinghouse.
4.  **🏗 Modular AI Blueprints:** 
    Represent complex neural architectures or logic flowcharts as signed SVGs. License your "Agent Brain" components to other agents securely.
5.  **🏅 Reputation Badges & Skill-Verify:** 
    Replace central profiles with a **Provenance Chain of Badges**. An agent's "Python Expert" badge is only valid if signed by a trusted "Validator Agent."

---

## 🛠 How it Works

1.  **Mint:** An agent creates an SVG and "canonicalizes" it to ensure a deterministic hash.
2.  **Sign:** The agent signs the hash with their private key. You can also inject **Custom Metadata** (like license terms or encrypted private claims).
3.  **Embed:** The signature, DID, and metadata are embedded as the "Genesis Manifest" in the `<metadata>` tag.
4.  **Transfer:** To trade, the current owner signs a "Grant of Ownership" to the buyer's DID. This grant is appended to the metadata.
5.  **Verify:** Any agent can re-canonicalize the SVG and walk the "Transfer Chain" to confirm who currently owns it.

## 📦 Getting Started

### Agents: How to consume this Skill
This repository contains a standardized `SKILL.md` file with YAML frontmatter. Tools like **OpenClaw** or **Claude Code** can ingest this repository directly to grant your agent the ability to mint and trade SVGs.

### Manual Setup
```bash
git clone https://github.com/obekt/niftyagents
npm install

# Run the test suite to verify cryptographic integrity
npm run test # (or npx tsx tests/suite.ts)
```

### Protocol Usage (TypeScript)
```typescript
import { signSVG, verifySVG, transferSVG } from 'nifty-agents-protocol';

// Verify the Genesis Artifact
const { isValid, currentOwner, metadata } = await verifySVG(genesisSVG);

if (isValid) {
  console.log(`Verified: ${metadata.artifactName}`);
  console.log(`Current Owner: ${currentOwner}`);
}
```

### 🌐 Standalone Verification Server (REST API)
Don't want to run Node.js in your agent loop? You can spin up the included verification server to validate SVGs via HTTP:
```bash
npx tsx server.ts
# Server runs on port 3000

# POST your SVG to the server
curl -X POST -H "Content-Type: image/svg+xml" --data-binary @genesis_artifact.svg http://localhost:3000/verify
```

## 🛡 Security & Hacks

*   **The "Double Spend" Fork:** Without a global ledger, if an agent sells an asset to Agent B and then sells an older saved copy to Agent C, the protocol creates two cryptographically valid, divergent chains (a fork). Agents rely on a central marketplace (or time-discovery) to determine which valid chain was registered first.
*   **Runtime Protection:** The core `nifty-agents-protocol` library uses a custom `safeJsonParse` reviver to strip dangerous keys (`__proto__`, `constructor`) from foreign SVGs, neutralizing Prototype Pollution injection attacks against your agent's Node.js runtime.
*   **Chain Integrity:** Tampering with the visual SVG content breaks the SHA-256 hash. Removing a previous owner from the JSON metadata breaks the Ed25519 signature chain. Both are instantly detected and blocked.
*   **Agent Silos:** Keys are stored in "Secret Vaults" (encrypted local files) and never shared.

---
*Built for the Autonomous Era by ObekT AI Works*
