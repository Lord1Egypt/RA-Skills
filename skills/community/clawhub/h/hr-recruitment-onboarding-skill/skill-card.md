## Description: <br>
Use when users ask to create a recruitment JD, initialize recruiting files, or configure the HR JD generator or its optional model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizizheng302](https://clawhub.ai/user/lizizheng302) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and recruiting users use this skill to turn natural-language hiring needs into structured job descriptions and workspace files for a position. It supports local rule-based generation and optional model-enhanced extraction when approved model settings are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates HR recruitment files in the configured workspace. <br>
Mitigation: Install and run it only in a workspace where creating HR recruitment files is intended. <br>
Risk: Optional model enhancement can send job descriptions and hiring details to the configured endpoint. <br>
Mitigation: Leave LLM_* unset for local rule-based generation, or use only an approved endpoint and secure environment variables. <br>
Risk: Generated job descriptions can contain errors or unsuitable hiring criteria. <br>
Mitigation: Require HR review before use and confirm criteria are job-related, necessary, legal, and non-discriminatory. <br>
Risk: The dependency list includes an unpinned pytest package. <br>
Mitigation: Pin or separate the pytest dependency before controlled CI or production packaging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizizheng302/skills/hr-recruitment-onboarding-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON CLI response with generated Markdown and JSON workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated job descriptions and requirements require HR review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
