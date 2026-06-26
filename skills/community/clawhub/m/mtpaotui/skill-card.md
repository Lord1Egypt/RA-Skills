## Description: <br>
mtpaotui helps an agent prepare, preview, submit, and check Meituan errand orders for pickup and delivery, purchasing, queue-number pickup, moving, disposal, and other local assistance scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-tech](https://clawhub.ai/user/meituan-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to collect address and item details, retrieve Meituan address and POI data, preview delivery fees, submit confirmed errand orders, and check order status. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real Meituan errand orders that may create real spending or operational consequences. <br>
Mitigation: Use the documented preview step first, verify addresses, contacts, item details, fees, and timing, and submit only after explicit user confirmation; require extra confirmation for fees over 100 yuan. <br>
Risk: Using the skill requires trusting the publisher with a Meituan account, address book data, local token files, and order submission capability. <br>
Mitigation: Install and run it only when the publisher is trusted for those account and address-book permissions, and review local token handling before use. <br>
Risk: The release evidence reports under-disclosed obfuscated code that starts a local background updater. <br>
Mitigation: Request readable documentation for CliGuard's daemon, remote update endpoint, local files, and disable or audit controls before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-tech/mtpaotui) <br>
- [commands.md](references/commands.md) <br>
- [params.md](references/params.md) <br>
- [errors.md](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted user prompts, fee previews, order status messages, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to hide technical request details from end users while showing addresses, item summaries, fees, timing, confirmations, and order outcomes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
