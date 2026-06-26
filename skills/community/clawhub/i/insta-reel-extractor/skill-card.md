## Description: <br>
Monitor Instagram DMs for reels, extract reel links from unread messages, and append the sender ID and reel link to instagram_reels.csv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thejas775](https://clawhub.ai/user/thejas775) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to inspect an already-open Instagram Direct Messages tab, find unread conversations containing reels, and collect sender IDs with reel links into a local CSV for follow-up tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects a logged-in Instagram Direct Messages tab, so private conversation data may be exposed to the agent while it searches for reel links. <br>
Mitigation: Run it only on conversations you are comfortable processing and keep the browser attached only for the intended session. <br>
Risk: Extracted sender IDs and reel links are written to instagram_reels.csv, creating a local record of message-derived data. <br>
Mitigation: Confirm the CSV location before use, restrict access to the file, and delete it when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thejas775/insta-reel-extractor) <br>
- [Instagram Direct Inbox](https://www.instagram.com/direct/inbox/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, files] <br>
**Output Format:** [Markdown guidance with JavaScript browser-evaluation snippets and CSV rows written as userid,reel_link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Instagram DM browser tab and writes findings to instagram_reels.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
