## Description: <br>
Deep research using Parallect.ai that queries multiple AI research providers in parallel and synthesizes results into a unified report with cross-referenced citations and conflict resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primeobsession](https://clawhub.ai/user/primeobsession) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an OpenClaw agent run paid, multi-provider research workflows, manage budget confirmation, poll asynchronous jobs, and return cited synthesis reports with follow-up options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed research jobs can spend user credits. <br>
Mitigation: Check balance, explain the selected budget tier and maximum cost, and get explicit user confirmation before starting research. <br>
Risk: Research prompts and context are sent to Parallect and its provider network. <br>
Mitigation: Avoid submitting secrets or sensitive business, personal, or regulated data unless that sharing is acceptable to the user. <br>
Risk: Asynchronous research jobs can be mishandled if results are requested before completion or polled too frequently. <br>
Mitigation: Poll job status with exponential backoff, wait for completed status before retrieving results, and handle rate limits or stalled jobs with user-visible recovery options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/primeobsession/parallect-ai-deep-research) <br>
- [Parallect.ai](https://parallect.ai) <br>
- [Parallect MCP Docs](https://parallect.ai/docs/mcp/overview) <br>
- [Parallect API Reference](https://parallect.ai/docs) <br>
- [Parallect Budget Tiers Reference](references/budget-tiers.md) <br>
- [Parallect API Error Reference](references/api-errors.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown synthesis reports with citations, plus setup/configuration guidance and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARALLECT_API_KEY; research jobs are asynchronous and may spend credits after user budget confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
