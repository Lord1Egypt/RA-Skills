## Description: <br>
Create a new git escrow bounty for a test suite. Use when the user wants to submit a challenge with escrowed token rewards for passing a failing test suite. Requires the git-escrows CLI (npm i -g git-escrows). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a git escrow bounty for a failing test suite by collecting repository, commit, reward, token, oracle, and arbiter inputs, then submitting them through the git-escrows CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create live blockchain escrow transactions that lock ERC20 tokens using wallet credentials. <br>
Mitigation: Use a dedicated low-balance wallet and require the agent to show the repo, commit, network, reward, token, oracle, arbiter, and exact command before approving submission. <br>
Risk: The skill relies on a `.env` file containing a private key. <br>
Mitigation: Protect the `.env` file, avoid sharing it with the agent beyond the required local execution context, and prefer a trusted pinned git-escrows CLI. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/arkhai-io/git-commit-trading) <br>
- [ClawHub skill page](https://clawhub.ai/mlegls/make-git-escrow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports escrow submission details and follow-up commands when execution succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
