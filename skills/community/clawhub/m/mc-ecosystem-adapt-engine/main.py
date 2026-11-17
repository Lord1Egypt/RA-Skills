"""MC Ecosystem Adapt Engineer V1 - Main Entry Point

Features:
1. Command-line argument parsing (argparse)
2. JSON config file batch task support
3. Feature routing (F1-F9)
4. Unified output structure

Usage:
    # Command-line mode
    python main.py --feature jar_parser --jar-path "D:\\mods\\create.jar"

    # JSON config mode
    python main.py --config "task.json"
"""

import sys
import os
import argparse
import json
import html
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import generate_unified_output
from core.i18n import t, set_language, get_current_language, get_supported_languages, save_language_preference

logger = get_logger("main")


FEATURES = {
    "jar_parser": {
        "name": "F1 JAR Structure Parse",
        "module": "core.jar_parser",
        "function": "run",
        "status": "implemented",
    },
    "mod_searcher": {
        "name": "F2 Mod Search & Download",
        "module": "core.mod_searcher",
        "function": "run",
        "status": "implemented",
    },
    "env_builder": {
        "name": "F3 Environment Setup Guide",
        "module": "core.env_builder",
        "function": "run",
        "status": "implemented",
    },
    "mixin_scanner": {
        "name": "F4 Mixin Conflict Scan",
        "module": "core.mixin_scanner",
        "function": "run",
        "status": "implemented",
    },
    "repacker": {
        "name": "F5 Resource Repack",
        "module": "core.repacker",
        "function": "run",
        "status": "implemented",
    },
    "save_sync": {
        "name": "F6 Save Sync",
        "module": "core.save_sync",
        "function": "run",
        "status": "implemented",
    },
    "translator": {
        "name": "F7 Basic Localization",
        "module": "core.translator",
        "function": "run",
        "status": "implemented",
    },
    "crash_analyzer": {
        "name": "F8 Crash Analysis & Fix",
        "module": "core.crash_analyzer",
        "function": "run",
        "status": "implemented",
    },
    "auto_fix": {
        "name": "F8.1 Auto Fix",
        "module": "core.auto_fix",
        "function": "auto_fix_run",
        "status": "implemented",
    },
    "migration_assess": {
        "name": "F9 Migration Feasibility Assessment",
        "module": "core.migration_assessor",
        "function": "run",
        "status": "implemented",
    },
}


def dispatch_feature(feature: str, args: argparse.Namespace) -> int:
    """Dispatch a feature for execution.

    Args:
        feature: Feature identifier
        args: Command-line arguments

    Returns:
        Exit code 0=success 1=failure
    """
    if feature not in FEATURES:
        logger.error(f"Unknown feature: {feature}")
        logger.info(f"Available features: {', '.join(FEATURES.keys())}")
        return 1

    feat_info = FEATURES[feature]
    logger.info(f"Dispatching: {feat_info['name']} ({feature})")

    if feat_info["status"] != "implemented":
        return _render_not_implemented(feature, feat_info, args)

    try:
        from core.auth_manager import check_permission, record_usage, FUNC_AUTO, FUNC_SEMI
        func_type = FUNC_SEMI if feature in ("env_builder", "save_sync") else FUNC_AUTO
        perm = check_permission(feature, func_type)
        if not perm["allowed"]:
            logger.warning(f"Feature limited: {perm['reason']}")
            print(f"\n⚠️  {t('auth.feature_limited_warning', reason=perm['reason'])}", flush=True)
            print(f"   {t('auth.member_tier')}: {perm['tier']}", flush=True)
            print(f"   {t('auth.remaining')}: {perm['remaining']}/{perm['limit']}", flush=True)
            print(f"   {t('auth.upgrade_tip')}\n", flush=True)
            return 1
    except Exception as e:
        logger.debug(f"Permission check skipped: {e}")

    try:
        import importlib
        module = importlib.import_module(feat_info["module"])
        func = getattr(module, feat_info["function"])
        result = func(args)
        try:
            record_usage(feature)
        except Exception:
            pass
        return 0 if result.get("status") != "error" else 1
    except ImportError as e:
        logger.error(f"Module import failed: {feat_info['module']} - {e}")
        print(f"\n❌ {t('error.module_import_failed', module=feat_info['module'])}: {e}", flush=True)
        return _render_not_implemented(feature, feat_info, args)
    except Exception as e:
        logger.exception(f"Feature execution error: {feature}")
        print(f"\n❌ {t('error.feature_execution_failed')}: {e}", flush=True)
        generate_unified_output(
            feature=feature,
            status="error",
            input_summary=vars(args),
            result={},
            title=f"{feat_info['name']} - {t('not_implemented.error_report')}",
            html_content=(
                f'<div class="callout red">'
                f'<div class="callout-title">{t("not_implemented.error_report")}</div>'
                f'<p>{t("not_implemented.error_report")}: {html.escape(feature)}</p>'
                f'<div class="code-block">{html.escape(str(e))}</div>'
                f'</div>'
            ),
            errors=[str(e)],
        )
        return 1


def _render_not_implemented(
    feature: str, feat_info: dict, args: argparse.Namespace
) -> int:
    """Render a "feature not implemented" notice

    Args:
        feature: Feature identifier
        feat_info: Feature info
        args: Command-line arguments

    Returns:
        Exit code 1
    """
    logger.warning(f"Feature {feature} not yet implemented (module: {feat_info['module']})")

    print(f"\n{t('error.feature_not_implemented', feature=feat_info['name'])}")
    print(f"  {t('not_implemented.module_path')}: {feat_info['module']}")
    print(f"  {t('not_implemented.current_status')}: {t('error.current_status')}")
    print(f"  {t('not_implemented.planned_phases')}:")
    print(f"    {t('not_implemented.p2')}")
    print(f"    {t('not_implemented.p3')}")
    print(f"    {t('not_implemented.p4')}")
    print(f"    {t('not_implemented.p5')}")
    print(f"    {t('not_implemented.p6')}")
    print(f"  {t('not_implemented.reference')}\n")

    generate_unified_output(
        feature=feature,
        status="error",
        input_summary=vars(args) if args else {},
        result={},
        title=f"{feat_info['name']} - {t('error.feature_not_implemented', feature='')}",
        html_content=(
            f'<div class="callout yellow">'
            f'<div class="callout-title">{t("not_implemented.title")}</div>'
            f'<p>{t("not_implemented.message", name=html.escape(feat_info["name"]))}</p>'
            f'<p>{t("not_implemented.planned_phases")}:</p>'
            f'<ul>'
            f'<li>{t("not_implemented.p2")}</li>'
            f'<li>{t("not_implemented.p3")}</li>'
            f'<li>{t("not_implemented.p4")}</li>'
            f'<li>{t("not_implemented.p5")}</li>'
            f'<li>{t("not_implemented.p6")}</li>'
            f'</ul>'
            f'<p>{t("not_implemented.module_path")}: <code>{html.escape(feat_info["module"])}</code></p>'
            f'</div>'
        ),
        errors=[t("error.feature_not_implemented", feature=feature)],
    )
    return 1


def run_task_from_config(config_path: str) -> int:
    """Run tasks from a JSON config file in batch mode

    Config file format:
    {
        "tasks": [
            {
                "feature": "jar_parser",
                "args": {
                    "jar_path": "D:\\mods\\create.jar",
                    "output": "D:\\output"
                }
            },
            ...
        ]
    }

    Args:
        config_path: JSON config file path

    Returns:
        Exit code (0=all success, 1=has failures)
    """
    config_path = Path(config_path)
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        print(f"❌ {t('error.config_not_found', path=config_path)}", flush=True)
        return 1

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            task_config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Config file JSON parse failed: {config_path} - {e}")
        print(f"❌ {t('error.config_parse_failed', path=config_path)}: {e}", flush=True)
        return 1

    tasks = task_config.get("tasks", [])
    if not tasks:
        logger.warning("No tasks in config file")
        print(f"⚠️  {t('common.no_data')}", flush=True)
        return 0

    logger.info(f"Loaded {len(tasks)} tasks from config file: {config_path.name}")
    print(f"\n📋 {t('examples.config')} ({config_path.name}): {len(tasks)} {t('common.import')}\n")

    exit_code = 0
    for i, task in enumerate(tasks, 1):
        feature = task.get("feature")
        task_args = task.get("args", {})

        if not feature:
            logger.warning(f"Task {i} missing feature field, skipping")
            print(f"  ⚠️  {t('warning.limited')}: task #{i} missing 'feature' field", flush=True)
            continue

        print(f"  ▶ [{i}/{len(tasks)}] {feature} ...", flush=True)

        args = argparse.Namespace(**task_args)
        if not hasattr(args, "output"):
            args.output = config.DEFAULTS["output_dir"]

        result = dispatch_feature(feature, args)
        if result != 0:
            exit_code = 1

    print()
    return exit_code


def build_arg_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser

    Contains all F1-F9 feature parameters, specify the feature via --feature
    """
    parser = argparse.ArgumentParser(
        prog="mc-skill",
        description=t("banner.tagline"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{t('examples.title')}
{t('examples.cmd')}
{t('examples.cmd_example')}

{t('examples.config')}
{t('examples.config_example')}

{t('examples.lang')}
{t('examples.lang_example')}

{t('examples.features_title')}
  jar_parser       {t('feature.f1.name')}
  mod_searcher     {t('feature.f2.name')}
  env_builder      {t('feature.f3.name')}
  mixin_scanner    {t('feature.f4.name')}
  repacker         {t('feature.f5.name')}
  save_sync        {t('feature.f6.name')}
  translator       {t('feature.f7.name')}
  crash_analyzer   {t('feature.f8.name')}
  auto_fix         {t('feature.f8_1.name')}
  migration_assess {t('feature.f9.name')}
        """,
    )

    parser.add_argument(
        "--feature",
        choices=list(FEATURES.keys()),
        help=t("help.feature"),
    )
    parser.add_argument(
        "--config",
        help=t("help.config"),
    )
    parser.add_argument(
        "--output",
        default=config.DEFAULTS["output_dir"],
        help=t("help.output", default=config.DEFAULTS["output_dir"]),
    )
    parser.add_argument(
        "--lang",
        choices=list(get_supported_languages().keys()),
        help=t("help.lang"),
    )

    parser.add_argument(
        "--jar-path",
        help=t("help.jar_path"),
    )
    parser.add_argument(
        "--detail-level",
        choices=["basic", "detailed"],
        default="basic",
        help=t("help.detail_level"),
    )

    parser.add_argument(
        "--query",
        help=t("help.query"),
    )
    parser.add_argument(
        "--mc-version",
        help=t("help.mc_version"),
    )
    parser.add_argument(
        "--loader",
        choices=config.LOADERS,
        help=t("help.loader"),
    )
    parser.add_argument(
        "--download",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.download"),
    )
    parser.add_argument(
        "--with-deps",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.with_deps"),
    )
    parser.add_argument(
        "--platform",
        choices=["modrinth", "curseforge", "both"],
        default="modrinth",
        help=t("help.platform"),
    )

    parser.add_argument(
        "--launcher",
        choices=config.LAUNCHERS,
        help=t("help.launcher"),
    )
    parser.add_argument(
        "--device",
        choices=config.DEVICES,
        default="pc",
        help=t("help.device"),
    )

    parser.add_argument(
        "--mods-dir",
        help=t("help.mods_dir"),
    )
    parser.add_argument(
        "--severity",
        choices=["summary", "full"],
        default="summary",
        help=t("help.severity"),
    )

    parser.add_argument(
        "--resources-dir",
        help=t("help.resources_dir"),
    )
    parser.add_argument(
        "--validate",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=True,
        help=t("help.validate"),
    )

    parser.add_argument(
        "--action",
        choices=["setup", "backup", "restore"],
        help=t("help.action"),
    )
    parser.add_argument(
        "--sync-dir",
        help=t("help.sync_dir"),
    )

    parser.add_argument(
        "--target-lang",
        default="zh_cn",
        help=t("help.target_lang"),
    )
    parser.add_argument(
        "--patch-only",
        action="store_true",
        help=t("help.patch_only"),
    )

    parser.add_argument(
        "--crash-log",
        help=t("help.crash_log"),
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help=t("help.offline"),
    )

    parser.add_argument(
        "--fix-mods-dir",
        help=t("help.fix_mods_dir"),
    )
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help=t("help.auto_confirm"),
    )

    parser.add_argument(
        "--from-mc-version",
        help=t("help.from_mc_version"),
    )
    parser.add_argument(
        "--to-mc-version",
        help=t("help.to_mc_version"),
    )
    parser.add_argument(
        "--from-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help=t("help.from_loader"),
    )
    parser.add_argument(
        "--to-loader",
        choices=["forge", "neoforge", "fabric", "quilt"],
        help=t("help.to_loader"),
    )

    parser.add_argument(
        "--auth-status",
        action="store_true",
        help=t("help.auth_status"),
    )
    parser.add_argument(
        "--activate",
        help=t("help.activate"),
    )
    parser.add_argument(
        "--set-tier",
        choices=["free", "normal", "premium"],
        help=t("help.set_tier"),
    )
    parser.add_argument(
        "--reset-usage",
        action="store_true",
        help=t("help.reset_usage"),
    )
    parser.add_argument(
        "--reset-free-period",
        action="store_true",
        help=t("help.reset_free_period"),
    )
    
    parser.add_argument(
        "--show-machine-id",
        action="store_true",
        help="显示您的机器码",
    )

    parser.add_argument(
        "--query-auth",
        action="store_true",
        help="查询本机授权状态（JSON格式，适合Agent调用）",
    )

    parser.add_argument(
        "--list-plans",
        action="store_true",
        help="查看可用套餐列表",
    )

    parser.add_argument(
        "--api-server",
        metavar="PORT",
        type=int,
        nargs="?",
        const=8765,
        default=None,
        help="启动本地HTTP API服务器（供Agent直接调用），默认端口8765",
    )

    return parser


def print_banner():
    """Print program startup banner"""
    title = t("banner.title")
    subtitle = t("banner.subtitle")
    features = t("banner.features")
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {title}  {t('banner.version')}                                ║
║   {subtitle}                                                 ║
║                                                              ║
║   {features}                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main(argv: Optional[list] = None) -> int:
    """Main entry point

    Args:
        argv: List of command-line arguments, None means use sys.argv

    Returns:
        Exit code 0=success 1=failure
    """
    print_banner()

    config.ensure_output_dirs()

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.lang:
        set_language(args.lang)
        save_language_preference(args.lang)
        print(t("lang.set_success", lang=args.lang))
        print_banner()
        return 0

    if args.config:
        return run_task_from_config(args.config)

    if args.auth_status:
        from core.auth_manager import print_auth_status
        print_auth_status()
        return 0

    if args.activate:
        from core.auth_manager import activate_license
        result = activate_license(args.activate)
        print(f"{t('auth.activate_result')}: {result['message']}", flush=True)
        return 0 if result["success"] else 1

    if args.set_tier:
        from core.auth_manager import set_tier
        set_tier(args.set_tier)
        print(t("auth.tier_set", tier=args.set_tier), flush=True)
        return 0

    if args.reset_usage:
        from core.auth_manager import reset_usage
        reset_usage()
        print(t("auth.usage_reset"), flush=True)
        return 0

    if args.reset_free_period:
        from core.auth_manager import reset_free_period
        reset_free_period()
        print(t("auth.free_period_reset"), flush=True)
        return 0

    if args.show_machine_id:
        from core.auth_manager import get_machine_id, _load_auth_state, _ensure_first_use_recorded
        # 确保首次使用记录（会显示欢迎提示）
        state = _load_auth_state()
        state = _ensure_first_use_recorded(state)
        # 显示当前机器码
        machine_id = state.get("machine_id", get_machine_id())
        print("\n" + "=" * 60)
        print("  📍 您的机器码:")
        print("=" * 60)
        print(f"\n  {machine_id}\n")
        print("=" * 60)
        # 尝试复制到剪贴板
        try:
            import subprocess
            import sys
            if sys.platform == "win32":
                subprocess.run("clip", input=machine_id, capture_output=True, text=True)
                print("  ✅ 机器码已复制到剪贴板\n")
        except Exception:
            print("  💡 请手动复制上面的机器码\n")
        return 0

    if args.query_auth:
        from core.auth_manager import get_auth_status_json
        import json
        # 以JSON格式输出授权状态，适合Agent直接解析
        status = get_auth_status_json()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0

    if args.list_plans:
        from core.auth_manager import print_available_plans
        print_available_plans()
        return 0

    if args.api_server is not None:
        return run_local_api_server(args.api_server)

    if not args.feature:
        parser.print_help()
        print(f"\n{t('error.missing_feature')}")
        return 1

    return dispatch_feature(args.feature, args)


def run_local_api_server(port: int = 8765) -> int:
    """启动本地HTTP API服务器（供Agent直接调用自助查询功能）

    提供的接口:
        GET  /api/machine-id        获取本机机器码
        GET  /api/auth/status       获取本机授权状态（JSON）
        GET  /api/auth/plans        获取可用套餐列表（JSON）
        GET  /api/health            健康检查
        GET  /                      API说明文档

    Args:
        port: 监听端口，默认8765

    Returns:
        退出码
    """
    import json
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    from core.auth_manager import (
        get_auth_status_json,
        get_available_plans,
        get_machine_id,
        _load_auth_state,
        _ensure_first_use_recorded,
    )

    class LocalAPIHandler(BaseHTTPRequestHandler):
        """本地API请求处理器"""

        def log_message(self, format, *args):
            """重写日志格式，简化输出"""
            print(f"  [API] {self.address_string()} - {format % args}", flush=True)

        def _set_headers(self, status_code: int = 200, content_type: str = "application/json"):
            self.send_response(status_code)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()

        def _json_response(self, data: dict, status_code: int = 200):
            self._set_headers(status_code, "application/json")
            response = json.dumps(data, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode("utf-8"))

        def _html_response(self, html: str, status_code: int = 200):
            self._set_headers(status_code, "text/html")
            self.wfile.write(html.encode("utf-8"))

        def do_OPTIONS(self):
            """CORS预检请求处理"""
            self._set_headers(204)

        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"

            # 健康检查
            if path == "/api/health":
                self._json_response({
                    "status": "ok",
                    "service": "mc-skill-local-api",
                    "version": "v1.0.4",
                    "port": port,
                })
                return

            # 获取机器码
            if path == "/api/machine-id":
                state = _load_auth_state()
                state = _ensure_first_use_recorded(state)
                machine_id = state.get("machine_id", get_machine_id())
                self._json_response({
                    "machine_id": machine_id,
                    "message": "请将此机器码提供给管理员或AI Agent以开通授权套餐",
                })
                return

            # 获取授权状态
            if path == "/api/auth/status":
                status = get_auth_status_json()
                self._json_response(status)
                return

            # 获取套餐列表
            if path == "/api/auth/plans":
                plans = get_available_plans()
                self._json_response(plans)
                return

            # API首页 - 文档说明
            if path == "/" or path == "/api":
                html = self._build_api_docs_html()
                self._html_response(html)
                return

            # 404
            self._json_response({
                "error": "not_found",
                "message": f"接口不存在: {path}",
                "available_endpoints": [
                    "GET /api/health",
                    "GET /api/machine-id",
                    "GET /api/auth/status",
                    "GET /api/auth/plans",
                ],
            }, 404)

        def _build_api_docs_html(self) -> str:
            """构建API文档首页"""
            state = _load_auth_state()
            state = _ensure_first_use_recorded(state)
            machine_id = state.get("machine_id", get_machine_id())

            return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MC Skill - 本地自助查询 API</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 32px 40px;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 32px 40px; }}
        .machine-id-card {{
            background: #f0f4ff;
            border: 1px solid #c7d2fe;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 28px;
        }}
        .machine-id-card .label {{
            font-size: 13px;
            color: #6366f1;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .machine-id-card .value {{
            font-family: "Consolas", "Monaco", monospace;
            font-size: 18px;
            background: #fff;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #e0e7ff;
            word-break: break-all;
            color: #1e1b4b;
            font-weight: 600;
        }}
        .section {{ margin-bottom: 28px; }}
        .section h2 {{
            font-size: 18px;
            color: #1e1b4b;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e0e7ff;
        }}
        .endpoint {{
            background: #fafafa;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
            transition: all 0.2s;
        }}
        .endpoint:hover {{
            border-color: #6366f1;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
        }}
        .endpoint .method {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            margin-right: 10px;
            letter-spacing: 0.5px;
        }}
        .method.get {{ background: #dcfce7; color: #166534; }}
        .endpoint .path {{
            font-family: "Consolas", "Monaco", monospace;
            font-weight: 600;
            color: #4338ca;
        }}
        .endpoint .desc {{
            margin-top: 8px;
            padding-left: 84px;
            font-size: 13px;
            color: #6b7280;
        }}
        .tip {{
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 10px;
            padding: 16px;
            color: #92400e;
            font-size: 13px;
            line-height: 1.7;
        }}
        .tip strong {{ color: #78350f; }}
        .footer {{
            text-align: center;
            padding: 20px 40px;
            background: #f9fafb;
            color: #9ca3af;
            font-size: 12px;
            border-top: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔌 MC Skill 本地自助查询 API</h1>
            <p>供 AI Agent 直接调用的本地接口服务</p>
        </div>
        <div class="content">
            <div class="machine-id-card">
                <div class="label">📍 当前设备机器码</div>
                <div class="value">{machine_id}</div>
            </div>
            <div class="section">
                <h2>📡 可用接口列表</h2>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/health</span>
                    <div class="desc">健康检查，确认API服务是否正常运行</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/machine-id</span>
                    <div class="desc">获取本机机器码（用于授权开通、查询套餐状态等）</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/auth/status</span>
                    <div class="desc">获取完整授权状态（会员等级、使用次数、免费期信息等）</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="path">/api/auth/plans</span>
                    <div class="desc">获取可用套餐列表（订阅方案、价格、各等级权限说明）</div>
                </div>
            </div>
            <div class="section">
                <h2>💡 使用说明</h2>
                <div class="tip">
                    <strong>Agent调用方式：</strong><br>
                    • 此API仅在本机运行（127.0.0.1:{port}），不会暴露到公网<br>
                    • 所有接口均返回 JSON 格式，便于程序解析<br>
                    • 可直接使用 HTTP GET 请求调用，无需额外认证<br>
                    • 如需停止服务，在终端按 <strong>Ctrl+C</strong> 即可
                </div>
            </div>
        </div>
        <div class="footer">
            MC Skill v1.0.1 · 本地API服务 · 端口 {port}
        </div>
    </div>
</body>
</html>"""

    # === 启动服务器 ===
    server = None
    try:
        server_address = ("127.0.0.1", port)
        server = HTTPServer(server_address, LocalAPIHandler)
    except OSError as e:
        print(f"\n❌ 端口 {port} 被占用，请使用其他端口：", flush=True)
        print(f"   python main.py --api-server 8766", flush=True)
        print(f"   错误信息: {e}\n", flush=True)
        return 1

    print("\n" + "=" * 65, flush=True)
    print("  🔌 MC Skill 本地自助查询 API 服务已启动", flush=True)
    print("=" * 65, flush=True)
    print(f"  📡 服务地址:  http://127.0.0.1:{port}", flush=True)
    print(f"  📖 API文档:   http://127.0.0.1:{port}/", flush=True)
    print(f"  🤖 Agent调用: http://127.0.0.1:{port}/api/auth/status", flush=True)
    print("-" * 65, flush=True)
    print("  可用接口:", flush=True)
    print(f"    GET /api/health         健康检查", flush=True)
    print(f"    GET /api/machine-id     获取机器码", flush=True)
    print(f"    GET /api/auth/status    授权状态查询", flush=True)
    print(f"    GET /api/auth/plans     套餐列表查询", flush=True)
    print("-" * 65, flush=True)
    print("  💡 提示: 按 Ctrl+C 停止服务", flush=True)
    print("=" * 65 + "\n", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  👋 API服务已停止\n", flush=True)
        server.server_close()
        return 0
    except Exception as e:
        print(f"\n❌ API服务异常: {e}\n", flush=True)
        server.server_close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
