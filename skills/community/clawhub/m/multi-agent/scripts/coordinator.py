#!/usr/bin/env python3
"""
Multi-Agent Coordinator for OpenClaw
Implements Claude Code-style Coordinator Mode

Phase 1: Research - Parallel workers explore and gather information
Phase 2: Synthesis - Coordinator reads findings and creates specs  
Phase 3: Implementation - Workers execute changes
Phase 4: Verification - Workers verify changes work
"""

import asyncio
import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import xml.etree.ElementTree as ET


@dataclass
class Worker:
    """Represents a spawned worker agent"""
    id: str
    role: str
    task: str
    status: str = "pending"  # pending, running, completed, failed, killed
    result: Optional[str] = None
    session_key: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "task": self.task,
            "status": self.status,
            "result": self.result,
            "session_key": self.session_key,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class XMLProtocol:
    """XML-based communication protocol between coordinator and workers"""
    
    @staticmethod
    def create_notification(
        task_id: str,
        status: str,
        summary: str,
        result: str = "",
        usage: Optional[Dict] = None
    ) -> str:
        """Create a task notification XML message"""
        usage_xml = ""
        if usage:
            usage_xml = f"""
  <usage>
    <total_tokens>{usage.get('total_tokens', 0)}</total_tokens>
    <tool_uses>{usage.get('tool_uses', 0)}</tool_uses>
    <duration_ms>{usage.get('duration_ms', 0)}</duration_ms>
  </usage>"""
        
        return f"""<task-notification>
  <task-id>{task_id}</task-id>
  <status>{status}</status>
  <summary>{summary}</summary>
  <result>{result}</result>{usage_xml}
</task-notification>"""
    
    @staticmethod
    def parse_notification(xml_text: str) -> Optional[Dict[str, Any]]:
        """Parse a task notification XML message"""
        try:
            root = ET.fromstring(xml_text)
            if root.tag != "task-notification":
                return None
            
            result = {
                "task_id": root.findtext("task-id", ""),
                "status": root.findtext("status", ""),
                "summary": root.findtext("summary", ""),
                "result": root.findtext("result", "")
            }
            
            # Parse usage if present
            usage_elem = root.find("usage")
            if usage_elem is not None:
                result["usage"] = {
                    "total_tokens": int(usage_elem.findtext("total_tokens", "0")),
                    "tool_uses": int(usage_elem.findtext("tool_uses", "0")),
                    "duration_ms": int(usage_elem.findtext("duration_ms", "0"))
                }
            
            return result
        except ET.ParseError:
            return None


class Scratchpad:
    """Shared filesystem for cross-worker knowledge exchange"""
    
    def __init__(self, base_dir: str = ".openclaw/scratchpad"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def write(self, filename: str, content: str) -> Path:
        """Write content to scratchpad"""
        filepath = self.base_dir / filename
        filepath.write_text(content, encoding="utf-8")
        return filepath
    
    def read(self, filename: str) -> Optional[str]:
        """Read content from scratchpad"""
        filepath = self.base_dir / filename
        if filepath.exists():
            return filepath.read_text(encoding="utf-8")
        return None
    
    def list_files(self) -> List[str]:
        """List all files in scratchpad"""
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]
    
    def get_path(self, filename: str) -> Path:
        """Get full path for a file"""
        return self.base_dir / filename


class Coordinator:
    """
    Pure orchestrator that manages workers but cannot directly execute commands.
    Implements the four-phase workflow from Claude Code Coordinator Mode.
    """
    
    COORDINATOR_TOOLS = ["spawn", "send", "stop", "summarize"]
    WORKER_TOOLS = [
        "read", "edit", "write", "bash", "grep", "glob",
        "web_search", "web_fetch", "todo_write"
    ]
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.workers: Dict[str, Worker] = {}
        self.scratchpad = Scratchpad()
        self.protocol = XMLProtocol()
        self.phase: str = "idle"  # idle, research, synthesis, implementation, verification
    
    def spawn_worker(
        self,
        task: str,
        role: str = "worker",
        context: Optional[str] = None
    ) -> Worker:
        """Spawn a new worker with specific role and task"""
        worker_id = f"{role}-{uuid.uuid4().hex[:8]}"
        
        worker = Worker(
            id=worker_id,
            role=role,
            task=task,
            status="running"
        )
        
        self.workers[worker_id] = worker
        
        # Write worker spec to scratchpad for reference
        spec = {
            "id": worker_id,
            "role": role,
            "task": task,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        self.scratchpad.write(f"worker-{worker_id}.json", json.dumps(spec, indent=2))
        
        print(f"[Coordinator] Spawned {role} worker: {worker_id}")
        print(f"[Coordinator] Task: {task[:100]}..." if len(task) > 100 else f"[Coordinator] Task: {task}")
        
        return worker
    
    def send_to_worker(self, worker_id: str, message: str) -> bool:
        """Send a message to a running worker"""
        worker = self.workers.get(worker_id)
        if not worker:
            print(f"[Coordinator] Worker {worker_id} not found")
            return False
        
        if worker.status != "running":
            print(f"[Coordinator] Worker {worker_id} is not running (status: {worker.status})")
            return False
        
        # In real implementation, this would use sessions_send
        print(f"[Coordinator] → {worker_id}: {message[:100]}..." if len(message) > 100 else f"[Coordinator] → {worker_id}: {message}")
        return True
    
    def stop_worker(self, worker_id: str) -> bool:
        """Stop a running worker"""
        worker = self.workers.get(worker_id)
        if not worker:
            print(f"[Coordinator] Worker {worker_id} not found")
            return False
        
        worker.status = "killed"
        worker.completed_at = datetime.now()
        print(f"[Coordinator] Stopped worker: {worker_id}")
        return True
    
    def receive_notification(self, xml_text: str) -> Optional[Worker]:
        """Receive and process a task notification from a worker"""
        notification = self.protocol.parse_notification(xml_text)
        if not notification:
            return None
        
        worker_id = notification.get("task_id")
        worker = self.workers.get(worker_id)
        
        if not worker:
            print(f"[Coordinator] Notification from unknown worker: {worker_id}")
            return None
        
        worker.status = notification.get("status", "unknown")
        worker.result = notification.get("result", "")
        worker.completed_at = datetime.now()
        
        # Save notification to scratchpad
        self.scratchpad.write(
            f"notification-{worker_id}.xml",
            xml_text
        )
        
        print(f"[Coordinator] ← {worker_id}: {notification.get('status')} - {notification.get('summary', '')}")
        
        return worker
    
    def list_workers(self, status: Optional[str] = None) -> List[Worker]:
        """List all workers, optionally filtered by status"""
        workers = list(self.workers.values())
        if status:
            workers = [w for w in workers if w.status == status]
        return workers
    
    def get_scratchpad_summary(self) -> str:
        """Get summary of scratchpad contents"""
        files = self.scratchpad.list_files()
        return f"Scratchpad: {len(files)} files\n" + "\n".join(f"  - {f}" for f in files[:10])
    
    # === Four-Phase Workflow ===
    
    async def phase_research(
        self,
        task: str,
        num_workers: int = 3,
        research_prompts: Optional[List[str]] = None
    ) -> List[Worker]:
        """
        Phase 1: Research
        Spawn parallel workers to explore different aspects
        """
        self.phase = "research"
        print(f"\n{'='*60}")
        print(f"PHASE 1: RESEARCH")
        print(f"{'='*60}")
        print(f"Main task: {task}")
        print(f"Spawning {num_workers} research workers...\n")
        
        if not research_prompts:
            # Default research angles
            research_prompts = [
                f"Explore codebase structure related to: {task}. Find key files and their relationships.",
                f"Analyze current implementation for: {task}. Identify patterns and potential issues.",
                f"Research dependencies and requirements for: {task}. What needs to change?"
            ]
        
        workers = []
        for i, prompt in enumerate(research_prompts[:num_workers]):
            worker = self.spawn_worker(
                task=prompt,
                role="researcher",
                context=f"Research angle {i+1}/{num_workers}"
            )
            workers.append(worker)
        
        # In real implementation, would wait for all workers to complete
        print(f"\n[Phase 1] Spawned {len(workers)} research workers")
        print("Waiting for research findings... (simulated)\n")
        
        return workers
    
    async def phase_synthesis(self, workers: List[Worker]) -> str:
        """
        Phase 2: Synthesis
        Read all findings and create implementation specs
        """
        self.phase = "synthesis"
        print(f"\n{'='*60}")
        print(f"PHASE 2: SYNTHESIS")
        print(f"{'='*60}")
        
        # Collect findings from workers
        findings = []
        for worker in workers:
            if worker.result:
                findings.append(f"[{worker.id}] {worker.result}")
        
        print(f"Synthesizing findings from {len(findings)} workers...")
        print("\nKey findings:")
        for finding in findings[:5]:
            print(f"  - {finding[:100]}...")
        
        # Create implementation spec
        spec = f"""
Implementation Specification (Synthesized)
=========================================
Based on research from {len(workers)} workers:

{chr(10).join(findings[:3])}

Next Steps:
1. Refactor core module
2. Update dependencies
3. Add tests
"""
        
        self.scratchpad.write("implementation-spec.md", spec)
        print(f"\n[Phase 2] Created implementation specification")
        
        return spec
    
    async def phase_implementation(self, spec: str, num_workers: int = 2) -> List[Worker]:
        """
        Phase 3: Implementation
        Spawn workers to execute changes based on specs
        """
        self.phase = "implementation"
        print(f"\n{'='*60}")
        print(f"PHASE 3: IMPLEMENTATION")
        print(f"{'='*60}")
        print(f"Spawning {num_workers} implementation workers...\n")
        
        impl_prompts = [
            "Implement core changes based on specification",
            "Update related files and dependencies"
        ]
        
        workers = []
        for i, prompt in enumerate(impl_prompts[:num_workers]):
            worker = self.spawn_worker(
                task=f"{prompt}\n\nSpecification:\n{spec[:500]}",
                role="implementer",
                context=f"Implementation worker {i+1}/{num_workers}"
            )
            workers.append(worker)
        
        return workers
    
    async def phase_verification(self, workers: List[Worker]) -> List[Worker]:
        """
        Phase 4: Verification
        Spawn workers to verify changes
        """
        self.phase = "verification"
        print(f"\n{'='*60}")
        print(f"PHASE 4: VERIFICATION")
        print(f"{'='*60}")
        print(f"Spawning verification workers...\n")
        
        verif_prompts = [
            "Run tests and verify implementation works correctly",
            "Check for regressions and edge cases"
        ]
        
        verif_workers = []
        for prompt in verif_prompts:
            worker = self.spawn_worker(
                task=prompt,
                role="verifier"
            )
            verif_workers.append(worker)
        
        return verif_workers
    
    async def run_full_workflow(self, task: str) -> Dict[str, Any]:
        """
        Run the complete four-phase workflow
        """
        print(f"\n{'='*60}")
        print(f"COORDINATOR MODE: Full Workflow")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        # Phase 1: Research
        research_workers = await self.phase_research(task, num_workers=3)
        
        # Simulate workers completing with findings
        for worker in research_workers:
            notification = self.protocol.create_notification(
                task_id=worker.id,
                status="completed",
                summary=f"Completed research on {worker.task[:50]}...",
                result=f"Found key files: src/{worker.role}/example.ts, src/{worker.role}/utils.ts"
            )
            self.receive_notification(notification)
        
        # Phase 2: Synthesis
        spec = await self.phase_synthesis(research_workers)
        
        # Phase 3: Implementation
        impl_workers = await self.phase_implementation(spec, num_workers=2)
        
        # Simulate implementation completion
        for worker in impl_workers:
            notification = self.protocol.create_notification(
                task_id=worker.id,
                status="completed",
                summary=f"Implemented changes for {worker.task[:50]}...",
                result="Modified 3 files, added 150 lines"
            )
            self.receive_notification(notification)
        
        # Phase 4: Verification
        verif_workers = await self.phase_verification(impl_workers)
        
        # Simulate verification completion
        for worker in verif_workers:
            notification = self.protocol.create_notification(
                task_id=worker.id,
                status="completed",
                summary=f"Verified implementation",
                result="All tests passed, no regressions found"
            )
            self.receive_notification(notification)
        
        # Final summary
        self.phase = "completed"
        print(f"\n{'='*60}")
        print(f"WORKFLOW COMPLETED")
        print(f"{'='*60}")
        
        summary = {
            "task": task,
            "phases_completed": ["research", "synthesis", "implementation", "verification"],
            "workers_spawned": len(self.workers),
            "workers_completed": len([w for w in self.workers.values() if w.status == "completed"]),
            "scratchpad_files": len(self.scratchpad.list_files())
        }
        
        print(f"\nSummary:")
        print(f"  Workers spawned: {summary['workers_spawned']}")
        print(f"  Workers completed: {summary['workers_completed']}")
        print(f"  Scratchpad files: {summary['scratchpad_files']}")
        
        return summary


# CLI Interface
def main():
    import sys
    
    coordinator = Coordinator()
    
    if len(sys.argv) < 2:
        print("Usage: coordinator.py <command> [args...]")
        print("\nCommands:")
        print("  workflow <task>          Run full four-phase workflow")
        print("  spawn <task> [--role]    Spawn a worker")
        print("  list                     List all workers")
        print("  send <id> <message>      Send message to worker")
        print("  stop <id>                Stop a worker")
        print("  scratchpad               Show scratchpad contents")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "workflow":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Example refactoring task"
        asyncio.run(coordinator.run_full_workflow(task))
    
    elif command == "spawn":
        if len(sys.argv) < 3:
            print("Usage: spawn <task> [--role <role>]")
            sys.exit(1)
        task = sys.argv[2]
        role = "worker"
        if "--role" in sys.argv:
            role_idx = sys.argv.index("--role")
            if role_idx + 1 < len(sys.argv):
                role = sys.argv[role_idx + 1]
        coordinator.spawn_worker(task, role=role)
    
    elif command == "list":
        workers = coordinator.list_workers()
        print(f"Active workers: {len(workers)}")
        for w in workers:
            print(f"  {w.id} [{w.status}] - {w.task[:50]}...")
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("Usage: send <id> <message>")
            sys.exit(1)
        coordinator.send_to_worker(sys.argv[2], " ".join(sys.argv[3:]))
    
    elif command == "stop":
        if len(sys.argv) < 3:
            print("Usage: stop <id>")
            sys.exit(1)
        coordinator.stop_worker(sys.argv[2])
    
    elif command == "scratchpad":
        print(coordinator.get_scratchpad_summary())
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
