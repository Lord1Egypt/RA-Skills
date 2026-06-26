## Description: <br>
Runs a local Python script that queries Hanime1 search results for miuuuuu and prints matching video titles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chgy123](https://clawhub.ai/user/chgy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users can ask an agent to check whether the configured Hanime1 search page appears to have matching updates and receive the script's printed title list. The skill is a local helper for user-initiated checks, and users should confirm that contacting the target site is appropriate from their network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts hanime1.me from the user's local network. <br>
Mitigation: Install and run it only where contacting that site is acceptable, and review local network and content policies before execution. <br>
Risk: The artifact documentation mentions JSON output, wait-time, and custom selector options that the current script does not implement. <br>
Mitigation: Treat the current release as plain console output from the hard-coded search URL unless the skill is updated. <br>
Risk: The script depends on locally installed requests and beautifulsoup4 packages. <br>
Mitigation: Install dependencies only from trusted package sources and review them according to your normal dependency policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chgy123/hanime1-search) <br>
- [Hanime1 search URL used by the script](https://hanime1.me/search?query=miuuuuu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text console output with status lines and a numbered list of titles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The current script uses a hard-coded search URL and prints up to 10 matching titles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
