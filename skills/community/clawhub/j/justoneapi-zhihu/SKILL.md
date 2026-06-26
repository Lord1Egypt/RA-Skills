---
name: Zhihu API
description: Search Zhihu topics, inspect answer lists, read column article detail, and track column article feeds through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_zhihu"}}
---

# Zhihu

Use this skill for Zhihu question research, answer mining, 专栏文章采集, and topic discovery. It fits analyst workflows where the user starts from a keyword, question ID, article ID, or column ID and wants structured Zhihu data rather than a high-level summary.

## When To Use It

- The user wants Zhihu keyword search, question answer extraction, or column article research.
- The task is about a specific Zhihu question, answer feed, 专栏文章, or column page.
- The user can provide `keyword`, `questionId`, `id`, `columnId`, or pagination values such as `cursor` and `offset`.
- The user needs Zhihu-native titles, content, authors, ranking context, or article metadata sourced directly from the API.

## Representative Operations

- `searchV1`: Keyword Search — Search Zhihu by keyword for topic discovery, source gathering, and question scouting.
- `getAnswerListV1`: Answer List — Pull the answer feed for a Zhihu question to inspect authors, content, and interaction signals.
- `getColumnArticleDetailV1`: Column Article Details — Read a single Zhihu column article in detail for archiving and content analysis.
- `getColumnArticleListV1`: Column Article List — Track the article feed of a Zhihu column for monitoring and collection work.

## Request Pattern

- 4 read-only `GET` operations are available in this skill.
- Common inputs are `keyword`, `questionId`, `columnId`, `id`, `cursor`, `offset`, and `order`.
- The workflow splits cleanly into search, question-answer feeds, single article detail, and column article listing.
- No operation in this skill requires a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchV1`, `getAnswerListV1`, `getColumnArticleDetailV1`, `getColumnArticleListV1`.
3. Pick the smallest matching operation instead of guessing.
4. Ask the user for any missing required parameter. Do not invent values.
5. Call the helper with:

```bash
node {baseDir}/bin/run.mjs --operation "<operation-id>" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

## Environment

- Required: `JUST_ONE_API_TOKEN`
- This skill uses `JUST_ONE_API_TOKEN` only for authenticated Just One API requests.
- Keep `JUST_ONE_API_TOKEN` private. Do not paste it into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu&utm_content=project_link).

## Output Rules

- Lead with the concrete Zhihu result: matched topic, answer feed insight, article detail, or column update.
- For keyword search, restate the keyword and offset before summarizing the most relevant matches.
- For answer-list requests, surface the question scope, top authors, engagement cues, and any ordering rule before raw JSON.
- For column-article requests, extract title, author, publication context, and the most important content signals before raw JSON.
- If the backend errors, include the backend payload and the exact operation ID.
