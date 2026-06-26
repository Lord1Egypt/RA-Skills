## Description: <br>
Google Play Developer API (Android Publisher) integration with managed OAuth for managing apps, subscriptions, in-app purchases, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and app operators use this skill to interact with Google Play Console programmatically through Maton-managed OAuth, including listing and updating in-app products, subscriptions, purchases, reviews, and app edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and access to a connected Google Play account. <br>
Mitigation: Keep MATON_API_KEY private, scope the connected account to the minimum permissions needed, and install only when Google Play access through Maton is intended. <br>
Risk: Create, update, delete, refund, cancel, reply, and commit operations can change Google Play resources or account state. <br>
Mitigation: Confirm the target resource, selected Maton connection, request body, and intended effect before running any write operation. <br>
Risk: Multiple Google Play connections can route requests to the wrong account. <br>
Mitigation: Use the Maton-Connection header whenever more than one connection exists and verify the connected Google Play account before acting. <br>


## Reference(s): <br>
- [Google Play skill on ClawHub](https://clawhub.ai/byungkyu/google-play) <br>
- [Android Publisher API Overview](https://developers.google.com/android-publisher) <br>
- [In-App Products API](https://developers.google.com/android-publisher/api-ref/rest/v3/inappproducts) <br>
- [Subscriptions API](https://developers.google.com/android-publisher/api-ref/rest/v3/monetization.subscriptions) <br>
- [Purchases API](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products) <br>
- [Reviews API](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews) <br>
- [Edits API](https://developers.google.com/android-publisher/api-ref/rest/v3/edits) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a connected Google Play account through Maton.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
