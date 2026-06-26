## Description: <br>
Uses a local Python wrapper to call official iFinD QuantAPI HTTP endpoints for market, macro, fund, code-conversion, calendar, report, and portfolio data while checking refresh_token setup and local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YannLong](https://clawhub.ai/user/YannLong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query iFinD QuantAPI data through local Python scripts, presets, and direct endpoint calls. It supports dependency checks, refresh_token setup, secure local token storage, and response reporting for credential-backed API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses broad credential-backed iFinD API access and stores a long-lived refresh_token locally. <br>
Mitigation: Use the token store helper, keep file permissions owner-only, prefer scoped preset commands, and remove or rotate the token when it is no longer needed. <br>
Risk: Agent-assisted token acquisition may expose the user's iFinD account page or refresh_token. <br>
Mitigation: Use only the official iFinD QuantAPI site or documented client flow, stop after storing the token, and avoid printing or pasting the token into chat or shell history. <br>
Risk: Direct endpoint calls can send arbitrary endpoint names and JSON payloads using the configured account. <br>
Mitigation: Review endpoint names, payloads, symbol lists, and date ranges before execution; prefer documented presets for common market-data queries. <br>


## Reference(s): <br>
- [iFind API Reference](references/iFind_API_Reference.md) <br>
- [refresh_token acquisition and storage](references/token-and-storage.md) <br>
- [iFinD QuantAPI](https://quantapi.51ifind.com) <br>
- [ClawHub release page](https://clawhub.ai/YannLong/ifind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API output depends on the selected iFinD endpoint, account permissions, token validity, requested symbols, and date range.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
