## Description: <br>
Lightcone Browse delegates cloud browser tasks to Lightcone's Northstar automation so agents can browse websites, scrape pages, check prices, monitor sites, fill forms, and operate web applications from natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieogola](https://clawhub.ai/user/eddieogola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to delegate visual web automation, scraping, price checks, site monitoring, form filling, and remote browser operation when a local browser or selector-based script is not suitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a remote browser through Lightcone's cloud automation service, so submitted instructions and page interactions may involve external processing. <br>
Mitigation: Use it only for tasks appropriate for the Lightcone service and avoid private account pages or sensitive data unless that transfer is intended and approved. <br>
Risk: Browser automation can submit forms, interact with purchases, or perform other actions that may be hard to reverse. <br>
Mitigation: Give explicit boundaries in the instruction and require review before credentials, payment details, purchases, or irreversible submissions. <br>
Risk: Automated browsing, scraping, or monitoring can conflict with a site's terms or data-use expectations. <br>
Mitigation: Review the target site's terms and limit tasks to permitted collection and interaction patterns. <br>


## Reference(s): <br>
- [Lightcone Documentation](https://docs.lightcone.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/eddieogola/lightcone-browse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Screenshots] <br>
**Output Format:** [Text responses with extracted page content and optional screenshots from remote browser sessions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TZAFON_API_KEY; task behavior is shaped by instruction, optional starting URL, and optional maximum step count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
