#!/usr/bin/env python3
"""Pattern learning system for OpenClaw."""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import defaultdict

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
PATTERN_DIR = WORKSPACE / "patterns"
PATTERN_DIR.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """Log a message with timestamp."""
    timestamp = datetime.now().isoformat()
    log_file = PATTERN_DIR / "learner.log"
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {level}: {message}\n")
    print(f"[{timestamp}] {level}: {message}")

class PatternLearner:
    """Learn patterns from various sources."""
    
    def __init__(self):
        """Initialize pattern learner."""
        self.patterns = defaultdict(list)
        self.load_patterns()
    
    def load_patterns(self):
        """Load existing patterns."""
        pattern_file = PATTERN_DIR / "patterns.json"
        if pattern_file.exists():
            try:
                with open(pattern_file) as f:
                    self.patterns.update(json.load(f))
            except Exception as e:
                log(f"Error loading patterns: {e}", "ERROR")
    
    def save_patterns(self):
        """Save learned patterns."""
        pattern_file = PATTERN_DIR / "patterns.json"
        try:
            with open(pattern_file, "w") as f:
                json.dump(dict(self.patterns), f, indent=2)
        except Exception as e:
            log(f"Error saving patterns: {e}", "ERROR")
    
    def learn_from_operations(self, days=7):
        """Learn from operation history."""
        log("Learning from operations...")
        
        try:
            memory_dir = WORKSPACE / "memory"
            since = datetime.now() - timedelta(days=days)
            
            for file in memory_dir.rglob("*.md"):
                if not self._is_recent(file, since):
                    continue
                
                with open(file) as f:
                    content = f.read()
                
                # Find operation patterns
                self._extract_command_patterns(content)
                self._extract_workflow_patterns(content)
                self._extract_error_patterns(content)
        
        except Exception as e:
            log(f"Error learning from operations: {e}", "ERROR")
    
    def learn_from_errors(self, days=7):
        """Learn from error logs."""
        log("Learning from errors...")
        
        try:
            log_dir = WORKSPACE / "logs"
            since = datetime.now() - timedelta(days=days)
            
            for file in log_dir.rglob("*.log"):
                if not self._is_recent(file, since):
                    continue
                
                with open(file) as f:
                    content = f.read()
                
                # Find error patterns
                self._extract_error_patterns(content)
        
        except Exception as e:
            log(f"Error learning from errors: {e}", "ERROR")
    
    def learn_from_resources(self, days=7):
        """Learn from resource usage."""
        log("Learning from resources...")
        
        try:
            metrics_dir = WORKSPACE / "metrics"
            since = datetime.now() - timedelta(days=days)
            
            for file in metrics_dir.rglob("*.json"):
                if not self._is_recent(file, since):
                    continue
                
                with open(file) as f:
                    data = json.load(f)
                
                # Find resource patterns
                self._extract_resource_patterns(data)
        
        except Exception as e:
            log(f"Error learning from resources: {e}", "ERROR")
    
    def _is_recent(self, file, since):
        """Check if file is recent enough."""
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            return mtime >= since
        except Exception:
            return False
    
    def _extract_command_patterns(self, content):
        """Extract command patterns from content."""
        # Look for command blocks
        command_blocks = re.findall(r"```bash\n(.*?)```", content, re.DOTALL)
        
        for block in command_blocks:
            commands = block.strip().split("\n")
            for cmd in commands:
                if cmd and not cmd.startswith("#"):
                    pattern = self._generalize_command(cmd)
                    self.patterns["commands"].append({
                        "pattern": pattern,
                        "example": cmd,
                        "count": self.patterns["commands"].count(pattern) + 1
                    })
    
    def _extract_workflow_patterns(self, content):
        """Extract workflow patterns from content."""
        # Look for ordered lists
        workflows = re.findall(r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", content, re.DOTALL)
        
        if workflows:
            self.patterns["workflows"].append({
                "steps": workflows,
                "count": 1
            })
    
    def _extract_error_patterns(self, content):
        """Extract error patterns from content."""
        # Look for error messages
        errors = re.findall(r"(?:error|ERROR|Error):(.*?)(?=\n|$)", content)
        
        for error in errors:
            pattern = self._generalize_error(error)
            self.patterns["errors"].append({
                "pattern": pattern,
                "example": error.strip(),
                "count": self.patterns["errors"].count(pattern) + 1
            })
    
    def _extract_resource_patterns(self, data):
        """Extract resource usage patterns from metrics."""
        if isinstance(data, dict):
            if "memory" in data:
                self.patterns["resources"].append({
                    "type": "memory",
                    "value": data["memory"],
                    "timestamp": data.get("timestamp")
                })
            
            if "cpu" in data:
                self.patterns["resources"].append({
                    "type": "cpu",
                    "value": data["cpu"],
                    "timestamp": data.get("timestamp")
                })
    
    def _generalize_command(self, command):
        """Generalize a command pattern."""
        # Replace specific values with placeholders
        pattern = re.sub(r"[\w-]+\.(sh|py|md)", "{file}", command)
        pattern = re.sub(r"\d+", "{number}", pattern)
        pattern = re.sub(r"[\w-]+/[\w-]+", "{path}", pattern)
        return pattern
    
    def _generalize_error(self, error):
        """Generalize an error pattern."""
        # Replace specific values with placeholders
        pattern = re.sub(r"[\w-]+\.(sh|py|md)", "{file}", error)
        pattern = re.sub(r"\d+", "{number}", pattern)
        pattern = re.sub(r"[\w-]+/[\w-]+", "{path}", pattern)
        return pattern.strip()

def main():
    """Main entry point."""
    learner = PatternLearner()
    
    # Learn from all sources
    learner.learn_from_operations()
    learner.learn_from_errors()
    learner.learn_from_resources()
    
    # Save learned patterns
    learner.save_patterns()
    
    log("Pattern learning complete")

if __name__ == "__main__":
    sys.exit(main())