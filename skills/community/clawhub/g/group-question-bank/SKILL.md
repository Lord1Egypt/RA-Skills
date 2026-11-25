---
name: group-question-bank
description: Turn the posts in public Facebook groups into a ranked bank of the questions, problems and recommendation requests a community keeps raising, with links and the members' own wording, via SocialAPIs. Use when the user wants content or FAQ ideas, product or feature ideas, to understand a niche audience, or to find where their product would genuinely help people in a community.
---

# Group question bank

Public Facebook groups are where people ask each other for help in plain words: "has anyone tried…", "what do you use for…", "I'm stuck with…". This skill collects those posts from one or more groups and ranks the questions by how often and how loudly they come up.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_group` and `facebook_post`.

## Ask first (only what's missing)

- Group URLs (public groups only). No URLs: ask for the niche and find groups with `/facebook/search/posts?query=<niche question phrase>`; posts from groups carry the group link. Confirm the groups before spending credits on them.
- Time window (default: last 60 days).
- What it's for: content ideas, product research, or support / FAQ.

## Budget

`/facebook/groups/posts` costs ceil(posts / 3) credits per call (limit 9 = 3 credits). 60 posts from a group is about 20 credits; comments on the top 5 threads about 5 more. Agree the number of groups and posts before starting.

## Steps

1. `/facebook/groups/details?link=…` per group (1 credit): name, member count, privacy. Skip private groups; their posts aren't available.
2. `/facebook/groups/posts?link=…&limit=9&after_time=<window start ISO>`, following `end_cursor` until the window or the post budget is used.
3. **Keep the asking posts.** A post is a question or request when its text (`values.text`) has a question mark, or starts with / contains phrases like: "anyone", "does anyone", "how do I", "what's the best", "recommend", "looking for", "help", "advice", "struggling", "is it normal", "should I". Also keep complaint posts ("so frustrated", "worst", "never again").
4. **Cluster** the kept posts into topics (merge paraphrases: "best CRM for a small agency" and "what CRM do you use, we're 5 people" are one topic). Name each topic as the question people are actually asking.
5. **Score** each topic: number of posts × (1 + average comments / 10). Comment counts are in `details.comments_count` (a string; parse it). Many comments mean the community cares, or disagrees.
6. **Read the hottest threads.** For the top 3 to 5 posts, `/facebook/posts/comments?link=<post_link>` (1 credit per 30 comments) to see the answers people give: which products, tips or workarounds get recommended, and what's still unanswered.

## Output

```
## Question bank: <groups> (<members total> members), <window>
<n> posts read, <q> were questions or requests.

| # | Question people ask | Posts | Avg comments | Example (quote, link) |
|---|---|---|---|---|

### What the community recommends
<topic -> the answers / products that come up, with counts>

### Unanswered or badly answered
<topics where replies disagree or are thin: the best openings>

### Use it
- Content: 5 titles answering the top questions, in the members' words
- Product: 2 to 4 needs nobody solves well
- FAQ: questions to answer on the user's site or docs
```

Quote short phrases, not whole posts, and link each example.

## Respect the community

- Report themes and short quotes; don't build lists of members or profile individual posters. Omit names in the output unless the user needs to see a public page's answer.
- Don't suggest spamming groups. If the user wants to take part, suggest answering genuinely, within the group's rules.
