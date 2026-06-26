## Description: <br>
Legal Docs Pro generates and reviews legal documents for freelancers, solopreneurs, and small businesses, with plain-English explanations and local profile-based document autofill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, solopreneurs, and small businesses use this skill to draft common legal documents, review contracts for risky clauses or missing protections, and explain legal language before deciding whether to seek attorney review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can be tricked into running local code or mishandling unusual filenames. <br>
Mitigation: Review or patch setup.sh and contract-scan.sh before running them, and avoid scanning files with unusual or untrusted filenames. <br>
Risk: Business identifiers, addresses, contact details, contracts, and generated documents may be stored in local plaintext files. <br>
Mitigation: Store only data you are comfortable keeping locally, restrict filesystem permissions, and avoid use on shared machines without additional controls. <br>
Risk: Legal templates and contract analysis may be incomplete or unsuitable for complex, high-value, or jurisdiction-specific matters. <br>
Mitigation: Use outputs as informational drafts and consult a licensed attorney before signing or relying on important legal documents. <br>


## Reference(s): <br>
- [Legal Docs Pro on ClawHub](https://clawhub.ai/nollio/normieclaw-legal-docs-pro) <br>
- [Nollio Publisher Profile](https://clawhub.ai/user/nollio) <br>
- [NormieClaw](https://normieclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated document text, review summaries, inline shell commands, and local configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local business profile settings and produce local document or review files when helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
