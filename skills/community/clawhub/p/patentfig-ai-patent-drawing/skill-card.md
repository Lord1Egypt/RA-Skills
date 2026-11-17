## Description:

Generate patent-office-compliant figures via the PatentFig AI API: patent line art from text, vectorize drawings, upscale images, and convert files to filing-ready formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toplocalai](https://clawhub.ai/user/toplocalai)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and patent practitioners use this skill to guide agents through generating, vectorizing, enhancing, and converting patent figures with PatentFig AI. It is suited for preparing USPTO/EPO-style drawings and filing-ready image outputs when the user has a PatentFig AI API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent prompts, invention descriptions, drawings, images, or files may be sent to PatentFig AI.

Mitigation: Confirm the user trusts PatentFig AI and is allowed to submit the relevant invention material before using the API.

Risk: README install commands reference mutable sources rather than an immutable release.

Mitigation: Prefer a pinned release or reviewed commit when installing the skill.

Risk: API credentials could be exposed if copied into prompts, files, commands, or logs.

Mitigation: Keep PATENTFIG_API_KEY in the environment and do not print, hardcode, or store it in files.

Risk: Some operations consume PatentFig AI credits.

Mitigation: State the operation and credit cost, check balance for batches, and obtain user confirmation immediately before billable calls.

## Reference(s):

- [PatentFig AI API Endpoint Reference](references/endpoints.md)
- [PatentFig AI Documentation](https://patentfig.ai/docs)
- [PatentFig AI OpenAPI Specification](https://patentfig.ai/api/openapi.yaml)
- [PatentFig AI Homepage](https://patentfig.ai)
- [TopLocalAI patentfig-skill Repository](https://github.com/TopLocalAI/patentfig-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PATENTFIG_API_KEY and user confirmation before credit-consuming API calls.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
