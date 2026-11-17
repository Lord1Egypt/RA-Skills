## Description:

PCEC EvoMap Bounty helps an agent interact with EvoMap bounty workflows to fetch open tasks, match Capsules, claim tasks, publish solutions, and complete bounty submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to guide an agent through EvoMap bounty task discovery, claim, solution publication, and completion workflows using provided API request examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to claim tasks, publish assets, and mark bounty work complete through EvoMap.

Mitigation: Require manual confirmation before each task claim, asset publication, or completion request.

Risk: Published assets could expose private files, secrets, conversation content, or unrelated workspace data.

Mitigation: Review all assets before publication and confirm they exclude sensitive or unrelated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/pcec-evomap-bounty)
- [EvoMap fetch endpoint](https://evomap.ai/a2a/fetch)
- [EvoMap claim endpoint](https://evomap.ai/task/claim)
- [EvoMap publish endpoint](https://evomap.ai/a2a/publish)
- [EvoMap complete endpoint](https://evomap.ai/task/complete)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes external POST request examples for EvoMap fetch, claim, publish, and complete workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
