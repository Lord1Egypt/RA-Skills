---
name: local-spot-report
description: Report what's happening at and around a place on Instagram and Facebook - top and recent posts tagged at a venue, nearby spots ranked by activity, and the local businesses' pages - via SocialAPIs. Use when the user is scouting a location for a business, event or shoot, comparing venues or neighborhoods, researching a local competitor, or planning local marketing.
---

# Local spot report

Pick a place (a venue, a street, a park, a mall) and see how people post about it and what's popular nearby, from Instagram location tags and Facebook pages.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `instagram_location`, `instagram_search` and `facebook_search`.

## Ask first (only what's missing)

- The place name and city.
- The goal: open a business nearby, plan an event or shoot, check a competitor venue, or find local partners.
- For business research: the category (cafes, gyms, salons…).

## Budget

1 credit per call. A report is about 8 to 14 credits: search 1, location posts 2 to 4 (ranked + recent), nearby 1, Facebook page search 2 to 4, page details 2 to 4.

## Steps

1. **Find the location.** `/instagram/search?keyword=<place> <city>` and pick the place result; keep its `location_id`. Confirm with the user if there are several similar places.
2. **What gets posted there.**
   - `/instagram/location/posts?location_id=…&tab=ranked`: the top posts (what performs).
   - `/instagram/location/posts?location_id=…&tab=recent`, 1 to 3 pages: how busy it is right now (posts per day from timestamps).
   - From captions and post types: what people come for (food, views, events, shopping), common hashtags, times of day, photo vs reel.
3. **Around it.** `/instagram/location/nearby?location_id=…`: nearby places with category and post count. Rank by post count as a rough "how much social activity" measure, grouped by category.
4. **Local businesses on Facebook (business goals).** `/facebook/search/locations?query=<city or area>` for a `location_uid`, then `/facebook/search/pages?query=<category>&location_uid=…` (3 results per call, follow `end_cursor` 1 to 3 times). For the most relevant 3 to 5, `/facebook/pages/details?link=…`: followers, rating, website, category.
5. Optional, for a competitor venue: run its recent posts through the `social-scorecard` skill.

## Output

```
## <place>, <city>: local spot report (<date>)

Activity: ~<x> tagged posts/day recently. Top posts are mostly <type> about <themes>.

### What performs here
| Post (first line) | Type | Likes | Comments | Link |

### Nearby, by social activity
| Place | Category | Tagged posts |

### Local businesses (<category>)
| Page | Followers | Rating | Website |

### So what
3 to 5 points for the user's goal: e.g. gaps in the category nearby, best content angle, partners to approach.
```

## Limits

- Location tags are optional, so counts undercount real visits. Use them to compare places, not as footfall.
- Report places and businesses, not the people who post there. Don't list or profile individual posters.
