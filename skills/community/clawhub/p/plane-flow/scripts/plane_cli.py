from __future__ import annotations

import argparse
import json
import sys
from typing import Any

try:
    from .client import PlaneAPIError, PlaneClient
    from .config import load_settings
    from .service import PlaneService, PlaneServiceError
except ImportError:
    from client import PlaneAPIError, PlaneClient
    from config import load_settings
    from service import PlaneService, PlaneServiceError


def build_service() -> PlaneService:
    settings = load_settings()
    client = PlaneClient(
        base_url=settings.base_url,
        api_token=settings.api_token,
        workspace_id=settings.workspace_id,
    )
    return PlaneService(client=client, settings=settings)


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_projects_list(
    service: PlaneService, args: argparse.Namespace
) -> int:
    projects = service.list_projects()

    if args.raw:
        print_json(projects)
        return 0

    output = [
        {
            "id": p.get("id"),
            "name": p.get("name"),
            "identifier": p.get("identifier"),
        }
        for p in projects
    ]
    print_json(output)
    return 0


def cmd_projects_summary(
    service: PlaneService, args: argparse.Namespace
) -> int:
    summary = service.summarize_project(args.project)
    print_json(summary)
    return 0


def cmd_issues_list(
    service: PlaneService, args: argparse.Namespace
) -> int:
    issues = service.list_issues(
        project=args.project,
        state=args.state,
        assignee_id=args.assignee_id,
        priority=args.priority,
        label_id=args.label_id,
        cycle_id=args.cycle_id,
    )

    if args.raw:
        print_json(issues)
        return 0

    output = [
        service.summarize_issue(issue)
        for issue in issues
    ]
    print_json([vars(s) for s in output])
    return 0


def cmd_issues_get(
    service: PlaneService, args: argparse.Namespace
) -> int:
    issue = service.get_issue_detail(args.id, project=args.project)
    print_json(issue)
    return 0


def cmd_issues_create(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.create_issue(
        title=args.title,
        description=args.desc,
        project=args.project,
        priority=args.priority,
        state=args.state,
        image_paths=args.image,
        image_align=args.image_align,
    )
    print_json(result)
    return 0



def cmd_issues_update_desc(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.update_issue_description(
        issue_id=args.id,
        description=args.desc,
        project=args.project,
        image_paths=args.image,
        image_align=args.image_align,
    )
    print_json(result)
    return 0



def cmd_issues_move(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.move_issue(
        issue_id=args.id,
        target_state=args.state,
        project=args.project,
    )
    print_json(result)
    return 0


def cmd_issues_assign(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.assign_issue(
        issue_id=args.id,
        assignee=args.assignee,
        project=args.project,
    )
    print_json(result)
    return 0


def cmd_issues_set_priority(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.set_issue_priority(
        issue_id=args.id,
        priority=args.priority,
        project=args.project,
    )
    print_json(result)
    return 0


def cmd_issues_set_labels(
    service: PlaneService, args: argparse.Namespace
) -> int:
    labels = [x.strip() for x in args.labels.split(",") if x.strip()]
    result = service.set_issue_labels(
        issue_id=args.id,
        labels=labels,
        project=args.project,
    )
    print_json(result)
    return 0


def cmd_issues_upload(
    service: PlaneService, args: argparse.Namespace
) -> int:
    result = service.upload_attachment(
        issue_id=args.id,
        file_path=args.file,
        project=args.project,
    )
    print_json(result)
    return 0


def cmd_cycles_list(service: PlaneService, args: argparse.Namespace) -> int:
    cycles = service.list_cycles(project=args.project)
    if args.raw:
        print_json(cycles)
        return 0
    output = [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "status": c.get("status"),
            "start_date": c.get("start_date"),
            "end_date": c.get("end_date"),
            "total_issues": c.get("total_issues"),
        }
        for c in cycles
    ]
    print_json(output)
    return 0


def cmd_cycles_create(service: PlaneService, args: argparse.Namespace) -> int:
    result = service.create_cycle(
        project=args.project,
        name=args.name,
        description=args.desc,
        start_date=args.start,
        end_date=args.end,
    )
    print_json(result)
    return 0


def cmd_cycles_add_issues(service: PlaneService, args: argparse.Namespace) -> int:
    issue_ids = [x.strip() for x in args.issues.split(",") if x.strip()]
    result = service.add_issues_to_cycle(
        project=args.project,
        cycle_id=args.cycle_id,
        issue_ids=issue_ids,
    )
    print_json(result)
    return 0


def cmd_cycles_remove_issue(service: PlaneService, args: argparse.Namespace) -> int:
    service.remove_issue_from_cycle(
        project=args.project,
        cycle_id=args.cycle_id,
        issue_id=args.issue_id,
    )
    print_json({"ok": True})
    return 0


def cmd_comments_list(service: PlaneService, args: argparse.Namespace) -> int:
    comments = service.list_comments(issue_id=args.issue_id, project=args.project)
    if args.raw:
        print_json(comments)
        return 0
    output = [
        {
            "id": c.get("id"),
            "created_at": c.get("created_at"),
            "created_by": c.get("created_by"),
            "content_html": c.get("content_html", "")[:100],
        }
        for c in comments
    ]
    print_json(output)
    return 0


def cmd_comments_create(service: PlaneService, args: argparse.Namespace) -> int:
    result = service.create_comment(
        issue_id=args.issue_id,
        content=args.content,
        project=args.project,
        image_paths=args.image,
        image_align=args.image_align,
    )
    print_json(result)
    return 0



def cmd_create_project(service: PlaneService, args: argparse.Namespace) -> int:
    result = service.create_project(
        name=args.name,
        identifier=args.identifier,
        description=args.desc,
    )
    print_json(result)
    return 0


def cmd_states_list(
    service: PlaneService, args: argparse.Namespace
) -> int:
    states = service.list_states(project=args.project)
    if args.raw:
        print_json(states)
        return 0

    output = [
        {
            "id": s.get("id"),
            "name": s.get("name"),
            "group": s.get("group"),
            "slug": s.get("slug"),
            "default": s.get("default"),
        }
        for s in states
    ]
    print_json(output)
    return 0


def cmd_labels_list(
    service: PlaneService, args: argparse.Namespace
) -> int:
    labels = service.list_labels(project=args.project)
    if args.raw:
        print_json(labels)
        return 0

    output = [
        {
            "id": l.get("id"),
            "name": l.get("name"),
            "color": l.get("color"),
        }
        for l in labels
    ]
    print_json(output)
    return 0


def cmd_members_list(
    service: PlaneService, args: argparse.Namespace
) -> int:
    members = service.list_members()
    if args.raw:
        print_json(members)
        return 0

    output = []
    for m in members:
        member = m.get("member") if isinstance(m.get("member"), dict) else m
        output.append(
            {
                "id": member.get("id"),
                "name": member.get("display_name") or member.get("name"),
                "email": member.get("email"),
            }
        )
    print_json(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="plane-cli",
        description="Local Plane integration CLI",
    )

    subparsers = parser.add_subparsers(dest="resource", required=True)

    # ---- projects ----
    proj_parser = subparsers.add_parser(
        "projects", help="Project operations"
    )
    proj_sub = proj_parser.add_subparsers(dest="action", required=True)

    proj_list = proj_sub.add_parser("list", help="List projects")
    proj_list.add_argument(
        "--raw", action="store_true", help="Print raw API data"
    )

    proj_summary = proj_sub.add_parser("summary", help="Summarize project")
    proj_summary.add_argument(
        "--project", required=True, help="Project name or alias"
    )

    # ---- states ----
    state_parser = subparsers.add_parser("states", help="State operations")
    state_sub = state_parser.add_subparsers(dest="action", required=True)

    state_list = state_sub.add_parser("list", help="List states")
    state_list.add_argument("--project", help="Project name or alias")
    state_list.add_argument(
        "--raw", action="store_true", help="Print raw API data"
    )

    # ---- labels ----
    label_parser = subparsers.add_parser("labels", help="Label operations")
    label_sub = label_parser.add_subparsers(dest="action", required=True)

    label_list = label_sub.add_parser("list", help="List labels")
    label_list.add_argument("--project", help="Project name or alias")
    label_list.add_argument(
        "--raw", action="store_true", help="Print raw API data"
    )

    # ---- members ----
    member_parser = subparsers.add_parser("members", help="Member operations")
    member_sub = member_parser.add_subparsers(dest="action", required=True)

    member_list = member_sub.add_parser("list", help="List workspace members")
    member_list.add_argument(
        "--raw", action="store_true", help="Print raw API data"
    )

    # ---- issues ----
    issue_parser = subparsers.add_parser(
        "issues", help="Issue operations"
    )
    issue_sub = issue_parser.add_subparsers(dest="action", required=True)

    issue_list = issue_sub.add_parser("list", help="List issues")
    issue_list.add_argument("--project", help="Project name or alias")
    issue_list.add_argument("--state", help="State name")
    issue_list.add_argument("--priority", help="Priority")
    issue_list.add_argument("--assignee-id", help="Assignee ID")
    issue_list.add_argument("--label-id", help="Label ID")
    issue_list.add_argument("--cycle-id", help="Cycle ID")
    issue_list.add_argument(
        "--raw", action="store_true", help="Print raw API data"
    )

    issue_get = issue_sub.add_parser("get", help="Get issue detail")
    issue_get.add_argument(
        "--id", required=True, help="Issue ID"
    )
    issue_get.add_argument("--project", required=True, help="Project name or alias")

    issue_create = issue_sub.add_parser("create", help="Create issue")
    issue_create.add_argument(
        "--title", required=True, help="Issue title"
    )
    issue_create.add_argument(
        "--desc", required=True, help="Issue description"
    )
    issue_create.add_argument("--project", help="Project name or alias")
    issue_create.add_argument("--priority", help="Priority")
    issue_create.add_argument("--state", help="Initial state name")
    issue_create.add_argument("--image", action="append", default=[], help="Path to an image to upload and embed in description (repeatable)")
    issue_create.add_argument(
        "--image-align",
        default="center",
        choices=["left", "center", "right"],
        help="Alignment for all --image images (default: center)",
    )


    issue_update_desc = issue_sub.add_parser(
        "update-desc", help="Update issue description"
    )
    issue_update_desc.add_argument(
        "--id", required=True, help="Issue ID"
    )
    issue_update_desc.add_argument("--project", required=True, help="Project name or alias")
    issue_update_desc.add_argument(
        "--desc", required=True, help="New issue description"
    )
    issue_update_desc.add_argument("--image", action="append", default=[], help="Path to an image to upload and embed in description (repeatable)")
    issue_update_desc.add_argument(
        "--image-align",
        default="center",
        choices=["left", "center", "right"],
        help="Alignment for all --image images (default: center)",
    )


    issue_move = issue_sub.add_parser(
        "move", help="Move issue to another state"
    )
    issue_move.add_argument(
        "--id", required=True, help="Issue ID"
    )
    issue_move.add_argument(
        "--state", required=True, help="Target state name"
    )
    issue_move.add_argument("--project", help="Project name or alias")

    issue_assign = issue_sub.add_parser("assign", help="Assign issue to a member")
    issue_assign.add_argument("--id", required=True, help="Issue ID")
    issue_assign.add_argument("--project", required=True, help="Project name or alias")
    issue_assign.add_argument("--assignee", required=True, help="Member name, email, or ID")

    issue_set_priority = issue_sub.add_parser(
        "set-priority", help="Set issue priority"
    )
    issue_set_priority.add_argument("--id", required=True, help="Issue ID")
    issue_set_priority.add_argument("--project", required=True, help="Project name or alias")
    issue_set_priority.add_argument("--priority", required=True, help="Priority")

    issue_set_labels = issue_sub.add_parser(
        "set-labels", help="Set issue labels (comma-separated)"
    )
    issue_set_labels.add_argument("--id", required=True, help="Issue ID")
    issue_set_labels.add_argument("--project", required=True, help="Project name or alias")
    issue_set_labels.add_argument("--labels", required=True, help="Comma-separated label names")

    issue_upload = issue_sub.add_parser(
        "upload", help="Upload a file as an attachment to an issue"
    )
    issue_upload.add_argument("--id", required=True, help="Issue ID")
    issue_upload.add_argument("--project", required=True, help="Project name or alias")
    issue_upload.add_argument("--file", required=True, help="Path to file to upload")

    # ---- cycles ----
    cycle_parser = subparsers.add_parser("cycles", help="Cycle/Sprint operations")
    cycle_sub = cycle_parser.add_subparsers(dest="action", required=True)

    cycle_list = cycle_sub.add_parser("list", help="List cycles")
    cycle_list.add_argument("--project", required=True, help="Project name or alias")
    cycle_list.add_argument("--raw", action="store_true", help="Print raw API data")

    cycle_create = cycle_sub.add_parser("create", help="Create a cycle")
    cycle_create.add_argument("--project", required=True, help="Project name or alias")
    cycle_create.add_argument("--name", required=True, help="Cycle name")
    cycle_create.add_argument("--desc", default="", help="Cycle description")
    cycle_create.add_argument("--start", help="Start date (YYYY-MM-DD)")
    cycle_create.add_argument("--end", help="End date (YYYY-MM-DD)")

    cycle_add_issues = cycle_sub.add_parser("add-issues", help="Add issues to a cycle")
    cycle_add_issues.add_argument("--project", required=True, help="Project name or alias")
    cycle_add_issues.add_argument("--cycle-id", required=True, help="Cycle ID")
    cycle_add_issues.add_argument("--issues", required=True, help="Comma-separated issue IDs")

    cycle_remove_issue = cycle_sub.add_parser("remove-issue", help="Remove an issue from a cycle")
    cycle_remove_issue.add_argument("--project", required=True, help="Project name or alias")
    cycle_remove_issue.add_argument("--cycle-id", required=True, help="Cycle ID")
    cycle_remove_issue.add_argument("--issue-id", required=True, help="Issue ID")

    # ---- comments ----
    comment_parser = subparsers.add_parser("comments", help="Comment operations")
    comment_sub = comment_parser.add_subparsers(dest="action", required=True)

    comment_list = comment_sub.add_parser("list", help="List comments on an issue")
    comment_list.add_argument("--issue-id", required=True, help="Issue ID")
    comment_list.add_argument("--project", required=True, help="Project name or alias")
    comment_list.add_argument("--raw", action="store_true", help="Print raw API data")

    comment_create = comment_sub.add_parser("create", help="Add a comment to an issue")
    comment_create.add_argument("--issue-id", required=True, help="Issue ID")
    comment_create.add_argument("--project", required=True, help="Project name or alias")
    comment_create.add_argument("--content", required=True, help="Comment content (supports markdown)")
    comment_create.add_argument("--image", action="append", default=[], help="Path to an image to upload and embed in comment (repeatable)")
    comment_create.add_argument(
        "--image-align",
        default="center",
        choices=["left", "center", "right"],
        help="Alignment for all images in this comment (default: center)",
    )


    # ---- projects ----
    project_create = subparsers.add_parser(
        "create-project", help="Create a new project"
    )
    project_create.add_argument("--name", required=True, help="Project name")
    project_create.add_argument("--identifier", required=True, help="Project identifier (e.g. PROJ)")
    project_create.add_argument("--desc", default="", help="Project description")

    return parser


def dispatch(
    service: PlaneService, args: argparse.Namespace
) -> int:
    if args.resource == "projects":
        if args.action == "list":
            return cmd_projects_list(service, args)
        if args.action == "summary":
            return cmd_projects_summary(service, args)

    if args.resource == "states":
        if args.action == "list":
            return cmd_states_list(service, args)

    if args.resource == "labels":
        if args.action == "list":
            return cmd_labels_list(service, args)

    if args.resource == "members":
        if args.action == "list":
            return cmd_members_list(service, args)

    if args.resource == "issues":
        if args.action == "list":
            return cmd_issues_list(service, args)
        if args.action == "get":
            return cmd_issues_get(service, args)
        if args.action == "create":
            return cmd_issues_create(service, args)
        if args.action == "update-desc":
            return cmd_issues_update_desc(service, args)
        if args.action == "move":
            return cmd_issues_move(service, args)
        if args.action == "assign":
            return cmd_issues_assign(service, args)
        if args.action == "set-priority":
            return cmd_issues_set_priority(service, args)
        if args.action == "set-labels":
            return cmd_issues_set_labels(service, args)
        if args.action == "upload":
            return cmd_issues_upload(service, args)

    if args.resource == "cycles":
        if args.action == "list":
            return cmd_cycles_list(service, args)
        if args.action == "create":
            return cmd_cycles_create(service, args)
        if args.action == "add-issues":
            return cmd_cycles_add_issues(service, args)
        if args.action == "remove-issue":
            return cmd_cycles_remove_issue(service, args)

    if args.resource == "comments":
        if args.action == "list":
            return cmd_comments_list(service, args)
        if args.action == "create":
            return cmd_comments_create(service, args)

    if args.resource == "create-project":
        return cmd_create_project(service, args)

    raise PlaneServiceError(
        f"Unsupported command: {args.resource} {args.action}"
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        service = build_service()
        return dispatch(service, args)
    except (
        PlaneAPIError,
        PlaneServiceError,
        RuntimeError,
        ValueError,
    ) as e:
        print(
            json.dumps({"error": str(e)}, ensure_ascii=False, indent=2),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
