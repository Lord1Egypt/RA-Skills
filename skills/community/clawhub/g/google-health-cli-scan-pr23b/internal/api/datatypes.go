package api

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"sort"
	"strings"
	"time"
)

// dataTypesJSON is the embedded catalog of every Google Health data type. It is
// transcribed from the upstream "Google Health data types" table and carries no
// runtime dependency on any external tool. Regenerate by hand if Google adds a
// type.
//
// One deliberate deviation: each defaultTimePath is the member the live v4 API
// actually accepts in a list filter, which is not always the documented default.
// Sleep, for instance, rejects interval.civil_start_time and only filters on
// interval.civil_end_time — so that is what the catalog records here.
//
//go:embed datatypes.json
var dataTypesJSON []byte

// DataType describes one Google Health data type: how to address its dataPoints
// endpoint, which OAuth scope guards it, what record shape it uses, and the
// field its time filter is built on.
type DataType struct {
	// Name is the human label, e.g. "Daily Resting Heart Rate".
	Name string `json:"name"`
	// EndpointName is the URL path segment, e.g. "daily-resting-heart-rate".
	EndpointName string `json:"endpointName"`
	// FilterName is the snake_case field root, e.g. "daily_resting_heart_rate".
	FilterName string `json:"filterName"`
	// RecordType is one of Session, Interval, Sample, Daily.
	RecordType string `json:"recordType"`
	// Operations are the read-only operations this tool exposes for the type, a
	// subset of readOnlyOps (list, get, reconcile, rollup, dailyRollUp). The
	// upstream API also defines mutating operations (create, update, batchDelete)
	// for some types; those are deliberately omitted because this client is
	// read-only and never calls them. init enforces that no write op leaks in.
	Operations []string `json:"operations"`
	// Scope is the short scope group, e.g. "activity_and_fitness".
	Scope string `json:"scope"`
	// DefaultTimePath is the field a time-range filter is built on, e.g.
	// "heart_rate.sample_time.physical_time".
	DefaultTimePath string `json:"defaultTimePath"`
}

var (
	dataTypes          []DataType
	dataTypeByEndpoint map[string]DataType
)

// readOnlyOps is the closed set of operations this read-only client may
// advertise. Each is a GET-shaped read or a read-only POST aggregation; none
// mutates Google Health data. The embedded catalog is validated against this set
// at init, so a write op (create/update/batchDelete/…) can never slip into the
// metadata and contradict the tool's read-only contract.
var readOnlyOps = map[string]bool{
	"list":        true,
	"get":         true,
	"reconcile":   true,
	"rollup":      true,
	"dailyRollUp": true,
}

func init() {
	if err := json.Unmarshal(dataTypesJSON, &dataTypes); err != nil {
		panic("api: bad embedded datatypes.json: " + err.Error())
	}
	dataTypeByEndpoint = make(map[string]DataType, len(dataTypes))
	for _, dt := range dataTypes {
		// Guard the read-only invariant: the catalog must never advertise a
		// mutating operation. This is a hard fail at startup, not a silent one.
		for _, op := range dt.Operations {
			if !readOnlyOps[op] {
				panic(fmt.Sprintf(
					"api: data type %q advertises non-read-only operation %q; this client is read-only",
					dt.EndpointName, op,
				))
			}
		}
		dataTypeByEndpoint[dt.EndpointName] = dt
	}
}

// DataTypes returns the full catalog, sorted by endpoint name. The slice is a
// copy, so callers may not mutate the package state.
func DataTypes() []DataType {
	out := make([]DataType, len(dataTypes))
	copy(out, dataTypes)
	sort.Slice(out, func(i, j int) bool { return out[i].EndpointName < out[j].EndpointName })
	return out
}

// LookupDataType resolves a data type by a user-supplied name. It accepts the
// canonical endpoint name ("heart-rate"), the snake_case filter name
// ("heart_rate"), or any case/separator mix of either ("Heart Rate"), so an
// agent can pass whatever it has on hand.
func LookupDataType(name string) (DataType, bool) {
	if dt, ok := dataTypeByEndpoint[name]; ok {
		return dt, true
	}
	norm := normalizeTypeName(name)
	for _, dt := range dataTypes {
		if normalizeTypeName(dt.EndpointName) == norm || normalizeTypeName(dt.FilterName) == norm {
			return dt, true
		}
	}
	return DataType{}, false
}

// normalizeTypeName lowercases and collapses spaces/underscores to hyphens so the
// endpoint, filter, and display forms of a type all compare equal.
func normalizeTypeName(s string) string {
	s = strings.ToLower(strings.TrimSpace(s))
	s = strings.NewReplacer("_", "-", " ", "-").Replace(s)
	return s
}

// Supports reports whether the type allows the given API operation (e.g. "list").
func (dt DataType) Supports(op string) bool {
	for _, o := range dt.Operations {
		if o == op {
			return true
		}
	}
	return false
}

// ReadScope returns the full OAuth read-only scope URL guarding this type, e.g.
// https://www.googleapis.com/auth/googlehealth.activity_and_fitness.readonly.
func (dt DataType) ReadScope() string {
	return "https://www.googleapis.com/auth/googlehealth." + dt.Scope + ".readonly"
}

// RangeFilter builds the dataPoints.list filter for a [from, to) window on this
// type's default time path: ">= lower AND < upper", with the bound format chosen
// by the path. The three formats below were each verified against the live v4
// API; the wrong format is rejected with INVALID_DATA_POINT_FILTER_*.
func (dt DataType) RangeFilter(from, to time.Time) string {
	p := dt.DefaultTimePath
	return fmt.Sprintf("%s >= %q AND %s < %q", p, formatTimeBound(p, from), p, formatTimeBound(p, to))
}

// formatTimeBound renders a window bound for a filter field:
//   - *.civil_* fields take a bare wall-clock (a zoned value is rejected with
//     INVALID_DATA_POINT_FILTER_CIVIL_DATE_TIME_FORMAT);
//   - *.date fields (daily records) take a date-only YYYY-MM-DD (an instant is
//     likewise rejected as a bad civil date-time);
//   - everything else (sample physical_time) takes a UTC RFC3339 instant.
func formatTimeBound(path string, t time.Time) string {
	switch {
	case strings.Contains(path, ".civil_"):
		return t.Format(civilLayout)
	case strings.HasSuffix(path, ".date"):
		return t.Format(dateLayout)
	default:
		return t.UTC().Format(time.RFC3339)
	}
}
