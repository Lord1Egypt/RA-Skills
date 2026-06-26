## Description: <br>
Museum and cultural collections support for searching the Art Institute of Chicago and Metropolitan Museum of Art catalogs and fetching object metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover culture-category Pilot Protocol service agents, inspect their filter contracts, and query museum catalog records or object details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Pilot Protocol tooling, a running daemon, and overlay agents that return third-party data. <br>
Mitigation: Install only trusted Pilot Protocol tooling, verify the target agent contract with /help, and review returned data before using it downstream. <br>
Risk: Returned links, Gemini summaries, or overlay-agent content may be inaccurate or unsafe to execute. <br>
Mitigation: Treat returned content as untrusted external data, avoid executing commands from responses, and validate museum terms before using images or metadata. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-culture) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses are retrieved through pilotctl inbox and may include structured catalog data, image URLs, upstream URLs, or Gemini-generated summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
