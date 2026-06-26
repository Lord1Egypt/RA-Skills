#!/usr/bin/env python3
"""
Multi-Agent System Design Proposal Validator
Checks the completeness and reasonableness of design proposals
"""

import json
import yaml
import argparse
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]
    
    def __init__(self):
        self.passed = True
        self.errors = []
        self.warnings = []
    
    def add_error(self, message: str):
        self.passed = False
        self.errors.append(message)
    
    def add_warning(self, message: str):
        self.warnings.append(message)


class DesignValidator:
    """Design proposal validator"""
    
    def __init__(self, design: Dict):
        self.design = design
        self.result = ValidationResult()
    
    def validate(self) -> ValidationResult:
        """Execute full validation"""
        self._validate_structure()
        self._validate_agents()
        self._validate_communication()
        self._validate_workflow()
        self._validate_dependencies()
        return self.result
    
    def _validate_structure(self):
        """Validate basic structure"""
        required_sections = ["agents", "communication"]
        
        for section in required_sections:
            if section not in self.design:
                self.result.add_error(f"Missing required section: {section}")
    
    def _validate_agents(self):
        """Validate Agent definitions"""
        if "agents" not in self.design:
            return
        
        agents = self.design["agents"]
        if not isinstance(agents, list):
            self.result.add_error("agents must be a list")
            return
        
        if len(agents) == 0:
            self.result.add_error("At least one Agent must be defined")
            return
        
        agent_ids = set()
        has_coordinator = False
        
        for i, agent in enumerate(agents):
            prefix = f"agents[{i}]"
            
            # Check required fields
            if "id" not in agent:
                self.result.add_error(f"{prefix}: missing id field")
                continue
            
            agent_id = agent["id"]
            
            # Check ID uniqueness
            if agent_id in agent_ids:
                self.result.add_error(f"{prefix}: duplicate Agent ID '{agent_id}'")
            agent_ids.add(agent_id)
            
            # Check type
            if "type" in agent:
                if agent["type"] == "coordinator":
                    has_coordinator = True
                elif agent["type"] not in ["worker", "specialist"]:
                    self.result.add_warning(f"{prefix}: unknown Agent type '{agent['type']}'")
            
            # Check capability definitions
            if "capabilities" not in agent:
                self.result.add_warning(f"{prefix}: it is recommended to define capabilities")
        
        if not has_coordinator and len(agents) > 1:
            self.result.add_warning("Multi-agent system is recommended to define a coordinator-type Agent")
    
    def _validate_communication(self):
        """Validate communication configuration"""
        if "communication" not in self.design:
            return
        
        comm = self.design["communication"]
        
        # Check topology type
        if "topology" in comm:
            valid_topologies = ["star", "bus", "mesh", "hierarchical", "pipeline"]
            if comm["topology"] not in valid_topologies:
                self.result.add_warning(f"Unknown topology type: {comm['topology']}")
        
        # Check protocol
        if "protocol" in comm:
            valid_protocols = ["http", "websocket", "grpc", "mqtt"]
            if comm["protocol"] not in valid_protocols:
                self.result.add_warning(f"Unknown communication protocol: {comm['protocol']}")
    
    def _validate_workflow(self):
        """Validate workflow definitions"""
        if "workflow" not in self.design:
            return
        
        workflow = self.design["workflow"]
        
        if "steps" not in workflow:
            self.result.add_warning("workflow: it is recommended to define steps")
            return
        
        steps = workflow["steps"]
        if not isinstance(steps, list):
            self.result.add_error("workflow.steps must be a list")
            return
        
        step_ids = set()
        for i, step in enumerate(steps):
            prefix = f"workflow.steps[{i}]"
            
            if "id" not in step:
                self.result.add_error(f"{prefix}: missing id field")
                continue
            
            if step["id"] in step_ids:
                self.result.add_error(f"{prefix}: duplicate step ID '{step['id']}'")
            step_ids.add(step["id"])
            
            if "agent" not in step:
                self.result.add_error(f"{prefix}: missing agent field")
    
    def _validate_dependencies(self):
        """Validate dependencies"""
        if "dependencies" not in self.design:
            return
        
        deps = self.design["dependencies"]
        if not isinstance(deps, list):
            return
        
        # Check for circular dependencies
        dep_graph = {}
        for dep in deps:
            task = dep.get("task", "")
            depends_on = dep.get("depends_on", [])
            dep_graph[task] = depends_on
        
        # Simple cycle detection
        visited = set()
        rec_stack = set()
        
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in dep_graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in dep_graph:
            if node not in visited:
                if has_cycle(node, visited, rec_stack):
                    self.result.add_error("Circular dependency detected")
                    break


def load_config(path: str) -> Dict:
    """Load configuration file"""
    with open(path, 'r', encoding='utf-8') as f:
        if path.endswith('.json'):
            return json.load(f)
        elif path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        else:
            # Try JSON first, fallback to YAML on failure
            try:
                return json.load(f)
            except:
                f.seek(0)
                return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Design Proposal Validator")
    parser.add_argument("config", help="Configuration file path (JSON/YAML)")
    parser.add_argument("--strict", "-s", action="store_true", help="Strict mode (warnings treated as errors)")
    
    args = parser.parse_args()
    
    try:
        design = load_config(args.config)
    except Exception as e:
        print(f"❌ Configuration file loading failed: {e}")
        return 1
    
    validator = DesignValidator(design)
    result = validator.validate()
    
    # Output results
    print("=" * 50)
    print("Design Proposal Validation Results")
    print("=" * 50)
    
    if result.errors:
        print(f"\n❌ Found {len(result.errors)} error(s):")
        for error in result.errors:
            print(f"   • {error}")
    
    if result.warnings:
        print(f"\n⚠️  Found {len(result.warnings)} warning(s):")
        for warning in result.warnings:
            print(f"   • {warning}")
    
    if result.passed and not result.warnings:
        print("\n✅ Validation passed! Design proposal is complete and reasonable.")
    elif result.passed:
        print("\n✅ Validation passed, but warnings exist. Recommended to review.")
    else:
        print("\n❌ Validation failed. Please fix the above errors.")
    
    # Strict mode
    if args.strict and result.warnings:
        print("\n[Strict Mode] Warnings treated as errors")
        return 1
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    exit(main())