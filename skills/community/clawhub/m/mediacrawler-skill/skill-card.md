## Description:

Media Crawler helps agents set up and operate MediaCrawler for multi-platform public information collection, including command-line runs, WebUI launch, result discovery, and common task templates.

This skill is for research and development only.

## Publisher:

[excalibur9527](https://clawhub.ai/user/excalibur9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install MediaCrawler, run common public-information collection workflows, launch its WebUI, and locate generated result files. It is best suited for learning, research, and compliance-reviewed collection tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs mutable internet-fetched code, repository code, and dependencies as the current user.

Mitigation: Review the setup before installing, install uv manually where possible, and run the skill in a dedicated low-privilege environment.

Risk: The upstream MediaCrawler repository is cloned or updated without a pinned, reviewed commit.

Mitigation: Pin or review the MediaCrawler commit before running collection workflows.

Risk: Crawler outputs and login or session caches may contain sensitive data.

Mitigation: Protect generated outputs and login/session caches during use, and delete them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/excalibur9527/skills/mediacrawler-skill)
- [Publisher profile](https://clawhub.ai/user/excalibur9527)
- [MediaCrawler upstream project](https://github.com/NanmiCoder/MediaCrawler.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run setup commands, clone or update MediaCrawler, install dependencies, launch a local WebUI, and inspect crawler result files.]

## Skill Version(s):

0.1.4 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
