## Description:

Verify Polymarket MR-V4 trading system deployment health by running a local check script that reports process, lock, config, trade activity, isolation, and collector status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyw1028](https://clawhub.ai/user/bobbyw1028)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill after Polymarket MR-V4 strategy deployments, config changes, process restarts, or gateway restarts to check local trading-system health and receive pass, warning, and failure results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script that inspects process state and trading-system config and log files.

Mitigation: Run it only in an authorized Polymarket workspace where those local checks are expected.

Risk: The verification script depends on hardcoded local paths and expected deployment values.

Mitigation: Review the paths and expected values before use so results reflect the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobbyw1028/skills/polymarket-verify)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command and pass, warning, and failure status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local script exits with the number of failed checks and prints a summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
