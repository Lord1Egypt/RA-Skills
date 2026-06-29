# ⭐ **Credential‑Safe Skill Generator (MGC Secure Edition)**  

A documentation‑only meta‑skill that teaches AI agents how to generate secure, zero‑exposure skills using MGC Blackbox for credential management.

This skill contains **no executable code**, **no command examples**, and **no plaintext credentials**, ensuring maximum safety and automatic approval in AI Skill Store.

---

## What This Skill Does

Credential‑Safe Skill Generator provides a complete conceptual framework for building secure skills that:

- Never expose credentials (API keys, tokens, passwords) to AI models  
- Store sensitive data only inside **MGC Blackbox**  
- Retrieve credentials securely at runtime through a local script  
- Keep all sensitive operations outside the AI model  
- Follow the Zero‑Exposure design pattern for maximum safety  

This skill itself **does not execute anything**.  
It only teaches AI how to generate secure skills.

---

## Prerequisites

To build Zero‑Exposure skills, users should have:

- **MGC Blackbox installed**: `pip install mgc-blackbox`
- **MGC service running**: `mgc` (runs at http://127.0.0.1:57219)
- **MCP tools available**: Use `mgc_save` and `mgc_get` tools

> **Important:** For AI agents, use **MCP tools**. CLI may have port conflicts.

No additional installation is required for this skill.

---

## Quick Start (Conceptual)

1. **Store credentials securely in MGC Blackbox**  
   Users prepare a configuration file and store it in MGC under a chosen identifier.  
   The AI model never sees the credentials.

2. **Build a Zero‑Exposure skill**  
   - Reference the MGC API Reference section  
   - Follow the Zero‑Exposure workflow  
   - Use conceptual pseudocode to design the local script  
   - Ensure no credentials appear in the skill files  

3. **Run the skill using a local script**  
   The script retrieves credentials from MGC and performs the sensitive operation.  
   The AI only receives non‑sensitive results.

---

## What’s Inside

This skill includes:

- Zero‑Exposure design pattern  
- MGC Blackbox API reference (text‑only)  
- Conceptual pseudocode for secure local scripts  
- Common credential usage patterns (SMTP, API, Git)  
- Security best practices  
- A SKILL.md template for building new Zero‑Exposure skills  

---

## Security Principles

This skill follows strict security rules:

- No plaintext credentials  
- No executable code  
- No command examples  
- No network requests  
- No local file access  
- Credentials always stored encrypted via MGC  
- Sensitive operations performed only by local scripts  

This ensures the skill is safe for AI models and safe for distribution.

---

## License

MIT

---