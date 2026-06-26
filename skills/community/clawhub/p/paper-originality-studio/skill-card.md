## Description: <br>
This skill helps revise Chinese and mixed Chinese-English academic manuscripts by scanning originality risks, comparing drafts, restructuring paragraphs, reducing mechanical phrasing, repairing citation flow, unifying terminology, and generating auditable rewrite guidance without fabricating evidence or designing detector-specific evasion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, academic authors, editors, and agent operators use this skill to scan Chinese or mixed Chinese-English manuscripts, compare drafts, split long texts, generate rewrite prompts, and produce auditable academic editing guidance while preserving facts, citations, and evidence boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be misused to disguise plagiarism, evade academic review systems, or outsource prohibited academic work. <br>
Mitigation: Use it only for legitimate revision, require audit notes, keep facts and evidence boundaries intact, and refuse detector-specific bypass, fabricated sources, fabricated data, and full ghostwriting requests. <br>
Risk: Manuscripts may contain confidential, unpublished, or institutionally restricted material. <br>
Mitigation: Process drafts locally when possible, avoid sending sensitive text to uncontrolled external services, and have the author, advisor, or collaborator review the final manuscript. <br>
Risk: Rewriting can accidentally alter citations, terminology, formulas, legal definitions, standards, or factual claims. <br>
Mitigation: Preserve citations, data, formulas, standards, and specialized terms by default, and manually verify references, figure labels, page numbers, and technical claims after editing. <br>
Risk: The artifact includes a publishing and patent service contact that may be mistaken for an official support channel. <br>
Mitigation: Show the contact only in relevant service-consultation contexts, do not present it as official support, and independently verify it before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/paper-originality-studio) <br>
- [Workflow guide](references/WORKFLOWS.md) <br>
- [Rewrite pattern resource](resources/rewrite_patterns_zh.json) <br>
- [Smoke test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown, JSON reports, text chunk files, and structured rewrite prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python tooling can scan manuscripts, compare original and revised drafts, split sections, and generate prompts; Python 3 or python is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
