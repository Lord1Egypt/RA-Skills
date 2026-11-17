## Description:

macOS Suite Readonly lets agents query unread Mail, Calendar events, Notes search results, and stock quotes on macOS and returns JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill on macOS to retrieve read-only personal productivity data from Mail, Calendar, and Notes, and to fetch stock quotes for user-requested symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Mail, Calendar, and Notes data can be exposed in agent-visible JSON output.

Mitigation: Use the skill only in workspaces and with agents authorized to access that local data, and treat returned JSON as private.

Risk: Stock quote commands send requested symbols to Tencent's quote service.

Mitigation: Avoid querying sensitive watchlists or proprietary symbol lists when external disclosure of requested symbols is a concern.

Risk: macOS automation or privacy permissions may be denied, producing failures or partial results.

Mitigation: Grant only the required macOS permissions and handle ok=false or warning responses as permission or availability signals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/macos-suite-readonly)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each command emits a single JSON object; list sizes are bounded by command limits.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
