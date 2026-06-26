## Description: <br>
Maintain persistent cross-session agent memory in the Mneme plain-text format for decisions, facts, preferences, gotchas, and goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Mneme to preserve durable project memory across sessions, including decisions, constraints, preferences, and lessons that future agent runs should recall. The skill is intended for local plaintext memory files and should not be used for secrets or sensitive personal or confidential data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mneme stores durable local project memory in plaintext .mneme files, which may persist decisions, preferences, facts, and project context across sessions. <br>
Mitigation: Review .mneme files like documentation and do not store secrets, credentials, personal data, or confidential material unless plaintext retention is intentional. <br>


## Reference(s): <br>
- [Mneme specification](https://github.com/casperkwok/mneme) <br>
- [ClawHub Mneme listing](https://clawhub.ai/casperkwok/mneme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with plaintext .mneme examples and optional shell commands for the bundled tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local .mneme files and the zero-dependency scripts/mneme_tool.py helper for spine, lint, and new-id operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
