## Description: <br>
Find, compare, and vet Groupon vouchers with fine-print checks, refund rules, and redemption planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to evaluate Groupon deals, shortlist vouchers, check merchant and fine-print risk, plan redemption, and prepare support or refund recovery steps before taking money-impacting action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deal-search context, location details, deal URLs, and optional support context may be sent to Groupon or a selected merchant during discovery, verification, booking, or support workflows. <br>
Mitigation: Keep stored notes minimal, share only the context needed for the task, and review any support or booking submission before approving it. <br>
Risk: Money-impacting actions such as buying, gifting, booking, marking redeemed, or submitting refund requests can affect the user's funds or voucher status. <br>
Mitigation: Require explicit user confirmation before any checkout, booking, redeemed-status change, or refund submission. <br>
Risk: Fine print, availability, merchant quality, and refund policies can change or be incomplete. <br>
Mitigation: Verify live deal terms, voucher status, merchant signals, and current Groupon policy before giving final purchase or recovery guidance. <br>
Risk: Local deal notes could expose sensitive voucher or account information if over-collected. <br>
Mitigation: Do not store payment details, login secrets, full voucher barcodes, or claim codes; store only reusable preferences, shortlist notes, and follow-up status. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/groupon) <br>
- [Groupon Skill Homepage](https://clawic.com/skills/groupon) <br>
- [Groupon](https://www.groupon.com/) <br>
- [Groupon Help](https://help.groupon.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown recommendations, scorecards, checklists, local memory templates, and support packet drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before checkout, booking, redemption, refund submission, or local memory writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
