"""
Memory Search Script
Search ReMe memory with semantic queries
"""

import asyncio
import sys
from reme.reme_light import ReMeLight


async def search_memory(working_dir=".reme", query="", max_results=5):
    """
    Search memory for specific information

    Args:
        working_dir: Path to ReMe working directory
        query: Search query
        max_results: Maximum number of results

    Returns:
        list: Matching memories
    """
    # Initialize ReMe
    reme = ReMeLight(working_dir=working_dir)
    await reme.start()

    # Search
    print(f"🔍 Searching for: {query}")
    results = await reme.memory_search(
        query=query,
        max_results=max_results
    )

    # Display results
    if results:
        print(f"\n✓ Found {len(results)} results:\n")
        for i, result in enumerate(results, 1):
            content = result.get('content', '')
            source = result.get('source', 'unknown')

            print(f"{i}. [{source}]")
            print(f"   {content[:150]}{'...' if len(content) > 150 else ''}")
            print()
    else:
        print(f"\n❌ No results found for: {query}")

    # Close
    await reme.close()

    return results


async def search_by_category(working_dir=".reme", category=""):
    """
    Search by specific category

    Args:
        working_dir: Path to ReMe working directory
        category: Category to search (e.g., "文件", "代码", "工具")
    """
    query = f"{category} 偏好 规则"
    return await search_memory(working_dir, query)


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python search_memory.py <query> [max_results]")
        print("  python search_memory.py --category <category> [max_results]")
        print("\nExamples:")
        print("  python search_memory.py \"文件发送 偏好\"")
        print("  python search_memory.py \"文件发送 偏好\" 3")
        print("  python search_memory.py --category 文件")
        return

    # Parse args
    if sys.argv[1] == "--category":
        if len(sys.argv) < 3:
            print("Error: --category requires a category argument")
            return

        category = sys.argv[2]
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        await search_by_category(category=category, max_results=max_results)
    else:
        query = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
        max_results = int(sys.argv[-1]) if sys.argv[-1].isdigit() and len(sys.argv) > 2 else 5

        if not query:
            print("Error: No query provided")
            return

        await search_memory(query=query, max_results=max_results)


if __name__ == "__main__":
    asyncio.run(main())
