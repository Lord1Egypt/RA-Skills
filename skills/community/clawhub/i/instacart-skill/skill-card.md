## Description: <br>
Place grocery orders on Instacart via browser automation. Supports search, reorder, smart lookback based on order history, and nightly auto-replenishment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigdaddyluke](https://clawhub.ai/user/bigdaddyluke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal automation agents use this skill to manage Instacart shopping sessions, search for groceries, rebuild or replenish carts from order history, and prepare an order for explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls an authenticated Instacart browser session and can modify the user's shopping cart. <br>
Mitigation: Use it only with an account you intend the agent to operate, and review cart changes during the session. <br>
Risk: Automated verification-code retrieval can access mailbox-derived login codes when INSTACART_CODE_EMAIL is configured. <br>
Mitigation: Leave INSTACART_CODE_EMAIL unset if automated code retrieval is not desired; the skill will ask the user for the code instead. <br>
Risk: Cart contents, fees, tip, delivery address, or payment method could be wrong before checkout. <br>
Mitigation: Require explicit approval after reviewing the final cart, totals, address, and payment method before placing an order. <br>


## Reference(s): <br>
- [Instacart](https://www.instacart.com) <br>
- [ClawHub Skill Release](https://clawhub.ai/bigdaddyluke/instacart-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status updates with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cart summaries, product options, auto-replenishment summaries, and explicit checkout confirmation prompts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
