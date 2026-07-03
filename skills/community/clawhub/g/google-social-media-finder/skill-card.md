## Description: <br>
Searches Google for public social media profiles associated with a person, brand, or username and returns platform names, profile URLs, usernames, snippets, and follower-count text when visible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up public social media profiles for a person, brand, or username from Google search results. It is suited for small, user-directed public lookups where platform, URL, username, snippet, and follower-count text need to be collected and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags instructions for stealth multi-session scraping and rate-limit avoidance. <br>
Mitigation: Use the skill only for small, user-directed public lookups; avoid stealth batching and rate-limit avoidance unless there is clear authorization and a compliant data-access path. <br>
Risk: Search results can be incomplete, duplicated, localized, or affected by Google layout changes. <br>
Mitigation: Verify important profile URLs manually, deduplicate by base URL when needed, and treat snippets and follower counts as display text rather than authoritative records. <br>
Risk: Collected profile URLs, snippets, and follower-count text may include personal data. <br>
Mitigation: Limit collection to legitimate public-profile lookup needs, minimize retention, and avoid using the output for sensitive or unauthorized profiling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/google-social-media-finder) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, JSON] <br>
**Output Format:** [Markdown guidance with shell command templates and JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include platform, username, URL, title, snippet, and follower-count text when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
