## Description: <br>
Provides authenticated access to Moegirlpedia's MediaWiki API for page search, wikitext parsing, page content, categories, category members, page summaries, user permissions, watchlist briefs, and recent changes briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[annangela](https://clawhub.ai/user/annangela) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve authenticated Moegirlpedia data through documented command-line operations. It supports read-oriented wiki research workflows that need search results, page content, parsed wikitext, category data, user permission data, watchlist summaries, or recent changes summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moegirlpedia credentials could expose account access if the bot password is overprivileged or reused. <br>
Mitigation: Use a dedicated Moegirlpedia bot password instead of the main password, grant only the documented read and watchlist-view permissions, and restrict IP ranges and editable pages where possible. <br>
Risk: The bundled client contains unused write-capable helpers even though this release is disclosed as an authenticated reader. <br>
Mitigation: Avoid granting edit, rollback, options, watchlist-modification, or other write-oriented rights unless a future version explicitly documents and gates those actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/annangela/moegirlpedia-mediawiki-api) <br>
- [Moegirlpedia Bot Passwords](https://mzh.moegirl.org.cn/Special:BotPasswords) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON printed to stdout; brief-style commands include concise summary arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports pagination through continueToken values; requires bash, Node.js, internet access, MOEGIRLPEDIA_USERNAME, and MOEGIRLPEDIA_BOT_PASSWORD.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
