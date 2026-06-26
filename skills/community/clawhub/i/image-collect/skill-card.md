## Description: <br>
This skill extracts knowledge from an image and saves it locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract OCR text, summaries, and keywords from image inputs and retain the image and extracted knowledge locally for later reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains image files and extracted OCR text locally, which can preserve sensitive document contents. <br>
Mitigation: Use it only with images whose local retention is intentional, and avoid secrets, IDs, medical documents, financial documents, and other private materials. <br>
Risk: The skill can fetch image URLs supplied to it, including URLs that may point to internal or private network resources. <br>
Mitigation: Use trusted image sources and avoid internal network URLs or private local paths unless that access is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bondli/image-collect) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Console text with a JSON knowledge record saved to a local JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves image assets locally and appends OCR text, summary, keywords, image path, and timestamp to a local JSON database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
