## Description:

Publish static HTML, ZIP archive, or directory to MyVibe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuzhuyule](https://clawhub.ai/user/zhuzhuyule)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to publish web content to MyVibe from an HTML file, ZIP archive, local directory, or URL. It helps analyze project metadata, optionally generate a screenshot, confirm publication details, and return the published MyVibe URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content through a user's MyVibe account and stores or reads account access tokens.

Mitigation: Install only when MyVibe publish authority is acceptable, use the default MyVibe hub, and rotate tokens after use with an untrusted hub.

Risk: The skill runs networked Node tooling and may request global npm installation for screenshot support.

Mitigation: Review global npm install requests before approval and run the skill only in environments where networked Node execution is acceptable.

Risk: Custom hub URLs combined with VIBE_HUB_ACCESS_TOKEN can expose publishing credentials to an unintended service.

Mitigation: Avoid custom hubs when VIBE_HUB_ACCESS_TOKEN is set unless the hub is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuzhuyule/skills/myvibe-skills)
- [Publisher profile](https://clawhub.ai/user/zhuzhuyule)
- [MyVibe hub](https://www.myvibe.so/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with shell commands and publication result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated metadata, selected tags, screenshot status, publish status, and upgrade guidance when returned by the publishing script.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
