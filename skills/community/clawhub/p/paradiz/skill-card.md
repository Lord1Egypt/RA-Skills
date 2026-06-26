## Description: <br>
Paradiz helps agents answer VK guest inquiries by quoting stays from a price table, checking booking availability, and preparing concise booking responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keeper1978](https://clawhub.ai/user/keeper1978) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External hospitality operators and booking agents use this skill to respond to VK inquiries, calculate stay costs, manage holds, and prepare booking records for Paradiz guests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores guest personal data in booking, hold, lead, and comment records. <br>
Mitigation: Remove bundled customer data before release, collect only needed booking fields, and define retention, deletion, and consent rules for guest records. <br>
Risk: Telegram notifications can forward guest details outside the local booking workflow. <br>
Mitigation: Use dedicated Paradiz Telegram credentials, disable global Telegram fallback, and confirm that guests understand how their booking details are shared. <br>
Risk: Database maintenance and synchronization scripts can modify booking and pricing data. <br>
Mitigation: Run database scripts only through an explicit administrator workflow with backups and review of intended changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keeper1978/paradiz) <br>
- [Price table](artifact/references/prices.csv) <br>
- [Price table template](artifact/references/price_template.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Short VK-ready text, JSON command output, booking files, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local booking, hold, document, and SQLite records when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
