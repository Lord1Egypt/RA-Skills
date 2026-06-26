## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this agent skill to draft new skills, revise existing skills, create test prompts, run evaluations, compare skill behavior, and iterate from review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or revised skill instructions could contain inaccurate, misleading, or overbroad guidance. <br>
Mitigation: Review generated skill descriptions and instructions before adopting or publishing them. <br>
Risk: The skill can guide an agent to write files in the active workspace while drafting skills, evals, benchmarks, or review artifacts. <br>
Mitigation: Run it only in workspaces where file writes are expected and acceptable. <br>
Risk: The workflow may reference local scripts, browser review pages, subagents, and CLI tools for evaluation and iteration. <br>
Mitigation: Confirm referenced local tools and viewer scripts are present and trusted before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PHY041/phy-skill-creator) <br>
- [Canlah AI Homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, JSON snippets, shell commands, and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace files such as SKILL.md drafts, eval metadata, benchmark summaries, feedback files, and static review pages when the host agent permits file writes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
