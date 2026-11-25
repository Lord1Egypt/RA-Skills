# Hashference for OpenClaw

Portable AgentSkill for using a person's own Hashference account with OpenClaw: secure setup, live model discovery, primary/fallback/delegated routes and troubleshooting.

## Install

Copy this whole directory to a skill location supported by your OpenClaw version, for example ~/.openclaw/skills/hashference-openclaw (personal) or YOUR_WORKSPACE/skills/hashference-openclaw (workspace). Start a new session or refresh skills as supported. Requires Python 3 and HTTPS; no pip/npm dependencies.

Ask: “Use hashference-openclaw to connect my own Hashference account without changing my current default.”

This is a skill, not a provider plugin or automatic installer. It contains no account credentials, miner, background job or automatic paid call. It uses the host installation's supported config/secret workflow.

## Example requests

- List all live Hashference model IDs with current prices.
- Add all tool-capable models, preserving primary and fallbacks.
- Set GLM 5.3 Flash Uncensored as my primary using masked key entry.
- Add an economical fallback for this agent.
- Fix Hashference showing only one model.
- Use Hashference for a subagent, not the main model.

## Version 1.0.1 security hardening

Catalog output is now stdout-only: --output has been removed rather than trying to maintain a blacklist of sensitive paths. The helper cannot create a missing configuration file. Path/symlink regressions and in-process CLI tests cover this boundary. See references/SECURITY.md for capabilities, limitations and the scanner findings addressed.

Install from ClawHub with: openclaw skills install @mpoletiek/hashference-provider --version 1.0.1

## Checks

~~~bash
python3 -m unittest discover -s tests -v
python3 scripts/catalog.py --input references/catalog-snapshot.json
python3 scripts/catalog.py --agents-only --format openclaw
~~~

Snapshot is historical; helper defaults to live discovery. See references/VERIFICATION.md for actual checks and untested scope.

## License and attribution

Independent OpenClaw-specific skill, MIT-0; no official endorsement implied. Complements the existing general skill https://hashference.com/skill.md (MIT or MIT-0). Uses public API/docs and setup lessons; see references/SOURCES.md. Installation is local, not public publication.
