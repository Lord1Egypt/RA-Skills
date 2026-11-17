# 详细参考 - go-security-vuln-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版Go漏洞调用路径深度分析"""

import json
import subprocess
from collections import defaultdict

class VulnCallPathAnalyzer:
    """漏洞调用路径分析器"""

    def __init__(self):
        self.vulns = []
        self.findings = []

    def run_govulncheck(self, path="."):
        """运行govulncheck并收集结果"""
        result = subprocess.run(
            ["govulncheck", "-json", "./..."],
            capture_output=True,
            text=True,
            cwd=path
        )

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            try:
                data = json.loads(line)
                if "osv" in data:
                    self.vulns.append(data["osv"])
                elif "finding" in data:
                    self.findings.append(data["finding"])
            except json.JSONDecodeError:
                continue

    def analyze_call_paths(self):
        """分析漏洞调用路径"""
        analysis = []

        for finding in self.findings:
            osv_id = finding.get("osv", "")
            trace = finding.get("trace", [])

            is_called = len(trace) > 1 and trace[1].get("function")

            if is_called:
                call_path = []
                for frame in trace:
                    call_path.append({
                        "function": frame.get("function", "unknown"),
                        "module": frame.get("module", ""),
                        "version": frame.get("version", ""),
                        "file": frame.get("filename", ""),
                        "line": frame.get("line", 0)
                    })

                vuln_info = next((v for v in self.vulns if v.get("id") == osv_id), {})

                analysis.append({
                    "vulnerability_id": osv_id,
                    "severity": vuln_info.get("database_specific", {}).get("severity", "UNKNOWN"),
                    "summary": vuln_info.get("summary", "无描述"),
                    "is_called": True,
                    "call_path": call_path,
                    "entry_point": call_path[-1] if call_path else None,
                    "vulnerable_function": call_path[0] if call_path else None,
                    "fix_version": self._get_fix_version(vuln_info)
                })
            else:
                analysis.append({
                    "vulnerability_id": osv_id,
                    "is_called": False,
                    "note": "漏洞存在于依赖中但未被代码调用"
                })

        return analysis

    def _get_fix_version(self, vuln_info):
        """获取修复版本"""
        affected = vuln_info.get("affected", [{}])
        if affected:
            ranges = affected[0].get("ranges", [{}])
            if ranges:
                events = ranges[0].get("events", [])
                for event in reversed(events):
                    if "fixed" in event:
                        return event["fixed"]
        return "暂无修复版本"

    def generate_report(self):
        """生成分析报告"""
        analysis = self.analyze_call_paths()

        called = [a for a in analysis if a.get("is_called")]
        not_called = [a for a in analysis if not a.get("is_called")]

        report = {
            "summary": {
                "total_vulnerabilities": len(analysis),
                "called_vulnerabilities": len(called),
                "not_called_vulnerabilities": len(not_called)
            },
            "high_priority": [a for a in called if a.get("severity") in ["HIGH", "CRITICAL"]],
            "all_called": called,
            "not_called": not_called
        }

        return report

if __name__ == "__main__":
    analyzer = VulnCallPathAnalyzer()
    analyzer.run_govulncheck()

    import json
    report = analyzer.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

## 代码示例 (bash)

```bash
#!/bin/bash
echo "=== Go专业版双重安全扫描 ==="
echo "项目: $(basename "$(pwd)")"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

install_tools() {
    if ! command -v govulncheck &> /dev/null; then
        echo "安装govulncheck..."
        go install golang.org/x/vuln/cmd/govulncheck@latest
    fi
    if ! command -v gosec &> /dev/null; then
        echo "安装gosec..."
        go install securego/gosec/v2/cmd/gosec@latest
    fi
}
install_tools

echo "============================================"
echo "1. 依赖漏洞扫描 (govulncheck)"
echo "============================================"
govulncheck -json ./... > /tmp/vuln-deps.json 2>/dev/null

DEP_VULNS=$(jq -s '[.[] | select(.osv)] | length' /tmp/vuln-deps.json 2>/dev/null || echo "0")
CALLED_VULNS=$(jq -s '[.[] | select(.finding and .finding.trace[1])] | length' /tmp/vuln-deps.json 2>/dev/null || echo "0")
echo "  依赖漏洞总数: ${DEP_VULNS}"
echo "  已调用漏洞: ${CALLED_VULNS}"

echo ""
echo "============================================"
echo "2. 代码安全扫描 (gosec)"
echo "============================================"
gosec -json -quiet ./... > /tmp/vuln-code.json 2>/dev/null

CODE_ISSUES=$(jq '.Issues | length' /tmp/vuln-code.json 2>/dev/null || echo "0")
echo "  代码安全问题: ${CODE_ISSUES}"

echo ""
echo "  按严重级别:"
HIGH=$(jq '[.Issues[] | select(.severity == "HIGH")] | length' /tmp/vuln-code.json 2>/dev/null || echo "0")
MEDIUM=$(jq '[.Issues[] | select(.severity == "MEDIUM")] | length' /tmp/vuln-code.json 2>/dev/null || echo "0")
LOW=$(jq '[.Issues[] | select(.severity == "LOW")] | length' /tmp/vuln-code.json 2>/dev/null || echo "0")
echo "    HIGH: ${HIGH}"
echo "    MEDIUM: ${MEDIUM}"
echo "    LOW: ${LOW}"

echo ""
echo "  按CWE分类:"
jq -r '.Issues[] | .details.CWE.ID' /tmp/vuln-code.json 2>/dev/null | sort | uniq -c | sort -rn | head -10

echo ""
echo "============================================"
echo "扫描完成"
echo "  依赖漏洞: ${DEP_VULNS} (已调用: ${CALLED_VULNS})"
echo "  代码问题: ${CODE_ISSUES} (HIGH: ${HIGH})"
echo "============================================"
```

