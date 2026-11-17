## Description:

清理和修复 txt 电子书中的乱码、广告和排版问题，并支持 AI 增强模式识别非标准广告、复杂乱码和章节格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunfirehw](https://clawhub.ai/user/sunfirehw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to clean TXT ebook files, remove common advertising/watermark patterns, repair mojibake, normalize chapter formatting, and receive a concise cleanup report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local TXT files and may upload ebook contents outside the device as part of its documented workflow.

Mitigation: Use an explicit local file path, review the selected file before processing, and process only documents you have rights to modify or share.

Risk: AI-enhanced modes can send book text to an OpenClaw LLM subagent for advertisement detection, mojibake repair, or chapter parsing.

Mitigation: Use fast mode for local-only rule processing when content is sensitive, or confirm the LLM data-handling posture before enabling balanced or thorough mode.

Risk: Auto-learned cleanup rules and cached LLM responses may influence future files.

Mitigation: Disable auto_learn for cautious use, review generated rules periodically, and clear caches or learned rules before processing unrelated books.

Risk: Automated advertisement and mojibake cleanup can remove or rewrite legitimate text.

Mitigation: Review the cleanup report and compare the cleaned output with the source file before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunfirehw/skills/good-txt-to-hwreader)
- [AI enhancement design](artifact/AI_ENHANCEMENT_DESIGN.md)
- [Changelog](artifact/CHANGELOG.md)
- [Advertisement patterns](artifact/references/ads_patterns.md)
- [Mojibake patterns](artifact/references/mojibake_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Cleaned TXT files, Markdown cleanup reports, and command-oriented agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cleaned output files, reports, logs, cache entries, and learned mojibake rules depending on processing mode and configuration.]

## Skill Version(s):

4.1.0 (source: server release metadata and changelog, released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
