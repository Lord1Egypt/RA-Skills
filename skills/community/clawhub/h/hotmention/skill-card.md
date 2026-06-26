## Description: <br>
Find people actively looking for products like yours on Reddit, X, LinkedIn, Quora, and Threads. Free mode uses web_search; paid mode uses the HotMention API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexandr-belogubov](https://clawhub.ai/user/alexandr-belogubov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, marketing, and growth teams use Hotmention to find and assess social posts that show buying intent for their product, then prepare concise reply drafts or follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and lead-finding queries may be sent to normal web search providers or to HotMention when paid mode is enabled. <br>
Mitigation: Use paid mode only with an intentional HOTMENTION_API_KEY configuration, and avoid submitting sensitive or confidential terms as monitoring keywords. <br>
Risk: Scheduled monitoring can continue sending queries after the initial setup if it is configured without clear operational controls. <br>
Mitigation: Set a clear monitoring schedule and keep an explicit way to pause or disable automated checks. <br>


## Reference(s): <br>
- [HotMention](https://hotmention.com) <br>
- [HotMention API documentation](https://hotmention.com/docs/api) <br>
- [ClawHub Hotmention listing](https://clawhub.ai/alexandr-belogubov/hotmention) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown-formatted lead summaries with intent scores, source links, reply guidance, and optional draft replies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use normal web search in free mode or the optional HotMention API when HOTMENTION_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
