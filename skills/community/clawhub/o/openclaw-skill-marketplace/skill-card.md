## Description: <br>
OpenClaw Skill Marketplace helps users discover, search, rank, recommend, sync, and install OpenClaw skills from ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to browse ClawHub skills, search in English or Chinese, get recommendations by scenario, industry, or role, and install selected skills into their local OpenClaw skills directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact ClawHub, run npx clawhub commands, write synced metadata, and install additional skills into the OpenClaw skills directory. <br>
Mitigation: Review skill names before installing, run commands only in a trusted OpenClaw workspace, and treat installed third-party skills as separate code that must be reviewed and trusted. <br>
Risk: The security summary says the artifact's documentation understates network use and local changes. <br>
Mitigation: Validate expected network access and file writes before deployment instead of relying only on the artifact's security notes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/williamwg2025/openclaw-skill-marketplace) <br>
- [Publisher Profile](https://clawhub.ai/user/williamwg2025) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown documentation with shell command examples and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw skill metadata, write synced marketplace metadata, and invoke ClawHub CLI commands when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
