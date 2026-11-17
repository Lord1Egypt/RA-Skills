## Description:

Parses shared Dedao note links to extract article text and download article images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymsha88](https://clawhub.ai/user/ymsha88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to process Dedao share links, extract readable note content, and save related images for local note-taking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open arbitrary web pages in an unsandboxed Chromium browser.

Mitigation: Use it only with trusted Dedao links or add a strict dedao.cn allowlist, and run browser activity in an isolated container or with Chromium sandboxing restored.

Risk: The skill can contact third-party image hosts and save page content or images locally.

Mitigation: Review target links before use and make the output directory explicit and configurable before deployment.

Risk: The included runner writes to a fixed local notes folder.

Mitigation: Configure an approved output path for the deployment environment and review written files before sharing or importing them into other systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ymsha88/skills/parse-deodao-shared-link)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown files with extracted text and local image references; JavaScript helpers may also return structured parse results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save downloaded images to local storage when image saving is enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
