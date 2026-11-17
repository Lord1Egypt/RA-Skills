// Package health ports the field extraction and allowlist filter from the Python
// google_health/health.py. It turns a raw exercise data point into the fields we
// log, never raising on a malformed point (a bad point yields nils rather than
// aborting a sync — GOAL.md §12).
package health

import (
	"encoding/json"
	"math"
	"strconv"
	"strings"
	"time"

	"github.com/stozo04/google-health-cli/internal/api"
)

// Session is the normalized form of one exercise data point. AvgHR and Calories
// hold the result of toNum: an int, a pyFloat, or nil — preserving Python's
// int-vs-float distinction for byte-faithful JSON (GOAL.md §11).
type Session struct {
	ExerciseType string
	DisplayName  string
	Start        *time.Time // naive local (civil); nil if unparseable.
	End          *time.Time
	DurationMin  *int
	AvgHR        any
	Calories     any
	Platform     string
	PointID      string
}

// ParseSession normalizes one raw exercise data point. It mirrors
// health.py:parse_session exactly and never panics.
func ParseSession(p api.DataPoint) Session {
	ex := p.Exercise
	start := localDT(ex.Interval, "start")
	end := localDT(ex.Interval, "end")

	secs := durationSecs(ex.ActiveDuration)
	if secs == nil && start != nil && end != nil && end.After(*start) {
		s := end.Sub(*start).Seconds()
		secs = &s
	}
	var durationMin *int
	if secs != nil && *secs != 0 {
		m := int(math.RoundToEven(*secs / 60))
		durationMin = &m
	}

	platform := ""
	switch {
	case ex.DataSource != nil:
		platform = ex.DataSource.Platform
	case p.DataSource != nil:
		platform = p.DataSource.Platform
	}

	return Session{
		ExerciseType: ex.ExerciseType,
		DisplayName:  ex.DisplayName,
		Start:        start,
		End:          end,
		DurationMin:  durationMin,
		AvgHR:        toNum(ex.MetricsSummary.AverageHeartRate),
		Calories:     toNum(ex.MetricsSummary.Calories),
		Platform:     platform,
		PointID:      p.Name,
	}
}

// localDT reconstructs the naive local (civil) wall-clock for interval
// start/end: the UTC instant shifted by its own per-session UTC offset. Using
// the per-session offset means dates bucket correctly regardless of DST or where
// the data was recorded (health.py:_local_dt). nil when the time can't be parsed.
func localDT(iv api.Interval, which string) *time.Time {
	timeStr, offStr := iv.StartTime, iv.StartUtcOffset
	if which == "end" {
		timeStr, offStr = iv.EndTime, iv.EndUtcOffset
	}
	utc := parseUTC(timeStr)
	if utc == nil {
		return nil
	}
	local := utc.Add(time.Duration(offsetSeconds(offStr)) * time.Second).UTC()
	return &local
}

// parseUTC parses an RFC3339 instant (with or without fractional seconds),
// returning nil on failure (health.py:_parse_utc). The result is in UTC.
func parseUTC(s string) *time.Time {
	if s == "" {
		return nil
	}
	t, err := time.Parse(time.RFC3339, s)
	if err != nil {
		return nil
	}
	t = t.UTC()
	return &t
}

// offsetSeconds parses "-18000s" -> -18000, defaulting to 0 (health.py:_offset_seconds).
func offsetSeconds(s string) int {
	if s == "" {
		return 0
	}
	n, err := strconv.Atoi(strings.TrimSuffix(s, "s"))
	if err != nil {
		return 0
	}
	return n
}

// durationSecs parses "1270s" -> 1270 (truncating like Python int(float(...))),
// returning nil on failure or empty (health.py:_duration_secs).
func durationSecs(s string) *float64 {
	if s == "" {
		return nil
	}
	f, err := strconv.ParseFloat(strings.TrimSuffix(s, "s"), 64)
	if err != nil {
		return nil
	}
	v := math.Trunc(f) // int(float(...)) truncates toward zero.
	return &v
}

// toNum replicates health.py:_to_num against a raw JSON value (GOAL.md §11):
//
//   - bool                -> nil
//   - JSON string "134"   -> int 134 (float if it contains a '.', else int;
//     unparseable -> nil)
//   - JSON number 122     -> int 122 (pyFloat if it has '.'/'e'; passthrough)
//   - null / absent       -> nil
func toNum(raw json.RawMessage) any {
	s := strings.TrimSpace(string(raw))
	if s == "" || s == "null" {
		return nil
	}
	if s == "true" || s == "false" {
		return nil
	}
	if s[0] == '"' {
		var str string
		if err := json.Unmarshal(raw, &str); err != nil {
			return nil
		}
		return strToNum(str)
	}
	return numericTokenToNum(s)
}

// strToNum applies Python's str branch: float(v) if "." in v else int(v).
func strToNum(str string) any {
	if strings.Contains(str, ".") {
		f, err := strconv.ParseFloat(str, 64)
		if err != nil {
			return nil
		}
		return pyFloat(f)
	}
	i, err := strconv.ParseInt(str, 10, 64)
	if err != nil {
		return nil
	}
	return int(i)
}

// numericTokenToNum passes a JSON number through, keeping int as int and float
// as a pyFloat so Python's "122" vs "122.0" rendering is preserved.
func numericTokenToNum(s string) any {
	if strings.ContainsAny(s, ".eE") {
		f, err := strconv.ParseFloat(s, 64)
		if err != nil {
			return nil
		}
		return pyFloat(f)
	}
	i, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		f, ferr := strconv.ParseFloat(s, 64)
		if ferr != nil {
			return nil
		}
		return pyFloat(f)
	}
	return int(i)
}
