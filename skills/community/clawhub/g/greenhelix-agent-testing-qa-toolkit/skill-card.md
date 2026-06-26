## Description: <br>
A testing guide for multi-agent commerce systems covering integration testing, mock strategies, chaos testing, contract validation, performance benchmarking, CI/CD, and canary releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this guide to plan and implement testing for multi-agent commerce workflows, including sandbox integration tests, recorded playback, chaos scenarios, contract checks, benchmarks, and progressive release controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied examples could affect real GreenHelix accounts, funds, escrows, or wallet-affecting workflows if run with production credentials. <br>
Mitigation: Keep examples in sandbox or staging by default and require explicit approval before production deploys, canary rollouts, escrow releases, or wallet-affecting tests. <br>
Risk: Recorded test cassettes could capture production keys, secrets, or sensitive account data if created against the wrong environment. <br>
Mitigation: Never record cassettes with production keys or secrets, and review cassette diffs before committing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mirni/greenhelix-agent-testing-qa-toolkit) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API documentation](https://api.greenhelix.net/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with Python examples and CI/CD configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing guide; adapted live examples may require GREENHELIX_API_KEY.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
