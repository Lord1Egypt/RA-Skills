## Description: <br>
Book restaurant tables on OpenTable via the browser tool, including hidden time slots and terms checkboxes, when the user is already logged in and has a saved card on file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eeshita-Pande](https://clawhub.ai/user/Eeshita-Pande) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to reserve restaurant tables on OpenTable through a browser session. It guides the agent through search, slot selection, terms review, reservation confirmation, and confirmation reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can act through a logged-in OpenTable profile with a saved card and may accept terms or complete a real reservation. <br>
Mitigation: Require the agent to stop before accepting terms or clicking the final reservation button until the user reviews the restaurant, date, time, party size, cancellation or no-show terms, and any card or fee implications. <br>


## Reference(s): <br>
- [Browser Booking JS Snippet Reference](artifact/browser-snippets.md) <br>
- [ClawHub skill page](https://clawhub.ai/Eeshita-Pande/opentable-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with browser workflow steps and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser.enabled, an authenticated OpenTable browser session, and a saved card in the user's OpenTable account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
