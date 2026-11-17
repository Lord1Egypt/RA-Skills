package cli

import "io"

// privacyNotice is the execution-time warning emitted to stderr (never stdout —
// stdout is data) by every command that prints personal health data. ClawHub's
// "Missing User Warnings" check wants a runtime heads-up, not only docs: in an
// agent or pipeline, stdout is frequently auto-captured and forwarded, so each
// run reminds the caller that the output is sensitive PII it must handle with
// care. It goes to stderr so it never corrupts the machine-readable stdout.
const privacyNotice = "privacy: output contains sensitive personal health data (PII); " +
	"downstream agents, logs, and pipelines may capture, persist, or forward it — handle accordingly."

// emitPrivacyNotice writes the runtime privacy notice to w (the command's
// stderr). It is deliberately unconditional and unsuppressable: the warning is a
// safety floor for sensitive-output commands, not a user preference to toggle.
func emitPrivacyNotice(w io.Writer) {
	fprintln(w, privacyNotice)
}
