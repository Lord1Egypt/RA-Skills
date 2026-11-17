// Package api is the Google Health API client: the single place that owns the
// dataPoints.list request URL, query params, filter syntax, and response decode.
// It speaks the v4 REST wire directly (no external helper binary) and covers
// every Google Health data type generically via the embedded [DataType] catalog.
package api

import "time"

// civilLayout formats a naive local (civil) wall-clock time with NO trailing Z
// and NO offset. Civil time paths (e.g. exercise.interval.civil_start_time)
// reject a zoned value with INVALID_DATA_POINT_FILTER_CIVIL_DATE_TIME_FORMAT.
const civilLayout = "2006-01-02T15:04:05"

// dateLayout formats a date-only value for daily ".date" filter fields, which
// reject a full date-time.
const dateLayout = "2006-01-02"

// Civil renders t as a civil date-time string. Only the wall-clock fields are
// used, so the time.Time's location is irrelevant to the output.
//
// The per-type [DataType.RangeFilter] builds the full dataPoints.list filter;
// this helper exists for callers (and tests) that need the bare civil format.
func Civil(t time.Time) string {
	return t.Format(civilLayout)
}
