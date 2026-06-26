## Description: <br>
Query DNS servers to resolve domain names to IP addresses for network troubleshooting and DNS diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network operators, and support engineers use this skill for basic hostname-to-IP resolution during network troubleshooting and DNS diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact behavior supports only basic hostname-to-IP resolution, while the skill text describes broader DNS features such as MX, TXT, CNAME, reverse lookup, and custom DNS-server queries. <br>
Mitigation: Use it only for basic hostname-to-IP checks unless the implementation is expanded and tested for the documented DNS features. <br>
Risk: DNS lookups can disclose queried hostnames to the configured resolver. <br>
Mitigation: Avoid resolving sensitive internal hostnames unless DNS query disclosure is acceptable in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/nslookup-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text DNS lookup results with concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single hostname-to-IP lookup result from the bundled Python script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
