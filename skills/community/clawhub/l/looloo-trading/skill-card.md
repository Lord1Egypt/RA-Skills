## Description: <br>
Use this skill when the user wants a LooLoo trade quote or a website confirmation link for a buy or sell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[looloolol](https://clawhub.ai/user/looloolol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request LooLoo buy or sell quotes and receive a confirmation URL for wallet-signature completion on the LooLoo website. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may act on an incorrect token address, trade side, amount, quote, or confirmation URL. <br>
Mitigation: Verify the token address, buy/sell side, amount, quote details, and legitimate LooLoo confirmation URL before signing in a wallet. <br>
Risk: A trade intent could be created before the user is ready to continue. <br>
Mitigation: Create a trade intent only after the user explicitly confirms they want to proceed. <br>


## Reference(s): <br>
- [LooLoo Trading on ClawHub](https://clawhub.ai/looloolol/looloo-trading) <br>
- [looloolol publisher profile](https://clawhub.ai/user/looloolol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown text with quote summary and confirmation URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before creating a trade intent; final wallet signature happens on the LooLoo website.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
