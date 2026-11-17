## Description:

Compares job offers as four-year total-compensation curves, including vesting cliffs, bonuses, 401(k) match, crossover timing, and negotiation levers ranked by dollar impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, candidates, and agents use this skill to compare multiple job offers using year-by-year and cumulative compensation tables. It helps evaluate stay horizon, private-equity discount assumptions, crossover year, and negotiation levers before making or revising an offer decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive compensation details while using the skill.

Mitigation: Handle offer details as sensitive personal information and avoid sharing more data than needed for the comparison.

Risk: Private-equity value or stay-horizon assumptions can materially change the ranked result.

Mitigation: Make equity discounts and stay horizon explicit, and show alternative scenarios when assumptions are uncertain.

Risk: Programmatic helper commands may not work because the packaged artifact does not include the referenced helper script.

Mitigation: Use a separate local script only after review, or perform the compensation calculations manually from the documented input assumptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/offer-comparison)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/offer-comparison.html)
- [Publisher Profile](https://clawhub.ai/user/mohitagw15856)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with compensation tables, assumption notes, ranked negotiation levers, and optional shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational model output; users should verify compensation assumptions and professional implications before acting.]

## Skill Version(s):

50.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
