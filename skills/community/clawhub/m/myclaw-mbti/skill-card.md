## Description: <br>
Claw Mbti analyzes recent natural-language interactions with the agent to produce a playful MBTI-style personality report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users invoke this skill to receive an MBTI-style report based on recent conversation patterns, with fallback guidance when interaction history is missing or sparse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill profiles the user from recent conversation history and memory without a clearly documented opt-in flow. <br>
Mitigation: Invoke the skill explicitly, avoid sharing reports that include private interaction details, and review whether history-based profiling is appropriate before use. <br>
Risk: The artifact includes Git-based installation commands that users may copy into an agent session. <br>
Mitigation: Prefer vetted ClawHub installation commands, or review the project repository before using remote Git installation commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoyang0807/myclaw-mbti) <br>
- [Project Homepage](https://github.com/xiaoyang0807/claw-mbti) <br>
- [Reference Manual](reference.md) <br>
- [Type Catalog](types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a table and inline shell commands when installation guidance is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses recent chat history and memory; filters shell, Git, code, and installation content from personality evidence.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
