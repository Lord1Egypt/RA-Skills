#!/usr/bin/env python3
"""Performance Monitor - Auto-generated"""
import time
import json
from functools import lru_cache
from datetime import datetime
from typing import Dict, Any

class PerformanceMonitor:
    def __init__(self):
        self.metrics = []
    
    def record(self, operation: str, duration: float, success: bool):
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": duration * 1000,
            "success": success
        })
    
    def get_stats(self) -> Dict[str, Any]:
        if not self.metrics:
            return {}
        durations = [m["duration_ms"] for m in self.metrics]
        return {
            "total_operations": len(self.metrics),
            "avg_duration_ms": sum(durations) / len(durations),
            "success_rate": sum(1 for m in self.metrics if m["success"]) / len(self.metrics)
        }
