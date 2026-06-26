## Description: <br>
Generate a structured GitHub repository digest with a briefing summary, categorized changes, community discussions, and clickable source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RoggeOhta](https://clawhub.ai/user/RoggeOhta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to brief themselves on recent GitHub repository releases, merged pull requests, open issues, and community discussion trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: For private repositories, the digest can include private issues, pull requests, releases, labels, author details, and other repository information visible to the authenticated GitHub CLI account. <br>
Mitigation: Run the skill only against intended repositories, review the generated digest before sharing it, and treat private-repository digests as confidential. <br>


## Reference(s): <br>
- [GitHub Digest on ClawHub](https://clawhub.ai/RoggeOhta/github-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown digest with clickable source links and optional shell commands for GitHub CLI data gathering] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's language and omits empty digest sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
