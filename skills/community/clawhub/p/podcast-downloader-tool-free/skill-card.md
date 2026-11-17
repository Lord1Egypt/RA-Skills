## Description: <br>
Helps individual users download single Xiaoyuzhou podcast episodes and show notes, then convert audio from M4A to MP3 for offline listening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal automation users use this skill to prepare single Xiaoyuzhou podcast episodes for offline listening by downloading audio, extracting show notes, and producing MP3 files. It is suited to individual podcast archiving rather than batch or multi-platform download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports unsafe filename handling that could write or delete files outside the intended podcast folder. <br>
Mitigation: Use a dedicated empty PODCAST_DIR, sanitize episode and podcast filenames before execution, and review generated paths before downloads or deletions occur. <br>
Risk: The security review reports overly broad activation language for a workflow that can execute shell commands. <br>
Mitigation: Use the skill only for explicit Xiaoyuzhou episode downloads and review proposed shell commands before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/podcast-downloader-tool-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>
- [Source Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-style result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MP3 audio files and Markdown show notes through agent-executed shell workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
