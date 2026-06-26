#!/usr/bin/env python3
"""
Nex Voice - Voice Note Transcription & Action Extractor
CLI Entry Point
"""

import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from lib.config import config
from lib.storage import Database
from lib.transcriber import (
    transcribe_audio,
    check_whisper,
    check_ffmpeg,
    validate_audio_format,
)
from lib.action_extractor import extract_actions, generate_summary

FOOTER = "[Nex Voice by Nex AI | nex-ai.be]"

# Get script directory for imports
SCRIPT_DIR = Path(__file__).parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def print_footer():
    """Print footer"""
    print(FOOTER)


def cmd_transcribe(args) -> None:
    """Transcribe audio file"""
    audio_path = Path(args.audio_file)

    if not audio_path.exists():
        print(f"ERROR: Audio file not found: {audio_path}")
        return

    if not validate_audio_format(str(audio_path)):
        print(f"ERROR: Unsupported audio format: {audio_path.suffix}")
        print("Supported formats: ogg, mp3, wav, m4a, opus, webm")
        return

    if not check_whisper():
        print("ERROR: Whisper CLI not found")
        print("Install with: pip install openai-whisper")
        return

    if not check_ffmpeg():
        print("ERROR: FFmpeg not found")
        print("Install from: https://ffmpeg.org")
        return

    try:
        print(f"Transcribing: {audio_path.name}...")

        # Transcribe
        language = args.language or config.get_whisper_language()
        model = config.get_whisper_model()

        result = transcribe_audio(str(audio_path), language=language, model=model)

        # Generate summary
        summary = generate_summary(result["text"])

        # Copy audio to data directory
        from lib.config import AUDIO_DIR
        dest_path = AUDIO_DIR / audio_path.name
        if dest_path != audio_path:
            shutil.copy2(audio_path, dest_path)
        else:
            dest_path = audio_path

        # Save to database
        db = Database()
        recording_id = db.save_recording(
            file_path=str(dest_path),
            original_filename=audio_path.name,
            duration_seconds=result["duration"],
            transcript=result["text"],
            language=result["language"],
            summary=summary,
            source="file",
            speaker=args.speaker,
            tags=args.tags,
        )

        print(f"Recording ID: {recording_id}")
        print(f"Duration: {result['duration']:.1f} seconds")
        print(f"Language: {result['language']}")
        print()
        print("TRANSCRIPT")
        print("---")
        print(result["text"])
        print()
        print("SUMMARY")
        print("---")
        print(summary)
        print()

        # Extract actions if not disabled
        if not args.skip_actions:
            actions = extract_actions(result["text"])
            if actions:
                print("ACTION ITEMS")
                print("---")
                for action in actions:
                    print(f"- [{action['type'].upper()}] {action['description']}")
                    if action.get("assigned_to"):
                        print(f"  Assigned to: {action['assigned_to']}")
                    if action.get("due_date"):
                        print(f"  Due: {action['due_date']}")
                    # Save action to database
                    db.save_action_item(
                        recording_id=recording_id,
                        type=action["type"],
                        description=action["description"],
                        assigned_to=action.get("assigned_to"),
                        due_date=action.get("due_date"),
                        priority=action.get("priority", "medium"),
                    )
                print()

        print_footer()

    except Exception as e:
        print(f"ERROR: {e}")
        print_footer()


def cmd_actions(args) -> None:
    """Extract actions from a recording"""
    db = Database()

    if args.last:
        recordings = db.list_recordings()
        if not recordings:
            print("ERROR: No recordings found")
            print_footer()
            return
        recording_id = recordings[0].id
    else:
        recording_id = args.recording_id

    recording = db.get_recording(recording_id)
    if not recording:
        print(f"ERROR: Recording {recording_id} not found")
        print_footer()
        return

    print(f"Recording: {recording.original_filename}")
    print(f"Date: {recording.created_at}")
    print()

    # Extract or list actions
    use_llm = args.use_llm and config.is_llm_configured()

    if use_llm:
        actions = extract_actions(
            recording.transcript,
            use_llm=True,
            api_key=config.get_api_key(),
            api_base=config.get_api_base(),
            model=config.get_api_model(),
        )
    else:
        actions = extract_actions(recording.transcript)

    if actions:
        print("ACTION ITEMS")
        print("---")
        for i, action in enumerate(actions, 1):
            print(f"{i}. [{action['type'].upper()}] {action['description']}")
            if action.get("assigned_to"):
                print(f"   Assigned to: {action['assigned_to']}")
            if action.get("due_date"):
                print(f"   Due: {action['due_date']}")
            if action.get("priority"):
                print(f"   Priority: {action['priority']}")
            print()
    else:
        print("No action items found in transcript")
        print()

    print_footer()


def cmd_list(args) -> None:
    """List recordings"""
    db = Database()

    recordings = db.list_recordings(
        since=args.since,
        speaker=args.speaker,
        tag=args.tag,
    )

    if not recordings:
        print("No recordings found")
        print_footer()
        return

    print("RECORDINGS")
    print("---")
    for rec in recordings:
        print(f"[{rec.id}] {rec.original_filename} ({rec.duration_seconds:.0f}s)")
        print(f"    Date: {rec.created_at}")
        if rec.speaker:
            print(f"    Speaker: {rec.speaker}")
        if rec.tags:
            print(f"    Tags: {rec.tags}")
        print()

    print_footer()


def cmd_show(args) -> None:
    """Show recording details"""
    db = Database()

    recording = db.get_recording(args.recording_id)
    if not recording:
        print(f"ERROR: Recording {args.recording_id} not found")
        print_footer()
        return

    print(f"Recording: {recording.original_filename}")
    print(f"ID: {recording.id}")
    print(f"Date: {recording.created_at}")
    print(f"Duration: {recording.duration_seconds:.1f} seconds")
    print(f"Language: {recording.language}")
    if recording.speaker:
        print(f"Speaker: {recording.speaker}")
    if recording.tags:
        print(f"Tags: {recording.tags}")
    print()

    print("TRANSCRIPT")
    print("---")
    print(recording.transcript)
    print()

    if recording.summary:
        print("SUMMARY")
        print("---")
        print(recording.summary)
        print()

    # Show actions
    actions = db.list_action_items(recording_id=args.recording_id)
    if actions:
        print("ACTION ITEMS")
        print("---")
        for action in actions:
            status = "✓" if action.completed else "○"
            print(f"[{status}] {action.type.upper()}: {action.description}")
            if action.assigned_to:
                print(f"    Assigned to: {action.assigned_to}")
            if action.due_date:
                print(f"    Due: {action.due_date}")
            print()

    print_footer()


def cmd_search(args) -> None:
    """Search transcripts"""
    db = Database()

    results = db.search_recordings(args.query)

    if not results:
        print(f"No results found for: {args.query}")
        print_footer()
        return

    print(f"Search results for: {args.query}")
    print("---")
    for result in results:
        print(f"[{result['id']}] {result['filename']} ({result['created_at']})")
        print(f"    {result['transcript'][:100]}...")
        print()

    print_footer()


def cmd_pending(args) -> None:
    """List pending action items"""
    db = Database()

    actions = db.list_action_items(type=args.type, completed=False)

    if not actions:
        print("No pending action items")
        print_footer()
        return

    print("PENDING ACTION ITEMS")
    print("---")
    for action in actions:
        print(f"[{action.id}] [{action.type.upper()}] {action.description}")
        if action.assigned_to:
            print(f"    Assigned to: {action.assigned_to}")
        if action.due_date:
            print(f"    Due: {action.due_date}")
        print(f"    Priority: {action.priority}")
        print()

    print_footer()


def cmd_complete(args) -> None:
    """Mark action as complete"""
    db = Database()

    action = None
    for a in db.list_action_items(completed=False):
        if a.id == args.action_id:
            action = a
            break

    if not action:
        print(f"ERROR: Action {args.action_id} not found or already completed")
        print_footer()
        return

    db.complete_action_item(args.action_id)

    print(f"Marked action {args.action_id} as complete")
    print(f"Description: {action.description}")
    print()
    print_footer()


def cmd_overdue(args) -> None:
    """List overdue actions"""
    db = Database()

    actions = db.list_action_items(overdue=True)

    if not actions:
        print("No overdue action items")
        print_footer()
        return

    print("OVERDUE ACTION ITEMS")
    print("---")
    for action in actions:
        print(f"[{action.id}] [{action.type.upper()}] {action.description}")
        if action.assigned_to:
            print(f"    Assigned to: {action.assigned_to}")
        print(f"    Due: {action.due_date}")
        print(f"    Priority: {action.priority}")
        print()

    print_footer()


def cmd_export(args) -> None:
    """Export transcript"""
    db = Database()

    try:
        export = db.export_transcript(args.recording_id, format=args.format)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(export)
            print(f"Exported to: {output_path}")
        else:
            print(export)

        print()
        print_footer()

    except Exception as e:
        print(f"ERROR: {e}")
        print_footer()


def cmd_stats(args) -> None:
    """Show statistics"""
    db = Database()

    stats = db.get_recording_stats()

    print("STATISTICS")
    print("---")
    print(f"Total recordings: {stats['total_recordings']}")
    print(f"Total duration: {stats['total_duration_hours']} hours")
    print()

    if stats['languages']:
        print("Languages:")
        for lang, count in stats['languages'].items():
            print(f"  {lang}: {count}")
        print()

    print("Action Items:")
    print(f"  Pending: {stats['pending_actions']}")
    print(f"  Completed: {stats['completed_actions']}")
    print(f"  Overdue: {stats['overdue_actions']}")
    print()

    print_footer()


def cmd_config(args) -> None:
    """Configuration management"""
    if args.action == "show":
        print("CONFIGURATION")
        print("---")
        print(f"Whisper model: {config.get_whisper_model()}")
        print(f"Whisper language: {config.get_whisper_language()}")
        if config.is_llm_configured():
            print(f"LLM configured: Yes")
            print(f"LLM API base: {config.get_api_base()}")
            print(f"LLM model: {config.get_api_model()}")
        else:
            print("LLM configured: No")
        print()

    elif args.action == "set-whisper-model":
        config.set_whisper_model(args.value)
        print(f"Whisper model set to: {args.value}")
        print()

    elif args.action == "set-whisper-language":
        config.set_whisper_language(args.value)
        print(f"Whisper language set to: {args.value}")
        print()

    elif args.action == "set-api-key":
        api_key = input("Enter API key: ")
        if api_key:
            config.set_api_key(api_key)
            print("API key saved")
        print()

    elif args.action == "set-api-base":
        config.set_api_base(args.value)
        print(f"API base set to: {args.value}")
        print()

    elif args.action == "set-api-model":
        config.set_api_model(args.value)
        print(f"API model set to: {args.value}")
        print()

    print_footer()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="nex-voice",
        description="Voice Note Transcription & Action Extractor",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe audio file")
    transcribe_parser.add_argument("audio_file", help="Path to audio file")
    transcribe_parser.add_argument("--language", help="Language (nl, en)")
    transcribe_parser.add_argument("--speaker", help="Speaker name")
    transcribe_parser.add_argument("--tags", help="Tags (comma-separated)")
    transcribe_parser.add_argument("--skip-actions", action="store_true", help="Don't extract actions")
    transcribe_parser.set_defaults(func=cmd_transcribe)

    # Actions command
    actions_parser = subparsers.add_parser("actions", help="Extract actions from recording")
    actions_parser.add_argument("recording_id", nargs="?", type=int, help="Recording ID")
    actions_parser.add_argument("--last", action="store_true", help="Use last recording")
    actions_parser.add_argument("--use-llm", action="store_true", help="Use LLM extraction")
    actions_parser.set_defaults(func=cmd_actions)

    # List command
    list_parser = subparsers.add_parser("list", help="List recordings")
    list_parser.add_argument("--since", help="Since date (ISO format)")
    list_parser.add_argument("--speaker", help="Filter by speaker")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.set_defaults(func=cmd_list)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show recording details")
    show_parser.add_argument("recording_id", type=int, help="Recording ID")
    show_parser.set_defaults(func=cmd_show)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search transcripts")
    search_parser.add_argument("query", help="Search query")
    search_parser.set_defaults(func=cmd_search)

    # Pending command
    pending_parser = subparsers.add_parser("pending", help="List pending actions")
    pending_parser.add_argument("--type", help="Filter by type")
    pending_parser.set_defaults(func=cmd_pending)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark action as complete")
    complete_parser.add_argument("action_id", type=int, help="Action ID")
    complete_parser.set_defaults(func=cmd_complete)

    # Overdue command
    overdue_parser = subparsers.add_parser("overdue", help="List overdue actions")
    overdue_parser.set_defaults(func=cmd_overdue)

    # Export command
    export_parser = subparsers.add_parser("export", help="Export transcript")
    export_parser.add_argument("recording_id", type=int, help="Recording ID")
    export_parser.add_argument("--format", choices=["txt", "json"], default="txt", help="Export format")
    export_parser.add_argument("--output", help="Output file path")
    export_parser.set_defaults(func=cmd_export)

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.set_defaults(func=cmd_stats)

    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="action", help="Config actions")

    config_subparsers.add_parser("show", help="Show configuration")
    config_subparsers.add_parser("set-api-key", help="Set API key")

    set_model_parser = config_subparsers.add_parser("set-whisper-model", help="Set Whisper model")
    set_model_parser.add_argument("value", help="Model (tiny, base, small, medium, large)")

    set_lang_parser = config_subparsers.add_parser("set-whisper-language", help="Set Whisper language")
    set_lang_parser.add_argument("value", help="Language (nl, en)")

    set_base_parser = config_subparsers.add_parser("set-api-base", help="Set API base URL")
    set_base_parser.add_argument("value", help="API base URL")

    set_api_model_parser = config_subparsers.add_parser("set-api-model", help="Set API model")
    set_api_model_parser.add_argument("value", help="Model name")

    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
