---
name: "movie-night-decider"
description: "AirnodeHub movie skill to choose picks by genre, year, mood, runtime, and ratings using attested MoviesDatabase and non-commercial OMDb data."
---

# Movie Night Decider

## Execute

1. Extract genre or mood, year range, runtime, audience, exclusions, and whether use is commercial. Ask only for a safety-critical audience constraint or unclear commercial context; otherwise default to six candidates and three finalists. **Done when:** usable constraints are known.

2. Read current documentation at `https://airnode-moviesdatabase.fly.dev/` and `https://airnode-omdb.fly.dev/`. Use only documented POST operations and parameters. **Done when:** contracts, licensing notes, costs, and signer addresses are known.

3. Discover through MoviesDatabase POST calls: `titles` for genre/year/list discovery, `searchByTitle` for a named film, or `searchByKeyword` for a documented theme. Use small limits and legal filter values. Before any paid, credentialed, or newly authorized call, state the scope and cost and obtain approval. **Done when:** an attested candidate set or exact blocker is received.

4. Shortlist up to three candidates. For each IMDb ID, POST `title` with `info:"base_info"` and `titleRatings`, or use the documented equivalent when sufficient. Never invent runtime, suitability, availability, or ratings. **Done when:** each finalist has sourced identity, details, and rating data.

5. Use OMDb only for personal or clearly non-commercial requests because its data is CC BY-NC. POST `getTitle` with the exact IMDb ID, `type:"movie"`, and `plot:"short"`; treat `Response:"False"` and `N/A` as missing. Attribute passed-on OMDb facts. **Done when:** cross-source data is collected where permitted or explicitly skipped.

6. Recommend one **Best pick tonight** and up to two alternatives. Give year, concise fit, sourced runtime, named rating sources, and one caveat. Do not imply ratings provide streaming availability. **Done when:** the user can choose quickly.

7. Retry discovery once with fewer filters. Omit unsupported fields instead of guessing; offer clearly labeled unsourced suggestions only after a real POST blocker. **Done when:** sourced choices or a transparent fallback is delivered.

## Verification

Confirm all data retrieval used documented POST operations, IDs remained consistent, explicit constraints were met, OMDb was used only non-commercially with attribution, and paid calls were approved. Require the attestation envelope fields; cryptographically verify the signer when tooling is available, otherwise do not claim independent verification.
