package gates

import "encoding/json"

// Status represents a gate's pass/fail status.
type Status string

const (
	StatusPass Status = "PASS"
	StatusFail Status = "FAIL"
	StatusWarn Status = "WARN"
	StatusSkip Status = "SKIP"
)

// Evidence represents a single piece of evidence collected during gate evaluation.
type Evidence struct {
	Source string `json:"source"`
	Key    string `json:"key"`
	Value  string `json:"value"`
}

// Result is the output of a single gate evaluation.
type Result struct {
	Gate     string     `json:"gate"`
	GateNum  int        `json:"gate_num"`
	Status   Status     `json:"status"`
	Reason   string     `json:"reason"`
	Evidence []Evidence `json:"evidence"`
}

// Gate is the interface all gates must implement.
type Gate interface {
	Name() string
	Number() int
	Evaluate(token string, chainID int64) (*Result, error)
}

// JSON serializes the result.
func (r *Result) JSON() string {
	b, _ := json.MarshalIndent(r, "", "  ")
	return string(b)
}

// NewResult creates a result with defaults.
func NewResult(gate string, num int) *Result {
	return &Result{
		Gate:     gate,
		GateNum:  num,
		Evidence: []Evidence{},
	}
}

// Pass marks the result as passed.
func (r *Result) Pass(reason string) *Result {
	r.Status = StatusPass
	r.Reason = reason
	return r
}

// Fail marks the result as failed.
func (r *Result) Fail(reason string) *Result {
	r.Status = StatusFail
	r.Reason = reason
	return r
}

// Warn marks the result as warning.
func (r *Result) Warn(reason string) *Result {
	r.Status = StatusWarn
	r.Reason = reason
	return r
}

// AddEvidence appends evidence to the result.
func (r *Result) AddEvidence(source, key, value string) {
	r.Evidence = append(r.Evidence, Evidence{
		Source: source,
		Key:    key,
		Value:  value,
	})
}
