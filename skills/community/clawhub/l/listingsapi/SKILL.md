---
name: listingsapi
description: Use the hosted ListingsAPI MCP server to inspect business locations, publisher listings, reviews, posts, and local analytics, or help a user try its Day Pass sandbox. Use the existing listingsapi-integration skill for adding the REST API to an application.
metadata:
  openclaw:
    homepage: https://listingsapi.com/mcp
    primaryEnv: LISTINGSAPI_API_KEY
    envVars:
      - name: LISTINGSAPI_API_KEY
        required: false
        description: Existing user-managed ListingsAPI key for API-key authentication; unnecessary when the connected MCP client uses OAuth.
---

# ListingsAPI

Use ListingsAPI through an already connected MCP client at `https://listingsapi.com/mcp` with Streamable HTTP. This skill supplies workflow instructions; it does not install an MCP client, start a local server, or bundle executable code. If the runtime has no MCP connection, explain the connection prerequisite rather than inventing an OpenClaw configuration or installing a bridge.

ListingsAPI is an external service. A paid plan is normally required for production use. The limited-availability Day Pass covers only sandbox locations and listings.

This skill is released under MIT-0; see [LICENSE](LICENSE). That license applies to the skill, not to the hosted ListingsAPI service.

## Authentication

Prefer the client's public OAuth browser flow when supported. ListingsAPI advertises dynamic client registration and PKCE, with `read` and `write` scopes; no pre-issued client secret is needed. Start with read access unless the user's task requires writes. The user completes sign-in and consent.

For an existing user-managed key, use `Authorization: API <key>`. If the runtime reads it from the environment, use `LISTINGSAPI_API_KEY`; never embed the value in this skill, generated source, logs, or chat. OAuth bearer tokens apply to the MCP endpoint; REST requests use the `API` key prefix. Do not create credentials or configure accounts without the user's authorization.

## Read an account

Use `whoami` to establish the connected account, then `locations_all` or `locations_search` to identify the requested location. Resolve the location before fetching `listings_premium`, `reviews_list`, or publisher analytics. Read `get_usage` when usage is relevant. An empty list is possible for a new account.

Use `search_docs`, `get_doc`, and `get_endpoint` to check current contracts before constructing inputs. These tools and the [MCP guide](https://listingsapi.com/guides/connect-an-ai-agent-with-mcp) are the source for supported operations; do not assume every REST operation has an MCP equivalent. Archive and delete operations are not exposed through MCP.

## Try the Day Pass

Read [live availability](https://listingsapi.com/api/day-pass) and the [Day Pass guide](https://listingsapi.com/docs/day-pass.md) before offering signup. Only offer it while `open` is true. The free pass lasts 24 hours from activation, supports up to 2 locations, and syncs to 10 ListingsAPI demo directories. It never writes to real publishers. Reviews, posts, social, analytics, connected accounts, and webhooks are excluded.

Direct the user to [Day Pass signup](https://listingsapi.com/signup?plan=day-pass&campaign=daypass). It asks for name, email, and company, acceptance of the Terms of Service and Privacy Policy, then activation by emailed link or 6-digit code. The user can sign in through OAuth with **Email me a sign-in link** using the Day Pass email, or configure their Day Pass key locally. Treat signup and activation as a separate user-authorized action, not an implicit part of installing this skill.

Once authenticated, first read the account and locations. If the user requests a sandbox write, verify the connection belongs to the active Day Pass, read the relevant endpoint contract, create or update only the requested sample location, and read its demo listing statuses and URLs back. A Day Pass does not authorize production writes or access to excluded features.

## Production writes

Read the target location and relevant contract first. For a review reply or post, show the proposed text and target before obtaining approval to publish. Connecting publisher accounts and creating or updating locations need a user-authorized task and write access. Reviews, posts, and publisher analytics also depend on the required connected and matched profiles. Read back the result without treating an accepted asynchronous request as a live listing.

For a read-only request, return findings or drafts and keep the operation read-only. Preserve tool approval prompts and follow the service's retry guidance; do not retry a write blindly.
