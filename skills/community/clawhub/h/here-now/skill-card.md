## Description: <br>
here.now lets agents publish websites and store private files in cloud Drives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamludwin](https://clawhub.ai/user/adamludwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish websites, static files, and media to live here.now URLs, and to store or share private cloud Drive files across sessions and tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send files, private context, code, or credentials-related content to here.now for persistent cloud storage or web publishing. <br>
Mitigation: Use it only for content the user intentionally wants uploaded, stored remotely, shared with agents, or published on the web. <br>
Risk: API keys and publish state may persist locally, and shared Drive tokens may grant access beyond the intended task. <br>
Mitigation: Store credentials with restrictive permissions, avoid command-line API key flags in interactive use, prefer narrow Drive token path prefixes and short TTLs, and revoke tokens when no longer needed. <br>


## Reference(s): <br>
- [here.now documentation](https://here.now/docs) <br>
- [Site access control documentation](https://here.now/docs#access-control) <br>
- [ClawHub skill page](https://clawhub.ai/adamludwin/here-now) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, API responses, live URLs, and local or cloud file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update remote hosted Sites, private Drive files, scoped Drive share tokens, and local here.now credential or state files.] <br>

## Skill Version(s): <br>
1.16.0 (source: server evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
