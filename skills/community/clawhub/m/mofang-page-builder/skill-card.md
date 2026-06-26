## Description: <br>
Builds Magicflu/Mofang web-table custom pages from the jsonv2 records API, including CRUD pages, H5 extension pages, local mock/proxy debugging, and same-origin publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicscape](https://clawhub.ai/user/magicscape) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate, test, and publish Magicflu/Mofang form, list, record, detail, and CRUD pages using real field definitions and jsonv2 API patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports credentialed Magicflu/Mofang workflows that may use cookies, JWTs, usernames, or passwords. <br>
Mitigation: Use least-privilege test accounts, keep secrets out of source control and shared logs, and prefer staging or sanitized data. <br>
Risk: Generated delete, update, proxy, or publishing flows can affect real business records or sites when pointed at production. <br>
Mitigation: Review generated data-changing and publishing commands before execution, test locally with mock data first, and run against production only with explicit intent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/magicscape/mofang-page-builder) <br>
- [API Summary](references/api-summary.md) <br>
- [Design](references/design.md) <br>
- [Requirements](references/requirements.md) <br>
- [Mock Data README](assets/mock-data/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, generated page code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local mock data workflows, API configuration, and same-origin publishing commands for Magicflu/Mofang environments.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
