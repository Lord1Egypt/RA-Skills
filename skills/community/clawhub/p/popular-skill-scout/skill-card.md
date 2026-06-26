## Description: <br>
Find popular and practical skills across ClawHub and GitHub for concrete user workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanziwen100](https://clawhub.ai/user/yuanziwen100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to find practical skill recommendations for a specific workflow. It guides the agent to compare ClawHub popularity signals with GitHub maintenance and source checks before returning a concise shortlist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend other skills that have their own security, maintenance, or provenance risks. <br>
Mitigation: Review each recommended skill separately before installation and treat security warnings as hard negatives unless the user explicitly asks to inspect a risky skill. <br>
Risk: Optional ClawHub CLI fallback may run local commands. <br>
Mitigation: Use the CLI fallback only after website and GitHub checks are insufficient and only when the user is comfortable running `npx clawhub` locally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuanziwen100/popular-skill-scout) <br>
- [Publisher Profile](https://clawhub.ai/user/yuanziwen100) <br>
- [Sources And Queries](artifact/references/sources-and-queries.md) <br>
- [Query Templates](artifact/references/query-templates.md) <br>
- [Ranking Rubric](artifact/references/ranking-rubric.md) <br>
- [Current Seeds](artifact/references/current-seeds.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown shortlist with concise recommendation fields and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional shell commands for trial installation or live verification when the user requests them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
