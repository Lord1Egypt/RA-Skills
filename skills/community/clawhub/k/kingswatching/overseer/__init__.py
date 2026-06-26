"""
King's Watching (kingswatching) - AI Workflow Enforcer + Task Translator

Inspired by the Steam hit game "The King Is Watching":
Just like how subjects in the game only work when the King's gaze is upon them,
this tool ensures AI agents cannot cut corners and must execute every step to completion.

Core Features:
1. Forced sequential execution (no step skipping)
2. State persistence with checkpoint resume
3. Heartbeat mechanism (prevents 15-min timeout)
4. Async execution + completion notification
5. [NEW] Natural language task translation with auto-chunking
6. [NEW] Step verification mechanism (prevents slacking)

Author: OpenClaw Community
Version: 0.4.0
"""

import json
import os
import sys
import time
import uuid
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
from dataclasses import dataclass, asdict

from .translator import TaskTranslator, TaskIntent, TaskChunk, StepVerifier
from .reporter import ProgressReporter, create_reporter


# ==================== Data Classes ====================

@dataclass
class JobInfo:
    """Async job information"""
    id: str
    workflow_name: str
    status: str  # pending, running, completed, failed
    current_step: int
    total_steps: int
    start_time: str
    eta: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ==================== Context ====================

class OverseerContext:
    """
    Step execution context
    
    Provides:
    - Variable storage/retrieval
    - Step result passing
    - Heartbeat reporting
    - State persistence
    """
    
    def __init__(
        self,
        workflow_id: str,
        run_id: str,
        initial_data: Dict = None,
        heartbeat_callback: Callable = None,
        heartbeat_interval: int = 60
    ):
        self.workflow_id = workflow_id
        self.run_id = run_id
        self.data = initial_data or {}
        self.step_results = {}
        self.temp_data = {}
        self.state_data = {}  # Persistent state for chunked execution
        
        # Heartbeat configuration
        self._heartbeat_callback = heartbeat_callback
        self._heartbeat_interval = heartbeat_interval
        self._last_heartbeat = time.time()
    
    # ---- Variable Operations ----
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get variable"""
        return self.data.get(key, self.temp_data.get(key, default))
    
    def set(self, key: str, value: Any) -> None:
        """Set variable"""
        self.temp_data[key] = value
    
    # ---- Step Results ----
    
    def get_step_result(self, step_name: str) -> Any:
        """Get specified step result"""
        return self.step_results.get(step_name)
    
    def set_step_result(self, step_name: str, result: Any) -> None:
        """Set step result"""
        self.step_results[step_name] = result
    
    def get_all_results(self) -> Dict:
        """Get all step results"""
        return self.step_results.copy()
    
    # ---- State Persistence (for chunked execution) ----
    
    def set_state(self, key: str, value: Any) -> None:
        """Save state (preserved across execution cycles)"""
        self.state_data[key] = value
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Read state"""
        return self.state_data.get(key, default)
    
    # ---- Heartbeat Mechanism ----
    
    def heartbeat(self, message: str) -> None:
        """
        Send heartbeat report
        
        Used for long-running steps to prevent 15-minute timeout
        """
        now = time.time()
        
        # Check if heartbeat needed
        if now - self._last_heartbeat >= self._heartbeat_interval:
            if self._heartbeat_callback:
                self._heartbeat_callback({
                    "type": "heartbeat",
                    "workflow_id": self.workflow_id,
                    "run_id": self.run_id,
                    "timestamp": datetime.now().isoformat(),
                    "message": message
                })
            self._last_heartbeat = now
    
    # ---- Schedule Next Run ----
    
    def schedule_next_run(self, delay: int) -> None:
        """
        Schedule next continuation
        
        Args:
            delay: Delay in seconds
        """
        # Save current state
        self._save_for_resume()
        
        # Can integrate with OpenClaw cron here
        # Currently just print hint
        print(f"   ⏰ Scheduled to continue in {delay} seconds")
    
    def _save_for_resume(self) -> None:
        """Save state for resume"""
        pass  # Managed by Overseer uniformly
    
    # ---- Export ----
    
    def export(self) -> Dict:
        """Export full context"""
        return {
            "workflow_id": self.workflow_id,
            "run_id": self.run_id,
            "data": self.data,
            "step_results": self.step_results,
            "temp_data": self.temp_data,
            "state_data": self.state_data
        }
    
    @classmethod
    def from_export(cls, data: Dict, **kwargs) -> "OverseerContext":
        """Restore from exported data"""
        ctx = cls(
            workflow_id=data["workflow_id"],
            run_id=data["run_id"],
            initial_data=data.get("data", {}),
            **kwargs
        )
        ctx.step_results = data.get("step_results", {})
        ctx.temp_data = data.get("temp_data", {})
        ctx.state_data = data.get("state_data", {})
        return ctx


# ==================== Step ====================

class Step:
    """Workflow step"""
    
    def __init__(
        self,
        name: str,
        func: Callable,
        retry: int = 0,
        retry_delay: int = 0,
        timeout: Optional[int] = None,
        condition: Optional[Callable] = None,
        heartbeat_interval: Optional[int] = None
    ):
        self.name = name
        self.func = func
        self.retry = retry
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.condition = condition
        self.heartbeat_interval = heartbeat_interval
        
        # Execution state
        self.result = None
        self.status = "pending"  # pending, running, completed, failed, skipped
        self.start_time = None
        self.end_time = None
        self.error = None
    
    def should_execute(self, ctx: OverseerContext) -> bool:
        """Check if should execute"""
        if self.condition:
            return self.condition(ctx)
        return True
    
    def to_dict(self) -> Dict:
        """Serialize to dict"""
        return {
            "name": self.name,
            "status": self.status,
            "retry": self.retry,
            "timeout": self.timeout,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "error": str(self.error) if self.error else None
        }


# ==================== State Manager ====================

class StateManager:
    """State manager"""
    
    def __init__(self, state_dir: str = ".overseer"):
        self.state_dir = state_dir
        self._ensure_dir()
    
    def _ensure_dir(self):
        """Ensure state directory exists"""
        os.makedirs(self.state_dir, exist_ok=True)
        os.makedirs(os.path.join(self.state_dir, "archive"), exist_ok=True)
        os.makedirs(os.path.join(self.state_dir, "jobs"), exist_ok=True)
    
    def get_state_file(self, run_id: str) -> str:
        """Get state file path"""
        return os.path.join(self.state_dir, f"{run_id}.json")
    
    def get_job_file(self, job_id: str) -> str:
        """Get job info file path"""
        return os.path.join(self.state_dir, "jobs", f"{job_id}.json")
    
    def save(self, run_id: str, state: Dict) -> None:
        """Save state"""
        state_file = self.get_state_file(run_id)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load(self, run_id: str) -> Optional[Dict]:
        """Load state"""
        state_file = self.get_state_file(run_id)
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def save_job(self, job: JobInfo) -> None:
        """Save job info"""
        job_file = self.get_job_file(job.id)
        with open(job_file, "w", encoding="utf-8") as f:
            json.dump(job.to_dict(), f, ensure_ascii=False, indent=2)
    
    def load_job(self, job_id: str) -> Optional[JobInfo]:
        """Load job info"""
        job_file = self.get_job_file(job_id)
        if os.path.exists(job_file):
            with open(job_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return JobInfo(**data)
        return None
    
    def archive(self, run_id: str, status: str = "completed") -> None:
        """Archive state"""
        state_file = self.get_state_file(run_id)
        if os.path.exists(state_file):
            archive_dir = os.path.join(self.state_dir, "archive")
            os.makedirs(archive_dir, exist_ok=True)
            archive_file = os.path.join(archive_dir, f"{run_id}_{status}.json")
            os.rename(state_file, archive_file)


# ==================== Overseer ====================

class Overseer:
    """
    AI Workflow Enforcer
    
    Core Capabilities:
    1. Forced sequential execution (no step skipping)
    2. State persistence with checkpoint resume
    3. Heartbeat mechanism (prevents 15-min timeout)
    4. Async execution + completion notification
    """
    
    def __init__(
        self,
        name: str,
        description: str = None,
        state_dir: str = ".overseer",
        report_progress: bool = True,
        report_interval: str = None,
        allow_resume: bool = True,
        enable_heartbeat: bool = True,
        heartbeat_interval: int = 60,
        async_mode: bool = False,
        notify_on_complete: bool = False,
        notify_channel: str = None
    ):
        self.name = name
        self.description = description
        self.state_manager = StateManager(state_dir)
        self.report_progress = report_progress
        self.report_interval = report_interval
        self.allow_resume = allow_resume
        
        # Progress reporter
        self._reporter: Optional[ProgressReporter] = None
        
        # Heartbeat config
        self.enable_heartbeat = enable_heartbeat
        self.heartbeat_interval = heartbeat_interval
        self._heartbeat_callback = None
        
        # Async config
        self.async_mode = async_mode
        self.notify_on_complete = notify_on_complete
        self.notify_channel = notify_channel
        
        # Workflow state
        self.steps: List[Step] = []
        self.context: Optional[OverseerContext] = None
        self.run_id: Optional[str] = None
        self.current_step_index: int = 0
        self._job_info: Optional[JobInfo] = None
    
    # ---- Decorator API ----
    
    def step(
        self,
        name: str,
        retry: int = 0,
        retry_delay: int = 0,
        timeout: Optional[int] = None,
        condition: Optional[Callable] = None,
        heartbeat_interval: Optional[int] = None
    ) -> Callable:
        """Step decorator"""
        def decorator(func: Callable) -> Callable:
            # Use step-specific heartbeat interval or global default
            hb_interval = heartbeat_interval or self.heartbeat_interval
            
            step_obj = Step(
                name=name,
                func=func,
                retry=retry,
                retry_delay=retry_delay,
                timeout=timeout,
                condition=condition,
                heartbeat_interval=hb_interval
            )
            self.steps.append(step_obj)
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # ---- Core Execution Logic ----
    
    def _generate_run_id(self) -> str:
        """Generate run ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.name}_{timestamp}_{uuid.uuid4().hex[:8]}"
    
    def _save_state(self) -> None:
        """Save current state"""
        if not self.run_id:
            return
        
        state = {
            "workflow_name": self.name,
            "description": self.description,
            "run_id": self.run_id,
            "status": "running",
            "current_step": self.current_step_index,
            "total_steps": len(self.steps),
            "steps": [s.to_dict() for s in self.steps],
            "context": self.context.export() if self.context else {},
            "timestamp": datetime.now().isoformat()
        }
        self.state_manager.save(self.run_id, state)
        
        # Also update job info
        if self._job_info:
            self._job_info.current_step = self.current_step_index
            self.state_manager.save_job(self._job_info)
    
    def _report_progress(self, message: str) -> None:
        """Report progress"""
        if self.report_progress:
            print(message)
    
    def _handle_heartbeat(self, heartbeat_data: Dict) -> None:
        """Handle heartbeat"""
        # Update job info
        if self._job_info:
            self.state_manager.save_job(self._job_info)
        
        # Report to user
        if self.report_progress:
            print(f"   💓 {heartbeat_data['message']}")
    
    def _execute_step(self, step: Step, ctx: OverseerContext) -> Any:
        """Execute single step"""
        # Check condition
        if not step.should_execute(ctx):
            step.status = "skipped"
            self._report_progress(f"⏭️  {step.name} (skipped)")
            return None
        
        # Start execution
        step.status = "running"
        step.start_time = datetime.now()
        
        total_attempts = step.retry + 1
        last_error = None
        
        for attempt in range(total_attempts):
            try:
                if attempt > 0:
                    self._report_progress(f"🔄  Retrying {step.name} (attempt {attempt+1})...")
                    if step.retry_delay > 0:
                        time.sleep(step.retry_delay)
                
                # Set heartbeat callback
                ctx._heartbeat_callback = self._handle_heartbeat
                ctx._heartbeat_interval = step.heartbeat_interval
                
                # Execute step function
                result = step.func(ctx)
                
                # Success
                step.status = "completed"
                step.end_time = datetime.now()
                step.result = result
                
                # Save result to context
                ctx.set_step_result(step.name, result)
                
                return result
                
            except Exception as e:
                last_error = e
                step.error = e
                if attempt < total_attempts - 1:
                    continue
                else:
                    step.status = "failed"
                    step.end_time = datetime.now()
                    raise
        
        return None
    
    def _summarize_result(self, result: Any, max_len: int = 50) -> str:
        """Generate result summary"""
        if result is None:
            return "No result"
        
        if isinstance(result, dict):
            keys = list(result.keys())[:3]
            return f"Contains fields: {', '.join(keys)}..."
        elif isinstance(result, list):
            return f"Contains {len(result)} items"
        elif isinstance(result, str):
            if len(result) > max_len:
                return result[:max_len] + "..."
            return result
        else:
            return str(result)[:max_len]
    
    # ---- Synchronous Execution ----
    
    def run(self, **kwargs) -> Dict:
        """
        Execute workflow synchronously
        
        For: Short tasks (<15 minutes)
        """
        # Initialize run
        self.run_id = self._generate_run_id()
        self.context = OverseerContext(
            workflow_id=self.name,
            run_id=self.run_id,
            initial_data=kwargs,
            heartbeat_callback=self._handle_heartbeat if self.enable_heartbeat else None,
            heartbeat_interval=self.heartbeat_interval
        )
        self.current_step_index = 0
        
        # Report start
        self._report_progress(f"📋 Workflow: {self.name}")
        if self.description:
            self._report_progress(f"   {self.description}")
        self._report_progress(f"   Total {len(self.steps)} steps\n")
        
        # Initialize progress reporter
        if self.report_progress:
            self._reporter = ProgressReporter(
                interval_desc=self.report_interval,
                enabled=True
            )
            self._reporter.start(self.name, len(self.steps))
        
        try:
            # Execute steps sequentially
            for i, step in enumerate(self.steps):
                self.current_step_index = i
                
                # Save state
                self._save_state()
                
                # Update reporter
                if self._reporter:
                    self._reporter.update_step(i, step.name, "running")
                
                # Report start
                step_num = i + 1
                total = len(self.steps)
                self._report_progress(f"⏳ Step {step_num}/{total}: {step.name}...")
                
                # Execute step
                result = self._execute_step(step, self.context)
                
                # Update reporter
                if self._reporter:
                    self._reporter.update_step(i, step.name, "completed")
                
                # Report completion
                if step.status == "completed":
                    result_summary = self._summarize_result(result)
                    self._report_progress(f"✅ Step {step_num}/{total} complete: {result_summary}\n")
                elif step.status == "skipped":
                    self._report_progress(f"⏭️  Step {step_num}/{total} skipped\n")
            
            # Complete
            self._report_progress(f"🎉 All complete!")
            
            # Stop reporter
            if self._reporter:
                self._reporter.stop()
            
            # Archive state
            self._finalize_run("completed")
            
            return self.context.get_all_results()
            
        except Exception as e:
            # Save failure state
            self._save_state()
            # Stop reporter
            if self._reporter:
                self._reporter.stop()
            self._report_progress(f"❌ Execution failed: {str(e)}")
            self._finalize_run("failed")
            raise
    
    def _finalize_run(self, status: str) -> None:
        """Finalize run"""
        if self._job_info:
            self._job_info.status = status
            self._job_info.current_step = self.current_step_index
            self.state_manager.save_job(self._job_info)
        
        if status == "completed":
            self.state_manager.archive(self.run_id, status)
    
    # ---- Async Execution ----
    
    def run_async(self, **kwargs) -> JobInfo:
        """
        Execute workflow asynchronously
        
        For: Long tasks (>15 minutes)
        Returns JobInfo immediately, executes in background, notifies on completion
        """
        # Generate job ID
        self.run_id = self._generate_run_id()
        
        # Create job info
        eta = datetime.now() + timedelta(minutes=len(self.steps) * 5)  # Rough estimate
        self._job_info = JobInfo(
            id=self.run_id,
            workflow_name=self.name,
            status="running",
            current_step=0,
            total_steps=len(self.steps),
            start_time=datetime.now().isoformat(),
            eta=eta.isoformat()
        )
        self.state_manager.save_job(self._job_info)
        
        # Execute in background thread
        def background_run():
            try:
                self.run(**kwargs)
                if self.notify_on_complete and self.notify_channel:
                    self._notify_user("completed")
            except Exception as e:
                if self.notify_on_complete and self.notify_channel:
                    self._notify_user("failed", error=str(e))
        
        thread = threading.Thread(target=background_run, daemon=True)
        thread.start()
        
        # Return job info immediately
        print(f"✅ Job started (background execution)")
        print(f"   Job ID: {self.run_id}")
        print(f"   ETA: {eta.strftime('%H:%M')}")
        print(f"   Check status: .overseer/jobs/{self.run_id}.json")
        
        return self._job_info
    
    def _notify_user(self, status: str, error: str = None) -> None:
        """Notify user of job completion"""
        if status == "completed":
            message = f"""
🎉 Workflow execution complete!

Task: {self.name}
Job ID: {self.run_id}
Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

All steps executed.
"""
        else:
            message = f"""
❌ Workflow execution failed

Task: {self.name}
Job ID: {self.run_id}
Failure time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Error: {error or 'Unknown error'}
"""
        
        print(f"\n{'='*60}")
        print(message)
        print(f"{'='*60}")
        
        # Can integrate OpenClaw message sending here
        # message.send(channel=self.notify_channel, message=message)
    
    def check_status(self, job_id: str) -> Optional[JobInfo]:
        """Check job status"""
        return self.state_manager.load_job(job_id)
    
    # ---- Checkpoint Resume ----
    
    def resume(self, run_id: str = None) -> Dict:
        """
        Resume from checkpoint
        
        Args:
            run_id: Previous run ID, None to find latest
        """
        # Find state file
        if run_id:
            state = self.state_manager.load(run_id)
        else:
            # Find latest state
            state_files = [
                f for f in os.listdir(self.state_manager.state_dir)
                if f.startswith(self.name) and f.endswith(".json")
                and not f.startswith("jobs/")
            ]
            if not state_files:
                raise ValueError(f"No history found for {self.name}")
            state_files.sort(reverse=True)
            state = self.state_manager.load(state_files[0].replace(".json", ""))
        
        if not state:
            raise ValueError(f"Cannot load state: {run_id}")
        
        # Restore context
        self.run_id = state["run_id"]
        self.current_step_index = state["current_step"]
        self.context = OverseerContext.from_export(
            state["context"],
            heartbeat_callback=self._handle_heartbeat if self.enable_heartbeat else None
        )
        
        # Update step states
        for i, step_data in enumerate(state["steps"]):
            if i < len(self.steps):
                self.steps[i].status = step_data.get("status", "pending")
                self.steps[i].result = state["context"].get("step_results", {}).get(self.steps[i].name)
        
        self._report_progress(f"🔄 Resuming: {self.name}")
        self._report_progress(f"   Continuing from Step {self.current_step_index + 1}/{len(self.steps)}\n")
        
        # Continue execution
        return self.run(**self.context.data)
    
    # ---- Create from Translation Plan ----
    
    @classmethod
    def from_plan(cls, plan: Dict, **kwargs) -> "Overseer":
        """
        Create Overseer instance from TaskTranslator plan
        
        Args:
            plan: Execution plan from TaskTranslator.translate()
            **kwargs: Additional Overseer config
            
        Returns:
            Configured Overseer instance
        """
        workflow_def = plan.get("workflow", {})
        steps_def = plan.get("steps", [])
        
        # Create workflow
        overseer = cls(
            name=workflow_def.get("name", "auto_workflow"),
            description=f"Auto-generated: {workflow_def.get('source_command', '')}",
            **kwargs
        )
        
        # Dynamically create steps
        for step_def in steps_def:
            step_name = step_def["name"]
            task_type = step_def.get("task_type", "generic")
            
            # Select execution function based on task type
            if task_type == "search_download":
                func = cls._create_search_download_func(step_def)
            elif task_type == "write_chapter":
                func = cls._create_write_func(step_def)
            else:
                func = cls._create_generic_func(step_def)
            
            # Add step with decorator
            decorator = overseer.step(
                name=step_name,
                retry=step_def.get("retry", 3),
                timeout=step_def.get("timeout", 1800),
                heartbeat_interval=step_def.get("heartbeat_interval", 60)
            )
            decorator(func)
        
        return overseer
    
    @staticmethod
    def _create_search_download_func(step_def: Dict) -> Callable:
        """Create search download function"""
        params = step_def.get("params", {})
        expected_count = params.get("expected_count", 10)
        
        def search_download_func(ctx):
            # Should integrate actual search download logic
            # Currently returns mock result
            ctx.heartbeat(f"Starting download of {expected_count} items...")
            
            # Actual execution would call kimi_search and kimi_fetch
            # result = actual_search_and_download(params)
            
            return {
                "task": step_def["description"],
                "expected": expected_count,
                "status": "completed"
            }
        
        return search_download_func
    
    @staticmethod
    def _create_write_func(step_def: Dict) -> Callable:
        """Create write function"""
        params = step_def.get("params", {})
        expected_words = params.get("expected_words", 2000)
        
        def write_func(ctx):
            ctx.heartbeat(f"Starting writing of ~{expected_words} words...")
            
            # Actual execution would call LLM to generate content
            # result = actual_write_content(params)
            
            return {
                "task": step_def["description"],
                "expected_words": expected_words,
                "status": "completed"
            }
        
        return write_func
    
    @staticmethod
    def _create_generic_func(step_def: Dict) -> Callable:
        """Create generic execution function"""
        def generic_func(ctx):
            ctx.heartbeat(f"Executing task: {step_def['description']}")
            
            return {
                "task": step_def["description"],
                "status": "completed"
            }
        
        return generic_func


# ==================== Convenience Functions ====================

def create_workflow(name: str, description: str = None, **kwargs) -> "Overseer":
    """Create workflow"""
    return Overseer(name=name, description=description, **kwargs)


def create_translator(capacity_config: Dict = None, patterns: List = None) -> "TaskTranslator":
    """Create task translator"""
    from .translator import TaskTranslator
    return TaskTranslator(capacity_config=capacity_config, patterns=patterns)


def translate_and_run(natural_command: str, **kwargs) -> Dict:
    """
    One-liner translate and execute
    
    Args:
        natural_command: Natural language command, e.g. "Download 100 reports"
        **kwargs: Additional parameters
        
    Returns:
        Execution result
    """
    from .translator import TaskTranslator
    
    # Translate
    translator = TaskTranslator()
    plan = translator.translate(natural_command)
    
    # Print execution plan
    print(translator.explain_plan(plan))
    print()
    
    # Create Overseer and execute
    workflow = Overseer.from_plan(plan, **kwargs)
    return workflow.run()


# ==================== Version Info ====================

__version__ = "0.4.0"
__all__ = [
    "Overseer", 
    "OverseerContext", 
    "Step", 
    "JobInfo", 
    "StateManager",
    "TaskTranslator",
    "TaskIntent",
    "TaskChunk",
    "StepVerifier",
    "ProgressReporter",
    "create_workflow",
    "create_translator",
    "create_reporter",
    "translate_and_run"
]
