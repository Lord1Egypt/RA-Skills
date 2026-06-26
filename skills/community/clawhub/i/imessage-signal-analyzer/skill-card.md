## Description: <br>
Analyze iMessage on macOS and Signal conversation history to reveal relationship dynamics, including message volume, initiation patterns, silence gaps, tone samples, and recent exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terellison](https://clawhub.ai/user/terellison) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to inspect local iMessage data or exported Signal conversations for relationship-pattern analysis. It helps summarize message counts, date ranges, yearly activity, conversation starts, long silences, recent messages, and conversational context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and summarize private chat history and contact data. <br>
Mitigation: Use a specific contact identifier, apply the message limit where practical, and review outputs before sharing or storing them. <br>
Risk: Broad Full Disk Access may expose more local data than the analysis needs. <br>
Mitigation: Grant Full Disk Access only when required for iMessage access, and revoke it after the analysis is complete. <br>
Risk: Signal export files contain sensitive conversation content. <br>
Mitigation: Protect exported JSON files, keep them in a controlled location, delete them when no longer needed, and unlink signal-cli when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terellison/imessage-signal-analyzer) <br>
- [signal-cli](https://github.com/AsamK/signal-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or conversational text with command examples and terminal analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include counts, date ranges, yearly volume bars, initiation estimates, notable silence gaps, message samples, and recent exchanges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
