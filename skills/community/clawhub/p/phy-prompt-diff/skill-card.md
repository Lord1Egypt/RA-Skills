## Description: <br>
Compares system prompts and agent instruction files to produce a semantic changelog that highlights behavioral changes, contradictions, guardrail removals, permission expansions, and instruction-density shifts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and skill authors use this skill to compare versions of prompt or agent-instruction files and review behavior-level changes before publishing or committing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt files or git revisions may contain secrets, private instructions, or sensitive internal context. <br>
Mitigation: Use the skill only on files intentionally provided for analysis, and avoid unrelated private files, secrets, or sensitive internal prompts unless they are meant to be reviewed locally. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-prompt-diff) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/PHY041) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with summaries, risk sections, comparison tables, and a changelog entry] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes user-provided prompt files, pasted prompt versions, or git revisions locally; no external API use is indicated by the artifact or security evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
