## Description: <br>
Prompt injection defense. Detect and block malicious prompts, protect system instructions, sanitize user input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maorun](https://clawhub.ai/user/maorun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add defensive prompt-injection checks, input boundary guidance, context separation, and sensitive-output filtering to assistant workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger keywords and detection patterns can interrupt benign workflows or create false positives. <br>
Mitigation: Review warnings before blocking work, tune local trigger patterns for the deployment context, and track recurring false positives. <br>
Risk: Logging detected prompt fragments can retain sensitive user or system information. <br>
Mitigation: Define log storage, retention, access controls, and redaction rules before enabling monitoring guidance. <br>
Risk: Publisher and source provenance are not independently resolved for this version. <br>
Mitigation: Confirm the ClawHub publisher handle, release version, and artifact hash before using the skill where provenance is required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with YAML-style rule examples and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only defensive guidance; no executable tools, API calls, or scripts are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
