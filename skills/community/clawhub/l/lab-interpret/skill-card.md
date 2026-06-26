## Description: <br>
Interprets clinical laboratory test results by identifying abnormal values, flagging critical results, and providing clinical context without replacing clinical judgment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anightmare2](https://clawhub.ai/user/anightmare2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interpret adult clinical lab reports, identify abnormal or critical values, and provide plain-language context for follow-up with qualified clinicians. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat informational lab-result interpretation as diagnosis, treatment advice, or urgent medical triage. <br>
Mitigation: Confirm abnormal, critical, or confusing results with a qualified clinician and do not rely on this skill alone for diagnosis, treatment, or urgent medical decisions. <br>
Risk: Adult reference and critical-value ranges may not match a specific lab, population, pregnancy status, pediatric case, or clinical context. <br>
Mitigation: Compare interpretations against the report's own reference ranges and patient-specific context before acting on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anightmare2/lab-interpret) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise text or Markdown with abnormal-value flags, critical-value notes, and clinical context.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational medical guidance only; no code execution, credential access, network behavior, or persistence is described by the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, clawhub.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
