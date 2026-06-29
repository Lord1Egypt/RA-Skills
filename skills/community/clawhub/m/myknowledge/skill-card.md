## Description: <br>
MyKnowledge helps agents create local knowledge bases, manage project documentation, track requirements, and organize personal knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codermoray](https://clawhub.ai/user/codermoray) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use MyKnowledge to maintain local Markdown/YAML knowledge bases, track requirement lifecycles, preserve project status, and optionally capture complex tasks from agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional hooks and auto-recording can inspect user messages and persist local task records. <br>
Mitigation: Review hook behavior before enabling it, keep auto_record disabled unless wanted, and periodically review or delete generated knowledge-base records. <br>
Risk: Recorded project notes may contain sensitive client data, credentials, or other private conversation details. <br>
Mitigation: Avoid storing secrets in recorded tasks, inspect exported knowledge bases before sharing, and delete sensitive records from the local Markdown/YAML files. <br>
Risk: Automatic update checks may conflict with environments that require no-network operation. <br>
Mitigation: Disable update checks in configuration when a no-network workflow is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codermoray/myknowledge) <br>
- [Publisher Profile](https://clawhub.ai/user/codermoray) <br>
- [README](README.md) <br>
- [Privacy Statement](PRIVACY.md) <br>
- [OpenClaw Hook Guide](hooks/openclaw/hook-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and YAML files with setup guidance and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local knowledge-base records, requirement documents, project status files, and optional platform hook configuration.] <br>

## Skill Version(s): <br>
1.4.89 (source: SKILL.md frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
