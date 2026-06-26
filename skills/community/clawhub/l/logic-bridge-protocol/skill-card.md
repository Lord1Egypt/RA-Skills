## Description: <br>
Validates vague product requirements and user stories against five closure rules, returning follow-up questions when incomplete or FileEditor-ready JSON tasks when ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoelaine80-boop](https://clawhub.ai/user/zhaoelaine80-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Non-technical builders, product collaborators, and coding-agent users use this skill to turn vague product ideas or user stories into closed requirements before implementation. It can ask bilingual follow-up questions or produce a structured task brief for downstream file-editing agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated task briefs may include private product details or user-provided sensitive information. <br>
Mitigation: Avoid entering secrets or private business details unless they are intended to appear in the generated brief. <br>
Risk: Downstream file-editing tasks may be applied without sufficient review. <br>
Mitigation: Review any generated FileEditor task before allowing another agent to write or modify files. <br>
Risk: The requirement checker is heuristic and may reject concise but valid requirements. <br>
Mitigation: Treat follow-up questions as review guidance and tune the regex checks for the target domain when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoelaine80-boop/logic-bridge-protocol) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhaoelaine80-boop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON with status, message, follow-up questions, or FileEditor task instructions for a Markdown brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bilingual English/Chinese follow-up questions and a sha256 digest of accepted input for traceability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
