# Sift Query Rewrite

## Purpose
Transform vague user queries into precise search queries using available context.

## Context Sources
- Conversation context — recent messages and topics
- Geolocation — if available from Relay or user profile
- Chronicle data — if Elephas is installed, use entity context
- Entity resolution — resolve ambiguous references from prior messages

## Rewrite Process
1. Parse the original query for intent and key entities
2. Expand with context (location, known entities, conversation topic)
3. Generate 1-3 specific search queries optimized for the target provider
4. For domain-scoped queries, add site: prefix

## Examples

Original: "best ramen near me"
Rewrite: ["ramen restaurants San Francisco reviews", "site:eater.com ramen san francisco", "site:yelp.com ramen san francisco"]

Original: "how does LadybugDB compare"
Rewrite: ["LadybugDB vs Neo4j graph database comparison", "LadybugDB embedded graph database review", "LadybugDB performance benchmarks"]

## Domain-Scoped Queries
When a user specifies a domain, restrict scope: "site:arxiv.org graph database" → search only that domain.

## Local Search Verticals
For local queries, use vertical-specific patterns: Google Maps, Yelp, OpenTable, Tock, Doordash, Instacart, Zocdoc. Also local media: Eater, SFist, Honolulu Magazine.

## URL Handling
If a user provides a URL: retrieve the page, perform structured extraction, summarize content. Do not search for the URL — fetch it directly.
