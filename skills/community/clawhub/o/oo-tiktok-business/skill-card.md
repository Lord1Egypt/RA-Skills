## Description: <br>
TikTok Business helps agents inspect authorized advertisers, campaigns, GMV Max stores, sessions, identities, videos, anchors, authorization status, reporting rows, and planning recommendations through an OOMOL-connected TikTok Business account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, commerce teams, and agent developers use this skill to discover TikTok Business account structure and retrieve GMV Max campaign, store, reporting, budget, and bid information from a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill's read-only framing conflicts with documented write/destructive account actions. <br>
Mitigation: Review exact TikTok Business actions before installation and require explicit user confirmation for any action tagged [write] or [destructive]. <br>
Risk: The security guidance flags an unsafe CLI install pattern. <br>
Mitigation: Install the oo CLI through a verified method and avoid blindly executing remote shell installer commands. <br>
Risk: The skill operates on connected TikTok Business data and may expose business account information through connector responses. <br>
Mitigation: Use an account whose TikTok Business data access is appropriate for the intended agent workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-tiktok-business) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [TikTok Business Homepage](https://business.tiktok.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL oo CLI actions against a connected TikTok Business account; action schemas should be inspected before payload construction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
