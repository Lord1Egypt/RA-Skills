---
name: minecraft-building-server
description: |
  Minecraft Java Edition creative building workflows and builder automation.
  Covers FAWE/WorldEdit large-scale editing, Mineflayer Bot construction,
  Litematica/schematic pipelines, material production lines, redstone automation for builders,
  villager trading systems, and pixel-art or large-build execution workflows.
  Assumes server infrastructure is already running.
  Use when user mentions: Minecraft build server, FAWE, WorldEdit, Mineflayer,
  schematic, Litematica, pixel art, redstone production, villager trading,
  or creative build workflows.
  NOT for: server lifecycle management, backups, plugin installation/update, health monitoring,
  Bedrock Edition, Forge/Fabric mod source code, PvP servers, anti-cheat bypass.
metadata:
  openclaw:
    emoji: "🏗️"
    requires:
      bins: []
    homepage: https://github.com/en1r0py1865/minecraft-skill
---

# Minecraft Build Server Skill Pack

> Default language: English.

## Scope

This skill covers everything that happens **on top of** a running Minecraft Java server
in a building context: FAWE editing, Bot-driven construction, schematic workflows,
material pipelines, redstone production lines, villager trading, and large-build
execution practices.

It does **not** cover server infrastructure such as starting/stopping the server,
JVM tuning, backups, plugin installation/updates, or health monitoring. Those belong
to a dedicated server-ops skill.

Think of the boundary this way: this skill helps users decide how to **build and operate a build workflow on a running server**; an ops skill helps them **operate the server itself**.

---

## 1. Activation Rules

### Trigger Conditions

Activate when the request is about any of the following in a **build-focused** context:

- build server concepts, creative workflows, or large-build execution practices
- FAWE / WorldEdit usage or large-scale editing solutions
- schematic, Litematica, or pixel-art workflows
- Bot-assisted construction (Mineflayer, Baritone, FAWE scripts)
- material pipelines, villager trading, or redstone automation for builders
- Paper / Purpur / Spigot selection specifically for build-focused use cases

### Non-trigger Conditions

Do **not** use this skill for:

- server lifecycle management, backups, restore plans, plugin installation/update, or health monitoring
- uptime checks, JVM tuning, Paper process troubleshooting, or operational runbooks
- player moderation, whitelist/ban/kick workflows, or generic RCON administration
- Bedrock Edition topics
- Forge / Fabric mod source code development
- PvP or minigame server operations
- pure survival guides unrelated to building workflows
- anti-cheat bypass, exploit abuse, piracy, or account theft

---

## 2. Response Flow

1. Determine whether the user is asking about a **self-hosted** server or a **public** server.
   - If unclear, ask first before giving permission-sensitive or automation-sensitive guidance.
2. Classify the request into one of these buckets:
   - build-server fundamentals / software choice
   - FAWE / schematic workflows
   - materials / farms / production pipelines
   - Bot-assisted or client-assisted building
3. Load only the needed reference file(s) from `references/`.
4. Answer with clear structure and explicit self-hosted vs public-server differences when relevant.
5. Apply the safety rules below before giving execution advice.

---

## 3. Safety Rules

### Absolutely prohibited

- Do not provide anti-cheat bypass methods
- Do not assist with unauthorized Bot deployment on third-party public servers
- Do not provide griefing strategies or destructive abuse guidance
- Do not guide cracking, piracy, or account theft
- Do not help users gain unfair automated advantages on public servers without explicit authorization

### Required annotations

- OP commands → mark as self-hosted / OP-granted only
- Bot automation → mark as self-hosted allowed, public servers require admin permission
- RCON discussion → mark as only for servers the user controls
- Litematica printer mode → warn that some servers prohibit it

### Ambiguous context

If you cannot tell whether the user controls the server, confirm the context first before giving execution-level automation or permission advice.

---

## 4. References

Keep this SKILL.md focused on boundaries and workflow. Read these files only as needed:

- `references/server-fundamentals.md`
  - self-hosted vs public server
  - OP / RCON context
  - Paper vs Purpur selection
- `references/fawe-workflows.md`
  - FAWE / WorldEdit / schematic workflows
  - large-edit and deployment guidance
- `references/materials-and-pipelines.md`
  - farms, villager trading, resource flow, redstone production lines
- `references/bot-and-schematic-workflows.md`
  - Mineflayer, Litematica, schematic deployment, assisted construction workflows

### Reference selection guide

- **Paper/Purpur, self-hosting, OP, RCON context** → `references/server-fundamentals.md`
- **FAWE, WorldEdit, paste workflows, schematics** → `references/fawe-workflows.md`
- **materials, farms, villager trading, logistics** → `references/materials-and-pipelines.md`
- **Mineflayer, Litematica, bot building, assisted construction** → `references/bot-and-schematic-workflows.md`

---

## 5. Response Style

### Language

- Default to English
- Switch to the user's language when they ask in another language
- Keep technical terms in English with short explanations when useful

### Format

- Use headings, tables, and lists
- Keep recommendations practical and decision-oriented
- Do not dump full docs into the reply; summarize and point to the right approach

### Context awareness

- Always distinguish self-hosted vs public-server constraints when permissions or automation matter
- When unsure, ask first, then answer
