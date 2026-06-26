#!/usr/bin/env python3
"""
King's Watching v0.4.0 - Development Task Splitting Demo

Shows how TaskTranslator handles software development tasks
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/kingswatching')

from overseer import TaskTranslator


def test_dev_task(name, command):
    """Test development task translation"""
    
    print("="*70)
    print(f"Task: {name}")
    print(f"Command: {command}")
    print("-"*70)
    
    translator = TaskTranslator()
    plan = translator.translate(command)
    
    print(f"Task type: {plan['workflow']['task_type']}")
    print(f"Total units: {plan['workflow']['total_units']}")
    print(f"Split into: {len(plan['steps'])} Steps")
    print()
    
    print("Execution plan:")
    for i, step in enumerate(plan['steps'][:5], 1):  # Show first 5
        print(f"  Step {i}: {step['description']}")
        print(f"         └─ Verify: At least {step['verification']['min_required']} items")
    
    if len(plan['steps']) > 5:
        print(f"  ... ({len(plan['steps']) - 5} more Steps)")
    
    print()


def demo_development_tasks():
    """Demo various development tasks"""
    
    print("="*70)
    print("King's Watching v0.4.0 - Development Task Splitting Demo")
    print("="*70)
    print()
    
    # Test case 1: Module development
    test_dev_task(
        "Develop Feature Modules",
        "Develop 10 user management modules"
    )
    
    # Test case 2: API implementation
    test_dev_task(
        "Implement REST APIs",
        "Implement 20 REST API endpoints"
    )
    
    # Test case 3: Write tests
    test_dev_task(
        "Write Unit Tests",
        "Write 50 unit test cases"
    )
    
    # Test case 4: Code refactoring
    test_dev_task(
        "Refactor Legacy Code",
        "Refactor 12 legacy modules"
    )
    
    # Test case 5: Write documentation
    test_dev_task(
        "Write API Documentation",
        "Write API documentation for 30 endpoints"
    )
    
    # Test case 6: Code review
    test_dev_task(
        "Code Review",
        "Review 25 code submissions"
    )


def demo_comparison():
    """Compare development with and without King's Watching"""
    
    print("="*70)
    print("Comparison: With vs Without King's Watching")
    print("="*70)
    print()
    
    print("❌ Without King's Watching:")
    print("  PM: 'Develop 10 feature modules this week'")
    print("  Dev: 'Working on it...'")
    print("  [End of week]")
    print("  PM: 'How many done?'")
    print("  Dev: '3 modules, but they're very high quality!'")
    print("  PM: '...'")
    print()
    
    print("✅ With King's Watching:")
    print("  PM: 'Develop 10 feature modules'")
    print("  King's Watching: 'Splitting into 4 Steps, 3 modules each'")
    print("  Day 1: Step 1 complete ✓ (Modules 1-3 verified)")
    print("  Day 2: Step 2 complete ✓ (Modules 4-6 verified)")
    print("  Day 3: Step 3 complete ✓ (Modules 7-9 verified)")
    print("  Day 4: Step 4 complete ✓ (Module 10 verified)")
    print("  Result: All 10 modules complete, every one verified")
    print()


if __name__ == "__main__":
    demo_development_tasks()
    demo_comparison()
    
    print("="*70)
    print("Demo complete!")
    print("="*70)
