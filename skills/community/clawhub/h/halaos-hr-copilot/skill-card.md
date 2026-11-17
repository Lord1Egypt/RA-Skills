## Description:

HalaOS HR Copilot helps agents answer Southeast Asia HR questions and, when configured with HalaOS MCP or API access, work with live employee, attendance, leave, payroll, compliance, and organization intelligence data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonypk](https://clawhub.ai/user/tonypk)

### License/Terms of Use:

MIT-0

## Use Case:

HR staff, managers, and authorized employees use this skill to get HR briefings, review leave and payroll information, answer compliance questions, generate HR documents, and inspect workforce intelligence for HalaOS tenants or offline PH/SG/LK HR guidance.

### Deployment Geography for Use:

Southeast Asia, with specific built-in guidance for the Philippines, Singapore, and Sri Lanka.

## Known Risks and Mitigations:

Risk: Broad prompts or shared chat contexts may expose sensitive employee, attendance, leave, payroll, compliance, or risk data from a connected HalaOS tenant.

Mitigation: Use the skill only with authorized users, avoid broad casual prompts in shared chats, and configure a least-privileged HALAOS_API_KEY.

Risk: Payroll, government form, approval, or rejection actions can affect important HR records or compliance outcomes.

Mitigation: Require human review before executing payroll, filing, approval, rejection, or similar state-changing actions.

Risk: Installing the MCP server with an unpinned @latest version can change behavior without review.

Mitigation: Prefer a pinned MCP server version and review release changes before upgrading.

Risk: Flight-risk results depend on background risk scoring and may be stale or unavailable.

Mitigation: Check data freshness and treat empty or unexpected risk results as a signal to verify whether scoring has run before taking action.

## Reference(s):

- [HalaOS Website](https://halaos.com)
- [Linked GitHub Repository](https://github.com/tonypk/aigonhr)
- [ClawHub Skill Page](https://clawhub.ai/tonypk/skills/halaos-hr-copilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell Commands, Configuration, Guidance]

**Output Format:** [Markdown responses with tables, JSON configuration snippets, shell commands, and HR document drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive HR, payroll, compliance, approval, and employee-risk information when connected to a HalaOS tenant.]

## Skill Version(s):

2.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
