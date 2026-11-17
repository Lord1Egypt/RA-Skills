## Description:

Explore and analyze public Facebook data through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to answer questions about public Facebook profiles, pages, posts, Reels, photos, groups, and future events through documentation-guided KeyAPI workflows. It helps agents resolve current endpoint docs, authenticate locally, execute live API calls, and return concise analysis or structured reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KeyAPI bearer tokens may be persisted in shell profile files.

Mitigation: Prefer session-scoped KEYAPI_TOKEN values or a safer secret store, avoid entering real tokens while screen sharing, and review shell profile permissions before use.

Risk: The authenticated API helper can run broad live Facebook data workflows and save complete response files.

Mitigation: Confirm report scope, pagination depth, and output-file paths before execution; protect or delete saved response files after analysis.

Risk: Reports can overstate what public API data proves.

Mitigation: Separate observed API fields from inference, use current KeyAPI docs for endpoint contracts, and avoid inferring private, demographic, or membership data not returned by the API.

## Reference(s):

- [KeyAPI documentation index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [Facebook profile ID](https://docs.keyapi.ai/en/facebook/profile_profile_id.md)
- [Facebook profile details by URL](https://docs.keyapi.ai/en/facebook/profile_details_url.md)
- [Facebook profile details by ID](https://docs.keyapi.ai/en/facebook/profile_details_id.md)
- [Facebook profile posts](https://docs.keyapi.ai/en/facebook/profile_posts.md)
- [Facebook profile Reels](https://docs.keyapi.ai/en/facebook/profile_reels.md)
- [Facebook profile photos](https://docs.keyapi.ai/en/facebook/profile_photos.md)
- [Facebook group ID](https://docs.keyapi.ai/en/facebook/group_id.md)
- [Facebook group details](https://docs.keyapi.ai/en/facebook/group_details.md)
- [Facebook group posts](https://docs.keyapi.ai/en/facebook/group_posts.md)
- [Facebook group future events](https://docs.keyapi.ai/en/facebook/group_future_events.md)
- [Global rules](references/global-rules.md)
- [Scenario cards](references/scenarios.md)
- [Routing policy](references/routing-policy.md)
- [Facebook rules](references/facebook-rules.md)
- [Facebook profile rules](references/facebook-profile-rules.md)
- [Facebook profile content rules](references/facebook-profile-content-rules.md)
- [Facebook group rules](references/facebook-group-rules.md)
- [Setup and auth](references/setup-and-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON summaries, helper-script command examples, and optional saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on live KeyAPI responses and should distinguish observed API facts from analysis or inference.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
