#!/usr/bin/env python3
"""
Worker agent implementation for OpenClaw Multi-Agent system.

Workers are execution agents with full tool access:
- File operations (read, edit, write)
- Shell commands (bash)
- Code search (grep, glob)
- Web access (web_search, web_fetch)
- Task management (todo_write)

Workers communicate with Coordinator via XML task notifications.
"""

import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable


@dataclass
class WorkerContext:
    """Context passed to a worker when spawned"""
    worker_id: str
    role: str
    task: str
    parent_session: Optional[str] = None
    scratchpad_dir: str = ".openclaw/scratchpad"
    allowed_tools: List[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    
    def get_scratchpad_path(self, filename: str) -> Path:
        """Get path to a scratchpad file"""
        return Path(self.scratchpad_dir) / filename
    
    def read_scratchpad(self, filename: str) -> Optional[str]:
        """Read from scratchpad"""
        path = self.get_scratchpad_path(filename)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None
    
    def write_scratchpad(self, filename: str, content: str) -> Path:
        """Write to scratchpad"""
        path = self.get_scratchpad_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


class WorkerTools:
    """
    Tool set available to workers.
    These are the tools workers can use to complete their tasks.
    """
    
    def __init__(self, context: WorkerContext):
        self.context = context
        self.tool_uses = 0
        self.results: List[Dict] = []
    
    def read(self, path: str, limit: int = 100) -> str:
        """Read a file"""
        self.tool_uses += 1
        try:
            file_path = Path(path)
            if not file_path.exists():
                return f"Error: File not found: {path}"
            
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            if len(lines) > limit:
                content = "\n".join(lines[:limit]) + f"\n... ({len(lines) - limit} more lines)"
            
            self.results.append({"tool": "read", "path": path, "status": "success"})
            return content
        except Exception as e:
            return f"Error reading {path}: {e}"
    
    def write(self, path: str, content: str) -> str:
        """Write a file"""
        self.tool_uses += 1
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            self.results.append({"tool": "write", "path": path, "status": "success"})
            return f"Written: {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"
    
    def edit(self, path: str, old: str, new: str) -> str:
        """Edit a file (find and replace)"""
        self.tool_uses += 1
        try:
            file_path = Path(path)
            if not file_path.exists():
                return f"Error: File not found: {path}"
            
            content = file_path.read_text(encoding="utf-8")
            if old not in content:
                return f"Error: Pattern not found in {path}"
            
            content = content.replace(old, new, 1)
            file_path.write_text(content, encoding="utf-8")
            self.results.append({"tool": "edit", "path": path, "status": "success"})
            return f"Edited: {path}"
        except Exception as e:
            return f"Error editing {path}: {e}"
    
    def bash(self, command: str, timeout: int = 60) -> str:
        """Execute a bash command"""
        self.tool_uses += 1
        import subprocess
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]: {result.stderr}"
            
            self.results.append({
                "tool": "bash",
                "command": command,
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode
            })
            return output[:2000]  # Limit output length
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout}s"
        except Exception as e:
            return f"Error executing command: {e}"
    
    def grep(self, pattern: str, path: str = ".", glob: str = "*") -> str:
        """Search for pattern in files"""
        self.tool_uses += 1
        import subprocess
        try:
            result = subprocess.run(
                ["grep", "-r", "-n", "--include", glob, pattern, path],
                capture_output=True,
                text=True
            )
            output = result.stdout if result.stdout else "No matches found"
            self.results.append({"tool": "grep", "pattern": pattern, "status": "success"})
            return output[:2000]
        except Exception as e:
            return f"Error searching: {e}"
    
    def glob(self, pattern: str, path: str = ".") -> List[str]:
        """Find files matching pattern"""
        self.tool_uses += 1
        from fnmatch import fnmatch
        
        matches = []
        base_path = Path(path)
        if base_path.exists():
            for f in base_path.rglob("*"):
                if f.is_file() and fnmatch(f.name, pattern):
                    matches.append(str(f.relative_to(base_path)))
        
        self.results.append({"tool": "glob", "pattern": pattern, "matches": len(matches)})
        return matches[:50]  # Limit results
    
    def web_search(self, query: str) -> str:
        """Search the web"""
        self.tool_uses += 1
        # Placeholder - would integrate with actual web search
        self.results.append({"tool": "web_search", "query": query})
        return f"[Web search placeholder] Results for: {query}"
    
    def web_fetch(self, url: str) -> str:
        """Fetch a web page"""
        self.tool_uses += 1
        # Placeholder - would integrate with actual web fetch
        self.results.append({"tool": "web_fetch", "url": url})
        return f"[Web fetch placeholder] Content from: {url}"
    
    def todo_write(self, todos: List[Dict[str, Any]]) -> str:
        """Write TODO list"""
        self.tool_uses += 1
        todo_file = self.context.get_scratchpad_path(f"todos-{self.context.worker_id}.json")
        todo_file.write_text(json.dumps(todos, indent=2), encoding="utf-8")
        self.results.append({"tool": "todo_write", "count": len(todos)})
        return f"TODO list saved: {len(todos)} items"


class WorkerAgent:
    """
    A worker agent that executes tasks using available tools.
    
    Workers are spawned by the Coordinator and report back via XML notifications.
    """
    
    def __init__(self, context: WorkerContext):
        self.context = context
        self.tools = WorkerTools(context)
        self.start_time = time.time()
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the worker's task.
        Returns a result dictionary that can be formatted as XML notification.
        """
        print(f"[Worker {self.context.worker_id}] Starting task: {self.context.task[:60]}...")
        
        # Simulate task execution based on role
        if self.context.role == "researcher":
            result = self._run_researcher()
        elif self.context.role == "implementer":
            result = self._run_implementer()
        elif self.context.role == "verifier":
            result = self._run_verifier()
        else:
            result = self._run_generic()
        
        duration_ms = int((time.time() - self.start_time) * 1000)
        
        return {
            "worker_id": self.context.worker_id,
            "role": self.context.role,
            "status": "completed",
            "summary": result.get("summary", "Task completed"),
            "result": result.get("detail", ""),
            "tool_uses": self.tools.tool_uses,
            "duration_ms": duration_ms,
            "findings": result.get("findings", [])
        }
    
    def _run_researcher(self) -> Dict[str, Any]:
        """Researcher role: explore codebase and gather information"""
        print(f"[Worker {self.context.worker_id}] Running as researcher...")
        
        # Simulate exploration
        files = self.tools.glob("*.py")
        
        findings = [
            f"Found {len(files)} Python files in the project",
            "Key modules identified: coordinator.py, worker.py, protocol.py",
            "Project structure follows clean architecture pattern"
        ]
        
        # Save findings to scratchpad
        self.context.write_scratchpad(
            f"findings-{self.context.worker_id}.json",
            json.dumps({
                "worker_id": self.context.worker_id,
                "task": self.context.task,
                "findings": findings,
                "files_discovered": files[:10]
            }, indent=2)
        )
        
        return {
            "summary": f"Explored codebase, found {len(files)} relevant files",
            "detail": "\n".join(findings),
            "findings": findings
        }
    
    def _run_implementer(self) -> Dict[str, Any]:
        """Implementer role: make code changes"""
        print(f"[Worker {self.context.worker_id}] Running as implementer...")
        
        # Simulate implementation
        changes = [
            "Added error handling to coordinator.py",
            "Updated worker protocol to support async",
            "Refactored tool registration"
        ]
        
        return {
            "summary": f"Implemented {len(changes)} changes",
            "detail": "\n".join(changes),
            "findings": changes
        }
    
    def _run_verifier(self) -> Dict[str, Any]:
        """Verifier role: verify changes work correctly"""
        print(f"[Worker {self.context.worker_id}] Running as verifier...")
        
        # Simulate verification
        test_results = [
            "✓ Unit tests pass (42/42)",
            "✓ Integration tests pass (15/15)",
            "✓ No regressions detected"
        ]
        
        return {
            "summary": "All tests passed, implementation verified",
            "detail": "\n".join(test_results),
            "findings": test_results
        }
    
    def _run_generic(self) -> Dict[str, Any]:
        """Generic worker role"""
        print(f"[Worker {self.context.worker_id}] Running generic task...")
        
        return {
            "summary": f"Completed generic task: {self.context.task[:50]}...",
            "detail": "Task executed successfully",
            "findings": []
        }
    
    def format_xml_notification(self, result: Dict[str, Any]) -> str:
        """Format result as XML notification for Coordinator"""
        from coordinator import XMLProtocol
        
        return XMLProtocol.create_notification(
            task_id=result["worker_id"],
            status=result["status"],
            summary=result["summary"],
            result=result["result"],
            usage={
                "total_tokens": len(str(result)),
                "tool_uses": result["tool_uses"],
                "duration_ms": result["duration_ms"]
            }
        )


def spawn_worker(worker_id: str, role: str, task: str, scratchpad_dir: str = ".openclaw/scratchpad") -> str:
    """
    Spawn a worker and run its task.
    Returns the XML notification to send back to Coordinator.
    """
    context = WorkerContext(
        worker_id=worker_id,
        role=role,
        task=task,
        scratchpad_dir=scratchpad_dir
    )
    
    worker = WorkerAgent(context)
    result = worker.run()
    
    return worker.format_xml_notification(result)


def main():
    """CLI for running a worker"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Worker agent for OpenClaw Multi-Agent system")
    parser.add_argument("--id", required=True, help="Worker ID")
    parser.add_argument("--role", default="worker", help="Worker role (researcher, implementer, verifier)")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--scratchpad", default=".openclaw/scratchpad", help="Scratchpad directory")
    
    args = parser.parse_args()
    
    # Run worker and output XML notification
    xml_notification = spawn_worker(
        worker_id=args.id,
        role=args.role,
        task=args.task,
        scratchpad_dir=args.scratchpad
    )
    
    print("\n" + "="*60)
    print("XML NOTIFICATION (send this to Coordinator):")
    print("="*60)
    print(xml_notification)


if __name__ == "__main__":
    main()
