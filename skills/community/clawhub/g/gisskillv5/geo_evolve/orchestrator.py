#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoEvolve 自进化闭环编排器 - 统一入口脚本
全局唯一知识ID: GIS-EVO-000 | 版本: V5.0 | 坤图_GIS:V5.0

功能: 顺序串联5个子模块，实现完整的自进化闭环:
  反馈采集 → 情报抓取 → 知识修正 → 索引重建 → 监控看板
"""

import json
import logging
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GEO_EVOLVE_DIR = BASE_DIR / "geo_evolve"
LOG_FILE = GEO_EVOLVE_DIR / "logs" / "orchestrator.log"
STATE_FILE = GEO_EVOLVE_DIR / "orchestrator_state.json"
VERSION = "V5.0"
ORCHESTRATOR_ID = "GIS-EVO-000"

PYTHON = sys.executable

MODULES = [
    {
        "id": "GIS-EVO-001",
        "name": "反馈采集层",
        "script": "feedback_collector/collector.py",
        "args": ["--days", "30"],
    },
    {
        "id": "GIS-EVO-002",
        "name": "情报抓取层",
        "script": "intelligence_crawler/crawler.py",
        "args": [],
    },
    {
        "id": "GIS-EVO-003",
        "name": "知识修正层",
        "script": "knowledge_fixer/fixer.py",
        "args": [],
    },
    {
        "id": "GIS-EVO-004",
        "name": "索引重建层",
        "script": "index_rebuilder/rebuilder.py",
        "args": [],
    },
    {
        "id": "GIS-EVO-005",
        "name": "量化监控看板",
        "script": "monitoring/monitor.py",
        "args": [],
    },
]


def setup_logging() -> logging.Logger:
    """配置日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("orchestrator")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = setup_logging()


def run_module(module: Dict) -> Dict:
    """运行单个模块"""
    script_path = GEO_EVOLVE_DIR / module["script"]
    if not script_path.exists():
        logger.error(f"脚本不存在: {script_path}")
        return {"module": module["name"], "status": "not_found", "error": str(script_path)}

    cmd = [PYTHON, str(script_path)] + module["args"]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=600,  # 10分钟超时
        )

        return {
            "module": module["name"],
            "module_id": module["id"],
            "status": "success" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout[-500:] if result.stdout else "",
            "stderr": result.stderr[-500:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        logger.error(f"[{module['name']}] 超时")
        return {"module": module["name"], "module_id": module["id"], "status": "timeout"}
    except Exception as e:
        logger.error(f"[{module['name']}] 异常: {e}")
        return {"module": module["name"], "module_id": module["id"], "status": "error", "error": str(e)}


def run_pipeline(skip_modules: Optional[list] = None) -> Dict:
    """运行完整自进化流水线"""
    logger.info("=" * 70)
    logger.info(f"GeoEvolve 自进化闭环编排器启动 | {ORCHESTRATOR_ID} | {VERSION}")
    logger.info(f"流水线: {' → '.join(m['name'] for m in MODULES)}")
    logger.info("=" * 70)

    skip_set = set(skip_modules or [])
    results = {
        "orchestrator_id": ORCHESTRATOR_ID,
        "version": VERSION,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "pipeline": [],
        "summary": {"total": 0, "success": 0, "failed": 0, "skipped": 0},
    }

    for i, module in enumerate(MODULES):
        if module["id"] in skip_set:
            logger.info(f"[{i+1}/{len(MODULES)}] 跳过: {module['name']}")
            results["pipeline"].append({"module": module["name"], "status": "skipped"})
            results["summary"]["skipped"] += 1
            continue

        logger.info(f"[{i+1}/{len(MODULES)}] 执行: {module['name']}")
        result = run_module(module)
        results["pipeline"].append(result)

        if result["status"] == "success":
            results["summary"]["success"] += 1
            logger.info(f"  ✓ {module['name']} 完成")
        else:
            results["summary"]["failed"] += 1
            logger.warning(f"  ✗ {module['name']} 失败: {result.get('error', result.get('stderr', ''))[:100]}")

        results["summary"]["total"] += 1

    results["completed_at"] = datetime.now().isoformat(timespec="seconds")
    logger.info(f"流水线完成: {results['summary']['success']}/{results['summary']['total']} 成功")

    return results


def save_state(results: Dict) -> None:
    """保存编排器状态"""
    state = {
        "last_run": datetime.now().isoformat(timespec="seconds"),
        "last_results": results,
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GeoEvolve 自进化闭环编排器")
    parser.add_argument("--skip", nargs="*", help="跳过的模块ID (如 GIS-EVO-002)")
    parser.add_argument("--module-only", type=str, help="仅运行指定模块ID")
    parser.add_argument("--list", action="store_true", help="列出所有模块")
    parser.add_argument("--output", "-o", type=str, help="输出结果路径")
    args = parser.parse_args()

    try:
        if args.list:
            for m in MODULES:
                print(f"  [{m['id']}] {m['name']}: {m['script']}")
            sys.exit(0)

        if args.module_only:
            module = next((m for m in MODULES if m["id"] == args.module_only), None)
            if not module:
                print(f"未知模块: {args.module_only}")
                sys.exit(1)
            result = run_module(module)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            results = run_pipeline(skip_modules=args.skip)
            save_state(results)
            if args.output:
                Path(args.output).write_text(
                    json.dumps(results, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            print(f"\n流水线完成: {results['summary']['success']}/{results['summary']['total']} 成功")
        sys.exit(0)
    except Exception as e:
        logger.exception("编排异常")
        print(f"错误: {e}")
        sys.exit(1)
