#!/usr/bin/env python3
"""
Tool Registry - Core of LLM Tools

Unified tool definition and format conversion for multiple LLM providers.
"""

import json
from typing import Dict, List, Callable, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Tool:
    """Represents a tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Optional[Callable] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


class ToolRegistry:
    """Registry for managing LLM tools"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, name: str, description: str, parameters: Dict[str, Any],
                 handler: Optional[Callable] = None) -> Tool:
        """Register a tool"""
        tool = Tool(name=name, description=description, 
                   parameters=parameters, handler=handler)
        self._tools[name] = tool
        return tool
    
    def register_decorator(self, name: str, description: str, 
                          parameters: Dict[str, Any]):
        """Decorator to register a function as a tool"""
        def decorator(func: Callable):
            self.register(name, description, parameters, func)
            return func
        return decorator
    
    def register_from_dict(self, data: Dict[str, Any]) -> None:
        """Register tools from dictionary"""
        tools = data.get("tools", [])
        for tool_def in tools:
            self.register(
                name=tool_def["name"],
                description=tool_def.get("description", ""),
                parameters=tool_def.get("parameters", {"type": "object", "properties": {}})
            )
    
    def register_from_json_file(self, path: str) -> None:
        """Register tools from JSON file"""
        data = json.loads(Path(path).read_text())
        self.register_from_dict(data)
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())
    
    def to_openai(self) -> List[Dict[str, Any]]:
        """Convert to OpenAI function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self._tools.values()
        ]
    
    def to_anthropic(self) -> List[Dict[str, Any]]:
        """Convert to Anthropic tool use format"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters
            }
            for tool in self._tools.values()
        ]
    
    def to_gemini(self) -> List[Dict[str, Any]]:
        """Convert to Google Gemini format"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool_parameters_to_gemini(tool.parameters)
            }
            for tool in self._tools.values()
        ]
    
    def to_ollama(self) -> List[Dict[str, Any]]:
        """Convert to Ollama format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self._tools.values()
        ]
    
    def validate_call(self, name: str, arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate tool call arguments"""
        tool = self._tools.get(name)
        if not tool:
            return False, f"Tool not found: {name}"
        
        # Check required parameters
        required = tool.parameters.get("required", [])
        for param in required:
            if param not in arguments:
                return False, f"Missing required parameter: {param}"
        
        # Check parameter types
        properties = tool.parameters.get("properties", {})
        for key, value in arguments.items():
            if key in properties:
                expected_type = properties[key].get("type")
                if expected_type and not validate_type(value, expected_type):
                    return False, f"Invalid type for {key}: expected {expected_type}"
        
        return True, None
    
    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool"""
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        if not tool.handler:
            raise ValueError(f"Tool has no handler: {name}")
        
        # Validate first
        is_valid, error = self.validate_call(name, arguments)
        if not is_valid:
            raise ValueError(f"Validation failed: {error}")
        
        return tool.handler(**arguments)


def tool_parameters_to_gemini(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Convert parameters to Gemini format"""
    # Gemini uses slightly different format
    result = {
        "type": "object",
        "properties": {},
        "required": parameters.get("required", [])
    }
    
    for key, prop in parameters.get("properties", {}).items():
        result["properties"][key] = {
            "type": prop.get("type", "string"),
            "description": prop.get("description", "")
        }
        if "enum" in prop:
            result["properties"][key]["enum"] = prop["enum"]
    
    return result


def validate_type(value: Any, expected_type: str) -> bool:
    """Validate value matches expected type"""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict
    }
    
    expected = type_map.get(expected_type)
    if expected is None:
        return True  # Unknown type, allow
    
    return isinstance(value, expected)


# Convenience decorator
def tool(name: str, description: str, parameters: Dict[str, Any]):
    """Decorator to define a tool"""
    registry = ToolRegistry()
    return registry.register_decorator(name, description, parameters)
