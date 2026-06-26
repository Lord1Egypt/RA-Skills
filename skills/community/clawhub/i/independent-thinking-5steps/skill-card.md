## Description: <br>
Guides agents through a five-step independent thinking workflow for architecture discussions, troubleshooting, retrospectives, decisions, and uncertain knowledge checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to structure deeper reasoning before responding or acting in architecture discussions, troubleshooting, retrospectives, decisions, and uncertain knowledge work. The workflow emphasizes self-checks against local vector and wiki knowledge before action and during review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents toward broad private-memory lookup and mandatory wiki persistence without clear user control. <br>
Mitigation: Install only when the local vector script and wiki/vector stores are trusted, and require explicit user approval for vector searches and wiki writes. <br>
Risk: The skill tells agents to disable the system Memory Search and rely on a dedicated local vector system. <br>
Mitigation: Review and edit this behavior before deployment so memory controls, storage location, retention, deletion, and review procedures are documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markma84/independent-thinking-5steps) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to the referenced local vector script and wiki/vector stores when the workflow is followed.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
