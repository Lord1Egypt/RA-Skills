## Description:

Searches media resources through the Prowlarr API and returns torrent, Usenet, and magnet-link results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhxyz](https://clawhub.ai/user/pengzhxyz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query their configured Prowlarr instance for movies, TV episodes, torrents, Usenet releases, and magnet links. It is useful when an agent needs structured media search results with title, size, indexer, link, and publish date fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Prowlarr API key in request URLs when querying the configured Prowlarr instance.

Mitigation: Use localhost or a trusted HTTPS PROWLARR_BASE_URL, avoid untrusted proxies, and rotate the Prowlarr API key if request URLs may have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengzhxyz/skills/prowlarr-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON array from the Prowlarr search helper, with error messages emitted as JSON on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a configured Prowlarr API key; accepts query text plus optional media type, season, and episode parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
