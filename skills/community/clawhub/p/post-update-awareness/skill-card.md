## Description: <br>
After an OpenClaw version change, read the CHANGELOG entry pinned to the installed version and surface user-relevant changes, including new tools, breaking changes, and optional native dependencies that may need verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussein1362](https://clawhub.ai/user/hussein1362) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill after OpenClaw updates to receive a concise, version-pinned summary of relevant release notes, plugin drift, optional dependency status, channel health, and configuration rewrite notices. It is intended for unattended or attended operational awareness without performing updates or configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local OpenClaw diagnostics and inspects plugin, channel, update-guard, and state-file information. <br>
Mitigation: Review the diagnostic scope before unattended use and run it in the intended OpenClaw profile so notices reflect the correct deployment. <br>
Risk: The skill may make an unauthenticated request to GitHub to fetch release notes for the installed OpenClaw version. <br>
Mitigation: Use the local changelog path when available; otherwise allow only the documented OpenClaw release-note endpoints if network egress is restricted. <br>
Risk: The skill writes a small per-profile state file so it can avoid repeating the same update notice. <br>
Mitigation: Keep the state directory profile-scoped and writable only by the OpenClaw user; deleting the file only causes the skill to re-baseline or re-notify. <br>
Risk: Plugin drift, stale config entries, missing optional dependencies, or unhealthy channels are reported but not fixed by this skill. <br>
Mitigation: Treat surfaced shell commands as guidance for a human or hand off to a maintenance skill that is explicitly scoped for mutations. <br>


## Reference(s): <br>
- [Post Update Awareness on ClawHub](https://clawhub.ai/hussein1362/post-update-awareness) <br>
- [Publisher profile](https://clawhub.ai/user/hussein1362) <br>
- [Post Update Maintenance companion skill](https://clawhub.ai/skills/post-update-maintenance) <br>
- [OpenClaw pinned changelog URL pattern](https://raw.githubusercontent.com/openclaw/openclaw/v<currentVersion>/CHANGELOG.md) <br>
- [OpenClaw GitHub Releases API tag URL pattern](https://api.github.com/repos/openclaw/openclaw/releases/tags/v<currentVersion>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown operational notice with short bullet buckets and inline shell commands when action is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hard cap of about 18 lines; empty buckets are omitted; state is persisted only after successful surfacing.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
