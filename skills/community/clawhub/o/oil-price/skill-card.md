## Description:

获取全国各省市油价信息，无需 API Key; use when a user asks about gas prices or fuel costs in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzihao0731](https://clawhub.ai/user/chenzihao0731)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current regional gasoline and diesel prices in China for answers, scripts, or command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to the disclosed v2.xxapi.cn oil price API.

Mitigation: Confirm that using this external API is acceptable for the deployment environment before installing or running the skill.

Risk: The skill depends on curl and jq and can fail if the API is unavailable, rate-limited, or returns an unexpected response.

Mitigation: Install the required binaries and handle command failures or stale data in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzihao0731/skills/oil-price)
- [Oil price API endpoint](https://v2.xxapi.cn/api/oilPrice)
- [API homepage](https://v2.xxapi.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Pipe-delimited text rows with region, 92, 95, 98, and diesel price fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; fetches public oil-price data from the disclosed v2.xxapi.cn API.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
