## Description: <br>
LeadFlow builds targeted business lead lists from Google Maps and Yelp, enriches and verifies contact data, scores lead quality, and exports CRM-ready files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LKocaj](https://clawhub.ai/user/LKocaj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales teams, agencies, service businesses, freelancers, and consultants use LeadFlow to generate local business prospect lists, enrich them with contact data, prioritize them by quality score, and prepare exports for CRM or outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business and contact lead data may be sent to configured enrichment, verification, and webhook providers. <br>
Mitigation: Use only approved provider keys and webhook destinations, and confirm the audience and compliance basis before enrichment, verification, export, or webhook workflows. <br>
Risk: Lead data is saved locally and can be exported to spreadsheet or CRM import files. <br>
Mitigation: Protect the local database and export files, restrict access to generated lead lists, and remove stale exports when they are no longer needed. <br>
Risk: Large scraping, verification, export, or webhook batches can increase provider costs or send more records than intended. <br>
Mitigation: Start with small limits, use available filters and batch-size controls, monitor provider quotas, and avoid large sends until the target list has been reviewed. <br>


## Reference(s): <br>
- [LeadFlow on ClawHub](https://clawhub.ai/LKocaj/leadflow) <br>
- [LeadFlow npm package](https://www.npmjs.com/package/leadflow) <br>
- [OnCall Automation](https://oncallautomation.ai) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON command responses, local database records, exports, and webhook payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports can include CSV, XLSX, Instantly, HubSpot, Salesforce, Pipedrive, and Airtable formats; webhook delivery posts lead data as JSON batches.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
