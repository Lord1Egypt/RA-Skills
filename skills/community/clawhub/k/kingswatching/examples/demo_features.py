#!/usr/bin/env python3
"""
King's Watching Feature Demo - Long Tasks + Heartbeat + Async Execution

Scenario: Batch process 1000 data entries, estimated 30 minutes runtime
"""

import sys
import time
sys.path.insert(0, '/root/.openclaw/workspace/skills/kingswatching')

from overseer import Overseer


# Simulate long-running task
def process_batch(items, ctx):
    """Process a batch of data with heartbeat reports"""
    for i, item in enumerate(items):
        # Simulate processing time
        time.sleep(0.1)
        
        # Send heartbeat every 10 items
        if i % 10 == 0:
            ctx.heartbeat(f"Processed {i}/{len(items)} items")
    
    return {"processed": len(items)}


# ==================== Example 1: Sync Execution (Short Tasks) ====================

def demo_sync():
    """Sync execution example - for tasks <15 minutes"""
    print("="*60)
    print("Example 1: Sync Execution (Short Tasks)")
    print("="*60)
    
    workflow = Overseer(
        name="data_sync",
        description="Sync process 50 items (estimated 5 minutes)",
        enable_heartbeat=True,
        heartbeat_interval=30  # Report every 30 seconds
    )
    
    @workflow.step("Fetch Data")
    def step1(ctx):
        return {"total": 50, "source": "database"}
    
    @workflow.step("Process Data", heartbeat_interval=10)
    def step2(ctx):
        total = ctx.get_step_result("Fetch Data")["total"]
        items = list(range(total))
        return process_batch(items, ctx)
    
    @workflow.step("Save Results")
    def step3(ctx):
        processed = ctx.get_step_result("Process Data")["processed"]
        return {"saved": processed, "status": "ok"}
    
    # Sync execution (blocking)
    result = workflow.run()
    print(f"\nResult: {result}")


# ==================== Example 2: Async Execution (Long Tasks) ====================

def demo_async():
    """Async execution example - for tasks >15 minutes"""
    print("\n" + "="*60)
    print("Example 2: Async Execution (Long Tasks, Background)")
    print("="*60)
    
    workflow = Overseer(
        name="big_data_job",
        description="Batch process 1000 items (estimated 30 minutes)",
        enable_heartbeat=True,
        heartbeat_interval=60,  # Report every minute
        async_mode=True,
        notify_on_complete=True,
        notify_channel="discord"
    )
    
    @workflow.step("Fetch Data")
    def step1(ctx):
        return {"total": 1000, "batches": 10}
    
    @workflow.step("Batch Process", heartbeat_interval=10)
    def step2(ctx):
        """This step runs ~25 minutes, needs heartbeat to prevent timeout"""
        total = ctx.get_step_result("Fetch Data")["total"]
        items = list(range(total))
        return process_batch(items, ctx)
    
    @workflow.step("Generate Report")
    def step3(ctx):
        processed = ctx.get_step_result("Batch Process")["processed"]
        return {"report_url": f"https://example.com/report/{processed}"}
    
    # Async execution (returns immediately)
    job = workflow.run_async()
    
    print(f"\nJob submitted to background!")
    print(f"You can close the conversation, task continues")
    print(f"Notification sent when complete")
    
    # Simulate user checking status
    time.sleep(2)
    status = workflow.check_status(job.id)
    print(f"\nStatus check: {status.status if status else 'unknown'}")
    
    # Wait for completion (not needed in actual use)
    print("\nWaiting for background task (demo)...")
    time.sleep(5)


# ==================== Example 3: Checkpoint Resume ====================

def demo_resume():
    """Checkpoint resume example - recover after interruption"""
    print("\n" + "="*60)
    print("Example 3: Checkpoint Resume")
    print("="*60)
    
    workflow = Overseer(
        name="resume_demo",
        description="Demo checkpoint resume",
        allow_resume=True
    )
    
    @workflow.step("Step A")
    def step_a(ctx):
        return {"status": "done"}
    
    @workflow.step("Step B")
    def step_b(ctx):
        return {"status": "done"}
    
    @workflow.step("Step C")
    def step_c(ctx):
        return {"status": "done"}
    
    # Simulate: Interrupt at Step B
    print("Simulating: System interrupt at Step B...")
    
    # Restart, auto-recover
    print("Restarting, auto-recover from checkpoint...")
    try:
        result = workflow.resume()
        print(f"Resume complete: {result}")
    except ValueError as e:
        print(f"No history found, running new task: {e}")
        # First run
        result = workflow.run()
        print(f"First run complete: {result}")


# ==================== Example 4: Chunked Execution (Very Long) ====================

def demo_chunked():
    """Chunked execution example - task too long, split into multiple runs"""
    print("\n" + "="*60)
    print("Example 4: Chunked Execution (Process 10000 items in 10 runs)")
    print("="*60)
    
    workflow = Overseer(
        name="chunked_processing",
        description="Chunked processing of large data"
    )
    
    @workflow.step("Process Batch")
    def process_chunk(ctx):
        """Process 1000 items each time, record progress"""
        # Get last processed position
        cursor = ctx.get_state("cursor", 0)
        chunk_size = 1000
        
        print(f"   Starting from item {cursor}, processing {chunk_size} this batch")
        
        # Simulate processing
        items = list(range(cursor, cursor + chunk_size))
        for i, item in enumerate(items):
            time.sleep(0.01)  # Simulate processing
        
        # Update cursor
        new_cursor = cursor + chunk_size
        ctx.set_state("cursor", new_cursor)
        
        result = {
            "processed": chunk_size,
            "cursor": new_cursor,
            "has_more": new_cursor < 10000
        }
        
        # If more data, schedule next run
        if result["has_more"]:
            print(f"   More data, scheduling continue in 5 minutes...")
            # ctx.schedule_next_run(delay=300)  # Continue in 5 minutes
        
        return result
    
    # Run once (actually runs 10 times)
    result = workflow.run()
    print(f"\nThis run: Processed up to item {result.get('cursor', 0)}")


# ==================== Main ====================

if __name__ == "__main__":
    print("King's Watching v0.4.0 Feature Demo")
    print("="*60)
    print()
    
    # Select demo to run
    import sys
    
    if len(sys.argv) > 1:
        demo_name = sys.argv[1]
        if demo_name == "sync":
            demo_sync()
        elif demo_name == "async":
            demo_async()
        elif demo_name == "resume":
            demo_resume()
        elif demo_name == "chunked":
            demo_chunked()
        else:
            print(f"Unknown demo: {demo_name}")
    else:
        # Default run all demos (shortened)
        demo_sync()
        # demo_async()  # Async needs long time, skip by default
        demo_resume()
        demo_chunked()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
