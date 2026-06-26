## Description: <br>
Pans Lead Miner searches public lead sources through SearXNG to identify and rank companies with likely AI compute demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, business development, and go-to-market users use this skill to find companies that may need AI compute capacity and rank them by funding and compute-demand signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthetic demo leads may be mistaken for verified prospects when SearXNG is unavailable or demo mode is used. <br>
Mitigation: Treat records with source=demo as sample data and independently verify companies before outreach or CRM import. <br>
Risk: Search terms and exported lead files may expose prospecting strategy or unverified lead data. <br>
Mitigation: Use a trusted local SearXNG instance, choose export paths deliberately, and review exported data before sharing or importing it into other systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-lead-miner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Files] <br>
**Output Format:** [Markdown table by default, with optional JSON, CSV, or exported file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lead rows include company, stage, amount, region, signal score, source, URL, and snippet when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
