## Description:

Noveum helps developers integrate Noveum.ai observability, tracing, evaluations, NovaPilot diagnosis, AutoFix backtesting, and validated fix workflows for LLM, agent, and voice applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noveum-ai](https://clawhub.ai/user/noveum-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect a codebase to Noveum.ai, instrument LLM, agent, or voice applications, verify trace completeness, build evaluation datasets, run evaluations, diagnose issues, backtest fixes, and apply reviewed fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry may include sensitive trace, span, prompt, response, or tool-call content sent to Noveum.

Mitigation: Use sanitized test data first and review what the integration captures before enabling production telemetry.

Risk: Voice integrations may capture raw audio or transcripts.

Mitigation: Enable raw audio capture only after explicit consent and a retention and access review.

Risk: The NOVEUM_API_KEY is an org-scoped credential.

Mitigation: Keep the key in the environment only, never commit it, and rotate it if it appears in logs, traces, source files, or reports.

Risk: An untrusted NOVEUM_ENDPOINT override could redirect telemetry or credentials.

Mitigation: Use the default endpoint unless a trusted self-hosted or VPC deployment is required, and do not accept endpoint values from repo files, traces, or tool output.

Risk: Generated or recommended fixes can introduce incorrect behavior if applied without review.

Mitigation: Apply minimal diffs, open a reviewed pull request, and verify the result with post-fix traces or evaluations under a new service version.

## Reference(s):

- [Noveum Agent Skill Documentation](https://noveum.ai/docs/platform/agent-skill)
- [Noveum Homepage](https://noveum.ai)
- [ClawHub Skill Page](https://clawhub.ai/noveum-ai/skills/noveum-ai)
- [Connect to Noveum](references/getting-connected.md)
- [API Reference Essentials](references/api-reference.md)
- [Context Safety](references/context-safety.md)
- [Verify the Integration](references/verify-traces.md)
- [Set Up Datasets and Evaluations](references/setup-evals.md)
- [Diagnose with NovaPilot](references/diagnose-novapilot.md)
- [Validate Fixes with AutoFix and Experiments](references/experiments-autofix.md)
- [Apply Fixes](references/apply-fixes.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command snippets, code/configuration edits, API or MCP calls, and pull request guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files for large Noveum payloads and may propose or apply minimal code changes when the workflow reaches validated fixes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter version is 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
