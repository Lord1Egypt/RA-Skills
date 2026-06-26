## Description: <br>
HiFleet provides agent guidance and scripts for querying vessel positions and related maritime data such as archives, voyages, PSC records, port information, traffic statistics, charter workflows, schedules, and pre-arrival vessels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charleiwang](https://clawhub.ai/user/charleiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External maritime users and developers use this skill to ask an agent for vessel position, voyage, archive, PSC, port, area traffic, charter, schedule, and pre-arrival information backed by HiFleet APIs and local chartering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials and HiFleet API keys may be exposed or over-permissioned if reused from normal accounts. <br>
Mitigation: Use a dedicated mailbox app password or limited credential, avoid sharing full secrets in chat, and review where config.json is stored before enabling the skill. <br>
Risk: Scheduled charter parsing can repeatedly fetch emails, parse them, store extracted data locally, and enrich records remotely. <br>
Mitigation: Enable scheduled parsing only after reviewing the mail parsing schedule, local database location, and enrichment behavior; disable it when continuous ingestion is not needed. <br>
Risk: Local charter data in charter_facts.sqlite3 may contain sensitive commercial email content. <br>
Mitigation: Keep the local database in a protected workspace, limit file access, and remove stored data when the charter workflow is no longer needed. <br>


## Reference(s): <br>
- [HiFleet homepage](https://www.hifleet.com) <br>
- [HiFleet API base](https://api.hifleet.com) <br>
- [MyTonnages homepage](https://mytonnages.hifleet.com) <br>
- [Skills index](references/skills_index.md) <br>
- [Position API reference](references/position_api.md) <br>
- [Voyage API reference](references/voyage_api.md) <br>
- [PSC API reference](references/psc_api.md) <br>
- [Port API reference](references/port_api.md) <br>
- [Charter module setup](hifleet-mytonnages/FIRST_SETUP.md) <br>
- [Security notes](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured vessel, port, PSC, schedule, charter, and traffic results; some workflows require API keys, mailbox credentials, or local storage.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
