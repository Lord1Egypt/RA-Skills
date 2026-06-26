"""
Add Memory Script
Add new entries to ReMe memory
"""

import asyncio
import sys
from datetime import datetime


async def add_preference(reme, content, user_name="default", priority="normal"):
    """
    Add a user preference to memory

    Args:
        reme: ReMeLight instance
        content: Preference content
        user_name: User identifier
        priority: Priority level (low/normal/high)
    """
    # Format the memory entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
## User Preference ({timestamp})
- **User**: {user_name}
- **Priority**: {priority}
- **Content**: {content}

"""

    # Add to MEMORY.md
    print(f"📝 Adding preference to MEMORY.md...")
    print(f"   User: {user_name}")
    print(f"   Priority: {priority}")
    print(f"   Content: {content[:80]}...")

    # Use summary_memory to write to file
    messages = [
        {"role": "user", "content": content},
        {"role": "assistant", "content": f"已记住：{content}"}
    ]

    await reme.summary_memory(messages=messages)
    print("✓ Preference saved")


async def add_learning(reme, lesson, context=""):
    """
    Add a learning point to memory

    Args:
        reme: ReMeLight instance
        lesson: What was learned
        context: Context around the learning
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""
## Learning Point ({timestamp})
- **Lesson**: {lesson}
- **Context**: {context}

"""

    print(f"🧠 Adding learning point...")
    print(f"   Lesson: {lesson[:80]}...")

    messages = [
        {"role": "user", "content": f"记住这个教训：{lesson}"},
        {"role": "assistant", "content": f"已记录：{lesson}"}
    ]

    if context:
        messages.append({"role": "user", "content": f"上下文：{context}"})

    await reme.summary_memory(messages=messages)
    print("✓ Learning saved")


async def add_error_pattern(reme, error_pattern, solution=""):
    """
    Add an error pattern to avoid

    Args:
        reme: ReMeLight instance
        error_pattern: Description of the error
        solution: How to avoid it
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""
## Error Pattern to Avoid ({timestamp})
- **Pattern**: {error_pattern}
- **Solution**: {solution}

"""

    print(f"⚠️  Adding error pattern...")
    print(f"   Pattern: {error_pattern[:80]}...")

    messages = [
        {"role": "user", "content": f"避免这个错误：{error_pattern}"},
        {"role": "assistant", "content": f"已记录错误模式：{error_pattern}"}
    ]

    if solution:
        messages.append({"role": "assistant", "content": f"解决方案：{solution}"})

    await reme.summary_memory(messages=messages)
    print("✓ Error pattern saved")


async def main():
    """Main entry point"""
    from reme.reme_light import ReMeLight

    if len(sys.argv) < 3:
        print("Usage:")
        print("  python add_memory.py <type> <content> [options]")
        print("\nTypes:")
        print("  preference - User preference")
        print("  learning    - Learning point")
        print("  error       - Error pattern to avoid")
        print("\nOptions:")
        print("  --user <name>     - User name")
        print("  --priority <level> - Priority (low/normal/high)")
        print("  --context <text>   - Additional context")
        print("\nExamples:")
        print("  python add_memory.py preference \"生成文件后必须直接发送\"")
        print("  python add_memory.py preference \"生成文件后必须直接发送\" --user 阿伟 --priority high")
        print("  python add_memory.py learning \"web_fetch需要设置30秒超时\"")
        print("  python add_memory.py error \"忘记发送文件\" --solution \"每次生成文件后立即检查并发送\"")
        return

    # Parse args
    mem_type = sys.argv[1]
    content = sys.argv[2]

    # Initialize ReMe
    working_dir = ".reme"
    reme = ReMeLight(working_dir=working_dir)
    await reme.start()

    # Parse options
    user_name = "default"
    priority = "normal"
    context = ""
    solution = ""

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--user" and i + 1 < len(sys.argv):
            user_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
            priority = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--context" and i + 1 < len(sys.argv):
            context = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--solution" and i + 1 < len(sys.argv):
            solution = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Add memory based on type
    if mem_type == "preference":
        await add_preference(reme, content, user_name, priority)
    elif mem_type == "learning":
        await add_learning(reme, content, context)
    elif mem_type == "error":
        await add_error_pattern(reme, content, solution)
    else:
        print(f"Error: Unknown type '{mem_type}'")
        print("Valid types: preference, learning, error")

    # Close
    await reme.close()


if __name__ == "__main__":
    asyncio.run(main())
