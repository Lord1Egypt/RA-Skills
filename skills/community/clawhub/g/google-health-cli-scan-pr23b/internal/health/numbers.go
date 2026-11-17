package health

import "strconv"

// NumFloat returns the numeric value of a toNum result (int | pyFloat | nil) and
// whether it is present (non-nil). Used for the duration-weighted HR and calorie
// merge math (GOAL.md §11).
func NumFloat(v any) (float64, bool) {
	switch x := v.(type) {
	case int:
		return float64(x), true
	case pyFloat:
		return float64(x), true
	default:
		return 0, false
	}
}

// Truthy reports Python truthiness of a toNum result: present and non-zero. This
// is the `s.get("avg_hr")` / `s.get("duration_min")` guard in merge_sessions.
func Truthy(v any) bool {
	f, ok := NumFloat(v)
	return ok && f != 0
}

// Render formats a toNum result the way Python's str()/f-string would: an int
// with no decimal point, a float with CPython's repr, and "" for nil. Used by
// the human `sessions` output (cli.py:cmd_sessions).
func Render(v any) string {
	switch x := v.(type) {
	case int:
		return strconv.Itoa(x)
	case pyFloat:
		return pyFloatRepr(float64(x))
	default:
		return ""
	}
}
