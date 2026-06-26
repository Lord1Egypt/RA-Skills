"""
King's Watching - AI Workflow Enforcer + Task Translator v0.4.0

Core Upgrades:
1. TaskTranslator - Natural language to executable YAML translator
2. Auto task chunking - Split tasks by AI capacity limits
3. Step verification mechanism - Prevents AI from cutting corners
4. Intent pattern library - Common task pattern recognition

Author: OpenClaw Community
Version: 0.4.0
"""

import json
import os
import sys
import time
import uuid
import re
import math
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from functools import wraps
from dataclasses import dataclass, asdict, field


# ==================== Data Classes ====================

@dataclass
class JobInfo:
    """Async job information"""
    id: str
    workflow_name: str
    status: str
    current_step: int
    total_steps: int
    start_time: str
    eta: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    chunks_completed: int = 0
    chunks_total: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TaskIntent:
    """Task intent recognition result"""
    name: str
    task_type: str
    total_units: int
    unit_name: str
    parameters: Dict = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class TaskChunk:
    """Task chunk (split task unit)"""
    index: int
    start: int
    end: int
    description: str
    expected_count: int
    verification_type: str
    timeout: int


@dataclass
class StepVerifier:
    """Step verification configuration"""
    verification_type: str  # count_check, word_count_check, completeness_check
    min_required: int
    max_retries: int = 3
    on_failure: str = "retry"  # retry, skip, abort


# ==================== AI Capacity Configuration ====================

DEFAULT_CAPACITY_CONFIG = {
    "search_download": {
        "max_items": 10,
        "time_limit": 300,
        "verification": "count_check",
        "description": "Search and download materials"
    },
    "report_writing": {
        "max_items": 2000,
        "time_limit": 600,
        "verification": "word_count_check",
        "description": "Write report content"
    },
    "data_analysis": {
        "max_items": 100,
        "time_limit": 300,
        "verification": "completeness_check",
        "description": "Analyze data"
    },
    "api_batch": {
        "max_items": 20,
        "time_limit": 60,
        "verification": "count_check",
        "description": "Batch API calls"
    },
    "file_processing": {
        "max_items": 10,
        "time_limit": 180,
        "verification": "count_check",
        "description": "Process files"
    }
}


# ==================== Intent Patterns ====================

DEFAULT_INTENT_PATTERNS = [
    {
        "name": "batch_download",
        "regexes": [
            r"download\s+(\d+)\s+(\w+)",
            r"fetch\s+(\d+)\s+(\w+)",
            r"collect\s+(\d+)\s+(\w+)",
            r"gather\s+(\d+)\s+(\w+)"
        ],
        "task_type": "search_download",
        "unit": "items",
        "parameters": {"source": "auto"}
    },
    {
        "name": "report_writing",
        "regexes": [
            r"write\s+(?:a\s+)?(\d+)\s*(k|thousand)?\s*(?:word)?\s*report",
            r"generate\s+(?:a\s+)?(\d+)\s*(k|thousand)?\s*(?:word)?\s*report",
            r"compose\s+(?:a\s+)?(\d+)\s*(k|thousand)?\s*(?:word)?\s*report"
        ],
        "task_type": "report_writing",
        "unit": "words",
        "parameters": {"style": "formal"}
    },
    {
        "name": "data_analysis",
        "regexes": [
            r"analyze\s+(\d+)\s+(\w+)",
            r"process\s+(\d+)\s+(\w+)",
            r"review\s+(\d+)\s+(\w+)"
        ],
        "task_type": "data_analysis",
        "unit": "entries",
        "parameters": {"output_format": "structured"}
    },
    {
        "name": "api_batch",
        "regexes": [
            r"call\s+(?:api\s+)?(\d+)\s+(?:times?|requests?)",
            r"invoke\s+(?:api\s+)?(\d+)\s+(?:times?|requests?)"
        ],
        "task_type": "api_batch",
        "unit": "calls",
        "parameters": {"rate_limit": "respect"}
    }
]


# ==================== Task Translator ====================

class TaskTranslator:
    """
    Natural language task translator
    
    Converts natural language commands like "Download 100 reports"
    into executable step plans with auto-chunking.
    """
    
    def __init__(
        self,
        capacity_config: Dict = None,
        patterns: List = None
    ):
        self.capacity_config = capacity_config or DEFAULT_CAPACITY_CONFIG.copy()
        self.patterns = patterns or DEFAULT_INTENT_PATTERNS.copy()
    
    def translate(self, natural_command: str, context: Dict = None) -> Dict:
        """
        Natural language → Executable YAML plan
        
        Args:
            natural_command: Natural language command
            context: Additional context
            
        Returns:
            Execution plan dictionary
        """
        # Recognize intent
        intent = self._recognize_intent(natural_command)
        
        # Get capacity limits
        capacity = self.capacity_config.get(intent.task_type, self.capacity_config["search_download"])
        
        # Calculate chunks
        chunks = self._calculate_chunks(intent, capacity)
        
        # Generate steps
        steps = self._generate_steps(chunks, intent, capacity)
        
        # Build plan
        plan = {
            "workflow": {
                "name": f"auto_{intent.task_type}_{uuid.uuid4().hex[:8]}",
                "source_command": natural_command,
                "intent": intent.name,
                "task_type": intent.task_type,
                "total_units": intent.total_units,
                "unit_name": intent.unit_name,
                "estimated_time": len(chunks) * capacity["time_limit"]
            },
            "steps": steps,
            "verification": {
                "type": capacity["verification"],
                "enabled": True
            }
        }
        
        return plan
    
    def explain_plan(self, plan: Dict) -> str:
        """Generate human-readable plan description"""
        wf = plan.get("workflow", {})
        steps = plan.get("steps", [])
        
        lines = [
            "📋 Task Translation Result",
            f"Original command: {wf.get('source_command', 'N/A')}",
            f"Task scale: {wf.get('total_units', 0)} {wf.get('unit_name', 'items')}",
            f"Estimated time: {wf.get('estimated_time', 0)} seconds",
            f"Auto split into {len(steps)} execution steps:",
        ]
        
        for i, step in enumerate(steps, 1):
            lines.append(f"  Step {i}: {step['name']}")
            lines.append(f"         └─ Verify: {step.get('verification', 'N/A')}")
        
        lines.append("")
        lines.append("✅ Each Step has forced verification, AI cannot cut corners")
        
        return "\n".join(lines)
    
    def _recognize_intent(self, command: str) -> TaskIntent:
        """Recognize task intent from natural language"""
        command_lower = command.lower()
        
        # Try match patterns
        for pattern in self.patterns:
            for regex in pattern["regexes"]:
                match = re.search(regex, command_lower, re.IGNORECASE)
                if match:
                    # Extract number
                    num_str = match.group(1)
                    if pattern.get("unit") == "words" and len(match.groups()) > 1:
                        multiplier = match.group(2)
                        if multiplier in ("k", "thousand"):
                            num = int(num_str) * 1000
                        else:
                            num = int(num_str)
                    else:
                        num = int(num_str)
                    
                    return TaskIntent(
                        name=pattern["name"],
                        task_type=pattern["task_type"],
                        total_units=num,
                        unit_name=pattern.get("unit", "items"),
                        parameters=pattern.get("parameters", {}),
                        confidence=0.9
                    )
        
        # Default: generic task
        # Try extract any number
        numbers = re.findall(r'\d+', command_lower)
        if numbers:
            total = max([int(n) for n in numbers])
        else:
            total = 10  # Default
        
        return TaskIntent(
            name="generic_batch",
            task_type="search_download",
            total_units=total,
            unit_name="items",
            parameters={},
            confidence=0.5
        )
    
    def _calculate_chunks(self, intent: TaskIntent, capacity: Dict) -> List[TaskChunk]:
        """Calculate task chunks"""
        max_per_chunk = capacity["max_items"]
        total = intent.total_units
        
        chunks = []
        num_chunks = math.ceil(total / max_per_chunk)
        
        for i in range(num_chunks):
            start = i * max_per_chunk + 1
            end = min((i + 1) * max_per_chunk, total)
            
            chunk = TaskChunk(
                index=i,
                start=start,
                end=end,
                description=f"Process {start}-{end} (of {total})",
                expected_count=end - start + 1,
                verification_type=capacity["verification"],
                timeout=capacity["time_limit"]
            )
            chunks.append(chunk)
        
        return chunks
    
    def _generate_steps(self, chunks: List[TaskChunk], intent: TaskIntent, capacity: Dict) -> List[Dict]:
        """Generate execution steps"""
        steps = []
        
        for chunk in chunks:
            step = {
                "name": f"{intent.task_type}_batch_{chunk.index + 1}",
                "description": chunk.description,
                "task_type": intent.task_type,
                "params": {
                    "start": chunk.start,
                    "end": chunk.end,
                    "expected_count": chunk.expected_count,
                    **intent.parameters
                },
                "verification": {
                    "type": chunk.verification_type,
                    "min_required": chunk.expected_count,
                    "max_retries": 3,
                    "on_failure": "retry"
                },
                "timeout": chunk.timeout,
                "heartbeat_interval": 60,
                "retry": 3
            }
            steps.append(step)
        
        return steps


# ==================== Convenience Functions ====================

def create_translator(capacity_config: Dict = None, patterns: List = None) -> TaskTranslator:
    """Create task translator"""
    return TaskTranslator(capacity_config=capacity_config, patterns=patterns)


__all__ = [
    "TaskTranslator",
    "TaskIntent",
    "TaskChunk",
    "StepVerifier",
    "create_translator"
]
