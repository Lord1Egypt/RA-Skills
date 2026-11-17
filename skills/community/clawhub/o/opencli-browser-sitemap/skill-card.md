## Description:

Guides agents using opencli browser to use sitemap context for website navigation while treating live browser state as authoritative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when driving websites with opencli browser and sitemap context is available or requested. It helps choose adapter or browser fallback paths, refresh state after actions, and record stale sitemap observations without treating prior sitemap data as ground truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local sitemap overlay notes and adapter health updates can persist and influence future browser automation.

Mitigation: Review ~/.opencli/sites/<site>/sitemap/ after use when persistent navigation hints affect future tasks.

Risk: Sitemap context can be stale and may point to missing buttons, URLs, routes, or APIs.

Mitigation: Refresh browser state after actions, treat live browser state as authoritative, and mark stale sitemap entries instead of repeatedly following outdated guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/opencli-browser-sitemap)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown guidance with inline shell commands and local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or edit local sitemap overlay notes under ~/.opencli/sites/<site>/sitemap/ when drift is found.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
