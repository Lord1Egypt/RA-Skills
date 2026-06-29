package cli

import "fmt"

// Exit codes. Two are part of the external contract (AGENTS.md): export/parse
// failure must be 2, success must be 0. The rest follow the Python tool and
// sysexits convention (generic failure 1, usage 64, config 78).
const (
	ExitOK      = 0
	ExitFailure = 1
	ExitExport  = 2  // export/parse failure — no token, bad ZIP, unreadable export.
	ExitUsage   = 64 // bad flags / bad --date.
	ExitConfig  = 78 // unreadable / invalid config.json.
)

// ExitError carries an explicit process exit code alongside an error. main
// unwraps it with errors.As to choose the exit status, keeping a single exit
// point instead of scattering os.Exit calls through commands.
type ExitError struct {
	Code int
	Err  error
}

func (e *ExitError) Error() string {
	if e.Err == nil {
		return fmt.Sprintf("exit code %d", e.Code)
	}
	return e.Err.Error()
}

func (e *ExitError) Unwrap() error { return e.Err }

// withCode wraps err so main exits with the given code. A nil err yields nil so
// callers can `return withCode(code, doThing())` without a guard.
func withCode(code int, err error) error {
	if err == nil {
		return nil
	}
	return &ExitError{Code: code, Err: err}
}
