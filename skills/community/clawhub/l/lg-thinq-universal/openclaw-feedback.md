# LG ThinQ Universal Skill — Improvement Notes

Developer-facing notes for improving the LG ThinQ universal integration and per-device SKILLs.

## What went well
- Automated device discovery and profile ingestion via setup.sh.
- Generated device control scripts with environment-driven device IDs (LG_DEVICE_ID).
- Script generation handled many profile properties (read-write) and a status endpoint.
- Security-conscious approach: env-based credentials, avoidance of embedding PAT in generated files.

## Issues and limitations encountered
- Template formatting pitfalls:
  - Initial KeyError: 'device_id' when formatting the CLI template due to missing placeholder in TEMPLATE.
  - Unterminated string literals in long generated help text causing syntax errors in lg_control.py until the template was corrected.
- File system and permissions edge cases:
  - Initial permission error running setup.sh; fixed by chmod +x.
- Cross-script dependencies and environment:
  - generate_control_script.py relied on the presence of LG_DEVICE_ID in the environment; ensured by injecting LG_DEVICE_ID in the format call.
  - Virtual environment context confusion between lg-thinq-universal and per-device skill directories.
- Path and references drift:
  - Generated per-device scripts needed to be aligned with SKILL.md workflow; some references files (skill-creation.md) became source of truth.
- Testing against live LG API requires valid PAT and reachable route; code paths should gracefully handle missing PAT (raise a clear error) and fallback to cached routes when possible.

## Concrete improvements to codify in SKILL.md
- [ ] Before API calls or file operations, explicitly call out the action and require user confirmation (ask_user) as per security mandates.
- [ ] Make setup.sh idempotent and clearly log what changes it makes, plus print a summary of discovered devices with IDs and types.
- [ ] Ensure generate_control_script.py accepts both profile JSON and environmental LG_DEVICE_ID in a robust way, with clear errors if missing.
- [ ] Improve error handling in generated scripts to return structured JSON with fields like success, status, error.
- [ ] Add a validation step in the skill: run python lg_control.py --help and python lg_control.py status and present their outputs to the user before proceeding.
- [ ] Add a dry-run mode to the generation script to preview the commands without executing API calls.
- [ ] Clarify how to handle multiple devices: distinct skill directories per device, with consistent SKILL.md templates.
- [ ] Include examples of common failure modes and recommended user prompts in SKILL.md.

## Suggested SKILL.md enhancements
- Include explicit troubleshooting section with common API errors (401 Unauthorized, 404 Device Not Found, route discovery failures) and remediation steps.
- Document security considerations for storing LG_DEVICE_ID and avoiding leakage of PAT.
- Provide templates for per-device SKILL.md with fields and example commands.

## Misc notes
- Consider adding unit tests for code generation to catch template formatting regressions.
- Maintain a changelog per device SKILL when significant updates are made.
