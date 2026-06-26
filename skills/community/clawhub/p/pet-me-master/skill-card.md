## Description: <br>
Batch-pet Aavegotchis on Base via Bankr with cooldown checks, reminder automation, and natural-language routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aavegotchi users and agents use this skill to check petting cooldowns, discover owned or delegated gotchis, and submit batch Bankr transactions when gotchis are ready. It also supports reminders and optional fallback automation for recurring petting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit Bankr blockchain transactions automatically. <br>
Mitigation: Use dry-run and status commands before enabling live petting, and confirm the Bankr wallet and target gotchi IDs are correct. <br>
Risk: The skill can reuse broad local credentials for Bankr and Telegram. <br>
Mitigation: Prefer dedicated Bankr and Telegram credentials, keep them out of shared environments, and avoid shared Telegram chats for reminders. <br>
Risk: Reminder, cron, at, or background jobs can keep rescheduling the workflow. <br>
Mitigation: Confirm how to list and cancel scheduled jobs before enabling fallback or recurring automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/pet-me-master) <br>
- [Aavegotchi Contract Information](artifact/references/contract-info.md) <br>
- [Usage Guide](artifact/USAGE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit transaction status, cooldown timers, dry-run JSON, job identifiers, and Telegram notification text depending on the command.] <br>

## Skill Version(s): <br>
2.4.4 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
