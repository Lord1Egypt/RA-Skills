package cli

import (
	"encoding/json"
	"io"
)

// writeJSON emits v as machine-readable JSON matching Python's
// json.dumps(indent=2): two-space indent, a trailing newline, and — crucially —
// HTML escaping OFF so characters like &, <, > survive byte-for-byte. The Python
// tool never escapes these (the zone2 label carries "<110"/">130"), and agents
// parse our stdout, so the `--json` output must match exactly (GOAL.md §2, §13).
//
// Callers pass cmd.OutOrStdout() so tests can capture output (GOAL.md §13).
func writeJSON(w io.Writer, v any) error {
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	return enc.Encode(v) // Encode already appends the trailing newline.
}
