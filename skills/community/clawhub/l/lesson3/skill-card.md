## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft, revise, evaluate, benchmark, package, and improve agent skills through an iterative workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scanner verdict is suspicious because the release has local side effects and packaging or privacy concerns. <br>
Mitigation: Review the skill contents before installing, including the hidden memory file and unrelated daily-menu files identified in the evidence. <br>
Risk: Packaging workflows may include dotfiles, logs, credentials, private notes, or unrelated folders if pointed at a broad directory. <br>
Mitigation: Package only the intended skill directory and inspect the archive contents before distribution. <br>
Risk: Evaluation helpers may use the local Claude CLI session and create temporary .claude command files. <br>
Mitigation: Run eval helpers only in the intended project and review generated commands, workspaces, and result files. <br>
Risk: The local review viewer may launch a local server and terminate a process already using the selected port. <br>
Mitigation: Check the selected port before starting the viewer or choose a dedicated port for review sessions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yequanzheng/lesson3) <br>
- [Skill Creator instructions](artifact/SKILL.md) <br>
- [Evaluation and benchmark schemas](artifact/references/schemas.md) <br>
- [Benchmark analyzer guidance](artifact/agents/analyzer.md) <br>
- [Blind comparison guidance](artifact/agents/comparator.md) <br>
- [Assertion grading guidance](artifact/agents/grader.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, shell commands, generated reports, and packaged skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate evaluation workspaces, benchmark summaries, HTML review pages, temporary command files, and packaged skill archives.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
