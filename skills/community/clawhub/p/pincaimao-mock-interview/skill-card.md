## Description:

聘才猫 - 模拟面试 Use when calling Pincaimao Mock Interview API to simulate a real interview scenario with multi-turn conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and interview-preparation agents use this skill to run multi-turn mock interviews from a job description, optional resume content, and configurable interview settings. It supports text and video interview flows, custom questions, interviewer role selection, and optional reference answers through Pincaimao's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends resume content, job descriptions, interview answers, and optional media references to api.pincaimao.com.

Mitigation: Use the skill only when that third-party data transfer is acceptable for the user and organization.

Risk: The skill depends on a referenced pincaimao-basic dependency for common API behavior.

Mitigation: Verify pincaimao-basic before installation or use.

Risk: API-key misuse could expose authenticated access to Pincaimao services.

Mitigation: Keep PCM_MOCK_INTERVIEW_KEY scoped, store it as an environment variable, and avoid hardcoding it in prompts or files.

Risk: Copying raw shell examples directly can produce fragile JSON request construction.

Mitigation: Prefer JSON-serialized request construction when adapting the examples for production workflows.

## Reference(s):

- [Pincaimao Homepage](https://www.pincaimao.com)
- [ClawHub Skill Page](https://clawhub.ai/pincaimao/skills/pincaimao-mock-interview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and optional raw API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize API responses for readability or return raw blocking/streaming answer content when requested.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
