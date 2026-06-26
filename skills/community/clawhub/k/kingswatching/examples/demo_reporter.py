#!/usr/bin/env python3
"""
King's Watching v0.4.0 - Progress Reporter Demo

Demonstrates natural language interval configuration
"""

import sys
import time
sys.path.insert(0, '/root/.openclaw/workspace/skills/kingswatching')

from overseer import Overseer


def demo_reporter():
    """Demonstrate periodic reporting"""
    
    print("="*70)
    print("King's Watching v0.4.0 - Progress Reporter Demo")
    print("="*70)
    print()
    print("Supported interval formats:")
    print("  - 'Every 5 minutes' → 300 seconds")
    print("  - 'Every 10 min' → 600 seconds")
    print("  - 'Every 30 seconds' → 30 seconds")
    print("  - 'Every 1 hour' → 3600 seconds")
    print("  - 'Quarterly' → 900 seconds (15 minutes)")
    print()
    
    # Create workflow with natural language report interval
    workflow = Overseer(
        name="demo_reporter",
        description="Demo periodic reporting",
        report_interval="Every 3 seconds",  # Fast for demo
        enable_heartbeat=True
    )
    
    @workflow.step("Step 1: Prepare")
    def step1(ctx):
        time.sleep(1)
        return {"status": "prepared"}
    
    @workflow.step("Step 2: Process")
    def step2(ctx):
        for i in range(5):
            time.sleep(0.5)
            ctx.heartbeat(f"Processing {i+1}/5")
        return {"processed": 5}
    
    @workflow.step("Step 3: Complete")
    def step3(ctx):
        time.sleep(1)
        return {"done": True}
    
    print("Starting workflow with auto progress reports...")
    print()
    
    result = workflow.run()
    
    print()
    print("="*70)
    print(f"Final result: {result}")
    print("="*70)


def demo_comparison():
    """Compare: with vs without reporter"""
    
    print("\n" + "="*70)
    print("Comparison: With vs Without Reporter")
    print("="*70)
    print()
    
    print("❌ Without reporter:")
    print("  User: 'How's it going?'")
    print("  AI:  '...' (silent)")
    print("  User: 'Done yet?'")
    print("  AI:  '...' (still silent)")
    print("  User: 'Hello??'")
    print()
    
    print("✅ With reporter (every 5 minutes):")
    print("  [00:00] Task started, 5 steps total")
    print("  [00:05] Progress report #1: 2/5 (40%), ETA 8 minutes")
    print("  [00:10] Progress report #2: 4/5 (80%), ETA 2 minutes")
    print("  [00:12] Task complete!")
    print()


if __name__ == "__main__":
    demo_reporter()
    demo_comparison()
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("="*70)
