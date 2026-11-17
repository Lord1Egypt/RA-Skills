---
name: go-asyncapi
description: Go library that loads AsyncAPI 3 documents. `asyncapi.Load(path)` from `github.com/psyb0t/go-asyncapi` reads a YAML or JSON spec plus every file it references and returns a `*asyncapi.Document` with servers (URL and variables), channels (address, parameters, messages), operations (send/receive action, channel, messages, reply) and messages (payload, headers, correlationId, content type, bindings) in document order, with every `$ref` followed and message and operation traits merged. Payload and header schemas stay as ordered `*asyncapi.Object` trees, and `Document.Resolver.Deref` follows the `$ref`s inside them. Errors wrap `ctxerrors/commerr` sentinels. Use when Go code needs to read, inspect, validate or generate from an AsyncAPI 3 spec, or is already importing go-asyncapi.
homepage: https://github.com/psyb0t/go-asyncapi
user-invocable: true
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads the spec file you pass to Load and the files that spec references by relative $ref; it writes nothing."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. The library makes no network calls; a $ref to a remote URL is rejected."
---

# go-asyncapi

Loads AsyncAPI 3 documents in Go. One call, `asyncapi.Load(path)`, gives you the servers, channels, operations and messages of a spec as plain structs, with `$ref`s already followed and traits merged.

For install, the full type reference and schema walking, see [references/setup.md](references/setup.md).

## Security & safety

- The library only reads files: the spec you pass to `Load` and the local files it references through relative `$ref`s. It writes nothing and opens no network connection. A `$ref` to an `http(s)://` URL fails with `commerr.ErrInvalidArgument` instead of being fetched.
- It compiles into your own binary and has no runtime surface of its own.

## When to use

- Go code needs the contents of an AsyncAPI 3 spec: list channels and their messages, read server URLs, find which messages an operation sends or receives.
- You are writing a generator, linter, doc tool or test helper on top of AsyncAPI 3 and want `$ref` resolution and trait merging done for you.
- The project already imports `github.com/psyb0t/go-asyncapi`.

## When NOT to use

- The spec is AsyncAPI 2.x. `Load` rejects it with `commerr.ErrInvalidValue`; only 3.x documents load.
- You want generated types and a client rather than a parsed document. Use [gen-asyncapi](https://github.com/psyb0t/gen-asyncapi), which is built on this library.
- You need full JSON Schema validation of payloads. go-asyncapi hands schemas back as `*asyncapi.Object` trees and does not validate messages against them.

## Usage

```go
import (
	"fmt"

	asyncapi "github.com/psyb0t/go-asyncapi"
)

document, err := asyncapi.Load("asyncapi.yaml")
if err != nil {
	return err // errors.Is(err, commerr.ErrNotFound) for a dangling $ref
}

for _, server := range document.Servers {
	fmt.Println(server.Name, server.URL()) // variables filled with their defaults
}

for _, operation := range document.Operations {
	if operation.Action != asyncapi.ActionReceive {
		continue
	}

	for _, message := range operation.Messages {
		fmt.Println(operation.Channel.Address, message.Name, message.ContentType)
	}
}
```

Walking a payload schema:

```go
message := document.Messages[0]

schema, at, err := document.Resolver.Deref(message.Payload, message.PayloadAt)
if err != nil {
	return err
}

object, ok := schema.(*asyncapi.Object)
if !ok {
	return nil // a boolean schema such as `payload: true`
}

properties := object.Object("properties")
if properties == nil {
	return nil // not an object schema: oneOf, allOf, a primitive and so on
}

for _, name := range properties.Keys {
	property, propertyAt, err := document.Resolver.Deref(
		properties.Values[name],
		at.Child("properties").Child(name),
	)
	if err != nil {
		return err
	}

	_ = property   // *asyncapi.Object, or a bool schema
	_ = propertyAt // pass on to resolve $refs nested deeper
}
```

Always carry the `Location` that `Deref` returns and build child locations with `Child`. A `$ref` inside a schema resolves against the file that schema came from, and the location is how the resolver knows which file that is.
