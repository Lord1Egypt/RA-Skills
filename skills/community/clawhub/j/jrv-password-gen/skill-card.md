## Description: <br>
Generate secure passwords, passphrases, and PINs with entropy analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to generate random passwords, passphrases, and PINs, or to estimate the entropy of an existing password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passphrase mode may make an outbound request and cache the downloaded word list in a shared temporary location. <br>
Mitigation: Review the network behavior before use in offline or restricted environments, and use only password or PIN generation when outbound access is not acceptable. <br>
Risk: Supplying real passwords through the documented --analyze argument can expose them through shell history or process listings. <br>
Mitigation: Avoid analyzing real passwords on shared systems, or use an input path that does not place secrets in command-line arguments. <br>


## Reference(s): <br>
- [EFF Large Wordlist](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate batches and includes entropy estimates with strength labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
