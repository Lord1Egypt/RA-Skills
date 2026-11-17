## Description:

Helps users write, analyze, improve, and review Xiaohongshu content through drafting, writing coaching, trend and note analysis, compliance checks, and content planning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to plan, draft, critique, polish, and review Xiaohongshu posts while maintaining a personal writing profile and avoiding automated posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require access to a user's Xiaohongshu cookie or authenticated browser profile.

Mitigation: Use the skill only in an isolated environment and only with credentials the user is comfortable exposing to the local agent session.

Risk: The release evidence warns about unsafe credential and browser-session handling, including xsec_token exposure.

Mitigation: Avoid storing or sharing xsec_token values and review browser-session workflows before routine use.

Risk: The security guidance flags a publishing-credential path in CLAUDE.md.

Mitigation: Do not follow that publishing-credential path when installing or using the public skill.

Risk: Optional dependencies and browser-assisted workflows expand the local execution surface.

Mitigation: Pin dependencies where possible and review scripts before executing browser, scraping, or credential-dependent commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-xiaohongshu)
- [Publisher Profile](https://clawhub.ai/user/zhaobod1)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Version Changelog](artifact/docs/changelog.md)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON files, shell command suggestions, and local draft/profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local user profile, draft, post, review, and snapshot files under the user's Xiaohongshu workspace; browser and API-assisted workflows require user-provided credentials or authenticated browser state.]

## Skill Version(s):

3.10.0 (source: frontmatter, release evidence, artifact metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
