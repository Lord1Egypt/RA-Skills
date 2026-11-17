## Description:

Skill Eval is an OpenClaw skill evaluation framework for testing trigger rate, quality comparisons, model comparisons, and latency profiling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxing9](https://clawhub.ai/user/xiaoxing9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate OpenClaw skills by running trigger-rate tests, quality comparisons, model comparisons, and latency profiles. It helps assess whether skill descriptions trigger correctly and whether a skill improves agent output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores raw conversation histories and tool outputs during evaluation.

Mitigation: Run evaluations in an isolated workspace, avoid real secrets or proprietary prompts, and review or delete eval-workspace artifacts after use.

Risk: The local review viewer has unsafe browser and server behavior according to the security evidence.

Mitigation: Patch or avoid the viewer until the script embedding, benchmark rendering, feedback endpoint, and automatic port termination issues are fixed.

Risk: Running the viewer with elevated privileges could increase impact from the reported unsafe behavior.

Mitigation: Do not run the viewer as a privileged user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoxing9/skills/openclaw-skill-eval)
- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE.md)
- [Architecture](artifact/docs/ARCHITECTURE.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell commands, JSON result files, and generated review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes evaluation artifacts such as histories, transcripts, timing files, JSON summaries, and review reports to an eval workspace.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
