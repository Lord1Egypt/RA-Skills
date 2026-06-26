## Description: <br>
Health Reasoner is a local, rule-based wellness habit scorer that uses sleep, diet, exercise, stress, smoking, and alcohol inputs to return a lifestyle score and improvement suggestions; it does not provide medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-feng123](https://clawhub.ai/user/chen-feng123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can run this local Python tool to assess everyday lifestyle habits and receive structured, rule-based suggestions for non-medical wellness improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake lifestyle scoring and wellness suggestions for medical diagnosis or treatment advice. <br>
Mitigation: Use the skill only for local wellness habit reflection and consult qualified medical professionals for health concerns. <br>
Risk: Input files and optional history files may contain sensitive personal health or lifestyle information. <br>
Mitigation: Keep inputs and history files private, avoid entering detailed medical history, and enable history only when local retention is intended. <br>
Risk: The artifact includes documentation mismatches around API mode and broader health fields. <br>
Mitigation: Prefer CLI, JSON input, and Python import workflows documented by the implemented code, and do not install Flask unless intentionally experimenting with the unfinished API path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chen-feng123/health-reasoner) <br>
- [API specification](API_SPEC.md) <br>
- [Use guide](USE_GUIDE.md) <br>
- [Design notes](references/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON objects or human-readable CLI text containing scores, risk level, risk factors, and suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally by deterministic Python rules and may include optional local history summaries when a history file is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
