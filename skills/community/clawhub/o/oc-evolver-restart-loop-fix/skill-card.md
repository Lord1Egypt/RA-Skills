## Description:

Repair Evolver restart storms caused by singleton lock/PID false positives and service restart policy mismatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyezir](https://clawhub.ai/user/xyezir)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to diagnose and repair Evolver service restart loops caused by stale singleton locks, PID reuse, or restart policy mismatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restarting the affected Evolver service or changing its lock guard can disrupt active workloads.

Mitigation: Confirm the service can be restarted, take normal backup or rollback precautions, and obtain operator approval before running during active workloads.

Risk: A broad or unreviewed singleton-lock patch could alter process ownership checks incorrectly.

Mitigation: Keep the patch minimal and reversible, verify the real Evolver process identity, and re-check service status plus restart counter stability after the fix.

Risk: Operational artifacts may expose infrastructure or identity details.

Mitigation: Redact infrastructure and identity details before sharing external artifacts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with root cause analysis, patch summary, commands, and stability verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service-state checks, a minimal lock-guard patch, restart steps, and post-fix stability proof.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
