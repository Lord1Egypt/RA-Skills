#!/usr/bin/env python3
"""
Multi-Agent Coordination Script

This script provides coordination capabilities for multiple AI agents working together
on complex tasks. It handles task delegation, progress tracking, and result aggregation.
"""

import json
import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentTask:
    """Represents a task assigned to an agent"""
    task_id: str
    agent_id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

@dataclass
class CoordinationSession:
    """Represents a multi-agent coordination session"""
    session_id: str
    master_task: str
    subtasks: List[AgentTask]
    status: str = "active"  # active, completed, failed
    created_at: str = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class MultiAgentCoordinator:
    """Main coordinator class for managing multiple agents"""
    
    def __init__(self, session_file: str = None):
        self.session_file = session_file or "coordination_session.json"
        self.session: Optional[CoordinationSession] = None
        
    def create_session(self, master_task: str, subtasks: List[Dict[str, str]]) -> str:
        """Create a new coordination session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        agent_tasks = []
        for i, subtask in enumerate(subtasks):
            task = AgentTask(
                task_id=f"task_{i+1}",
                agent_id=subtask.get("agent_id", f"agent_{i+1}"),
                description=subtask["description"]
            )
            agent_tasks.append(task)
            
        self.session = CoordinationSession(
            session_id=session_id,
            master_task=master_task,
            subtasks=agent_tasks
        )
        
        self._save_session()
        return session_id
    
    def assign_task(self, agent_id: str, task_description: str) -> str:
        """Assign a new task to a specific agent"""
        if not self.session:
            raise ValueError("No active session")
            
        task_id = f"task_{len(self.session.subtasks) + 1}"
        new_task = AgentTask(
            task_id=task_id,
            agent_id=agent_id,
            description=task_description
        )
        
        self.session.subtasks.append(new_task)
        self._save_session()
        return task_id
    
    def update_task_status(self, task_id: str, status: str, result: str = None):
        """Update the status of a specific task"""
        if not self.session:
            raise ValueError("No active session")
            
        for task in self.session.subtasks:
            if task.task_id == task_id:
                task.status = status
                if result:
                    task.result = result
                task.updated_at = datetime.now().isoformat()
                break
                
        # Check if all tasks are completed
        if all(task.status == "completed" for task in self.session.subtasks):
            self.session.status = "completed"
            self.session.completed_at = datetime.now().isoformat()
            
        self._save_session()
    
    def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        """Get the current status of a specific task"""
        if not self.session:
            return None
            
        for task in self.session.subtasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get the overall session status"""
        if not self.session:
            return {"error": "No active session"}
            
        completed_tasks = sum(1 for task in self.session.subtasks if task.status == "completed")
        total_tasks = len(self.session.subtasks)
        
        return {
            "session_id": self.session.session_id,
            "master_task": self.session.master_task,
            "status": self.session.status,
            "progress": f"{completed_tasks}/{total_tasks}",
            "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "tasks": [
                {
                    "task_id": task.task_id,
                    "agent_id": task.agent_id,
                    "description": task.description,
                    "status": task.status,
                    "result": task.result
                }
                for task in self.session.subtasks
            ]
        }
    
    def _save_session(self):
        """Save the current session to file"""
        if self.session:
            session_data = {
                "session_id": self.session.session_id,
                "master_task": self.session.master_task,
                "status": self.session.status,
                "created_at": self.session.created_at,
                "completed_at": self.session.completed_at,
                "subtasks": [
                    {
                        "task_id": task.task_id,
                        "agent_id": task.agent_id,
                        "description": task.description,
                        "status": task.status,
                        "result": task.result,
                        "created_at": task.created_at,
                        "updated_at": task.updated_at
                    }
                    for task in self.session.subtasks
                ]
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
    
    def load_session(self, session_file: str = None):
        """Load a session from file"""
        file_to_load = session_file or self.session_file
        
        if os.path.exists(file_to_load):
            with open(file_to_load, 'r') as f:
                session_data = json.load(f)
                
            subtasks = []
            for task_data in session_data["subtasks"]:
                task = AgentTask(
                    task_id=task_data["task_id"],
                    agent_id=task_data["agent_id"],
                    description=task_data["description"],
                    status=task_data["status"],
                    result=task_data.get("result"),
                    created_at=task_data["created_at"],
                    updated_at=task_data["updated_at"]
                )
                subtasks.append(task)
                
            self.session = CoordinationSession(
                session_id=session_data["session_id"],
                master_task=session_data["master_task"],
                subtasks=subtasks,
                status=session_data["status"],
                created_at=session_data["created_at"],
                completed_at=session_data.get("completed_at")
            )
        else:
            raise FileNotFoundError(f"Session file {file_to_load} not found")

def main():
    """Command line interface for the coordinator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Agent Coordinator")
    parser.add_argument("--action", required=True, 
                       choices=["create", "assign", "update", "status", "load"],
                       help="Action to perform")
    parser.add_argument("--session-file", default="coordination_session.json",
                       help="Session file path")
    parser.add_argument("--master-task", help="Master task description")
    parser.add_argument("--subtasks", help="JSON array of subtasks")
    parser.add_argument("--agent-id", help="Agent ID")
    parser.add_argument("--task-description", help="Task description")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--status", help="New status")
    parser.add_argument("--result", help="Task result")
    
    args = parser.parse_args()
    
    coordinator = MultiAgentCoordinator(args.session_file)
    
    if args.action == "create":
        if not args.master_task or not args.subtasks:
            print("Error: --master-task and --subtasks required for create action")
            return 1
            
        subtasks = json.loads(args.subtasks)
        session_id = coordinator.create_session(args.master_task, subtasks)
        print(f"Created session: {session_id}")
        
    elif args.action == "assign":
        if not args.agent_id or not args.task_description:
            print("Error: --agent-id and --task-description required for assign action")
            return 1
            
        task_id = coordinator.assign_task(args.agent_id, args.task_description)
        print(f"Assigned task: {task_id}")
        
    elif args.action == "update":
        if not args.task_id or not args.status:
            print("Error: --task-id and --status required for update action")
            return 1
            
        coordinator.update_task_status(args.task_id, args.status, args.result)
        print(f"Updated task {args.task_id} to status: {args.status}")
        
    elif args.action == "status":
        status = coordinator.get_session_status()
        print(json.dumps(status, indent=2))
        
    elif args.action == "load":
        try:
            coordinator.load_session()
            print("Loaded session successfully")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())