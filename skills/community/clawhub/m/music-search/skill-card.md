## Description:

Searches for music resources such as songs, albums, and lossless audio, returning public cloud-drive resource links from Quark, Baidu, Aliyun, and UC Netdisks.

This skill is for research and development only.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search public web results for music-resource links, filter by cloud-drive provider or audio format, and present structured results with titles, links, formats, extraction codes, and source pages. The artifact states it is for personal learning and research use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live third-party crawling and URL fetching can expose the runtime to untrusted pages or unsafe redirects.

Mitigation: Run the skill in an isolated environment, avoid internal or sensitive networks, and validate fetched URLs before use.

Risk: Unsafe @file argument expansion can read local files when untrusted arguments are passed.

Mitigation: Do not pass untrusted arguments to the skill; remove or restrict @file expansion before broader deployment.

Risk: Runtime Python dependency installation can introduce supply-chain or environment drift risk.

Mitigation: Pin and pre-review dependencies in a controlled virtual environment before installation.

Risk: Local caching may retain search terms or result links.

Mitigation: Avoid sensitive queries and clear the temporary cache according to local retention requirements.

## Reference(s):

- [ClawHub Music Search skill page](https://clawhub.ai/patches429/skills/music-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with agent-facing Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include cloud-drive links, audio format labels, extraction codes, source pages, and provider filters.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
