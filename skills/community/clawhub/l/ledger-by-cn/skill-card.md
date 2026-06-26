## Description: <br>
A Chinese-language personal ledger and bookkeeping skill for managing multiple SQLite-backed ledgers, recording transactions, reviewing balances, producing summaries, and generating charts or Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victor233k](https://clawhub.ai/user/victor233k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to keep local personal financial records, add or batch-add transactions, inspect monthly summaries and balance trends, and prepare Markdown, chart, or CSV-style reporting outputs for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal financial records locally and its scanner verdict is suspicious because broad activation and unsafe path handling could expose or write finance data outside the intended scope. <br>
Mitigation: Install only when local storage of personal finance data is acceptable, use simple ledger names without slashes or path-like text, and review ledger and output paths before saving files. <br>
Risk: Chart output and any cloud or Feishu sharing workflow can disclose ledger details if the destination is wrong. <br>
Mitigation: Confirm chart paths and any cloud or Feishu upload destination explicitly before writing or sharing files. <br>
Risk: Broad activation around ledger, balance, charting, sync, or Feishu terms may invoke the skill outside a clear bookkeeping request. <br>
Mitigation: Prefer explicit bookkeeping prompts and review agent actions before execution, especially when a request mentions upload, sync, chart output, or ledger names. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/victor233k/ledger-by-cn) <br>
- [Publisher profile](https://clawhub.ai/user/victor233k) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Chinese prose with CLI commands, terminal tables, Markdown summaries, SQLite-backed local files, and chart image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores personal finance records locally under the user's OpenClaw skill data directory and may save charts to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
