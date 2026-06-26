# Go HTTP Static Server

## goware/webify

```bash
go run github.com/goware/webify@latest -port 8000 .
```

Or install first:

```bash
go install github.com/goware/webify@latest
webify -port 8000 .
```

Features:
- Directory listing: Yes
- Single binary, fast
- Requires Go installed

## Inline Go (no dependencies)

```bash
go run -e 'package main; import "net/http"; func main() { http.ListenAndServe(":8000", http.FileServer(http.Dir("."))) }'
```

Or create a file `server.go`:

```go
package main

import "net/http"

func main() {
    http.ListenAndServe(":8000", http.FileServer(http.Dir(".")))
}
```

Then:

```bash
go run server.go
```

Features:
- Directory listing: Yes
- Zero dependencies
- Production-grade performance
- Bind to all interfaces by default (`:8000`)
