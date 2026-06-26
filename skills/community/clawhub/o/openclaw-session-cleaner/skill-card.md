## Description: <br>
OpenClaw session cleanup assistant for cleaning old session files, rebuilding sessions.json, and addressing session-file growth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccc-3po](https://clawhub.ai/user/ccc-3po) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to inspect session storage, clean old session files, and rebuild sessions.json when session files grow too large. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may delete sensitive OpenClaw session files or rewrite sessions.json without enough safeguards. <br>
Mitigation: Confirm the exact sessions path, make a backup, request a dry run or preview, and manually approve any deletion or sessions.json rewrite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccc-3po/openclaw-session-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/ccc-3po) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets local OpenClaw session files and sessions.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
