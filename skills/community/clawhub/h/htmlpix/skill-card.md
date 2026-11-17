## Description:

Use when the user wants to call, test, or integrate the HTMLPix HTML-to-image API, including auth setup, signed URL minting, image rendering, template CRUD, and AI template generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jymaa](https://clawhub.ai/user/jymaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate code, curl commands, SDK wrapper guidance, and troubleshooting responses for HTMLPix API integrations. It supports server-side image URL minting, template management, image rendering, and AI-assisted template generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may prepare or run HTMLPix API requests using HTMLPIX_API_KEY.

Mitigation: Keep the API key server-side, avoid browser client calls to private endpoints, and review commands before execution.

Risk: Template code, variables, or generation prompts may be sent to HTMLPix during normal use.

Mitigation: Do not include secrets or private data in template variables, template code, or prompts unless the transfer is intended.

Risk: Changing a minted image URL's query parameters can invalidate the signed URL.

Mitigation: Treat minted URLs as opaque and store or embed the returned URL directly.

## Reference(s):

- [HTMLPix API base URL](https://api.htmlpix.com)
- [HTMLPix API keys](https://htmlpix.com/api-keys)
- [HTMLPix ClawHub skill page](https://clawhub.ai/jymaa/skills/htmlpix)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, endpoint contract summaries, and integration troubleshooting guidance.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
