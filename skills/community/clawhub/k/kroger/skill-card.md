## Description:

Search Kroger products and add items to a Kroger cart via the Kroger API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongyanli-hash](https://clawhub.ai/user/tongyanli-hash)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Kroger grocery products, find nearby Kroger store locations, authenticate with Kroger, and add confirmed products to a Kroger cart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local code execution paths may be reachable through skill-provided shell and Python command construction.

Mitigation: Review the script before use, run it only in a trusted environment, and avoid passing untrusted search text or command arguments.

Risk: OAuth tokens are stored locally and may be exposed if the token file is readable by other users or processes.

Mitigation: Store the token file at a private path with restrictive permissions and avoid shared or untrusted hosts.

Risk: The skill can authenticate with Kroger and add items to a cart.

Mitigation: Require explicit user confirmation before starting authentication flows or performing any add-to-cart action.

## Reference(s):

- [Kroger Developer Portal](https://developer.kroger.com)
- [Kroger API Base URL](https://api.kroger.com/v1)
- [ClawHub skill page](https://clawhub.ai/tongyanli-hash/skills/kroger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Kroger API requests for product search, store lookup, OAuth token exchange, token refresh, and add-to-cart actions when invoked through the bundled shell script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
