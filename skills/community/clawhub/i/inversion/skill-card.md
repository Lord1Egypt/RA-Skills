## Description: <br>
Guides an agent through an Inversion Audit that identifies, ranks, and mitigates plausible failure paths before a high-stakes or hard-to-reverse decision is made. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and decision makers use this skill to run a structured pre-mortem on important plans, investments, launches, or other high-stakes decisions. The expected result is a practical audit with failure paths, load-bearing risks, mitigations, not-to-do rules, and abort triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste sensitive business, legal, financial, or personnel details while applying the advisory framework. <br>
Mitigation: Avoid sharing sensitive details unless the user is comfortable exposing them to the agent environment where the skill runs. <br>
Risk: The audit can produce incomplete or misleading guidance if treated as expert judgment instead of structured decision support. <br>
Mitigation: Review outputs with relevant domain experts before using them for high-stakes commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/inversion) <br>
- [Sources - inversion](references/sources.md) <br>
- [Method in Action: Apollo 1 and the FMEA Mandate (1967)](examples/apollo-1-fmea-1967.md) <br>
- [Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem) <br>
- [Apollo 204 Review Board Final Report](https://history.nasa.gov/Apollo204/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured audit sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hard-stop prompts for stepwise user reflection.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
