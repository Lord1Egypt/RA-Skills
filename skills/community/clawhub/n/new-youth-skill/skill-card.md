## Description: <br>
New Youth.skill provides a reflective critical-thinking persona based on Chen Duxiu's six standards from A Call to Youth for self-assessment, decision support, viewpoint review, daily practice, perspective expansion, and action planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for reflective self-assessment, critical-thinking prompts, decision support, viewpoint review, daily action planning, perspective expansion, and converting ideas into action steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The session-start hook can automatically introduce the New Youth persona into new sessions and influence ordinary conversations. <br>
Mitigation: Install only when that reflective posture is desired, disable the session-start hook where possible, or limit activation to explicit commands such as /新青年. <br>
Risk: Capability tags include crypto and purchase-related labels even though the reviewed artifacts do not require financial, wallet, purchase, or broad tool permissions. <br>
Mitigation: Do not grant financial, purchase, wallet, or broader tool permissions based on those metadata tags; keep runtime permissions limited to the artifact's documented needs. <br>
Risk: The skill uses a worldview and persona framework that may shape how options are framed during reflection or decision support. <br>
Mitigation: Use the skill as a questioning and self-assessment aid, keep final decisions with the user, and independently verify factual claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/moroiser/new-youth-skill) <br>
- [README](README.md) <br>
- [Six Standards: Full Commentary](references/six-standards.md) <br>
- [Five-Layer Persona Architecture](references/persona-layer.md) <br>
- [Application Scenario Examples](references/application-cases.md) <br>
- [Historical Narratives](references/historical-narratives.md) <br>
- [30 Classic Quotes](references/30-classic-quotes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown prose with optional command snippets and plain-text helper-script reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional helper scripts can produce scoring reports and daily task lists; no external APIs are required by the artifact.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata; artifact frontmatter/package.json report 1.0/1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
