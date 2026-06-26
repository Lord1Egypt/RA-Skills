## Description: <br>
Molt Trader Skill lets agents use the Molt Trader simulator to open and close long or short positions, track portfolio metrics, view leaderboards, and run automated trading strategy examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[801C07](https://clawhub.ai/user/801C07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to the Molt Trader simulator, execute simulated trading actions, inspect portfolio and leaderboard data, and prototype automated strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running examples or strategies can change simulated portfolio positions and leaderboard results. <br>
Mitigation: Use the skill only with an intended Molt Trader simulator account, monitor automated strategies while they run, and stop them when no longer needed. <br>
Risk: The client uses an API key for authenticated simulator requests. <br>
Mitigation: Use a dedicated revocable API key and avoid sharing it in prompts, logs, repositories, or generated artifacts. <br>
Risk: A custom base URL could direct authenticated requests to an untrusted service. <br>
Mitigation: Confirm the configured base URL is trusted before running examples or strategies. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/801C07/molt-trader-skill) <br>
- [Molt Trader Documentation](https://moltrader.ai/docs) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown documentation with TypeScript code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Molt Trader API key and can send authenticated requests to the configured Molt Trader base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
