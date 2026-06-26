#!/usr/bin/env python3
"""
Phase 2: Real Multi-Agent Coordinator for OpenClaw
Integrates with sessions_spawn, sessions_send, sessions_list, sessions_history
"""

import asyncio
import json
import os
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


@dataclass
class Worker:
    """Represents a spawned worker agent"""
    id: str
    role: str
    task: str
    status: str = "pending"  # pending, running, completed, failed, killed
    result: Optional[str] = None
    session_key: Optional[str] = None
    label: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    spawn_output: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "task": self.task,
            "status": self.status,
            "result": self.result,
            "session_key": self.session_key,
            "label": self.label,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class OpenClawAPI:
    """
    Interface to OpenClaw's real multi-session capabilities.
    Uses sessions_spawn, sessions_send, sessions_list, sessions_history
    """
    
    def __init__(self):
        self.workspace = Path(".openclaw/multi-agent")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def spawn_worker(
        self,
        worker_id: str,
        role: str,
        task: str,
        timeout_seconds: int = 300
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Spawn a real worker using sessions_spawn.
        Returns: (success, output, session_key)
        """
        label = f"multi-agent-worker-{worker_id}"
        
        # Create a task file for the worker
        task_file = self.workspace / f"task-{worker_id}.json"
        task_spec = {
            "worker_id": worker_id,
            "role": role,
            "task": task,
            "created_at": datetime.now().isoformat()
        }
        task_file.write_text(json.dumps(task_spec, indent=2))
        
        # Build the task message for the sub-agent
        worker_prompt = f"""You are a worker agent in OpenClaw's multi-agent system.

Role: {role}
Worker ID: {worker_id}

Your Task:
{task}

Instructions:
1. Complete the task to the best of your ability
2. Use available tools (read, edit, bash, web_search, etc.)
3. When finished, report results in this exact XML format:

<task-notification>
  <task-id>{worker_id}</task-id>
  <status>completed</status>
  <summary>Brief summary of what you did</summary>
  <result>Detailed results and findings</result>
</task-notification>

Start working now."""
        
        # Call sessions_spawn via openclaw CLI
        cmd = [
            "openclaw", "sessions", "spawn",
            "--label", label,
            "--task", worker_prompt,
            "--cleanup", "keep",
            "--timeout", str(timeout_seconds)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # CLI timeout, not worker timeout
            )
            
            output = result.stdout + result.stderr
            
            # Try to extract session key from output
            session_key = None
            for line in output.split('\n'):
                if 'session_key' in line.lower() or 'session key' in line.lower():
                    # Extract session key from various possible formats
                    parts = line.split(':')
                    if len(parts) >= 2:
                        session_key = parts[-1].strip()
                    break
                # Alternative: look for key in JSON-like output
                if '"session_key"' in line or "'session_key'" in line:
                    try:
                        json_part = line[line.find('{'):line.rfind('}')+1]
                        data = json.loads(json_part)
                        session_key = data.get('session_key')
                    except:
                        pass
            
            # If we can't extract session key, use label to identify
            if not session_key:
                session_key = label
            
            success = result.returncode == 0
            return success, output, session_key if success else None
            
        except subprocess.TimeoutExpired:
            return False, "Timeout spawning worker", None
        except Exception as e:
            return False, f"Error spawning worker: {e}", None
    
    def send_to_worker(self, session_key: str, message: str) -> bool:
        """Send a message to a running worker via sessions_send"""
        cmd = [
            "openclaw", "sessions", "send",
            "--session-key", session_key,
            "--message", message
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception as e:
            print(f"[OpenClawAPI] Error sending message: {e}")
            return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions via sessions_list"""
        cmd = ["openclaw", "sessions", "list", "--json"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return []
        except Exception as e:
            print(f"[OpenClawAPI] Error listing sessions: {e}")
            return []
    
    def get_session_history(self, session_key: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get session history via sessions_history"""
        cmd = [
            "openclaw", "sessions", "history",
            "--session-key", session_key,
            "--limit", str(limit)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Parse the history output
                lines = result.stdout.strip().split('\n')
                messages = []
                for line in lines:
                    if line.strip():
                        # Try to parse as JSON, otherwise treat as raw text
                        try:
                            msg = json.loads(line)
                            messages.append(msg)
                        except:
                            messages.append({"raw": line})
                return messages
            return []
        except Exception as e:
            print(f"[OpenClawAPI] Error getting history: {e}")
            return []
    
    def check_worker_status(self, session_key: str) -> Dict[str, Any]:
        """Check if worker is still running"""
        sessions = self.list_sessions()
        for session in sessions:
            if session.get('session_key') == session_key or session.get('label') == session_key:
                return {
                    "found": True,
                    "active": session.get('active', False),
                    "last_activity": session.get('last_activity'),
                    "status": session.get('status', 'unknown')
                }
        return {"found": False}


class Scratchpad:
    """Shared filesystem for cross-worker knowledge exchange"""
    
    def __init__(self, base_dir: str = ".openclaw/scratchpad"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def write(self, filename: str, content: str) -> Path:
        filepath = self.base_dir / filename
        filepath.write_text(content, encoding="utf-8")
        return filepath
    
    def read(self, filename: str) -> Optional[str]:
        filepath = self.base_dir / filename
        if filepath.exists():
            return filepath.read_text(encoding="utf-8")
        return None
    
    def list_files(self) -> List[str]:
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]


class XMLProtocol:
    """XML-based communication protocol"""
    
    @staticmethod
    def create_notification(
        task_id: str,
        status: str,
        summary: str,
        result: str = "",
        usage: Optional[Dict] = None
    ) -> str:
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
        """Parse XML notification, handling partial/incomplete XML"""
        import xml.etree.ElementTree as ET
        
        try:
            # Look for task-notification tag
            start = xml_text.find('<task-notification>')
            end = xml_text.find('</task-notification>')
            
            if start == -1:
                # Try self-closing or single-line format
                start = xml_text.find('<task-notification')
                if start == -1:
                    return None
            
            if end != -1:
                end += len('</task-notification>')
                xml_text = xml_text[start:end]
            else:
                # Incomplete XML, try to parse what we have
                xml_text = xml_text[start:] + '</task-notification>'
            
            root = ET.fromstring(xml_text)
            if root.tag != 'task-notification':
                return None
            
            result = {
                "task_id": root.findtext("task-id", ""),
                "status": root.findtext("status", ""),
                "summary": root.findtext("summary", ""),
                "result": root.findtext("result", "")
            }
            
            usage_elem = root.find("usage")
            if usage_elem is not None:
                result["usage"] = {
                    "total_tokens": int(usage_elem.findtext("total_tokens", "0")),
                    "tool_uses": int(usage_elem.findtext("tool_uses", "0")),
                    "duration_ms": int(usage_elem.findtext("duration_ms", "0"))
                }
            
            return result
        except Exception as e:
            # Return partial data if we can extract it
            result = {"task_id": "", "status": "unknown", "summary": "", "result": xml_text}
            if '<task-id>' in xml_text:
                try:
                    start = xml_text.find('<task-id>') + 9
                    end = xml_text.find('</task-id>')
                    if end > start:
                        result["task_id"] = xml_text[start:end]
                except:
                    pass
            return result


class Phase2Coordinator:
    """
    Phase 2 Coordinator using real OpenClaw sessions.
    """
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.workers: Dict[str, Worker] = {}
        self.scratchpad = Scratchpad()
        self.protocol = XMLProtocol()
        self.openclaw = OpenClawAPI()
        self.phase: str = "idle"
    
    def spawn_worker(
        self,
        task: str,
        role: str = "worker",
        context: Optional[str] = None,
        timeout: int = 300
    ) -> Optional[Worker]:
        """Spawn a real worker using OpenClaw sessions_spawn"""
        worker_id = f"{role}-{uuid.uuid4().hex[:8]}"
        
        print(f"[Coordinator] Spawning {role} worker: {worker_id}")
        print(f"[Coordinator] Task: {task[:80]}..." if len(task) > 80 else f"[Coordinator] Task: {task}")
        
        # Spawn via OpenClaw API
        success, output, session_key = self.openclaw.spawn_worker(
            worker_id=worker_id,
            role=role,
            task=task,
            timeout_seconds=timeout
        )
        
        if not success:
            print(f"[Coordinator] Failed to spawn worker: {output}")
            return None
        
        worker = Worker(
            id=worker_id,
            role=role,
            task=task,
            status="running",
            session_key=session_key,
            label=f"multi-agent-worker-{worker_id}",
            spawn_output=output
        )
        
        self.workers[worker_id] = worker
        
        # Save worker spec to scratchpad
        spec = {
            "id": worker_id,
            "role": role,
            "task": task,
            "session_key": session_key,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        self.scratchpad.write(f"worker-{worker_id}.json", json.dumps(spec, indent=2))
        
        print(f"[Coordinator] ✓ Worker spawned with session: {session_key}")
        
        return worker
    
    def check_worker_result(self, worker: Worker) -> bool:
        """Check if worker has completed and extract result"""
        if not worker.session_key:
            return False
        
        # Get session history
        history = self.openclaw.get_session_history(worker.session_key, limit=20)
        
        # Look for task-notification in the history
        for msg in history:
            content = msg.get('content', '') if isinstance(msg, dict) else str(msg)
            if '<task-notification>' in content:
                notification = self.protocol.parse_notification(content)
                if notification:
                    worker.status = notification.get('status', 'completed')
                    worker.result = notification.get('result', '')
                    worker.completed_at = datetime.now()
                    
                    # Save notification
                    self.scratchpad.write(
                        f"notification-{worker.id}.xml",
                        content
                    )
                    
                    print(f"[Coordinator] ✓ Worker {worker.id} completed: {notification.get('summary', '')}")
                    return True
        
        # Check if session is still active
        status = self.openclaw.check_worker_status(worker.session_key)
        if not status.get('found', True):
            worker.status = "failed"
            worker.completed_at = datetime.now()
            print(f"[Coordinator] ✗ Worker {worker.id} session not found")
            return True
        
        return False
    
    def wait_for_workers(
        self,
        workers: List[Worker],
        timeout: int = 300,
        poll_interval: int = 5
    ) -> List[Worker]:
        """Wait for all workers to complete"""
        print(f"\n[Coordinator] Waiting for {len(workers)} workers...")
        print(f"[Coordinator] Timeout: {timeout}s, Poll interval: {poll_interval}s\n")
        
        start_time = time.time()
        completed = set()
        
        while len(completed) < len(workers):
            if time.time() - start_time > timeout:
                print(f"[Coordinator] Timeout! {len(workers) - len(completed)} workers still running")
                break
            
            for worker in workers:
                if worker.id in completed:
                    continue
                
                if self.check_worker_result(worker):
                    completed.add(worker.id)
                else:
                    print(f"[Coordinator] Worker {worker.id} still running...")
            
            if len(completed) < len(workers):
                time.sleep(poll_interval)
        
        print(f"\n[Coordinator] {len(completed)}/{len(workers)} workers completed")
        return workers
    
    def list_workers(self, status: Optional[str] = None) -> List[Worker]:
        """List all workers, optionally filtered by status"""
        workers = list(self.workers.values())
        if status:
            workers = [w for w in workers if w.status == status]
        return workers
    
    # === Four-Phase Workflow ===
    
    async def phase_research(
        self,
        task: str,
        num_workers: int = 3,
        research_prompts: Optional[List[str]] = None
    ) -> List[Worker]:
        """Phase 1: Research - Spawn parallel workers"""
        self.phase = "research"
        print(f"\n{'='*60}")
        print(f"PHASE 1: RESEARCH (Real Workers)")
        print(f"{'='*60}")
        print(f"Main task: {task}\n")
        
        if not research_prompts:
            research_prompts = [
                f"Explore codebase structure related to: {task}. Find key files and their relationships. List all relevant files and their purposes.",
                f"Analyze current implementation for: {task}. Identify patterns, potential issues, and areas for improvement.",
                f"Research dependencies and requirements for: {task}. What external libraries or internal modules need to be modified?"
            ]
        
        workers = []
        for i, prompt in enumerate(research_prompts[:num_workers]):
            worker = self.spawn_worker(
                task=prompt,
                role="researcher",
                context=f"Research angle {i+1}/{num_workers}",
                timeout=180
            )
            if worker:
                workers.append(worker)
        
        if not workers:
            print("[Phase 1] ERROR: Failed to spawn any workers!")
            return []
        
        print(f"\n[Phase 1] Spawned {len(workers)} research workers")
        
        # Wait for completion
        return self.wait_for_workers(workers, timeout=300)
    
    async def phase_synthesis(self, workers: List[Worker]) -> str:
        """Phase 2: Synthesis - Combine findings"""
        self.phase = "synthesis"
        print(f"\n{'='*60}")
        print(f"PHASE 2: SYNTHESIS")
        print(f"{'='*60}")
        
        findings = []
        for worker in workers:
            if worker.result:
                findings.append(f"[{worker.role} - {worker.id}]\n{worker.result}")
        
        print(f"Synthesizing findings from {len(findings)} workers...")
        
        # Create implementation spec
        spec_lines = [
            "# Implementation Specification",
            "",
            f"Generated at: {datetime.now().isoformat()}",
            f"Based on research from {len(workers)} workers",
            "",
            "## Research Findings",
            ""
        ]
        
        for i, finding in enumerate(findings, 1):
            spec_lines.append(f"### Finding {i}")
            spec_lines.append(finding)
            spec_lines.append("")
        
        spec_lines.extend([
            "## Recommended Implementation Steps",
            "",
            "1. Refactor core module",
            "2. Update dependencies",
            "3. Add comprehensive tests",
            "4. Verify no regressions",
            ""
        ])
        
        spec = "\n".join(spec_lines)
        self.scratchpad.write("implementation-spec.md", spec)
        
        print(f"[Phase 2] ✓ Created implementation specification")
        print(f"[Phase 2] Saved to: .openclaw/scratchpad/implementation-spec.md")
        
        return spec
    
    async def phase_implementation(self, spec: str, num_workers: int = 2) -> List[Worker]:
        """Phase 3: Implementation"""
        self.phase = "implementation"
        print(f"\n{'='*60}")
        print(f"PHASE 3: IMPLEMENTATION")
        print(f"{'='*60}")
        
        impl_tasks = [
            "Implement the core changes based on the specification. Focus on the main functionality.",
            "Update related files, dependencies, and add any necessary helper functions."
        ]
        
        workers = []
        for i, task_desc in enumerate(impl_tasks[:num_workers]):
            full_task = f"{task_desc}\n\nSpecification:\n{spec[:800]}..."
            worker = self.spawn_worker(
                task=full_task,
                role="implementer",
                context=f"Implementation worker {i+1}/{num_workers}",
                timeout=300
            )
            if worker:
                workers.append(worker)
        
        if workers:
            print(f"\n[Phase 3] Spawned {len(workers)} implementation workers")
            return self.wait_for_workers(workers, timeout=600)
        
        return []
    
    async def phase_verification(self, workers: List[Worker]) -> List[Worker]:
        """Phase 4: Verification"""
        self.phase = "verification"
        print(f"\n{'='*60}")
        print(f"PHASE 4: VERIFICATION")
        print(f"{'='*60}")
        
        verif_tasks = [
            "Run tests and verify the implementation works correctly. Report any failures.",
            "Check for regressions, edge cases, and code quality issues."
        ]
        
        verif_workers = []
        for task_desc in verif_tasks:
            worker = self.spawn_worker(
                task=task_desc,
                role="verifier",
                timeout=180
            )
            if worker:
                verif_workers.append(worker)
        
        if verif_workers:
            print(f"\n[Phase 4] Spawned {len(verif_workers)} verification workers")
            return self.wait_for_workers(verif_workers, timeout=400)
        
        return []
    
    async def run_full_workflow(self, task: str) -> Dict[str, Any]:
        """Run complete four-phase workflow with real workers"""
        print(f"\n{'='*60}")
        print(f"COORDINATOR MODE: Real Multi-Agent Workflow")
        print(f"{'='*60}")
        print(f"Task: {task}\n")
        
        # Phase 1: Research
        research_workers = await self.phase_research(task, num_workers=3)
        if not research_workers:
            return {"error": "Failed to complete research phase"}
        
        # Phase 2: Synthesis
        spec = await self.phase_synthesis(research_workers)
        
        # Phase 3: Implementation
        impl_workers = await self.phase_implementation(spec, num_workers=2)
        
        # Phase 4: Verification
        verif_workers = []
        if impl_workers:
            verif_workers = await self.phase_verification(impl_workers)
        
        # Final summary
        self.phase = "completed"
        print(f"\n{'='*60}")
        print(f"WORKFLOW COMPLETED")
        print(f"{'='*60}")
        
        summary = {
            "task": task,
            "phases_completed": ["research", "synthesis", "implementation", "verification"],
            "workers_spawned": len(self.workers),
            "workers_completed": len([w for w in self.workers.values() if w.status in ("completed", "failed")]),
            "research_workers": len(research_workers),
            "implementation_workers": len(impl_workers),
            "verification_workers": len(verif_workers),
            "scratchpad_files": len(self.scratchpad.list_files())
        }
        
        print(f"\nSummary:")
        print(f"  Total workers spawned: {summary['workers_spawned']}")
        print(f"  Workers completed: {summary['workers_completed']}")
        print(f"  Research workers: {summary['research_workers']}")
        print(f"  Implementation workers: {summary['implementation_workers']}")
        print(f"  Verification workers: {summary['verification_workers']}")
        print(f"  Scratchpad files: {summary['scratchpad_files']}")
        
        return summary


def main():
    import sys
    
    coordinator = Phase2Coordinator()
    
    if len(sys.argv) < 2:
        print("Usage: coordinator_phase2.py <command> [args...]")
        print("\nCommands:")
        print("  workflow <task>          Run full four-phase workflow")
        print("  spawn <task> [--role]    Spawn a single worker")
        print("  list                     List all workers")
        print("  check <worker-id>        Check worker status")
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
        worker = coordinator.spawn_worker(task, role=role)
        if worker:
            print(f"\nSpawned worker: {worker.id}")
            print(f"Session key: {worker.session_key}")
    
    elif command == "list":
        workers = coordinator.list_workers()
        print(f"Workers: {len(workers)}")
        for w in workers:
            print(f"  {w.id} [{w.status}] role={w.role}")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: check <worker-id>")
            sys.exit(1)
        worker_id = sys.argv[2]
        worker = coordinator.workers.get(worker_id)
        if worker:
            coordinator.check_worker_result(worker)
            print(f"Worker {worker_id}: {worker.status}")
            if worker.result:
                print(f"Result: {worker.result[:200]}...")
        else:
            print(f"Worker {worker_id} not found")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
