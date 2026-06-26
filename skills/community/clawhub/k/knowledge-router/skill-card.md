## Description: <br>
Build a lightweight routing layer across existing knowledge sources such as MEMORY.md, daily memory files, self-improving notes, skill references, and audit records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lethehades](https://clawhub.ai/user/lethehades) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide which existing knowledge source to read first for rules, facts, methods, evidence, or workflow improvements before loading broad context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local memory, skill reference, audit, and ~/self-improving note files. <br>
Mitigation: Use narrower --scope values when possible and keep secrets out of knowledge files. <br>
Risk: The optional --output argument can create or overwrite a report path. <br>
Mitigation: Write reports only to paths you intend to create or overwrite. <br>


## Reference(s): <br>
- [Knowledge Router ClawHub Page](https://clawhub.ai/lethehades/knowledge-router) <br>
- [Source Types](artifact/references/source-types.md) <br>
- [Routing Rules](artifact/references/routing-rules.md) <br>
- [Promotion Rules](artifact/references/promotion-rules.md) <br>
- [Report Format](artifact/references/report-format.md) <br>
- [Release Minimal](artifact/references/release-minimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown routing report with optional saved text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include query intent, primary sources, secondary sources, rationale, and promotion hints.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
