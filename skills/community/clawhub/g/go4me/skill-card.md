## Description: <br>
Send XCH to Twitter users via Go4Me address lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to resolve Go4Me profiles from Twitter-style handles, view the associated XCH address, and prepare or submit Chia payments through sage-wallet after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real XCH wallet transfers. <br>
Mitigation: Verify the full resolved XCH address and payment amount before confirming any send or tip action. <br>
Risk: Recipient lookup is not tightly scoped enough for the level of transfer risk. <br>
Mitigation: Use only normal Twitter-style handles and reject unexpected handle formats before lookup. <br>
Risk: Wallet certificate and key paths are sensitive secrets. <br>
Mitigation: Keep wallet certificate and key paths private and avoid exposing them in prompts, logs, or shared transcripts. <br>
Risk: The transfer workflow depends on sage-wallet. <br>
Mitigation: Install sage-wallet only from a trusted source before using this skill for wallet operations. <br>


## Reference(s): <br>
- [Go4Me Skill Page](https://clawhub.ai/Koba42Corp/go4me) <br>
- [Go4Me](https://go4.me/) <br>
- [Sage Wallet](https://github.com/xch-dev/sage) <br>
- [Chia Network](https://www.chia.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display resolved Go4Me profile fields, XCH addresses, wallet confirmation prompts, and transaction status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
