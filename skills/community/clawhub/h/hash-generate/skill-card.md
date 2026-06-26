## Description: <br>
Hash, HMAC, encode/decode, UUID generation, and hash identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to compute hashes and HMACs, encode or decode text, generate UUIDs, and identify likely hash algorithms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service receives the exact input submitted for hashing or encoding, which can expose secrets or private text. <br>
Mitigation: Do not submit passwords, API keys, private documents, or other sensitive material; use a local hash command for sensitive inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CutTheMustard/hash-generate) <br>
- [Hash service homepage](https://hash.agentutil.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text or JSON results from the hash service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hash value, algorithm, encoding, input length, request ID, and service URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
