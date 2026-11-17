## Description:

Naver Search helps agents retrieve Naver web, news, shopping, image, video, and booking or place results through SerpAPI-backed command-line scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[downwind7clawd-ctrl](https://clawhub.ai/user/downwind7clawd-ctrl)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to collect Korean search results across Naver categories for research, comparison, and answer preparation. It can return compact summaries for reading or JSON for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency loading may prefer user-site Python packages, which can expose the SerpAPI key and search terms if the local environment is unsafe.

Mitigation: Pin and verify the serpapi dependency, remove user-site sys.path precedence before deployment, and run the skill in a dedicated virtual environment.

Risk: Search queries and the SerpAPI key are sent through a third-party search provider.

Mitigation: Avoid sensitive or private queries, store SERPAPI_API_KEY securely, and review provider terms before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/downwind7clawd-ctrl/skills/naver-search)
- [Publisher profile](https://clawhub.ai/user/downwind7clawd-ctrl)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Compact Korean text summaries or JSON search-result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPAPI_API_KEY; search queries and the SerpAPI key are sent through a third-party search provider.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
