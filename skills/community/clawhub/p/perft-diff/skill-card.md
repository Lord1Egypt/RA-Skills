## Description:

Finds an incorrect or missing move in a user's chess engine by comparing perft results with Stockfish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ottofreund](https://clawhub.ai/user/ottofreund)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building chess engines use this skill to isolate a perft mismatch by comparing engine move counts against Stockfish until it identifies the move sequence that leads to an illegal or missed move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Stockfish and may install the Stockfish package in the user's environment.

Mitigation: Confirm the Stockfish package installation is acceptable before use.

Risk: The workflow may make narrow test or logging changes in the user's chess-engine repository.

Mitigation: Restrict changes to the specified failing test case or a temporary perft logging helper, then review changes before keeping them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ottofreund/skills/perft-diff)
- [Example perft diff workflow](artifact/example.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown narrative with perft logs, Stockfish commands, and the final anomalous move sequence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Stockfish and a user-provided failing perft test case with FEN and depth.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
