## Description:

Debug Linux kernel crashes through evidence-first vmcore analysis with the crash utility and memory and concurrency debugging tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazyss](https://clawhub.ai/user/crazyss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and systems engineers use this skill to investigate Linux kernel panics and crash dumps, trace symptoms to evidence-supported causes, and choose focused follow-up debugging steps. It guides offline vmcore analysis and cautious live-system diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is benign with medium confidence, but the scan was partial: one referenced file was not fully inspected and a trigger may be broad.

Mitigation: Review the complete release contents and trigger scope before installation; interpret the verdict as based on incomplete scan evidence.

Risk: Privileged setup, service changes, tracing, or other live diagnostics can modify a host; vmcores and trace output can contain sensitive process data.

Mitigation: Prefer offline read-only analysis. Make live changes only with explicit authorization for the host and action, a bounded plan and rollback; keep collected data access-controlled and do not share it without approval and sanitization.

## Reference(s):

- [Evidence-first analysis workflow](references/evidence-first-workflow.md)
- [Crash dump format and validation](references/vmcore-format.md)
- [Debugging tools guide](references/debug-tools-guide.md)
- [Kdump setup guide](references/kdump-setup-guide.md)
- [Worked kernel crash case studies](references/case-studies.md)
- [Crash utility documentation](https://crash-utility.github.io/)
- [Linux kernel Kdump documentation](https://docs.kernel.org/admin-guide/kdump/kdump.html)
- [Project homepage (metadata.clawdis)](https://github.com/crazyss/linux-kernel-crash-debug)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown findings, diagnostic runbooks, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-linked conclusions with confidence and disproof checks; live-system commands require explicit authorization.]

## Skill Version(s):

1.5.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
