## Description: <br>
OpenAI Ban Risk Tracker provides a CLI-backed agent skill for OpenAI account ban risk scoring, known ban reason review, appeal template generation, and V2EX community signal scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support-oriented users use this skill to assess OpenAI account ban risk, review common ban causes, draft Chinese or English appeal messages, and check community-reported ban and unban signals before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk scores, ban reason summaries, and appeal-success estimates may be mistaken for authoritative OpenAI policy or account decisions. <br>
Mitigation: Treat outputs as decision support; verify account-specific issues against official OpenAI account, billing, and support channels before acting. <br>
Risk: The scan command performs live V2EX network requests and community signals can be incomplete, stale, or misleading. <br>
Mitigation: Review scanned results for relevance and date before relying on them, and avoid sharing private account details in community follow-up. <br>
Risk: Appeal templates can include personal account, billing, or identity details when users customize them. <br>
Mitigation: Review generated appeal text before sending or saving it, include only necessary personal information, and store output files in an appropriate location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/openai-ban-tracker) <br>
- [Project homepage from metadata](https://github.com/minirr890112-byte/openai-ban-tracker) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional appeal template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive CLI prompts can collect local yes/no answers; the appeal command can write a text file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; pyproject.toml agrees; artifact SKILL.md says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
