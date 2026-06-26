package ui

import (
	"encoding/json"
	"os"
)

// OutputFormat holds the global output format ("text" or "json").
var OutputFormat string

// IsJSON returns true if JSON output is requested.
func IsJSON() bool {
	return OutputFormat == "json"
}

// PrintJSON encodes data as JSON to stdout.
func PrintJSON(data any) {
	json.NewEncoder(os.Stdout).Encode(data)
}

// PrintOrJSON prints JSON if --output json, otherwise calls the text function.
func PrintOrJSON(data any, textFn func()) {
	if IsJSON() {
		PrintJSON(data)
	} else {
		textFn()
	}
}
