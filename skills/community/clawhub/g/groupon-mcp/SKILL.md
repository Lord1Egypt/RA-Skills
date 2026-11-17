---
name: groupon
description: Search and read Groupon deals from the terminal via curl — the consumer GraphQL API (deal search/browse, deal detail, category taxonomy). Anonymous, no key or login. Use when asked to find Groupon deals, look up a specific deal, or browse a city's offers.
---

# Groupon deals via curl

Groupon's consumer deal data comes from **one GraphQL endpoint** that answers a
plain server-side `curl` with **no cookies, no key, no login, no bot wall**:

```
POST https://www.groupon.com/mobilenextapi/graphql
  -H 'content-type: application/json'
  -H 'apollographql-client-name: mobilenextapi'
```

Requests are a **batched JSON array** of Apollo **persisted-query** operations
(`operationName` + `variables` + `extensions.persistedQuery.sha256Hash`, no query
text — introspection is off and the server masks GraphQL errors as opaque 400
HTML, so you cannot hand-author queries). The response is a **JSON array**;
`.[0].data.<field>` holds the payload. Ready-to-run bodies + `jq` recipes are in
[`references/graphql-queries.md`](references/graphql-queries.md).

## The three operations

| Need | Op | Root field |
|------|----|-----------|
| Search / browse a city's deals | `BrowseDealFeed` | `.[0].data.browseDealFeed.cards` |
| One deal's full detail (options, price, reviews, fine print) | `getDeal` | `.[0].data.getDeal` |
| Category taxonomy | `GetMainNavigation` | `.[0].data...` |

`division` is a Groupon **city slug** (`new-york`, `chicago`, `syracuse`, `los-angeles`, …).
`dealId` for `getDeal` is a deal's **permalink slug** = the last path segment of a
card's `.url` (`https://www.groupon.com/deals/<dealId>`).

## Two failure modes

- **Empty / non-JSON 2xx** → almost always a challenge interstitial; retry, don't `JSON.parse` it blind.
- **`{"errors":[{"message":"PersistedQueryNotFound"}]}`** → the baked `sha256Hash`
  went stale (Groupon redeployed its frontend queries). **Re-capture it:**
  1. Open a Groupon search page in a signed-in-or-not browser, DevTools → Network.
  2. Filter for `mobilenextapi/graphql`, click the request whose payload `operationName`
     matches the one you need.
  3. Copy `extensions.persistedQuery.sha256Hash` from the request payload and replace
     the stale hash in `references/graphql-queries.md`. (The hash is a public query
     fingerprint, not a secret.)

Note: the deal **web page** `groupon.com/deals/<slug>` returns 403 to servers, but
the `getDeal` GraphQL op above returns the same detail with no auth.

## In context groups

When this server runs behind mcp-host, its tools join the **food** group
(`_meta.mint.domain: "food"`). It has **no canonical read**: Groupon is a
public deal catalogue plus your signed-in cart, and neither is a dated,
per-person feed, so a "what's new / due / on" ask fans out to the group's
other members (reservations, orders) and not to Groupon. There are no
subjects to pick from either. The hints only place the tools in the group:
the deal reads and `groupon_view_cart` are lookups, `groupon_purchase` and
`groupon_clear_cart` are cart changes (still confirmation-gated).

A compound ask looks like "what's on for dinner this week, and any Groupon
deals for pizza nearby?": the group answers the first half from its
canonical reads and the second by calling `groupon_search_deals`.

The deal reads are anonymous and always answer. The cart tools need a
groupon.com session lifted through the browser bridge (or
`GROUPON_SESSION_COOKIE`); without one, the group answers that Groupon
**needs your browser open** for the cart.
