## Description:

Helps agriculture businesses create AI-assisted image, short-video, and content marketing plans with audience strategy, content calendars, prompts, AI-HIVE task tracking, and human review gates for factual claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External agriculture businesses, marketing teams, and content operators use this skill to plan channel-specific campaigns, generate reviewable image and video prompts, run AI-HIVE media tasks, and validate claims before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private media could be exposed when running AI-HIVE scripts.

Mitigation: Use environment variables instead of command-line API keys, use a low-privilege key, avoid untrusted base URLs, and review outputs before sharing.

Risk: Downloaded or generated files could overwrite local files or land outside an intended review area.

Mitigation: Run generation in a contained output directory and inspect downloaded media before publication or reuse.

Risk: Agriculture origin, testing, nutrition, efficacy, pricing, authorization, or platform-rule claims could be inaccurate.

Mitigation: Require human verification of claims, rights, and current platform requirements before publication.

## Reference(s):

- [Agriculture image and video content marketing industry playbook](artifact/references/industry-playbook.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/industry-agriculture-company-marketing-ai-hive)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and downloaded image or video files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
