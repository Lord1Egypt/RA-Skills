## Description:

Provides patterns for detecting sensitive data like API keys, credit cards, emails, SSNs, phone numbers, and IPs for authorized security testing and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaai-1337](https://clawhub.ai/user/pandaai-1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security testers, developers, and engineers use this skill to find sensitive-data indicators and security-auditing strings in code, logs, packet captures, thick-client artifacts, and filesystems during authorized assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pattern lists can be used outside an authorized assessment scope.

Mitigation: Use the skill only for systems, code, logs, packet captures, and data that you are authorized to test.

Risk: Searches may surface sensitive-looking strings or regulated identifiers.

Mitigation: Handle matches as potentially sensitive data and follow the applicable data-handling and reporting process.

Risk: Pattern matches may be false positives because the files contain indicators rather than validation logic.

Mitigation: Review each match in context before treating it as a confirmed secret, vulnerability, or data exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pandaai-1337/skills/pattern-matching)
- [Pattern Matching README](references/Pattern-Matching/README.md)
- [Basic grep strings](references/Pattern-Matching/grepstrings-basic.txt)
- [PHP auditing grep strings](references/Pattern-Matching/grepstrings-auditing-php.md)
- [PHP source auditing functions](references/Pattern-Matching/Source-Code-(PHP)/php-auditing.txt)
- [Repository scan strings](references/Pattern-Matching/repo-scan.txt)
- [Packet capture strings](references/Pattern-Matching/pcap-strings.txt)
- [PHP magic hashes](references/Pattern-Matching/php-magic-hashes.txt)
- [Dangerous Angular functions](references/Pattern-Matching/dangerous-functions-angular.txt)
- [Malicious string indicators](references/Pattern-Matching/malicious.txt)
- [Error message strings](references/Pattern-Matching/errors.txt)
- [Thick-client basic strings](references/Pattern-Matching/thickclient-basic.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with reference text lists and inline shell/Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static pattern files; no network calls or code execution are required by the package itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
