package cli

import (
	"fmt"
	"time"
)

// resolveDate ports cli.py:_resolve_date — "today" | "yesterday" | YYYY-MM-DD,
// using the local calendar date. The returned time is a civil midnight (the
// location is irrelevant; only the Y/M/D components are ever used).
func resolveDate(s string) (time.Time, error) {
	switch s {
	case "", "today":
		return civilToday(), nil
	case "yesterday":
		return civilToday().AddDate(0, 0, -1), nil
	}
	t, err := time.ParseInLocation("2006-01-02", s, time.UTC)
	if err != nil {
		return time.Time{}, fmt.Errorf("invalid --date %q (want today|yesterday|YYYY-MM-DD)", s)
	}
	return t, nil
}

// civilToday is the local calendar date at midnight, represented in UTC so its
// wall-clock components match the user's "today".
func civilToday() time.Time {
	n := time.Now()
	return time.Date(n.Year(), n.Month(), n.Day(), 0, 0, 0, 0, time.UTC)
}

// window is the [start, end) civil window covering `days` calendar days ending
// on target: start = midnight(target-(days-1)), end = midnight(target+1).
func window(target time.Time, days int) (start, end time.Time) {
	start = target.AddDate(0, 0, -(days - 1))
	end = target.AddDate(0, 0, 1)
	return start, end
}
