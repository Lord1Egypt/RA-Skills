## Description: <br>
Leveling overlay for OpenClaw Control UI (badge + XP + daily tip + level list + icons). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pureheart](https://clawhub.ai/user/pureheart) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users use this skill to add a local PondDepth progress badge, XP levels, tips, and skill-install guidance to the OpenClaw Control UI. It is intended for users who are comfortable running local install and uninstall commands that modify their OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow modifies the local OpenClaw UI assets and creates persistent scheduled jobs. <br>
Mitigation: Review the install script before running it, confirm the target OpenClaw paths, and inspect or remove the created cron jobs after installation or uninstall. <br>
Risk: The helper tasks read local activity and session-derived data to calculate XP and status indicators. <br>
Mitigation: Install only if that local activity processing is acceptable, and review the generated JSON files before exposing the Control UI to other users. <br>
Risk: The overlay can guide users toward ClawHub login and recommended skill installation actions. <br>
Mitigation: Treat install prompts as suggestions, verify each recommended skill separately, and run copied commands manually only after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pureheart/ponddepth-levels) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands plus local JavaScript, Python, and shell helper files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an OpenClaw Homebrew installation unless paths are overridden.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
