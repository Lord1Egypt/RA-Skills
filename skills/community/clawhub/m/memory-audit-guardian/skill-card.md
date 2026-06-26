## Description: <br>
Weekly memory governance audit for OpenClaw. Use when user asks to audit/optimize memory quality, reduce token overhead, verify MEMORY/TOOLS/AGENTS role boundaries, validate QMD routing quality, or run a periodic memory health check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markisadesigner1992-eng](https://clawhub.ai/user/markisadesigner1992-eng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw memory files for role separation, token-budget drift, QMD routing quality, retrieval discipline, and weekly cleanup priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect persistent memory, profile, and governance files that contain sensitive user or workspace context. <br>
Mitigation: Install it only for memory audits, review generated reports before saving or sharing them, and approve any memory-file edits only after checking the proposed changes. <br>
Risk: Audit findings or keyword suggestions could remove useful context or introduce incorrect governance guidance if applied without review. <br>
Mitigation: Treat the report as a proposal, preserve role boundaries, and require explicit user approval before overwriting or changing memory files. <br>


## Reference(s): <br>
- [Memory Audit Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with findings, an action plan, and a report path suggestion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a five-line executive summary, A/B/C score, risk list, weekly fixes, and add/remove keyword suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
