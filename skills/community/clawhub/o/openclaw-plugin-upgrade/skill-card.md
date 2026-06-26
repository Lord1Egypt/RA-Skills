## Description: <br>
Helps agents upgrade OpenClaw plugins, including general npm-based plugins and the QQ bot plugin, by running a bundled upgrade script with version targeting, file verification, compatibility handling, rollback, and optional gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upgrade installed OpenClaw plugins from npm packages and report the resulting plugin version and status. It is especially tailored for @tencent-connect/openclaw-qqbot upgrades that need file checks, legacy directory cleanup, and OpenClaw 3.23+ configuration compatibility handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upgrade script can install npm packages, remove legacy plugin directories, execute plugin postinstall code, and restart the gateway. <br>
Mitigation: Use only trusted OpenClaw plugins and confirm the package name, plugin ID, target version, cleanup directories, and restart behavior before execution. <br>
Risk: Untrusted or typo-prone package names may install unintended code. <br>
Mitigation: Confirm the exact npm package name and avoid untrusted package sources. <br>
Risk: Custom legacy directory values can cause unintended cleanup. <br>
Mitigation: Pass legacy directory names only after verifying they are simple plugin directory names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/openclaw-plugin-upgrade) <br>
- [Publisher profile](https://clawhub.ai/user/ryanlee-gemini) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script output includes fields such as PLUGIN_NEW_VERSION, PLUGIN_ID, and PLUGIN_REPORT for agent-facing summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
