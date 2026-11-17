## Description:

Deep research using Parallect.ai that queries Perplexity, Gemini, OpenAI, Grok, and Anthropic in parallel, then synthesizes findings into a unified cited report with conflict resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primeobsession](https://clawhub.ai/user/primeobsession)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run paid, multi-provider research through Parallect.ai, receive cited Markdown synthesis, track costs, and continue research with follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and related thread context are sent to Parallect.ai and downstream AI providers.

Mitigation: Avoid submitting secrets or confidential material unless that external data sharing is approved.

Risk: The skill can spend the user's paid Parallect.ai credits when research is submitted.

Mitigation: Check balance, discuss budget tier, and obtain confirmation before starting research; report cost after each job.

Risk: Research results are asynchronous, and requesting results before completion causes job-state errors.

Mitigation: Poll research_status with backoff and call get_results only after the job is completed.

Risk: Polling too frequently can trigger rate limits.

Mitigation: Use exponential backoff, wait at least 30 seconds between status checks, and slow down after rate-limit responses.

## Reference(s):

- [Parallect Budget Tiers Reference](references/budget-tiers.md)
- [Parallect API Error Reference](references/api-errors.md)
- [Parallect.ai](https://parallect.ai)
- [Parallect MCP Documentation](https://parallect.ai/docs/mcp/overview)
- [Parallect API Reference](https://parallect.ai/docs)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/primeobsession/skills/parallect-ai-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown synthesis with citations, brief summaries, cost reports, follow-on suggestions, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research jobs are asynchronous and require polling before completed results are retrieved.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
