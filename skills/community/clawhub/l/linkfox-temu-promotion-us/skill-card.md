## Description:

This skill helps agents work with Temu US promotion workflows through LinkFox gateway scripts for Partner US Promotion APIs, including activity queries, candidate goods lookup, enrollment, operation status checks, and goods updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, operators, and developers use this skill to prepare and run US marketplace promotion API calls through LinkFox, including promotion discovery, product enrollment, and promotion goods updates.

### Deployment Geography for Use:

United States (Temu US marketplace)

## Known Risks and Mitigations:

Risk: The skill requires LinkFox and Temu merchant credentials.

Mitigation: Use only trusted environments, keep workspaces private, and protect or delete local token files when the task is complete.

Risk: Generic proxy and file-download scripts can reach beyond the six promotion-specific workflows.

Mitigation: Prefer the promotion-specific scripts and review requested API types before running broader proxy or download commands.

Risk: Full API responses are persisted to local files and may contain sensitive merchant or campaign data.

Mitigation: Review saved response locations, restrict file access, and remove local response files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-promotion-us)
- [API reference](references/api.md)
- [Partner US Promotion catalog](references/partner-us-catalog.md)
- [Temu access token guide](references/access-token.md)
- [Promotion API documentation index](references/apis/README.md)
- [bg.promotion.activity.query Partner documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=05820fed7179430c8e353905692d51b6)
- [bg.promotion.activity.candidate.goods.query Partner documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=0a11814e7d4146b595918ff3c0f3e239)
- [bg.promotion.activity.goods.enroll Partner documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=27a87ec9d0d94273a48096c050f17854)
- [bg.promotion.activity.goods.operation.query Partner documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=57a37eb5dd104e3f9f90118e3276b291)
- [bg.promotion.activity.goods.update Partner documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=29959238217c41f38f5904e32bf1d14f)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts print small JSON responses directly and summarize larger responses while saving the full response under a local linkfox session directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
