"""
Save Session Summary Script
Automatically generate and save session summaries
"""

import asyncio
import sys
from datetime import datetime
import json


async def save_session_summary(reme, messages, session_info=None):
    """
    Generate and save session summary

    Args:
        reme: ReMeLight instance
        messages: List of conversation messages
        session_info: Dict with session metadata
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"\n💾 Generating session summary...")
    print(f"   Timestamp: {timestamp}")
    print(f"   Messages: {len(messages)}")

    # Extract key events
    key_events = extract_key_events(messages)

    # Generate summary
    summary = generate_summary_text(key_events, session_info, timestamp)

    # Write to memory file
    filename = f"memory/{date_str}.md"

    print(f"\n📝 Writing to {filename}...")
    await reme.summary_memory(messages=messages)

    print("✓ Summary saved")


def extract_key_events(messages):
    """
    Extract key events from messages

    Args:
        messages: List of conversation messages

    Returns:
        dict: Key events categorized by type
    """
    events = {
        "user_requests": [],
        "actions_taken": [],
        "files_generated": [],
        "user_feedback": [],
        "learnings": []
    }

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        if role == "user":
            # Check for requests
            if any(keyword in content for keyword in ["生成", "创建", "写个", "给我"]):
                events["user_requests"].append(content)
            # Check for feedback
            elif any(keyword in content for keyword in ["忘记", "错误", "不对", "记住"]):
                events["user_feedback"].append(content)
        elif role == "assistant":
            # Check for file generation
            if "文件已生成" in content or "Created file" in content:
                events["files_generated"].append(content)
            # Check for actions
            elif any(keyword in content for keyword in ["正在", "已", "✓"]):
                events["actions_taken"].append(content)

    return events


def generate_summary_text(events, session_info, timestamp):
    """
    Generate formatted summary text

    Args:
        events: Key events dict
        session_info: Session metadata
        timestamp: Current timestamp

    Returns:
        str: Formatted summary
    """
    lines = [
        f"# {datetime.now().strftime('%Y-%m-%d')} Session Summary",
        "",
        f"## Session - {timestamp}",
        ""
    ]

    # Add session info if available
    if session_info:
        lines.append("### Session Information")
        for key, value in session_info.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

    # Add user requests
    if events["user_requests"]:
        lines.append("### User Requests")
        for i, req in enumerate(events["user_requests"], 1):
            lines.append(f"{i}. {req}")
        lines.append("")

    # Add actions taken
    if events["actions_taken"]:
        lines.append("### Actions Taken")
        for i, action in enumerate(events["actions_taken"], 1):
            lines.append(f"- {action[:100]}{'...' if len(action) > 100 else ''}")
        lines.append("")

    # Add files generated
    if events["files_generated"]:
        lines.append("### Files Generated")
        for i, file in enumerate(events["files_generated"], 1):
            lines.append(f"{i}. {file}")
        lines.append("")

    # Add user feedback
    if events["user_feedback"]:
        lines.append("### User Feedback")
        for i, feedback in enumerate(events["user_feedback"], 1):
            lines.append(f"- {feedback}")
        lines.append("")

    return "\n".join(lines)


async def save_with_auto_cleanup(reme, messages, retention_days=7):
    """
    Save summary and cleanup old tool results

    Args:
        reme: ReMeLight instance
        messages: List of conversation messages
        retention_days: Days to keep tool results
    """
    import os
    from pathlib import Path

    # Save summary
    await save_session_summary(reme, messages)

    # Cleanup tool results
    tool_result_dir = Path(".reme/tool_result")
    if tool_result_dir.exists():
        print(f"\n🧹 Cleaning up tool results (retention: {retention_days} days)...")

        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 3600)
        cleaned = 0

        for file_path in tool_result_dir.glob("*.txt"):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                cleaned += 1

        print(f"✓ Cleaned {cleaned} old files")


async def main():
    """Main entry point"""
    from reme.reme_light import ReMeLight

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python save_summary.py <messages_file>")
        print("  python save_summary.py --auto <messages_file>")
        print("\nExamples:")
        print("  python save_summary.py session_messages.json")
        print("  python save_summary.py --auto session_messages.json")
        print("\nNote: messages_file should be a JSON array of message objects")
        print("  Each message should have 'role' and 'content' fields")
        return

    # Initialize ReMe
    working_dir = ".reme"
    reme = ReMeLight(working_dir=working_dir)
    await reme.start()

    # Load messages from file
    messages_file = sys.argv[2] if sys.argv[1] == "--auto" else sys.argv[1]

    try:
        with open(messages_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)

        print(f"✓ Loaded {len(messages)} messages from {messages_file}")

        # Save summary
        if sys.argv[1] == "--auto":
            await save_with_auto_cleanup(reme, messages)
        else:
            await save_session_summary(reme, messages)

    except FileNotFoundError:
        print(f"Error: File not found: {messages_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {messages_file}")
    finally:
        # Close
        await reme.close()


if __name__ == "__main__":
    asyncio.run(main())
