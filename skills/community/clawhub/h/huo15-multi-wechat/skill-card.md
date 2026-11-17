## Description:

Creates multiple independent WeChat app copies on macOS so users can run and sign in to multiple WeChat accounts at the same time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users use this skill when they need an agent to create and verify multiple WeChat application copies for simultaneous account login on one Mac.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete and modify copied WeChat application bundles in /Applications, re-sign them with an ad-hoc signature, and refresh macOS Launch Services.

Mitigation: Run it only when the user understands those macOS application changes, review the proposed commands first, and keep the original /Applications/WeChat.app installed.

Risk: The security scan reports an argument-handling bug that can execute unintended shell commands if the copy count is untrusted or non-numeric.

Mitigation: Accept only a small numeric copy count from a trusted user, and patch or review count validation before running scripts/multi_wechat.sh.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-multi-wechat)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/docs/changelog.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to choose a WeChat copy count before proposing script execution.]

## Skill Version(s):

1.1.0 (source: server release evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
