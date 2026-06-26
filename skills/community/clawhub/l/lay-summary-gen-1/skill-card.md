## Description: <br>
Converts complex medical abstracts into plain language summaries for non-expert audiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Medical writers, researchers, trial teams, and agents supporting public-facing health communication use this skill to turn medical abstracts into plain-language summaries with key takeaways, reading-level estimates, and jargon replacements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft summaries may be medically or regulatorily inaccurate if used without review. <br>
Mitigation: Review outputs for medical and regulatory accuracy, and do not treat them as clinical advice. <br>
Risk: Medical abstracts or prompts may include patient-identifiable or confidential study information. <br>
Mitigation: Use only workspaces appropriate for that data and avoid entering identifiable or confidential information unless handling controls are in place. <br>


## Reference(s): <br>
- [Lay Summary Gen References](references/guidelines.md) <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/lay-summary-gen-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing a lay summary, reading level, key takeaways, word counts, target audience, and replaced jargon terms.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated summaries should be reviewed for medical and regulatory accuracy before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
