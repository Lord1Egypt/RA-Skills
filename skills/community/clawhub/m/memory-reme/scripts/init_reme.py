"""
ReMe Initialization Script
Initializes ReMeLight and retrieves user preferences
"""

import asyncio
import sys
from reme.reme_light import ReMeLight


async def init_reme(working_dir=".reme", language="zh"):
    """
    Initialize ReMe and retrieve user preferences

    Args:
        working_dir: Path to ReMe working directory
        language: Memory summary language (zh/en)

    Returns:
        tuple: (reme_instance, preferences_list)
    """
    # Initialize ReMeLight
    reme = ReMeLight(
        working_dir=working_dir,
        max_input_length=128000,
        memory_compact_ratio=0.7,
        language=language,
        tool_result_threshold=1000,
        retention_days=7,
    )

    await reme.start()
    print("✓ ReMe initialized")
    print(f"  Working dir: {working_dir}")
    print(f"  Language: {language}")

    # Retrieve user preferences
    print("\n📖 Retrieving user preferences...")
    prefs = await reme.memory_search(
        query="用户偏好 偏好 规则",
        max_results=10
    )

    if prefs:
        print(f"✓ Found {len(prefs)} preferences")
        for i, pref in enumerate(prefs, 1):
            print(f"  {i}. {pref.get('content', pref)[:80]}...")
    else:
        print("  No preferences found yet")

    return reme, prefs


async def search_preferences(reme, query):
    """
    Search for specific preferences

    Args:
        reme: ReMeLight instance
        query: Search query

    Returns:
        list: Matching preferences
    """
    results = await reme.memory_search(
        query=query,
        max_results=5
    )
    return results


async def main():
    """Main entry point"""
    import os

    # Get working directory from args or use default
    working_dir = sys.argv[1] if len(sys.argv) > 1 else ".reme"
    language = sys.argv[2] if len(sys.argv) > 2 else "zh"

    # Ensure directory exists
    os.makedirs(working_dir, exist_ok=True)

    # Initialize
    reme, prefs = await init_reme(working_dir, language)

    # Print summary
    print("\n" + "="*50)
    print("INITIALIZATION COMPLETE")
    print("="*50)
    print(f"ReMe instance ready at: {working_dir}")
    print(f"Loaded {len(prefs)} preferences")
    print("\nUsage in Python code:")
    print("  reme, prefs = await init_reme()")
    print("  # Use reme and prefs throughout session")
    print("\nRemember to close when done:")
    print("  await reme.close()")


if __name__ == "__main__":
    asyncio.run(main())
