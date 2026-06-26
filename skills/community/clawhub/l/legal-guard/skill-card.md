## Description: <br>
Prevents agents from autonomously signing contracts, accepting binding terms, confirming subscriptions, or approving wallet signatures by requiring a term summary and explicit one-time user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoofzion](https://clawhub.ai/user/echoofzion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use Legal Guard to force human review before an agent takes actions that may create legal, financial, IP, subscription, or on-chain obligations. The skill is meant for contract signing, Terms of Service acceptance, free-trial checkout, CLA prompts, and wallet-signature workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Standing approvals for legal or financial actions may create unclear future authority. <br>
Mitigation: Use allow-once for contracts, subscriptions, Terms of Service acceptance, CLAs, and wallet signatures; avoid allow-always unless the approval scope, duration, and revocation path are explicit. <br>
Risk: The skill is an instruction-level guardrail, so effectiveness depends on the host agent honoring the protocol. <br>
Mitigation: Review and scan the skill before deployment, and confirm the agent requires formal approval output before any signing, submission, or wallet-signature action. <br>


## Reference(s): <br>
- [ClawHub listing for Legal Guard](https://clawhub.ai/echoofzion/legal-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with approval-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries cover parties, commitments, duration, obligations, IP ownership, governing law, termination, dispute resolution, and red flags when the source material provides them.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
