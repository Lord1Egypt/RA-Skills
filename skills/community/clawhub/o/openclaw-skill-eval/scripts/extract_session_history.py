#!/usr/bin/env python3
"""
Extract conversation history from a completed session.

Phase 3.3 tool: extract conversation history from a real session for context testing.

Usage:
    python extract_session_history.py \
        --session-key "agent:...:subagent:uuid" \
        --eval-id 1 \
        --output-file evals/history-eval-1.json
"""

import argparse
import json
from pathlib import Path
from oc_tools import invoke


def extract_history_from_session(session_key: str) -> list:
    """
    Extract conversation history from a session.
    
    Returns list of {"role": "user"|"assistant", "content": "..."}
    """
    
    history_data = invoke("sessions_history", {
        "sessionKey": session_key,
        "includeTools": False  # text conversation only, skip tool calls
    })
    
    messages = history_data.get("messages", [])
    conversation = []
    
    for msg in messages:
        role = msg.get("role")
        
        # Keep only user/assistant messages
        if role not in ("user", "assistant"):
            continue
        
        # Handle content (may be string or list)
        content = msg.get("content", "")
        
        if isinstance(content, str):
            # Direct string content
            if content.strip():
                conversation.append({
                    "role": role,
                    "content": content
                })
        elif isinstance(content, list):
            # Content is array, extract all text blocks
            text_parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text = block.get("text", "")
                        if text.strip():
                            text_parts.append(text)
            
            if text_parts:
                conversation.append({
                    "role": role,
                    "content": "\n".join(text_parts)
                })
    
    return conversation


def save_history_to_eval_format(
    history: list,
    eval_id: int,
    eval_name: str,
    session_key: str
) -> dict:
    """
    Format extracted history as eval metadata.
    """
    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "source_session_key": session_key,
        "conversation_history": history,
        "metadata": {
            "num_turns": len(history),
            "user_turns": sum(1 for m in history if m["role"] == "user"),
            "assistant_turns": sum(1 for m in history if m["role"] == "assistant")
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract conversation history from OpenClaw session"
    )
    parser.add_argument(
        "--session-key",
        required=True,
        help="Session key (e.g., 'agent:...:subagent:uuid')"
    )
    parser.add_argument(
        "--eval-id",
        type=int,
        default=1,
        help="Eval ID for metadata"
    )
    parser.add_argument(
        "--eval-name",
        default="extracted",
        help="Eval name for reference"
    )
    parser.add_argument(
        "--output-file",
        default="evals/extracted-history.json",
        help="Output file (JSON format)"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print extracted history to stdout"
    )
    
    args = parser.parse_args()
    
    print(f"Extracting history from session: {args.session_key[:40]}...")
    
    try:
        history = extract_history_from_session(args.session_key)
    except Exception as e:
        print(f"❌ Error fetching session history: {e}")
        return 1
    
    if not history:
        print("⚠️  No conversation found in session")
        return 1
    
    print(f"✅ Extracted {len(history)} messages")
    print(f"   User turns: {sum(1 for m in history if m['role'] == 'user')}")
    print(f"   Assistant turns: {sum(1 for m in history if m['role'] == 'assistant')}")
    
    # Format as eval metadata
    result = save_history_to_eval_format(
        history=history,
        eval_id=args.eval_id,
        eval_name=args.eval_name,
        session_key=args.session_key
    )
    
    # Save to file
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved to {output_path}")
    
    # Print if requested
    if args.print:
        print("\n=== Extracted Conversation ===")
        for msg in history:
            role = msg["role"].upper()
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"\n[{role}]")
            print(f"  {content}")
    
    return 0


if __name__ == "__main__":
    exit(main())
