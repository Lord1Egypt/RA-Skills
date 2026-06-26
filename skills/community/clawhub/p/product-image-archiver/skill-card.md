## Description: <br>
Archives original product images from a manually supplied product link into a structured folder with an Excel manifest for download, integrity, and risk-review fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowaa223](https://clawhub.ai/user/guowaa223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and developers use this skill to archive original images for a single manually identified product, preserve downloaded files, and produce a manifest for follow-up review. The generated risk and compliance fields should be treated as unverified prompts for human review, not as legal conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present infringement, license, CMA, and supplier-quality fields as if they were validated compliance evidence. <br>
Mitigation: Treat generated risk and compliance entries as unverified review prompts and require manual legal or business review before relying on them. <br>
Risk: Downloaded product images may come from untrusted or incorrect product links. <br>
Mitigation: Use trusted product URLs and manually inspect downloaded images before business publication or legal decisions. <br>
Risk: Runtime dependencies and network downloads affect production security posture. <br>
Mitigation: Pin and audit Python dependencies before production use, and run the skill in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guowaa223/product-image-archiver) <br>
- [Baidu AI Console](https://console.bce.baidu.com/ai/) <br>
- [1688](https://www.1688.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured archive folders, downloaded image files, an Excel manifest, and terminal progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires manual product ID and product URL input; Windows and python3 are declared in ClawHub metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
