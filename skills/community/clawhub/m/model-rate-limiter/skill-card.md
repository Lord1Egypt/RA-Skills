## Description: <br>
Helps an agent manage local model request rate limits using a workspace JSON state file with configurable enablement, request count, and time window settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mazhimin-123](https://clawhub.ai/user/mazhimin-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect and adjust a local rate-limit state file so model requests stay within a configured per-minute limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update a local workspace file named rate-limit-state.json. <br>
Mitigation: Use it only in workspaces where local persistent rate-limit settings are expected, and review the file before relying on its values. <br>
Risk: Broad Chinese trigger wording such as "限速" may activate the skill in conversations about rate limits. <br>
Mitigation: Confirm the requested rate-limit action before changing enablement, maxPerMinute, windowMs, or timestamps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mazhimin-123/model-rate-limiter) <br>
- [Publisher profile](https://clawhub.ai/user/mazhimin-123) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local workspace file named rate-limit-state.json for persistent rate-limit state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
