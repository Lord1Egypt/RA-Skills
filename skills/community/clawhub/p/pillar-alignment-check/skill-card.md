## Description: <br>
Checks draft or pre-publication Redditech Labs content against six content pillars and returns a primary pillar, optional secondary pillar, alignment score, and pass/flag/reject verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents producing or reviewing Redditech Labs content use this skill before drafting or publishing blog posts, tweets, threads, or LinkedIn posts to check pillar alignment and brand voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Outsider Perspective pillar can introduce personal, Caribbean, or Australian framing that is not present in the source content. <br>
Mitigation: Use that pillar only when the framing is user-approved and factually supported by the content being reviewed. <br>
Risk: The skill may reject or escalate content under Redditech-specific editorial rules, including DeFi/Web3 scope checks and forbidden phrasing. <br>
Mitigation: Treat verdicts as editorial guidance and route reject, DeFi/Web3, or recent Outsider Perspective cases to the responsible reviewer before publishing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown verdict block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes primary pillar, optional secondary pillar, verdict, reason, and action when rejected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
