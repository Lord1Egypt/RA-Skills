## Description: <br>
Provides patterns for detecting sensitive data like API keys, credit cards, emails, SSNs, phone numbers, and IPs for authorized security testing and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PandaAI-1337](https://clawhub.ai/user/PandaAI-1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security testers, developers, and engineers use this skill to find sensitive-data and security-relevant strings in code, logs, packet captures, and filesystem content during authorized testing or validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern matching can expose sensitive data during authorized scans. <br>
Mitigation: Keep searches scoped to systems and folders the user is allowed to assess, and review sensitive matches before sharing them. <br>
Risk: Static pattern lists may produce false positives or miss data types outside the included references. <br>
Mitigation: Verify the included pattern files and validate matches against the target data type before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PandaAI-1337/pattern-matching) <br>
- [Pattern-Matching README](references/Pattern-Matching/README.md) <br>
- [PHP auditing grep strings](references/Pattern-Matching/grepstrings-auditing-php.md) <br>
- [Basic grep strings](references/Pattern-Matching/grepstrings-basic.txt) <br>
- [Repository scan patterns](references/Pattern-Matching/repo-scan.txt) <br>
- [Malicious string patterns](references/Pattern-Matching/malicious.txt) <br>
- [Error message patterns](references/Pattern-Matching/errors.txt) <br>
- [PCAP strings](references/Pattern-Matching/pcap-strings.txt) <br>
- [PHP magic hashes](references/Pattern-Matching/php-magic-hashes.txt) <br>
- [Angular dangerous function patterns](references/Pattern-Matching/dangerous-functions-angular.txt) <br>
- [Thick-client basic strings](references/Pattern-Matching/thickclient-basic.txt) <br>
- [PHP dangerous functions](references/Pattern-Matching/Source-Code-(PHP)/php-auditing.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or text with optional grep-style shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses static pattern lists; users should verify matches before sharing or acting on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
