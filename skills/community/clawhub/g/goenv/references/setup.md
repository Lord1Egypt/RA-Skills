# goenv setup and reference

## Requirements

- Go **1.26** or newer (per the module's `go.mod`).
- Nothing else. goenv's only import is the standard library `os`; it pulls in zero third-party dependencies.

## Install

```bash
go get github.com/psyb0t/goenv
```

Then import it in your Go code:

```go
import "github.com/psyb0t/goenv"
```

Module path: `github.com/psyb0t/goenv`.

## The entire API

Three functions, three constants, and one type. That's the whole surface.

| Symbol | Kind | Behavior |
|---|---|---|
| `goenv.Get() goenv.Type` | func | Returns the current environment: `Dev` if `ENV == "dev"` exactly, otherwise `Prod`. |
| `goenv.IsProd() bool` | func | `Get() == Prod`. True unless `ENV` is exactly `"dev"`. |
| `goenv.IsDev() bool` | func | `Get() == Dev`. True only when `ENV` is exactly `"dev"`. |
| `goenv.Prod` | const | The string `"prod"`. |
| `goenv.Dev` | const | The string `"dev"`. |
| `goenv.EnvVarName` | const | The string `"ENV"`, the variable it reads. |
| `goenv.Type` | type | A **string alias** (`type Type = string`). `goenv.Type` is interchangeable with `string`; the constants above are typed as `Type` but provide no compile-time enum enforcement. |

## Behavior table

`Get()` does a single exact-match `switch` on `os.Getenv("ENV")`:

| `ENV` value | `Get()` | `IsProd()` | `IsDev()` |
|---|---|---|---|
| `dev` | `dev` | false | true |
| `prod` | `prod` | true | false |
| (unset) | `prod` | true | false |
| empty string | `prod` | true | false |
| `DEV` / `Dev` | `prod` | true | false |
| `development` | `prod` | true | false |
| anything else | `prod` | true | false |

The match is **case-sensitive and exact**: only the literal lowercase `"dev"` counts as dev. Everything else (including the string `"prod"` itself, and any typo) resolves to `Prod`. This is deliberate: an unknown or misconfigured environment fails safe toward production behavior.

Each call re-reads the environment (`os.Getenv`), so if something in your process mutates `ENV` at runtime, subsequent `Get()`/`IsProd()`/`IsDev()` calls reflect the new value. In practice set `ENV` once before launch and leave it.

## Worked example

```go
package main

import (
	"fmt"

	"github.com/psyb0t/goenv"
)

func main() {
	fmt.Printf("environment: %s\n", goenv.Get())

	if goenv.IsDev() {
		fmt.Println("dev mode: verbose logging, hot reload, relaxed timeouts")
		return
	}

	// goenv.IsProd(): the default path
	fmt.Println("prod mode: structured logs, strict timeouts")
}
```

```bash
ENV=dev go run .    # → environment: dev  → dev mode ...
go run .            # → environment: prod → prod mode ...  (ENV unset)
```

## Notes / limitations

- **Two environments only.** There is no `staging`/`test`/`ci`; anything that isn't exactly `"dev"` is treated as `prod`. If you need more, this library can't express it; use a fuller config package.
- **Fixed variable name.** It always reads `ENV`; the name isn't configurable (it's exported as `goenv.EnvVarName` for reference, not for override).
- **No type safety.** Because `Type` is a `string` alias, the compiler won't stop you assigning an arbitrary string where a `goenv.Type` is expected. Treat `Prod`/`Dev` as convenient constants, not a closed enum.
