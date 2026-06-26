## Description: <br>
Predictive Error Correction for Claude Code corrects bash commands before execution, predicts token costs with a trained ML oracle, and captures opt-in counterfactual telemetry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yijunyu](https://clawhub.ai/user/yijunyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use PRECC to reduce failed shell commands, compress command and context output, and estimate token costs while working in Claude Code. The skill is intended for local command-correction and productivity workflows that can tolerate a shell hook reviewing proposed Bash commands before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PRECC persistently configures Claude Code shell-command hooks that can intercept and potentially rewrite Bash commands in later sessions. <br>
Mitigation: Review the exact changes to ~/.claude/settings.json, confirm the hook path points to the expected binary, and understand how to disable or remove the hook before relying on it. <br>
Risk: The installer behavior may be broader than the skill page fully explains. <br>
Mitigation: Inspect the installation path, downloaded binaries, and checksum verification before installing, especially in shared or sensitive development environments. <br>
Risk: Counterfactual telemetry can record would-have-run and did-run command outcomes if explicitly enabled. <br>
Mitigation: Keep telemetry disabled unless intentionally needed, review consent.toml before enabling it, and confirm where local telemetry stores are written. <br>


## Reference(s): <br>
- [PRECC ClawHub skill page](https://clawhub.ai/yijunyu/skills/precc) <br>
- [PRECC repository](https://github.com/peri-a-i/precc-cc) <br>
- [PRECC releases](https://github.com/peri-a-i/precc-cc/releases) <br>
- [cocoindex-code](https://github.com/cocoindex-io/cocoindex-code) <br>
- [cocoindex-code on PyPI](https://pypi.org/project/cocoindex-code/) <br>
- [RTK](https://github.com/rtk-ai/rtk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the precc and precc-hook binaries; may modify Claude Code settings and local PRECC data files; PRECC_LICENSE_KEY is optional for premium features.] <br>

## Skill Version(s): <br>
0.3.108 (source: server release metadata and release changelog; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
