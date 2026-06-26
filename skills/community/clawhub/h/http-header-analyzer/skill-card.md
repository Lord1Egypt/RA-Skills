## Description: <br>
Analyze HTTP security headers and TLS configuration. Find missing headers, weak ciphers, and misconfigurations in web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run a local header analysis script against one or more web targets, identify missing HTTP security headers, inspect exposed server metadata, and optionally report TLS details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TLS-related output may be unreliable because the analyzer disables certificate verification. <br>
Mitigation: Treat TLS findings as advisory and confirm certificate validity with a verifier that enforces certificate checks before making security decisions. <br>
Risk: The script makes network requests to URLs supplied by the user. <br>
Mitigation: Run it only against targets you are authorized to assess and review the requested URL list before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hostilespider/http-header-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/hostilespider) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON from a local Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports present and missing headers, severity-filtered findings, information disclosure headers, score, risk rating, and optional TLS details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
