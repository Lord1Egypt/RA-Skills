# Instagram Discovery Module Rules

## 1. Module Scope

Use this module for broad Instagram search, hashtag search, music search, place search, city lookup, coordinate-based location search, and discovery seed resolution before content/user workflows.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. General and user-facing search

- Documentation: `https://docs.keyapi.ai/en/instagram/general_search.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/search_users.md`
- Purpose: Search broadly or find accounts by keyword.

### Best Suited For

- initial discovery when entity type is unclear
- creator/account search
- query exploration

### Routing Rules

- Use search users when the target is clearly an account.
- Use general search when the user asks for a broader Instagram search across surfaces.
- Route selected users to user rules and selected posts/Reels to content rules.

## 3. Hashtag and music seed resolution

- Documentation: `https://docs.keyapi.ai/en/instagram/search_hashtags.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/search_music.md`
- Purpose: Resolve hashtag or music/audio targets before fetching related posts.

### Best Suited For

- hashtag discovery
- audio/music trend seed selection
- topic expansion

### Routing Rules

- Use these endpoints before content endpoints when the user provides only text.
- Preserve returned IDs/names exactly for posts-by-hashtag or posts-using-music workflows.
- If multiple candidates are similar, present a short choice rather than guessing.

## 4. Place, city, and coordinate discovery

- Documentation: `https://docs.keyapi.ai/en/instagram/search_places.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_cities.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/search_by_coordinates.md`
- Purpose: Resolve location-based targets for local Instagram research.

### Best Suited For

- local place discovery
- city/region lookup
- coordinate-based location research
- venue or travel content workflows

### Routing Rules

- Use cities by country when the user needs city/region options.
- Use search places for place-name queries.
- Use coordinate search when the user provides latitude/longitude or asks for nearby locations.
- Route selected places/locations to content workflows only when the docs support the follow-on endpoint.

## 5. Reels and Explore discovery

- Documentation: `https://docs.keyapi.ai/en/instagram/search_reels.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_explore_sections.md`
- Documentation: `https://docs.keyapi.ai/en/instagram/fetch_section_posts.md`
- Purpose: Find short-video examples or Explore sections for content research.

### Best Suited For

- Reels topic discovery
- Explore category review
- creative inspiration research

### Routing Rules

- Use search reels for explicit Reels intent.
- Use explore sections before posts by section when section ID is unknown.
- Enrich selected results through content rules only after shortlisting.

## 6. Common Workflows

- Discovery to profile: search users/general search -> user info -> related/similar or content portfolio.
- Discovery to content: hashtag/music/place/Reels search -> selected content endpoint -> post detail/comments.
- Local discovery: country/city or coordinates -> place candidates -> selected location/content workflow.
