# Reddit Discovery Module Rules

## 1. Module Scope

Use this module for Reddit dynamic search, typeahead, trending searches, popular/home/news/games feeds, and user activity discovery.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Dynamic search and query expansion

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_dynamic_search.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_search_typeahead.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_trending_searches.md`
- Purpose: Discover posts, communities, comments, media, users, search suggestions, and trending topics.

### Best Suited For

- topic discovery
- community discovery
- query expansion
- current interest monitoring

### Routing Rules

- Use dynamic search for explicit keyword search.
- Use typeahead for search-seed expansion.
- Use trending searches when the user asks what topics are currently trending.
- Route selected posts to post/comment rules and selected communities to community rules.

## 3. Feed surface monitoring

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_popular_feed.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_home_feed.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_news_feed.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_games_feed.md`
- Purpose: Retrieve different Reddit feed surfaces.

### Best Suited For

- popular content scan
- news feed monitoring
- gaming topic scan
- home-style recommendation review

### Routing Rules

- Use the feed that matches the user surface request.
- Enrich selected posts with post detail/comments only when deeper analysis is needed.
- Do not mix feed surfaces without labeling them.

## 4. User activity discovery

- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_profile.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_posts.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_comments.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_trophies.md`
- Documentation: `https://docs.keyapi.ai/en/reddit/fetch_user_active_subreddits.md`
- Purpose: Retrieve profile, posts, comments, trophies, and active communities for a Reddit user.

### Best Suited For

- user activity reports
- interest mapping
- post/comment history review
- account context

### Routing Rules

- Use user profile first when identity/context is unknown.
- Fetch posts/comments/trophies/active subreddits only as requested.
- Route selected posts/comments to post/comment rules for deeper thread analysis.

## 5. Common Workflows

- Topic discovery: typeahead/trending -> dynamic search -> selected post/community enrichment.
- Feed monitor: chosen feed -> batch/single post details for selected posts -> comments if requested.
- User report: user profile -> posts/comments/trophies/active subreddits by section.
