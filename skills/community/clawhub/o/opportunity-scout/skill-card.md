## Description: <br>
Finds profitable business opportunities in a niche by researching public demand signals, scoring opportunities, and generating a ranked recommendation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avnikulin35](https://clawhub.ai/user/avnikulin35) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, founders, product teams, and market researchers use this skill to scan public sources for unmet needs, compare opportunities, and decide what to build next. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill researches public markets and may expose confidential business plans, customer names, secrets, or private business details if those are included in the niche prompt. <br>
Mitigation: Use only public or non-sensitive niche descriptions, and avoid entering confidential plans, customer data, credentials, or private business details. <br>
Risk: The skill suggests running local CLI searches, so unsafe prompt handling could turn niche text into risky shell arguments. <br>
Mitigation: Run only trusted local tools and pass niche text as quoted or structured arguments rather than interpolating raw user text into shell commands. <br>
Risk: Market research reports can overstate demand or monetization when public signals are sparse or noisy. <br>
Mitigation: Treat generated opportunities as decision support, verify evidence links and quotes, and validate promising ideas before committing significant resources. <br>


## Reference(s): <br>
- [Opportunity Scoring Guide](references/scoring-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/avnikulin35/opportunity-scout) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with ranked opportunity tables, evidence summaries, scores, and recommendations; optional JSON opportunity templates or inputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores opportunities on demand, competition, feasibility, and monetization using a 1-5 scale for each criterion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
