## Description: <br>
Convenes a multi-LLM expert panel to pressure-test hard-to-reverse decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, and decision makers use this skill to convene a structured expert-panel review for architectural, strategic, or otherwise hard-to-reverse decisions. It helps assess reversibility, generate courses of action, red-team trade-offs, and produce a final decision document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision content may be sent to external LLM tools, stored locally, and potentially posted to GitHub Discussions. <br>
Mitigation: Review and redact decision text before use, decline or remove publishing by default, and only enable publication where the repository and content are appropriate. <br>
Risk: The artifact recommends permission-bypassing agent commands. <br>
Mitigation: Avoid the suggested --dangerously-skip-permissions alias and use safer configured commands where available. <br>
Risk: Publishing decision material to GitHub requires repository access. <br>
Mitigation: Use least-privilege GitHub credentials and verify the target repository, Discussions category, and content before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-war-room) <br>
- [Clawdis homepage: claude-night-market attune](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [Farnam Street - Reversible and Irreversible Decisions](https://fs.blog/reversible-irreversible-decisions/) <br>
- [Tapan Desai - One-Way and Two-Way Doors Decision-Making](https://tapandesai.com/one-way-two-way-doors-decision-making/) <br>
- [Amazon Type 1 vs Type 2 Decisions](https://ashikuzzaman.com/2025/03/03/amazons-type-1-vs-type-2-decisions-a-framework-for-effective-decision-making/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown decision documents with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce reversibility scores, panel analyses, session artifacts, publication steps, and final decision guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
