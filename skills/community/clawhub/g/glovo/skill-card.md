## Description: <br>
Navigate Glovo in a live browser session to compare stores, manage carts, and reach checkout safely before ordering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse Glovo with their own signed-in session, compare live store options, prepare draft carts, verify checkout details, and recover from order issues. The skill is intended for workflows where Glovo-specific state such as address, cart, availability, fees, promotions, and support status matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate in a real signed-in Glovo session with live addresses, carts, payment methods, and purchase consequences. <br>
Mitigation: Keep browser-control permission explicit, summarize checkout details, and require current-thread approval before changing sensitive state or placing an order. <br>
Risk: Optional local memory in ~/glovo/ could capture sensitive ordering context if used carelessly. <br>
Mitigation: Store only non-sensitive preferences and durable operating notes; do not store passwords, payment card data, verification codes, full receipts, or raw support transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/glovo) <br>
- [Glovo website](https://glovoapp.com) <br>
- [Skill homepage](https://clawic.com/skills/glovo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checkout summaries, browser-control instructions, and optional local memory setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft cart summaries, store comparisons, issue-recovery steps, and local notes for ~/glovo/ when the user permits persistent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
