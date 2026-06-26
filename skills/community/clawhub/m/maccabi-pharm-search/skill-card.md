## Description: <br>
Search for medications and check real-time stock availability at Maccabi pharmacies in Israel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to search the Maccabi Pharm medication catalog, find Largo drug codes, and check city-level branch stock before visiting a pharmacy. It can also support user-requested recurring availability checks. <br>

### Deployment Geography for Use: <br>
Israel <br>

## Known Risks and Mitigations: <br>
Risk: Medication names, drug identifiers, and selected city codes may reveal sensitive health-related interests when sent to Maccabi's service API or shown in agent logs. <br>
Mitigation: Run searches only when the user has requested them, avoid shared logs or public notifications for sensitive medicines, and explain that these queries leave the local agent context. <br>
Risk: Stock information may be delayed or inaccurate. <br>
Mitigation: Treat results as planning guidance and confirm availability with the pharmacy before visiting. <br>
Risk: Recurring medication-stock checks can repeatedly process sensitive health-related queries. <br>
Mitigation: Create scheduled checks only after explicit user request and include a clear way for the user to stop them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexpolonsky/maccabi-pharm-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/alexpolonsky) <br>
- [Maccabi Pharm website](https://serguide.maccabi4u.co.il/heb/pharmacy/) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with CLI commands and stock-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Medication names, Largo codes, city codes, pharmacy names, addresses, phone numbers, distances, prescription flags, and stock status summaries may appear in outputs.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
