## Description: <br>
Find, subscribe to, track, and summarize podcast episodes using public RSS feeds and lightweight local tracking files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage podcast subscriptions, check for new or unheard episodes, track listening state, and produce concise episode summaries or action notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public podcast websites or RSS hosts and stores subscription and listening records locally. <br>
Mitigation: Use official feed URLs when available and delete files under memory/podcasts to clear retained podcast history. <br>
Risk: Malformed XML feeds, non-podcast URLs, or unexpected feed metadata may cause failed parsing or misleading episode details. <br>
Mitigation: Validate HTTP/HTTPS feed URLs, require XML/RSS/Atom-like responses, reject suspicious XML constructs, and report incomplete metadata instead of fabricating details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/podcast-manager) <br>
- [README](artifact/README.md) <br>
- [Security Review](artifact/SECURITY_REVIEW.md) <br>
- [Feed Probe Helper](artifact/scripts/feed_probe.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, shell commands, guidance] <br>
**Output Format:** [Markdown responses with local JSON tracking files and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps podcast state under memory/podcasts, limits routine episode listings to the newest 3-10 entries unless the user asks for more, and uses compact summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
