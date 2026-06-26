# Hermes Agent Install Notes

Recommended integration path:

1. Install the canonical repository on the machine where Hermes can run tools.
2. Add `platforms/hermes-agent/SKILL.md` as a Hermes skill.
3. Add `platforms/hermes-agent/SOUL.md` to the Hermes persona or project memory if supported.
4. Register `platforms/mcp-server/server.py` through the Hermes MCP configuration.
5. Run a test request that calls `preflight_check` before allowing workspace writes.

Do not enable automatic skill mutation on this adapter without a review step. Hermes may propose improved skills, but the founder or maintainer should approve the final patch.
