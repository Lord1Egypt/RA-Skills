## Description: <br>
Filter mbc-20 token minting spam from Moltbook feeds (96% spam removal rate). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymode](https://clawhub.ai/user/ymode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Moltbook feeds, measure mbc-20 spam prevalence, and return a filtered JSON feed for downstream tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Moltbook API key and uses it for authenticated feed requests. <br>
Mitigation: Install only if authenticated Moltbook feed access is intended, prefer a limited-scope or read-only key if available, and review the bundled JavaScript before use. <br>
Risk: Agents may invoke authenticated feed access automatically if the skill is installed for autonomous use. <br>
Mitigation: Run the tool manually or configure the agent environment to require approval for this skill when automatic authenticated access is not desired. <br>
Risk: Pattern-based filtering can miss changed spam formats or hide legitimate short posts that mention minting terms. <br>
Mitigation: Review filtered output for important workflows and update the filter patterns when Moltbook spam behavior changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ymode/moltbook-filter) <br>
- [Publisher profile](https://clawhub.ai/user/ymode) <br>
- [Moltbook API endpoint](https://www.moltbook.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the bundled JavaScript tool can emit JSON or console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ~/.config/moltbook/credentials.json and network access to moltbook.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
