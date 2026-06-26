#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path

from scripts.runtime_bootstrap import RuntimeBootstrapError, ensure_runtime
from scripts.utils import (
    DEFAULT_OUTPUT_DIRNAME,
    load_config,
    prepare_output_dir_for_run,
    resolve_default_lang,
    resolve_output_dir,
    resolve_upload_mode,
    restore_run_logging,
    setup_run_logging,
    t,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GIGO · Lobster Taster local benchmark")
    parser.add_argument("--auto-yes", action="store_true", help="Skip interactive confirmation")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive prompts for language/profile/upload choices")
    parser.add_argument("--skip-upload", action="store_true", help="Do not upload leaderboard score")
    parser.add_argument("--register-only", action="store_true", help="Only register the share ref, not the leaderboard score")
    parser.add_argument("--offline", action="store_true", help="Use fallback tasks and mock gateway")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint if available")
    parser.add_argument("--fresh", action="store_true", help="Discard any existing checkpoint and start from scratch")
    parser.add_argument("--doctor", action="store_true", help="Run the environment doctor and exit")
    parser.add_argument("--keep-task-cache", action="store_true", help="Keep the encrypted remote task cache on disk for debugging")
    parser.add_argument("--require-png-cert", action="store_true", help="Fail early unless the enhanced PNG certificate runtime is ready")
    parser.add_argument("--checkpoint-policy", default="auto", choices=["auto", "resume", "fresh"])
    parser.add_argument("--lang", default=None, choices=["zh", "en"])
    parser.add_argument("--upload-mode", default=None, choices=["ask", "upload", "local", "register"])
    parser.add_argument("--lobster-name", default=None, help="Override the lobster name for this run")
    parser.add_argument("--lobster-tags", default=None, help="Override lobster tags with a comma-separated list")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIRNAME)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(__file__).resolve().parent
    interactive = bool(args.interactive and sys.stdin.isatty() and not args.auto_yes)
    non_interactive = not interactive
    output_dir = resolve_output_dir(repo_root, args.output_dir)
    prepare_output_dir_for_run(output_dir)
    log_state = setup_run_logging(output_dir)
    config: dict[str, object] = {}

    if args.skip_upload and args.register_only:
        error_lang = args.lang or os.environ.get("GIGO_DEFAULT_LANG") or "zh"
        print("⚠️ --skip-upload 和 --register-only 不能同时使用。" if error_lang == "zh" else "⚠️ --skip-upload and --register-only cannot be used together.")
        restore_run_logging(log_state)
        return 2
    try:
        lang = resolve_default_lang(non_interactive, args.lang)
        os.environ["GIGO_SELECTED_LANG"] = lang
        print(t(lang, "output_dir_notice", output_dir=output_dir))
        print(t(lang, "run_log_notice", log_path=log_state.log_path))
        active_skill = os.environ.get("GIGO_ACTIVE_SKILL")
        if active_skill:
            print(f"🦞 Active skill: {active_skill}")

        try:
            ensure_runtime(repo_root, lang)
        except RuntimeBootstrapError as error:
            print(
                t(lang, "runtime_bootstrap_failed", error=str(error))
                if lang in {"zh", "en"}
                else f"Runtime bootstrap failed: {error}"
            )
            return 1

        from scripts.cert_generator import generate_cert, supports_png_certificate
        from scripts.checkpoint import clear_checkpoint, load_checkpoint
        from scripts.doctor import run_doctor
        from scripts.gateway_client import GatewayClient
        from scripts.report_generator import generate_report
        from scripts.score_uploader import apply_cloud_evaluation, submit_for_cloud_scoring
        from scripts.session_client import end_task_session, start_task_session
        from scripts.soul_parser import parse_soul_md
        from scripts.task_fetcher import cleanup_task_cache, fetch_task_package
        from scripts.tasting_runner import TastingRunner
        from scripts.tasting_scorer import score_results
        from scripts.utils import (
            apply_host_profile_overrides,
            check_environment,
            describe_bundle_source,
            print_summary,
            prompt_lobster_profile,
            prompt_resume_choice,
            prompt_upload_choice,
        )
        from scripts.version_checker import check_skill_version

        config = load_config(repo_root / "scripts" / "tasting_config.json")
        config["lang"] = lang
        config["output_dir"] = str(output_dir)
        config["offline_mode"] = bool(args.offline)
        config["force_embedded_bundle"] = os.environ.get("GIGO_FORCE_EMBEDDED_BUNDLE") == "1"
        config["task_cache_policy"] = "persist" if args.keep_task_cache else "ephemeral"
        config["require_png_cert"] = bool(args.require_png_cert or (os.environ.get("GIGO_REQUIRE_PNG_CERT") == "1"))
        config["checkpoint_policy"] = args.checkpoint_policy
        config["skill_version"] = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
        config["runtime_mode"] = "v2" if str(config["skill_version"]).startswith("2.") else "v1"
        if args.skip_upload:
            config["upload_mode"] = "local"
        elif args.register_only:
            config["upload_mode"] = "register"
        else:
            config["upload_mode"] = resolve_upload_mode(non_interactive, args.upload_mode)
        if non_interactive and config["upload_mode"] == "ask":
            config["upload_mode"] = "upload"
        config["interactive_mode"] = interactive

        if args.offline:
            os.environ["GIGO_GATEWAY_MOCK"] = "1"

        if args.doctor:
            return run_doctor(config, repo_root, offline=args.offline)

        if config["require_png_cert"] and not supports_png_certificate():
            print(
                "⚠️ 当前还不能生成规整的 PNG 证书。先运行 python main.py --doctor 检查 Pillow / qrcode / pip / venv，再回来正式开跑。"
                if lang == "zh"
                else "⚠️ A polished PNG certificate is not available yet. Run python main.py --doctor first to check Pillow / qrcode / pip / venv before the real run."
            )
            return 1

        version_check = check_skill_version(config, repo_root, offline=args.offline)
        config["skill_version"] = version_check.local_version
        config["runtime_mode"] = "v2" if str(version_check.local_version).startswith("2.") else "v1"
        if version_check.is_blocked:
            print(
                f"⚠️ 当前 skill 版本 {version_check.local_version} 已被阻止运行，请先更新。"
                if lang == "zh"
                else f"⚠️ Skill version {version_check.local_version} has been blocked. Please update before running again."
            )
            return 1
        if version_check.update_available and version_check.latest_stable:
            print(
                f"📦 检测到新版本：{version_check.latest_stable}（当前 {version_check.local_version}）"
                if lang == "zh"
                else f"📦 New version available: {version_check.latest_stable} (current {version_check.local_version})"
            )
            if version_check.release_notes:
                print(f"📝 {'更新说明' if lang == 'zh' else 'Release notes'}：{version_check.release_notes}")
        elif version_check.error and not args.offline:
            print(
                f"ℹ️ 暂时无法检查版本更新：{version_check.error}"
                if lang == "zh"
                else f"ℹ️ Could not check for updates right now: {version_check.error}"
            )
        if version_check.rollback_recommended == version_check.local_version:
            print(
                f"⚠️ 当前版本 {version_check.local_version} 被标记为建议回滚，请尽快更新。"
                if lang == "zh"
                else f"⚠️ Version {version_check.local_version} is flagged for rollback. Please update soon."
            )

        env_info = check_environment(config, repo_root)
        if not env_info.gateway_available and not args.offline:
            print(
                "Gateway 不可用。你可以先启动本地 Gateway，或使用 --offline 跑 fallback 闭环。"
                if lang == "zh"
                else "Gateway is unavailable. Start your local Gateway first, or use --offline for the fallback flow."
            )
            return 1

        soul = parse_soul_md(repo_root, lang)
        soul = apply_host_profile_overrides(
            soul,
            name_override=args.lobster_name,
            tags_override=args.lobster_tags,
        )
        if interactive and not (
            args.lobster_name
            or args.lobster_tags
            or os.environ.get("GIGO_LOBSTER_NAME")
            or os.environ.get("GIGO_LOBSTER_TAGS")
        ):
            soul = prompt_lobster_profile(lang, soul, env_info.soul_path)

        if not args.offline and not config.get("force_embedded_bundle"):
            try:
                config["task_session"] = start_task_session(config)
            except Exception as error:
                config["task_bundle_warning"] = (
                    f"暂时无法建立云端题包会话：{error}" if lang == "zh" else f"Could not start the remote task session: {error}"
                )

        tasks = fetch_task_package(config, repo_root)
        test_task_ids = [item.strip() for item in os.environ.get("GIGO_TEST_TASK_IDS", "").split(",") if item.strip()]
        if test_task_ids:
            requested = set(test_task_ids)
            tasks = [task for task in tasks if task.id in requested]
            missing = [task_id for task_id in test_task_ids if task_id not in {task.id for task in tasks}]
            if missing:
                raise RuntimeError(f"GIGO_TEST_TASK_IDS contains unknown task ids: {', '.join(missing)}")
        test_task_limit = os.environ.get("GIGO_TEST_MAX_TASKS", "").strip()
        if test_task_limit.isdigit():
            tasks = tasks[: max(1, int(test_task_limit))]
        config["expected_task_count"] = len(tasks)
        env_info.render_confirmation(soul, config, ask_to_start=not non_interactive)
        if config.get("task_bundle_warning"):
            print(f"⚠️ {config['task_bundle_warning']}")
        if config.get("task_bundle_source") in {"remote", "remote_session"}:
            print(f"📦 {t(lang, 'bundle_remote_loaded', version=config.get('task_bundle_version', 'unknown'))}")
        else:
            source_label = describe_bundle_source(str(config.get("task_bundle_source", "unknown")), lang)
            print(f"📦 {t(lang, 'bundle_fallback_loaded', version=config.get('task_bundle_version', 'unknown'), source=source_label)}")

        gateway_client = GatewayClient(
            base_url=config["gateway_base"],
            mock_mode=bool(args.offline or os.environ.get("GIGO_GATEWAY_MOCK") == "1"),
        )
        checkpoint = load_checkpoint(output_dir)
        resume_data = None
        if checkpoint and config.get("runtime_mode") == "v1":
            completed_count = len(checkpoint.get("completed_task_ids", []))
            checkpoint_policy = str(config.get("checkpoint_policy", "auto"))
            if args.fresh or checkpoint_policy == "fresh":
                clear_checkpoint(output_dir)
                print("🧼 已按要求清掉旧进度，本次会从头重新试吃。" if lang == "zh" else "🧼 Existing progress discarded as requested. Starting from scratch.")
            elif args.resume or checkpoint_policy == "resume" or non_interactive or prompt_resume_choice(lang, completed_count, len(tasks)):
                if lang == "zh":
                    print(f"♻️ 已接上次进度，继续完成剩下的 {len(tasks) - completed_count} 道菜。")
                else:
                    print(f"♻️ Progress restored. Picking up the remaining {len(tasks) - completed_count} dishes.")
                resume_data = checkpoint
            else:
                clear_checkpoint(output_dir)
                print("🧼 已放弃旧进度，本次会从头重新试吃。" if lang == "zh" else "🧼 Previous progress discarded. Starting a fresh tasting run.")
        elif checkpoint and config.get("runtime_mode") == "v2":
            clear_checkpoint(output_dir)
            print(
                "🧼 v2 stable 当前默认从头重新跑，不复用旧的 v1/v2 checkpoint。"
                if lang == "zh"
                else "🧼 The v2 stable runtime currently starts fresh and does not reuse older v1/v2 checkpoints."
            )

        if config.get("runtime_mode") == "v2":
            from scripts.v2_agent_runner import AgentRunner as V2AgentRunner
            from scripts.v2_scorer import score_results_v2

            runner = V2AgentRunner(config=config, gateway_client=gateway_client)
            raw_results = runner.run(tasks=tasks)
            scores = score_results_v2(raw_results=raw_results, config=config, soul=soul)
        else:
            runner = TastingRunner(config=config, soul=soul, gateway_client=gateway_client, output_dir=output_dir)
            raw_results = runner.run(tasks=tasks, resume_data=resume_data)
            scores = score_results(raw_results=raw_results, config=config, soul=soul)

        ref_code = "pending"
        upload_result = None
        upload_mode = config.get("upload_mode", "ask")
        if upload_mode != "local" and not args.offline:
            should_upload = upload_mode in {"upload", "register"} or (interactive and prompt_upload_choice(lang))
            if should_upload:
                try:
                    effective_upload_mode = upload_mode if upload_mode in {"upload", "register"} else "upload"
                    upload_result = submit_for_cloud_scoring(
                        scores=scores,
                        raw_results=raw_results,
                        upload_mode=effective_upload_mode,
                        config=config,
                    )
                    if upload_result.get("ref_code"):
                        ref_code = str(upload_result["ref_code"])
                    apply_cloud_evaluation(scores, raw_results, upload_result)
                except Exception as error:
                    upload_result = {"success": False, "score_verified": False, "error": str(error)}

        report_path = generate_report(
            scores=scores,
            raw_results=raw_results,
            ref_code=ref_code,
            config=config,
            template_path=repo_root / "templates" / "report_template.html",
            upload_result=upload_result,
        )
        cert_path = generate_cert(
            scores=scores,
            ref_code=ref_code,
            config=config,
            output_dir=output_dir,
            template_path=repo_root / "templates" / "cert_template.png",
            upload_result=upload_result,
        )

        print_summary(
            scores=scores,
            report_path=report_path,
            cert_path=cert_path,
            upload_result=upload_result,
            os_name=env_info.os_name,
        )
        clear_checkpoint(output_dir)
        return 0
    except Exception:
        traceback.print_exc()
        raise
    finally:
        if config.get("task_session") and not args.offline:
            end_task_session(config)
        try:
            from scripts.task_fetcher import cleanup_task_cache

            cleanup_task_cache(config)
        except Exception:
            pass
        restore_run_logging(log_state)


if __name__ == "__main__":
    raise SystemExit(main())
