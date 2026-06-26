## Description: <br>
Validate email addresses with syntax checks (RFC 5322), MX record verification, disposable/temporary email detection, and common typo suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to validate signup addresses, clean email lists, check deliverability signals, flag disposable addresses, and suggest corrections for common domain typos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live MX validation may reveal queried domains to configured DNS resolvers. <br>
Mitigation: Use the --no-dns flag when checking sensitive, private, or internal domains. <br>
Risk: Email validation results can be incomplete because syntax, MX, disposable-domain, and typo checks do not prove account ownership or guaranteed deliverability. <br>
Mitigation: Treat results as screening signals and use confirmation flows or other verification where account ownership or deliverability matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Terminal text output or machine-readable JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-address input, multi-address input, batch file input, optional JSON output, and flags to skip DNS or disposable-domain checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
