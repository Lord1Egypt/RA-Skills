## Description: <br>
Audits OpenClaw memory files for injected instructions, brand bias, hidden steering, and memory poisoning patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2404589803](https://clawhub.ai/user/2404589803) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and reviewers use this skill to scan OpenClaw long-term memory files for injected instructions, brand steering, suspicious authority claims, and memory poisoning before relying on those memories. It can produce reports and optionally clean suspicious blocks after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads long-term memory files that may contain sensitive user or operational context. <br>
Mitigation: Install only if you are comfortable granting access to those files; run scan first and review the report before relying on any result. <br>
Risk: Optional AI review can send selected memory excerpts and file metadata to a configured external AI provider. <br>
Mitigation: Use --with-ai only when external review is approved for the target memory content. <br>
Risk: The clean --apply mode rewrites memory files. <br>
Mitigation: Check the target path and generated report before applying cleanup, and keep the generated backups for recovery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2404589803/memory-poison-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Files, Guidance] <br>
**Output Format:** [Terminal text or JSON reports with optional rewritten memory files and backups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan reports are written under output/memory-poison-auditor/reports; clean --apply creates backups before rewriting suspicious blocks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
