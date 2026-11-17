## Description:

Turn product images and campaign copy into polished seasonal promo posters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, designers, and commerce operators use this skill to convert product image URLs, concise campaign copy, and a chosen holiday or shopping event into a finished seasonal promotional poster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles a user-provided mew.design API key, which could be exposed if copied into logs or reused too broadly.

Mitigation: Use a low-privilege or newly created API key, avoid sharing it outside the active task, and rotate it if it may have appeared in logs.

Risk: Local or attached product images may need to be uploaded to an external file host before they can be used as public image URLs.

Mitigation: Prefer user-provided public URLs and upload local images only after explicit consent to the privacy tradeoff.

Risk: Changing the validator base URL could send key-validation traffic away from the expected mew.design service.

Mitigation: Keep validation pointed at the default mew.design endpoint unless the user intentionally supplies a trusted alternative.

## Reference(s):

- [Holiday Promo Poster Presets](references/holiday-presets.md)
- [ClawHub Skill Page](https://clawhub.ai/shuminliu026/skills/holiday-promo-poster)
- [Mew Design Generate API Endpoint](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with image links, a short campaign summary, and helper command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON request bodies for the Mew design API during poster generation.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
