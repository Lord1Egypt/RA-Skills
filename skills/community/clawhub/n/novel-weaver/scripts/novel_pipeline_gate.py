#!/usr/bin/env python3
"""
Pipeline Gate — 流程门禁系统
状态管理与阶段锁定，防止跳过必要步骤。
"""
import json, sys, os
from pathlib import Path

GATES = [
    "outline_causality",
    "sub_causality",
    "chapter_finalized",
    "fidelity",
    "ending_verify",
]
PHASES = ["setup", "stage1_init", "stage1_done", "writing", "stage3_ready", "complete"]

def gate_path(state_path):
    return Path(state_path).parent / ".workbuddy" / "gate_state.json"

def load_gates(state_path):
    gp = gate_path(state_path)
    if gp.exists():
        return json.loads(gp.read_text(encoding="utf-8-sig"))
    return {}

def save_gates(state_path, gates):
    gp = gate_path(state_path)
    gp.parent.mkdir(parents=True, exist_ok=True)
    gp.write_text(json.dumps(gates, ensure_ascii=False, indent=2), encoding="utf-8")

def pass_gate(state_path, gate_name):
    gates = load_gates(state_path)
    gates[gate_name] = "PASS"
    save_gates(state_path, gates)
    print(f"[门禁] {gate_name} [OK] PASS")

def require_gate(state_path, gate_name):
    gates = load_gates(state_path)
    status = gates.get(gate_name, "PENDING")
    if status != "PASS":
        print(f"[门禁] {gate_name} [FAIL] BLOCKED (当前={status})")
        sys.exit(1)
    print(f"[门禁] {gate_name} [OK] 通过")

def status(state_path):
    gates = load_gates(state_path)
    sp = Path(state_path)
    phase = "unknown"
    if sp.exists():
        data = json.loads(sp.read_text(encoding="utf-8-sig"))
        phase = data.get("meta", {}).get("current_phase", "unknown")
    print(f"[门禁状态] 当前阶段: {phase}")
    for g in GATES:
        s = gates.get(g, "PENDING")
        icon = "[OK]" if s == "PASS" else "[_]"
        print(f"  {icon} {g}: {s}")

def set_phase(state_path, new_phase):
    sp = Path(state_path)
    if not sp.exists():
        print(f"[错误] novel_state.json 不存在: {state_path}")
        sys.exit(1)
    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    if "meta" not in data:
        data["meta"] = {}
    # 门禁检查：关键阶段转换必须通过对应门禁
    if new_phase == "writing":
        require_gate(state_path, "outline_causality")
        require_gate(state_path, "sub_causality")
    elif new_phase == "stage3_ready":
        require_gate(state_path, "fidelity")
        require_gate(state_path, "ending_verify")
    data["meta"]["current_phase"] = new_phase
    sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[阶段] → {new_phase}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python novel_pipeline_gate.py <status|pass|require|set-phase> <state_path> [gate_name|phase]")
        sys.exit(1)
    cmd = sys.argv[1]
    state_path = sys.argv[2]
    if cmd == "status":
        status(state_path)
    elif cmd == "pass":
        pass_gate(state_path, sys.argv[3])
    elif cmd == "require":
        require_gate(state_path, sys.argv[3])
    elif cmd == "set-phase":
        set_phase(state_path, sys.argv[3])
    else:
        print(f"[错误] 未知命令: {cmd}")
