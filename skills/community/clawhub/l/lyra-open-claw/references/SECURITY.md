# SECURITY — lyra-open-claw (public)

## Non-negotiables

- **No secrets in package** — no API keys, Discord tokens, wallet private keys, PATs.
- **No auto publish** — git / HF / ClawHub / social remain human-gated.
- **P0 before external actions** — social post, browser write, token launch.
- **Runtime-only credentials** — operator supplies keys at run time from local vault.
- **Memory hygiene** — never grow secrets into LYRA 3-Brain or public feeds.

## SkillSpector stance

This public skill is documentation + install map. Host OpenClaw/LYRA runtimes may have network and shell; those are outside this package and remain operator-controlled.
