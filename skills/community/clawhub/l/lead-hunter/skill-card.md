## Description: <br>
Automated lead generation and enrichment for AI agents that helps find prospects, enrich them with contact and company data, and score them for prioritization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galacticpuffin](https://clawhub.ai/user/galacticpuffin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure lead discovery, enrichment, scoring, export, CRM, and webhook workflows for B2B prospecting. It is intended for lawful, approved data sources and should be reviewed before any automated outreach or CRM write actions are enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides broad personal-data collection, enrichment, external exports, and automated outreach without enough built-in scoping or compliance controls. <br>
Mitigation: Use only lawful, approved data sources; define opt-out, retention, deletion, and compliance rules for generated lead lists; and manually review workflows before operational use. <br>
Risk: LinkedIn proxy scraping and other scraping-oriented discovery paths can create legal, platform-policy, and operational risk. <br>
Mitigation: Avoid the LinkedIn proxy-scraping path and prefer approved APIs, public sources, or sources where the user has explicit authorization. <br>
Risk: External enrichment vendors, webhooks, and CRM integrations can expose unnecessary lead data or write unreviewed records. <br>
Mitigation: Use least-privileged test credentials, minimize fields sent to enrichment vendors and webhooks, and disable auto-outreach and CRM writes until manually reviewed. <br>


## Reference(s): <br>
- [Lead Hunter release page](https://clawhub.ai/galacticpuffin/lead-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes templates for ICP definitions, discovery sources, enrichment providers, scoring rules, exports, CRM integrations, and webhooks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
