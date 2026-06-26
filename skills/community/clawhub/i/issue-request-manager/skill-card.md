## Description: <br>
Issue Request Manager helps agents create, track, update, assign, prioritize, close, and notify stakeholders about issue requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viv888-AI](https://clawhub.ai/user/Viv888-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and project managers use this skill to manage issue request lifecycles, including creation, tracking, replies, assignments, priority changes, closure, local persistence, and optional Enterprise WeChat notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue records may contain sensitive project, customer, or security details and are persisted locally. <br>
Mitigation: Limit sensitive ticket content, protect the local data path, and apply normal access controls and retention practices for stored issue data. <br>
Risk: Enterprise WeChat notifications can expose selected issue details or credentials if recipients or secrets are mishandled. <br>
Mitigation: Keep the WeChat Secret out of committed files, verify recipient lists before enabling notifications, and avoid sending secrets or sensitive customer/security details in notification bodies. <br>
Risk: Runtime dependencies and network notification behavior may change if dependencies are installed without review. <br>
Mitigation: Pin or audit dependencies before production use and review outbound notification behavior in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viv888-AI/issue-request-manager) <br>
- [README](artifact/README.md) <br>
- [Notification guide](artifact/NOTIFICATION_GUIDE.md) <br>
- [Configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, JSON configuration, and issue/status data returned as strings or dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write issue data to a local JSON file and can send selected issue details through Enterprise WeChat when notification credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
