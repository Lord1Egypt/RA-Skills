## Description: <br>
OpenClaw-Skill-Creator helps agents create, edit, optimize, evaluate, benchmark, and improve skills, including trigger-description refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nattsukun](https://clawhub.ai/user/nattsukun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to draft or revise skills, create evaluation prompts, run comparative evaluations and benchmarks, and review outputs during iterative skill development. It is most appropriate for non-sensitive skill work or isolated workspaces because the security evidence flags external CLI calls and local file side effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can send skill content, prompts, and evaluation data through the configured Claude CLI session. <br>
Mitigation: Use only with non-sensitive skill material, review what will be sent before running evaluations, or run in an isolated environment with controlled credentials. <br>
Risk: Helper scripts can write into local Claude project files and create temporary evaluation or review artifacts. <br>
Mitigation: Run from a dedicated workspace and inspect generated files before reusing or committing them. <br>
Risk: The review server behavior can terminate an existing local process on the selected port. <br>
Mitigation: Prefer static review output or choose an unused port after checking local processes. <br>
Risk: The release is flagged as suspicious by clawscan and the artifact changelog recommends a safer successor. <br>
Mitigation: Prefer the documented safer successor when available; otherwise inspect scripts before execution and avoid server mode unless its behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nattsukun/openclaw-skill-creator-th) <br>
- [Skill creator schemas](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML] <br>
**Output Format:** [Markdown guidance with code blocks, JSON evaluation artifacts, benchmark summaries, and optional HTML review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill files, evaluation metadata, benchmark files, grading results, and local review artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
