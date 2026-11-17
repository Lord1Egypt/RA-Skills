#!/usr/bin/env python3
"""Initialize and advance a privacy-preserving voiceover-video job."""

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


STAGES = [
    "01-intake",
    "02-timing",
    "03-editorial",
    "04-storyboard",
    "05-visuals",
    "06-edit",
    "07-qc",
]

STAGE_DIRS = ["00-source", *STAGES, "08-delivery"]

REQUIRED = {
    "01-intake": ["01-intake/input-report.json"],
    "02-timing": [
        "02-timing/audio-report.json",
        "02-timing/timing.json",
        "02-timing/segments.json",
        "02-timing/subtitles.srt",
    ],
    "03-editorial": ["03-editorial/editorial-brief.json"],
    "04-storyboard": ["04-storyboard/storyboard.json"],
    "05-visuals": ["05-visuals/visual-manifest.json"],
    "06-edit": ["06-edit/composition-report.json", "08-delivery/final.mp4"],
    "07-qc": [
        "07-qc/qc-report.json",
        "08-delivery/final.mp4",
        "08-delivery/cover.png",
        "08-delivery/publish-copy.json",
    ],
}


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_json(value) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_name(index: int, source: Path) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", source.name).strip("-")
    return f"{index:03d}-{name or 'source'}"


def command_init(args) -> None:
    root = Path(args.job_dir).expanduser().resolve()
    article = Path(args.article).expanduser().resolve()
    audio = Path(args.audio).expanduser().resolve()
    images = [Path(item).expanduser().resolve() for item in args.images]
    videos = [Path(item).expanduser().resolve() for item in args.videos]
    if not 0.5 <= args.source_video_speed <= 2.0:
        raise SystemExit("Source-video speed must be between 0.5 and 2.0")

    for item in [article, audio, *images, *videos]:
        if not item.is_file():
            raise SystemExit(f"Missing input: {item.name}")
    if root.exists():
        raise SystemExit("Refusing to overwrite an existing job directory")

    root.mkdir(parents=True)
    for stage_dir in STAGE_DIRS:
        (root / stage_dir).mkdir()
    (root / "05-visuals" / "assets").mkdir()
    (root / "06-edit" / "chunks").mkdir()

    sources = []
    source_specs = (
        [("article", article), ("audio", audio)]
        + [("image", image) for image in images]
        + [("video", video) for video in videos]
    )
    for index, (kind, source_path) in enumerate(source_specs, start=1):
        target = root / "00-source" / safe_name(index, source_path)
        shutil.copy2(source_path, target)
        sources.append(
            {
                "kind": kind,
                "path": target.relative_to(root).as_posix(),
                "sha256": hash_file(target),
                "bytes": target.stat().st_size,
            }
        )

    source_manifest = {"schema_version": 1, "sources": sources}
    write_json(root / "00-source" / "source-manifest.json", source_manifest)

    config = {
        "mode": args.mode,
        "speech_rate": args.speech_rate,
        "target_minutes": args.target_minutes,
        "canvas": {"width": 1080, "height": 1920, "fps": 30},
        "source_video": {
            "mode": "interlude",
            "speed": args.source_video_speed,
            "audio": "original-only",
            "narration": "pause-resume",
            "captions": "pause-resume",
        },
        "delivery": {
            "canonical_path": "08-delivery/final.mp4",
            "atomic_replace": True,
            "duplicate_versions": False,
        },
    }
    now = datetime.now(timezone.utc).isoformat()
    title = args.title or article.stem
    job = {
        "schema_version": 1,
        "job_id": f"{datetime.now().strftime('%Y%m%d')}-{hash_json(source_manifest)[:10]}",
        "title": title,
        "stage": STAGES[0],
        "status": "running",
        "config": config,
        "source_manifest": "00-source/source-manifest.json",
        "input_hash": hash_json(source_manifest),
        "config_hash": hash_json(config),
        "cache_key": hash_json({"sources": source_manifest, "config": config}),
        "outputs": {},
        "history": [{"event": "initialized", "at": now}],
    }
    write_json(root / "job.json", job)
    print(json.dumps({"job_id": job["job_id"], "stage": job["stage"]}))


def validate_stage(root: Path, stage: str):
    if stage not in REQUIRED:
        raise SystemExit(f"Unknown stage: {stage}")
    missing = [path for path in REQUIRED[stage] if not (root / path).is_file()]
    errors = []
    report_path = root / REQUIRED[stage][0]
    if report_path.is_file() and report_path.suffix == ".json":
        try:
            report = load_json(report_path)
            if report.get("stage") != stage:
                errors.append(f"Report stage is {report.get('stage')!r}")
            if report.get("status") not in {"pass", "needs-human", "fail"}:
                errors.append("Report has an invalid status")
            if report.get("status") == "fail":
                errors.append("Worker reported fail")
        except Exception as exc:
            errors.append(f"Invalid report JSON: {exc}")
    return {"stage": stage, "ok": not missing and not errors, "missing": missing, "errors": errors}


def command_validate(args) -> None:
    root = Path(args.job_dir).expanduser().resolve()
    result = validate_stage(root, args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


def command_advance(args) -> None:
    root = Path(args.job_dir).expanduser().resolve()
    job_path = root / "job.json"
    job = load_json(job_path)
    if job.get("stage") != args.stage:
        raise SystemExit(f"Current stage is {job.get('stage')}, not {args.stage}")
    result = validate_stage(root, args.stage)
    if not result["ok"]:
        raise SystemExit(json.dumps(result, ensure_ascii=False))

    report_path = root / REQUIRED[args.stage][0]
    report = load_json(report_path)
    if report.get("status") != "pass":
        raise SystemExit(f"Cannot advance with status {report.get('status')!r}")

    index = STAGES.index(args.stage)
    next_stage = STAGES[index + 1] if index + 1 < len(STAGES) else "complete"
    job["stage"] = next_stage
    job["status"] = "complete" if next_stage == "complete" else "running"
    job["outputs"][args.stage] = {
        "report": report_path.relative_to(root).as_posix(),
        "sha256": hash_file(report_path),
    }
    job["history"].append(
        {
            "event": "handoff",
            "from": args.stage,
            "to": next_stage,
            "worker": report.get("worker", "unknown"),
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_json(job_path, job)
    print(json.dumps({"from": args.stage, "to": next_stage}))


def command_status(args) -> None:
    root = Path(args.job_dir).expanduser().resolve()
    job = load_json(root / "job.json")
    summary = {
        "job_id": job.get("job_id"),
        "stage": job.get("stage"),
        "status": job.get("status"),
        "mode": job.get("config", {}).get("mode"),
        "cache_key": job.get("cache_key"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    init_parser.add_argument("--job-dir", required=True)
    init_parser.add_argument("--article", required=True)
    init_parser.add_argument("--audio", required=True)
    init_parser.add_argument("--images", nargs="*", default=[])
    init_parser.add_argument("--videos", nargs="*", default=[])
    init_parser.add_argument("--title", default="")
    init_parser.add_argument("--mode", choices=("fast", "balanced", "quality"), default="fast")
    init_parser.add_argument("--speech-rate", type=float, default=1.0)
    init_parser.add_argument("--source-video-speed", type=float, default=1.0)
    init_parser.add_argument("--target-minutes", default="")
    init_parser.set_defaults(handler=command_init)

    for name, handler in (("validate", command_validate), ("advance", command_advance)):
        stage_parser = commands.add_parser(name)
        stage_parser.add_argument("--job-dir", required=True)
        stage_parser.add_argument("--stage", choices=STAGES, required=True)
        stage_parser.set_defaults(handler=handler)

    status_parser = commands.add_parser("status")
    status_parser.add_argument("--job-dir", required=True)
    status_parser.set_defaults(handler=command_status)
    return parser


def main():
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
