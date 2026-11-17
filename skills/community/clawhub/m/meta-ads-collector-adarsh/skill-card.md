## Description:

Collects active Meta ads for a brand, reporting total ads, formats, ad types, longest-running ad duration, and estimated spend if available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing operations teams use this skill to query the Meta Ad Library for brand advertising activity and feed paid ads strategy reporting with summarized ad metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Meta API credentials provided through environment variables, and service or SDK errors may expose sensitive details in logs.

Mitigation: Confirm credential handling before installation and configure logging so Meta access tokens, app secrets, and sensitive API error details are not recorded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/meta-ads-collector-adarsh)
- [Meta Ad Library API endpoint](https://graph.facebook.com/v19.0/ads_archive)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with TypeScript interfaces, implementation guidance, and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces collector design guidance and a typed MetaAdsData result shape with graceful error handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
