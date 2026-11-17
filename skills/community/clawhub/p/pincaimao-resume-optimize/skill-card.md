## Description:

聘才猫（Pincaimao）简历优化 helps an agent upload a resume and target job description to Pincaimao's API to optimize or rewrite the resume for the role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect a job description and resume file, upload the resume to Pincaimao, and return optimized resume content in a readable form or as raw API output when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume files and job descriptions are sent to Pincaimao's third-party API and uploaded files are stored in Pincaimao COS.

Mitigation: Require explicit user confirmation before uploads and use the skill only when Pincaimao's privacy and retention terms are acceptable for the resume data.

Risk: The skill requires the companion pincaimao-basic skill without server evidence of a pinned source or exact version.

Mitigation: Verify the source and exact version of pincaimao-basic before allowing an agent to install or load it.

Risk: The API key authorizes uploads and resume optimization requests against the user's Pincaimao account.

Mitigation: Keep PCM_RESUME_OPTIMIZE_KEY in the environment only, avoid hardcoding it, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-resume-optimize)
- [Pincaimao homepage](https://www.pincaimao.com)
- [Pincaimao agent login](https://www.pincaimao.com/agents/login?invite_code=uwqc)
- [Pincaimao API endpoint](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or raw API answer text, with bash snippets for example API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a readable summary of the API answer; raw output mode returns the answer field or concatenated streaming answer fragments without rewriting.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
