# OneHome GraphQL + REST operations for fpx

Ready-to-run bodies for `fpx post-json 'https://services.onehome.com/graphql' @body.json -p onehome -H "Authorization: $TOKEN" -H 'Origin: https://portal.onehome.com' -H 'Referer: https://portal.onehome.com/'`.
Every query string and variable shape below is drawn from `src/queries.ts`
in this repo (the same documents `onehome-mcp`'s tools send) — some are
copied verbatim, others are trimmed field subsets for readability here,
but none are guessed. Get `$TOKEN` first (see `../SKILL.md`).

Pattern: write the GraphQL text to a file (a heredoc avoids shell-quoting
the doc), assemble the JSON body with `jq -n --rawfile`, then POST:

```sh
cat > /tmp/q.graphql <<'GQL'
<query text>
GQL
jq -n --rawfile query /tmp/q.graphql --argjson variables '<vars>' \
  '{query:$query, variables:$variables}' > /tmp/body.json
fpx post-json 'https://services.onehome.com/graphql' @/tmp/body.json -p onehome \
  -H "Authorization: $TOKEN" -H 'Origin: https://portal.onehome.com' \
  -H 'Referer: https://portal.onehome.com/' | jq '.data'
```

Always check for GraphQL errors first: `jq '.errors // empty'` (an errors
array can ride in an HTTP-200 body — e.g. `Access Denied` on agent-only
fields for a consumer session).

---

## 0. Auth bootstrap — email-token → sessionToken (REST, not GraphQL)

`POST /api/authentication/checkToken` — the Angular app's own load-time
exchange. Not auth-gated itself; needs no `Authorization` header. See
`../SKILL.md`'s "Path A" for the full flow (extracting `?token=` from the
magic link, running this, and deriving `$TOKEN`).

```json
{ "emailToken": "REPLACE_WITH_URL_TOKEN_PARAM" }
```

Response fields used downstream: `sessionToken` (the bearer JWT),
`groupID`, `savedSearchID`, `agentID`, `contactID`, `mlsID`, `email`,
`signedIn`, `registered`.

```sh
fpx post-json 'https://services.onehome.com/api/authentication/checkToken' @/tmp/checktoken-body.json -p onehome \
  -H 'Origin: https://portal.onehome.com' -H 'Referer: https://portal.onehome.com/' \
  | jq '{sessionToken, groupID, savedSearchID, agentID, contactID, mlsID, email}'
```

---

## 1. User + groups — `GetOneHomeUser` (agent sessions only)

Returns `Access Denied` for a consumer-share session (the `user` field is
agent-only) — try `GetSavedSearchBySearchId` (§2) first unless you know
this is an agent session.

```graphql
query GetOneHomeUser {
  user {
    id
    firstName
    lastName
    email
    phone
    registered
    lastAccessedGroupId
    lastAccessedSavedSearchId
    userWelcomed
    groups {
      id
      firstName
      lastName
      contactId
      emails
      contactStatus
      createdAt
      agent {
        id
        firstName
        lastName
        fullName
        email
        phone
        officeName
        officePhone
        teamName
        mls {
          mlsid
        }
      }
    }
  }
}
```

No variables.

```sh
jq -r '.data.user.groups[] | "\(.id)\t\(.firstName) \(.lastName)"'
```

## 2. Saved search by id — `GetSavedSearchBySearchId` (consumer-readable)

The by-groupId variant is agent-only; this one works for a consumer share.
`savedSearch.listingIds` feeds §4.

```graphql
query GetSavedSearchBySearchId($searchId: String!) {
  savedSearch(id: $searchId) {
    id
    name
    createdAt
    updatedAt
    setType
    listingIds
    isActive
    resourceID
    userQuery {
      fieldName
      type
      values
    }
    polygon {
      latitude
      longitude
    }
  }
}
```

```json
{ "searchId": "REPLACE_WITH_SAVED_SEARCH_ID" }
```

```sh
jq -r '.data.savedSearch | "\(.name): \(.listingIds | length) listings"'
```

## 3. Group listings — `GetListings` (`listings(groupId, browseParameter)`)

Free-form filter via `BrowseParameter` (`searchQuery` / `sort` /
`pageInput`). Often returns 0 for a consumer session — the consumer view
is usually scoped to a saved search (§4), not the group as a whole.

```graphql
query GetListings($groupId: String!, $browseParameter: BrowseParameter, $includeDislikes: Boolean) {
  listings(groupId: $groupId, browseParameter: $browseParameter, includeDislikes: $includeDislikes) {
    pageInfo {
      totalElements
      totalPages
      pageNumber
      pageSize
    }
    listings {
      id
      hideWhenUnauth
      property {
        OriginatingSystemKey
        StreetNumber
        StreetName
        StreetSuffix
        UnitNumber
        City
        StateOrProvince
        PostalCode
        ListPrice
        LivingArea
        PropertyType
        BedroomsTotal
        BathroomsTotalInteger
        Latitude
        Longitude
        StandardStatus
        MajorChangeType
        MajorChangeTimestamp
        PreviousListPrice
      }
      UnparsedAddress
      customProperty {
        ListingKey
        FIPSCode
      }
    }
  }
}
```

```json
{
  "groupId": "REPLACE_WITH_GROUP_ID",
  "browseParameter": { "pageInput": { "pageNum": 0, "size": 50 } },
  "includeDislikes": false
}
```

```sh
jq -r '.data.listings | "total=\(.pageInfo.totalElements)", (.listings[] | "\(.id)\t\(.property.ListPrice)\t\(.UnparsedAddress)")'
```

## 4. Saved-search listings — `GetSavedListings` (`listingsBySavedSearchId`) — the canonical consumer view

What the portal renders for "Homes at `<name>`". Supply `listingIds` from
§2's `savedSearch.listingIds`.

```graphql
query GetSavedListings($groupId: String!, $listingIds: [String!]!, $sort: SortCriteria, $pageInput: PageInput, $savedSearchId: String!, $includeDislikes: Boolean!, $suppressEvent: Boolean!) {
  listingsBySavedSearchId(groupId: $groupId, osks: $listingIds, sort: $sort, pageInput: $pageInput, savedSearchId: $savedSearchId, includeDislikes: $includeDislikes, suppressEvent: $suppressEvent) {
    pageInfo {
      totalElements
      totalPages
      pageNumber
      pageSize
    }
    listings {
      id
      property {
        StreetNumber
        StreetName
        City
        StateOrProvince
        ListPrice
        LivingArea
        BedroomsTotal
        BathroomsTotalInteger
        StandardStatus
      }
      UnparsedAddress
    }
  }
}
```

```json
{
  "groupId": "REPLACE_WITH_GROUP_ID",
  "savedSearchId": "REPLACE_WITH_SAVED_SEARCH_ID",
  "listingIds": ["REPLACE", "WITH", "IDS", "FROM", "SECTION", "2"],
  "sort": { "name": "property.MajorChangeTimestamp", "order": "DESC" },
  "pageInput": { "pageNum": 0, "size": 50 },
  "includeDislikes": false,
  "suppressEvent": true
}
```

```sh
jq -r '.data.listingsBySavedSearchId.listings[] | "\(.id)\t\(.property.ListPrice)\t\(.UnparsedAddress)"'
```

## 5. Free-text search — `ListingSuggestionsSearch` (works without a group scope)

Useful for an MLS-number / address lookup when you don't know the group id
yet. `groupId` is optional.

```graphql
query ListingSuggestionsSearch($browseParameter: String!, $groupId: String) {
  listingSuggestionsSearch(browseParameter: $browseParameter, groupId: $groupId) {
    id
    listingId
    postalCode
    city
    stateOrProvince
    streetName
    streetNumber
    unitNumber
    bedroomsTotal
    bathroomsTotalInteger
    listPrice
    media {
      Image {
        Thumbnail {
          mediaUrl
          width
          height
        }
      }
    }
  }
}
```

```json
{ "browseParameter": "123 Main St", "groupId": null }
```

```sh
jq -r '.data.listingSuggestionsSearch[] | "\(.id)\t\(.listPrice)\t\(.streetNumber) \(.streetName), \(.city)"'
```

## 6. Listing detail by id — `ListingById` (`listingDetail`)

`listingId` is an OSK (from any of the searches above, or from a portal
URL — the trailing path segment). `groupId` is required; `savedSearchId`
is optional context.

```graphql
query ListingById($listingId: String!, $groupId: String!, $savedSearchId: String, $suppressEvent: Boolean = true) {
  listingDetail(listingId: $listingId, groupId: $groupId, savedSearchId: $savedSearchId, suppressEvent: $suppressEvent) {
    id
    createdAt
    property {
      StreetNumber
      StreetName
      City
      StateOrProvince
      PostalCode
      ListPrice
      LivingArea
      BedroomsTotal
      BathroomsTotalInteger
      YearBuilt
      AssociationFee
      AssociationFeeFrequency
      TaxAnnualAmount
      TaxYear
      PublicRemarks
      Latitude
      Longitude
      VirtualTourURLUnbranded
    }
    UnparsedAddress
    rooms {
      RoomType
      RoomLevel
      RoomDimensions
      RoomFeatures
    }
    openHouse {
      OpenHouseDate
      OpenHouseStartTime
      OpenHouseEndTime
      OpenHouseType
    }
  }
}
```

```json
{
  "listingId": "REPLACE_WITH_LISTING_OSK",
  "groupId": "REPLACE_WITH_GROUP_ID",
  "savedSearchId": null,
  "suppressEvent": true
}
```

```sh
jq '.data.listingDetail | {addr: .UnparsedAddress, price: .property.ListPrice, beds: .property.BedroomsTotal, baths: .property.BathroomsTotalInteger}'
```

## 7. Listing photos — `MediaListingById`

```graphql
query MediaListingById($listingId: String!, $groupId: String!, $suppressEvent: Boolean = true) {
  listingDetail(listingId: $listingId, groupId: $groupId, suppressEvent: $suppressEvent) {
    id
    media {
      LongDescription
      ShortDescription
      MediaType
      Order
      Image {
        Thumbnail {
          mediaUrl
          width
          height
        }
        Medium {
          mediaUrl
          width
          height
        }
        Large {
          mediaUrl
          width
          height
        }
      }
    }
  }
}
```

```json
{ "listingId": "REPLACE_WITH_LISTING_OSK", "groupId": "REPLACE_WITH_GROUP_ID", "suppressEvent": true }
```

```sh
jq -r '.data.listingDetail.media[] | select(.Image.Large) | .Image.Large.mediaUrl'
```

---

## 8. LocalLogic — schools / walk score (REST, not GraphQL)

The portal bundle wraps these in an Apollo `@rest` directive, which is a
client-side construct — POSTing the "query" to `/graphql` fails with
`UnknownDirective 'rest'`. Hit the real REST URLs directly with `fpx get`,
same bearer:

```sh
fpx get 'https://services.onehome.com/api/locallogic/scores?lat=35.4382&lng=-82.1968&locale=en-US' -p onehome \
  -H "Authorization: $TOKEN" -H 'Origin: https://portal.onehome.com' | jq '.'

fpx get 'https://services.onehome.com/api/locallogic/schools?lat=35.4382&lng=-82.1968&locale=en-US' -p onehome \
  -H "Authorization: $TOKEN" -H 'Origin: https://portal.onehome.com' | jq '.'
```

`schools` frequently 403s for a consumer-share session (agent-only
dataset) — `scores` (walk score + school-proximity summaries) is the
consumer-safe equivalent. `lat`/`lng` come from `ListingById`'s
`property.Latitude`/`property.Longitude` (§6).
