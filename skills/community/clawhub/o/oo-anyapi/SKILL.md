---
name: oo-anyapi
description: "AnyAPI (getanyapi.com). Use this skill for ANY AnyAPI request — reading, creating, and updating data. Whenever a task involves AnyAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AnyAPI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["anyapi"]
  icon: "https://static.oomol.com/logo/third-party/anyapi.svg"
---

# AnyAPI

Operate **AnyAPI** through your OOMOL-connected account. This skill calls the `anyapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AnyAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "anyapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "anyapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `aliexpress_product` — Look up one AliExpress product by id and get its price, original price, rating, reviews count, images, options, variants with stock, specifications, store, ship-from country and delivery estimate in one normalized response.
- `aliexpress_reviews` — Get one page of buyer reviews for an AliExpress product by id, with rating, text, buyer country, date, bought variant and photos for each review, plus the product's total reviews, average rating and star distribution, in one normalized response.
- `aliexpress_search` — Search AliExpress by keyword with optional sort, price-range, page, ship-to country and currency, and get title, price, original price, units sold and image for each product in one normalized response.
- `asos_product` — Fetch an ASOS product by URL from any of its 11 country stores and get title, price, brand, colour, description, images, and per-size stock in one normalized response.
- `asos_search` — Search ASOS by keyword in any of its 11 country stores with optional sort, price-range, and page filters and get title, price, brand, and colour for each product in one normalized response.
- `bestbuy_product` — Fetch a BestBuy.com product by URL and get title, price, brand, model, UPC, rating, description, and images in one normalized response.
- `bestbuy_reviews` — Pull a page of 10 customer reviews for any BestBuy.com product by URL, newest first or by relevance, helpfulness, or rating: rating, title, text, date, reviewer, and verified-purchase badge.
- `bestbuy_search` — Search BestBuy.com by keyword with optional sort, price-range, and page filters and get title, price, rating, and brand for each product in one normalized response.
- `bluesky_post` — Get a single Bluesky post by URL - text, author handle, like, reply, and repost counts as clean JSON.
- `bluesky_profile` — Get a Bluesky user's public profile by handle - display name, bio, follower and post counts as clean JSON.
- `bluesky_user_posts` — List a Bluesky account's recent posts (text, author handle, like, reply, and repost counts) by handle as clean JSON.
- `congress_trades` — Get US Congress members' financial disclosures and stock trades (member, ticker, transaction type, amount range, and dates), filterable by member, ticker, or date range. Results come newest filing first (by reportedUtc, not tradedUtc), so a recent filing can list trades made years earlier.
- `email_finding_hunter_count` — Count how many contacts a company domain has, split by personal and generic mailboxes and broken down by department and seniority. Scope a domain for $1 per 1,000 requests before paying per contact.
- `email_finding_hunter_domain` — Find named contacts and their work email addresses at a company domain, filtered by job title, seniority or department. Priced per returned contact, so limit is the cost control.
- `email_finding_zerobounce_domain` — Read the email address format a company domain uses, with every alternative format ZeroBounce has seen and how confident it is in each. Use it to build addresses for a whole account at once.
- `email_verification_allegrow` — Validate an email address and return its deliverability verdict and mailbox signals.
- `email_verification_bounceban` — Verify an email address, including catch-all handling. Completion uses the durable Request lifecycle; a negative verdict is a successful result. [write]
- `email_verification_icypeas` — Verify an email address. A valid negative verdict is a successful, billable result.
- `email_verification_zerobounce` — Validate one email address against ZeroBounce, with the deliverability verdict, why it was reached, the mailbox provider, and any owner details ZeroBounce holds. A negative verdict is a successful, billable result.
- `email_verification_zerobounce_activity` — Check whether an email address has shown recent activity across ZeroBounce's engagement network before you re-engage it. A no-activity answer is a successful, billable result.
- `facebook_events` — List public Facebook events for a city or place by its events-page URL (event name, date, venue, and attendance) as normalized JSON.
- `facebook_followers` — List the public followers (or accounts followed) of any Facebook page or profile URL as normalized JSON records.
- `facebook_marketplace_location_search` — Resolve a place name to Facebook Marketplace locations with coordinates and metadata as normalized JSON.
- `facebook_page_lookup` — Look up Facebook Pages and profiles by name with Facebook's own quick search. A name lookup that returns basic identity fields only: name, URL, profile image, Facebook id, and verified status. Matches can include personal profiles as well as Pages. For full Page details (category, followers, phone, website), use facebook.search_pages.
- `facebook_search_pages` — Search Facebook Pages by keyword, optionally narrowed to a location, and get structured page profiles (name, category, followers, contact details).
- `fiverr_search` — Extract Fiverr gig listings from any search or category URL: titles, sellers, ratings, and pricing as structured JSON.
- `get_balance` — Read the USD wallet balance associated with your AnyAPI key without a paid business call.
- `get_request` — Read a durable AnyAPI request and its retained result without submitting another paid job.
- `get_result` — Read or reshape an AnyAPI cached result without executing the business request again.
- `github_repository_readme` — Get a GitHub repository's README by repository URL, as the Markdown text the maintainers wrote, with its file name, path and size. Use it to learn what a project does, which models and tools it uses, and how to reach its authors.
- `github_trending_developers` — List trending GitHub developers (rank, username, name, avatar, and their most popular repository), optionally filtered by programming language and time range.
- `github_trending_repositories` — List GitHub Trending repositories (rank, stars, stars gained today, language, and description), filterable by language and time window.
- `github_user_activity` — List a GitHub user's public contribution activity by handle (grouped monthly summaries of commits, pull requests, and issues with repository links) for a given year.
- `github_user_contributions` — Fetch a GitHub user's contribution graph for a year (total contributions plus per-day counts and heatmap intensity).
- `github_user_followers` — List a GitHub user's followers by handle (each follower's login, type, avatar, and profile URL) with pagination.
- `github_user_following` — List the GitHub users a given user follows by handle (each account's login, type, avatar, and profile URL) with pagination.
- `github_user_pull_requests` — List a GitHub user's public pull requests by handle (title, repository, state, creation date, and URL) with optional date filtering and pagination.
- `google_hotels_details` — Get one hotel from Google Hotels by its property ID: address, phone, website, rating, nightly price, prices from each booking site, amenities and check-in times as normalized JSON.
- `google_hotels_search` — Search Google Hotels by destination and dates and get hotels with their Google property ID, nightly price, rating, review count, coordinates, star class and photos as normalized JSON.
- `google_job` — Fetch one Google Jobs listing by the listingToken that google.jobs returns: title, company, location, the site it was found on, the full description, apply links on every board that carries it, the posting details Google shows (posted, pay, job type, benefits), and the employer's ratings on review sites such as Glassdoor and Indeed when Google shows them.
- `google_jobs` — Search Google Jobs, the job listings Google gathers from LinkedIn, Indeed, ZipRecruiter, company career sites and other boards, and get about 10 listings per call: title, company, location, the site it was found on, the full description, apply links on every board that carries it, and the posting details Google shows (posted, pay, job type, benefits). Each listing carries a listingToken you can pass to google.job for employer ratings. Send nextCursor back as cursor to walk further pages.
- `hackernews_profile` — Get a Hacker News user's public profile by username - karma, bio, and account details as clean JSON.
- `hackernews_story` — Get a Hacker News story by id - title, link, author, points, and comment count as clean JSON.
- `hackernews_story_comments` — List the comments on a Hacker News story by id - text, author, and timestamp as clean JSON.
- `ikea_search` — Search IKEA's US store by keyword and get title, price, rating, and image for each product in one normalized response.
- `levels_jobs` — Search Levels.fyi job listings by title or keyword and get each job with its salary range and estimated total compensation where Levels.fyi has them, plus company, location, posting date and apply link. Returns up to 20 jobs per call, grouped by company; filter by location and sort by relevance, date or pay.
- `linkedin_ads` — Search the LinkedIn Ad Library by search URL and list the matching ads (advertiser, creative text, format).
- `linkedin_group` — Fetch one LinkedIn group by URL or id: name, description, rules, member count, logo and cover image, creation date, visibility and join settings, and its admins.
- `linkedin_group_posts` — List the posts in a LinkedIn group by group URL, newest first: full text, canonical link, publish date, author, engagement counts with a per-reaction breakdown, and attached media. One call returns a page of about 100 posts; pass page to go further back.
- `linkedin_search_groups` — Search LinkedIn groups by keyword, 10 per page: group name, URL, member count, summary, and logo.
- `linkedin_search_services` — Find freelancers and service providers on LinkedIn by the service they offer (e.g. 'Web Development'), optionally in a location. One call returns a page of up to 10 people, each with name, headline, location, about text, photo, profile URL, service page URL, and the list of services they offer. The profile URL can be passed to linkedin.profile for the full record.
- `linktree_profile` — Get a public Linktree page by URL: title, bio, picture, contact email, linked social accounts, and every link card with its destination.
- `naver_blog_search` — Search up to five enriched Naver blog results by keyword with stable cursor pagination: result rank, title, excerpt, post and blogger URLs, blogger name, publish time, and Naver's total match count.
- `nextdoor_business` — Fetch one Nextdoor business page by its slug, with phone, email, website, and street address.
- `nextdoor_search` — Find local businesses listed on Nextdoor by city and trade category, with phone, email, website, and street address.
- `pexels_search_photos` — Search Pexels for free stock photos by keyword. Returns image URLs in several sizes, dimensions, alt text, the photographer's name and profile, and the photo's Pexels page.
- `property_records_enformion` — Look up the public property records for one US address: current and previous owners, parcel number (APN), last sale, assessed and market values, property tax, beds, baths, living area, lot size, year built, land use, and zoning. One address can match several parcels, and every match is returned. Billed only when a record is found.
- `redfin_property` — Fetch full details for a single Redfin home by its listing URL (price, beds, baths, square feet, address, listing agent, description and photos) as normalized JSON.
- `redfin_search` — Run a Redfin map search by URL and get matching home listings (price, address, beds, baths, status) as normalized JSON.
- `samsclub_product` — Fetch a SamsClub.com product by URL and get title, member price, stock, brand, model, UPC, rating, description, and images in one normalized response.
- `samsclub_search` — Search SamsClub.com by keyword with optional sort, price-range, and page filters and get title, member price, stock, and rating for each product in one normalized response.
- `slickdeals_deal` — Fetch one Slickdeals deal by URL and get title, price, list price, store, coupon code, score, views, comments, and description in one normalized response.
- `slickdeals_search` — Search Slickdeals deals by keyword with optional sort, price, discount, and page filters and get title, price, list price, store, score, and comment count for each deal in one normalized response.
- `snapchat_profile` — Fetch a Snapchat user's public profile by username: display name, bio, subscriber count, and recent public content.
- `spotify_album` — Fetch a Spotify album's tracklist, play counts, label, and release details by album URL or ID.
- `spotify_artist` — Fetch a Spotify artist's discography (albums, singles, top tracks) and metadata by artist URL or ID.
- `spotify_play_count` — Fetch stream counts and stats for a Spotify track, album, or artist URL.
- `spotify_podcast` — Fetch a Spotify podcast show's name, publisher, description, rating, and topics by show URL or ID.
- `spotify_podcast_episodes` — List a Spotify podcast show's episodes with titles, durations, descriptions, and release dates by show URL or ID.
- `spotify_search` — Search Spotify for matching tracks, albums, artists, podcasts, and playlists by keyword.
- `spotify_track` — Fetch a Spotify track's play count, popularity, duration, and album details by track URL or ID.
- `target_product` — Fetch a Target.com product by URL and get title, price, brand, rating, description, and images in one normalized response.
- `target_reviews` — Pull a page of 10 customer reviews for any Target.com product by URL, newest first or by helpfulness or rating: rating, title, text, date, reviewer, and verified-purchase badge.
- `target_search` — Search Target.com by keyword with optional sort, price-range, and page filters and get title, price, rating, and brand for each product in one normalized response.
- `tripadvisor_reviews` — Fetch the latest reviews for any Tripadvisor hotel, restaurant, or attraction by its page URL: rating, text, date, and trip details as normalized JSON.
- `tripadvisor_search` — Search Tripadvisor for hotels, restaurants, and attractions in any destination and get rich place records (ratings, review counts, contact details, pricing) as normalized JSON.
- `truthsocial_post` — Get a single Truth Social post by its URL - text, author, engagement (likes, comments, shares), and timestamp as clean JSON.
- `truthsocial_profile` — Get a Truth Social account's public profile by handle - display name, bio, follower/following counts, and post count as clean JSON.
- `unsplash_search_photos` — Search Unsplash for free stock photos by keyword. Returns image URLs in several sizes, dimensions, alt text, the photographer's name and profile, and the photo's Unsplash page.
- `yelp_search` — Search Yelp for businesses by keyword and location: up to 20 listings with ratings, categories, and core business info per request.
- `zillow_agent` — Fetch one Zillow real estate agent's profile by URL: name, phone, email, brokerage, rating, review count, sales, and service areas.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AnyAPI state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AnyAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/anyapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- AnyAPI homepage: https://getanyapi.com
- API documentation: https://getanyapi.com/docs
