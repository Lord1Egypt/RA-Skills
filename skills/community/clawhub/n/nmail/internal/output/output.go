package output

import (
	"encoding/json"
	"fmt"
	"os"
)

// JSON prints v as indented JSON to stdout.
func JSON(v any) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(v); err != nil {
		fmt.Fprintf(os.Stderr, "error encoding JSON: %v\n", err)
		os.Exit(1)
	}
}

// Error prints an error as JSON to stdout (agent-friendly).
func Error(msg string) {
	JSON(map[string]string{"error": msg})
}

// Pretty prints a human-readable string.
func Pretty(format string, args ...any) {
	fmt.Printf(format+"\n", args...)
}
