## Description:

Motor FOC Control is a Chinese-language field-oriented control guide covering SVPWM, MTPA, flux weakening, observers, troubleshooting, C examples, and PI tuning support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor-control engineers use this skill to understand and draft FOC implementation guidance, tune current and speed PI loops, and review engineering thresholds for PMSM control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PI tuning and flux-weakening outputs may be unsafe if applied directly to real motors as production settings.

Mitigation: Treat outputs as theoretical starting points and validate on current-limited, speed-limited, temperature-monitored hardware with emergency stop and rollback procedures.

Risk: Chinese-language motor-control material may be misunderstood by users who cannot accurately review the technical content.

Mitigation: Use reviewers with both Chinese-language fluency and motor-control expertise before deploying or acting on the guidance.

## Reference(s):

- [FOC Engineering Parameter Quick Reference](artifact/references/foc-quick-ref.md)
- [FOC PI Tuning Script](artifact/scripts/foc_pi_tuner.py)
- [ClawHub Skill Page](https://clawhub.ai/yongjie666888/skills/motor-foc-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with C code snippets, bash command examples, and plain-text PI tuning output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled tuner can optionally generate a Bode plot image when plotting dependencies are installed.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
