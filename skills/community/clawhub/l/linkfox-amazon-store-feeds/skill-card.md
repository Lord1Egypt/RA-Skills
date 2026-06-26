## Description: <br>
Helps agents manage Amazon SP-API Feeds v2021-06-30 through LinkFox store-token and developer-proxy calls, including creating feed documents, uploading feed content, creating feeds, checking feed status, listing feeds, retrieving feed documents, and canceling feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to prepare, submit, monitor, and cancel Amazon seller feed workflows from an agent environment. It is intended for workflows that already have LinkFox API credentials, Amazon seller authorization, and the required Amazon Feeds roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and may process seller IDs, feed files, feed results, API keys, and access tokens. <br>
Mitigation: Install only when the publisher is trusted, keep LINKFOXAGENT_API_KEY and Amazon tokens protected, and treat feed input and output files as sensitive business data. <br>
Risk: The scripts make network calls to configured LinkFox gateway endpoints and to Amazon presigned upload URLs. <br>
Mitigation: Verify STORE_API_BASE_URL, SPAPI_BASE_URL, and uploadUrl values before execution, and confirm that the upload URL came from the expected createFeedDocument response. <br>
Risk: Creating or canceling feeds can affect Amazon seller listings, inventory, fulfillment, or other store operations. <br>
Mitigation: Review feedType, contentType, marketplaceIds, inputFeedDocumentId, and cancellation targets before running the scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-feeds) <br>
- [Local API reference](references/api.md) <br>
- [Amazon SP-API createFeedDocument](https://developer-docs.amazon.com/sp-api/reference/createfeeddocument) <br>
- [Amazon SP-API getFeedDocument](https://developer-docs.amazon.com/sp-api/reference/getfeeddocument) <br>
- [Amazon SP-API createFeed](https://developer-docs.amazon.com/sp-api/reference/createfeed) <br>
- [Amazon SP-API getFeed](https://developer-docs.amazon.com/sp-api/reference/getfeed) <br>
- [Amazon SP-API getFeeds](https://developer-docs.amazon.com/sp-api/reference/getfeeds) <br>
- [Amazon SP-API cancelFeed](https://developer-docs.amazon.com/sp-api/reference/cancelfeed) <br>
- [Amazon SP-API Feed Type Values](https://developer-docs.amazon.com/sp-api/docs/feed-type-values) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command inputs, and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts require LINKFOXAGENT_API_KEY and Amazon seller/feed identifiers; feed file contents and returned feed documents may contain sensitive business data.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
