package health

import (
	"encoding/json"
	"testing"

	"github.com/stozo04/google-health-cli/internal/api"
)

// point builds an api.DataPoint shaped like the offline test fixtures
// (test_offline.py:_point): dataSource nested under exercise, HR as a JSON
// string, calories as a JSON number.
func point(etype, startUTC, endUTC, hr string, kcal int, dur, name string) api.DataPoint {
	return api.DataPoint{
		Exercise: api.Exercise{
			ExerciseType:   etype,
			DisplayName:    name,
			ActiveDuration: dur,
			Interval: api.Interval{
				StartTime: startUTC, StartUtcOffset: "-18000s",
				EndTime: endUTC, EndUtcOffset: "-18000s",
			},
			MetricsSummary: api.MetricsSummary{
				AverageHeartRate: json.RawMessage(`"` + hr + `"`),
				Calories:         json.RawMessage(itoa(kcal)),
			},
			DataSource: &api.DataSource{Platform: "FITBIT"},
		},
		Name: "users/me/dataTypes/exercise/dataPoints/" + name,
	}
}

func itoa(n int) string {
	b, _ := json.Marshal(n)
	return string(b)
}

// 23:00Z - 18000s = 18:00 local on 2026-06-16.
func elliptical() api.DataPoint {
	return point("ELLIPTICAL", "2026-06-16T23:00:00Z", "2026-06-16T23:30:00Z", "122", 245, "1800s", "Elliptical")
}

func TestParsePullsFields(t *testing.T) {
	s := ParseSession(elliptical())
	if s.ExerciseType != "ELLIPTICAL" {
		t.Errorf("ExerciseType = %q", s.ExerciseType)
	}
	if s.DurationMin == nil || *s.DurationMin != 30 {
		t.Errorf("DurationMin = %v, want 30", s.DurationMin)
	}
	if s.AvgHR != 122 {
		t.Errorf("AvgHR = %v (%T), want int 122", s.AvgHR, s.AvgHR)
	}
	if s.Calories != 245 {
		t.Errorf("Calories = %v (%T), want int 245", s.Calories, s.Calories)
	}
	if s.Start == nil || s.Start.Format("2006-01-02") != "2026-06-16" {
		t.Errorf("Start date = %v, want 2026-06-16", s.Start)
	}
	if s.Start.Hour() != 18 {
		t.Errorf("Start hour = %d, want 18 (UTC 23:00 + (-5h))", s.Start.Hour())
	}
	if s.Platform != "FITBIT" {
		t.Errorf("Platform = %q, want FITBIT", s.Platform)
	}
}

func TestDurationFallbackFromInterval(t *testing.T) {
	// No activeDuration: duration is derived from end-start (45 min here).
	p := point("ELLIPTICAL", "2026-06-16T17:00:00Z", "2026-06-16T17:45:00Z", "120", 100, "", "x")
	s := ParseSession(p)
	if s.DurationMin == nil || *s.DurationMin != 45 {
		t.Errorf("DurationMin = %v, want 45 (from interval)", s.DurationMin)
	}
}

func TestToNumEdgeCases(t *testing.T) {
	cases := []struct {
		raw  string
		want any
	}{
		{`"134"`, 134},
		{`122`, 122},
		{`"134.5"`, pyFloat(134.5)},
		{`122.0`, pyFloat(122.0)},
		{`true`, nil},
		{`false`, nil},
		{`null`, nil},
		{`"abc"`, nil},
		{``, nil},
	}
	for _, c := range cases {
		got := toNum(json.RawMessage(c.raw))
		if got != c.want {
			t.Errorf("toNum(%q) = %v (%T), want %v (%T)", c.raw, got, got, c.want, c.want)
		}
	}
}

func TestParseNeverPanicsOnGarbage(t *testing.T) {
	// Missing interval/metrics: all nil, no panic (parse tolerance, GOAL.md §12).
	s := ParseSession(api.DataPoint{})
	if s.Start != nil || s.DurationMin != nil || s.AvgHR != nil || s.Calories != nil {
		t.Errorf("expected all-nil parse for empty point, got %+v", s)
	}
}
