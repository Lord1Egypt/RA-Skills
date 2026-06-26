"""
Incident Replay — Configuration Example (Python Reference)
============================================================
⚠️  Config is now JSON format. Use config_example.json instead.
    cp config_example.json incident_config.json

This file is kept as a human-readable reference only. The active
config loader requires a .json file and will raise ValueError on .py.
"""

# ---------------------------------------------------------------------------
# WORKSPACE & PATHS
# ---------------------------------------------------------------------------

# Root directory to monitor for state snapshots
WORKSPACE_ROOT = "."

# Where to store snapshots and incident database
DATA_DIR = "incident_data"

# Subdirectories (created automatically under DATA_DIR)
SNAPSHOTS_DIR = "snapshots"       # state snapshots
INCIDENTS_DIR = "incidents"       # incident records
REPORTS_DIR = "reports"           # generated reports

# ---------------------------------------------------------------------------
# SNAPSHOT CONFIGURATION
# ---------------------------------------------------------------------------

# File patterns to include in snapshots (glob patterns)
INCLUDE_PATTERNS = [
    "*.py",
    "*.md",
    "*.txt",
    "*.json",
    "*.jsonl",
    "*.yaml",
    "*.yml",
    "*.toml",
    "*.cfg",
    "*.ini",
    "*.log",
]

# Patterns to exclude (applied after include)
EXCLUDE_PATTERNS = [
    "__pycache__/*",
    "*.pyc",
    ".git/*",
    "node_modules/*",
    "incident_data/*",     # don't snapshot our own data
    "*.tmp",
    "*.swp",
]

# Maximum file size to include in snapshot content (bytes)
# Files larger than this are tracked (path + hash) but content isn't stored
MAX_FILE_SIZE = 1_000_000  # 1 MB

# Maximum total snapshot size (bytes) — abort if workspace is too large
MAX_SNAPSHOT_SIZE = 50_000_000  # 50 MB

# Maximum number of snapshots to retain (0 = unlimited)
MAX_SNAPSHOTS = 100

# ---------------------------------------------------------------------------
# INCIDENT TRIGGERS
# ---------------------------------------------------------------------------
# Triggers define conditions that flag an output as an incident.
# Each trigger is a dict with:
#   name     — identifier
#   type     — "pattern", "file_change", "log_match", "exit_code"
#   config   — type-specific settings
#   severity — "critical", "high", "medium", "low"

TRIGGERS = [
    {
        "name": "crash_traceback",
        "type": "log_match",
        "config": {
            "patterns": [
                r"Traceback \(most recent call last\)",
                r"Error:|Exception:|FATAL:|CRITICAL:",
            ],
            "log_files": ["*.log", "stderr.txt"],
        },
        "severity": "critical",
    },
    {
        "name": "unexpected_file_deletion",
        "type": "file_change",
        "config": {
            "change_type": "deleted",
            "protected_patterns": ["*.md", "*.py", "config*.py"],
        },
        "severity": "high",
    },
    {
        "name": "config_drift",
        "type": "file_change",
        "config": {
            "change_type": "modified",
            "watch_patterns": ["config*.py", "*.cfg", "*.ini", "*.yaml"],
        },
        "severity": "medium",
    },
    {
        "name": "constraint_violation",
        "type": "pattern",
        "config": {
            "patterns": [
                r"api[_-]?key\s*[:=]",
                r"password\s*[:=]",
                r"secret\s*[:=]",
            ],
            "scan_files": ["*.py", "*.md", "*.txt"],
            "description": "Potential secret or credential in output",
        },
        "severity": "high",
    },
    {
        "name": "empty_output",
        "type": "pattern",
        "config": {
            "check": "empty_file",
            "watch_patterns": ["output*.txt", "result*.json"],
        },
        "severity": "medium",
    },
]

# ---------------------------------------------------------------------------
# ROOT CAUSE CATEGORIES
# ---------------------------------------------------------------------------
# Used for classification during analysis. Each has a description and
# suggested remediation actions.

ROOT_CAUSE_CATEGORIES = {
    "config_error": {
        "description": "Misconfiguration or invalid settings caused the failure",
        "remediation": [
            "Review recent config changes",
            "Validate config against schema",
            "Restore last known good config from snapshot",
            "Add config validation checks",
        ],
    },
    "data_corruption": {
        "description": "Input data was malformed, missing, or corrupted",
        "remediation": [
            "Check data source integrity",
            "Add input validation",
            "Restore data from snapshot",
            "Implement checksums on critical data files",
        ],
    },
    "drift": {
        "description": "Gradual degradation — workspace state drifted from expected",
        "remediation": [
            "Compare current state to baseline snapshot",
            "Identify when drift began using timeline",
            "Reset to known good state",
            "Add periodic state verification checks",
        ],
    },
    "external_failure": {
        "description": "External dependency failed (API, network, filesystem)",
        "remediation": [
            "Check external service status",
            "Review timeout and retry configuration",
            "Add fallback handling",
            "Improve error messages for external failures",
        ],
    },
    "logic_error": {
        "description": "Bug in agent logic or prompt produced incorrect behavior",
        "remediation": [
            "Review decision chain leading to failure",
            "Check for recent prompt or code changes",
            "Add guardrails or validation on outputs",
            "Test with known-good inputs to isolate the bug",
        ],
    },
    "resource_exhaustion": {
        "description": "Ran out of memory, disk, tokens, or time",
        "remediation": [
            "Check resource usage at time of failure",
            "Increase limits or add pagination",
            "Clean up temporary files",
            "Add resource monitoring and early warnings",
        ],
    },
    "unknown": {
        "description": "Root cause could not be determined from available data",
        "remediation": [
            "Increase logging verbosity",
            "Add more snapshot points around the failure area",
            "Reproduce the failure with more instrumentation",
            "Escalate for manual investigation",
        ],
    },
}

# ---------------------------------------------------------------------------
# LOG PARSING
# ---------------------------------------------------------------------------

# Log file patterns to scan for decision chain extraction
LOG_FILES = ["*.log", "memory/*.md", "*.jsonl"]

# Regex patterns to extract decision points from logs
DECISION_MARKERS = [
    r"(?:decided|choosing|selected|picked|using|switching to)\s+(.+)",
    r"(?:action|step|phase|stage):\s*(.+)",
    r"(?:reason|because|rationale):\s*(.+)",
]

# Maximum log lines to process per file
MAX_LOG_LINES = 10000

# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------

# How many snapshots back to examine when building a timeline
TIMELINE_DEPTH = 10

# Minimum file changes to flag as "significant" in diff analysis
SIGNIFICANT_CHANGE_THRESHOLD = 5

# ---------------------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------------------

# Default report format: "markdown" or "json"
DEFAULT_REPORT_FORMAT = "markdown"

# Include full file diffs in reports (can be verbose)
INCLUDE_FULL_DIFFS = False

# Include decision chain in reports
INCLUDE_DECISION_CHAIN = True

# Maximum diff lines to include per file
MAX_DIFF_LINES = 100
