## Description: <br>
ManoBrowser lets agents operate a user's logged-in Chrome through a Chrome extension and MCP connection to extract web data, reverse-engineer web APIs, and build reusable browser automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ManoBrowser to automate browser tasks, extract login-gated web data, explore platforms, reverse-engineer APIs, and generate reusable skills from recorded browser workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Chrome session through a remote MCP connection. <br>
Mitigation: Use it only with accounts and browser sessions where delegated automation is acceptable, and avoid banking, healthcare, email, admin consoles, and other highly sensitive services. <br>
Risk: The skill can use cookies and collect sensitive page data while extracting login-gated content. <br>
Mitigation: Review the target site, requested data, and extraction output before reuse, and remove sensitive fields from saved artifacts. <br>
Risk: Generated workflows may perform uploads, submits, publishes, or other state-changing actions. <br>
Mitigation: Require final manual confirmation before any upload, submit, publish, purchase, or account-changing operation. <br>
Risk: Temporary cookie files and detailed workflow logs may persist sensitive session or page information. <br>
Mitigation: Delete temporary cookie files and workflow logs after use, and store any retained artifacts only in approved locations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sophie-xin9/manobrowser) <br>
- [Metadata Homepage](https://github.com/ClawCap/ManoBrowser) <br>
- [Chrome Web Store Listing](https://chromewebstore.google.com/detail/manobrowser/ihlggihggghoiijfcmgkapojamifohfh) <br>
- [Browser Automation Module](browser-automation/SKILL.md) <br>
- [Web Data Extractor Module](web-data-extractor/SKILL.md) <br>
- [API Skill Builder Module](api-skill-builder/SKILL.md) <br>
- [Platform Data Explorer Module](platform-data-explorer/SKILL.md) <br>
- [Chrome Workflow Build Module](chrome-workflow-build/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, JSON snippets, shell commands, and generated skill files or workflow artifacts when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser operation plans, extracted page data, API mappings, reusable skill drafts, workflow logs, and configuration instructions.] <br>

## Skill Version(s): <br>
2.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
