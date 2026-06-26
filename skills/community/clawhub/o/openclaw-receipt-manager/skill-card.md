## Description: <br>
Manage personal receipts by extracting data from images, storing records, and providing expense searches and monthly financial summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clinchcc](https://clawhub.ai/user/clinchcc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to save receipt images and extracted purchase details in a local SQLite database, then list, search, update, delete, and summarize expenses by month, vendor, category, or item. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipts can contain personal and financial information stored on the user's device. <br>
Mitigation: Install only when local receipt storage is intended, review data/receipts/ periodically, and avoid use on shared or automatically backed-up devices unless that storage is acceptable. <br>
Risk: Broad receipt and expense triggers may save recognized receipt data automatically. <br>
Mitigation: Use explicit requests when saving receipts and review newly saved records for accuracy and sensitivity. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/clinchcc/openclaw-receipt-manager) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local receipt records, copied receipt images, and SQLite database files under data/receipts/.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
