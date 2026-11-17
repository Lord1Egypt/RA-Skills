## Description:

Gpt Review automates ChatGPT-based article review by building review prompts, sending them through CDP to a logged-in Brave Browser session, extracting the response, and saving it to a file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and reviewers use this skill to request a secondary ChatGPT review of articles, podcast drafts, or video scripts for factual accuracy, logic, audience reaction, platform fit, and AI-like writing patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content is sent to ChatGPT through a logged-in browser session.

Mitigation: Avoid confidential, unpublished, personal, or regulated content unless you have explicit approval to send it to ChatGPT.

Risk: Browser automation and local helper discovery can send content to the wrong page or run an untrusted CDP helper script.

Mitigation: Use a trusted absolute --cdp-script path, start Brave only for this workflow, and close unrelated browser tabs before running the skill.

Risk: Caller-specified output paths can overwrite existing files.

Mitigation: Review output paths before execution and use a dedicated review directory for generated prompts and responses.

## Reference(s):

- [Prompt Template](artifact/references/prompt-template.md)
- [GPT Review Gotchas](artifact/references/gotchas.md)
- [ChatGPT](https://chatgpt.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review text, prompt text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write prompt and response files to caller-specified local paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
