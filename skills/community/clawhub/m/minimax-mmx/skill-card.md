## Description: <br>
MiniMax MMX helps agents use the MMX CLI for MiniMax multimodal tasks including image, video, speech, music, vision, search, and text chat workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clx20000410](https://clawhub.ai/user/clx20000410) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run MiniMax MMX CLI commands for generating media, describing images, querying search, checking quota, and managing authentication. It is intended for workflows where an agent needs concise command guidance and JSON-oriented CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, files, images, and search queries may be transmitted to MiniMax through the MMX CLI. <br>
Mitigation: Avoid sending secrets, private documents, regulated data, or sensitive images unless the user has approved that third-party transmission. <br>
Risk: The workflow depends on the external MiniMax MMX CLI package and account credentials. <br>
Mitigation: Install the CLI only from trusted sources, verify account setup before use, and prefer a limited-scope API key. <br>


## Reference(s): <br>
- [MMX-CLI Detailed Command Reference](references/commands.md) <br>
- [ClawHub MiniMax MMX Release Page](https://clawhub.ai/clx20000410/minimax-mmx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly request quiet JSON output for easier agent parsing; generated media and downloaded task results may be written as files by the MMX CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
