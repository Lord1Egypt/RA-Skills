## Description: <br>
Queries poe.ninja for Path of Exile currency, item, and price trend data across leagues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qpooqp777](https://clawhub.ai/user/qpooqp777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Path of Exile market prices, compare leagues, and retrieve currency, item, map, gem, and trend data from poe.ninja. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: League names and item search terms are sent to poe.ninja. <br>
Mitigation: Use public game-market queries only and avoid entering private information as search text. <br>
Risk: Cross-type search can issue multiple poe.ninja requests in a short period. <br>
Mitigation: Use focused item types when possible, limit repeated searches, and respect API rate limits. <br>
Risk: Market prices can be stale, low confidence, or affected by low trading volume. <br>
Mitigation: Check league selection, listing counts, trend fields, and low-confidence indicators before relying on results. <br>


## Reference(s): <br>
- [Poe.ninja API Reference](artifact/references/api_reference.md) <br>
- [poe.ninja API](https://poe.ninja/api/data) <br>
- [poe.ninja](https://poe.ninja) <br>
- [poe.ninja API Documentation](https://github.com/ayberkgezer/poe.ninja-API-Document) <br>
- [ClawHub Skill Page](https://clawhub.ai/qpooqp777/poe1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional raw JSON from bundled Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs price tables, filtered search results, trend percentages, listing counts, and optional raw API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
