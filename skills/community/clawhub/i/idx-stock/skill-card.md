## Description:

Scrapes and returns a translated company profile from the Indonesia Stock Exchange website for a supplied IDX stock code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zororaka00](https://clawhub.ai/user/zororaka00)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch public Indonesia Stock Exchange company profile data and normalize Indonesian profile fields into English keys for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live IDX website responses, so output can fail or change if the site is unavailable or its page structure changes.

Mitigation: Handle unsuccessful responses and review downstream assumptions before relying on scraped profile data.

Risk: Dependency versions may vary across environments.

Mitigation: Pin requests and beautifulsoup4 versions in stricter deployments.

Risk: Publisher security claims about VirusTotal compliance are not a substitute for local review.

Mitigation: Use the server security verdict as the authoritative summary and perform environment-specific scanning before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zororaka00/skills/idx-stock)
- [Publisher profile](https://clawhub.ai/user/zororaka00)
- [Indonesia Stock Exchange company profile source](https://www.idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Structured JSON-like result with a success flag, company profile data object, and status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an IDX stock code string and makes a live read-only HTTP GET request to the IDX website.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
