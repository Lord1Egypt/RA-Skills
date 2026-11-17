# Output Format Reference — JSON Schema v2.1

> `audit.py --format json` 输出的完整字段定义。

## 顶层结构

```json
{
  "schema_version": "2.0",
  "scanner": "lz-skill-vetter-plus",
  "scanner_version": "2.1.0",
  "scan_time": "2026-08-19T10:30:00+08:00",
  "skill_path": "/absolute/path/to/skill",
  "skill_name": "skill-name",
  "summary": { ... },
  "findings": [ ... ],
  "verdict": "✅ SAFE TO INSTALL",
  "verdict_code": "ok"
}
```

---

## `summary` 字段

```json
{
  "files_scanned": 12,
  "total_lines_scanned": 1234,
  "total_findings": 5,
  "by_severity": {
    "critical": 0,
    "high": 2,
    "medium": 1,
    "low": 1,
    "info": 1
  },
  "by_category": {
    "code_execution": 0,
    "credentials": 2,
    "quality": 3
  }
}
```

---

## `findings[]` 字段

每条 finding：

```json
{
  "id": "SEC-CRED-001",
  "severity": "critical",
  "category": "credentials",
  "name": "硬编码 API key/secret/token",
  "file": "scripts/run.py",
  "line": 8,
  "match": "api_key = \"ghp_***\"",
  "context": "api_key = \"ghp_***\"",
  "description": "代码中硬编码的凭据字符串，疑似泄露"
}
```

### 字段含义

| 字段 | 类型 | 含义 |
|---|---|---|
| `id` | string | 模式 ID（如 `SEC-CRED-001`） |
| `severity` | enum | `critical`/`high`/`medium`/`low`/`info` |
| `category` | string | 类别（security/performance/quality + 子类） |
| `name` | string | 简短中文名 |
| `file` | string | 相对路径（相对 skill 根） |
| `line` | int | 行号（0 = 文件级 finding） |
| `match` | string | 命中的字符串（最长 80 字符） |
| `context` | string | 上下文行（最长 120 字符） |
| `description` | string | 为什么危险（可空） |

---

## `verdict` 计算规则

```
max(critical) > 0     → ❌ DO NOT INSTALL
max(high) > 0         → ⚠️ INSTALL WITH CAUTION
max(medium) > 0       → ⚠️ REVIEW MEDIUM ISSUES
max(low/info) > 0     → ✅ SAFE TO INSTALL (minor notes)
无任何命中            → ✅ SAFE TO INSTALL
```

---

## `--exit-code` 退出码

| 退出码 | 含义 |
|---|---|
| `0` | 无 critical/high（pass） |
| `1` | 有 medium（warning） |
| `2` | 有 critical 或 high（fail） |

CI 用法：

```yaml
# .github/workflows/skill-audit.yml
- name: Audit skill
  run: |
    python3 lz-skill-vetter-plus/scripts/audit.py . --exit-code
```

非零退出码会中断 CI。

---

## CI 集成示例

### GitHub Actions

```yaml
name: Skill Audit
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pyyaml
      - name: Run lz-skill-vetter-plus
        run: |
          python3 .openclaw/skills/lz-skill-vetter-plus/scripts/audit.py \
            --format json \
            --exit-code \
            > audit-report.json
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: skill-audit-report
          path: audit-report.json
      - name: Fail on critical/high
        run: |
          python3 -c "
          import json, sys
          r = json.load(open('audit-report.json'))
          s = r['summary']['by_severity']
          if s['critical'] > 0 or s['high'] > 0:
              sys.exit(1)
          "
```

### 本地批量审计

```bash
for skill in ~/.openclaw/workspace/skills/*/; do
  echo "=== $(basename "$skill") ==="
  python3 ~/.openclaw/workspace/skills/lz-skill-vetter-plus/scripts/audit.py \
    "$skill" --severity medium --quiet
done
```

### JSON 解析（jq）

```bash
# 仅看 critical 命中
python3 audit.py . --format json --quiet \
  | jq '.findings[] | select(.severity=="critical") | {id, file, line, name}'

# 统计每个类别的 finding 数
python3 audit.py . --format json --quiet \
  | jq '.summary.by_category'

# 输出 markdown 表格
python3 audit.py . --format json --quiet \
  | jq -r '.findings[] | "| \(.severity) | \(.id) | \(.file):\(.line) | \(.name) |"'
```

---

## Schema 版本演进

| 版本 | 日期 | 变更 |
|---|---|---|
| 2.1.0 | 2026-08-19 | 修 9 个问题：original_severity bug / .key 词边界 / QUAL-STRUCT-002 实现 / 版本命名漂移清理 |
| 2.0.1 | 2026-08-19 | 3 个误判修复 + severity-cap 机制 |
| 2.0 | 2026-08-19 | 初版（v2.0.0 release） |

后续版本必须保持向后兼容——新增字段用 optional，废弃字段保留 2 版本过渡。