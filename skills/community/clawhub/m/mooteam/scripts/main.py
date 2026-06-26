#!/usr/bin/env python3
import argparse
import sys
import json
from MooTeamClient import MooTeamClient

def main():
    parser = argparse.ArgumentParser(description="MooTeam API CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # --- Teams ---
    subparsers.add_parser("user-profiles")

    # --- Projects ---
    subparsers.add_parser("projects")
    
    pc = subparsers.add_parser("project-create")
    pc.add_argument("--name", required=True)
    pc.add_argument("--workflow_id", type=int, required=True)
    
    pi = subparsers.add_parser("project-info")
    pi.add_argument("--id", type=int, required=True)
    
    pu = subparsers.add_parser("project-update")
    pu.add_argument("--id", type=int, required=True)
    pu.add_argument("--name", required=True)
    
    pd = subparsers.add_parser("project-delete")
    pd.add_argument("--id", type=int, required=True)
    pd.add_argument("--force", action="store_true")

    pta = subparsers.add_parser("project-team-add")
    pta.add_argument("--project", type=int, required=True)
    pta.add_argument("--user", type=int, required=True)

    ptr = subparsers.add_parser("project-team-remove")
    ptr.add_argument("--map_id", type=int, required=True)

    # --- Tasks ---
    ts = subparsers.add_parser("tasks")
    ts.add_argument("--project", type=int)

    tc = subparsers.add_parser("task-create")
    tc.add_argument("--project", type=int, required=True)
    tc.add_argument("--header", required=True)
    tc.add_argument("--user_id", type=int)

    ti = subparsers.add_parser("task-info")
    ti.add_argument("--id", type=int, required=True)

    tu = subparsers.add_parser("task-update")
    tu.add_argument("--id", type=int, required=True)
    tu.add_argument("--header")
    tu.add_argument("--status_id", type=int)

    tde = subparsers.add_parser("task-delete")
    tde.add_argument("--id", type=int, required=True)

    # --- Drafts ---
    subparsers.add_parser("task-draft")
    
    tdu = subparsers.add_parser("task-draft-update")
    tdu.add_argument("--header")
    tdu.add_argument("--project", type=int)
    
    subparsers.add_parser("task-from-draft")

    # --- Comments ---
    cms = subparsers.add_parser("comments")
    cms.add_argument("--task_id", type=int, required=True)
    
    cmc = subparsers.add_parser("comment-create")
    cmc.add_argument("--task_id", type=int, required=True)
    cmc.add_argument("--text", required=True)
    
    cmd = subparsers.add_parser("comment-delete")
    cmd.add_argument("--id", type=int, required=True)

    # --- Workflows & Statuses ---
    subparsers.add_parser("workflows")
    
    wfc = subparsers.add_parser("workflow-create")
    wfc.add_argument("--name", required=True)
    
    wfi = subparsers.add_parser("workflow-info")
    wfi.add_argument("--id", type=int, required=True)
    
    wfu = subparsers.add_parser("workflow-update")
    wfu.add_argument("--id", type=int, required=True)
    wfu.add_argument("--name", required=True)
    
    wfd = subparsers.add_parser("workflow-delete")
    wfd.add_argument("--id", type=int, required=True)

    subparsers.add_parser("statuses")
    
    sc = subparsers.add_parser("status-create")
    sc.add_argument("--name", required=True)
    sc.add_argument("--workflow_id", type=int, required=True)
    
    si = subparsers.add_parser("status-info")
    si.add_argument("--id", type=int, required=True)
    
    su = subparsers.add_parser("status-update")
    su.add_argument("--id", type=int, required=True)
    su.add_argument("--name", required=True)
    
    sde = subparsers.add_parser("status-delete")
    sde.add_argument("--id", type=int, required=True)

    # --- Labels ---
    subparsers.add_parser("label-groups")
    
    lgc = subparsers.add_parser("label-group-create")
    lgc.add_argument("--name", required=True)
    
    lgu = subparsers.add_parser("label-group-update")
    lgu.add_argument("--id", type=int, required=True)
    lgu.add_argument("--name", required=True)
    
    lgd = subparsers.add_parser("label-group-delete")
    lgd.add_argument("--id", type=int, required=True)

    subparsers.add_parser("labels")
    
    lc = subparsers.add_parser("label-create")
    lc.add_argument("--group", type=int, required=True)
    lc.add_argument("--name", required=True)
    lc.add_argument("--color")
    
    li = subparsers.add_parser("label-info")
    li.add_argument("--id", type=int, required=True)
    
    lu = subparsers.add_parser("label-update")
    lu.add_argument("--id", type=int, required=True)
    lu.add_argument("--name")
    lu.add_argument("--color")
    
    ld = subparsers.add_parser("label-delete")
    ld.add_argument("--id", type=int, required=True)

    # --- Timer & Time Logs ---
    subparsers.add_parser("timer-current")
    
    tlc = subparsers.add_parser("time-create")
    tlc.add_argument("--task_id", type=int, required=True)
    tlc.add_argument("--seconds", type=int, required=True)
    
    tlu = subparsers.add_parser("time-update")
    tlu.add_argument("--id", type=int, required=True)
    tlu.add_argument("--seconds", type=int, required=True)
    
    tld = subparsers.add_parser("time-delete")
    tld.add_argument("--id", type=int, required=True)

    st = subparsers.add_parser("start")
    st.add_argument("task_id", type=int)
    
    subparsers.add_parser("stop")
    
    ttl = subparsers.add_parser("task-time")
    ttl.add_argument("--task_id", type=int, required=True)
    
    subparsers.add_parser("time-list")

    # --- Activity ---
    act = subparsers.add_parser("activity")
    act.add_argument("--project", type=int)
    act.add_argument("--user", type=int)
    act.add_argument("--type")
    
    subparsers.add_parser("activity-projects")

    args = parser.parse_args()

    # --- Logic Mapping ---
    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        from rich.console import Console
        from rich.table import Table
        from rich.json import JSON as RichJSON
        from rich.panel import Panel
        console = Console()
    except ImportError:
        console = None

    client = MooTeamClient()
    result = {"error": "Unknown command"}
    
    # ... (logic mapping remains same until result processing) ...
    # (re-pasting the logic mapping here to ensure it's correct)
    if args.command == "user-profiles":
        result = client.get_user_profiles()
    elif args.command == "projects":
        result = client.get_projects()
    elif args.command == "project-create":
        result = client.create_project(args.name, args.workflow_id)
    elif args.command == "project-info":
        result = client.get_project_details(args.id)
    elif args.command == "project-update":
        result = client.update_project(args.id, {"name": args.name})
    elif args.command == "project-delete":
        result = client.delete_project(args.id)
    elif args.command == "project-team-add":
        result = client.add_team_member(args.project, args.user)
    elif args.command == "project-team-remove":
        result = client.remove_team_member(args.map_id)
    elif args.command == "tasks":
        result = client.get_tasks(args.project)
    elif args.command == "task-create":
        result = client.create_task(args.project, args.header, userId=args.user_id)
    elif args.command == "task-info":
        result = client.get_task_details(args.id)
    elif args.command == "task-update":
        data = {}
        if args.header: data["header"] = args.header
        if args.status_id: data["statusId"] = args.status_id
        result = client.update_task(args.id, data)
    elif args.command == "task-delete":
        result = client.delete_task(args.id)
    elif args.command == "task-draft":
        result = client.get_task_draft()
    elif args.command == "task-draft-update":
        data = {}
        if args.header: data["header"] = args.header
        if args.project: data["projectId"] = args.project
        result = client.update_task_draft(data)
    elif args.command == "task-from-draft":
        result = client.create_task_from_draft()
    elif args.command == "comments":
        result = client.get_comments(args.task_id)
    elif args.command == "comment-create":
        result = client.create_comment(args.task_id, args.text)
    elif args.command == "comment-delete":
        result = client.delete_comment(args.id)
    elif args.command == "workflows":
        result = client.get_workflows()
    elif args.command == "workflow-create":
        result = client.create_workflow(args.name)
    elif args.command == "workflow-info":
        result = client.get_workflow_details(args.id)
    elif args.command == "workflow-update":
        result = client.update_workflow(args.id, args.name)
    elif args.command == "workflow-delete":
        result = client.delete_workflow(args.id)
    elif args.command == "statuses":
        result = client.get_statuses()
    elif args.command == "status-create":
        result = client.create_status(args.name, args.workflow_id)
    elif args.command == "status-info":
        result = client.get_status_details(args.id)
    elif args.command == "status-update":
        result = client.update_status(args.id, args.name)
    elif args.command == "status-delete":
        result = client.delete_status(args.id)
    elif args.command == "label-groups":
        result = client.get_label_groups()
    elif args.command == "label-group-create":
        result = client.create_label_group(args.name)
    elif args.command == "label-group-update":
        result = client.update_label_group(args.id, args.name)
    elif args.command == "label-group-delete":
        result = client.delete_label_group(args.id)
    elif args.command == "labels":
        result = client.get_labels()
    elif args.command == "label-create":
        result = client.create_label(args.group, args.name, args.color or None)
    elif args.command == "label-info":
        result = client.get_label_details(args.id)
    elif args.command == "label-update":
        data = {}
        if args.name: data["name"] = args.name
        if args.color: data["color"] = args.color
        result = client.update_label(args.id, data)
    elif args.command == "label-delete":
        result = client.delete_label(args.id)
    elif args.command == "timer-current":
        result = client.get_timer_current()
    elif args.command == "time-create":
        result = client.create_time_log(args.task_id, args.seconds)
    elif args.command == "time-update":
        result = client.update_time_log(args.id, args.seconds)
    elif args.command == "time-delete":
        result = client.delete_time_log(args.id)
    elif args.command == "start":
        result = client.start_timer(args.task_id)
    elif args.command == "stop":
        result = client.stop_timer()
    elif args.command == "task-time":
        result = client.get_task_time_list(args.task_id)
    elif args.command == "time-list":
        result = client.get_time_logs()
    elif args.command == "activity":
        result = client.get_activity_logs(args.project, args.user, args.type)
    elif args.command == "activity-projects":
        result = client.get_activity_projects()
    else:
        parser.print_help()
        sys.exit(0)

    # --- Pretty Output ---
    if console and isinstance(result, list) and len(result) > 0:
        table = Table(title=f"MooTeam: {args.command}")
        
        # Infer columns from the first object
        keys = result[0].keys()
        for key in keys:
            table.add_column(str(key), overflow="fold")
            
        for item in result:
            table.add_row(*[str(item.get(k, "")) for k in keys])
            
        console.print(table)
    elif console and isinstance(result, dict) and "error" in result:
        console.print(Panel(RichJSON(json.dumps(result)), title="Error", border_style="red"))
    elif console:
        console.print(Panel(RichJSON(json.dumps(result)), title=f"Result: {args.command}", border_style="green"))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()