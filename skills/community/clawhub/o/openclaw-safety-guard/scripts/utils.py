import os
import json
import re
from datetime import datetime
from pathlib import Path


def _is_real_openclaw_root(path):
    """The real .openclaw root contains config file or shared/ dir, not just workspace-state.json."""
    return (
        os.path.exists(os.path.join(path, 'config')) or
        os.path.isdir(os.path.join(path, 'shared')) or
        any(d.startswith('workspace-') for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)))
    )


def get_openclaw_root():
    """Finds the .openclaw directory dynamically by walking up from this script."""
    current = os.path.abspath(os.path.dirname(__file__))
    while current != '/':
        if os.path.basename(current) == '.openclaw' and _is_real_openclaw_root(current):
            return current
        candidate = os.path.join(current, '.openclaw')
        if os.path.isdir(candidate) and _is_real_openclaw_root(candidate):
            return candidate
        current = os.path.dirname(current)
    fallback = os.path.expanduser('~/.openclaw')
    if os.path.exists(fallback):
        return fallback
    raise RuntimeError("Cannot find .openclaw root directory")


def get_workspace_root():
    """Returns the project root containing the .openclaw folder."""
    oc_root = get_openclaw_root()
    if os.path.basename(oc_root) == '.openclaw':
        return os.path.dirname(oc_root)
    return oc_root


def get_data_dir():
    """Returns the data directory inside the watchdog skill."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_watchdog_config():
    """Loads watchdog config.json with defaults."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def auto_detect_agents(config=None):
    """
    Returns a list of agent IDs.
    If config["agents"] == "auto" or is missing, scans .openclaw/ for workspace-* dirs.
    Otherwise uses the explicit list from config.
    """
    if config is None:
        config = get_watchdog_config()

    agents_cfg = config.get("agents", "auto")

    if isinstance(agents_cfg, list) and len(agents_cfg) > 0:
        return agents_cfg

    root = Path(get_openclaw_root())
    detected = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name.startswith("workspace-"):
            agent_id = entry.name[len("workspace-"):]
            if agent_id:
                detected.append(agent_id)
    return detected if detected else []


def read_file_safe(path) -> str:
    """Read a file, returning empty string on any error."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError):
        return ""


# --- Dimension label mapping (scanner_name -> Chinese label) ---
DIMENSION_LABELS = {
    "heartbeat": "心跳监控",
    "standards": "核心规范",
    "memory": "记忆健康",
    "cron": "定时任务",
    "shared": "共享层",
    "comm": "通信路由",
    "security": "安全底座",
}

DIMENSION_ORDER = ["heartbeat", "standards", "memory", "cron", "shared", "comm", "security"]


class WatchdogReport:
    def __init__(self, scanner_name):
        self.scanner_name = scanner_name
        self.status = "active"  # "active" | "not_applicable"
        self.na_reason = ""
        self.issues = []
        self.metadata = {}  # hover panel data, populated by each scanner
        self.summary = {"total": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

    def mark_not_applicable(self, reason):
        self.status = "not_applicable"
        self.na_reason = reason

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def add_issue(self, issue_id, severity, title, fix_command,
                  affected_files=None, evidence=None, fix_action=None):
        if severity not in ("HIGH", "MEDIUM", "LOW"):
            severity = "MEDIUM"
        issue = {
            "id": f"{self.scanner_name}_{issue_id}",
            "severity": severity,
            "title": title,
            "fix_command": fix_command,
            "affected_files": affected_files or [],
        }
        if evidence:
            issue["evidence"] = evidence if isinstance(evidence, list) else [evidence]
        if fix_action:
            issue["fix_action"] = fix_action
        self.issues.append(issue)
        self.summary["total"] += 1
        self.summary[severity] += 1

    def save(self):
        data = {
            "scanner": self.scanner_name,
            "status": self.status,
            "scanned_at": datetime.now().isoformat(),
            "summary": self.summary,
            "metadata": self.metadata,
            "issues": self.issues,
        }
        if self.status == "not_applicable":
            data["na_reason"] = self.na_reason

        out_path = os.path.join(get_data_dir(), f"latest_{self.scanner_name}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        label = DIMENSION_LABELS.get(self.scanner_name, self.scanner_name)
        if self.status == "not_applicable":
            print(f"[{label}] N/A - {self.na_reason}")
        else:
            print(f"[{label}] Saved report with {self.summary['total']} issues")
