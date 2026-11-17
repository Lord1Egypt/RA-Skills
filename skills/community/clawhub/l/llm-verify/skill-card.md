## Description:

Verify an LLM API endpoint for model authenticity, billing inflation, relay provenance, performance issues, and silent downgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to check whether an LLM API endpoint is genuine, relayed, silently downgraded, over-metered, or behaving inconsistently before relying on it in development or production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends executing mutable remote installer scripts directly in a shell or PowerShell.

Mitigation: Review and verify fetched installer scripts before running them; prefer a ClawHub install or immutable signed release.

Risk: The built-in installer can write to every detected AI tool by default.

Mitigation: Use targeted install-skill options and review install locations before broad installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/llm-verify)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration, Files]

**Output Format:** [Markdown guidance with command examples and optional report-file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an HTML report and optional JSON report through the llm-verify CLI.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
