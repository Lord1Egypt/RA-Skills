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

// wantedDates ports _wanted_dates: the set of ISO dates covering `days` calendar
// days ending on target (target, target-1, …, target-(days-1)).
func wantedDates(target time.Time, days int) map[string]bool {
	want := make(map[string]bool, days)
	for i := 0; i < days; i++ {
		want[target.AddDate(0, 0, -i).Format("2006-01-02")] = true
	}
	return want
}
