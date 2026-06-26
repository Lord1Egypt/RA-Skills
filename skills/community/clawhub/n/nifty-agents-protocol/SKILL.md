---
name: nifty-agents-protocol
version: "1.0.3"
license: MIT
description: A cryptographic protocol for AI agents to mint, sign, verify, and transfer SVG digital assets without a blockchain.
metadata:
  openclaw:
    requires:
      env: []
    files: ["index.ts", "server.ts", "package.json", "tsconfig.json"]
    homepage: "https://github.com/obekt/niftyagents"
---
# 💎 Nifty Agent SVG Protocol (NASP) - Agent Skill Manual

NASP is a cryptographic protocol for creating, signing, and trading SVGs with verifiable provenance—**without a blockchain.**

## 🎯 Objective
Use this skill to mint "Nifty" digital assets, verify their ownership, and securely transfer them to other agents using `did:key` identities.

## 🛠 Setup & Imports
To use this skill in your environment:
```typescript
import { 
  generateIdentity, 
  signSVG, 
  verifySVG, 
  transferSVG 
} from './index.js';
```

## 📋 Data Structures

### `AgentIdentity`
```typescript
{
  did: string;        // e.g. "did:key:z6Mk..."
  publicKey: Uint8Array;
  secretKey: Uint8Array;
}
```

### `VerificationResult`
```typescript
{
  isValid: boolean;     // Cryptographic integrity check
  creator: string;      // DID of the original minter
  currentOwner: string; // DID of the latest owner in the chain
  chain: string[];      // Array of DIDs representing the full history
}
```

## 🕹 Usage Guide

### 1. Generate an Identity
Call this once to create your agent's cryptographic persona. **Store the `secretKey` securely.**
```typescript
const myIdentity = generateIdentity();
```

### 2. Mint & Sign a New SVG
Takes a raw SVG string and returns a "Nifty" SVG with embedded NASP metadata.
```typescript
const rawSVG = `<svg>...</svg>`;
const signedSVG = await signSVG(rawSVG, myIdentity);
```

### 3. Verify an Asset
Always verify an SVG before accepting a trade or performing an action.
```typescript
const audit = await verifySVG(receivedSVG);
if (audit.isValid) {
  console.log(`Current Owner: ${audit.currentOwner}`);
}
```

### 4. Transfer Ownership
Appends a new signed grant to the metadata. This function **throws an error** if:
- The SVG is invalid/tampered.
- You (the signer) are not the `currentOwner` of the asset.
```typescript
const updatedSVG = await transferSVG(currentSVG, myIdentity, targetAgentDID);
```

## 🛡 Security Protocol for Agents
1.  **Canonicalization:** The library automatically handles canonicalization using `svgo`. Do not manually edit the SVG content after signing, or the signature will break.
2.  **Private Keys:** Never log, share, or expose your `secretKey`. Treat it as your agent's "soul."
3.  **Audit First:** Never assume an SVG is valid based on its filename. Always run `verifySVG()`.
4.  **Double Spend Detection:** In decentralized environments, if you are presented with two different valid chains for the same asset, the one with the **longest chain** or the **latest timestamp** is typically preferred.
