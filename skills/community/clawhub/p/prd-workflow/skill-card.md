## Description: <br>
Complete PRD workflow with integrated review, flowchart, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, analysts, and development teams use this skill to turn unclear requirements into PRDs, review findings, Mermaid flowcharts, HTML prototypes, quality checks, and Word exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install process may mutate the host environment through a postinstall hook. <br>
Mitigation: Review installation behavior before use and remove or disable the postinstall hook in sensitive environments. <br>
Risk: The package includes hardcoded internal-login credentials according to the authoritative security scan. <br>
Mitigation: Delete the credentials, rotate any exposed secrets, and review the affected automation before deployment. <br>
Risk: Path handling and shell or AppleScript invocation may allow unsafe execution or writes. <br>
Mitigation: Constrain output paths and replace shell-string or AppleScript path handling with safe argument APIs. <br>
Risk: Documentation may not fully disclose CDN/API use, browser automation, local storage paths, subagent use, and cleanup behavior. <br>
Mitigation: Update user-facing documentation so operators can review these behaviors before installation or execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gotomanutd-dot/prd-workflow) <br>
- [PRD Workflow README](artifact/README.md) <br>
- [Release v5.1.0 Notes](artifact/RELEASE-v5.1.0.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown PRDs and reviews, Mermaid diagrams, HTML prototype code, JSON workflow state, and Word export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow output is written under per-user and per-project output directories with version snapshots.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release, clawhub.json, SKILL.md, and RELEASE-v5.1.0.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
