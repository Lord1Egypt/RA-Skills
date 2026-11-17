## Description:

Generates professional AI product photos with ProductAI.photo for e-commerce, marketing, catalogs, and campaigns, including background replacement, product placement, scene generation, compositing, and upscaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shapes-2](https://clawhub.ai/user/shapes-2)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, marketers, and e-commerce teams use this skill to configure ProductAI access, generate product photos from image URLs, create lifestyle or catalog visuals, upscale images, and run batch generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived ProductAI API keys.

Mitigation: Use the official ProductAI endpoint, avoid sharing API keys in ordinary chat or logs, store credentials with user-only permissions, and rotate any key that may have been exposed.

Risk: Product images and generated outputs are sent to and downloaded from a third-party service.

Mitigation: Submit only images that are appropriate for ProductAI's handling terms, avoid confidential or rights-restricted material unless approved, and treat downloaded image results as untrusted remote content.

Risk: Generation and upscaling consume ProductAI tokens and can create unexpected cost if used carelessly.

Mitigation: Monitor ProductAI token usage, respect the documented rate limits, and use batch workflows deliberately.

## Reference(s):

- [ProductAI Website](https://www.productai.photo)
- [ProductAI API Reference](references/API.md)
- [ProductAI Integration Guide](references/INTEGRATION_GUIDE.md)
- [Quick Start Guide](QUICKSTART.md)
- [Setup Guide](SETUP-GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/shapes-2/skills/productai-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, API requests, and generated or upscaled image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ProductAI API jobs, may print job IDs or result URLs, and can download generated images to local output paths.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and CHANGELOG list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
