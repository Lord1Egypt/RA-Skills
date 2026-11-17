## Description:

This skill helps developers audit OpenAI-compatible relay usage and plan a staged migration to AI-HIVE for text, image, video, routing, task tracking, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit current OpenAI-compatible API relay or gateway usage, compare AI-HIVE requirements, and produce a testable migration plan with rollback, routing, task ledger, and acceptance criteria. It is aimed at teams moving text workflows into image, video, ecommerce, advertising, marketing, and batch generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable AI-HIVE clients can make real API calls and trigger billable generation.

Mitigation: Review scripts before installation, use a limited test API key and budget, and confirm AI-HIVE use is intended before running generation commands.

Risk: The skill handles API keys, media uploads, downloads, and local output paths.

Mitigation: Avoid sensitive media, confirm input rights, use a controlled output directory, keep keys out of files and logs, and rotate test keys after evaluation.

Risk: Security evidence reports identity mismatches and unsafe URL or file handling.

Mitigation: Keep the default AI-HIVE base URL unless the endpoint is trusted, and require publisher fixes for identity drift plus URL and output-path validation before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/openai-compatible-relay-migration-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)
- [Platform source and comparison boundaries](references/platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON files and runnable Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce migration audit JSON, blueprint JSON, API task records, media output paths, and ffmpeg command output when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
