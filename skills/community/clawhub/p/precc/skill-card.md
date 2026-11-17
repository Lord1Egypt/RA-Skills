## Description:

Predictive Error Correction for Claude Code — corrects bash commands before execution, predicts token costs via a trained ML oracle, and captures opt-in counterfactual telemetry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yijunyu](https://clawhub.ai/user/yijunyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code or the DeepSeek Harness can use PRECC to correct Bash commands, reduce verbose tool output, search code semantically, compress context files, and estimate token costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions pipe a remote script directly into a shell.

Mitigation: Review the installer and verify its source and contents before running it.

Risk: The security review reports session-history mining and capabilities beyond the stated purpose, and the scan was partial because a referenced local path was missing.

Mitigation: Review the installer's and skill's data access before installation, and treat the available scan as incomplete.

## Reference(s):

- [PRECC project repository](https://github.com/peri-a-i/precc-cc)
- [PRECC releases](https://github.com/peri-a-i/precc-cc/releases)
- [cocoindex-code project](https://github.com/cocoindex-io/cocoindex-code)
- [RTK project](https://github.com/rtk-ai/rtk)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Bash commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose corrected commands and compressed command output; behavior depends on local PRECC configuration and learned history.]

## Skill Version(s):

0.3.112 (source: server-resolved release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
