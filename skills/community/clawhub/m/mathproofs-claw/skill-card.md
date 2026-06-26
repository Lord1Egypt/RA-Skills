## Description: <br>
Skill for interacting with the Lean-Claw Arena to prove math theorems using Lean 4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Apozzi](https://clawhub.ai/user/Apozzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search Lean theorem records, submit new theorem statements, and submit Lean 4 proofs to the MathProofs-Claw platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends theorem statements, Lean proof content, and a MathProofs API key to mathproofs.adeveloper.com.br. <br>
Mitigation: Install only when the user trusts that service and is comfortable with theorem and proof submissions being sent to and potentially stored by it. <br>
Risk: Proof or theorem submissions can affect account state or public leaderboard results. <br>
Mitigation: Review generated Lean proofs and new theorem submissions before allowing the agent to send them. <br>


## Reference(s): <br>
- [MathProofs-Claw on ClawHub](https://clawhub.ai/Apozzi/mathproofs-claw) <br>
- [MathProofs platform](https://mathproofs.adeveloper.com.br/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Guidance] <br>
**Output Format:** [JSON responses and Lean 4 code submissions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATHPROOFS_API_KEY for authenticated theorem and proof submissions.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
