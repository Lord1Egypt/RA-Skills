#!/usr/bin/env python3
"""
Sparse Activation Script - Activate only relevant submodules.
Simulates sparse coding with <5% neuron activation principle.
"""

import json
import sys
from typing import Dict, List


def activate_sparse(modules: List[Dict], threshold: float = 0.05) -> List[Dict]:
    """
    Activate sparse subset of modules based on priority and threshold.
    
    Args:
        modules: All available modules
        threshold: Maximum active ratio (default 5% like brain)
        
    Returns:
        List of active module definitions
    """
    if not modules:
        return []
    
    # Sort by priority (lower = higher priority)
    sorted_modules = sorted(modules, key=lambda m: m.get("priority", 999))
    
    active = []
    for module in sorted_modules:
        # Activate high priority modules
        if module.get("priority", 999) <= 2:
            active.append(module)
        else:
            # Check if we're at threshold
            active_ratio = len(active) / len(sorted_modules)
            if active_ratio < threshold:
                active.append(module)
            else:
                break
    
    return active


def filter_modules(task_type: str, modules: List[Dict]) -> List[Dict]:
    """
    Filter modules based on task type.
    
    Args:
        task_type: Type of task (e.g., "qa", "analysis", "generation")
        modules: All available modules
        
    Returns:
        Filtered module list
    """
    task_keywords = {
        "qa": ["language", "memory"],
        "analysis": ["perception", "association", "decision"],
        "generation": ["language", "memory", "action"],
        "multi_modal": ["perception", "language", "association"]
    }
    
    allowed_types = task_keywords.get(task_type, ["memory"])
    
    return [m for m in modules if m["name"] in allowed_types]


def main():
    """Main entry point for sparse activation."""
    if len(sys.argv) < 2:
        print("Usage: python sparse_activate.py --modules <module1,module2> --threshold <ratio>")
        print("\nExample:")
        print("  python sparse_activate.py --modules 'visual,language,association' --threshold 0.1")
        return
    
    args = sys.argv[1:]
    
    # Parse arguments
    modules = []
    task_type = None
    threshold = 0.05
    
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
        elif arg.startswith("--threshold="):
            threshold = float(arg[13:])
        elif arg.startswith("--task="):
            task_type = arg[7:]
    
    if not modules:
        print("Error: Please specify modules with --modules='name1,name2,...'")
        return
    
    print(f"=== Sparse Activation ===\n")
    print(f"Available modules: {len(modules)}")
    print(f"Task type: {task_type or 'general'}")
    print(f"Threshold: {threshold:.1%}\n")
    
    # Apply filtering if task type specified
    if task_type:
        filtered = filter_modules(task_type, modules)
        print(f"After task filtering: {len(filtered)} modules\n")
        modules = filtered
    
    # Activate sparse subset
    active = activate_sparse(modules, threshold)
    
    print(f"Activated {len(active)} out of {len(modules)} modules")
    print(f"Activation ratio: {len(active)/len(modules):.1%}\n")
    
    print("Active modules:")
    for i, module in enumerate(active, 1):
        print(f"  [{i}] {module['name']}: {module['function']}")
    
    print(f"\nEnergy savings: {(1 - len(active)/len(modules))*100:.0f}%")


if __name__ == "__main__":
    main()
