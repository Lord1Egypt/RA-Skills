## Description: <br>
降价监控+自动下单。用户设置目标价和截止日期后，系统定时轮询飞猪价格，达标后通知或自动下单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaorabbits](https://clawhub.ai/user/zhaorabbits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to monitor Fliggy hotel, flight, and travel product prices against a target price and deadline, then receive price-drop alerts or optionally request booking when a price target is met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background monitoring with optional automatic booking could create financial commitments without enough visible safeguards. <br>
Mitigation: Keep auto_book disabled unless the runtime provides explicit maximum price, payment method, traveler detail, refundable-only, cancellation, and final confirmation controls before any booking is placed. <br>
Risk: Recurring checks may continue after the user no longer needs the tracked itinerary or product. <br>
Mitigation: Confirm the monitoring deadline and provide a clear way to cancel scheduled checks when the trip plan changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaorabbits/price-drop-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/zhaorabbits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON task configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule recurring background price checks and produce price alerts, expiry reminders, and booking guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
