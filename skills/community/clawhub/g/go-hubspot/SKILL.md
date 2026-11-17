---
name: go-hubspot
description: Unofficial Go client for the HubSpot API. `hubspot.NewClientWithResponses("https://api.hubapi.com", ...)` from `github.com/psyb0t/go-hubspot` gives a typed method for every path in HubSpot's 2026-03 OpenAPI documents, including CRM objects such as contacts and companies, single-deal reads and updates, associations, properties, search, marketing, CMS, automation, conversations, files and webhooks. Auth is a Bearer private app or OAuth access token set through a request editor. Responses decode into typed `JSON200`/`JSON201` fields. Use when Go code needs to read or write HubSpot data, or already imports go-hubspot.
license: MIT
homepage: https://github.com/psyb0t/go-hubspot
user-invocable: true
metadata:
  openclaw:
    emoji: "🧲"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you pass, normally https://api.hubapi.com."
---

# go-hubspot

Typed Go client for the HubSpot API, generated with oapi-codegen. The package is `hubspot`; every endpoint is a method on `*hubspot.ClientWithResponses`.

For install details, naming, more operations and the developer API key scheme, see [references/setup.md](references/setup.md).

## Security & safety

- Read the access token from an environment variable such as `HUBSPOT_ACCESS_TOKEN`. Never hardcode it, commit it or log it, and never print request headers.
- The client talks only to the base URL you give it. Use `https://api.hubapi.com`; HubSpot data goes nowhere else.
- Create, update, merge, archive, delete and GDPR purge endpoints change a live HubSpot account. Call them only when the user asked for that change, and only on records the task owns.

## When to use

- Go code needs to read or write HubSpot CRM records, associations, properties, marketing, CMS or other HubSpot API data.
- You want typed request and response structs instead of hand-written HTTP calls.
- The project already imports `github.com/psyb0t/go-hubspot`.

## When NOT to use

- The code is not Go. Use one of HubSpot's own SDKs.
- You need an endpoint outside HubSpot's 2026-03 specs, such as a legacy v1 API. The client has no method for it.
- You only need to receive HubSpot webhooks. The client sends requests; it does not run a webhook server.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-hubspot`, from inside your module:

```bash
go doc github.com/psyb0t/go-hubspot ClientWithResponsesInterface                       # every endpoint method
go doc github.com/psyb0t/go-hubspot Getcrmobjects202603contactsContactIdGetByIdParams  # one method, params type or model
go doc -all github.com/psyb0t/go-hubspot                                               # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-hubspot.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. HubSpot's operation IDs join the HTTP method, the path with its API version date and an action, and each method's doc comment names its path, so filter the interface listing by path, for example `go doc github.com/psyb0t/go-hubspot ClientWithResponsesInterface | grep '/crm/objects/2026-03/companies'`.

## Usage

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-hubspot"
)

auth := hubspot.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("HUBSPOT_ACCESS_TOKEN"))

	return nil
})

client, err := hubspot.NewClientWithResponses("https://api.hubapi.com", auth)
if err != nil {
	return err
}
```

Read one contact (`GET /crm/objects/2026-03/contacts/{contactId}`):

```go
props := []string{"email", "firstname"}

res, err := client.Getcrmobjects202603contactsContactIdGetByIdWithResponse(
	ctx,
	"101",
	&hubspot.Getcrmobjects202603contactsContactIdGetByIdParams{Properties: &props},
)
if err != nil {
	return err // transport or decode failure
}

if res.JSON200 == nil {
	return fmt.Errorf("hubspot: %s: %s", res.Status(), res.Body)
}

fmt.Println(res.JSON200.Id, res.JSON200.Properties["email"])
```

Create a contact (`POST /crm/objects/2026-03/contacts`, answers 201):

```go
res, err := client.Postcrmobjects202603contactsCreateWithResponse(
	ctx,
	hubspot.SimplePublicObjectInputForCreate{
		Associations: []hubspot.PublicAssociationsForObject{},
		Properties:   map[string]string{"email": "user@example.com"},
	},
)
if err != nil {
	return err
}

if res.JSON201 == nil {
	return fmt.Errorf("hubspot: %s: %s", res.Status(), res.Body)
}
```

Search contacts (`POST /crm/objects/2026-03/contacts/search`):

```go
value := "user@example.com"

res, err := client.Postcrmobjects202603contactssearchDoSearchWithResponse(
	ctx,
	hubspot.PublicObjectSearchRequest{
		FilterGroups: []hubspot.FilterGroup{{
			Filters: []hubspot.Filter{{
				PropertyName: "email",
				Operator:     hubspot.FilterOperatorEQ,
				Value:        &value,
			}},
		}},
		Limit:      10,
		Properties: []string{"email"},
		Sorts:      []string{},
	},
)
```

`err` is only set for network, request building or JSON decode failures. A HubSpot error status still returns `err == nil`: check `res.StatusCode()` or that the matching `JSON2xx` field is non-nil, and read `res.Body` for the error payload.
