## Description: <br>
Fetch public Maoyan Show data from show.maoyan.com, including event lists, event details, ticket prices, sessions, venues, city IDs, and crawler workflows, while avoiding login, order, payment, real-name verification, ticket verification, favorites, comments, and user account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onewilk](https://clawhub.ai/user/onewilk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query and document public Maoyan Show event, venue, city, session, and ticket-price data. It is intended for public display-data workflows, not private account, payment, order, identity, or ticket-verification actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be misapplied to private account, order, payment, real-name, ticket-verification, favorites, comment, or user-data workflows. <br>
Mitigation: Keep use limited to public show, city, venue, session, price, recommendation, search, and list endpoints, and decline private or transactional workflows. <br>
Risk: List and category filters may return unstable or mismatched results, especially across city contexts. <br>
Mitigation: Validate returned city, category, keyword, and date fields locally before presenting results or making follow-up detail calls. <br>
Risk: Automated public API querying can create avoidable load or trigger service-side defenses. <br>
Mitigation: Keep request volume reasonable, reuse task-scoped values where appropriate, and avoid unnecessary repeated calls. <br>


## Reference(s): <br>
- [Maoyan Show H5 API Usage Guide](references/api.md) <br>
- [Maoyan Show public entry](https://show.maoyan.com/qqw#/) <br>
- [ClawHub release page](https://clawhub.ai/onewilk/maoyan-show) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with normalized result fields and optional HTTP or curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public Maoyan Show results should include relevant event, price, venue, city, and API caveat fields when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
