## Description: <br>
Automated weekly workflow that scrapes GOG store discounts, analyzes the full discounted-game dataset with Gemini, generates a markdown insights report, and syncs it to Feishu Drive. Use for recurring game-deal reporting and team distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to produce recurring GOG discount reports, identify high-value game deals, and distribute the generated markdown report through Feishu Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the default workflow publishes the current working directory to ClawHub after report generation. <br>
Mitigation: Review or remove the publish step before execution, and confirm that local secret files such as `.env` are excluded from publishing. <br>
Risk: The workflow uses Gemini, Feishu, and ClawHub credentials and uploads reports to a configured Feishu Drive folder. <br>
Mitigation: Use least-privilege credentials, keep secrets outside published artifacts, and verify the Feishu folder's intended visibility before running the upload. <br>


## Reference(s): <br>
- [GOG discounted games listing](https://www.gog.com/en/games?priceDiscounted=true) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu Drive upload_all API](https://open.feishu.cn/open-apis/drive/v1/files/upload_all) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/gog-sales-analytics) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, JSON data file, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports can be uploaded to a configured Feishu Drive folder.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
