---
name: lyrashield
description: Review LyraShield release-assurance evidence through an OAuth-first MCP connection.
version: 0.1.0
license: MIT-0
metadata:
  category: security
  author: LyraShield AI
  source:
    repository: https://github.com/ecryptoguru/lyrashield-marketplace
    path: openclaw
    license_path: openclaw/LICENSE
  openclaw:
    requires:
      env:
        - LYRASHIELD_API_KEY
---

# LyraShield AI review skill

Use the LyraShield MCP connection to inspect release-assurance evidence, summarize current
issues, and explain pending approvals. Prefer read-only tools. Do not claim that a result is a
security guarantee or that all Vibe Security 50 controls were verified.

The skill is a community ClawHub listing. It is not an official OpenClaw channel. Link to
LyraShield dashboard evidence instead of
recreating dashboard UI or copying report contents into prompts.

Write actions require OAuth `lyrashield.write` plus the exact-argument approval gate.
