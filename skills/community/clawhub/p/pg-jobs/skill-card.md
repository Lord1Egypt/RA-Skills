## Description: <br>
Pg Jobs helps agents interact with the ProxyGate job marketplace and bounty board by listing jobs, creating bounties, claiming work, submitting results, and managing the job lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to manage ProxyGate bounty workflows, from browsing and creating escrow-backed jobs through claiming, submitting, accepting, rejecting, canceling, or refunding work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ProxyGate job and escrow commands may create, claim, submit, accept, reject, cancel, deposit, withdraw, lock, release, or refund funds as real account actions. <br>
Mitigation: Confirm the job ID, reward amount, deadline, wallet or account, and escrow action before running commands that change job state or move funds. <br>
Risk: Broad trigger wording such as gigs, freelance tasks, bounty, or job board can cause the skill to activate for ambiguous marketplace requests. <br>
Mitigation: Confirm the user intends to use ProxyGate job-marketplace workflows before producing create, claim, submit, accept, reject, cancel, deposit, withdraw, or listing-management commands. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [Pg Jobs on ClawHub](https://clawhub.ai/jwelten/pg-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ProxyGate CLI commands that perform account, wallet, job, and escrow actions.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
