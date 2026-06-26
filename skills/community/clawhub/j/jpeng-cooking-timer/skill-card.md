## Description: <br>
Kitchen cooking timer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate cooking-related timer tasks and receive JSON-formatted results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for TIMER_API_KEY without identifying the API provider or explaining why the key is needed. <br>
Mitigation: Do not use a real key until the publisher documents the provider, scope, and handling requirements. <br>
Risk: The documented command calls scripts/cooking_timer.py, but that script is not included in the artifact evidence. <br>
Mitigation: Review the actual script before running the command and install only a release that includes the expected file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-cooking-timer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIMER_API_KEY according to the skill text; the referenced cooking_timer.py script is not present in the artifact evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
