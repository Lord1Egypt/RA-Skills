## Description: <br>
Generate lottery numbers and check results. Use when picking numbers for draws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to generate random lottery number picks for generic draws, Powerball, and Mega Millions, compare entered numbers with winning numbers, and view local history or statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell commands may read or create local files for lottery history. <br>
Mitigation: Review commands before execution and run them in an environment where ~/.local/share/lottery/ access is acceptable. <br>
Risk: Lottery number generation is random helper output and does not improve the odds of winning. <br>
Mitigation: Treat generated numbers as convenience output only and verify any draw results against official lottery sources. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local shell execution and may read lottery history from ~/.local/share/lottery/.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
