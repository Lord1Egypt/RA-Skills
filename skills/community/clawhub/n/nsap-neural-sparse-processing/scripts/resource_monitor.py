#!/usr/bin/env python3
"""
Resource Monitor Script - Track efficiency gains and metrics.
Monitors modular processing vs traditional approaches.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List


class ResourceMonitor:
    """Monitor resource usage for modular processing."""
    
    def __init__(self):
        self.metrics = {
            "total_modules": 0,
            "active_modules": 0,
            "energy_used": 0,
            "time_taken": 0,
            "traditional_comparison": {}
        }
    
    def add_execution(self, module_name: str, time_ms: float):
        """Record an execution."""
        self.metrics["active_modules"] += 1
        self.metrics["time_taken"] += time_ms / 1000  # Convert to seconds
    
    def report(self) -> Dict:
        """Generate resource usage report."""
        active_ratio = self.metrics["active_modules"] / max(1, self.metrics["total_modules"])
        energy_savings = (1 - active_ratio) * 100
        
        return {
            "timestamp": datetime.now().isoformat(),
            "modular_processing": {
                "modules_used": self.metrics["active_modules"],
                "total_available": self.metrics["total_modules"],
                "activation_ratio": active_ratio,
                "time_taken_s": self.metrics["time_taken"],
                "energy_units": self.metrics["active_modules"]
            },
            "traditional_comparison": {
                "would_use_modules": self.metrics["total_modules"],
                "activation_ratio": 1.0,
                "time_estimate_s": self.metrics["time_taken"] * 1.5,
                "energy_units": self.metrics["total_modules"]
            },
            "improvement": {
                "energy_savings_pct": energy_savings,
                "time_savings_estimate": self.metrics["time_taken"] * 0.5,
                "efficiency_boost": f"{energy_savings:.0f}% energy savings"
            }
        }


def main():
    """Main entry point for resource monitoring."""
    monitor = ResourceMonitor()
    
    print("=== Modular Processing Resource Monitor ===\n")
    print("This script tracks efficiency gains when using modular processing.")
    print("It compares modular approach vs traditional dense activation.\n")
    
    # Simulate some executions
    print("Simulating task execution...\n")
    
    # Example scenario
    modules = ["perception", "association", "decision", "memory", "action"]
    monitor.metrics["total_modules"] = len(modules)
    
    print(f"Available modules: {', '.join(modules)}\n")
    
    # Simulate activating only necessary modules
    print("Activating modules based on task requirements...\n")
    
    # Active modules for this task
    active_modules = ["perception", "association", "memory"]
    
    for module in active_modules:
        time_ms = 100  # Simulated execution time
        monitor.add_execution(module, time_ms)
        print(f"  ✓ {module}: {time_ms}ms")
    
    # Display report
    print("\n" + "=" * 60)
    print("Resource Usage Report")
    print("=" * 60)
    
    report = monitor.report()
    
    print(f"\n📊 Modular Processing:")
    print(f"   Modules used: {report['modular_processing']['modules_used']}")
    print(f"   Activation ratio: {report['modular_processing']['activation_ratio']:.1%}")
    print(f"   Time taken: {report['modular_processing']['time_taken_s']:.2f}s")
    print(f"   Energy units: {report['modular_processing']['energy_units']}")
    
    print(f"\n⚖️  Traditional Comparison:")
    print(f"   Would use modules: {report['traditional_comparison']['would_use_modules']}")
    print(f"   Activation ratio: {report['traditional_comparison']['activation_ratio']:.0%}")
    print(f"   Estimated time: {report['traditional_comparison']['time_estimate_s']:.2f}s")
    print(f"   Energy units: {report['traditional_comparison']['energy_units']}")
    
    print(f"\n🚀 Improvement:")
    print(f"   Energy savings: {report['improvement']['energy_savings_pct']:.0f}%")
    print(f"   Time savings estimate: ~{report['improvement']['time_savings_estimate']:.2f}s")
    print(f"   Overall boost: {report['improvement']['efficiency_boost']}")
    
    print(f"\n💡 Recommendation:")
    print(f"   Continue using modular processing for {report['improvement']['energy_savings_pct']:.0f}% energy savings!")
    
    # Save report to file
    report_file = "resource_usage.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📝 Report saved to: {report_file}")


if __name__ == "__main__":
    main()
