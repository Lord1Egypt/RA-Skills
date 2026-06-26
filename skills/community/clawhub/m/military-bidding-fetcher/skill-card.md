## Description: <br>
Fetches public procurement notices from the all-army weapon equipment procurement site, the military procurement site, and the National University of Defense Technology procurement site, then filters results and generates Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect recent military procurement opportunities, filter them by keywords, regions, and exclusion terms, and produce an Excel workbook for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external procurement sites and writes local Excel reports. <br>
Mitigation: Run it only when public procurement scraping is intended, use the explicit /milb-fetcher command, and set the output path deliberately. <br>
Risk: Local .env configuration can change keywords, proxy settings, regions, and output location. <br>
Mitigation: Run the skill from a trusted directory and review .env settings before collection. <br>
Risk: Broad trigger wording may start collection when a user gives a general scraping or procurement request. <br>
Mitigation: Confirm the target date, sites, filters, and report path before running broad collection requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/military-bidding-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console status text and Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .xlsx reports to a configured output path and supports keyword, exclusion keyword, high-value keyword, region, date, and proxy configuration.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
