#!/usr/bin/env python3
"""Create a non-overwriting, review-oriented task documentation package."""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SAFE_SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


@dataclass(frozen=True)
class Part:
    part_id: str
    slug: str
    title: str
    filename: str


@dataclass(frozen=True)
class Worker:
    worker_id: str
    label: str


def parse_named_value(raw: str, *, option: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(f"{option} must use id=value syntax: {raw!r}")
    key, value = raw.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key or not value:
        raise ValueError(f"{option} requires non-empty id and value: {raw!r}")
    if not SAFE_SLUG.fullmatch(key):
        raise ValueError(f"{option} id must be lowercase slug text: {key!r}")
    return key, value


def parse_parts(raw_parts: list[str]) -> list[Part]:
    entries = raw_parts or ["main=Main task"]
    seen: set[str] = set()
    parts: list[Part] = []
    for index, raw in enumerate(entries, start=1):
        slug, title = parse_named_value(raw, option="--part")
        if slug in seen:
            raise ValueError(f"duplicate part slug: {slug}")
        seen.add(slug)
        part_id = f"T{index:02d}"
        parts.append(
            Part(
                part_id=part_id,
                slug=slug,
                title=title,
                filename=f"{index:02d}_{slug}.md",
            )
        )
    return parts


def parse_workers(raw_workers: list[str]) -> list[Worker]:
    workers: list[Worker] = []
    seen: set[str] = set()
    for raw in raw_workers:
        worker_id, label = parse_named_value(raw, option="--worker")
        if worker_id in seen:
            raise ValueError(f"duplicate worker id: {worker_id}")
        seen.add(worker_id)
        workers.append(Worker(worker_id=worker_id, label=label))
    return workers


def parse_assignments(
    raw_assignments: list[str], *, parts: list[Part], workers: list[Worker]
) -> dict[str, list[str]]:
    worker_ids = {worker.worker_id for worker in workers}
    part_ids = {part.part_id for part in parts}
    assignments = {worker.worker_id: [] for worker in workers}
    owner_by_part: dict[str, str] = {}

    for raw in raw_assignments:
        worker_id, part_list = parse_named_value(raw, option="--assign")
        if worker_id not in worker_ids:
            raise ValueError(f"--assign references unknown worker: {worker_id}")
        ids = [item.strip().upper() for item in part_list.split(",") if item.strip()]
        if not ids:
            raise ValueError(f"--assign has no part ids for worker: {worker_id}")
        for part_id in ids:
            if part_id not in part_ids:
                raise ValueError(f"--assign references unknown part id: {part_id}")
            prior = owner_by_part.get(part_id)
            if prior is not None:
                raise ValueError(
                    f"part {part_id} assigned more than once: {prior}, {worker_id}"
                )
            owner_by_part[part_id] = worker_id
            assignments[worker_id].append(part_id)

    missing = sorted(part_ids - owner_by_part.keys())
    if missing:
        raise ValueError(
            "parallel mode requires every part to be assigned exactly once; "
            f"missing: {', '.join(missing)}"
        )
    empty_workers = sorted(worker_id for worker_id, ids in assignments.items() if not ids)
    if empty_workers:
        raise ValueError(
            "parallel mode does not allow workers without assigned parts: "
            + ", ".join(empty_workers)
        )
    return assignments


def render_template(template_name: str, values: dict[str, str]) -> str:
    content = (ASSET_DIR / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", content)))
    if unresolved:
        raise ValueError(
            f"unresolved placeholders in {template_name}: {', '.join(unresolved)}"
        )
    return content


def write_rendered(
    destination: Path, template_name: str, values: dict[str, str]
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_template(template_name, values), encoding="utf-8")


def part_index(parts: list[Part]) -> str:
    return "\n".join(
        f"- [{part.part_id}: {part.title}](design/{part.filename})"
        for part in parts
    )


def point_rows(parts: list[Part]) -> str:
    return "\n".join(
        f"| `{part.part_id}-01` | `{part.part_id}` | `pending` | "
        f"[Design](design/{part.filename}) | To fill | To fill | To fill |"
        for part in parts
    )


def part_audit_rows(parts: list[Part]) -> str:
    return "\n".join(
        f"| `{part.part_id}` | no | `pending` | To fill |" for part in parts
    )


def assigned_parts_text(parts: list[Part], assigned_ids: list[str]) -> str:
    by_id = {part.part_id: part for part in parts}
    return ", ".join(
        f"`{part_id}` ({by_id[part_id].title})" for part_id in assigned_ids
    )


def worker_table(workers: list[Worker]) -> str:
    lines = [
        "| Worker | Label | Worker model | Session mode | Worker enforcement | Review mode | Reviewer | Reviewer source | Reviewer enforcement |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| `{worker.worker_id}` | {worker.label} | `gpt-5.6-sol/high` | "
        f"`fork_current` | `planned`; receipt to fill | `inherited_subagent` | "
        f"`reviewer-{worker.worker_id}` (inherits Worker settings) | "
        f"full Worker history at pre-execution boundary | `planned`; receipt to fill |"
        for worker in workers
    )
    return "\n".join(lines)


def build_single(temp_root: Path, *, common: dict[str, str], parts: list[Part]) -> None:
    readme_values = common | {
        "EXECUTION_MODE": "Single Worker",
        "DESIGN_INDEX": part_index(parts),
        "GOAL_INDEX": "",
        "EXECUTION_INDEX": "- [Worker execution record](execution/worker-main.md)",
        "REVIEW_INDEX": "- [Review record](review/reviewer-main.md)",
        "COORDINATION_INDEX": "",
    }
    write_rendered(temp_root / "README.md", "task-readme.md.tmpl", readme_values)
    write_rendered(
        temp_root / "GOAL.md",
        "goal-single.md.tmpl",
        common
        | {"POINT_ROWS": point_rows(parts), "PART_AUDIT_ROWS": part_audit_rows(parts)},
    )
    write_rendered(
        temp_root / "execution/worker-main.md",
        "execution.md.tmpl",
        common
        | {
            "WORKER_ID": "main",
            "GOAL_PATH": "`../GOAL.md`",
            "FIRST_POINT_ID": f"{parts[0].part_id}-01",
        },
    )
    write_rendered(
        temp_root / "review/reviewer-main.md",
        "review.md.tmpl",
        common
        | {
            "REVIEWER_ID": "reviewer-main",
            "WORKER_ID": "main",
            "FIRST_POINT_ID": f"{parts[0].part_id}-01",
        },
    )


def build_parallel(
    temp_root: Path,
    *,
    common: dict[str, str],
    parts: list[Part],
    workers: list[Worker],
    assignments: dict[str, list[str]],
) -> None:
    owner_by_part = {
        part_id: worker_id
        for worker_id, part_ids in assignments.items()
        for part_id in part_ids
    }
    readme_values = common | {
        "EXECUTION_MODE": "Confirmed parallel execution with per-lane review modes",
        "DESIGN_INDEX": part_index(parts),
        "GOAL_INDEX": "- Worker GOALs under `goals/`",
        "EXECUTION_INDEX": "- Worker execution records under `execution/`",
        "REVIEW_INDEX": "- Review records under `review/`",
        "COORDINATION_INDEX": "- [Parallel coordination entry](coordination/README.md)",
    }
    write_rendered(temp_root / "README.md", "task-readme.md.tmpl", readme_values)

    parallel_rows = "\n".join(
        f"| `{part.part_id}-01` | `{part.part_id}` | `{owner_by_part[part.part_id]}` | "
        f"`pending` | [GOAL](goals/{owner_by_part[part.part_id]}.md) | "
        f"[Execution](execution/{owner_by_part[part.part_id]}.md) | "
        f"[Review](review/reviewer-{owner_by_part[part.part_id]}.md) |"
        for part in parts
    )
    integration_rows = "\n".join(
        f"| `{part.part_id}` | no | no | Not run | `pending` |" for part in parts
    )
    write_rendered(
        temp_root / "GOAL.md",
        "goal-parallel-root.md.tmpl",
        common
        | {
            "WORKER_TABLE": worker_table(workers),
            "PARALLEL_POINT_ROWS": parallel_rows,
            "INTEGRATION_ROWS": integration_rows,
        },
    )

    for worker in workers:
        assigned_ids = assignments[worker.worker_id]
        assigned = [part for part in parts if part.part_id in assigned_ids]
        worker_rows = "\n".join(
            f"| `{part.part_id}-01` | `{part.part_id}` | `pending` | "
            f"[Design](../design/{part.filename}) | [Execution](../execution/{worker.worker_id}.md) | "
            f"[Review](../review/reviewer-{worker.worker_id}.md) |"
            for part in assigned
        )
        write_rendered(
            temp_root / f"goals/{worker.worker_id}.md",
            "goal-worker.md.tmpl",
            common
            | {
                "WORKER_ID": worker.worker_id,
                "WORKER_LABEL": worker.label,
                "ASSIGNED_PARTS": assigned_parts_text(parts, assigned_ids),
                "WORKER_POINT_ROWS": worker_rows,
            },
        )
        write_rendered(
            temp_root / f"execution/{worker.worker_id}.md",
            "execution.md.tmpl",
            common
            | {
                "WORKER_ID": worker.worker_id,
                "GOAL_PATH": f"`../goals/{worker.worker_id}.md`",
                "FIRST_POINT_ID": f"{assigned[0].part_id}-01",
            },
        )
        write_rendered(
            temp_root / f"review/reviewer-{worker.worker_id}.md",
            "review.md.tmpl",
            common
            | {
                "REVIEWER_ID": f"reviewer-{worker.worker_id}",
                "WORKER_ID": worker.worker_id,
                "FIRST_POINT_ID": f"{assigned[0].part_id}-01",
            },
        )

    write_rendered(
        temp_root / "coordination/README.md", "coordination-readme.md.tmpl", common
    )
    lane_sections = []
    for worker in workers:
        lane_sections.append(
            "\n".join(
                [
                    f"### Lane `{worker.worker_id}`: {worker.label}",
                    "",
                    f"- Assigned parts: {assigned_parts_text(parts, assignments[worker.worker_id])}",
                    f"- Reviewer: `reviewer-{worker.worker_id}`",
                    "- Impact scope: To fill.",
                    "- Write scope: To fill exact directories and files.",
                    "- Shared hotspots: To fill.",
                    "- No-touch scope: To fill.",
                    "- Branch/worktree/exact baseline: To fill.",
                    "- Worker task/session: To fill; default `fork_current`.",
                    "- Reviewer task/session: To fill; default `fork_worker_pre_execution`.",
                    "- Configuration provenance: current user / task package / same-family history / project default / skill default.",
                    "- Pre-execution fork point / execution dispatch time: To fill.",
                    "- Validation and delivery commit: To fill.",
                    "- Pause gates and notification targets: To fill.",
                    "- Conflict status: `pending`.",
                ]
            )
        )
    write_rendered(
        temp_root / "coordination/lanes.md",
        "lanes.md.tmpl",
        common | {"LANE_SECTIONS": "\n\n".join(lane_sections)},
    )
    integration_precheck = "\n".join(
        f"| `{worker.worker_id}` | no | To fill | no | no | `pending` |"
        for worker in workers
    )
    write_rendered(
        temp_root / "coordination/integration.md",
        "integration.md.tmpl",
        common | {"INTEGRATION_PRECHECK_ROWS": integration_precheck},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a dated task documentation package without overwriting files."
    )
    parser.add_argument("--parent", required=True, type=Path, help="Parent directory")
    parser.add_argument("--slug", required=True, help="Stable lowercase task slug")
    parser.add_argument("--title", required=True, help="Human-readable task title")
    parser.add_argument("--date", help="Frozen YYYY-MM-DD date; default: local date")
    parser.add_argument(
        "--document-language",
        default="English",
        help="Selected output language label; localize scaffold prose after generation",
    )
    parser.add_argument(
        "--part", action="append", default=[], metavar="SLUG=TITLE", help="Repeatable task part"
    )
    parser.add_argument("--parallel", action="store_true", help="Enable multi-worker structure")
    parser.add_argument(
        "--worker", action="append", default=[], metavar="ID=LABEL", help="Parallel worker"
    )
    parser.add_argument(
        "--assign",
        action="append",
        default=[],
        metavar="WORKER=T01,T02",
        help="Assign each task part exactly once in parallel mode",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if not SAFE_SLUG.fullmatch(args.slug):
            raise ValueError("--slug must be lowercase letters/digits with '-' or '_'")
        if not args.title.strip():
            raise ValueError("--title must not be blank")
        if not args.document_language.strip():
            raise ValueError("--document-language must not be blank")
        date = args.date or datetime.now().astimezone().date().isoformat()
        if not DATE_PATTERN.fullmatch(date):
            raise ValueError("--date must use YYYY-MM-DD")
        parts = parse_parts(args.part)
        workers = parse_workers(args.worker)
        if args.parallel:
            if len(workers) < 2:
                raise ValueError("--parallel requires at least two --worker entries")
            assignments = parse_assignments(args.assign, parts=parts, workers=workers)
        else:
            if workers or args.assign:
                raise ValueError("--worker/--assign require --parallel")
            assignments = {}

        parent = args.parent.expanduser().resolve()
        parent.mkdir(parents=True, exist_ok=True)
        task_dir_name = f"{date}_{args.slug}"
        target = parent / task_dir_name
        if target.exists():
            raise ValueError(f"target already exists; refusing to overwrite: {target}")

        common = {
            "TASK_TITLE": args.title.strip(),
            "TASK_DIR_NAME": task_dir_name,
            "DATE": date,
            "DOCUMENT_LANGUAGE": args.document_language.strip(),
        }
        temp_root = Path(tempfile.mkdtemp(prefix=f".{task_dir_name}.", dir=parent))
        try:
            write_rendered(
                temp_root / "design/00_discussion-decisions.md",
                "discussion-decisions.md.tmpl",
                common,
            )
            for part in parts:
                write_rendered(
                    temp_root / f"design/{part.filename}",
                    "part-design.md.tmpl",
                    common | {"PART_ID": part.part_id, "PART_TITLE": part.title},
                )
            if args.parallel:
                build_parallel(
                    temp_root,
                    common=common,
                    parts=parts,
                    workers=workers,
                    assignments=assignments,
                )
            else:
                build_single(temp_root, common=common, parts=parts)
            temp_root.rename(target)
        except Exception:
            shutil.rmtree(temp_root, ignore_errors=True)
            raise
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
