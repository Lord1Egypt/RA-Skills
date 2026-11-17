#!/usr/bin/env python3
"""Single command-line entry point for the file-backed Novel Skill gates."""

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine import __version__
from novelforge_engine.blueprint import validate_blueprint
from novelforge_engine.context import build_context
from novelforge_engine.distill import build_distill_from_spec, distill_engine, prepare_distill
from novelforge_engine.engine import load_engine
from novelforge_engine.genesis import evaluate_story_capacity, init_project_with_genesis
from novelforge_engine.manifest import verify_manifest, write_manifest
from novelforge_engine.io import file_lock
from novelforge_engine.pipeline import (
    advance_pipeline,
    find_project_root,
    get_pipeline_status,
    interrupt_pipeline,
    resume_pipeline,
)
from novelforge_engine.project import activate_engine, verify_project
from novelforge_engine.review import apply_review
from novelforge_engine.settlement import apply_settlement
from novelforge_engine.skill_audit import audit_builtin_core
from novelforge_engine.state import init_project, transition_chapter
from novelforge_engine.style_detector import detect_style, policy_for_profile
from novelforge_engine.wiki import rebuild_wiki


def _json(value):
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _profile_for_path(path):
    path = Path(path).resolve()
    for parent in (path.parent,) + tuple(path.parent.parents):
        project_file = parent / ".novelforge" / "state" / "project.json"
        if project_file.is_file():
            with project_file.open("r", encoding="utf-8") as handle:
                return json.load(handle)
    return {}


def _engine_install(project, source):
    source_input = Path(source)
    if source_input.is_symlink():
        raise ValueError("engine source must not be a symlink")
    source = source_input.resolve()
    engine = load_engine(source, require_manifest=False)
    project_root = Path(project).resolve()
    target = project_root / ".novelforge" / "engines" / engine["id"]
    if any(path.is_symlink() for path in source.rglob("*")):
        raise ValueError("engine source must not contain symlinks")
    target.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(project_root / ".novelforge" / "locks" / "engines.lock"):
        if target.exists():
            raise ValueError("engine already installed: {}".format(engine["id"]))
        staging_parent = Path(tempfile.mkdtemp(prefix=".engine-install-", dir=str(target.parent)))
        staging = staging_parent / engine["id"]
        try:
            shutil.copytree(str(source), str(staging), symlinks=False)
            write_manifest(staging)
            load_engine(staging)
            os.replace(str(staging), str(target))
        finally:
            shutil.rmtree(str(staging_parent), ignore_errors=True)
    return {"status": "PASS", "engine": engine["id"], "path": str(target)}


def build_parser():
    parser = argparse.ArgumentParser(prog="novelforgectl")
    parser.add_argument("--version", "-V", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")
    skill = sub.add_parser("skill-audit")
    skill.add_argument("--root", default=str(SKILL_ROOT))
    project = sub.add_parser("project")
    project_sub = project.add_subparsers(dest="project_command")
    init = project_sub.add_parser("init")
    init.add_argument("root")
    init.add_argument("--genre", default=None)
    init.add_argument("--scale", default="standard")
    init.add_argument("--words", type=int, default=None)
    init.add_argument("--engine", default="jin-yong")
    assess = project_sub.add_parser("assess-capacity")
    assess.add_argument("--scale", default="standard")
    assess.add_argument("--words", type=int, default=None)
    assess.add_argument("--ranks", type=int, default=1)
    assess.add_argument("--factions", type=int, default=1)
    assess.add_argument("--motivations", type=int, default=1)
    assess.add_argument("--genre", default=None)
    project_verify = project_sub.add_parser("verify")
    project_verify.add_argument("root")
    engine = sub.add_parser("engine")
    engine_sub = engine.add_subparsers(dest="engine_command")
    validate = engine_sub.add_parser("validate")
    validate.add_argument("root")
    install = engine_sub.add_parser("install")
    install.add_argument("project")
    install.add_argument("source")
    use = engine_sub.add_parser("use")
    use.add_argument("project")
    use.add_argument("engine_id")
    manifest = engine_sub.add_parser("manifest")
    manifest.add_argument("root")
    distill = engine_sub.add_parser("distill")
    distill.add_argument("target", help="Action ('prepare', 'build') or source path")
    distill.add_argument("extra", nargs="?", default=None, help="Second argument (source for prepare, spec for build)")
    distill.add_argument("--id", dest="engine_id", default=None)
    distill.add_argument("--label", default=None)
    distill.add_argument("--output", default=None)
    distill.add_argument("--spec", default=None)
    blueprint = sub.add_parser("blueprint")
    blueprint_sub = blueprint.add_subparsers(dest="blueprint_command")
    bp_validate = blueprint_sub.add_parser("validate")
    bp_validate.add_argument("root")
    bp_validate.add_argument("chapter")
    context = sub.add_parser("context")
    context_sub = context.add_subparsers(dest="context_command")
    ctx_build = context_sub.add_parser("build")
    ctx_build.add_argument("root")
    ctx_build.add_argument("chapter")
    review = sub.add_parser("review")
    review_sub = review.add_subparsers(dest="review_command")
    review_apply = review_sub.add_parser("apply")
    review_apply.add_argument("root")
    review_apply.add_argument("artifact")
    settlement = sub.add_parser("settlement")
    settlement_sub = settlement.add_subparsers(dest="settlement_command")
    settlement_apply = settlement_sub.add_parser("apply")
    settlement_apply.add_argument("root")
    settlement_apply.add_argument("artifact")
    wiki = sub.add_parser("wiki")
    wiki_sub = wiki.add_subparsers(dest="wiki_command")
    wiki_rebuild = wiki_sub.add_parser("rebuild")
    wiki_rebuild.add_argument("root")
    chapter = sub.add_parser("chapter")
    chapter_sub = chapter.add_subparsers(dest="chapter_command")
    transition = chapter_sub.add_parser("transition")
    transition.add_argument("root")
    transition.add_argument("chapter")
    transition.add_argument("target")
    style = sub.add_parser("style")
    style_sub = style.add_subparsers(dest="style_command")
    style_detect = style_sub.add_parser("detect")
    style_detect.add_argument("file")
    pipeline = sub.add_parser("pipeline")
    pipeline_sub = pipeline.add_subparsers(dest="pipeline_command")
    p_status = pipeline_sub.add_parser("status")
    p_status.add_argument("root", nargs="?", default=".")
    p_status.add_argument("--chapter", default=None)
    p_advance = pipeline_sub.add_parser("advance")
    p_advance.add_argument("root", nargs="?", default=".")
    p_advance.add_argument("chapter", nargs="?", default=None)
    p_advance.add_argument("--stop-at", default=None)
    p_resume = pipeline_sub.add_parser("resume")
    p_resume.add_argument("root", nargs="?", default=".")
    p_resume.add_argument("chapter", nargs="?", default=None)
    p_resume.add_argument("--stop-at", default=None)
    p_interrupt = pipeline_sub.add_parser("interrupt")
    p_interrupt.add_argument("root", nargs="?", default=".")
    p_interrupt.add_argument("chapter", nargs="?", default=None)
    p_interrupt.add_argument("--reason", required=True)
    return parser


def dispatch(args):
    if args.command == "skill-audit":
        result = audit_builtin_core(args.root)
    elif args.command == "project" and args.project_command == "init":
        if args.genre or args.scale != "standard" or args.words:
            project_data = init_project_with_genesis(
                args.root,
                genre=args.genre,
                scale_tier=args.scale,
                target_words=args.words,
                engine=args.engine,
            )
            result = {"status": "PASS", "project": project_data}
        else:
            result = {"status": "PASS", "project": init_project(args.root)}
    elif args.command == "project" and args.project_command == "assess-capacity":
        result = evaluate_story_capacity(
            scale_tier=args.scale,
            target_words=args.words,
            progression_ranks=args.ranks,
            factions_count=args.factions,
            motivations_count=args.motivations,
            genre=args.genre,
        )
    elif args.command == "project" and args.project_command == "verify":
        result = verify_project(args.root)
    elif args.command == "engine" and args.engine_command == "validate":
        result = {"status": "PASS", "engine": load_engine(args.root)["id"]}
    elif args.command == "engine" and args.engine_command == "install":
        result = _engine_install(args.project, args.source)
    elif args.command == "engine" and args.engine_command == "use":
        result = activate_engine(args.project, args.engine_id)
    elif args.command == "engine" and args.engine_command == "manifest":
        result = write_manifest(args.root)
        result["verified"] = verify_manifest(args.root, result)
    elif args.command == "engine" and args.engine_command == "distill":
        if args.target == "prepare":
            source = args.extra
            if not source:
                raise ValueError("engine distill prepare requires a source path")
            result = prepare_distill(
                source,
                engine_id=args.engine_id,
                label=args.label,
                output_dir=args.output,
            )
        elif args.target == "build":
            spec = args.extra
            if not spec:
                raise ValueError("engine distill build requires a spec file path")
            result = build_distill_from_spec(
                spec,
                output_dir=args.output,
            )
        else:
            result = distill_engine(
                args.target,
                engine_id=args.engine_id,
                label=args.label,
                output_dir=args.output,
                spec_path=args.spec,
            )
    elif args.command == "blueprint" and args.blueprint_command == "validate":
        result = {"status": "PASS", "blueprint": validate_blueprint(args.root, args.chapter)}
    elif args.command == "context" and args.context_command == "build":
        result = build_context(args.root, args.chapter)
    elif args.command == "review" and args.review_command == "apply":
        result = apply_review(args.root, _read_artifact(args.artifact))
    elif args.command == "settlement" and args.settlement_command == "apply":
        result = apply_settlement(args.root, _read_artifact(args.artifact))
    elif args.command == "wiki" and args.wiki_command == "rebuild":
        result = rebuild_wiki(args.root)
    elif args.command == "chapter" and args.chapter_command == "transition":
        result = transition_chapter(args.root, args.chapter, args.target)
    elif args.command == "style" and args.style_command == "detect":
        path = Path(args.file)
        profile = _profile_for_path(path)
        result = detect_style(path.read_text(encoding="utf-8"), policy_for_profile(profile))
    elif args.command == "pipeline" and args.pipeline_command == "status":
        result = get_pipeline_status(args.root, args.chapter)
    elif args.command == "pipeline" and args.pipeline_command == "advance":
        result = advance_pipeline(args.root, args.chapter, stop_at=args.stop_at)
    elif args.command == "pipeline" and args.pipeline_command == "resume":
        result = resume_pipeline(args.root, args.chapter, stop_at=args.stop_at)
    elif args.command == "pipeline" and args.pipeline_command == "interrupt":
        result = interrupt_pipeline(args.root, args.chapter, reason=args.reason)
    else:
        raise ValueError("unknown or incomplete command")
    _json(result)
    return 0 if result.get("status", "PASS") not in ("FAIL", "ERROR") else 1


def _read_artifact(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv=None):
    try:
        parser = build_parser()
        return dispatch(parser.parse_args(argv))
    except (OSError, ValueError, KeyError) as exc:
        print("novelforgectl: {}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
