# go-asyncapi: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependencies: `github.com/psyb0t/ctxerrors` and `gopkg.in/yaml.v3`.

## Install

```bash
go get github.com/psyb0t/go-asyncapi
```

The package name is `asyncapi`. The module path ends in `go-asyncapi`, so import it with an explicit name:

```go
import asyncapi "github.com/psyb0t/go-asyncapi"
```

## Loading

`asyncapi.Load(path string) (*asyncapi.Document, error)` reads the document at `path`, YAML or JSON, and every local file it references.

- Only AsyncAPI 3.x loads. A 2.x document fails.
- `$ref`s are followed inside the file and into relative files. Chains are followed up to 64 hops; a cycle fails.
- Message and operation `traits` are merged in list order. A trait fills properties the message or operation leaves out and never overrides one it sets, nested objects included.
- Every list comes back in the order the document writes it.
- A message used by several channels or operations is one `*Message`, so pointers compare.

## Types

| Type | Fields and methods |
|---|---|
| `Document` | `AsyncAPIVersion`, `Title`, `Version`, `Description`, `DefaultContentType`, `Servers`, `Channels`, `Operations`, `Messages` (every distinct message), `ComponentSchemas` (`components.schemas` in order), `Resolver`, `Root` |
| `Server` | `Name`, `Host`, `Pathname`, `Protocol`, `ProtocolVersion`, `Description`, `Variables`; `URL()` with variables at their defaults, `URLTemplate()` with `{placeholders}` |
| `ServerVariable` | `Name`, `Default`, `Enum`, `Description` |
| `Channel` | `Name`, `Address` (empty for a null address), `Description`, `Parameters`, `Messages`, `Location` |
| `Parameter` | `Name`, `Description`, `Enum`, `Default` |
| `Operation` | `Name`, `Action` (`ActionSend` or `ActionReceive`), `Summary`, `Description`, `Channel`, `Messages`, `Reply` |
| `Reply` | `Channel`, `Messages`, `AddressLocation` (runtime expression of a dynamic reply address) |
| `Message` | `Key`, `Name`, `Title`, `Summary`, `Description`, `ContentType`, `Deprecated`, `Payload`, `PayloadAt`, `UnsupportedFormat`, `Headers`, `HeadersAt`, `CorrelationIDLocation`, `Bindings`, `Location` |
| `SchemaComponent` | `Name`, `Value`, `At` |
| `Object` | `Keys` (document order), `Values`; `Get(key)`, `String(key)`, `Object(key)` |
| `Location` | `File`, `Pointer`; `Child(key)`, `LastToken()`, `String()` |
| `Resolver` | `NewResolver()`, `Document(path)`, `Lookup(location)`, `Deref(value, location)` |

Field notes:

- `Message.Key` is the `components.messages` key, or `<channel>_<key>` for a message defined inline in a channel.
- `Message.ContentType` falls back to the document's `defaultContentType`.
- `Message.Payload` is nil when the message has no payload, or when its `schemaFormat` is not AsyncAPI, JSON Schema or OpenAPI. `UnsupportedFormat` then names the format, for example an Avro schema format.
- `Object` values are `string`, `int64`, `float64`, `bool`, `nil`, `[]any` or `*Object`. A JSON Schema can also be a bare `true` or `false`.

## Following `$ref`s inside schemas

`Load` resolves the document's structure. Schemas stay raw, so walk them with the resolver:

1. Start from a value and its location: `message.Payload` with `message.PayloadAt`, or `component.Value` with `component.At`.
2. `document.Resolver.Deref(value, location)` follows any `$ref` chain and returns the target value and the target's own `Location`.
3. For a nested value, build its location from the returned one with `Child`, for example `at.Child("properties").Child("name")`, then `Deref` again.

Two `$ref`s that resolve to the same `Location` point at the same schema, so `Location` works as a map key to visit each schema once.

## Errors

Errors wrap `github.com/psyb0t/ctxerrors/commerr` sentinels and carry file and line context:

| Sentinel | When |
|---|---|
| `commerr.ErrNotFound` | A `$ref` or JSON pointer points at nothing, or an operation's channel is not an entry under `channels`. |
| `commerr.ErrInvalidValue` | Not AsyncAPI 3, a section that should be a mapping is not, an unknown operation action, a `$ref` cycle. |
| `commerr.ErrInvalidArgument` | A `$ref` to a remote URL. |
| `commerr.ErrRequiredFieldNotSet` | An operation without a `channel`. |
| `commerr.ErrParseFailed` | The file is not valid YAML or JSON, or its top level is not a mapping. |
| `os.ErrNotExist` | The spec file or a referenced file is missing. |

```go
_, err := asyncapi.Load("asyncapi.yaml")
if errors.Is(err, commerr.ErrNotFound) {
	// a dangling $ref
}
```
