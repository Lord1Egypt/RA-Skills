#!/usr/bin/env python3
"""Pattern analysis system for OpenClaw."""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
PATTERN_DIR = WORKSPACE / "patterns"
PATTERN_DIR.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """Log a message with timestamp."""
    timestamp = datetime.now().isoformat()
    log_file = PATTERN_DIR / "analyzer.log"
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {level}: {message}\n")
    print(f"[{timestamp}] {level}: {message}")

class PatternAnalyzer:
    """Analyze patterns and suggest optimizations."""
    
    def __init__(self):
        """Initialize pattern analyzer."""
        self.patterns = self._load_patterns()
        self.suggestions = defaultdict(list)
    
    def _load_patterns(self):
        """Load learned patterns."""
        pattern_file = PATTERN_DIR / "patterns.json"
        try:
            with open(pattern_file) as f:
                return json.load(f)
        except Exception as e:
            log(f"Error loading patterns: {e}", "ERROR")
            return defaultdict(list)
    
    def analyze_operations(self):
        """Analyze operation patterns."""
        log("Analyzing operations...")
        
        try:
            commands = self.patterns.get("commands", [])
            
            # Find common command sequences
            sequences = self._find_sequences(commands)
            
            # Find opportunities for batching
            batching = self._find_batching(commands)
            
            # Find template opportunities
            templates = self._find_templates(commands)
            
            self.suggestions["operations"].extend([
                {"type": "sequence", "data": sequences},
                {"type": "batching", "data": batching},
                {"type": "template", "data": templates}
            ])
        
        except Exception as e:
            log(f"Error analyzing operations: {e}", "ERROR")
    
    def analyze_resources(self):
        """Analyze resource usage patterns."""
        log("Analyzing resources...")
        
        try:
            resources = self.patterns.get("resources", [])
            
            # Find resource bottlenecks
            bottlenecks = self._find_bottlenecks(resources)
            
            # Find optimization opportunities
            optimizations = self._find_optimizations(resources)
            
            self.suggestions["resources"].extend([
                {"type": "bottleneck", "data": bottlenecks},
                {"type": "optimization", "data": optimizations}
            ])
        
        except Exception as e:
            log(f"Error analyzing resources: {e}", "ERROR")
    
    def analyze_workflows(self):
        """Analyze workflow patterns."""
        log("Analyzing workflows...")
        
        try:
            workflows = self.patterns.get("workflows", [])
            
            # Find common workflows
            common = self._find_common_workflows(workflows)
            
            # Find optimization opportunities
            optimizations = self._find_workflow_optimizations(workflows)
            
            self.suggestions["workflows"].extend([
                {"type": "common", "data": common},
                {"type": "optimization", "data": optimizations}
            ])
        
        except Exception as e:
            log(f"Error analyzing workflows: {e}", "ERROR")
    
    def _find_sequences(self, commands):
        """Find common command sequences."""
        sequences = []
        
        # Group by pattern
        by_pattern = defaultdict(int)
        for cmd in commands:
            by_pattern[cmd["pattern"]] += 1
        
        # Find frequent sequences
        frequent = [p for p, c in by_pattern.items() if c >= 3]
        if frequent:
            sequences.append({
                "type": "frequent_commands",
                "patterns": frequent,
                "suggestion": "Create shortcuts or aliases for common commands"
            })
        
        return sequences
    
    def _find_batching(self, commands):
        """Find batching opportunities."""
        batching = []
        
        # Look for similar commands
        similar = defaultdict(list)
        for cmd in commands:
            key = cmd["pattern"].split()[0]  # Group by first word
            similar[key].append(cmd)
        
        # Find batch opportunities
        for key, cmds in similar.items():
            if len(cmds) >= 3:
                batching.append({
                    "type": "similar_commands",
                    "command": key,
                    "count": len(cmds),
                    "suggestion": f"Batch {len(cmds)} similar {key} operations"
                })
        
        return batching
    
    def _find_templates(self, commands):
        """Find template opportunities."""
        templates = []
        
        # Look for parameterized commands
        parameterized = [c for c in commands if "{" in c["pattern"]]
        if parameterized:
            templates.append({
                "type": "parameterized_commands",
                "count": len(parameterized),
                "suggestion": "Create templates for parameterized commands"
            })
        
        return templates
    
    def _find_bottlenecks(self, resources):
        """Find resource bottlenecks."""
        bottlenecks = []
        
        # Group by resource type
        by_type = defaultdict(list)
        for r in resources:
            by_type[r["type"]].append(r)
        
        # Find high usage patterns
        for rtype, values in by_type.items():
            high = [v for v in values if v["value"] > 80]
            if high:
                bottlenecks.append({
                    "type": rtype,
                    "count": len(high),
                    "suggestion": f"High {rtype} usage detected {len(high)} times"
                })
        
        return bottlenecks
    
    def _find_optimizations(self, resources):
        """Find resource optimization opportunities."""
        optimizations = []
        
        # Look for patterns in resource usage
        for r in resources:
            if r["value"] > 90:
                optimizations.append({
                    "type": "critical",
                    "resource": r["type"],
                    "value": r["value"],
                    "suggestion": f"Critical {r['type']} usage needs immediate optimization"
                })
            elif r["value"] > 75:
                optimizations.append({
                    "type": "warning",
                    "resource": r["type"],
                    "value": r["value"],
                    "suggestion": f"High {r['type']} usage should be optimized"
                })
        
        return optimizations
    
    def _find_common_workflows(self, workflows):
        """Find common workflow patterns."""
        common = []
        
        # Count workflow patterns
        by_pattern = defaultdict(int)
        for w in workflows:
            pattern = tuple(w["steps"])
            by_pattern[pattern] += 1
        
        # Find frequent workflows
        frequent = [(p, c) for p, c in by_pattern.items() if c >= 2]
        for pattern, count in frequent:
            common.append({
                "type": "frequent_workflow",
                "steps": list(pattern),
                "count": count,
                "suggestion": f"Create automation for workflow used {count} times"
            })
        
        return common
    
    def _find_workflow_optimizations(self, workflows):
        """Find workflow optimization opportunities."""
        optimizations = []
        
        # Look for patterns in workflow steps
        for w in workflows:
            steps = w["steps"]
            if len(steps) > 5:
                optimizations.append({
                    "type": "long_workflow",
                    "steps": len(steps),
                    "suggestion": f"Long workflow with {len(steps)} steps - consider breaking down"
                })
        
        return optimizations
    
    def get_suggestions(self):
        """Get all suggestions."""
        return dict(self.suggestions)

def main():
    """Main entry point."""
    analyzer = PatternAnalyzer()
    
    # Run all analyses
    analyzer.analyze_operations()
    analyzer.analyze_resources()
    analyzer.analyze_workflows()
    
    # Save suggestions
    suggestions_file = PATTERN_DIR / "suggestions.json"
    with open(suggestions_file, "w") as f:
        json.dump(analyzer.get_suggestions(), f, indent=2)
    
    log("Pattern analysis complete")

if __name__ == "__main__":
    sys.exit(main())