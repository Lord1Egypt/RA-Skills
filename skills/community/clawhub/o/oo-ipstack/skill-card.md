## Description:

ipstack (ipstack.com). Use this skill for ANY ipstack request — searching and reading data. Whenever a task involves ipstack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up current or supplied IPv4 and IPv6 addresses and retrieve ipstack geolocation data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup commands can run remote code and make lasting local changes; the remote installers were unavailable during review.

Mitigation: Install a reviewed, fixed oo CLI release yourself, inspect setup steps, and require approval before future installation changes; check whether bundled-skill synchronization is acceptable.

Risk: Lookup addresses pass through OOMOL to ipstack.

Mitigation: Use the lookup workflow only for addresses permitted to be shared with those services.

## Reference(s):

- [ipstack API documentation](https://docs.apilayer.com/ipstack/docs/api-documentation)
- [ipstack](https://ipstack.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results may include geolocation data; responses include an execution ID.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
