package api

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// civilDate is google.type.Date: a whole calendar date with no zone.
type civilDate struct {
	Year  int `json:"year"`
	Month int `json:"month"`
	Day   int `json:"day"`
}

// civilTimeOfDay is google.type.TimeOfDay (zone-free). Fields are omitempty so a
// midnight bound serializes compactly.
type civilTimeOfDay struct {
	Hours   int `json:"hours,omitempty"`
	Minutes int `json:"minutes,omitempty"`
	Seconds int `json:"seconds,omitempty"`
}

// civilDateTime mirrors the API's CivilDateTime, which deliberately cannot carry
// a timezone or UTC offset: the rollup buckets on the civil (local) calendar day,
// exactly the wall-clock semantics `data list` uses for civil types. time is
// omitted when the bound falls on midnight (the API defaults it to start-of-day).
type civilDateTime struct {
	Date civilDate       `json:"date"`
	Time *civilTimeOfDay `json:"time,omitempty"`
}

// civilTimeInterval is the closed-open [start, end) range the rollup aggregates.
type civilTimeInterval struct {
	Start civilDateTime `json:"start"`
	End   civilDateTime `json:"end"`
}

// dailyRollUpRequest is the DailyRollUpDataPointsRequest body. windowSizeDays is
// fixed at 1 (daily). pageSize is deliberately omitted: the API caps the query at
// windowSizeDays * pageSize days (e.g. 90 for steps) and rejects a too-large
// pageSize with INVALID_ROLLUP_QUERY_DURATION — so we let it default and bound
// the query by the civil range itself. dataSourceFamily is left empty so the API
// reconciles across every available data source.
type dailyRollUpRequest struct {
	Range          civilTimeInterval `json:"range"`
	WindowSizeDays int               `json:"windowSizeDays"`
}

// rollUpResponse is the dataPoints:dailyRollUp envelope. The wrapper key is
// "rollupDataPoints" (not "dataPoints") and there is no nextPageToken. Points
// stay raw so each aggregated row is re-emitted byte-for-byte (dumb collector).
type rollUpResponse struct {
	RollupDataPoints []json.RawMessage `json:"rollupDataPoints"`
}

// RollUpDaily returns the server-side daily rollup of dt over the civil window
// [from, to). from/to are naive civil (local) datetimes — their wall-clock Y/M/D
// (and time-of-day, when off midnight) are sent verbatim as the aggregation
// range; the API buckets each value onto its civil calendar day. The raw rollup
// rows are returned unchanged. Daily rollups do not paginate.
func (c *Client) RollUpDaily(ctx context.Context, dt DataType, from, to time.Time) ([]json.RawMessage, error) {
	endpoint := fmt.Sprintf("%s/v4/%s/dataTypes/%s/dataPoints:dailyRollUp", c.baseURL, c.user, dt.EndpointName)
	body := dailyRollUpRequest{
		Range:          civilTimeInterval{Start: toCivilDateTime(from), End: toCivilDateTime(to)},
		WindowSizeDays: 1,
	}
	payload, err := json.Marshal(body)
	if err != nil {
		return nil, fmt.Errorf("encode rollup request: %w", err)
	}
	resp, err := c.post(ctx, endpoint, payload)
	if err != nil {
		return nil, err
	}
	return resp.RollupDataPoints, nil
}

// toCivilDateTime renders a civil time.Time as a zone-free CivilDateTime. The
// time member is included only when the bound is off midnight, keeping the
// common (day-aligned) request compact.
func toCivilDateTime(t time.Time) civilDateTime {
	cdt := civilDateTime{Date: civilDate{Year: t.Year(), Month: int(t.Month()), Day: t.Day()}}
	if h, m, s := t.Hour(), t.Minute(), t.Second(); h != 0 || m != 0 || s != 0 {
		cdt.Time = &civilTimeOfDay{Hours: h, Minutes: m, Seconds: s}
	}
	return cdt
}

// post issues one authenticated POST with a JSON body and decodes the rollup
// envelope, mapping non-2xx responses to a typed *Error carrying Google's error
// message — the same decode discipline as get.
func (c *Client) post(ctx context.Context, reqURL string, body []byte) (*rollUpResponse, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, reqURL, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := c.http.Do(req)
	if err != nil {
		return nil, &Error{Message: fmt.Sprintf("request failed: %v", err)}
	}
	defer func() { _ = resp.Body.Close() }()

	data, err := io.ReadAll(io.LimitReader(resp.Body, maxResponseBytes))
	if err != nil {
		return nil, &Error{StatusCode: resp.StatusCode, Message: fmt.Sprintf("read response: %v", err)}
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, &Error{StatusCode: resp.StatusCode, Message: errorMessage(data, resp.StatusCode)}
	}
	var out rollUpResponse
	if err := json.Unmarshal(data, &out); err != nil {
		return nil, &Error{StatusCode: resp.StatusCode, Message: fmt.Sprintf("decode response: %v", err)}
	}
	return &out, nil
}
