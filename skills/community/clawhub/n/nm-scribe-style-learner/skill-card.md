## Description: <br>
Extracts writing style patterns from exemplar text into a reusable profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze writing samples, extract style metrics and representative exemplars, and create a reusable profile for consistent generation or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad style, voice, tone, and exemplar triggers may activate the skill during general writing requests. <br>
Mitigation: Confirm the user wants style learning before collecting exemplars or generating a profile. <br>
Risk: Exemplar text may include sensitive or proprietary writing samples. <br>
Mitigation: Use only exemplar text the user is comfortable having analyzed in the local agent workflow. <br>
Risk: A weak or unrepresentative sample set can produce a profile that does not match the intended voice. <br>
Mitigation: Collect at least 1000 words across representative samples, include multiple exemplars, and validate generated output against the profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-scribe-style-learner) <br>
- [Scribe Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Feature Extraction Module](modules/feature-extraction.md) <br>
- [Exemplar Reference Module](modules/exemplar-reference.md) <br>
- [Style Application Module](modules/style-application.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML-style profile content and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Style profiles combine quantitative metrics, selected exemplars, anti-patterns, and validation checks.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
