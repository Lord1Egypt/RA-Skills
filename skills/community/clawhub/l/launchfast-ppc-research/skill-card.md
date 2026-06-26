## Description: <br>
Conducts Amazon PPC keyword research by analyzing up to 15 ASINs, segmenting keywords by tier and match type, and producing an Amazon Sponsored Products bulk upload TSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlockchainHB](https://clawhub.ai/user/BlockchainHB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amazon sellers, advertisers, and ecommerce operators use this skill to turn competitor or own-ASIN keyword research into tiered Sponsored Products campaign inputs and a bulk upload file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated bulk upload file can affect live Amazon advertising campaigns if uploaded without review. <br>
Mitigation: Review campaign name, daily budget, bids, ASINs, keyword tiers, and negatives before submitting the file in Seller Central. <br>
Risk: Rerunning the skill can overwrite a prior export if the same output filename is reused. <br>
Mitigation: Check the output filename in Downloads before rerunning or preserve the prior export under a distinct name. <br>
Risk: The workflow depends on LaunchFast keyword research being available. <br>
Mitigation: Confirm the LaunchFast keyword research tool is available before starting PPC research. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BlockchainHB/launchfast-ppc-research) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/BlockchainHB) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, file, configuration, guidance] <br>
**Output Format:** [Markdown summary plus tab-separated Amazon Sponsored Products bulk upload text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a dated launchfast-ppc-bulk text export in the user's Downloads folder after confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
