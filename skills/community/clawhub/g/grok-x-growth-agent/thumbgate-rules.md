# ThumbGate Prevention Rules – X Growth Agent

1. **Rate Limit Guard** — Block the agent from executing the 'post_reply' tool if it has been used more than 2 times in the last 60 minutes.
2. **Spam Prevention** — Block replying to any X User ID that exists in the 'Recent Interactions' log within the past 48 hours.
3. **Sentiment Check** — Block replying to any post where the initial Grok sentiment analysis returns "negative", "tragic", "political", or "controversial".
4. **Relevance Threshold** — Block the 'post_reply' action if the contextual similarity score between the original post and the drafted reply is below 0.85.
5. **Link Throttle** — Block the inclusion of an affiliate link if the previous 3 tweets also contained links (enforce a 3:1 value-to-ask ratio).