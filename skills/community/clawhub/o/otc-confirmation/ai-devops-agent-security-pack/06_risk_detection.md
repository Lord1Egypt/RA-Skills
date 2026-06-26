# 06 — Risk Detection Engine

> Pattern matching and anomaly detection for AI agent operations.

## Overview

Risk Detection is the **proactive** layer of the security stack. While Permission Guard checks rules and OTC confirms intent, the Risk Detection Engine looks for **suspicious patterns** that individual checks might miss.

It answers: "Even though each operation might be individually permitted, does the overall behavior look dangerous?"

## Threat Scoring Model

Every operation receives a **risk score** (0-100):

```
0-20:   LOW       → Normal operation, no action
21-50:  MEDIUM    → Log for review, continue
51-75:  HIGH      → Require OTC confirmation
76-100: CRITICAL  → Block and alert immediately
```

### Scoring Factors

```python
RISK_FACTORS = {
    # Operation type base scores
    "base_scores": {
        "file_read": 5,
        "file_write": 15,
        "file_delete": 40,
        "exec_command": 30,
        "send_email": 35,
        "deploy": 50,
        "modify_permissions": 60,
        "network_request": 20,
    },
    
    # Multipliers based on context
    "multipliers": {
        "production_target": 2.0,
        "system_path": 1.8,
        "after_hours": 1.3,      # 22:00-08:00
        "high_frequency": 1.5,    # Above normal rate
        "first_time_operation": 1.4,
        "recursive_flag": 1.6,    # -r, -R, --recursive
        "force_flag": 1.5,        # -f, --force
        "sudo_prefix": 1.8,
    },
    
    # Reduction factors (lower risk)
    "reductions": {
        "dry_run_flag": 0.3,      # --dry-run
        "within_project_dir": 0.7,
        "previously_confirmed": 0.5,
        "read_only": 0.4,
    }
}

def calculate_risk_score(operation: dict) -> int:
    """Calculate composite risk score for an operation."""
    base = RISK_FACTORS["base_scores"].get(operation["type"], 25)
    score = float(base)
    
    # Apply multipliers
    for factor, multiplier in RISK_FACTORS["multipliers"].items():
        if check_factor(operation, factor):
            score *= multiplier
    
    # Apply reductions
    for factor, reduction in RISK_FACTORS["reductions"].items():
        if check_factor(operation, factor):
            score *= reduction
    
    return min(100, max(0, int(score)))
```

## Pattern Detection

### Dangerous Command Patterns

```python
DANGEROUS_PATTERNS = [
    {
        "name": "recursive_delete",
        "pattern": r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*|-[a-zA-Z]*R[a-zA-Z]*|--recursive)",
        "risk_score": 80,
        "description": "Recursive file deletion"
    },
    {
        "name": "disk_format",
        "pattern": r"(mkfs|fdisk|parted|diskutil\s+eraseDisk)",
        "risk_score": 100,
        "description": "Disk formatting operation"
    },
    {
        "name": "permission_change_recursive",
        "pattern": r"(chmod|chown)\s+(-[a-zA-Z]*R[a-zA-Z]*|--recursive)",
        "risk_score": 70,
        "description": "Recursive permission change"
    },
    {
        "name": "service_stop",
        "pattern": r"(systemctl\s+stop|service\s+\S+\s+stop|kill\s+-9)",
        "risk_score": 60,
        "description": "Service termination"
    },
    {
        "name": "data_exfiltration",
        "pattern": r"curl\s+.*(-d|--data|--upload-file)\s+.*\.(pem|key|env|passwd|shadow)",
        "risk_score": 95,
        "description": "Potential data exfiltration of sensitive files"
    },
    {
        "name": "reverse_shell",
        "pattern": r"(bash\s+-i\s+>|nc\s+-[a-z]*e|/dev/tcp/|python.*socket.*connect)",
        "risk_score": 100,
        "description": "Potential reverse shell"
    },
    {
        "name": "env_dump",
        "pattern": r"(printenv|env\s*$|echo\s+\$[A-Z_]*(PASS|SECRET|KEY|TOKEN))",
        "risk_score": 75,
        "description": "Environment variable exposure"
    },
    {
        "name": "ssh_key_access",
        "pattern": r"cat\s+.*\.ssh/(id_|authorized_keys|known_hosts)",
        "risk_score": 85,
        "description": "SSH key file access"
    },
]

def scan_command(command: str) -> list[dict]:
    """Scan a command for dangerous patterns."""
    matches = []
    for pattern_def in DANGEROUS_PATTERNS:
        if re.search(pattern_def["pattern"], command, re.IGNORECASE):
            matches.append({
                "pattern": pattern_def["name"],
                "risk_score": pattern_def["risk_score"],
                "description": pattern_def["description"],
            })
    return matches
```

### Behavioral Anomaly Detection

Beyond individual commands, detect suspicious **sequences**:

```python
class BehaviorAnalyzer:
    """Detect suspicious operation sequences."""
    
    def __init__(self, window_minutes=30):
        self.window = window_minutes * 60
        self.history = []
    
    def analyze(self, operation: dict) -> list[str]:
        """Check for anomalous behavior patterns."""
        now = time.time()
        self.history.append({"operation": operation, "time": now})
        
        # Clean old history
        self.history = [h for h in self.history if now - h["time"] < self.window]
        
        alerts = []
        
        # Pattern: Reconnaissance → Exploitation
        # Read sensitive files, then exec commands
        if self._detect_recon_then_exec():
            alerts.append("RECON_EXPLOIT: Read sensitive files followed by command execution")
        
        # Pattern: Rapid file access across directories
        # Indicates scanning/enumeration
        if self._detect_directory_scan():
            alerts.append("DIR_SCAN: Rapid file access across many directories")
        
        # Pattern: Privilege escalation attempt
        # Normal ops → sudo/chmod → sensitive file access
        if self._detect_privesc():
            alerts.append("PRIVESC: Potential privilege escalation sequence")
        
        # Pattern: Data staging
        # Multiple reads → archive/compress → network send
        if self._detect_data_staging():
            alerts.append("DATA_STAGING: Potential data exfiltration preparation")
        
        return alerts
    
    def _detect_recon_then_exec(self) -> bool:
        recent = self.history[-10:]
        sensitive_reads = [h for h in recent 
                          if h["operation"]["type"] == "file_read"
                          and any(p in h["operation"].get("path", "") 
                                 for p in [".env", ".ssh", "passwd", "shadow", ".key"])]
        exec_after = [h for h in recent
                      if h["operation"]["type"] == "exec_command"
                      and any(h["time"] > r["time"] for r in sensitive_reads)]
        return len(sensitive_reads) > 0 and len(exec_after) > 0
    
    def _detect_directory_scan(self) -> bool:
        recent_reads = [h for h in self.history[-20:]
                        if h["operation"]["type"] == "file_read"]
        if len(recent_reads) < 5:
            return False
        unique_dirs = set(os.path.dirname(h["operation"].get("path", "")) 
                         for h in recent_reads)
        return len(unique_dirs) > 8
    
    def _detect_privesc(self) -> bool:
        recent = self.history[-15:]
        has_chmod = any(h for h in recent 
                       if "chmod" in h["operation"].get("command", "")
                       or "chown" in h["operation"].get("command", ""))
        has_sudo = any(h for h in recent
                      if h["operation"].get("command", "").startswith("sudo"))
        return has_chmod and has_sudo
    
    def _detect_data_staging(self) -> bool:
        recent = self.history[-20:]
        reads = sum(1 for h in recent if h["operation"]["type"] == "file_read")
        archives = sum(1 for h in recent 
                      if any(cmd in h["operation"].get("command", "") 
                            for cmd in ["tar", "zip", "gzip", "base64"]))
        network = sum(1 for h in recent
                     if any(cmd in h["operation"].get("command", "")
                           for cmd in ["curl", "wget", "scp", "rsync"]))
        return reads > 5 and archives > 0 and network > 0
```

## Prompt Injection Detection

```python
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)\s+instructions",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"new\s+instructions?\s*:",
    r"system\s*:\s*you",
    r"forget\s+(everything|all|your\s+rules)",
    r"act\s+as\s+(if|though)\s+you",
    r"pretend\s+(you|to\s+be)",
    r"override\s+(safety|security|rules)",
    r"disregard\s+(all|previous|safety)",
    r"jailbreak",
    r"DAN\s+mode",
]

def detect_prompt_injection(text: str) -> tuple[bool, list[str]]:
    """Scan text for prompt injection attempts."""
    matches = []
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)
    return len(matches) > 0, matches
```

## Integration: Risk-Based Decision Flow

```python
def evaluate_operation(operation: dict, agent_role: str) -> dict:
    """Complete risk evaluation pipeline."""
    
    # Step 1: Pattern scan
    pattern_matches = scan_command(operation.get("command", ""))
    
    # Step 2: Risk score
    risk_score = calculate_risk_score(operation)
    
    # Step 3: Behavioral analysis
    behavior_alerts = behavior_analyzer.analyze(operation)
    
    # Step 4: Combine signals
    if pattern_matches:
        max_pattern_score = max(m["risk_score"] for m in pattern_matches)
        risk_score = max(risk_score, max_pattern_score)
    
    if behavior_alerts:
        risk_score = min(100, risk_score + 20)  # Behavioral bump
    
    # Step 5: Decision
    if risk_score >= 76:
        decision = "BLOCK"
    elif risk_score >= 51:
        decision = "CONFIRM"  # Trigger OTC
    elif risk_score >= 21:
        decision = "LOG"      # Allow but log prominently
    else:
        decision = "ALLOW"
    
    return {
        "risk_score": risk_score,
        "decision": decision,
        "pattern_matches": pattern_matches,
        "behavior_alerts": behavior_alerts,
    }
```
