## Description: <br>
Use when the operator asks to merge configured transit notes into domain wiki pages with source metadata, index updates, status transitions, and audit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arroncn993-sys](https://clawhub.ai/user/arroncn993-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators use this skill to merge compiled markdown transit notes into configured domain wiki pages while keeping source metadata, index entries, backlinks, status fields, and final audit checks aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit, move, and audit many files in a configured markdown vault. <br>
Mitigation: Run it only in an explicitly configured vault, keep backups or version control, and review checkpoint and audit results before treating a run as complete. <br>
Risk: A broad audit command hook can execute trusted shell code. <br>
Mitigation: Use only audit commands supplied by a trusted operator or vetted workflow step, and avoid passing unreviewed dynamic shell text. <br>
Risk: Broad QMD or history collections may expose more local knowledge-base content than needed. <br>
Mitigation: Configure QMD only when local recall is needed and scope searchable collections to the relevant vault material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arroncn993-sys/openclaw-wiki-entry-skill) <br>
- [README](README.md) <br>
- [Workflow](references/workflow.md) <br>
- [Path Decision](references/path-decision.md) <br>
- [Self-Check Checklist](references/self-check-checklist.md) <br>
- [Error Playbook](references/error-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown file updates with shell command invocations and checkpoint/audit status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit vault and wiki path configuration through environment variables or command arguments; QMD recall is optional.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
