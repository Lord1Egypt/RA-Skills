---
name: "host-dependency-triage"
description: "ComfyUI logs report missing external tools; isolate host, config, and executable paths quickly."
---

# Host Dependency Triage

Use when a Windows-hosted ComfyUI package reports a missing external executable while startup otherwise continues.

1. Classify each log line as fatal, warning, or informational, then use the final node-load count to decide whether the dependency blocks startup or only a feature; finish when the blocked scope is explicit.
2. Extract the dependency name and the configuration key/path named by the warning, and inspect that exact configuration before changing anything; finish when the configured value is confirmed as real, placeholder, or unset.
3. Identify the host that runs the application, then test the executable on that host rather than reusing a same-named binary from another environment; finish when the application’s runtime boundary and a matching executable boundary agree.
4. Search the application tree with a bounded depth for the executable, and check the host’s normal command lookup when available; finish when you have either an absolute executable path or evidence that it is absent.
5. Set the configuration to the discovered host-native absolute path, preserving the existing JSON structure, then restart the application and refresh its browser client; finish when the startup warning is gone or the remaining failure names a different cause.
6. Treat unrelated startup messages independently: stale registry-cache notices do not explain a missing executable, and a successful node load does not prove feature-level dependencies work; finish when each remaining message has a separate disposition.

Evidence: Session 4, activity 2026-07-07.
