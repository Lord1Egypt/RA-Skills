## Description:

Brave Rotator uses the Brave Search API with automatic rotation across multiple API keys for web, news, and image search requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to perform Brave Search API web, news, and image lookups while rotating among multiple configured API keys to reduce rate-limit interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists full Brave API keys in the local rotation state file.

Mitigation: Treat the state file as sensitive, restrict file permissions, avoid shared BRAVE_KEY_STATE_FILE paths, and prefer storing non-secret key labels or hashes.

Risk: The skill logs a prefix of the API key used for a request.

Mitigation: Avoid collecting stderr logs in shared locations and remove or mask key-prefix logging before broader deployment.

Risk: Search queries are sent to Brave Search API outside the local environment.

Mitigation: Do not submit confidential, regulated, or sensitive queries unless that data sharing is approved for the intended use.

## Reference(s):

- [Brave Search API Reference](references/brave-api.md)
- [Brave Search API base URL](https://api.search.brave.com/res/v1)
- [ClawHub skill page](https://clawhub.ai/mrnsmh/skills/openclaw-skill-brave-rotator)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or Markdown-formatted search results from Brave Search API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEYS and may use BRAVE_KEY_STATE_FILE for local rotation state.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
