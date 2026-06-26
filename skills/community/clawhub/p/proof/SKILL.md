---
name: proof
version: 2.0.0
description: >
  A local-first cryptographic toolkit. Executes zero-knowledge proof (ZKP) generation, 
  circuit compilation via SnarkJS/ZoKrates, and formal verification analysis on local files. 
  Requires local toolchains. No external API or cloud data transmission.
---

# PROOF 2.0: The Execution Layer

## I. System Capability
Proof is now a functional engine for local cryptographic operations. It interfaces with your local environment to provide mathematical certainty.

**Key Operations:**
- **`proof.zkp_gen`**: Compiles circuits and generates proofs locally.
- **`proof.formal_check`**: Runs static analysis and formal verification templates on code.
- **`proof.audit`**: Generates a cryptographic manifest for local project files.

## II. Local Environment Requirements
- Node.js & SnarkJS (ZKP)
- ZoKrates (optional)
- Python 3.10+ (glue scripts)

## III. Usage & Examples

**User:** "Generate a ZKP for this statement: x * y = 12."  
**Agent:** (Calls `scripts/zkp_tool.py`) -> "Compiling circuit... generating witness... proof.json created in \`~/.openclaw/workspace/proof/\`."

**User:** "Run a formal check on my Solidity contract."  
**Agent:** (Calls `scripts/verify_lib.py`) -> "Scanning for reentrancy and integer overflow... Result: PASS."

## IV. Security & Privacy
- Local-only computation  
- Workspace isolation (\`~/.openclaw/workspace/proof/\`)  
- No persistent daemons or background processes  
- No credentials requested or transmitted
