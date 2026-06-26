## Description: <br>
UK Parliament CLI searches bills, divisions, members, and written questions from official UK Parliament APIs, with stable JSON envelopes for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up UK Parliament bills, members, divisions or votes, and written questions through the parliament CLI. It is suited for workflows that need structured Parliament API results, including JSON envelopes for success and error cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a third-party global npm package. <br>
Mitigation: Verify the @shan8851/parliament-cli package and shan8851 publisher before installation, and run it in a controlled agent environment. <br>
Risk: The skill queries public Parliament APIs, so results can be ambiguous or change as public records update. <br>
Mitigation: Use JSON mode for automation, handle AMBIGUOUS_QUERY responses, and verify critical decisions against official Parliament sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shan8851/parliament-cli) <br>
- [Publisher profile](https://clawhub.ai/user/shan8851) <br>
- [Parliament CLI homepage](https://www.parliment-cli.xyz) <br>
- [npm package @shan8851/parliament-cli](https://www.npmjs.com/package/@shan8851/parliament-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the installed CLI returns text or JSON envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI defaults to text in a TTY, JSON when piped, and supports --json for forced structured output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
