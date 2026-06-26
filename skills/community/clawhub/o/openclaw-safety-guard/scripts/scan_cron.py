#!/usr/bin/env python3
"""Cron job health scanner: job status, consecutive failures, zombie processes.
Metadata for hover panel: jobs configured, last 24h runs, failure rate, recent jobs list.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from utils import get_workspace_root, get_watchdog_config, WatchdogReport


def read_json_safe(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def scan_cron(config, report, root):
    cron_cfg = config.get("cron", {})
    cron_dir = root / cron_cfg.get("target", ".openclaw/state/cron")

    jobs_file = cron_dir / "jobs.json"
    runs_dir = cron_dir / "runs"

    if not jobs_file.exists():
        report.mark_not_applicable("未配置 Cron 任务（jobs.json 不存在）")
        return

    jobs_data = read_json_safe(jobs_file)
    if not jobs_data:
        report.add_issue(
            "cron_jobs_file_corrupted", "HIGH",
            "jobs.json 文件损坏或无法解析",
            f"检查并修复 {jobs_file}",
            [str(jobs_file)],
            evidence=["jobs.json 无法解析为 JSON"],
            fix_action="手动检查 jobs.json 格式"
        )
        return

    # Support both "list" and "jobs" keys (OpenClaw version differences)
    all_jobs = jobs_data.get("list") or jobs_data.get("jobs") or []
    if not all_jobs:
        report.mark_not_applicable("jobs.json 中无任何任务定义")
        return
    active_jobs = {j["id"]: j for j in all_jobs if j.get("enabled", True)}
    disabled_jobs = [j for j in all_jobs if not j.get("enabled", True)]

    max_fails = cron_cfg.get("max_consecutive_failures", 3)
    max_hours = cron_cfg.get("max_running_hours", 2)

    recent_jobs = []
    job_catalog = []
    total_runs_24h = 0
    total_failures_24h = 0
    now = datetime.now()
    cutoff_24h = now - timedelta(hours=24)

    if runs_dir.exists():
        for job_id, job_info in active_jobs.items():
            job_run_file = runs_dir / f"{job_id}.json"
            if not job_run_file.exists():
                job_catalog.append({
                    "id": job_id,
                    "name": job_info.get("name", job_id),
                    "enabled": True,
                    "schedule": job_info.get("schedule", {}),
                    "sessionTarget": job_info.get("sessionTarget", "unknown"),
                    "deliveryMode": job_info.get("delivery", {}).get("mode", "unknown"),
                    "wakeMode": job_info.get("wakeMode", "unknown"),
                    "lastStatus": "unknown",
                    "lastRun": "",
                    "lastRunLabel": "从未运行",
                    "consecutiveFailures": 0,
                    "hasRunRecord": False,
                })
                recent_jobs.append({
                    "name": job_info.get("name", job_id),
                    "last_run": "从未运行",
                    "status": "unknown",
                })
                continue

            run_data = read_json_safe(job_run_file)
            if not run_data:
                job_catalog.append({
                    "id": job_id,
                    "name": job_info.get("name", job_id),
                    "enabled": True,
                    "schedule": job_info.get("schedule", {}),
                    "sessionTarget": job_info.get("sessionTarget", "unknown"),
                    "deliveryMode": job_info.get("delivery", {}).get("mode", "unknown"),
                    "wakeMode": job_info.get("wakeMode", "unknown"),
                    "lastStatus": "corrupted",
                    "lastRun": "",
                    "lastRunLabel": "运行记录损坏",
                    "consecutiveFailures": 0,
                    "hasRunRecord": False,
                })
                continue

            status = run_data.get("status", "unknown")
            consecutive_failures = run_data.get("consecutiveFailures", 0)
            last_started = run_data.get("lastStartedAt", "")
            elapsed = run_data.get("lastElapsedMs")

            elapsed_str = f"{int(elapsed/1000)}s" if elapsed else "?"
            job_entry = {
                "name": job_info.get("name", job_id),
                "last_run": f"{'成功' if status == 'idle' else '失败'}（耗时 {elapsed_str}）",
                "status": status,
            }
            job_catalog.append({
                "id": job_id,
                "name": job_info.get("name", job_id),
                "enabled": True,
                "schedule": job_info.get("schedule", {}),
                "sessionTarget": job_info.get("sessionTarget", "unknown"),
                "deliveryMode": job_info.get("delivery", {}).get("mode", "unknown"),
                "wakeMode": job_info.get("wakeMode", "unknown"),
                "lastStatus": status,
                "lastRun": last_started,
                "lastRunLabel": job_entry["last_run"],
                "consecutiveFailures": consecutive_failures,
                "hasRunRecord": True,
            })
            recent_jobs.append(job_entry)

            if last_started:
                try:
                    last_time = datetime.fromisoformat(last_started.replace('Z', '+00:00'))
                    if last_time.replace(tzinfo=None) > cutoff_24h:
                        total_runs_24h += 1
                        if consecutive_failures > 0:
                            total_failures_24h += 1
                except ValueError:
                    pass

            if consecutive_failures >= max_fails:
                report.add_issue(
                    f"cron_job_failing_{job_id}", "HIGH",
                    f"Cron 任务 [{job_info.get('name', job_id)}] 已连续失败 {consecutive_failures} 次",
                    "排查 agent 日志或修复脚本，然后重置状态",
                    [str(job_run_file)],
                    evidence=[f"consecutiveFailures: {consecutive_failures}"],
                    fix_action="在飞书群告知 techops 排查该 Cron 任务日志"
                )

            if status == "running":
                if last_started:
                    try:
                        start_time = datetime.fromisoformat(last_started.replace('Z', '+00:00'))
                        duration = now.astimezone(start_time.tzinfo) - start_time if start_time.tzinfo else now - start_time.replace(tzinfo=None)
                        if duration > timedelta(hours=max_hours):
                            report.add_issue(
                                f"cron_job_zombie_{job_id}", "HIGH",
                                f"Cron 任务 [{job_info.get('name', job_id)}] 处于 running 状态超过 {max_hours} 小时（疑似僵尸）",
                                f"kill 掉相关进程，并手动修改 {job_run_file} 状态",
                                [str(job_run_file)],
                                evidence=[f"started: {last_started}, duration: {duration}"],
                                fix_action="手动 kill 进程并重置 run 状态文件"
                            )
                    except ValueError:
                        pass

    else:
        for job_id, job_info in active_jobs.items():
            job_catalog.append({
                "id": job_id,
                "name": job_info.get("name", job_id),
                "enabled": True,
                "schedule": job_info.get("schedule", {}),
                "sessionTarget": job_info.get("sessionTarget", "unknown"),
                "deliveryMode": job_info.get("delivery", {}).get("mode", "unknown"),
                "wakeMode": job_info.get("wakeMode", "unknown"),
                "lastStatus": "unknown",
                "lastRun": "",
                "lastRunLabel": "从未运行（无 runs/ 目录）",
                "consecutiveFailures": 0,
                "hasRunRecord": False,
            })
            recent_jobs.append({
                "name": job_info.get("name", job_id),
                "last_run": "从未运行（无 runs/ 目录）",
                "status": "unknown",
            })

    for job_info in disabled_jobs:
        job_id = job_info.get("id", "unknown")
        job_catalog.append({
            "id": job_id,
            "name": job_info.get("name", job_id),
            "enabled": False,
            "schedule": job_info.get("schedule", {}),
            "sessionTarget": job_info.get("sessionTarget", "unknown"),
            "deliveryMode": job_info.get("delivery", {}).get("mode", "unknown"),
            "wakeMode": job_info.get("wakeMode", "unknown"),
            "lastStatus": "disabled",
            "lastRun": "",
            "lastRunLabel": "已禁用",
            "consecutiveFailures": 0,
            "hasRunRecord": False,
        })

    failure_rate = f"{int(total_failures_24h/total_runs_24h*100)}%" if total_runs_24h > 0 else "0%"

    report.set_metadata("jobs_configured", len(active_jobs))
    report.set_metadata("jobs_disabled", len(disabled_jobs))
    report.set_metadata("last_24h_runs", total_runs_24h)
    report.set_metadata("failure_rate", failure_rate)
    report.set_metadata("recent_jobs", recent_jobs[:5])
    report.set_metadata("job_catalog", job_catalog)


def main():
    config = get_watchdog_config()
    report = WatchdogReport("cron")
    root = Path(get_workspace_root())

    scan_cron(config, report, root)
    report.save()


if __name__ == "__main__":
    main()
