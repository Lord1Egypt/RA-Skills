#!/usr/bin/env python3
"""
King's Watching v0.4.0 - Multi-Scenario Test

Tests various task types and edge cases
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/kingswatching')

from overseer import TaskTranslator, Overseer


def test_scenario(name, command, expected_type="search_download"):
    """Test a scenario"""
    
    print(f"\n{'='*70}")
    print(f"Scenario: {name}")
    print(f"Command: '{command}'")
    print(f"{'-'*70}")
    
    translator = TaskTranslator()
    plan = translator.translate(command)
    
    wf = plan.get('workflow', {})
    
    print(f"Detected type: {wf.get('task_type', 'unknown')}")
    print(f"Total units: {wf.get('total_units', 0)}")
    print(f"Number of steps: {len(plan.get('steps', []))}")
    
    # Show first 3 steps
    steps = plan.get('steps', [])
    if steps:
        print("\nFirst 3 steps:")
        for i, step in enumerate(steps[:3], 1):
            print(f"  {i}. {step.get('name', 'N/A')}")
            print(f"     └─ {step.get('description', 'N/A')}")
    
    if len(steps) > 3:
        print(f"  ... ({len(steps) - 3} more)")
    
    return plan


def run_all_tests():
    """Run all test scenarios"""
    
    print("="*70)
    print("King's Watching v0.4.0 - Multi-Scenario Test")
    print("="*70)
    
    scenarios = [
        ("Download Reports", "Download 100 industry research reports"),
        ("Write Report", "Write 50000 words industry analysis report"),
        ("Analyze Data", "Analyze 1000 user feedback entries"),
        ("API Calls", "Call API 500 times to fetch data"),
        ("Process Files", "Process 200 PDF files"),
        ("Develop Modules", "Develop 10 feature modules"),
        ("Write Tests", "Write 50 unit test cases"),
        ("Small Task", "Download 5 reference materials"),
        ("Large Task", "Download 1000 academic papers"),
        ("Complex Task", "Research new energy industry policy market technology from 4 dimensions, collect 200 reports"),
    ]
    
    results = []
    for name, command in scenarios:
        try:
            plan = test_scenario(name, command)
            results.append((name, "✅ Pass", len(plan.get('steps', []))))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((name, "❌ Fail", 0))
    
    # Summary
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    
    passed = sum(1 for _, status, _ in results if "Pass" in status)
    failed = sum(1 for _, status, _ in results if "Fail" in status)
    
    for name, status, steps in results:
        print(f"{status} {name} ({steps} steps)")
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    
    print(f"\n{'='*70}")
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print(f"{'='*70}")
