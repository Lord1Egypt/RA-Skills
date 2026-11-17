# Google Rules

Use this file for Google platform-level routing boundaries. Use module files for scenario-specific workflows.

## Entity Scope

queries, SERP results, images, Lens inputs, videos, news, shopping results, places, maps, reviews, scholar results, patents, autocomplete suggestions, and webpages

## Scenario Module Routing

- Use `google-search-rules.md` for web search and autocomplete.
- Use `google-webpage-rules.md` for selected URL/page extraction.
- Use `google-visual-rules.md` for images, Lens, and video search.
- Use `google-local-rules.md` for places, maps, and reviews.
- Use `google-vertical-rules.md` for news, shopping, scholar, and patents.

## Identifier Discipline

- Treat queries, URLs, place/review inputs, image URLs, and vertical surfaces as different input types.
- Use webpage extraction when page content is required; search snippets are not source content.

## Output Guidance

- Name the Google surface used in the final answer.
- Separate search-result evidence from extracted-page evidence.
