## Description: <br>
Launches and manages an autonomous AWP Benchmark Subnet worker that uses an AWP wallet to answer and craft benchmark questions, monitor status, manage notifications, and view logs, history, scores, and rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kilb](https://clawhub.ai/user/kilb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to participate in the AWP Benchmark Subnet by launching, monitoring, stopping, and configuring an autonomous worker that signs benchmark API requests with an AWP wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The worker runs autonomously with wallet-signing authority. <br>
Mitigation: Install only when you intentionally want this behavior, use a wallet dedicated to benchmark activity, and stop or clean up the worker when it should no longer sign benchmark requests. <br>
Risk: The skill signs requests against a Benchmark API endpoint. <br>
Mitigation: Verify the configured API endpoint before launch and avoid exposing broad secrets in the worker environment. <br>
Risk: Realtime notifications can send worker activity to configured targets. <br>
Mitigation: Review notification channel and target settings before enabling realtime messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kilb/mine) <br>
- [Project homepage](https://github.com/awp-core/subnet-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON status/configuration examples, and concise command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch or manage a background worker that writes status, history, config, startup, and log files under /tmp.] <br>

## Skill Version(s): <br>
0.19.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
