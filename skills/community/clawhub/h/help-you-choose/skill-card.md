## Description: <br>
A bilingual decision-coaching skill that uses Socratic questioning, decision frameworks, optional visual analysis, history tracking, and user preference profiles to help users make clearer personal and professional choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stella-ji-shuting](https://clawhub.ai/user/stella-ji-shuting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to guide structured decision coaching for career, relationship, relocation, and other life choices. The skill helps clarify values, compare options, stress-test assumptions, and produce a decision report without presenting the framework score as the final answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive decision details may be stored in local history and profile files. <br>
Mitigation: Ask for explicit consent before saving, decline persistence for private topics, and review or delete local decision data when it is no longer needed. <br>
Risk: Generated decision reports may expose personal information if deployed to a public URL. <br>
Mitigation: Review the exact report content and intentionally approve sharing before any public deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stella-ji-shuting/help-you-choose) <br>
- [Decision framework reference](references/frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance, Markdown decision reports, optional HTML visualization files, and local script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist decision history and profile data locally when the user consents; may generate interactive decision reports for review.] <br>

## Skill Version(s): <br>
1.2.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
