## Description: <br>
Calculate, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use Hashcheck to calculate checksums, verify download hashes, compare local files, or hash short text strings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads user-selected files to calculate or compare hashes. <br>
Mitigation: Run it only on files the user is comfortable allowing the agent to read. <br>
Risk: The text-hashing command prints a short preview of the input text. <br>
Mitigation: Do not pass passwords, tokens, or other secrets to text hashing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON hash results with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b; verification and comparison failures are reported as mismatches.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
