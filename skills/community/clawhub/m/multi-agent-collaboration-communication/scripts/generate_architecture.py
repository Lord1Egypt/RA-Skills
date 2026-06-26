#!/usr/bin/env python3
"""
Multi-Agent System Architecture Generator
Generate system architecture diagrams and configuration files
"""

import json
import yaml
import argparse
from datetime import datetime
from typing import Dict, List, Any


def generate_agent_config(agents: List[Dict], topology: str) -> Dict:
    """Generate Agent configuration"""
    config = {
        "system": {
            "name": "multi-agent-system",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat()
        },
        "agents": [],
        "communication": {
            "topology": topology,
            "protocol": "websocket"
        }
    }
    
    for i, agent in enumerate(agents):
        agent_config = {
            "id": agent.get("id", f"agent-{i}"),
            "name": agent.get("name", f"Agent {i}"),
            "description": agent.get("description", ""),
            "type": agent.get("type", "worker"),
            "capabilities": agent.get("capabilities", []),
            "endpoints": agent.get("endpoints", [])
        }
        config["agents"].append(agent_config)
    
    return config


def generate_workflow_config(steps: List[Dict], workflow_type: str = "sequential") -> Dict:
    """Generate workflow configuration"""
    return {
        "workflow": {
            "name": "generated-workflow",
            "type": workflow_type,
            "steps": steps,
            "error_handling": {
                "strategy": "retry_then_fallback",
                "retry": {
                    "max_attempts": 3,
                    "delay": 5
                }
            }
        }
    }


def generate_architecture_diagram(agents: List[Dict], topology: str) -> str:
    """Generate text-based architecture diagram"""
    lines = ["System Architecture Diagram", "=" * 40, ""]
    
    if topology == "star":
        lines.append("        ┌─────────────┐")
        lines.append("        │ Coordinator │")
        lines.append("        └──────┬──────┘")
        lines.append("               │")
        connections = "    ".join([f"[{a['id']}]" for a in agents if a.get('type') != 'coordinator'])
        lines.append(f"    {connections}")
        
    elif topology == "pipeline":
        flow = " → ".join([f"[{a['id']}]" for a in agents])
        lines.append(flow)
        
    elif topology == "mesh":
        for agent in agents:
            connections = ", ".join([a['id'] for a in agents if a['id'] != agent['id']])
            lines.append(f"[{agent['id']}] ↔ {connections}")
            
    elif topology == "hierarchical":
        lines.append("           [Root]")
        lines.append("          /      \\")
        children = [a for a in agents if a.get('type') != 'coordinator']
        mid = len(children) // 2
        left = "    ".join([f"[{c['id']}]" for c in children[:mid]])
        right = "    ".join([f"[{c['id']}]" for c in children[mid:]])
        lines.append(f"      {left}      {right}")
    
    return "\n".join(lines)


def generate_dependency_graph(dependencies: List[Dict]) -> str:
    """Generate dependency graph"""
    lines = ["Task Dependency Graph", "=" * 40, ""]
    
    for dep in dependencies:
        task = dep.get("task", "")
        deps = dep.get("depends_on", [])
        if deps:
            dep_str = ", ".join(deps)
            lines.append(f"[{dep_str}] ──► [{task}]")
        else:
            lines.append(f"[Start] ──► [{task}]")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Architecture Generator")
    parser.add_argument("--config", "-c", help="Input configuration file (JSON/YAML)")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--topology", "-t", default="star", 
                       choices=["star", "bus", "mesh", "hierarchical", "pipeline"],
                       help="Architecture topology")
    parser.add_argument("--format", "-f", default="yaml", choices=["json", "yaml"],
                       help="Output format")
    
    args = parser.parse_args()
    
    # Example Agent definitions
    example_agents = [
        {
            "id": "coordinator",
            "name": "Coordinator",
            "type": "coordinator",
            "description": "Responsible for overall coordination",
            "capabilities": ["dispatch", "monitor"]
        },
        {
            "id": "worker-1",
            "name": "Worker Node 1",
            "type": "worker",
            "description": "Data processing",
            "capabilities": ["process"]
        },
        {
            "id": "worker-2",
            "name": "Worker Node 2",
            "type": "worker",
            "description": "Data analysis",
            "capabilities": ["analyze"]
        }
    ]
    
    # Generate architecture diagram
    diagram = generate_architecture_diagram(example_agents, args.topology)
    print(diagram)
    print("\n")
    
    # Generate configuration
    config = generate_agent_config(example_agents, args.topology)
    
    if args.format == "json":
        output = json.dumps(config, indent=2, ensure_ascii=False)
    else:
        output = yaml.dump(config, allow_unicode=True, sort_keys=False)
    
    print("Generated Configuration:")
    print("-" * 40)
    print(output)
    
    if args.output:
        import os
        os.makedirs(args.output, exist_ok=True)
        
        # Save configuration
        ext = "json" if args.format == "json" else "yaml"
        config_path = os.path.join(args.output, f"agent-config.{ext}")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nConfiguration saved to: {config_path}")
        
        # Save architecture diagram
        diagram_path = os.path.join(args.output, "architecture.txt")
        with open(diagram_path, "w", encoding="utf-8") as f:
            f.write(diagram)
        print(f"Architecture diagram saved to: {diagram_path}")


if __name__ == "__main__":
    main()