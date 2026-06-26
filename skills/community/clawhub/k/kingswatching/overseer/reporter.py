#!/usr/bin/env python3
"""
King's Watching v0.4.0 - Progress Reporter

Supports natural language interval configuration, periodic execution progress output
"""

import re
import time
import threading
from typing import Optional, Callable, Dict, Any
from datetime import datetime, timedelta


class ProgressReporter:
    """
    Periodic Progress Reporter
    
    Features:
    1. Natural language interval parsing ("every 5 minutes" → 300 seconds)
    2. Timed progress reporting
    3. Customizable report content and callbacks
    """
    
    # Default report interval (seconds)
    DEFAULT_INTERVAL = 900  # 15 minutes
    
    # Time unit mappings
    TIME_UNITS = {
        "sec": 1,
        "second": 1,
        "s": 1,
        "min": 60,
        "minute": 60,
        "m": 60,
        "hour": 3600,
        "h": 3600,
        "hr": 3600,
    }
    
    def __init__(
        self,
        interval_desc: str = None,  # Natural language description, e.g. "every 5 minutes"
        interval_seconds: int = None,  # Direct seconds specification
        report_callback: Callable = None,  # Report callback function
        enabled: bool = True
    ):
        """
        Initialize reporter
        
        Args:
            interval_desc: Natural language description, e.g. "report every 5 minutes"
            interval_seconds: Direct seconds specification (higher priority than interval_desc)
            report_callback: Report callback function, receives report data
            enabled: Whether reporting is enabled
        """
        self.enabled = enabled
        self.report_callback = report_callback or self._default_report
        
        # Parse report interval
        if interval_seconds is not None:
            self.interval = interval_seconds
        elif interval_desc:
            self.interval = self._parse_interval(interval_desc)
        else:
            self.interval = self.DEFAULT_INTERVAL
        
        # Report state
        self._start_time = None
        self._last_report_time = None
        self._report_count = 0
        self._stop_event = threading.Event()
        self._report_thread = None
        self._workflow_name = None
        self._total_steps = 0
        self._current_step = 0
        self._step_status = {}
        
    def _parse_interval(self, desc: str) -> int:
        """
        Parse natural language interval description
        
        Args:
            desc: e.g. "report every 5 minutes", "every 10 minutes", "every 30 seconds"
            
        Returns:
            Interval in seconds
        """
        import re
        
        desc = desc.strip().lower()
        
        # Special keywords (exact match)
        if "30 sec" in desc or "30s" in desc:
            return 30
        if "quarter" in desc or "15 min" in desc:
            return 900
        if "half hour" in desc or "30 min" in desc:
            return 1800
        
        # Match number + unit pattern
        patterns = [
            # every 15 minutes, every 15 min
            r"every\s+(\d+)\s*(sec|second|s|min|minute|m|hour|h|hr)s?",
            # 15 minutes once, every fifteen minutes
            r"(\d+)\s*(sec|second|s|min|minute|m|hour|h|hr)s?.*?(once|time)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, desc)
            if match:
                num_str = match.group(1)
                unit = match.group(2)
                
                try:
                    value = float(num_str)
                except:
                    continue
                
                # Get unit seconds
                unit_seconds = 60  # Default minutes
                for unit_key, unit_val in self.TIME_UNITS.items():
                    if unit_key in unit:
                        unit_seconds = unit_val
                        break
                
                return int(value * unit_seconds)
        
        # Default 15 minutes
        return self.DEFAULT_INTERVAL
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            if secs == 0:
                return f"{minutes}min"
            return f"{minutes}m{secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes == 0:
                return f"{hours}h"
            return f"{hours}h{minutes}m"
    
    def _default_report(self, data: Dict[str, Any]) -> None:
        """Default report output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{'='*60}")
        print(f"📊 [{timestamp}] Progress Report #{data['report_count']}")
        print(f"{'='*60}")
        print(f"Task: {data['workflow_name']}")
        print(f"Overall: {data['current_step']}/{data['total_steps']} ({data['progress_percent']:.1f}%)")
        print(f"Elapsed: {data['elapsed_formatted']}")
        print(f"ETA: {data['eta_formatted']}")
        
        if data.get('current_step_name'):
            print(f"Current: {data['current_step_name']}")
        
        if data.get('step_status'):
            completed = sum(1 for s in data['step_status'].values() if s == 'completed')
            print(f"Steps: {completed} done / {len(data['step_status'])} total")
        
        print(f"{'='*60}\n")
    
    def start(self, workflow_name: str, total_steps: int) -> None:
        """Start reporter"""
        if not self.enabled:
            return
            
        self._workflow_name = workflow_name
        self._total_steps = total_steps
        self._current_step = 0
        self._start_time = time.time()
        self._last_report_time = self._start_time
        self._report_count = 0
        self._step_status = {}
        
        # Start background report thread
        self._stop_event.clear()
        self._report_thread = threading.Thread(target=self._report_loop, daemon=True)
        self._report_thread.start()
        
        # Report immediately
        self._do_report()
    
    def stop(self) -> None:
        """Stop reporter"""
        if not self.enabled:
            return
            
        self._stop_event.set()
        if self._report_thread and self._report_thread.is_alive():
            self._report_thread.join(timeout=1)
        
        # Final report
        self._do_report(final=True)
    
    def update_step(
        self,
        step_index: int,
        step_name: str,
        status: str = "running",
        step_data: Dict = None
    ) -> None:
        """Update step status"""
        self._current_step = step_index
        self._step_status[step_name] = status
        
        # Report immediately if step completed
        if status == "completed":
            self._do_report()
    
    def _report_loop(self) -> None:
        """Background report loop"""
        while not self._stop_event.is_set():
            # Wait for report interval
            if self._stop_event.wait(self.interval):
                break
            
            # Execute report
            self._do_report()
    
    def _do_report(self, final: bool = False) -> None:
        """Execute report"""
        if not self.enabled or self._start_time is None:
            return
        
        now = time.time()
        elapsed = int(now - self._start_time)
        
        # Calculate estimated remaining time
        if self._current_step > 0 and self._total_steps > 0:
            avg_time_per_step = elapsed / self._current_step
            remaining_steps = self._total_steps - self._current_step
            eta = int(avg_time_per_step * remaining_steps)
        else:
            eta = 0
        
        # Calculate progress percentage
        progress = (self._current_step / self._total_steps * 100) if self._total_steps > 0 else 0
        
        # Get current step name
        current_step_name = None
        for name, status in self._step_status.items():
            if status == "running":
                current_step_name = name
                break
        
        # Assemble report data
        report_data = {
            "report_count": self._report_count + 1,
            "workflow_name": self._workflow_name,
            "total_steps": self._total_steps,
            "current_step": self._current_step,
            "progress_percent": progress,
            "elapsed_seconds": elapsed,
            "elapsed_formatted": self._format_duration(elapsed),
            "eta_seconds": eta,
            "eta_formatted": self._format_duration(eta),
            "current_step_name": current_step_name,
            "step_status": self._step_status.copy(),
            "is_final": final,
            "interval_seconds": self.interval,
        }
        
        # Execute callback
        try:
            self.report_callback(report_data)
            self._report_count += 1
            self._last_report_time = now
        except Exception as e:
            print(f"Report error: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        if self._start_time is None:
            return {}
        
        elapsed = int(time.time() - self._start_time)
        completed = sum(1 for s in self._step_status.values() if s == 'completed')
        
        return {
            "workflow_name": self._workflow_name,
            "total_steps": self._total_steps,
            "completed_steps": completed,
            "total_time": self._format_duration(elapsed),
            "total_seconds": elapsed,
            "report_count": self._report_count,
        }


# Convenience function
def create_reporter(interval_desc: str = None, **kwargs) -> ProgressReporter:
    """Create reporter"""
    return ProgressReporter(interval_desc=interval_desc, **kwargs)


# Test
if __name__ == "__main__":
    print("="*60)
    print("ProgressReporter Test")
    print("="*60)
    
    # Test natural language parsing
    test_cases = [
        "every 5 minutes",
        "every 10 min",
        "every 30 seconds",
        "every 1 hour",
        "every 15 min",
        "every 2 minutes",
        "every 20 min",
    ]
    
    print("\n📌 Natural Language Parsing Test:")
    for desc in test_cases:
        reporter = ProgressReporter(interval_desc=desc, enabled=False)
        print(f"  '{desc}' → {reporter.interval}s ({reporter._format_duration(reporter.interval)})")
    
    # Simulate report flow
    print("\n📌 Simulated Report Flow (every 3 seconds):")
    
    def custom_report(data):
        status = "✅ Complete" if data['is_final'] else "⏳ In Progress"
        print(f"[{data['report_count']:02d}] {status} {data['progress_percent']:.0f}% | "
              f"Elapsed {data['elapsed_formatted']} | ETA {data['eta_formatted']}")
    
    reporter = ProgressReporter(
        interval_desc="every 3 seconds",
        report_callback=custom_report
    )
    
    # Simulate 3-step workflow
    reporter.start("Test Workflow", total_steps=3)
    
    for i in range(1, 4):
        reporter.update_step(i, f"step_{i}", "running")
        time.sleep(2)  # Simulate execution time
        reporter.update_step(i, f"step_{i}", "completed")
        time.sleep(1)
    
    reporter.stop()
    
    print("\n📌 Execution Summary:")
    summary = reporter.get_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")
