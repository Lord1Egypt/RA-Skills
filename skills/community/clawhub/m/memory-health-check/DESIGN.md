# DESIGN.md — memory-health-check

> **Version:** 1.0.0  
> **Date:** 2026-04-17  
> **Author:** 道衍 (架构师)  
> **Status:** Ready for Development  

---

## 1. Overview

`memory-health-check` is a proactive diagnostic Skill for OpenClaw agents that monitors memory integrity, detects corruption, identifies bloat, flags orphaned entries, and provides actionable repair recommendations — analogous to a medical check-up for the Agent's brain.

**Core Promise:** An ounce of prevention is worth a pound of lost memories.

---

## 2. Technical Architecture

### 2.1 High-Level Architecture

```
[Scheduled Trigger / Manual Invoke]
              │
              ▼
┌─────────────────────────────────────────────────────┐
│              Health Diagnostic Pipeline              │
│                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ Integrity   │  │ Bloat       │  │ Orphan       │  │
│  │ Scanner     │  │ Detector    │  │ Finder       │  │
│  │             │  │             │  │             │  │
│  │ • SQLite    │  │ • Dir size  │  │ • Link graph │  │
│  │   checksum  │  │ • File cnt  │  │ • Ref count  │  │
│  │ • Corruption│  │ • Growth    │  │ • Orphan %   │  │
│  │   markers   │  │   rate      │  │             │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │         │
│         └────────────────┼────────────────┘         │
│                          │                          │
│         ┌────────────────┼────────────────┐         │
│         ▼                ▼                ▼         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ Dedup       │  │ Freshness   │  │ Coverage    │  │
│  │ Scanner     │  │ Report      │  │ Analyzer    │  │
│  │             │  │             │  │             │  │
│  │ • Token     │  │ • Age dist  │  │ • Domain    │  │
│  │   overlap   │  │ • 7/30/90d  │  │   breadth   │  │
│  │ • Dup rate  │  │ • Fresh %   │  │ • Gap       │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │         │
│         └────────────────┼────────────────┘         │
│                          │                          │
│              ┌───────────▼───────────┐              │
│              │  Health Score Engine   │              │
│              │                        │              │
│              │  Weighted avg 0-100     │              │
│              │  6 dimensions           │              │
│              └───────────┬─────────────┘              │
│                          │                          │
│              ┌───────────▼───────────┐              │
│              │  Report Generator    │              │
│              │                      │              │
│              │  Auto-repairable?    │              │
│              │  Human actionable?    │              │
│              └──────────────────────┘              │
└─────────────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
      [health-reports/*.json]  [auto-repair on approval]
```

### 2.2 Component Architecture

```
memory-health-check/
├── SKILL.md                      # Public skill manifest
├── DESIGN.md                      # This file — technical design
├── bin/
│   ├── health_check.sh            # CLI entry point
│   ├── integrity_scan.py          # DB corruption / checksum checks
│   ├── bloat_detector.py          # Size + file count analysis
│   ├── orphan_finder.py           # Reference graph orphan detection
│   ├── dedup_scanner.py           # Duplicate entry detection
│   ├── freshness_report.py        # Entry age distribution
│   └── health_score.py           # Aggregate scoring engine
├── scripts/
│   ├── generate_report.py         # HTML/text report generator
│   └── auto_repair.py            # Orphan cleanup script
├── lib/                          # Shared utilities (NEW)
│   ├── __init__.py
│   ├── config_loader.py          # YAML config loader with defaults
│   ├── sqlite_scanner.py         # Reusable SQLite scanning utilities
│   ├── file_scanner.py           # Reusable file system scanning
│   └── health_models.py          # dataclass definitions for health data
├── config/
│   └── thresholds.yaml            # Configurable health thresholds
├── reports/                       # Generated health reports
│   └── .gitkeep
├── tests/                        # Test suite (NEW)
│   ├── __init__.py
│   ├── test_integrity_scan.py
│   ├── test_bloat_detector.py
│   ├── test_orphan_finder.py
│   ├── test_dedup_scanner.py
│   ├── test_freshness_report.py
│   ├── test_health_score.py
│   └── test_integration.py
└── README.md                     # Usage documentation
```

---

## 3. Health Dimensions & Scoring

### 3.1 Six Health Dimensions

| # | Dimension | What It Measures | Healthy | Warning | Critical |
|---|-----------|-----------------|---------|---------|---------|
| 1 | **Integrity** | DB checksums, corruption markers | 100 | 80 | <80 |
| 2 | **Freshness** | % entries updated in last 30 days | >70% | 40-70% | <40% |
| 3 | **Bloat** | Total memory directory size | <500MB | 500MB-2GB | >2GB |
| 4 | **Orphans** | Entries with zero inbound references | 0% | 1-5% | >5% |
| 5 | **Dedup** | Duplicate/near-duplicate rate | <2% | 2-10% | >10% |
| 6 | **Coverage** | Breadth of knowledge domains | >80% | 50-80% | <50% |

### 3.2 Overall Health Score Formula

```python
# Weighted average of 6 dimensions
HEALTH_SCORE = (
    integrity_score  * 0.30 +   # Most critical — data loss risk
    freshness_score  * 0.20 +
    bloat_score      * 0.15 +
    orphan_score     * 0.15 +
    dedup_score      * 0.10 +
    coverage_score   * 0.10
)

# Status thresholds
if HEALTH_SCORE >= 80:  status = "healthy"   (✅ Green)
elif HEALTH_SCORE >= 50: status = "warning"   (⚠️ Yellow)
else:                   status = "critical"  (🔴 Red)
```

### 3.3 Per-Dimension Scoring Detail

**Integrity Score (0/100):**
```python
def integrity_score(issues: list[str]) -> int:
    if len(issues) == 0: return 100
    if any("corruption" in i.lower() for i in issues): return 0
    if any("error" in i.lower() for i in issues): return 50
    return 80  # some warnings but no errors
```

**Freshness Score (0-100):**
```python
def freshness_score(recent_30d: int, total: int) -> int:
    rate = recent_30d / max(total, 1)
    if rate > 0.70: return 100
    if rate > 0.40: return 60
    return 20
```

**Bloat Score (0-100):**
```python
def bloat_score(total_mb: float) -> int:
    if total_mb < 500:   return 100
    if total_mb < 2000:  return 60
    return 20
```

**Orphan Score (0-100):**
```python
def orphan_score(orphan_rate: float) -> int:
    if orphan_rate < 0.01: return 100
    if orphan_rate < 0.05: return 70
    return 30
```

**Dedup Score (0-100):**
```python
def dedup_score(dup_rate: float) -> int:
    if dup_rate < 0.02:  return 100
    if dup_rate < 0.10:  return 60
    return 20
```

**Coverage Score (0-100):**
```python
# Defined domains:
DOMAINS = ["技术", "商业", "创意", "人际关系", "个人成长", "日常"]

def coverage_score(domains_found: set[str], total: int) -> int:
    coverage = len(domains_found) / len(DOMAINS)
    if total == 0: return 0  # no content at all
    if coverage > 0.80: return 100
    if coverage > 0.50: return 60
    return 20
```

---

## 4. Data Flow

### 4.1 Pipeline Data Flow

```
INVOCATION (cron / manual / pre-upgrade)
    │
    ▼
[1] DISCOVER MEMORY PATHS
    • ~/.openclaw/workspace/memory/         (A-layer)
    • ~/.openclaw/memory/*.sqlite           (B-layer)
    • ~/.openclaw/workspace/*/memory/       (other agents)
    │
    ▼
[2] RUN 6 DIAGNOSTICS IN PARALLEL
    ├── integrity_scan()    → integrity_issues[], integrity_score
    ├── bloat_detector()    → total_bytes, file_count, growth_rate, bloat_score
    ├── orphan_finder()    → orphan_count, orphan_rate, orphan_score
    ├── dedup_scanner()    → dup_count, dup_rate, dedup_score
    ├── freshness_report() → recent_7d, recent_30d, freshness_score
    └── coverage_analyzer() → domains_found[], coverage_score
    │
    ▼
[3] AGGREGATE HEALTH SCORE
    health_score = weighted_avg(all_6_dimensions)
    │
    ▼
[4] GENERATE REPAIR PLAN
    ├── Auto-repairable: orphaned temp files, .DS_Store
    └── Human actionable: DB corruption, bloat, dedup suggestions
    │
    ▼
[5] OUTPUT
    ├── Report: ~/.openclaw/workspace/memory/health-reports/health-report-YYYY-MM-DD.json
    ├── Auto-repair: ~/.openclaw/workspace/memory/health-reports/auto-repair-plan.md
    └── (Optional) Health badge in OpenClaw UI
```

### 4.2 Data Structures

```python
@dataclass
class HealthReport:
    ts: str                           # ISO timestamp
    overall_score: float              # 0-100
    status: str                      # "healthy" | "warning" | "critical"
    dimensions: dict[str, DimResult]
    recommendations: list[Recommendation]
    auto_repair_plan: list[str]
    metadata: ReportMetadata

@dataclass
class DimResult:
    score: int                        # 0-100
    status: str                      # "healthy" | "warning" | "critical"
    value: Any                       # Dimension-specific value
    details: dict                    # Additional info
    issues: list[str]                # Specific issues found

@dataclass
class Recommendation:
    dimension: str
    severity: str                    # "critical" | "warning" | "info"
    action: str                      # Human-readable action
    auto_repairable: bool
    cli_command: str | None         # Optional fix command
```

---

## 5. File Structure

```
memory-health-check/
├── SKILL.md                          # Public skill manifest
├── DESIGN.md                         # This file
├── bin/
│   ├── health_check.sh               # CLI orchestrator
│   ├── integrity_scan.py             # DB integrity checker
│   ├── bloat_detector.py             # Size/growth analyzer
│   ├── orphan_finder.py              # Reference graph analyzer
│   ├── dedup_scanner.py              # Duplicate detector
│   ├── freshness_report.py           # Age distribution
│   └── health_score.py               # Aggregator
├── scripts/
│   ├── generate_report.py            # Report file writer
│   └── auto_repair.py               # Cleanup executor
├── lib/                              # Shared code (NEW)
│   ├── __init__.py
│   ├── config_loader.py              # YAML config
│   ├── sqlite_scanner.py             # SQLite utilities
│   ├── file_scanner.py               # FS utilities
│   └── health_models.py              # dataclasses
├── config/
│   └── thresholds.yaml               # Health thresholds
├── reports/
│   └── .gitkeep
├── tests/                            # Test suite (NEW)
│   ├── __init__.py
│   ├── test_integrity_scan.py
│   ├── test_bloat_detector.py
│   ├── test_orphan_finder.py
│   ├── test_dedup_scanner.py
│   ├── test_freshness_report.py
│   ├── test_health_score.py
│   └── test_integration.py
└── README.md
```

---

## 6. API Design

### 6.1 bin/integrity_scan.py

```python
def find_memory_dbs() -> list[Path]:
    """Find all SQLite DBs in the OpenClaw memory hierarchy.
    
    Searches:
        ~/.openclaw/memory/*.sqlite
        ~/.openclaw/workspace/*/memory/*.sqlite
        
    Returns:
        List of Path objects to discovered DB files
    """

def check_sqlite_integrity(db_path: Path) -> dict:
    """Run SQLite integrity_check pragma.
    
    Args:
        db_path: Path to SQLite file
        
    Returns:
        dict: {
            "path": str,
            "ok": bool,
            "issues": list[str],
            "table_count": int,
            "row_counts": dict[str, int],
        }
    """

def check_file_checksums(base_dir: Path) -> dict:
    """Verify file checksums for known-good files.
    
    Computes SHA256 for all .sqlite and .md files.
    Caches checksums in .checksums.sha256 file.
    
    Returns:
        dict: {
            "files_checked": int,
            "changed_files": list[str],
            "new_files": list[str],
            "deleted_files": list[str],
        }
    """

def integrity_scan(
    scan_dbs: bool = True,
    scan_files: bool = True,
    db_paths: list[Path] = None,
) -> dict:
    """Run full integrity scan across all memory storage.
    
    Args:
        scan_dbs: Run SQLite integrity checks (default: True)
        scan_files: Run checksum verification (default: True)
        db_paths: Override DB paths to scan
        
    Returns:
        dict: {
            "score": int,           # 0-100
            "status": str,          # healthy/warning/critical
            "issues": list[str],
            "details": {
                "db_results": list[dict],
                "file_checksum_results": dict,
            }
        }
    """
```

### 6.2 bin/bloat_detector.py

```python
def get_dir_size(path: Path, follow_symlinks: bool = False) -> int:
    """Recursively compute directory size in bytes.
    
    Args:
        path: Directory path
        follow_symlinks: Whether to follow symlinks
        
    Returns:
        int: Total bytes
    """

def get_file_counts(base_dir: Path) -> dict:
    """Count files by extension/type.
    
    Returns:
        dict: {"total": int, "md": int, "sqlite": int, "json": int, "other": int}
    """

def get_growth_rate(
    base_dir: Path,
    snapshots: int = 4,
    interval_days: int = 7,
) -> dict:
    """Estimate growth rate by comparing recent snapshots.
    
    Reads previous health reports to get historical sizes.
    
    Returns:
        dict: {
            "growth_rate_mb_per_week": float,
            "trend": "increasing" | "stable" | "decreasing",
            "projected_90d_mb": float,
        }
    """

def bloat_detection(
    base_dir: Path = None,
    include_growth: bool = True,
) -> dict:
    """Detect memory bloat across all storage layers.
    
    Args:
        base_dir: Override base directory (default: ~/.openclaw/workspace)
        include_growth: Include growth rate projection
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "total_bytes": int,
            "total_mb": float,
            "file_counts": dict,
            "growth_rate": dict | None,
            "projected_critical_date": str | None,
        }
    """
```

### 6.3 bin/orphan_finder.py

```python
def build_reference_graph(base_dir: Path) -> dict[str, set[str]]:
    """Build a graph of file references.
    
    Detects references via:
        - Obsidian-style [[wikilinks]]
        - Markdown [text](url) links
        - Cross-file content references (file name mentions)
        - SQLite foreign key relationships
    
    Returns:
        dict: {
            "referrer": {set of referenced files},
            "orphaned_files": [list of file paths with zero inbound refs],
        }
    """

def detect_orphaned_entries(
    base_dir: Path,
    reference_graph: dict = None,
) -> dict:
    """Find entries with no inbound references.
    
    Args:
        base_dir: Memory directory
        reference_graph: Pre-built graph (optional)
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "orphan_count": int,
            "total_entries": int,
            "orphan_rate": float,
            "orphaned_files": list[str],
            "orphan_types": dict[str, int],  # {"md": n, "sqlite": n, ...}
        }
    """

def find_orphans(
    base_dir: Path = None,
    min_age_days: int = 7,
) -> dict:
    """Public API — find orphaned memory entries.
    
    Args:
        base_dir: Override base directory
        min_age_days: Only flag files older than this
        
    Returns:
        dict: Full orphan detection result
    """
```

### 6.4 bin/dedup_scanner.py

```python
def token_similarity(a: str, b: str) -> float:
    """Compute token-overlap similarity.
    
    Uses Jaccard + overlap coefficient.
    
    Returns:
        float: 0.0-1.0
    """

def read_memory_entries(
    base_dir: Path,
    limit: int = 5000,
) -> list[dict]:
    """Read all memory entries for dedup comparison.
    
    Reads .md files and SQLite memories table.
    
    Returns:
        list of {"id": str, "content": str, "source": str}
    """

def scan_for_duplicates(
    base_dir: Path,
    threshold: float = 0.85,
    limit: int = 5000,
) -> dict:
    """Scan memory for duplicate/near-duplicate entries.
    
    Args:
        base_dir: Memory directory
        threshold: Similarity threshold (default: 0.85)
        limit: Max entries to scan (performance cap)
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "dup_count": int,
            "total_entries": int,
            "dup_rate": float,
            "duplicate_pairs": list[dict],  # [(id_a, id_b, similarity), ...]
        }
    """

def dedup_scan(
    base_dir: Path = None,
    threshold: float = 0.85,
) -> dict:
    """Public API for dedup scanning.
    
    Returns:
        Full dedup scan result
    """
```

### 6.5 bin/freshness_report.py

```python
def get_file_age_distribution(
    base_dir: Path,
    categories: list[str] = None,
) -> dict:
    """Compute age distribution of memory files.
    
    Categories: ["<7d", "7-30d", "30-90d", ">90d"]
    
    Returns:
        dict: {
            "total": int,
            "by_category": dict[str, int],
            "by_percentage": dict[str, float],
        }
    """

def freshness_report(
    base_dir: Path = None,
    reference_date: datetime = None,
) -> dict:
    """Generate freshness report for memory entries.
    
    Args:
        base_dir: Memory directory
        reference_date: Reference for "now" (default: now)
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "recent_7d": int,
            "recent_30d": int,
            "recent_90d": int,
            "stale": int,
            "total": int,
            "freshness_rate": float,   # 30d fresh rate
            "age_distribution": dict,
        }
    """
```

### 6.6 bin/health_score.py

```python
def aggregate_dimensions(
    integrity: dict,
    bloat: dict,
    orphans: dict,
    dedup: dict,
    freshness: dict,
) -> dict:
    """Aggregate all dimension results into overall health score.
    
    Args:
        integrity: Result from integrity_scan()
        bloat: Result from bloat_detection()
        orphans: Result from find_orphans()
        dedup: Result from dedup_scan()
        freshness: Result from freshness_report()
        
    Returns:
        dict: {
            "overall_score": float,
            "status": str,
            "dimensions": dict[str, int],  # name → score
            "weights": dict[str, float],
        }
    """

def health_score(
    base_dir: Path = None,
    run_all: bool = True,
    run_dims: list[str] = None,
) -> dict:
    """Public API — run full or partial health check.
    
    Args:
        base_dir: Override base directory
        run_all: Run all 6 dimensions (default: True)
        run_dims: Specific dimensions to run (overrides run_all)
                  Options: ["integrity", "bloat", "orphans", "dedup", "freshness", "coverage"]
        
    Returns:
        Full health report dict
    """
```

### 6.7 scripts/generate_report.py

```python
def generate_report(
    health_result: dict,
    output_dir: Path = None,
    format: str = "json",
) -> Path:
    """Generate human-readable health report file.
    
    Args:
        health_result: Result from health_score()
        output_dir: Directory for output (default: memory/health-reports/)
        format: "json" (default) or "markdown"
        
    Returns:
        Path: Path to generated report file
    """

def generate_recommendations(
    dimensions: dict[str, dict],
) -> list[Recommendation]:
    """Generate actionable recommendations from dimension scores.
    
    Returns:
        list of Recommendation dataclass instances
    """
```

### 6.8 scripts/auto_repair.py

```python
def get_auto_repair_items(
    orphan_files: list[str],
    temp_files: list[str],
    empty_files: list[str],
    dry_run: bool = True,
) -> dict:
    """Prepare auto-repair plan.
    
    Args:
        orphan_files: Files flagged as orphaned
        temp_files: Temp files (.DS_Store, etc.)
        empty_files: Empty .md files
        dry_run: Don't actually delete
        
    Returns:
        dict: {
            "items": list[str],
            "would_delete": int,
            "space_to_free_mb": float,
            "errors": list[str],
        }
    """

def execute_auto_repair(
    items: list[str],
    require_confirmation: bool = True,
) -> dict:
    """Execute auto-repair with user confirmation.
    
    Args:
        items: List of file paths to delete
        require_confirmation: Prompt user before deleting
        
    Returns:
        dict: {
            "deleted": list[str],
            "failed": list[str],
            "space_freed_mb": float,
        }
    """
```

---

## 7. Configuration Schema

```yaml
# config/thresholds.yaml

version: "1.0.0"

# Health dimension thresholds
thresholds:
  integrity:
    healthy: 100
    warning: 80
    critical: 50
  
  freshness_rate:
    healthy: 0.70    # >70% of entries updated in last 30d
    warning: 0.40
    critical: 0.20
  
  bloat_mb:
    healthy: 500     # <500MB total
    warning: 2000    # 500MB-2GB
    critical: 5000  # >2GB
  
  orphan_rate:
    healthy: 0.01   # <1%
    warning: 0.05   # 1-5%
    critical: 0.10  # >10%
  
  dedup_rate:
    healthy: 0.02   # <2%
    warning: 0.10   # 2-10%
    critical: 0.20 # >10%
  
  coverage_rate:
    healthy: 0.80   # >80% domains covered
    warning: 0.50
    critical: 0.20

# Known knowledge domains (for coverage check)
knowledge_domains:
  - 技术       # Technical / coding
  - 商业       # Business / BD
  - 创意       # Creative
  - 人际关系   # Interpersonal
  - 个人成长   # Personal growth
  - 日常       # Daily life

# Health scoring weights
weights:
  integrity:  0.30
  freshness:   0.20
  bloat:       0.15
  orphans:     0.15
  dedup:       0.10
  coverage:    0.10

# Scan settings
scan:
  max_db_size_mb: 5000       # Skip DBs larger than this
  max_file_count: 100000     # Abort if file count exceeds
  timeout_seconds: 300        # Overall scan timeout
  db_sample_size: 10000      # Max rows to sample per DB table

# Auto-repair settings
auto_repair:
  enabled: false             # Must be explicitly enabled
  require_confirmation: true # Always confirm before deleting
  remove_ds_store: true
  remove_empty_files: true
  remove_orphans: false       # Disabled by default (risky)
  min_file_age_days: 7       # Only remove files older than this
  max_archive_age_days: 90    # Purge archives older than this

# Reporting
reporting:
  summary_dir: "health-reports"
  max_reports_stored: 30     # Keep last 30 reports
  include_recommendations: true
  include_auto_repair_plan: true

# Coverage detection keywords
coverage_keywords:
  技术:
    - Python, JavaScript, API, 数据库, 代码, 架构, 部署
    - skill, agent, tool, framework
  商业:
    - 客户, 合同, 报价, 商业, 合作, BD, 销售, 收入
    - business, deal, contract, revenue
  创意:
    - 创意, 设计, 想法, 灵感, 创新
    - creative, idea, design, innovation
  人际关系:
    - 团队, 沟通, 合作, 家人, 朋友, 会议
    - team, meeting, communication, collaboration
  个人成长:
    - 学习, 目标, 计划, 反思, 成长
    - learning, goal, plan, reflection, growth
  日常:
    - 今天, 明天, 会议, 日程, 任务
    - today, tomorrow, schedule, task, reminder
```

---

## 8. B-Layer SQLite Schema (What We Inspect)

```sql
-- Standard OpenClaw B-layer schema (what we inspect, not modify)
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    score INTEGER DEFAULT 50,
    tag TEXT DEFAULT 'context',
    source TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS dreaming_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_content_hash TEXT,
    action TEXT,
    score INTEGER,
    ts TEXT
);

-- Schema version tracking (for compatibility)
CREATE TABLE IF NOT EXISTS schema_info (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## 9. Edge Cases & Error Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| No memory directory exists | Return "healthy" score 100, log info |
| SQLite DB is locked | Retry 3x with 1s delay, then skip + warn |
| SQLite DB is corrupted | Flag as critical, include in report issues |
| DB is >5GB | Skip full scan, use sampling, warn |
| No entries at all (fresh install) | Return "healthy" score 100, coverage=0% |
| All entries are stale (>90d) | Freshness=0%, flag as critical |
| 100% duplicate rate | Dedup=100%, suggest running dreaming-optimizer |
| Circular wiki links | Graph cycle detection, exclude from orphan count |
| File deleted during scan | Catch FileNotFoundError, skip, continue |
| Non-UTF8 file content | Decode with errors='replace', log warning |
| Permission denied on file | Log error, skip file, continue |
| Report dir doesn't exist | Create it before writing |
| Auto-repair enabled but no items | Log "Nothing to repair", exit 0 |
| Orphan detection expensive (>5min) | Abort with timeout, partial results |

---

## 10. Testing Strategy

### 10.1 Unit Tests

**test_integrity_scan.py:**
- `test_ok_db_returns_100`: Healthy DB → score 100
- `test_corrupted_db_returns_0`: Corrupted DB → score 0
- `test_missing_db_skipped`: Non-existent DB → handled gracefully
- `test_multiple_dbs_aggregated`: Multiple DBs with one bad → weighted

**test_bloat_detector.py:**
- `test_under_500mb_healthy`: <500MB → score 100
- `test_500mb_to_2gb_warning`: 500MB-2GB → score 60
- `test_over_2gb_critical`: >2GB → score 20
- `test_empty_dir_returns_0`: Empty directory → score 100, size=0

**test_orphan_finder.py:**
- `test_no_orphans_healthy`: 0 orphans → score 100
- `test_orphans_rate_3pct_warning`: 3% → score 70
- `test_orphans_rate_10pct_critical`: 10% → score 30
- `test_wikilink_reference_detected`: [[file]] → not orphaned

**test_dedup_scanner.py:**
- `test_identical_content_flagged`: Exact dup → flagged
- `test_different_content_not_flagged`: No overlap → not flagged
- `test_dup_rate_calculation`: Verify rate = dups/total

**test_freshness_report.py:**
- `test_all_recent_healthy`: All <30d → score 100
- `test_mixed_ages_correct_distribution`: Mixed → correct counts
- `test_stale_memory_critical`: All >90d → score 20

**test_health_score.py:**
- `test_weighted_average_correct`: Known weights → verify calc
- `test_status_thresholds`: 80/50 boundary conditions
- `test_all_dimensions_aggregated`: All 5 present → full score

### 10.2 Integration Tests

**test_integration.py:**
- `test_full_health_check_runs`: health_check.sh → output exists
- `test_report_file_created`: health-report-YYYY-MM-DD.json exists
- `test_auto_repair_plan_generated`: plan file exists when auto-repair enabled
- `test_empty_memory_graceful`: No memory dir → healthy 100, no crash
- `test_cron_safe`: No interactive prompts in cron mode

---

## 11. Known Issues

| Issue | Severity | Workaround |
|-------|----------|------------|
| Orphan detection is simplified (no full graph) | Medium | Uses file-name mention detection, not full ref graph |
| Coverage detection is keyword-based only | Low | Works for MVP, LLM-based in v1.1 |
| Growth rate requires prior reports | Medium | First run shows "unknown", improves over time |
| SQLite pragma integrity_check is not comprehensive | Low | Supplement with row count + table enumeration |
| Auto-repair disabled by default (require_confirmation=True) | Low | By design, safety first |
| No support for remote/nfs memory paths | Low | Local filesystem only for v1.0 |

---

## 12. Development Task Breakdown

See: `~/.openclaw/workspace/skills/TODO-20260417.md`

**Priority Order:**
1. `lib/` shared utilities (config_loader, sqlite_scanner, file_scanner, health_models)
2. `bin/health_score.py` orchestration (aggregator)
3. `bin/bloat_detector.py` enhanced (add growth rate)
4. `bin/orphan_finder.py` enhanced (proper reference graph)
5. `bin/integrity_scan.py` enhanced (add checksum tracking)
6. `bin/dedup_scanner.py` enhanced (use lib utilities)
7. `bin/freshness_report.py` enhanced (add age distribution)
8. `scripts/generate_report.py` enhanced (recommendations engine)
9. `scripts/auto_repair.py` enhanced (safer delete)
10. `config/thresholds.yaml` already exists — verify completeness
11. `tests/` test suite
12. `README.md` documentation

---

## 13. Performance Considerations

### 13.1 Scan Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Integrity scan | <30s for 10 DBs | PRAGMA integrity_check is fast |
| Bloat detection | <10s for 100K files | Use os.walk with stat caching |
| Orphan detection | <60s for 10K files | O(n²) wikilink parse — limit to recent files |
| Dedup scan | <120s for 5K entries | O(n²) comparison — batch for large sets |
| Full health scan | <5 minutes | All dimensions combined |

### 13.2 Optimization Strategies

**Integrity Scan:**
- Run `PRAGMA integrity_check` only on DBs modified in last 7 days
- Skip DBs >5GB (too large, use sampling instead)
- Parallelize DB scans with `concurrent.futures`

**Bloat Detection:**
- Use `os.scandir()` instead of `rglob()` for faster traversal
- Cache dir size in `.bloat_cache.json`
- Incremental update: only recount changed files

**Orphan Detection:**
- Limit content search to files <1MB (skip large files)
- Use regex pre-compilation for wikilink detection
- Build reference graph incrementally

**Dedup Scan:**
- Pre-filter with exact hash match before similarity
- Use MinHash for near-duplicate detection at scale
- Limit comparison to last 90 days of entries

### 13.3 Caching Strategy

```python
# Health check caching
.health_cache/
  bloat_cache.json      # Dir size cache
  checksum_cache.json    # File checksum cache
  orphan_graph.json     # Reference graph cache

# Cache invalidation: regenerate if any file mtime > cache mtime
```

---

## 14. Security & Safety

### 14.1 Auto-Repair Safety Rules

| Rule | Rationale |
|------|----------|
| `--auto-repair` flag required | Opt-in prevents accidental deletion |
| `--dry-run` always available | Preview before commit |
| Confirmation prompt | 5-second countdown before action |
| `require_confirmation: true` in config | Default-safe behavior |
| No network deletions | Only local filesystem |
| No deletion of non-temp files | Only .DS_Store, empty files, confirmed orphans |

### 14.2 Data Integrity Rules

| Rule | Implementation |
|------|----------------|
| Never delete from B-layer directly | Only archive, never hard delete |
| All deletions are reversible | Archived files can be restored |
| Checksum before/after | Verify file integrity after operations |
| Transaction rollback | SQLite transactions for multi-step operations |

### 14.3 Privacy

- All checks are local — no network calls
- Checksums computed client-side only
- Report files stay in user's workspace
- No third-party data sharing

---

## 15. Monitoring & Alerting

### 15.1 Health Score Metrics

```python
# Key operational metrics
METRICS = {
    "health_score_overall": gauge,          # 0-100
    "health_score_integrity": gauge,
    "health_score_bloat": gauge,
    "health_score_orphans": gauge,
    "health_score_dedup": gauge,
    "health_score_freshness": gauge,
    "health_score_coverage": gauge,
    "scan_duration_seconds": histogram,
    "db_count": gauge,
    "file_count": gauge,
    "orphan_count": gauge,
    "dup_count": gauge,
}
```

### 15.2 Alert Thresholds

| Condition | Severity | Action |
|-----------|----------|--------|
| Overall score <50 | CRITICAL | Page user immediately |
| Integrity score = 0 | CRITICAL | DB corruption — data loss risk |
| Bloat >2GB | WARNING | Run dreaming-optimizer |
| Orphan rate >5% | WARNING | Review orphaned files |
| Dedup rate >10% | WARNING | Run dedup |
| Freshness <40% | WARNING | Memory is stale |

### 15.3 Logging

| Level | Use Case |
|-------|----------|
| DEBUG | File paths checked, checksum values, SQL queries |
| INFO | Scan phase transitions, dimension scores, final report |
| WARNING | Config missing, partial failures, thresholds approached |
| ERROR | DB corruption, permission denied, scan failures |

---

## 16. Deployment & ClawHub

### 16.1 Publishing Checklist

- [ ] SKILL.md complete and accurate
- [ ] DESIGN.md >1000 lines
- [ ] All bin/*.sh have executable permissions
- [ ] `bin/health_check.sh --help` works
- [ ] Tests pass: `pytest tests/ -v`
- [ ] README.md with usage examples
- [ ] Pricing tiers documented
- [ ] Health score badge design
- [ ] Demo screenshots / video

### 16.2 Version Policy

Follows SemVer (MAJOR.MINOR.PATCH):
- MAJOR: Score formula changes, breaking config format
- MINOR: New dimensions, new health checks
- PATCH: Bug fixes, threshold adjustments

### 16.3 Migration Guide

When thresholds.yaml format changes:
1. Version the config file: `thresholds.v1.yaml`
2. Provide migration script: `migrate_thresholds.py`
3. Support loading old format for 2 minor versions

---

## 17. Future Roadmap

| Version | Feature | Priority |
|---------|---------|----------|
| v1.1 (Pro) | 90-day health history + trend charts | P1 |
| v1.1 (Pro) | Weekly digest via 飞书/email | P1 |
| v1.1 | Pre-upgrade compatibility check mode | P1 |
| v1.2 (Team) | Cross-agent health comparison | P2 |
| v1.2 | Team-wide health dashboard | P2 |
| v1.2 | Custom threshold profiles | P2 |
| v1.3 | Predictive bloat alerts (ML) | P3 |
| v1.3 | Auto-defragment SQLite | P3 |

### Bundle Opportunity

`dreaming-optimizer Pro + memory-health-check Pro` = **$17.90/mo**
- Shared "Memory Suite" branding
- Unified health dashboard
- Cross-feature recommendations (e.g., "Run optimizer to fix dedup issue")

---

*End of DESIGN.md — memory-health-check v1.0.0*
