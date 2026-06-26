## Description: <br>
Use medical translation for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate medical terms or paragraphs for academic writing, with explicit source and target languages, assumptions, and output limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes local Python helper scripts that may read or write workspace files. <br>
Mitigation: Review the bundled scripts before installation and run them only against intended workspace paths. <br>
Risk: Medical terminology output can be incomplete when a term or language pair is unsupported. <br>
Mitigation: Keep source and target languages explicit and require manual confirmation for unsupported terms or flagged translations. <br>
Risk: Requests outside the documented scope or missing required inputs can lead to weak boundary handling. <br>
Mitigation: Stop on out-of-scope or incomplete requests and return the missing inputs, safe partial steps, assumptions, and next checks. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with optional plain-text translation results and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a term or paragraph, source language, target language, and optional context; unsupported terms or language pairs require manual confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
