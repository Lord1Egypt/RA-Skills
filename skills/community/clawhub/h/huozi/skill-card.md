## Description:

Publish Markdown and HTML to huozi.app as beautiful, shareable web pages. Register, manage, and publish through conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachein](https://clawhub.ai/user/dachein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to register for Huozi, manage a workspace, and publish or update Markdown and HTML pages through API-backed agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Bash examples can become unsafe if untrusted user content is pasted directly into shell-quoted JSON.

Mitigation: Serialize request bodies safely before calling curl and review commands before execution.

Risk: Delete operations may remove the wrong published page if the page slug is ambiguous or incorrect.

Mitigation: Confirm the exact page slug with the user before any delete request.

Risk: Publishing sends user email, API credentials, and page content to Huozi.

Mitigation: Use the skill only when the user trusts Huozi with that information and keep HUOZI_API_KEY out of shared logs and files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dachein/skills/huozi)
- [Huozi](https://huozi.app)
- [Huozi Agent API Reference](https://huozi.app/docs4agent)
- [Huozi Setup Options](https://huozi.app/start)
- [Huozi Documentation](https://huozi.app/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Bash curl commands, JSON request examples, and generated Markdown or HTML content for publication.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for API calls and uses HUOZI_API_KEY for authenticated page operations.]

## Skill Version(s):

0.3.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
