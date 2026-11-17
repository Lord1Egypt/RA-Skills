## Description:

Turn a public figure into a private AI mentor by collecting public posts, speeches, and platform content, extracting thinking frameworks and communication style, and generating a local MENTOR.md for advice in that figure's style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to build local mentor profiles from a chosen public figure's public content, then ask for decision support through that figure's documented thinking patterns and communication style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled collectors can export logged-in account profile, likes, favorites, follows, and activity data.

Mitigation: Use an isolated browser profile with no unrelated logged-in accounts, and run deep-profile collectors only when intentionally exporting your own account data.

Risk: Browser automation endpoints and MCP tokens can grant broad access to active browsing sessions.

Mitigation: Verify the ManoBrowser endpoint and version before use, and do not provide MCP tokens to untrusted environments.

Risk: Optional dependency downloads and local scripts may expand the execution surface.

Mitigation: Review dependencies and scripts before running them, and disable automatic dependency downloads unless they are required and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophie-xin9/skills/mentor)
- [Artifact README](artifact/README.md)
- [Mentor analysis guide](artifact/guides/ANALYSIS.md)
- [Social media collection guide](artifact/guides/SOCIAL_MEDIA.md)
- [Video subtitle collection guide](artifact/guides/VIDEO_SUBTITLE.md)
- [Wiki and quotes collection guide](artifact/guides/WIKI_QUOTES.md)
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown mentor profile files, JSON source-data templates, and command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary generated artifact is a local MENTOR.md; supporting outputs may include raw collected data and analysis notes.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
