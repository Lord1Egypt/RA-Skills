## Description: <br>
Scrapes Goofish (xianyu) second-hand marketplace search result pages and returns structured item listings with optional sort, price range, publish-date, and pagination controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and marketplace analysts use this skill to collect structured Goofish search-result listings for price research, inventory analysis, or monitoring used-goods listings from pages available in their browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated scraping and stealth multi-session throughput can create platform-abuse or terms-compliance risk. <br>
Mitigation: Use only authorized, user-directed browser sessions; avoid stealth multi-session throughput unless explicitly permitted; keep collection rate-limited and compliant with Goofish rules. <br>
Risk: Dynamic page behavior, login state, CAPTCHA challenges, and site layout changes can make extracted marketplace results incomplete or unreliable. <br>
Mitigation: Confirm login and page state, test small batches before larger runs, respect CAPTCHA or rate-limit signals, and review extracted results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/goofish-search-list) <br>
- [Goofish search](https://www.goofish.com/search?q={keyword}) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON outputs from browser DOM extraction scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search keyword plus optional sort, publish-date, price range, and page-number controls; normal extraction returns up to 30 item records per page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
