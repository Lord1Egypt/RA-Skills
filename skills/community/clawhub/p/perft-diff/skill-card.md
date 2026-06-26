## Description: <br>
Finds an incorrect or missing move in a user's chess engine by comparing perft results with Stockfish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ottofreund](https://clawhub.ai/user/ottofreund) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and chess engine authors use this skill to narrow a perft mismatch to the move sequence that exposes an illegal or missing generated move. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run local perft commands and may rely on helper scripts or chess test files supplied by the user. <br>
Mitigation: Install Stockfish only from trusted package sources and use the skill with chess engine test files or helper scripts you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ottofreund/perft-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command snippets and perft comparison notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the move sequence leading to the perft anomaly; expects Stockfish to be available locally.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
