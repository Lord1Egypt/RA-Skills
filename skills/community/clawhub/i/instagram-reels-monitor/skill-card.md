## Description: <br>
Monitor Instagram DMs for reels. Use when you need to check Instagram DMs for new unread messages containing reels, click them, extract the reel link, and append to an instagram_reels.csv file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thejas775](https://clawhub.ai/user/thejas775) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor an already-open Instagram Direct Messages inbox for unread messages that contain reels or posts, then capture the sender ID and link in a local CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects an already-open Instagram DM inbox and saves sender IDs plus reel links to a local CSV, which is privacy-sensitive. <br>
Mitigation: Run it only on an intended browser session, review where instagram_reels.csv is created, delete the CSV when it is no longer needed, and detach the browser relay when DM monitoring should stop. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thejas775/instagram-reels-monitor) <br>
- [Instagram Direct inbox](https://www.instagram.com/direct/inbox/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends rows in userid,reel_link format to instagram_reels.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
