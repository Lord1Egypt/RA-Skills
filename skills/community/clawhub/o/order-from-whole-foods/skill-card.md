## Description: <br>
Order groceries from Whole Foods using browser automation and a saved purchase policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chadnewbry](https://clawhub.ai/user/chadnewbry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn a grocery list into a Whole Foods cart or order through OpenClaw browser automation while enforcing saved spending, confirmation, delivery-window, and calendar preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Amazon/Whole Foods browser session and may place an order when saved policy allows. <br>
Mitigation: For first use, set purchase_mode to add_to_cart_only or confirm_before_buy to true, choose a low max_auto_spend, and require manual login in the browser session. <br>
Risk: Incorrect item matches, substitutions, totals, or delivery slots could materially change the order. <br>
Mitigation: Stop for unresolved ambiguity, unknown totals, out-of-window delivery slots, account or payment uncertainty, or policy conflicts, and report only observed cart and checkout state. <br>
Risk: Calendar blocking can add delivery or pickup events automatically when enabled. <br>
Mitigation: Leave calendar_blocking_enabled false unless automatic calendar events are desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chadnewbry/order-from-whole-foods) <br>
- [Whole Foods Amazon Storefront](https://www.amazon.com/alm/storefront?almBrandId=VUZHIFdob2xlIEZvb2Rz&ref=nav_cs_dsk_grfl_stfr_wf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Concise Markdown status updates with observed cart, total, delivery-window, and blocker details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order state labels such as order placed, cart ready for review, or blocked; it should not invent prices, delivery windows, or cart state.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
