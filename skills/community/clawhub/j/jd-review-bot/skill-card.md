## Description: <br>
Automates pending JD product reviews in a logged-in browser by filling review text, selecting five-star ratings, choosing positive service tags, submitting reviews, and checking completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzuim](https://clawhub.ai/user/fzuim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People managing a JD account use this skill to automate reviews for pending JD orders, including review text entry, five-star scoring, service-impression selection, submission, and final status checks. It is intended only for users who deliberately want an agent to operate their own logged-in JD account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in JD account and publish bulk five-star reviews publicly. <br>
Mitigation: Use it only when the account owner intentionally authorizes that behavior, review each review before submission, and confirm the activity complies with JD rules and the user's authenticity expectations. <br>
Risk: The skill may install or run browser automation tooling and Chromium/system dependencies. <br>
Mitigation: Provision and audit browser-use yourself where possible, run it in a controlled browser profile, and inspect commands before execution. <br>
Risk: Automated submissions may post inaccurate or difficult-to-reverse public content. <br>
Mitigation: Keep the browser headed and visible, require a pre-submit check, and only submit reviews whose text accurately reflects the user's real purchase experience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fzuim/jd-review-bot) <br>
- [JD review list](https://club.jd.com/myJdcomments/myJdcomment.action) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash, JavaScript, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser-use, a visible real browser session, and an already logged-in JD account; actions can submit public reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
