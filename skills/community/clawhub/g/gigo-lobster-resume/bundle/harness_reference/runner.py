"""端到端 runner 样板：从 task 目录到 report 一条龙。

研发的产品代码应基于此结构改造，集成 OpenClaw 现有的 gateway_client、
checkpoint、score_uploader 等模块。
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import time
from pathlib import Path

import yaml


def load_check_py(task_dir: Path):
    spec = importlib.util.spec_from_file_location(
        f"check_{task_dir.name}", task_dir / "check.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate


def run_one_task(task_dir: Path, agent_runner, judge_client) -> dict:
    """
    agent_runner: callable(workdir, prompt, shell_shim, timeout) -> transcript dict
    judge_client: JudgeClient 实例
    """
    cfg = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
    prompt = (task_dir / "prompt.md").read_text(encoding="utf-8")
    workdir = Path(tempfile.mkdtemp(prefix=f"eval_{cfg['id']}_"))
    setup = task_dir / "setup"
    if setup.exists():
        shutil.copytree(setup, workdir, dirs_exist_ok=True)

    try:
        from harness_reference.shell_shim import ShellShim
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from harness_reference.shell_shim import ShellShim
    shim = ShellShim(workdir)
    started = time.time()
    transcript = agent_runner(workdir, prompt, shim, cfg["timeout_seconds"])
    transcript["shell_violations"] = shim.violations()
    transcript["elapsed_ms"] = int((time.time() - started) * 1000)

    fixtures = task_dir / "fixtures"
    evaluate = load_check_py(task_dir)
    result = evaluate(workdir, transcript, fixtures)

    if result.get("judge_required"):
        jr = result["judge_required"]
        rubric_id = f"{cfg['id']}_rubric_v1"
        judge_resp = judge_client.judge({
            "rubric_id": rubric_id,
            "task_id": cfg["id"],
            "agent_output_excerpt": jr["agent_output_excerpt"],
            "context": jr.get("context", {}),
            "dimensions_to_judge": jr["dimensions_to_judge"],
        })
        for dim, val in judge_resp.get("scores", {}).items():
            result.setdefault("scores", {})[dim] = val

    return {
        "task_id": cfg["id"],
        "scores": result["scores"],
        "violations": result.get("violations", []),
        "duration_ms": transcript["elapsed_ms"],
        "tokens": transcript.get("tokens", {"prompt": 0, "completion": 0}),
        "details": result.get("details", {}),
    }


def run_bundle(bundle_root: Path, agent_runner, judge_client) -> dict:
    tasks_dir = bundle_root / "tasks"
    results = []
    for task_dir in sorted(tasks_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        results.append(run_one_task(task_dir, agent_runner, judge_client))
    return {"bundle_version": "v2.0.0", "tasks": results}


if __name__ == "__main__":
    import sys
    bundle = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(f"[dry-run] bundle root: {bundle.resolve()}")
    tasks_dir = bundle / "tasks"
    if tasks_dir.exists():
        ids = sorted(p.name for p in tasks_dir.iterdir() if p.is_dir())
        print(f"[dry-run] {len(ids)} task dirs: {ids[:5]}...")
    print("[dry-run] 请提供 agent_runner 和 judge_client 后调用 run_bundle()")
