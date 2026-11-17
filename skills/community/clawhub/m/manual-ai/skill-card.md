## Description:

Manual AI helps users complete AI generation tasks through guided human-in-the-loop use of Gemini, Google AI, ChatGPT, Doubao, Qianwen, and NotebookLM when automated API calls fail or a specific platform is better suited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI-assisted content creators use this skill as a fallback path when API access is rate-limited, unavailable, or not suited to the task. It recommends an external AI platform and provides prompts and manual steps for text, image, code, document, and knowledge-visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External AI websites may process or retain submitted prompts, files, personal data, confidential business material, or regulated content under their own terms.

Mitigation: Do not paste or upload secrets, credentials, personal data, confidential documents, or regulated material unless organizational policy permits that provider and use case.

Risk: Installer or source integrity depends on obtaining the skill through a trusted ClawHub path.

Mitigation: Install through a trusted ClawHub path or a pinned verified installer when possible.

Risk: Manual guidance for third-party AI platforms can become outdated as platform availability, account requirements, pricing, or capabilities change.

Mitigation: Verify the selected platform's current access requirements, limits, and terms before relying on generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luhuiwang/skills/manual-ai)
- [Platform operation quick reference](artifact/references/platform-guides.md)
- [Gemini](https://gemini.google.com)
- [Google AI Search](https://google.com/search?udm=50)
- [ChatGPT](https://chatgpt.com)
- [Doubao](https://doubao.com)
- [Qianwen](https://qianwen.com)
- [NotebookLM](https://notebooklm.google.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with platform recommendations, prompts, links, step-by-step instructions, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for manual execution by a user on third-party AI websites.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
