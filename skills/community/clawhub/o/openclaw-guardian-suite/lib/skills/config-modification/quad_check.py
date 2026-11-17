#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
quad_check.py — 四联校验状态机
==============================

功能:
- 顺序执行四阶段校验: Schema → Diff → Rollback → Health
- 任意失败则停止并返回失败结果
- 支持单独执行任意阶段

使用:
  from quad_check import QuadCheckStateMachine, CheckPhase, CheckResult
  
  qc = QuadCheckStateMachine()
  results = qc.run_all("/path/to/config.json")
"""

import json
import subprocess
import os
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional, Callable
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path.home() / ".openclaw"
WORKSPACE_DIR = CONFIG_DIR / "workspace"
LOG_DIR = CONFIG_DIR / "logs"
SNAPSHOT_DIR = CONFIG_DIR / "backup" / "snapshots"


class CheckPhase(Enum):
    SCHEMA = "schema"       # JSON Schema 校验
    DIFF = "diff"           # 变更差异分析
    ROLLBACK = "rollback"  # 回滚能力验证
    HEALTH = "health"       # Gateway 健康检查


@dataclass
class CheckResult:
    """单个校验阶段的结果"""
    phase: str
    passed: bool
    message: str
    details: Optional[dict] = None
    duration_ms: Optional[int] = None
    timestamp: Optional[str] = None
    
    def to_dict(self):
        return {
            "phase": self.phase,
            "passed": self.passed,
            "message": self.message,
            "details": self.details or {},
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }


class QuadCheckStateMachine:
    """
    四联校验状态机
    
    执行顺序: schema → diff → rollback → health
    任意失败则停止，不执行后续阶段
    """
    
    PHASE_ORDER = [
        CheckPhase.SCHEMA,
        CheckPhase.DIFF,
        CheckPhase.ROLLBACK,
        CheckPhase.HEALTH,
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.results: list[CheckResult] = []
        self._start_time: Optional[datetime] = None
    
    def run_all(self, config_path: Optional[str] = None) -> list[CheckResult]:
        """
        运行全部四阶段校验
        
        Returns:
            list[CheckResult] - 每个阶段的结果
        """
        self._start_time = datetime.now()
        self.results = []
        
        target_path = config_path or self.config_path
        if not target_path:
            raise ValueError("config_path is required")
        
        for phase in self.PHASE_ORDER:
            result = self._run_phase(phase, target_path)
            self.results.append(result)
            
            if not result.passed:
                self._log("ERROR", f"Phase {phase.value} failed, stopping cascade")
                break
        
        return self.results
    
    def run_phase(self, phase: CheckPhase, config_path: Optional[str] = None) -> CheckResult:
        """单独运行某个阶段"""
        target_path = config_path or self.config_path
        if not target_path:
            raise ValueError("config_path is required")
        
        return self._run_phase(phase, target_path)
    
    def _run_phase(self, phase: CheckPhase, config_path: str) -> CheckResult:
        """执行单个校验阶段"""
        import time
        start = time.time()
        
        if phase == CheckPhase.SCHEMA:
            result = self._check_schema(config_path)
        elif phase == CheckPhase.DIFF:
            result = self._check_diff(config_path)
        elif phase == CheckPhase.ROLLBACK:
            result = self._check_rollback(config_path)
        elif phase == CheckPhase.HEALTH:
            result = self._check_health(config_path)
        else:
            result = CheckResult(
                phase=phase.value,
                passed=False,
                message=f"Unknown phase: {phase}"
            )
        
        duration_ms = int((time.time() - start) * 1000)
        result.duration_ms = duration_ms
        result.timestamp = datetime.now().isoformat()
        
        self._log("INFO" if result.passed else "ERROR", 
                  f"{phase.value}: {'✅' if result.passed else '❌'} {result.message}")
        
        return result
    
    def _check_schema(self, config_path: str) -> CheckResult:
        """
        阶段1: Schema 校验
        - JSON 语法验证
        - 必需字段检查
        """
        try:
            # 1. JSON 语法
            with open(config_path, 'r') as f:
                data = json.load(f)
            
            # 2. 必需字段检查 (针对 openclaw.json)
            # 实际结构是 meta, env, wizard 等，不是顶层直接字段
            if "openclaw.json" in config_path or config_path.endswith("openclaw.json"):
                # 检查顶层结构是否存在有效配置
                if not data or not any(k in data for k in ["meta", "env", "agents", "models"]):
                    return CheckResult(
                        phase=CheckPhase.SCHEMA.value,
                        passed=False,
                        message="Invalid openclaw.json structure",
                        details={"keys_found": list(data.keys()) if data else []}
                    )
            
            return CheckResult(
                phase=CheckPhase.SCHEMA.value,
                passed=True,
                message="Schema validation passed",
                details={"fields_count": len(data), "file": config_path}
            )
            
        except json.JSONDecodeError as e:
            return CheckResult(
                phase=CheckPhase.SCHEMA.value,
                passed=False,
                message=f"JSON syntax error: {e}",
                details={"error": str(e)}
            )
        except FileNotFoundError:
            return CheckResult(
                phase=CheckPhase.SCHEMA.value,
                passed=False,
                message=f"File not found: {config_path}",
                details={"path": config_path}
            )
        except Exception as e:
            return CheckResult(
                phase=CheckPhase.SCHEMA.value,
                passed=False,
                message=f"Schema check error: {e}",
                details={"error": str(e)}
            )
    
    def _check_diff(self, config_path: str) -> CheckResult:
        """
        阶段2: Diff 校验
        - 与上一个快照对比
        - 输出变更摘要
        """
        try:
            # 查找最新快照
            if not SNAPSHOT_DIR.exists():
                return CheckResult(
                    phase=CheckPhase.DIFF.value,
                    passed=True,
                    message="No snapshots found, skipping diff",
                    details={"reason": "first_config"}
                )
            
            snapshots = sorted(SNAPSHOT_DIR.iterdir(), reverse=True)
            if not snapshots:
                return CheckResult(
                    phase=CheckPhase.DIFF.value,
                    passed=True,
                    message="No snapshots found, skipping diff",
                    details={"reason": "first_config"}
                )
            
            latest_snapshot = snapshots[0]
            
            # 查找对应的快照文件
            config_name = os.path.basename(config_path)
            snap_file = latest_snapshot / config_name
            
            if not snap_file.exists():
                # 子代理配置可能在 agents/ 子目录
                if "agents/" in config_path:
                    agent_name = config_path.split("agents/")[1].split("/")[0]
                    snap_file = latest_snapshot / "agents" / agent_name / config_name
            
            if not snap_file.exists():
                return CheckResult(
                    phase=CheckPhase.DIFF.value,
                    passed=True,
                    message="No previous snapshot found, skipping diff",
                    details={"config": config_name}
                )
            
            # 读取两个版本
            with open(config_path, 'r') as f:
                current = json.load(f)
            with open(snap_file, 'r') as f:
                previous = json.load(f)
            
            # 简单对比
            changes = self._compute_diff(previous, current)
            
            return CheckResult(
                phase=CheckPhase.DIFF.value,
                passed=True,
                message=f"Diff computed: {len(changes.get('changed', []))} changes",
                details=changes
            )
            
        except Exception as e:
            return CheckResult(
                phase=CheckPhase.DIFF.value,
                passed=False,
                message=f"Diff check error: {e}",
                details={"error": str(e)}
            )
    
    def _compute_diff(self, old: dict, new: dict, path: str = "") -> dict:
        """计算两个 JSON 对象的差异"""
        diff = {"added": [], "removed": [], "changed": []}
        
        all_keys = set(old.keys()) | set(new.keys())
        
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key
            
            if key not in old:
                diff["added"].append(current_path)
            elif key not in new:
                diff["removed"].append(current_path)
            elif old[key] != new[key]:
                # 深入比较
                if isinstance(old[key], dict) and isinstance(new[key], dict):
                    sub_diff = self._compute_diff(old[key], new[key], current_path)
                    diff["added"].extend(sub_diff.get("added", []))
                    diff["removed"].extend(sub_diff.get("removed", []))
                    diff["changed"].extend(sub_diff.get("changed", []))
                else:
                    diff["changed"].append({
                        "path": current_path,
                        "old": str(old[key])[:100],
                        "new": str(new[key])[:100]
                    })
        
        return diff
    
    def _check_rollback(self, config_path: str) -> CheckResult:
        """
        阶段3: Rollback 能力验证
        - 检查快照是否存在
        - 检查回滚脚本是否可用
        """
        try:
            # 1. 检查快照目录
            if not SNAPSHOT_DIR.exists():
                return CheckResult(
                    phase=CheckPhase.ROLLBACK.value,
                    passed=False,
                    message="Snapshot directory does not exist",
                    details={"path": str(SNAPSHOT_DIR)}
                )
            
            snapshots = list(SNAPSHOT_DIR.iterdir())
            if not snapshots:
                return CheckResult(
                    phase=CheckPhase.ROLLBACK.value,
                    passed=False,
                    message="No snapshots available for rollback",
                    details={"count": 0}
                )
            
            # 2. 检查回滚脚本
            rollback_script = WORKSPACE_DIR / ".lib" / "config-rollback-guard.py"
            if not rollback_script.exists():
                return CheckResult(
                    phase=CheckPhase.ROLLBACK.value,
                    passed=False,
                    message="Rollback script not found",
                    details={"script": str(rollback_script)}
                )
            
            # 3. 检查最新快照是否包含当前配置文件
            latest = sorted(snapshots, reverse=True)[0]
            config_name = os.path.basename(config_path)
            has_backup = (latest / config_name).exists()
            
            return CheckResult(
                phase=CheckPhase.ROLLBACK.value,
                passed=True,
                message="Rollback capability verified",
                details={
                    "snapshots_count": len(snapshots),
                    "latest_snapshot": latest.name,
                    "has_backup": has_backup,
                    "rollback_script": str(rollback_script)
                }
            )
            
        except Exception as e:
            return CheckResult(
                phase=CheckPhase.ROLLBACK.value,
                passed=False,
                message=f"Rollback check error: {e}",
                details={"error": str(e)}
            )
    
    def _check_health(self, config_path: str) -> CheckResult:
        """
        阶段4: Health 检查
        - Gateway 可达性
        - 配置文件可写性
        """
        try:
            # 1. 检查 Gateway 健康
            try:
                result = subprocess.run(
                    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                     "http://127.0.0.1:18789/health"],
                    timeout=5, capture_output=True, text=True
                )
                gateway_ok = result.stdout.strip() == "200"
                gateway_code = result.stdout.strip()
            except Exception:
                gateway_ok = False
                gateway_code = "error"
            
            # 2. 检查配置文件可写
            config_file = Path(config_path)
            writable = os.access(config_file, os.W_OK) if config_file.exists() else False
            
            if not gateway_ok:
                return CheckResult(
                    phase=CheckPhase.HEALTH.value,
                    passed=False,
                    message=f"Gateway health check failed (HTTP {gateway_code})",
                    details={"gateway_code": gateway_code, "writable": writable}
                )
            
            if not writable:
                return CheckResult(
                    phase=CheckPhase.HEALTH.value,
                    passed=False,
                    message=f"Config file not writable: {config_path}",
                    details={"path": config_path, "writable": False}
                )
            
            return CheckResult(
                phase=CheckPhase.HEALTH.value,
                passed=True,
                message="Health check passed",
                details={"gateway": "healthy", "writable": True}
            )
            
        except Exception as e:
            return CheckResult(
                phase=CheckPhase.HEALTH.value,
                passed=False,
                message=f"Health check error: {e}",
                details={"error": str(e)}
            )
    
    def _log(self, level: str, msg: str):
        """写日志"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] [{level}] quad_check: {msg}"
        print(entry)
        
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / "quad-check.log"
        with open(log_file, "a") as f:
            f.write(entry + "\n")
    
    def get_summary(self) -> dict:
        """获取校验摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        total_time = sum(r.duration_ms or 0 for r in self.results)
        
        return {
            "total_phases": total,
            "passed": passed,
            "failed": failed,
            "success_rate": f"{passed/total*100:.1f}%" if total > 0 else "0%",
            "total_duration_ms": total_time,
            "results": [r.to_dict() for r in self.results]
        }


# CLI 接口
if __name__ == "__main__":
    import sys
    
    config_path = sys.argv[1] if len(sys.argv) > 1 else str(CONFIG_DIR / "openclaw.json")
    
    qc = QuadCheckStateMachine()
    results = qc.run_all(config_path)
    
    summary = qc.get_summary()
    print("\n=== Quad Check Summary ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # Exit code: 0 = all passed, 1 = any failed
    sys.exit(0 if summary["failed"] == 0 else 1)
