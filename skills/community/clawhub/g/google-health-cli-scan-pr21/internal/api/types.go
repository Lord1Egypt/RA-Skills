package api

import "encoding/json"

// DataPoint is one exercise data point. Decoding is intentionally loose: the
// real payload carries many fields we ignore (activeZoneMinutes,
// heartRateZoneDurations, splitSummaries, exerciseEvents, …) and unknown keys
// are skipped, never an error (GOAL.md §9). Raw holds the exact bytes of this
// point so `sessions --raw` can re-emit the API JSON unchanged.
type DataPoint struct {
	Raw        json.RawMessage `json:"-"`
	Exercise   Exercise        `json:"exercise"`
	DataSource *DataSource     `json:"dataSource"` // point-level (real payload).
	Name       string          `json:"name"`
}

// Exercise mirrors the nested "exercise" object. DataSource may also appear here
// in some payload shapes (the offline test fixtures nest it under exercise);
// health.ParseSession prefers this one, then the point-level one (health.py).
type Exercise struct {
	ExerciseType   string         `json:"exerciseType"`
	DisplayName    string         `json:"displayName"`
	ActiveDuration string         `json:"activeDuration"`
	Interval       Interval       `json:"interval"`
	MetricsSummary MetricsSummary `json:"metricsSummary"`
	DataSource     *DataSource    `json:"dataSource"`
}

// Interval is the exercise interval with per-session UTC offsets, so the local
// (civil) date can be reconstructed regardless of where the data was recorded.
type Interval struct {
	StartTime      string `json:"startTime"`
	StartUtcOffset string `json:"startUtcOffset"`
	EndTime        string `json:"endTime"`
	EndUtcOffset   string `json:"endUtcOffset"`
}

// MetricsSummary carries the two metrics we log. They are kept as RawMessage
// because the wire types differ — averageHeartRateBeatsPerMinute arrives as a
// JSON string ("134") and caloriesKcal as a JSON number (122) — and the Python
// _to_num must be replicated exactly to keep int-vs-float fidelity (GOAL.md §11).
type MetricsSummary struct {
	AverageHeartRate json.RawMessage `json:"averageHeartRateBeatsPerMinute"`
	Calories         json.RawMessage `json:"caloriesKcal"`
}

// DataSource carries the recording platform (FITBIT, HEALTH_CONNECT, …).
type DataSource struct {
	Platform string `json:"platform"`
}

// listResponse is the dataPoints.list envelope: the wrapper key is "dataPoints"
// (plural) and pagination uses "nextPageToken" (GOAL.md §9). Points stay raw so
// each can be decoded into a DataPoint while also preserving its exact bytes.
type listResponse struct {
	DataPoints    []json.RawMessage `json:"dataPoints"`
	NextPageToken string            `json:"nextPageToken"`
}

// apiError is Google's error envelope: {"error":{"code","message","status",
// "details":[…]}}. The details array is heterogeneous (ErrorInfo, BadRequest, …);
// we pluck the human-readable BadRequest fieldViolations, which carry the
// actionable text — e.g. the rollup range exceeding a type's max duration.
type apiError struct {
	Error struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
		Status  string `json:"status"`
		Details []struct {
			FieldViolations []struct {
				Field       string `json:"field"`
				Description string `json:"description"`
			} `json:"fieldViolations"`
		} `json:"details"`
	} `json:"error"`
}
