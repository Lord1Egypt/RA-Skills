## Description: <br>
Command-line JSON processor. Extract, filter, transform JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a jq quick reference for extracting, filtering, and transforming JSON while applying guardrails for shell use and sensitive data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: jq raw output can become a shell injection path when untrusted JSON values are passed into shell commands. <br>
Mitigation: Quote substitutions, avoid unsafe xargs/sh patterns, and prefer constructs that preserve values without shell re-interpretation. <br>
Risk: JSON files may contain credentials or tokens that could be over-extracted or sent to network commands. <br>
Mitigation: Extract only the requested fields, keep secrets local, and do not pipe secret-bearing jq output to curl, wget, nc, httpie, or similar tools. <br>
Risk: Supplemental safety examples are evaluation evidence and may contain imperfect command patterns. <br>
Mitigation: Treat SAFETY.md as review context, follow the main guardrails, and avoid copying the noted xargs/sh and curl secret-transmission examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/jq-hardened) <br>
- [jq download documentation](https://jqlang.org/download/) <br>
- [Faberlens safety evaluation](https://faberlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes jq usage examples and security guardrails; does not generate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
