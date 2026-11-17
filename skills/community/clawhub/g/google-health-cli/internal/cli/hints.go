package cli

import (
	"fmt"

	"github.com/stozo04/google-health-cli/internal/api"
)

// readHint names the command that can actually read dt, derived from its
// catalog operations so a rejection can never point the caller at another
// command that also fails (daily-heart-rate-zones is reconcile-only: neither
// `data list` nor `rollup daily` works, only the `api get` escape hatch).
// api.TestEveryTypeReachableByTypedCommandOrDocumentedException keeps the
// escape-hatch case an explicit, documented exception.
func readHint(dt api.DataType) string {
	switch {
	case dt.Supports("list"):
		return fmt.Sprintf("read it with `google-health-cli data list %s`", dt.EndpointName)
	case dt.Supports("dailyRollUp"):
		return fmt.Sprintf("read it with `google-health-cli rollup daily %s`", dt.EndpointName)
	default:
		return fmt.Sprintf("no typed command reads it; use `google-health-cli api get` against a read-only v4 %s endpoint",
			dt.EndpointName)
	}
}
