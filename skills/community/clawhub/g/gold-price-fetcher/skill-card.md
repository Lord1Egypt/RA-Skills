## Description:

Fetches real-time gold price information from a disclosed JD Finance endpoint and returns a timestamped price response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayhenry00](https://clawhub.ai/user/jayhenry00)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to query current reference gold prices and receive a clear timestamped response for informational checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes a network request to JD Finance.

Mitigation: Install only where outbound access to the disclosed endpoint is acceptable.

Risk: The returned gold price is informational and may differ from transaction prices.

Mitigation: Confirm actual transaction prices with the relevant bank or trading venue before making financial decisions.

Risk: The helper script writes a local cache file with the last fetched price and timestamp.

Mitigation: Review local storage expectations before deployment in restricted environments.

## Reference(s):

- [JD Finance gold price endpoint](https://ms.jr.jd.com/gw2/generic/CreatorSer/newh5/m/getFirstRelatedProductInfo)
- [ClawHub skill page](https://clawhub.ai/jayhenry00/skills/gold-price-fetcher)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Timestamped plain text response, with optional JSON fields when the helper script is used programmatically.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a small local cache file containing the last fetched price and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata, README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
