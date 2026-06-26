#!/usr/bin/env python3
"""
NextLink - Unified CLI for Email, Calendar, Tasks, Files, and Contacts.

Orchestrates Exchange (mail, calendar, tasks) and Nextcloud (files) operations,
plus Contacts from both sources.
"""

import sys
import os

# Add skill root to path so 'modules' package is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, SKILL_ROOT)


def main():
    """Main entry point for NextLink CLI."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Parse global flags before routing to modules.
    # --no-memory: disable LCM persistent memory for this session.
    global_flags = {"--no-memory"}
    module_args = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--no-memory":
            os.environ["NEXLINK_NO_MEMORY"] = "1"
        else:
            module_args.append(arg)
        i += 1

    module = module_args[0] if module_args else "help"
    args = module_args[1:]

    # Reconstruct sys.argv for sub-modules (pass through remaining flags)
    sys.argv = [sys.argv[0], module] + args

    if module in ('mail', 'cal', 'calendar', 'tasks', 'analytics', 'sync'):
        # Route to Exchange module
        from modules.exchange.cli import main as exchange_main
        # Normalize 'cal' to 'calendar'
        normalized_module = 'calendar' if module == 'cal' else module
        # Set sys.argv for exchange module and call main()
        sys.argv = [sys.argv[0], normalized_module] + args
        exchange_main()

    elif module == 'youtube':
        from modules.youtube.youtube import run_cli as youtube_run_cli
        sys.exit(youtube_run_cli(args))

    elif module in ('files', 'nextcloud', 'nc'):
        from modules.nextcloud.nextcloud import run_cli as nextcloud_run_cli

        if len(args) < 1:
            print("Error: No command specified for files.")
            print(
                "Available commands: list, search, upload, download, mkdir, "
                "delete, move, copy, info, shared, share-create, share-list, share-revoke"
            )
            sys.exit(1)

        sys.exit(nextcloud_run_cli(args))

    elif module == 'contacts':
        _run_contacts(args)

    elif module in ('help', '-h', '--help'):
        print_usage()

    else:
        print(f"Error: Unknown module: {module}")
        print_usage()
        sys.exit(1)


def _run_contacts(args):
    """Handle 'nexlink contacts <command> [--source exchange|nextcloud] ...'."""
    if len(args) < 1:
        print("Error: No command specified for contacts.")
        print(
            "Available commands: list, get, create, update, delete, search, "
            "addressbooks, addressbook-list"
        )
        print("\nUse --source exchange|nextcloud to choose provider (default: exchange)")
        sys.exit(1)

    command = args[0]
    source = 'exchange'
    remaining = []

    # Parse --source from args
    i = 1
    while i < len(args):
        arg = args[i]
        if arg == '--source':
            i += 1
            if i < len(args):
                source = args[i]
            else:
                print("Error: --source requires a value (exchange|nextcloud)")
                sys.exit(1)
        elif arg.startswith('--source='):
            source = arg.split('=', 1)[1]
        else:
            remaining.append(arg)
        i += 1

    if source == 'exchange':
        import argparse
        from modules.exchange.contacts import add_parser as ex_add_parser
        parser = argparse.ArgumentParser(prog='nexlink contacts', add_help=False)
        sub = parser.add_subparsers(dest='contact_cmd')
        ex_add_parser(sub)
        ex_args = parser.parse_args([command] + remaining)
        if hasattr(ex_args, 'func'):
            ex_args.func(ex_args)
        else:
            parser.print_help()
            sys.exit(1)

    elif source == 'nextcloud':
        _run_nc_contacts(command, remaining)

    else:
        print(f"Error: Unknown source '{source}'. Use --source exchange|nextcloud")
        sys.exit(1)


def _run_nc_contacts(command, remaining):
    """Route a contacts command to the Nextcloud CardDAV handler."""
    from modules.nextcloud.contacts import add_parser as nc_add_parser
    from modules.nextcloud.contacts import out as nc_out
    from modules.nextcloud.contacts import list_addressbooks as nc_list_addressbooks

    # Special subcommand for listing addressbooks
    if command in ('addressbooks', 'addressbook-list'):
        books = nc_list_addressbooks()
        nc_out({"ok": True, "count": len(books), "addressbooks": books})
        sys.exit(0)

    import argparse
    parser = argparse.ArgumentParser(prog='nexlink contacts', add_help=False)
    sub = parser.add_subparsers(dest='contact_cmd')
    nc_add_parser(sub)

    nc_args = parser.parse_args([command] + remaining)
    if hasattr(nc_args, 'func'):
        nc_args.func(nc_args)
    else:
        parser.print_help()
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""
NextLink - Unified CLI for Email, Calendar, Tasks, Files, and Contacts

Usage:
    nexlink <module> <command> [options]

Global Options:
    --json          Output results in JSON format
    --no-memory     Disable LCM persistent memory for this session

Modules:
    mail        Email operations (Exchange)
    cal         Calendar operations (Exchange)
    tasks       Task management (Exchange)
    analytics   Email analytics and statistics (Exchange)
    sync        Task sync and reminders (Exchange)
    files       File operations (Nextcloud)
    contacts    Contact operations (Exchange + Nextcloud)
    youtube     YouTube transcript extraction

Email Commands:
    nexlink mail connect              Test Exchange connection
    nexlink mail read [--folder FOLDER] [--limit N] [--unread]
    nexlink mail send --to EMAIL --subject SUBJECT --body BODY
    nexlink mail reply --id EMAIL_ID --body BODY
    nexlink mail forward --id EMAIL_ID --to EMAIL

Calendar Commands:
    nexlink cal today                 Show today's events
    nexlink cal week                  Show this week's events
    nexlink cal list [--days N]
    nexlink cal create --subject SUBJECT --start DATETIME [--duration MIN]

Task Commands:
    nexlink tasks list [--overdue] [--status STATUS]
    nexlink tasks create --subject SUBJECT [--due DATE] [--priority LEVEL]
    nexlink tasks complete --id TASK_ID
    nexlink tasks trash --id TASK_ID

Sync Commands:
    nexlink sync sync                 Sync tasks with Exchange
    nexlink sync status               Show sync status
    nexlink sync reminders [--hours N] [--dry-run]

Analytics Commands:
    nexlink analytics stats --days N     Email statistics
    nexlink analytics response-time      Response time analysis
    nexlink analytics top-senders        Top senders by count
    nexlink analytics heatmap            Activity heatmap
    nexlink analytics folders            Folder statistics
    nexlink analytics report             Full analytics report

File Commands:
    nexlink files list [PATH] [--recursive] List files in directory
    nexlink files search QUERY [PATH]       Search files/folders by name
    nexlink files extract-text PATH         Extract readable text from one file
    nexlink files summarize PATH            Summarize one file
    nexlink files ask-file PATH QUESTION    Answer a question from one file
    nexlink files extract-actions PATH      Extract workflow actions from one file
    nexlink files create-tasks-from-file PATH [--mailbox EMAIL] [--priority LEVEL] [--select 1,2] [--execute]
    nexlink files upload LOCAL REMOTE       Upload file to Nextcloud
    nexlink files download REMOTE LOCAL     Download file from Nextcloud
    nexlink files mkdir PATH                Create directory
    nexlink files delete PATH               Delete file or directory
    nexlink files move OLD NEW              Move/rename file
    nexlink files copy SRC DEST             Copy file
    nexlink files info PATH                 Get file info
    nexlink files shared                    List items shared with current user
    nexlink files share-create PATH [--password VALUE] [--expire-date YYYY-MM-DD] [--public-upload]
    nexlink files share-list [PATH]         List public share links
    nexlink files share-revoke SHARE_ID     Revoke public share link

Contact Commands:
    nexlink contacts list [--limit N]                                  List Exchange contacts (default)
    nexlink contacts list --source nextcloud [--addressbook HREF]        List Nextcloud contacts
    nexlink contacts get --id CONTACT_ID                                Get Exchange contact by ID
    nexlink contacts get --uid UID --source nextcloud                   Get Nextcloud contact by UID
    nexlink contacts create --name NAME [--email EMAIL] [--phone PHONE]
    nexlink contacts update --id CONTACT_ID [--name NAME] [--email EMAIL]
    nexlink contacts delete --id CONTACT_ID
    nexlink contacts search --query QUERY                                Search contacts
    nexlink contacts addressbooks --source nextcloud                     List CardDAV addressbooks

Configuration:
    Set environment variables:
        EXCHANGE_SERVER    - Exchange EWS URL
        EXCHANGE_USERNAME  - Exchange username
        EXCHANGE_PASSWORD  - Exchange password
        EXCHANGE_EMAIL     - Exchange email address
        NEXTCLOUD_URL      - Nextcloud base URL
        NEXTCLOUD_USERNAME - Nextcloud username
        NEXTCLOUD_APP_PASSWORD - Nextcloud app password

    Or use config.yaml in skill directory.

Examples:
    # Send email
    nexlink mail send --to client@example.com --subject "Offer" --body "Please find attached..."

    # Create calendar event
    nexlink cal create --subject "Meeting" --start "2024-01-15 14:00" --duration 60

    # Create task
    nexlink tasks create --subject "Follow-up" --due "+7d" --priority high

    # Contacts (Exchange — default)
    nexlink contacts list
    nexlink contacts create --name "John Doe" --email john@example.com --phone "+40-700-000-000"

    # Contacts (Nextcloud)
    nexlink contacts addressbooks --source nextcloud
    nexlink contacts list --source nextcloud
    nexlink contacts create --source nextcloud --name "Jane Doe" --email jane@example.com

    # Search contacts
    nexlink contacts search --query "Acme"

    # Upload file to Nextcloud
    nexlink files upload /local/report.pdf /Documents/

    # Search files in Nextcloud
    nexlink files search contract /Clients/

    # Extract / summarize / ask a file
    nexlink files extract-text /Clients/contract.docx
    nexlink files summarize /Clients/contract.docx
    nexlink files ask-file /Clients/contract.docx When is the renewal due?

    # Extract workflow actions and preview/create tasks
    nexlink files extract-actions /Clients/contract.txt
    nexlink files create-tasks-from-file /Clients/contract.txt
    nexlink files create-tasks-from-file /Clients/contract.txt --select 1,2 --execute

    # Create a share link
    nexlink files share-create /Contracts/offer.pdf --expire-date 2026-04-30

    # YouTube transcript extraction
    nexlink youtube transcript <url>              # Get plain text transcript (English)
    nexlink youtube transcript <url> --lang ro    # Romanian transcript
    nexlink youtube transcript <url> --format json  # JSON with timestamps
    nexlink youtube transcript <url> --save       # Also save to Nextcloud
    nexlink youtube languages <url>               # List available caption languages

For more information, see references/setup.md
""")


if __name__ == '__main__':
    main()
