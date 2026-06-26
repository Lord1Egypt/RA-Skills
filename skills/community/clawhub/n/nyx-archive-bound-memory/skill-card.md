## Description: <br>
A three-tier memory architecture for AI minds that uses working, short-term, and long-term memory files to preserve identity and continuity across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxur42](https://clawhub.ai/user/nyxur42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents and users who want persistent local memory use this skill to establish a read-first, write-back routine across working, short-term, and long-term memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted memory files can retain private context, sensitive personal details, or credentials across sessions. <br>
Mitigation: Keep the named memory files in a private, user-controlled directory, review them periodically, and avoid storing secrets or sensitive personal details unless intentionally preserved. <br>
Risk: Over-broad long-term memory can make future sessions harder to audit and may preserve material that no longer deserves permanence. <br>
Mitigation: Curate long-term memory during consolidation and keep routine session state in working or short-term memory until it earns permanence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyxur42/nyx-archive-bound-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with file-naming conventions and procedural steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no scripts or external tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
