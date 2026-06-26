## Description: <br>
Event Analyzer helps agents analyze important events through a four-step collect, select, judge, and analyze framework that emphasizes source checks, signal filtering, and investment-oriented event interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to evaluate recent market, policy, industrial, or company events, filter weak signals, grade source quality, and produce structured event-analysis reports. The reports may include business implications and investment-oriented commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-oriented analyses may include buy/sell, position-size, entry, stop-loss, or take-profit ideas. <br>
Mitigation: Treat outputs as unverified general commentary, not personalized financial advice; require independent review before any financial decision. <br>
Risk: The skill requests broad Write and Exec tool access despite being primarily an analysis prompt. <br>
Mitigation: Deploy with the narrowest tool permissions needed for the workflow and remove Write/Exec unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/lj22503-fanli-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/lj22503) <br>
- [Skill README](artifact/README.md) <br>
- [Event analysis sample](artifact/examples/event-analysis-sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown event-analysis reports with sourced bullets, scoring tables, and action-oriented commentary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concrete trading ideas, position sizing, entry, stop-loss, or take-profit commentary; treat as unverified general information.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
