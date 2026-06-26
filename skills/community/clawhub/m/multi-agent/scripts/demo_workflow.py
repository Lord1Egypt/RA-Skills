#!/usr/bin/env python3
"""
Production Four-Phase Multi-Agent Workflow Demo

This script demonstrates the complete workflow:
1. Research Phase: Spawn 3 parallel researchers
2. Synthesis Phase: Coordinator generates specification
3. Implementation Phase: Spawn 2 implementers
4. Verification Phase: Spawn 2 verifiers

Usage: python3 demo_workflow.py "Your task description here"
"""

import sys
import time
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from coordinator_v2 import Coordinator, Worker, WorkerStatus


def demo_four_phase_workflow(task: str):
    """Run complete four-phase workflow"""
    
    print("="*70)
    print(" MULTI-AGENT WORKFLOW DEMO")
    print("="*70)
    print(f"\nTask: {task}\n")
    
    coordinator = Coordinator(scratchpad_dir=".openclaw/scratchpad")
    
    # ========================================================================
    # PHASE 1: RESEARCH
    # ========================================================================
    print("\n" + "="*70)
    print(" PHASE 1: RESEARCH")
    print("="*70)
    
    research_tasks = [
        f"Explore the codebase structure for: {task}. Find all relevant files and understand the architecture.",
        f"Analyze the current implementation related to: {task}. Identify patterns and potential issues.",
        f"Research dependencies and requirements for: {task}. What needs to change?"
    ]
    
    research_workers = []
    for i, rtask in enumerate(research_tasks, 1):
        print(f"\n[Research {i}/3] Preparing worker...")
        result = coordinator.spawn_worker(
            task=rtask,
            role="researcher",
            context=f"Research angle {i}/3",
            timeout=180
        )
        if result:
            worker, prompt = result
            research_workers.append(worker)
            
            # In real usage, you would now spawn this via sessions_spawn
            # For demo, we simulate completion after a delay
            print(f"  Worker ID: {worker.id}")
            print(f"  Prompt saved, ready to spawn via sessions_spawn")
    
    print(f"\n[Phase 1] Prepared {len(research_workers)} research workers")
    print("[Phase 1] In production, these would be spawned and run in parallel")
    
    # ========================================================================
    # PHASE 2: SYNTHESIS
    # ========================================================================
    print("\n" + "="*70)
    print(" PHASE 2: SYNTHESIS")
    print("="*70)
    
    # For demo, simulate that workers completed
    print("\n[Phase 2] Simulating worker completions...")
    for i, worker in enumerate(research_workers, 1):
        # Simulate receiving notification
        notification = f"""<task-notification>
  <task-id>{worker.id}</task-id>
  <status>completed</status>
  <summary>Found {5+i} relevant files and identified key patterns</summary>
  <result>
Research finding {i}:
- Analyzed codebase structure
- Found relevant modules in src/ and lib/
- Identified dependencies: x, y, z
- Recommended approach: refactoring with backward compatibility
  </result>
</task-notification>"""
        coordinator.process_notification(worker.id, notification)
    
    print(f"[Phase 2] Processing {len(research_workers)} research results...")
    
    # Generate specification
    spec = coordinator.generate_spec(research_workers)
    
    if spec:
        print(f"\n[Phase 2] ✓ Specification generated")
        print(f"[Phase 2] Saved to scratchpad/specs/")
    
    # ========================================================================
    # PHASE 3: IMPLEMENTATION
    # ========================================================================
    print("\n" + "="*70)
    print(" PHASE 3: IMPLEMENTATION")
    print("="*70)
    
    impl_tasks = [
        f"Implement core changes based on specification:\n{spec[:500]}...",
        f"Update related files and add helper functions:\n{spec[:500]}..."
    ]
    
    impl_workers = []
    for i, itask in enumerate(impl_tasks, 1):
        print(f"\n[Implementation {i}/2] Preparing worker...")
        result = coordinator.spawn_worker(
            task=itask,
            role="implementer",
            context=f"Implementation worker {i}/2",
            timeout=300
        )
        if result:
            worker, prompt = result
            impl_workers.append(worker)
            
            # Simulate completion
            notification = f"""<task-notification>
  <task-id>{worker.id}</task-id>
  <status>completed</status>
  <summary>Implemented changes: modified 3 files, added 2 helper functions</summary>
  <result>
Implementation {i}:
- Modified: src/core.py (lines 45-67)
- Modified: src/utils.py (lines 12-34)
- Added: src/helpers.py (new file, 120 lines)
- All changes follow existing patterns
  </result>
</task-notification>"""
            coordinator.process_notification(worker.id, notification)
    
    print(f"\n[Phase 3] Completed {len(impl_workers)} implementation workers")
    
    # ========================================================================
    # PHASE 4: VERIFICATION
    # ========================================================================
    print("\n" + "="*70)
    print(" PHASE 4: VERIFICATION")
    print("="*70)
    
    verif_tasks = [
        "Run tests and verify implementation works correctly",
        "Check for regressions and edge cases"
    ]
    
    verif_workers = []
    for i, vtask in enumerate(verif_tasks, 1):
        print(f"\n[Verification {i}/2] Preparing worker...")
        result = coordinator.spawn_worker(
            task=vtask,
            role="verifier",
            timeout=180
        )
        if result:
            worker, prompt = result
            verif_workers.append(worker)
            
            # Simulate completion
            notification = f"""<task-notification>
  <task-id>{worker.id}</task-id>
  <status>completed</status>
  <summary>All tests passed, no regressions found</summary>
  <result>
Verification {i}:
- Unit tests: 42/42 passed
- Integration tests: 15/15 passed
- No regressions detected
- Code coverage: 87%
  </result>
</task-notification>"""
            coordinator.process_notification(worker.id, notification)
    
    print(f"\n[Phase 4] Completed {len(verif_workers)} verification workers")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print(" WORKFLOW COMPLETED")
    print("="*70)
    
    all_workers = research_workers + impl_workers + verif_workers
    completed = len([w for w in all_workers if w.status == WorkerStatus.COMPLETED])
    
    print(f"\nSummary:")
    print(f"  Total workers: {len(all_workers)}")
    print(f"  Completed: {completed}")
    print(f"  Phases: Research ({len(research_workers)}) → Implementation ({len(impl_workers)}) → Verification ({len(verif_workers)})")
    
    print(f"\nResults saved to: .openclaw/scratchpad/")
    print(f"  - workers/     : Worker state files")
    print(f"  - results/     : Worker results")
    print(f"  - specs/       : Generated specifications")
    print(f"  - prompts/     : Worker prompts")
    
    print("\n" + "="*70)
    print(" DEMO COMPLETE")
    print("="*70)
    print("\nNote: This was a demonstration with simulated worker completions.")
    print("In production, use sessions_spawn to run workers in parallel.")


def real_workflow_example():
    """Show how to use this in real production"""
    print("""
Real Production Usage:
======================

1. Prepare workers (creates prompts and specs):
   
   python3 coordinator_v2.py prepare "Your task" --role researcher

2. Spawn workers via OpenClaw (run for each prepared worker):
   
   sessions_spawn --label "multi-agent-worker-{id}" \\
                  --task "$(cat .openclaw/scratchpad/prompts/prompt-{id}.txt)" \\
                  --timeout 300

3. When workers complete, they output XML notifications.
   Collect these and process:
   
   python3 coordinator_v2.py notify {worker-id} --file notification.xml

4. Generate specification from completed research workers:
   
   python3 coordinator_v2.py spec {worker-id-1} {worker-id-2} {worker-id-3}

5. Repeat phases 3-4 (Implementation → Verification) with new workers

For full automation, wrap steps 2-3 in a polling loop that checks
sessions_history for each worker session periodically.
""")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(__doc__)
            sys.exit(0)
        elif sys.argv[1] == "--real" or sys.argv[1] == "-r":
            real_workflow_example()
            sys.exit(0)
        else:
            task = " ".join(sys.argv[1:])
    else:
        task = "Refactor the authentication module to use OAuth2"
    
    demo_four_phase_workflow(task)
