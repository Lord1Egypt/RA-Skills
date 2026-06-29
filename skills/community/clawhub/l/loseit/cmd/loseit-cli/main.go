// Command loseit-cli is a self-contained, read-only nutrition extractor for the
// Lose It! data export. It obtains the export ZIP (a downloaded file or a cookie
// fetch), parses the food log, and emits per-day nutrition as JSON. It does no
// application writing — no DAILY_LOG, no sync, no upsert; the consuming agent
// does the storing. The only file it writes locally is its own session-token
// cache (token_path, mode 0600). No Python runtime, no external helper binary.
//
// This entrypoint is deliberately thin: it owns the ldflags version vars (the
// linker's -X only reaches package main), wires a cancelable context for Ctrl-C,
// runs the cobra tree, and maps the resulting error to a single process exit code.
package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/signal"

	"github.com/stozo04/loseit-cli/internal/cli"
	"github.com/stozo04/loseit-cli/internal/version"
)

// Set by GoReleaser via -ldflags "-X main.versionString=... -X main.commit=...
// -X main.date=...". See .goreleaser.yaml. Forwarded into the version package
// below. The var is versionString (not version) because package main imports the
// version package.
var (
	versionString = ""
	commit        = ""
	date          = ""
)

func main() {
	os.Exit(run())
}

// run executes the program and returns a process exit code. Keeping the only
// os.Exit in main() guarantees deferred cleanup in commands still runs.
func run() int {
	version.Set(versionString, commit, date)

	// Cancel the context on the first interrupt so an in-flight export fetch can
	// abort cleanly; a second interrupt restores default behavior (hard kill).
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	root := cli.NewRootCmd()
	err := root.ExecuteContext(ctx)
	if err == nil {
		return cli.ExitOK
	}

	// One error line to stderr; stdout stays clean (stdout is data). A command
	// that already produced its own output returns a message-less error, so skip
	// the line when there's nothing to say.
	if msg := err.Error(); msg != "" {
		fmt.Fprintln(os.Stderr, "loseit-cli: "+msg)
	}

	var exit *cli.ExitError
	if errors.As(err, &exit) {
		return exit.Code
	}
	return cli.ExitFailure
}
