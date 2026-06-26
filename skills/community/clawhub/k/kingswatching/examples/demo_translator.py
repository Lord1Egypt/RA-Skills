#!/usr/bin/env python3
"""
King's Watching v0.4.0 Example: Task Translator Demo

Demonstrates how natural language commands are auto-translated into executable Overseer workflows
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/kingswatching')

from overseer import TaskTranslator, translate_and_run


def demo_translation():
    """Demonstrate task translation process"""
    
    print("=" * 60)
    print("King's Watching v0.4.0 - Task Translator Demo")
    print("=" * 60)
    print()
    
    # Create translator
    translator = TaskTranslator()
    
    # Example 1: Download task
    command1 = "Download 100 photochemistry research reports"
    print(f"📝 Original command: {command1}")
    print()
    
    plan1 = translator.translate(command1)
    print(translator.explain_plan(plan1))
    print()
    
    # Example 2: Writing task
    command2 = "Write 100k word industry report"
    print(f"📝 Original command: {command2}")
    print()
    
    plan2 = translator.translate(command2)
    print(translator.explain_plan(plan2))
    print()
    
    # Example 3: Data analysis task
    command3 = "Analyze 1000 user feedback entries"
    print(f"📝 Original command: {command3}")
    print()
    
    plan3 = translator.translate(command3)
    print(translator.explain_plan(plan3))
    print()
    
    print("=" * 60)
    print("Core Features:")
    print("1. Natural language → Executable plan (auto task type recognition)")
    print("2. Big task → Small Steps (split by AI capacity limits)")
    print("3. Each Step forced verification (prevents AI slacking)")
    print("=" * 60)


def demo_execution():
    """Demonstrate actual execution (simulated)"""
    
    print("\n" + "=" * 60)
    print("Execution Demo: Download 100 reports")
    print("=" * 60)
    print()
    
    # Use translate_and_run one-liner execution
    # Note: This is framework demo, actual execution needs kimi_search/fetch integration
    
    translator = TaskTranslator()
    plan = translator.translate("Download 100 research reports")
    
    print("Generated execution plan:")
    print(f"- Total Steps: {len(plan['steps'])}")
    print(f"- Per Step target: 10 items")
    print(f"- Estimated total time: {plan['workflow']['estimated_time']} seconds")
    print()
    
    print("Execution flow preview:")
    for i, step in enumerate(plan['steps'], 1):
        print(f"  Step {i}: {step['description']}")
        print(f"         └─ Verify: Must complete at least {step['verification']['min_required']} items")
    
    print()
    print("✅ Each Step has forced verification, AI cannot cut corners")


def demo_comparison():
    """Compare: Traditional vs Translator approach"""
    
    print("\n" + "=" * 60)
    print("Comparison: Traditional vs TaskTranslator")
    print("=" * 60)
    print()
    
    print("❌ Traditional approach:")
    print("  User: 'Download 100 reports'")
    print("  AI:  'OK' → Downloads 14 → 'Done'")
    print("  Result: Only 14% complete, 86% slacking")
    print()
    
    print("✅ TaskTranslator approach:")
    print("  User: 'Download 100 reports'")
    print("  AI:  'Received, splitting into 10 Steps'")
    print("       Step 1: Download 1-10 ✓ (verification passed)")
    print("       Step 2: Download 11-20 ✓ (verification passed)")
    print("       ...")
    print("       Step 10: Download 91-100 ✓ (verification passed)")
    print("  Result: 100% complete, no slacking")
    print()


if __name__ == "__main__":
    demo_translation()
    demo_execution()
    demo_comparison()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
