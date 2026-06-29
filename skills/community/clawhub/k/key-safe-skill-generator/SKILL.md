---

spec: usk/3.0
id: key_safe_skill_generator
version: 1.0.1
name: Key‑Safe Skill Generator
description: A documentation‑only meta‑skill that teaches AI agents how to generate secure, zero‑exposure skills using MGC Blackbox for credential management. Contains no executable code.
author: MirginCipher Team
license: MIT
tags: zero-exposure, mgc, security, credential-management, skill-generator, meta-skill
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.0.1
    changes:
      - Updated to emphasize MCP tools over CLI
  - version: 1.0.0
    changes:
      - Initial release with conceptual workflow and USK v3 structure

---

# Overview

Key‑Safe Skill Generator is a **meta‑skill** that teaches AI agents how to generate secure skills that interact with external services requiring credentials (email, APIs, tokens, SSH keys, etc.).  
It provides a **design pattern**, **structural templates**, and **conceptual workflows** for building skills that never expose secrets to AI models.

This skill contains **no executable code** and is safe for automatic approval.

---

# What This Skill Enables

After reading this documentation, an AI agent will understand how to:

- Build new skills that interact with external services **without exposing credentials**  
- Use **MGC Blackbox** as the secure storage and runtime provider  
- Structure a Zero‑Exposure skill using **USK v3 conventions**  
- Guide users to prepare and store credentials safely  
- Generate a complete skill package (SKILL.md + README + local script)  
- Ensure all sensitive operations happen **outside the AI model**

---

# Why Zero‑Exposure Matters

Traditional skills often embed credentials in:

- Code  
- Environment variables  
- Prompts  
- Logs  
- AI-visible memory  

Zero‑Exposure skills avoid this entirely:

- Credentials are stored only in **MGC Blackbox**  
- AI never receives or processes secrets  
- Local scripts retrieve credentials securely  
- All sensitive operations run outside the model  
- The AI only orchestrates logic, not secrets  

---

# Prerequisites for Zero‑Exposure Skills

To build a Zero‑Exposure skill, users must:

1. Install MGC Blackbox: `pip install mgc-blackbox`
2. Start the MGC service: `mgc` (runs at http://127.0.0.1:57219)
3. Use **MCP tools** (`mgc_save`, `mgc_get`) for credential management
4. Store credentials in MGC under a chosen identifier
5. Use a local script to retrieve credentials and perform sensitive operations

> **Important:** For AI agents, use **MCP tools** (`mgc_save`, `mgc_get`). CLI may have port conflicts in some environments.  

---

# Zero‑Exposure Workflow (Conceptual)

A Zero‑Exposure skill follows this pattern:

1. **User stores credentials in MGC**  
   Example identifiers: smtp_config, slack_bot_token, github_token.

2. **Skill references the identifier**  
   The AI never sees the actual credentials.

3. **Local script retrieves credentials from MGC**  
   The script communicates with the local MGC service to fetch encrypted content.

4. **Local script performs the sensitive operation**  
   Examples: sending email, calling an API, pushing to Git.

5. **AI receives only the result**  
   No secrets are ever exposed.

---

# How to Build a Zero‑Exposure Skill

A typical Zero‑Exposure skill package contains:

```
your_skill/
  SKILL.md
  README.md
  local_script
```

## 1. SKILL.md (USK v3)

Should describe:

- Purpose  
- Required user setup  
- Credential identifier  
- Tool interface (if any)  
- Safety considerations  
- Zero‑Exposure design principles  

## 2. README.md

Should explain:

- How to install MGC  
- How to store credentials  
- How to run the local script  
- How the Zero‑Exposure pattern works  

## 3. Local Script (Conceptual)

The script should:

- Retrieve credentials from MGC  
- Perform the sensitive operation  
- Return only non‑sensitive results  

The script must **never** print or expose secrets.

---

# MGC Blackbox API Reference (Text‑Only)

This section provides the technical details needed to interact with MGC Blackbox.  
All information is text‑only and not executable.

## Service Endpoint

- Base URL: http://127.0.0.1:57219
- Token File: ~/.mgc/database/mgc_black_box/.mgc_token
- Token: A string token read from the token file, required for all API calls  

## Get Credentials API

Retrieve stored credentials from MGC Blackbox.

**Endpoint:** /api/mgc/sensitive/get  
**Method:** POST  
**Headers:**  
- X-MGC-Token: (string token read from ~/.mgc/database/mgc_black_box/.mgc_token)  
- Content-Type: application/json  

**Body fields:**  
- info_type: type of stored data (e.g., “config”)  
- info_owner: identifier chosen by the user  

**Response fields:**  
- code: status code  
- msg: status message  
- data.content: JSON string containing the stored configuration  

## Save Credentials API

Store credentials in MGC Blackbox.

**Endpoint:** /api/mgc/sensitive/save  
**Method:** POST  
**Headers:** same as above  

**Body fields:**  
- info_type  
- info_owner  
- content: JSON string representing the stored configuration  

---

# Conceptual Pseudocode (Non‑Executable)

A local script should follow this conceptual flow:

- Read the MGC token from the local environment  
- Construct a request containing the credential identifier  
- Send the request to the MGC sensitive‑data endpoint  
- Parse the returned configuration  
- Use the configuration to perform the sensitive operation  
- Return only non‑sensitive results to the AI  

---

# Common Zero‑Exposure Patterns

## Email Sender

- User stores SMTP credentials in MGC  
- Local script retrieves them  
- Script sends email  
- AI provides only subject/body/recipient  

## API Client

- User stores API key in MGC  
- Local script retrieves it  
- Script performs authenticated request  
- AI provides endpoint and payload  

## Git Automation

- User stores GitHub token in MGC  
- Local script retrieves it  
- Script performs push/pull/commit  
- AI provides commit message  

---

# Safety

This skill:

- Contains **no executable code**  
- Does not perform network requests  
- Does not access local files  
- Does not interact with external services  
- Does not process or store credentials  
- Provides only conceptual guidance  

---

# Entrypoint

This skill has **no runtime entrypoint**.  
It is a documentation‑only instructional skill.

---