## Description:

Creates Miaoying online forms, surveys, polls, appointment bookings, exams, query tables, data exports, and QR codes through a bundled Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creatorkuang](https://clawhub.ai/user/creatorkuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create and manage Miaoying form-based workflows such as check-ins, sign-ups, polls, appointment bookings, exams, query tables, exports, and QR-code sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a reusable Miaoying API key in ~/.miaoying/config.json after WeChat login.

Mitigation: Prefer MIAOYING_API_KEY from a secure secret store; if local storage is used, restrict permissions on ~/.miaoying/config.json and exclude it from source control.

Risk: The skill depends on mutable remote prompt and configuration content from the Miaoying service.

Mitigation: Review fetched prompt/configuration content before allowing the agent to create or update activities.

Risk: Broad form creation or export requests may send unintended activity data to the Miaoying service.

Mitigation: Confirm the intended activity type, fields, recipients, and export scope before running CLI commands or API calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/creatorkuang/skills/miaoying)
- [Miaoying OpenAPI Prompt Endpoint](https://www.aiphoto8.cn/api/openapi/prompts)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration examples, and generated QR-code or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Miaoying API key and network access to the Miaoying service.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence; artifact package.json and skill.json report 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
