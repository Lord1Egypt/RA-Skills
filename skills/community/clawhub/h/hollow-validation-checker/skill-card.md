## Description: <br>
Helps detect hollow validation in AI agent skills by identifying fake tests that always pass without actually verifying behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketplace reviewers use this skill to inspect validation commands, test scripts, or batches of skills for hollow validation patterns such as echo-only checks, tautological assertions, and exit-code gaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unknown validation commands may be unsafe if executed during review. <br>
Mitigation: Use the skill for static review of validation snippets and do not run unknown validation commands just to analyze them. <br>
Risk: The release declares curl as a required binary without security findings explaining why it is needed. <br>
Mitigation: Ask the publisher why curl is required before deploying the skill in stricter environments. <br>
Risk: Static review may miss sophisticated test theater that appears substantive while testing trivial properties. <br>
Mitigation: Treat findings as validation-quality signals and pair them with human review or additional assurance checks for high-risk releases. <br>


## Reference(s): <br>
- [Hollow Validation Checker on ClawHub](https://clawhub.ai/andyxinweiminicloud/hollow-validation-checker) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown validation quality report with findings, evidence, ratings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report classifies validation quality as SUBSTANTIVE, WEAK, or HOLLOW when supported by the reviewed input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
