## Description: <br>
Execute queries to Grok AI via Playwright browser automation without requiring an X API KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aquarius-wing](https://clawhub.ai/user/aquarius-wing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit prompts to Grok through an existing X Premium browser session and collect the response as local Markdown output. It is useful when a user wants Grok answers without configuring an X API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a persisted logged-in X/Grok browser session. <br>
Mitigation: Use it only on a trusted machine, avoid shared environments, and delete or protect the session directory when finished. <br>
Risk: Prompts, scraped responses, logs, debug files, and recordings may remain in local output directories. <br>
Mitigation: Avoid sensitive prompts and periodically review, protect, or delete generated output and debug artifacts. <br>
Risk: Scheduled runs can repeatedly automate an X Premium account and may create account or policy risk. <br>
Mitigation: Avoid cron or other unattended scheduling unless the user has reviewed the account and terms-of-use implications. <br>
Risk: The scraper can fail when X/Grok page structure or CSS selectors change. <br>
Mitigation: Use the included selector inspection and DOM fix guides before relying on failed or empty output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aquarius-wing/grok-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/aquarius-wing) <br>
- [Grok web interface](https://x.com/i/grok) <br>
- [DOM selector fix guide](dom-selector-fix.md) <br>
- [DOM selector fragility notes](learn/dom-selector-fragility.md) <br>
- [Record mode empty output notes](learn/record-mode-empty-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown files and agent-facing text with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the latest Grok response to output/latest.md and may retain logs, historical Markdown outputs, debug artifacts, and optional recordings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
