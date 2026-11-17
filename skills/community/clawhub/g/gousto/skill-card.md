## Description:

Search and browse 9,000+ Gousto recipes. Get full ingredients and step-by-step cooking instructions via official API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhruvkelawala](https://clawhub.ai/user/dhruvkelawala)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to search Gousto recipes, retrieve ingredients, and get step-by-step cooking instructions through command-line scripts that agents can call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Gousto's API and depends on external network availability.

Mitigation: Install it only in trusted workspaces and review network use before enabling it in restricted environments.

Risk: The cache updater creates local recipe cache files and uses a temporary file under the skill's data directory.

Mitigation: Run the cache updater from a trusted, non-shared directory until temporary-file handling is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhruvkelawala/skills/gousto)
- [Gousto recipe listing API](https://production-api.gousto.co.uk/cmsreadbroker/v1/recipes?limit=50&offset=0)
- [Gousto recipe detail API](https://production-api.gousto.co.uk/cmsreadbroker/v1/recipe/{slug})
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Structured JSON and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search uses a local recipe cache; full recipe retrieval and cache refresh require network access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
