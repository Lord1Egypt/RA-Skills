# Twitter/X Content Module Rules

## 1. Module Scope

Use this module for tweet detail, tweet thread, replies, retweets, content search, trends, inspiration posts, jobs search, and topic monitoring.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Tweet detail, thread, and reply context

- Documentation: `https://docs.keyapi.ai/en/twitter/tweet.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/tweet_thread.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/latest_replies.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/replies.md`
- Purpose: Inspect tweets, reconstruct thread context, and retrieve reply streams.

### Best Suited For

- tweet report
- conversation context
- reply behavior review
- post-level evidence

### Routing Rules

- Use tweet info for one tweet and tweet thread when surrounding thread context matters.
- Use latest replies for replies to a tweet or surface as documented.
- Use user replies when the requested surface is an account reply stream.
- Preserve tweet IDs for retweets, relationship checks, and follow-on enrichment.

## 3. Retweets and social proof

- Documentation: `https://docs.keyapi.ai/en/twitter/retweets.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/checkretweet.md`
- Purpose: Retrieve retweet evidence or check whether one account retweeted a tweet.

### Best Suited For

- amplification checks
- social proof review
- specific retweet verification

### Routing Rules

- Use retweets when the user wants retweeter lists or repost evidence.
- Use check retweet for a specific account/tweet relationship.
- Do not infer endorsement beyond the returned retweet relationship.

## 4. Search, trends, and content ideation

- Documentation: `https://docs.keyapi.ai/en/twitter/search.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/trends.md`
- Documentation: `https://docs.keyapi.ai/en/twitter/top_posts.md`
- Purpose: Search posts, inspect current trends, or retrieve inspiration posts.

### Best Suited For

- topic monitoring
- trend discovery
- content ideation
- candidate tweet collection

### Routing Rules

- Use search for explicit keyword/topic queries.
- Use trends when the user asks what is trending.
- Use inspiration posts only for ideation-style requests.
- Enrich selected tweets with tweet info/thread/replies only after shortlisting.

## 5. Jobs search

- Documentation: `https://docs.keyapi.ai/en/twitter/jobs.md`
- Purpose: Search Twitter/X job-related listings or job surface results.

### Best Suited For

- job lookup
- hiring topic search
- role discovery

### Routing Rules

- Use only for job-related requests.
- If account/company context is needed, combine with profile rules after selecting relevant results.

## 6. Common Workflows

- Tweet report: tweet info -> thread -> replies/retweets as requested.
- Topic monitor: search or trends -> selected tweet info/thread -> replies if needed.
- Content ideation: inspiration posts -> selected tweet/profile enrichment.
