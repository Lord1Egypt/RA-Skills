## Description: <br>
Route each incoming message to the right Bankr/OpenClaw model or to a zero-LLM path based on task type, risk, and cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose a Bankr model or zero-LLM route for each incoming aaigotchi/OpenClaw message based on task type, risk, and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake a model-routing recommendation for approval to perform wallet signing, approvals, fund transfers, or other security-sensitive actions. <br>
Mitigation: Keep separate human or policy approval for wallet actions, and force the high-stakes route when a request is ambiguous or financially important. <br>


## Reference(s): <br>
- [Model Brain ClawHub Release](https://clawhub.ai/aaigotchi/model-brain) <br>
- [Routing Table](artifact/references/routing-table.md) <br>
- [Bankr Models Available to aaigotchi](artifact/references/bankr-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text, JSON, or shell-style environment lines with route, fallback, risk, task type, and reason] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory routing recommendations only; it does not execute wallet actions or approve transactions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
