package wire

// WireResult describes what happened during a wiring operation.
type WireResult struct {
	Service string // source service
	Target  string // target service or resource
	Action  string // "ok", "created", "updated", "skipped", "failed"
	Detail  string // human-readable detail
	Err     error  // nil on success
}
