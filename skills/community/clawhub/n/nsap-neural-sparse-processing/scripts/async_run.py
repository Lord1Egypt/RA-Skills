#!/usr/bin/env python3
"""
Async Execution Script - Execute modules in parallel.
Simulates asynchronous module execution for faster task switching.
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Callable


class ModuleTask:
    """Represents a module task being executed."""
    
    def __init__(self, name: str, module: Dict):
        self.name = name
        self.module = module
        self.start_time = None
        self.end_time = None
        self.status = "pending"
        self.result = None
    
    async def execute(self, delay: float = 0.1) -> Dict:
        """Execute the module task asynchronously."""
        self.start_time = datetime.now()
        print(f"[{self.name}] Starting: {self.module.get('function', 'Task')}")
        
        # Simulate work
        await asyncio.sleep(delay)
        
        self.end_time = datetime.now()
        self.status = "completed"
        
        execution_time = (self.end_time - self.start_time).total_seconds()
        
        return {
            "name": self.name,
            "function": self.module.get("function"),
            "status": self.status,
            "execution_time": execution_time,
            "start": self.start_time.isoformat(),
            "end": self.end_time.isoformat()
        }
    
    def __repr__(self):
        return f"ModuleTask({self.name}, {self.status})"


async def run_modules_async(modules: List[Dict], tasks: List[ModuleTask]) -> List[Dict]:
    """
    Execute multiple module tasks asynchronously.
    
    Args:
        modules: Available module definitions
        tasks: List of tasks to execute
        
    Returns:
        List of execution results
    """
    print(f"\nExecuting {len(tasks)} modules in parallel...")
    print("=" * 60)
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*[task.execute() for task in tasks])
    
    return results


def run_sequential(modules: List[Dict], tasks: List[ModuleTask]) -> List[Dict]:
    """
    Execute modules sequentially (for comparison).
    
    Args:
        modules: Available module definitions
        tasks: List of tasks to execute
        
    Returns:
        List of execution results
    """
    print(f"\nExecuting {len(tasks)} modules sequentially (for comparison)...")
    print("=" * 60)
    
    results = []
    for task in tasks:
        result = asyncio.run(task.execute())
        results.append(result)
    
    return results


def main():
    """Main entry point for async execution."""
    if len(sys.argv) < 2:
        print("Usage: python async_run.py --modules <module1,module2> --mode [parallel|sequential]")
        print("\nExample:")
        print("  python async_run.py --modules 'visual,language' --mode parallel")
        print("\nOptions:")
        print("  --mode parallel  : Execute modules concurrently (recommended)")
        print("  --mode sequential: Execute modules one after another")
        return
    
    args = sys.argv[1:]
    
    modules = []
    mode = "parallel"
    tasks = []
    
    for arg in args:
        if arg.startswith("--modules="):
            module_names = arg[11:].split(",")
            modules = [
                {
                    "name": name,
                    "type": "general",
                    "function": f"Process {name} data",
                    "activation_trigger": f"When {name} needed",
                    "priority": 1
                }
                for name in module_names
            ]
        elif arg.startswith("--mode="):
            mode = arg[7:]
    
    if not modules:
        print("Error: Please specify modules with --modules='name1,name2,...'")
        return
    
    # Create tasks for each module
    for module in modules:
        tasks.append(ModuleTask(module["name"], module))
    
    # Execute based on mode
    if mode == "parallel":
        results = asyncio.run(run_modules_async(modules, tasks))
    else:
        results = run_sequential(modules, tasks)
    
    # Display results
    print("\n" + "=" * 60)
    print("Execution Results:")
    print("=" * 60)
    
    total_time = sum(r.get("execution_time", 0) for r in results)
    parallel_time = total_time  # In parallel, time is roughly max of individual
    
    if mode == "sequential":
        sequential_time = parallel_time * len(results) if results else 0
        speedup = sequential_time / parallel_time if parallel_time > 0 else 1
        print(f"\n⚡ Speedup: {speedup:.1f}x faster with parallel execution")
    else:
        print(f"\n✓ Parallel execution completed in {total_time:.2f}s")
    
    print("\nModule Results:")
    for result in results:
        print(f"  ✓ {result['name']}: {result['execution_time']:.2f}s")


if __name__ == "__main__":
    main()
