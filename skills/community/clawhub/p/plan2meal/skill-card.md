## Description:

Manage recipes and grocery lists in Plan2Meal via chat by adding recipe URLs, listing, searching, showing, and deleting recipes, and creating and managing grocery lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okikesolutions](https://clawhub.ai/user/okikesolutions)

### License/Terms of Use:

MIT

## Use Case:

External Plan2Meal users use this skill to manage their stored recipes and grocery lists through chat commands. Developers or operators configure the Plan2Meal backend and OAuth credentials before enabling authenticated recipe and grocery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes authentication and recipe or grocery data to a configured Plan2Meal backend, with an optional shared backend.

Mitigation: Install only with a trusted HTTPS CONVEX_URL, enable the shared backend only intentionally with ALLOW_DEFAULT_BACKEND=true, and disclose backend routing in relevant responses.

Risk: OAuth login grants temporary access to provider profile tokens and Plan2Meal recipe or grocery data.

Mitigation: Configure only needed OAuth providers, protect client secrets, avoid exposing tokens in output, and prefer scoped Plan2Meal tokens bound to authenticated sessions.

Risk: Recipe URL ingestion can send user-provided URLs to backend extraction logic.

Mitigation: Restrict accepted URL schemes and targets, reject invalid URLs, and review backend extraction behavior before deployment.

## Reference(s):

- [Plan2Meal Output Templates](references/output-templates.md)
- [Plan2meal ClawHub Skill Page](https://clawhub.ai/okikesolutions/skills/plan2meal)
- [okikesolutions Publisher Profile](https://clawhub.ai/user/okikesolutions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown command responses with IDs, counts, links, errors, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should avoid exposing secrets or tokens and should disclose backend routing when relevant.]

## Skill Version(s):

1.2.5 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
