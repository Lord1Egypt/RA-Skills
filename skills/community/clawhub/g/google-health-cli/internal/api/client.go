package api

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// maxResponseBytes caps how much of a response body we read, guarding against a
// hostile or broken server streaming forever (GOAL.md §9 decode discipline).
const maxResponseBytes = 32 << 20 // 32 MiB

// pageSize is clamped to 25: Google caps exercise/sleep dataPoints at 25 per
// page regardless of the documented 10k max (GOAL.md §9).
const pageSize = 25

// Error is a typed API failure. The CLI maps it to exit code 2 (GOAL.md §12).
// Message is Google's error-envelope message when available, else an HTTP/IO
// description.
type Error struct {
	StatusCode int
	Message    string
}

func (e *Error) Error() string { return e.Message }

// Client issues read-only exercise dataPoints.list requests. The *http.Client it
// holds already injects + refreshes the OAuth2 bearer token and carries the
// request timeout (built in internal/auth); this type only owns URL building,
// pagination, and decode (GOAL.md §9).
type Client struct {
	http    *http.Client
	baseURL string // e.g. https://health.googleapis.com
	user    string // e.g. users/me
	logger  *slog.Logger
}

// New builds a Client. baseURL and user come from config (both overridable as a
// test seam); httpClient is the authenticated client from internal/auth.
func New(httpClient *http.Client, baseURL, user string, logger *slog.Logger) *Client {
	if logger == nil {
		logger = slog.New(slog.NewTextHandler(io.Discard, nil))
	}
	return &Client{
		http:    httpClient,
		baseURL: strings.TrimRight(baseURL, "/"),
		user:    strings.Trim(user, "/"),
		logger:  logger,
	}
}

// ListDataPoints returns every data point of dt whose default time field falls
// in [from, to). When filtered is false the time filter is omitted and the API
// returns everything it has for that type. It follows nextPageToken until the
// API stops paginating. For civil types from/to are naive local civil datetimes;
// for sample/daily types they are absolute instants.
func (c *Client) ListDataPoints(ctx context.Context, dt DataType, from, to time.Time, filtered bool) ([]DataPoint, error) {
	endpoint := fmt.Sprintf("%s/v4/%s/dataTypes/%s/dataPoints", c.baseURL, c.user, dt.EndpointName)

	var points []DataPoint
	pageToken := ""
	for {
		q := url.Values{}
		if filtered {
			q.Set("filter", dt.RangeFilter(from, to))
		}
		q.Set("pageSize", fmt.Sprintf("%d", pageSize))
		if pageToken != "" {
			q.Set("pageToken", pageToken)
		}
		reqURL := endpoint + "?" + q.Encode()

		resp, err := c.get(ctx, reqURL)
		if err != nil {
			return nil, err
		}
		for _, raw := range resp.DataPoints {
			var dp DataPoint
			if err := json.Unmarshal(raw, &dp); err != nil {
				// A single malformed point shouldn't abort the list, nor should
				// it disappear from `sessions --raw`. Keep the raw bytes; the
				// zero-valued typed fields make ParseSession yield nils, exactly
				// as the tolerant Python parse_session does (GOAL.md §12).
				c.logger.Warn("data point typed-decode failed; keeping raw", "err", err)
			}
			dp.Raw = raw
			points = append(points, dp)
		}
		if resp.NextPageToken == "" {
			break
		}
		pageToken = resp.NextPageToken
	}
	return points, nil
}

// ErrPathNotAllowed is returned by RawGet when the requested path falls outside
// the advertised read-only Google Health v4 surface — a non-`v4/` path, an
// absolute URL / "//authority", or a parent-directory traversal. The CLI maps it
// to a usage error (exit 64). It exists so the `api get` escape hatch's *actual*
// reach equals what the tool advertises (a read-only v4 GET), closing the
// description/behavior gap a scanner would otherwise flag.
var ErrPathNotAllowed = errors.New("path is outside the read-only Google Health v4 surface")

// validateRawPath enforces that RawGet can address only the read-only v4 surface.
// A GET is already non-mutating, but without this a caller could aim the path at
// any endpoint under the configured base host — or, via a smuggled scheme or
// protocol-relative "//authority", at a different host entirely. We therefore
// require a "v4/…" path and reject absolute URLs and ".." traversal. It returns
// the cleaned, base-relative path (leading slash removed) on success.
func validateRawPath(path string) (string, error) {
	trimmed := strings.TrimSpace(path)
	if trimmed == "" {
		return "", fmt.Errorf("%w: empty path (expected e.g. v4/users/me/profile)", ErrPathNotAllowed)
	}
	// No absolute URL or protocol-relative authority: the escape hatch may only
	// address the configured base host, never an arbitrary one.
	if strings.Contains(trimmed, "://") || strings.HasPrefix(trimmed, "//") {
		return "", fmt.Errorf("%w: %q must be a base-relative v4 path, not an absolute URL", ErrPathNotAllowed, path)
	}
	rel := strings.TrimLeft(trimmed, "/")
	// Inspect the path portion (excluding any query/fragment) for traversal and
	// the required v4 prefix.
	pathPart := rel
	if i := strings.IndexAny(pathPart, "?#"); i >= 0 {
		pathPart = pathPart[:i]
	}
	for _, seg := range strings.Split(pathPart, "/") {
		if seg == ".." {
			return "", fmt.Errorf("%w: %q must not contain '..' segments", ErrPathNotAllowed, path)
		}
	}
	if pathPart != "v4" && !strings.HasPrefix(pathPart, "v4/") {
		return "", fmt.Errorf("%w: %q is not a /v4/ path (api get reaches only read-only v4 endpoints)", ErrPathNotAllowed, path)
	}
	return rel, nil
}

// RawGet performs one authenticated GET against path (joined to the base URL) and
// returns the response body verbatim. It is the read-only escape hatch behind the
// `api get` command, reaching read-only v4 endpoints the typed surface does not
// model (profile, settings, identity, a single dataPoint by name, …). The path is
// validated to the read-only v4 surface first (see validateRawPath): a non-`v4/`
// path, an absolute URL, or a ".." traversal is rejected with ErrPathNotAllowed
// and makes no network call. Non-2xx responses become a typed *Error carrying
// Google's message.
func (c *Client) RawGet(ctx context.Context, path string) (json.RawMessage, error) {
	rel, err := validateRawPath(path)
	if err != nil {
		return nil, err
	}
	reqURL := c.baseURL + "/" + rel
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, reqURL, nil)
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
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
	return json.RawMessage(data), nil
}

// get performs one GET and decodes the list envelope, mapping non-2xx responses
// to a typed *Error carrying Google's error message (GOAL.md §9).
func (c *Client) get(ctx context.Context, reqURL string) (*listResponse, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, reqURL, nil)
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
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

	var out listResponse
	if err := json.Unmarshal(data, &out); err != nil {
		return nil, &Error{StatusCode: resp.StatusCode, Message: fmt.Sprintf("decode response: %v", err)}
	}
	return &out, nil
}

// errorMessage extracts Google's error-envelope message, falling back to a
// generic HTTP status description. When the envelope carries BadRequest
// fieldViolations (e.g. an over-long rollup range), their descriptions are
// appended so the user sees the actionable detail, not just "Invalid argument".
func errorMessage(body []byte, status int) string {
	var ae apiError
	if err := json.Unmarshal(body, &ae); err == nil && ae.Error.Message != "" {
		msg := ae.Error.Message
		var violations []string
		for _, d := range ae.Error.Details {
			for _, fv := range d.FieldViolations {
				if fv.Description == "" {
					continue
				}
				if fv.Field != "" {
					violations = append(violations, fv.Field+": "+fv.Description)
				} else {
					violations = append(violations, fv.Description)
				}
			}
		}
		if len(violations) > 0 {
			msg += " (" + strings.Join(violations, "; ") + ")"
		}
		return msg
	}
	snippet := strings.TrimSpace(string(body))
	if len(snippet) > 300 {
		snippet = snippet[:300]
	}
	if snippet == "" {
		return fmt.Sprintf("HTTP %d", status)
	}
	return fmt.Sprintf("HTTP %d: %s", status, snippet)
}
