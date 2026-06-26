## Description: <br>
Feed lobsters in the Lobster Farmer game by calling the local CLI command `lobster-farmer feed` with `--model`, `--input-tokens`, `--output-tokens`, and optional `--emotion`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murongg](https://clawhub.ai/user/murongg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users of the Lobster Farmer project use this skill to feed model-specific lobsters, simulate model token usage, and report updated growth metrics through the local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running feed or service commands from the wrong project root, or through an unexpected `lobster-farmer` command, could update unintended local game state. <br>
Mitigation: Before running feed, start, or batch operations, verify the Lobster Farmer project root and confirm that `lobster-farmer` resolves to the expected local command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/murongg/lobster-farmer-feeder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports model name, token values, optional emotion, total tokens, feed count, and size when command output is available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
