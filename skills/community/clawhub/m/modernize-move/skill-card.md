## Description: <br>
Detects and modernizes outdated Move V1 syntax, patterns, and APIs to Move V2+ for legacy contract upgrades and migrations to current Move practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Move projects, choose a modernization scope, apply tiered V1-to-V2+ transformations, and verify behavior with tests after each tier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects and modifies local Move source files. <br>
Mitigation: Keep the project under version control, review the analysis report before approving changes, and inspect generated diffs before relying on them. <br>
Risk: Full Tier 3 migrations can introduce ABI, storage, or event format breaking changes for deployed contracts. <br>
Mitigation: Avoid full Tier 3 migrations on deployed contracts unless breaking changes are intended; use compatible mode to exclude breaking changes. <br>
Risk: Modernization without tests can miss behavior changes. <br>
Mitigation: Establish a passing test baseline first, generate tests when none exist, and run Move tests after each approved tier. <br>


## Reference(s): <br>
- [Detection Rules](references/detection-rules.md) <br>
- [Transformation Guide](references/transformation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Move source edits, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses analysis and confirmation gates, requires a passing test baseline before edits, and verifies after each transformation tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
