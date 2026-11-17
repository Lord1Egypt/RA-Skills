# Why this skill does not use Jobber's documented API

Jobber publishes a clean, well-documented GraphQL API. It is the wrong surface
for a customer, and the reason is worth writing down because the API looks so
much more appetising than scraping a portal.

## The two surfaces

| | Developer API | Client Hub |
| --- | --- | --- |
| Host | `api.getjobber.com/api/graphql` | `clienthub.getjobber.com` |
| Serves | the business running on Jobber | that business's customers |
| Auth | OAuth2 against an app you register | a secret hub URL + session |
| Node-reachable | yes | **no** — Cloudflare |

The Developer API is a **seller** surface. To use it you register an app in
Jobber's Developer Center, and the OAuth grant is authorized *by a Jobber
account* — the business's. As their customer you have no such account and
nothing to authorize. There is no consumer tier, and no scope that exposes "the
invoices sent to me".

## Probes that establish it

Verified 2026-08-09. The API accepts the client identity immediately, which is
what makes it tempting:

```sh
# unauthenticated: the field is hidden, not rejected
curl -s -X POST https://api.getjobber.com/api/graphql \
  -H 'Content-Type: application/json' \
  -H 'X-JOBBER-GRAPHQL-VERSION: 2025-04-16' \
  -d '{"query":"{ account { id name } }"}'
# -> "The field account on an object of type Query was hidden because you are
#     unauthenticated"  (HTTP 200)

# bogus bearer: the token is checked, so the transport is fine
curl -s -X POST https://api.getjobber.com/api/graphql \
  -H 'Authorization: Bearer nope' ... 
# -> {"message":"Token not recognized"}  (HTTP 401)

# the OAuth token endpoint exists and validates client credentials
curl -s -X POST https://api.getjobber.com/api/oauth/token \
  -d 'grant_type=authorization_code&client_id=x&client_secret=y&code=z'
# -> "The provided client id and secret do not match an existing application"
```

Everything works except the one thing that matters: the account those tokens
would reach is the vendor's, not yours.

Introspection is open unauthenticated and returns **410 queries and 629
mutations** — the full staff schema. That breadth is a trap, not an
opportunity: it is the surface Jobber's own web app uses, and every field of it
is gated on a staff session.

`clienthub.getjobber.com/api/graphql` answers introspection too, and returns
that *same* staff schema. It is not a client-facing API and not a shortcut.

## Cloudflare fingerprints the TLS client

The hub pages 403 with `<title>Just a moment...` from Node and curl, and keep
doing so when given a current Chrome User-Agent plus the full browser `Accept*`
set. What clears the challenge is being a real browser at the TLS layer, which
is why the request has to originate in the tab.

Two consequences worth stating plainly:

- **Do not add UA spoofing.** It does not work here, and code that spoofs a UA
  reads as though someone verified that it did.
- **A lifted cookie will not travel.** `cf_clearance` is bound to IP, UA and
  TLS fingerprint, so a cookie captured on a laptop is dead when replayed from
  a server. That is why the hosted MCP still fetches through your own tab over
  the bridge rather than replaying a captured session.

## If you *are* the business

Then the Developer API is the right answer and this skill is not: register an
app at `developer.getjobber.com`, take the `authorization_code` grant against
`https://api.getjobber.com/api/oauth/authorize`, and send
`X-JOBBER-GRAPHQL-VERSION` with every request. That is a different integration
with a different archetype — a bearer/direct-API client, no browser bridge.
