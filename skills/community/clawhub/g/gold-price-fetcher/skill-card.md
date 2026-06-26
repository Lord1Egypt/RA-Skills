## Description: <br>
Fetches real-time gold price data from the JD Finance API and returns a timestamped price response when users ask for current gold prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayhenry00](https://clawhub.ai/user/jayhenry00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to answer current gold price questions by running the included Python lookup and returning a timestamped price for reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTPS requests to JD Finance and depends on that endpoint's availability and accuracy. <br>
Mitigation: Install only where that network access is acceptable and treat returned prices as informational. <br>
Risk: Displayed prices may differ from executable transaction prices. <br>
Mitigation: Confirm prices with the bank or trading venue before making financial decisions. <br>
Risk: The script writes a local cache file at cache/last_price.json. <br>
Mitigation: Review local write permissions and clear the cache if stale local price data should not be reused. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayhenry00/gold-price-fetcher) <br>
- [JD Finance gold price endpoint](https://ms.jr.jd.com/gw2/generic/CreatorSer/newh5/m/getFirstRelatedProductInfo) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text timestamped price line, with script-level success or error data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cache/last_price.json with the last fetched price and timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
