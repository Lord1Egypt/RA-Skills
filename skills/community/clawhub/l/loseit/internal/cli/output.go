package cli

import (
	"encoding/json"
	"io"
)

// writeJSON emits v as machine-readable JSON matching Python's
// json.dumps(indent=2): two-space indent, a trailing newline, and — crucially —
// HTML escaping OFF so characters like &, <, > survive byte-for-byte. Agents
// parse our stdout, so `--json` output must match the Python tool exactly.
//
// Callers pass cmd.OutOrStdout() so tests can capture output.
func writeJSON(w io.Writer, v any) error {
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	return enc.Encode(v) // Encode already appends the trailing newline.
}
