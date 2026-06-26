#!/usr/bin/env python3
"""
State Manager for gstack-skills

This script manages workflow state between gstack skills.
It stores and retrieves context, allowing skills to share information.

Usage:
    python state_manager.py init <workflow_id>
    python state_manager.py set <workflow_id> <key> <value>
    python state_manager.py get <workflow_id> <key>
    python state_manager.py list <workflow_id>
"""

import json
import uuid
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class StateManager:
    """Manages workflow state between gstack skills."""

    def __init__(self, state_dir: str = None):
        """
        Initialize the state manager.

        Args:
            state_dir: Directory to store state files
        """
        if state_dir is None:
            # Default to .workbuddy/gstack-state in the project
            self.state_dir = Path(".workbuddy/gstack-state")
        else:
            self.state_dir = Path(state_dir)
        
        # Ensure state directory exists
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def create_workflow(self) -> str:
        """
        Create a new workflow with a unique ID.

        Returns:
            Workflow ID
        """
        workflow_id = str(uuid.uuid4())[:8]
        workflow_file = self.state_dir / f"{workflow_id}.json"
        
        state = {
            "workflow_id": workflow_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "current_step": None,
            "steps": [],
            "data": {},
        }
        
        with open(workflow_file, "w") as f:
            json.dump(state, f, indent=2)
        
        return workflow_id

    def load_workflow(self, workflow_id: str) -> Optional[Dict]:
        """
        Load a workflow's state.

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow state dictionary, or None if not found
        """
        workflow_file = self.state_dir / f"{workflow_id}.json"
        
        if not workflow_file.exists():
            return None
        
        with open(workflow_file, "r") as f:
            return json.load(f)

    def save_workflow(self, workflow_id: str, state: Dict) -> bool:
        """
        Save a workflow's state.

        Args:
            workflow_id: Workflow ID
            state: State dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        workflow_file = self.state_dir / f"{workflow_id}.json"
        
        state["updated_at"] = datetime.now().isoformat()
        
        try:
            with open(workflow_file, "w") as f:
                json.dump(state, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving workflow: {e}")
            return False

    def set_data(self, workflow_id: str, key: str, value: Any) -> bool:
        """
        Set a data key in the workflow state.

        Args:
            workflow_id: Workflow ID
            key: Data key
            value: Data value

        Returns:
            True if saved successfully, False otherwise
        """
        state = self.load_workflow(workflow_id)
        
        if state is None:
            print(f"Workflow {workflow_id} not found")
            return False
        
        state["data"][key] = value
        return self.save_workflow(workflow_id, state)

    def get_data(self, workflow_id: str, key: str) -> Optional[Any]:
        """
        Get a data value from the workflow state.

        Args:
            workflow_id: Workflow ID
            key: Data key

        Returns:
            Data value, or None if not found
        """
        state = self.load_workflow(workflow_id)
        
        if state is None:
            return None
        
        return state["data"].get(key)

    def add_step(self, workflow_id: str, skill_name: str, step_data: Dict) -> bool:
        """
        Add a step to the workflow.

        Args:
            workflow_id: Workflow ID
            skill_name: Name of the skill that executed this step
            step_data: Data from this step

        Returns:
            True if saved successfully, False otherwise
        """
        state = self.load_workflow(workflow_id)
        
        if state is None:
            print(f"Workflow {workflow_id} not found")
            return False
        
        step = {
            "skill": skill_name,
            "timestamp": datetime.now().isoformat(),
            "data": step_data,
        }
        
        state["steps"].append(step)
        state["current_step"] = skill_name
        
        return self.save_workflow(workflow_id, state)

    def get_workflow_summary(self, workflow_id: str) -> Optional[Dict]:
        """
        Get a summary of the workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            Summary dictionary, or None if not found
        """
        state = self.load_workflow(workflow_id)
        
        if state is None:
            return None
        
        summary = {
            "workflow_id": state["workflow_id"],
            "created_at": state["created_at"],
            "updated_at": state["updated_at"],
            "current_step": state["current_step"],
            "steps_completed": len(state["steps"]),
            "data_keys": list(state["data"].keys()),
        }
        
        return summary

    def list_workflows(self) -> list:
        """
        List all workflows.

        Returns:
            List of workflow summaries
        """
        workflows = []
        
        for workflow_file in self.state_dir.glob("*.json"):
            workflow_id = workflow_file.stem
            summary = self.get_workflow_summary(workflow_id)
            if summary:
                workflows.append(summary)
        
        return workflows

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            True if deleted successfully, False otherwise
        """
        workflow_file = self.state_dir / f"{workflow_id}.json"
        
        if workflow_file.exists():
            workflow_file.unlink()
            return True
        
        return False


# Command line interface
def main():
    """Main entry point for command line usage."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python state_manager.py init")
        print("  python state_manager.py set <workflow_id> <key> <value>")
        print("  python state_manager.py get <workflow_id> <key>")
        print("  python state_manager.py list <workflow_id>")
        print("  python state_manager.py workflows")
        print("  python state_manager.py delete <workflow_id>")
        sys.exit(1)

    manager = StateManager()
    command = sys.argv[1]

    if command == "init":
        workflow_id = manager.create_workflow()
        print(json.dumps({"workflow_id": workflow_id, "status": "created"}))

    elif command == "set":
        if len(sys.argv) < 5:
            print("Usage: python state_manager.py set <workflow_id> <key> <value>")
            sys.exit(1)
        workflow_id = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        
        success = manager.set_data(workflow_id, key, value)
        print(json.dumps({"status": "success" if success else "failed"}))

    elif command == "get":
        if len(sys.argv) < 4:
            print("Usage: python state_manager.py get <workflow_id> <key>")
            sys.exit(1)
        workflow_id = sys.argv[2]
        key = sys.argv[3]
        
        value = manager.get_data(workflow_id, key)
        print(json.dumps({"value": value}, indent=2))

    elif command == "list":
        if len(sys.argv) < 3:
            print("Usage: python state_manager.py list <workflow_id>")
            sys.exit(1)
        workflow_id = sys.argv[2]
        
        state = manager.load_workflow(workflow_id)
        if state:
            print(json.dumps(state, indent=2))
        else:
            print(json.dumps({"error": "Workflow not found"}))

    elif command == "workflows":
        workflows = manager.list_workflows()
        print(json.dumps(workflows, indent=2))

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python state_manager.py delete <workflow_id>")
            sys.exit(1)
        workflow_id = sys.argv[2]
        
        success = manager.delete_workflow(workflow_id)
        print(json.dumps({"status": "success" if success else "failed"}))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
