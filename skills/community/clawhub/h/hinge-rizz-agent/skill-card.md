## Description: <br>
Operates an already-open Hinge session to review profiles, triage queues, analyze matches, draft respectful openers or replies, and perform explicit like, reply, or rose actions only when the user has enabled that workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jdave211](https://clawhub.ai/user/Jdave211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using Hinge can use this skill for live profile review, inbox triage, shortlist management, message drafting, and consent-gated account actions. Developers and operators can also use its bundled scripts for Appium-based iOS automation, queue state, and profile or thread analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously act on a dating account through likes, roses, and replies. <br>
Mitigation: Start in review or queue behavior and keep autonomous sending disabled unless the user explicitly enables that mode for the session. <br>
Risk: The skill can control an iPhone session broadly through Appium. <br>
Mitigation: Run it only against an intended, already-authenticated Hinge session and require visible confirmation before claiming or relying on account-changing actions. <br>
Risk: Sensitive profile, message, screenshot, and preference data may be sent to outside services or retained locally. <br>
Mitigation: Install only if that data exposure is acceptable, avoid broad credential fallbacks, and delete hinge-data regularly when retained dating logs or examples are not needed. <br>


## Reference(s): <br>
- [iOS Access](artifact/references/ios-access.md) <br>
- [Rizz Style Notes](artifact/references/rizz-style-notes.md) <br>
- [Lovepanky flirty text examples](https://www.lovepanky.com/flirting-flings/naughty-affairs/flirty-text-examples) <br>
- [The Cut texting and flirting advice](https://www.thecut.com/article/how-to-text-flirt-examples-advice.html) <br>
- [wikiHow examples of rizz lines](https://www.wikihow.com/Examples-of-Rizz-Lines) <br>
- [wikiHow how to rizz over text](https://www.wikihow.com/How-to-Rizz-a-Girl-over-Text) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries and message drafts, JSON analysis files, and shell commands for bundled automation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local hinge-data runtime state such as queues, observations, screenshots, taste models, and latest analysis files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
