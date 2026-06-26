## Description: <br>
Fetch and save WeChat Official Account articles with full content and images, including automatic image download, JSON export, and full-page screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations users can use this skill to archive, back up, or analyze WeChat Official Account articles. It supports single-article and batch workflows that save article text, metadata, images, and screenshots for local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local archives of WeChat article text, images, and screenshots, which may include sensitive or copyrighted content. <br>
Mitigation: Use it only for content you are authorized to store, choose the output directory deliberately, and use --no-images or --no-screenshot when those files are not needed. <br>
Risk: The virtual environment helper includes a --script option that can run a user-selected local Python script. <br>
Mitigation: Use --script only when both the script path and virtual environment are fully trusted. <br>
Risk: Batch fetching can produce broad network activity and local storage growth. <br>
Mitigation: Start with a small test set, keep delays enabled for batch runs, and review the generated output before scaling up. <br>


## Reference(s): <br>
- [Playwright Python Documentation](https://playwright.dev/python/) <br>
- [WeChat Open Platform](https://open.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; runtime outputs include JSON files, downloaded images, and PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped local output directories; image download and screenshot capture can be disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
