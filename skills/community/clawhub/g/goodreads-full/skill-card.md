## Description: <br>
Full Goodreads integration for reading shelves, searching books, retrieving details and reviews, and making write actions such as ratings, shelves, reviews, reading dates, and progress through browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phuc-nt](https://clawhub.ai/user/phuc-nt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect Goodreads shelves, activity, book metadata, and reviews, then optionally update a logged-in Goodreads account. It is intended for user-directed reading-list and review-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make durable changes to a logged-in Goodreads account, including ratings, shelves, reviews, reading dates, and progress. <br>
Mitigation: Confirm each requested write action and its target book before running the write command. <br>
Risk: The write workflow stores a persistent browser session for Goodreads access. <br>
Mitigation: Use a private machine and isolated virtual environment, and delete scripts/.browser-data or log out when retained access is no longer wanted. <br>
Risk: The browser automation uses stealth behavior and may be blocked or may stop working if Goodreads changes its UI. <br>
Mitigation: Treat failed or unverified actions as requiring manual review in Goodreads before relying on the result. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/phuc-nt/goodreads-full) <br>
- [Goodreads](https://www.goodreads.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; invoked scripts return JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands use Goodreads RSS and HTML scraping; write commands require a logged-in browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
