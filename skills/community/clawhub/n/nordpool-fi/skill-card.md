## Description: <br>
Hourly electricity prices for Finland with optimal EV charging window calculation (3h, 4h, 5h). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovaris](https://clawhub.ai/user/ovaris) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to fetch public Finnish electricity prices and identify lower-cost 3h, 4h, and 5h charging windows for energy-intensive tasks such as EV charging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Porssisahko.net whenever it runs. <br>
Mitigation: Install only where contacting that public price API is acceptable for the deployment environment. <br>
Risk: Charging-window times may be inaccurate around Finnish daylight-saving-time behavior. <br>
Mitigation: Check daylight-saving-time behavior, especially during Finnish summer time, before relying on the calculated windows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ovaris/nordpool-fi) <br>
- [Porssisahko latest prices API](https://api.porssisahko.net/v2/latest-prices.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis] <br>
**Output Format:** [JSON object printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current price, current-hour average, optimal 3h/4h/5h charging windows, and daily average/min/max statistics.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence; artifact package.json reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
