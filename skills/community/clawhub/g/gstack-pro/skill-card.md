## Description: <br>
GStack Pro turns an AI assistant into a structured virtual software engineering team with specialist roles for product planning, architecture, design review, code review, QA, shipping, retrospectives, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run structured product, architecture, review, QA, release, retrospective, and documentation workflows through OpenClaw subagents. It is most useful when planning a feature, preparing to ship, reviewing code, running browser QA, or reassessing product direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QA workflows can drive browser actions against live applications, including actions that submit forms or change data. <br>
Mitigation: Run QA against staging or test accounts where possible, and manually approve browser actions that submit forms or modify data. <br>
Risk: Shipping workflows can perform high-impact repository operations such as rebasing, version bumps, force-with-lease pushes, PR creation, or direct pushes. <br>
Mitigation: Confirm the repository, branch ownership, clean working tree, test results, and PR target before allowing release commands. <br>
Risk: Instruction-only review and planning outputs may contain incomplete or misleading guidance. <br>
Mitigation: Review and scan the skill before deployment, and keep human approval in the loop for production changes. <br>


## Reference(s): <br>
- [GStack](https://gstacks.org) <br>
- [CEO product thinking SOP](references/plan-ceo.md) <br>
- [Architecture review SOP](references/plan-eng.md) <br>
- [Paranoid code review SOP](references/review.md) <br>
- [Automated QA SOP](references/qa.md) <br>
- [One-command ship SOP](references/ship.md) <br>
- [Engineering retro SOP](references/retro.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured reports, checklists, JSON snippets, code examples, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include role-specific reports, QA health scores, review findings, release plans, and documentation updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
