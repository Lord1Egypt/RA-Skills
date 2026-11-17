## Description:

Provides multilingual query and analysis support for Northern Europe, Australia, New Zealand, and Canada market policies, regulations, and investment-environment information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, analysts, and agent developers can use this skill to query policy categories and generate basic investment-environment summaries for Northern Europe, Australia, New Zealand, and Canada market work. The artifact behaves as a mock/demo-quality helper unless real data-source handling is corrected and validated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured data-source or API-key values may be returned in query results and stored in the in-memory cache.

Mitigation: Do not configure real API keys or sensitive endpoint credentials as dataSources until the implementation redacts secrets from returned objects and cached values.

Risk: The artifact claims real-time or API-backed policy collection, but the implementation returns mock policy and analysis data.

Mitigation: Treat outputs as illustrative guidance unless live data integration is implemented, tested, and documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-europe-anz-policy)
- [Huimai documentation](https://docs.huimai.ai)
- [DeepSeek](https://deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime methods return JavaScript objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English responses, category-based policy query results, investment analysis summaries, and cached mock results.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json, README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
