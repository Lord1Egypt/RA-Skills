## Description: <br>
Helps AI agents plan, review, implement, audit, or improve newsletter workflows across editorial calendars, issue structure, sponsorship inventory, reader growth, and retention loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, editors, and growth teams use this skill to make newsletter planning, audits, sponsorship reviews, reader survey synthesis, and retention recommendations specific, reviewable, and safe before any live email-system action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Newsletter guidance could lead to live sends, contact imports, suppression edits, DNS changes, production automation changes, provider migrations, or destructive cleanup. <br>
Mitigation: Treat those actions as high risk and stop for explicit human approval before execution. <br>
Risk: Recommendations may rely on incomplete newsletter metrics, consent state, suppression status, or sponsor obligations. <br>
Mitigation: State which source material supports each recommendation and do not assume missing fields, consent, or suppression state. <br>
Risk: Sponsor placement or growth experiments could reduce reader trust if they conflict with the publication promise. <br>
Mitigation: Keep sponsor copy distinct from editorial copy and match growth ideas to the audience and publication promise. <br>


## Reference(s): <br>
- [Newsletter Skill Operating Checklist](references/operating-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/polnikale/newsletterskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations separate analysis from live-system actions and require explicit approval before high-risk email operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
