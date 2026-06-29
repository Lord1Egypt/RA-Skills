## Description: <br>
Use only when explicitly invoked to run a read-only project-truth audit that checks project claims against reachable runtime behavior, configuration, deployment reality, tests, executable proof, installation, packaging, upgrade, and release paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill when they explicitly want a read-only claim-vs-reality audit of a project. It produces evidence-grounded findings about stale claims, contract drift, proof gaps, runtime wiring, installation, packaging, upgrade, and release behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit commands or follow-up checks could write files, touch external systems, or expose sensitive values if run without review. <br>
Mitigation: Use the skill's read-only default, set the audit root and output path clearly, and review any command that could write files, touch external systems, or reveal credentials before execution. <br>
Risk: The bundled quick validator currently checks for a removed skill-card.md file. <br>
Mitigation: Treat that validator result as a known package validation gap and rely on server evidence plus targeted artifact review for this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/go-get-uncle-matts-hammerrr) <br>
- [README](README.md) <br>
- [Claim Model](references/claim-model.md) <br>
- [Evidence Rules](references/evidence-rules.md) <br>
- [Command Safety](references/command-safety.md) <br>
- [Reality Gap Checklist](references/reality-gap-checklist.md) <br>
- [Report Rules](references/report-rules.md) <br>
- [Project Truth Audit JSON Schema](schemas/project-truth-audit.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown audit report, with optional JSON and remediation-plan output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; commands that may mutate files, external systems, or secrets are reported for review instead of executed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
