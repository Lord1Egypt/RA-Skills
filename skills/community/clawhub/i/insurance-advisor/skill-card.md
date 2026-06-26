## Description: <br>
Insurance Advisor provides insurance recommendations, product comparisons, premium estimates, claim guidance, and term life or health insurance planning support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for general insurance education, CLI-assisted coverage planning, product-type comparison, premium estimation, and claim-process guidance. It should not be treated as licensed financial, insurance, legal, medical, or tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security assessment flags under-disclosed finance logging that can store and export sensitive entries in plaintext. <br>
Mitigation: Review the scripts before installing, avoid entering sensitive health, claim, policy, beneficiary, tax, or detailed financial information, and delete or protect local files under ~/.local/share/insurance-advisor when no longer needed. <br>
Risk: Insurance and finance guidance may be incomplete, jurisdiction-specific, or unsuitable for a user's personal circumstances. <br>
Mitigation: Use the output for general education only and confirm coverage decisions, claims steps, and tax implications with qualified professionals and official insurer materials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/insurance-advisor) <br>
- [Publisher Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Plain text CLI output with optional local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands write plaintext history, logs, and exports under ~/.local/share/insurance-advisor.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
