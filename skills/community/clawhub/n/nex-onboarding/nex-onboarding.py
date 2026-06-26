#!/usr/bin/env python3
"""
Nex Onboarding - Client Onboarding Checklist Runner
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

A tool for agency operators to manage client onboarding checklists,
track progress, and ensure nothing falls through the cracks.
"""

import sys
import argparse
from lib.storage import (
    init_db,
    start_onboarding,
    get_onboarding,
    list_onboardings,
    get_onboarding_progress,
    get_next_step,
    complete_step,
    skip_step,
    block_step,
    complete_onboarding,
    pause_onboarding,
    get_onboarding_stats,
    export_onboarding,
    save_template,
    get_template,
    list_templates,
)
from lib.formatter import (
    format_progress,
    format_onboarding_list,
    format_step_detail,
    format_stats,
    format_template_detail,
    format_error,
    format_success,
)

FOOTER = "[Nex Onboarding by Nex AI | nex-ai.be]"


def cmd_start(args):
    """Start a new onboarding."""
    try:
        onboarding_id = start_onboarding(
            client_name=args.client,
            client_email=args.email,
            client_phone=args.phone,
            template_name=args.template or "default",
            retainer_tier=args.tier,
            assigned_to=args.assigned_to,
        )

        onboarding = get_onboarding(onboarding_id)
        progress = get_onboarding_progress(onboarding_id)

        print(format_success(f"Onboarding started for {args.client}"))
        print("")
        print(format_progress(onboarding, progress))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_next(args):
    """Show or complete next step."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        next_step = get_next_step(args.onboarding_id)

        if not next_step:
            print("All steps are completed!")
            sys.exit(0)

        if args.done:
            # Mark as complete
            complete_step(
                args.onboarding_id,
                next_step["step_number"],
                notes=args.notes,
                completed_by=args.completed_by,
            )
            print(format_success(f"Step {next_step['step_number']} marked as completed"))

            # Show new next step
            next_step = get_next_step(args.onboarding_id)
            if next_step:
                print("")
                print(format_step_detail(next_step))
        else:
            # Just show it
            print(format_step_detail(next_step))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_complete(args):
    """Complete a specific step."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        success = complete_step(
            args.onboarding_id,
            args.step,
            notes=args.notes,
            completed_by=args.completed_by,
        )

        if success:
            print(format_success(f"Step {args.step} marked as completed"))
            progress = get_onboarding_progress(args.onboarding_id)
            print(f"Progress: {progress['percentage']}% ({progress['completed']}/{progress['total']})")
        else:
            print(format_error(f"Step {args.step} not found"))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_skip(args):
    """Skip a step."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        success = skip_step(args.onboarding_id, args.step, reason=args.reason)

        if success:
            print(format_success(f"Step {args.step} skipped"))
            if args.reason:
                print(f"Reason: {args.reason}")
        else:
            print(format_error(f"Step {args.step} not found"))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_block(args):
    """Block a step."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        success = block_step(args.onboarding_id, args.step, reason=args.reason)

        if success:
            print(format_success(f"Step {args.step} blocked"))
            if args.reason:
                print(f"Reason: {args.reason}")
        else:
            print(format_error(f"Step {args.step} not found"))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_progress(args):
    """Show onboarding progress."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        progress = get_onboarding_progress(args.onboarding_id)

        print(format_progress(onboarding, progress))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_list(args):
    """List onboardings."""
    try:
        onboardings = list_onboardings(status=args.status, retainer_tier=args.tier)

        if args.status:
            print(f"Onboardings ({args.status}):")
        elif args.tier:
            print(f"Onboardings ({args.tier} tier):")
        else:
            print("All Onboardings:")

        print("")
        print(format_onboarding_list(onboardings))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_show(args):
    """Show full onboarding details."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        progress = get_onboarding_progress(args.onboarding_id)

        print(format_progress(onboarding, progress))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_finish(args):
    """Complete an onboarding."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        success = complete_onboarding(args.onboarding_id)

        if success:
            print(format_success(f"Onboarding completed for {onboarding['client_name']}"))
        else:
            print(format_error("Failed to complete onboarding"))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_pause(args):
    """Pause an onboarding."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        success = pause_onboarding(args.onboarding_id)

        if success:
            print(format_success(f"Onboarding paused for {onboarding['client_name']}"))
        else:
            print(format_error("Failed to pause onboarding"))

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_stats(args):
    """Show statistics."""
    try:
        stats = get_onboarding_stats()

        print(format_stats(stats))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_export(args):
    """Export onboarding."""
    try:
        onboarding = get_onboarding(args.onboarding_id)
        if not onboarding:
            print(format_error(f"Onboarding '{args.onboarding_id}' not found"))
            sys.exit(1)

        export_format = args.format or "json"
        content = export_onboarding(args.onboarding_id, format=export_format)

        if args.output:
            with open(args.output, "w") as f:
                f.write(content)
            print(format_success(f"Exported to {args.output}"))
        else:
            print(content)

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_template_list(args):
    """List templates."""
    try:
        templates = list_templates()

        print("Available Templates:")
        print("")

        for t in templates:
            print(f"- {t['name']}: {t['description']}")

        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def cmd_template_show(args):
    """Show template details."""
    try:
        template = get_template(args.name)
        if not template:
            print(format_error(f"Template '{args.name}' not found"))
            sys.exit(1)

        print(format_template_detail(template, template["steps"]))
        print("")
        print(FOOTER)

    except Exception as e:
        print(format_error(str(e)))
        sys.exit(1)


def main():
    """Main CLI entry point."""
    init_db()

    parser = argparse.ArgumentParser(
        description="Nex Onboarding - Client Checklist Runner for Agencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Start
    start_parser = subparsers.add_parser("start", help="Start onboarding for a client")
    start_parser.add_argument("client", help="Client name")
    start_parser.add_argument("--email", help="Client email")
    start_parser.add_argument("--phone", help="Client phone")
    start_parser.add_argument("--template", default="default", help="Template name (default: default)")
    start_parser.add_argument("--tier", help="Retainer tier (starter, standard, premium, enterprise)")
    start_parser.add_argument("--assigned-to", help="Assign to team member")
    start_parser.set_defaults(func=cmd_start)

    # Next
    next_parser = subparsers.add_parser("next", help="Show or complete next step")
    next_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    next_parser.add_argument("--done", action="store_true", help="Mark as complete")
    next_parser.add_argument("--notes", help="Notes for completion")
    next_parser.add_argument("--completed-by", help="Who completed it")
    next_parser.set_defaults(func=cmd_next)

    # Complete
    complete_parser = subparsers.add_parser("complete", help="Complete specific step")
    complete_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    complete_parser.add_argument("step", type=int, help="Step number")
    complete_parser.add_argument("--notes", help="Notes for completion")
    complete_parser.add_argument("--completed-by", help="Who completed it")
    complete_parser.set_defaults(func=cmd_complete)

    # Skip
    skip_parser = subparsers.add_parser("skip", help="Skip a step")
    skip_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    skip_parser.add_argument("step", type=int, help="Step number")
    skip_parser.add_argument("--reason", help="Reason for skipping")
    skip_parser.set_defaults(func=cmd_skip)

    # Block
    block_parser = subparsers.add_parser("block", help="Block a step")
    block_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    block_parser.add_argument("step", type=int, help="Step number")
    block_parser.add_argument("--reason", help="Reason for blocking")
    block_parser.set_defaults(func=cmd_block)

    # Progress
    progress_parser = subparsers.add_parser("progress", help="Show progress")
    progress_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    progress_parser.set_defaults(func=cmd_progress)

    # List
    list_parser = subparsers.add_parser("list", help="List onboardings")
    list_parser.add_argument("--status", help="Filter by status (active, completed, paused, cancelled)")
    list_parser.add_argument("--tier", help="Filter by retainer tier")
    list_parser.set_defaults(func=cmd_list)

    # Show
    show_parser = subparsers.add_parser("show", help="Show full details")
    show_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    show_parser.set_defaults(func=cmd_show)

    # Finish
    finish_parser = subparsers.add_parser("finish", help="Complete onboarding")
    finish_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    finish_parser.set_defaults(func=cmd_finish)

    # Pause
    pause_parser = subparsers.add_parser("pause", help="Pause onboarding")
    pause_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    pause_parser.set_defaults(func=cmd_pause)

    # Stats
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.set_defaults(func=cmd_stats)

    # Export
    export_parser = subparsers.add_parser("export", help="Export onboarding")
    export_parser.add_argument("onboarding_id", help="Onboarding ID or client name")
    export_parser.add_argument("--format", choices=["json", "csv"], help="Export format (json or csv)")
    export_parser.add_argument("--output", help="Output file")
    export_parser.set_defaults(func=cmd_export)

    # Template subcommands
    template_parser = subparsers.add_parser("template", help="Manage templates")
    template_subs = template_parser.add_subparsers(dest="template_command")

    template_list = template_subs.add_parser("list", help="List templates")
    template_list.set_defaults(func=cmd_template_list)

    template_show = template_subs.add_parser("show", help="Show template")
    template_show.add_argument("name", help="Template name")
    template_show.set_defaults(func=cmd_template_show)

    # Parse and execute
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
