## Description:

Provides agent tools for listing, searching, and inspecting Hong Kong DATA.GOV.HK datasets, categories, and file formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route open-data questions to tools that list datasets, inspect dataset or category details, search by query, and filter results by file format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill depends on XiaoBenYang as a proxy for DATA.GOV.HK data.

Mitigation: Install only if that proxy is intentional and acceptable; prefer a version that directly accesses DATA.GOV.HK when direct provenance or routing is required.

Risk: The security evidence says the skill stores the XiaoBenYang API key in a plaintext .env file.

Mitigation: Use a dedicated non-sensitive key, keep .env out of source control, and prefer a safer secret store for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/open-data-hk)
- [XiaoBenYang API key service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown or plain text summaries based on JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY and returns normalized success, raw, and message fields from upstream calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
