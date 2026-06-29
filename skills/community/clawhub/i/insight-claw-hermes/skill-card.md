## Description: <br>
Download, configure, run, verify, and troubleshoot Insight Claw, an A-share self-selected stock analysis pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geraltjc](https://clawhub.ai/user/geraltjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help Hermes set up, run, verify, and troubleshoot Insight Claw for A-share self-selected stock analysis. The skill guides local validation, configuration, optional GitHub Actions execution, and troubleshooting without treating Insight Claw as an order-execution system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for LLM analysis and optional data, search, and notification providers. <br>
Mitigation: Use Hermes secret handling or user-approved local environment configuration; never display, upload, commit, or overwrite raw secret values. <br>
Risk: The skill can guide dependency installation, repository checkout, local analysis runs, and optional notification or GitHub Actions setup. <br>
Mitigation: Confirm the target checkout and configuration before execution, run the no-notification validation path first, and enable notification or scheduled workflows only after local reports are verified. <br>


## Reference(s): <br>
- [Insight Claw Hermes ClawHub release](https://clawhub.ai/geraltjc/insight-claw-hermes) <br>
- [Insight Claw Quickstart](artifact/references/quickstart.md) <br>
- [Insight Claw Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, dotenv examples, and verification paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps credentials local and uses no-notification validation before optional notification setup.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
