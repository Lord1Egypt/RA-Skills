# JSON — encoding/json Without the Silent Failures

`encoding/json` fails quietly by design: unknown fields are skipped, unexported fields are invisible, and missing fields leave zero values. Most JSON bugs in Go are not errors — they are zeros nobody noticed.

## Struct Rules

```go
type User struct {
    ID        int64      `json:"id"`
    Name      string     `json:"name"`
    Email     string     `json:"email,omitempty"`
    internal  string     // never encoded, never decoded — unexported
    Password  string     `json:"-"`          // explicitly excluded
    CreatedAt time.Time  `json:"created_at"` // RFC 3339 both ways
}
```

- **Only exported fields participate.** A lowercase field with a perfect tag is silently ignored in both directions — the number-one cause of "unmarshal succeeded but everything is zero".
- Field matching on decode is **case-insensitive** and prefers an exact tag match: `{"NAME": "x"}` fills `Name`. That leniency hides typos in producers.
- `json:"-"` excludes; `json:"-,"` means the field is literally named `-`.
- Unknown fields in the input are discarded without error. To reject them, use a `Decoder` with `DisallowUnknownFields()` — the only way to catch a client sending `emial` instead of `email`.
- Missing fields are indistinguishable from zero values. When "absent" and "zero" differ (PATCH semantics, feature flags), use a pointer (`*bool`) or `json.RawMessage` and check for nil.

## omitempty and Its Limits

`omitempty` omits false, 0, "", nil pointer, nil interface, and empty array/slice/map. It does **not** omit an empty struct, a zero `time.Time`, or a zero-valued nested value — `omitempty` on a `struct` field does nothing at all.

- Serializing a zero `time.Time` produces `"0001-01-01T00:00:00Z"`, which downstream parsers usually reject or store as a real date. Use `*time.Time` with `omitempty`, or a custom marshaler.
- A nil slice encodes as `null`, an empty slice as `[]`. Clients that iterate without a nil check break on `null` — either guarantee `[]T{}` or state `null` in the contract (`collections.md`).
- `omitzero` (`go >=1.24`) omits any field equal to its zero value, including structs and `time.Time`, and honors an `IsZero() bool` method — the fix for the case `omitempty` never covered.

## Numbers

- Decoding into `any` turns **every** number into `float64`. Integers above 2^53 lose precision silently — an int64 ID becomes a different ID with no error.
- Fix: decode into a typed struct, or use `dec := json.NewDecoder(r); dec.UseNumber()` so numbers arrive as `json.Number` (a string) and you choose `Int64()` or `Float64()`.
- Encoding a `float64` NaN or ±Inf returns an `UnsupportedValueError`; JSON has no representation for them. Handle before encoding.
- Large integers are also a *producer* problem: JavaScript clients cannot hold your int64 IDs. Emit them as strings (`json:"id,string"`) when the consumer is a browser.
- `json:",string"` encodes a numeric or bool field as a JSON string and decodes it back — the tag for APIs that quote their numbers.

## Custom Marshaling

```go
func (d Duration) MarshalJSON() ([]byte, error) {
    return json.Marshal(time.Duration(d).String())
}
func (d *Duration) UnmarshalJSON(b []byte) error {   // POINTER receiver
    var s string
    if err := json.Unmarshal(b, &s); err != nil { return err }
    v, err := time.ParseDuration(s)
    *d = Duration(v)
    return err
}
```

- `UnmarshalJSON` must have a **pointer receiver** or it can never write anything; the encoder simply will not call a value-receiver version on an addressable value the way you expect.
- Calling `json.Marshal(x)` on the same type inside its own `MarshalJSON` recurses until the stack overflows. Define `type alias T` (a distinct type with no methods) and marshal that.
- `encoding.TextMarshaler`/`TextUnmarshaler` is honored by `encoding/json` *and* by other encoders and by map keys — implement it instead when the value has a natural string form.
- Embedded structs are **flattened** into the parent object unless the embedded field has a tag; an embedded field with `json:"meta"` becomes a nested object (`structs.md`).

## Streaming and Large Payloads

- `json.Unmarshal` requires the whole document in memory. For a large body or a file, `json.NewDecoder(r).Decode(&v)` streams and avoids the second copy.
- Reading a stream of concatenated or newline-delimited objects: call `Decode` in a loop until `io.EOF`. `Decoder.More()` walks arrays element by element after consuming the opening token.
- `json.Encoder` writes directly to an `io.Writer` and **appends a newline** after each value — the reason handler output sometimes has a trailing byte that byte-for-byte tests do not expect.
- Always bound untrusted input: `http.MaxBytesReader(w, r.Body, 1<<20)` before decoding, or a malicious client streams gigabytes into your heap (`security.md`, `http.md`).
- Marshaling escapes `<`, `>`, and `&` as `\u003c`, `\u003e`, and `\u0026` by default (HTML-safety), so the bytes on the wire are not the bytes you typed. Disable with `enc.SetEscapeHTML(false)` when producing files or signatures that must match byte-for-byte — a golden-file or HMAC comparison fails on exactly those three sequences.

## Deferred and Dynamic Shapes

- `json.RawMessage` defers decoding: keep the bytes, inspect a discriminator field, then unmarshal into the right concrete type. This is how you decode polymorphic payloads without a two-pass parse.
- `map[string]any` is the last resort — it loses types, orders keys alphabetically on re-encode, and pushes every access to a runtime assertion (`interfaces.md`).
- Map keys always encode as strings, sorted. An `int` key becomes `"1"`; a struct key needs `TextMarshaler` or it is an error.

## Errors Worth Recognizing

| Error | Cause |
|---|---|
| `json: cannot unmarshal string into Go struct field X.y of type int` | Type mismatch; the message names the exact path — read it before opening the code |
| `json: Unmarshal(non-pointer main.T)` | Passed the value, not `&v` |
| `unexpected end of JSON input` | Truncated body; often a client timeout or an unread `io.Reader` |
| `invalid character 'x' looking for beginning of value` | Not JSON at all — usually an HTML error page or a proxy response |
| `json: unsupported type: chan int` | A channel, func, or complex number reached the encoder, typically through an `any` field |

Partial decode is real: `Unmarshal` fills what it can before returning an error, so a struct can hold half the payload alongside a non-nil error. Never use the value when the error is non-nil.

## Performance

- `encoding/json` uses reflection; it is fast enough for almost everything and is the default. Replace it only after a profile shows serialization at the top (`performance.md`).
- Cheap wins first: stream instead of buffering, reuse `[]byte` buffers, avoid `map[string]any`, and drop fields nobody reads.
- `GOEXPERIMENT=jsonv2` (`go >=1.25`) exposes an experimental `encoding/json/v2` with different defaults and better performance. Experimental means the API can still change — do not build a public API contract on it yet (`versions.md`).

## Back To SKILL.md

Struct tags and embedding rules: `structs.md`. Request bodies and size limits: `http.md`. Untrusted input handling: `security.md`.
