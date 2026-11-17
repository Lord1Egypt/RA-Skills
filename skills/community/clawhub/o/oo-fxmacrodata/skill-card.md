## Description:

FXMacroData (fxmacrodata.com). Use this skill for ANY FXMacroData request — searching and reading data. Whenever a task involves FXMacroData, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve FXMacroData macroeconomic releases, CFTC positioning data, foreign-exchange rates, indicator catalogues, and release calendars through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may run a remote CLI installer whose contents were not verified, without a clear approval step.

Mitigation: Review and explicitly authorize CLI installation separately; prefer a fixed, independently verified release and control automatic skill synchronization.

Risk: OOMOL receives connector requests and manages the connected service credentials.

Mitigation: Use an account and service connection appropriate for the requested data, and do not include raw credentials in command payloads.

## Reference(s):

- [FXMacroData documentation](https://fxmacrodata.com/docs)
- [FXMacroData homepage](https://fxmacrodata.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Text, Guidance]

**Output Format:** [Structured JSON data with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results and history depend on the selected action, currency, and API-key access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
