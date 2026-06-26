## Description: <br>
Which of these addresses are smart money? Batch-profile a list in one call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to batch-profile Ethereum wallet addresses with the Nansen CLI and identify addresses labeled as smart_money or fund. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Nansen API key and submits wallet addresses for profiling. <br>
Mitigation: Install and run it only when you trust the nansen-cli package and are comfortable sharing those wallet addresses with Nansen. <br>
Risk: A broader nansen command could go beyond wallet label lookup. <br>
Mitigation: Review any proposed nansen command before execution and keep usage scoped to the documented batch profiler workflow. <br>
Risk: Invalid wallet addresses can produce per-result errors. <br>
Mitigation: Check each result for an error field and skip errored addresses instead of treating them as successful classifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-wallet-batch) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with bash command examples and filtering guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NANSEN_API_KEY and the nansen CLI; output may include wallet labels, balances, and per-address errors.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
