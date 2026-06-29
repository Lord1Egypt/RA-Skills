package api

import (
	"testing"
	"time"
)

func TestRangeFilter(t *testing.T) {
	from := time.Date(2026, 6, 14, 0, 0, 0, 0, time.UTC)
	to := time.Date(2026, 6, 18, 0, 0, 0, 0, time.UTC)

	cases := []struct {
		typeName string
		want     string
	}{
		{
			// Session/civil: bare wall-clock, no trailing Z.
			"exercise",
			`exercise.interval.civil_start_time >= "2026-06-14T00:00:00" AND exercise.interval.civil_start_time < "2026-06-18T00:00:00"`,
		},
		{
			// Sample/physical: absolute RFC3339 instant.
			"heart-rate",
			`heart_rate.sample_time.physical_time >= "2026-06-14T00:00:00Z" AND heart_rate.sample_time.physical_time < "2026-06-18T00:00:00Z"`,
		},
		{
			// Daily/date: date-only, no time component.
			"daily-resting-heart-rate",
			`daily_resting_heart_rate.date >= "2026-06-14" AND daily_resting_heart_rate.date < "2026-06-18"`,
		},
		{
			// Sleep filters on civil_end_time (start time is not a valid member).
			"sleep",
			`sleep.interval.civil_end_time >= "2026-06-14T00:00:00" AND sleep.interval.civil_end_time < "2026-06-18T00:00:00"`,
		},
	}
	for _, c := range cases {
		dt, ok := LookupDataType(c.typeName)
		if !ok {
			t.Fatalf("LookupDataType(%q) not found", c.typeName)
		}
		if got := dt.RangeFilter(from, to); got != c.want {
			t.Errorf("RangeFilter(%s):\n got: %s\nwant: %s", c.typeName, got, c.want)
		}
	}
}

func TestCivilHasNoZone(t *testing.T) {
	// The endpoint rejects a trailing Z / offset; Civil must emit bare wall-clock.
	tm := time.Date(2026, 6, 16, 20, 33, 51, 0, time.FixedZone("CST", -5*3600))
	if got := Civil(tm); got != "2026-06-16T20:33:51" {
		t.Errorf("Civil = %q, want 2026-06-16T20:33:51 (no zone)", got)
	}
}
