## Description: <br>
Browse, search, and analyze Chia NFTs, collections, profiles, marketplace events, and activity through the public MintGarden API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to look up Chia NFT collections, individual NFTs, profiles, sales activity, trending collections, and marketplace summaries in CLI or chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, lookups, and identifiers are sent to the MintGarden API. <br>
Mitigation: Avoid submitting sensitive identifiers or private research queries unless sharing them with MintGarden is acceptable. <br>
Risk: Trading-related command labels may imply broader coverage than the implementation actually returns. <br>
Mitigation: Treat prices, offers, history, trending, and activity output as informational and verify material trading decisions against authoritative marketplace data. <br>
Risk: Installation uses npm dependencies and can optionally link global CLI commands. <br>
Mitigation: Review npm dependencies before installation and skip global linking unless the mg or mintgarden commands are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Koba42Corp/mintgarden) <br>
- [MintGarden API documentation](https://api.mintgarden.io/docs) <br>
- [MintGarden](https://mintgarden.io) <br>
- [Chia Network](https://chia.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI and chat-friendly responses; marketplace data is retrieved from the MintGarden API and should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
