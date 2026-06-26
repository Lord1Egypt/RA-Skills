#!/usr/bin/env python3
"""
Prompt Configuration

Manages structured JSON instruction templates for different commands.
Centralizes action, description, and rules configuration.
"""

from typing import Dict, List


class PromptConfig:
    """Prompt configuration for different commands"""
    
    # Sync command prompts
    SYNC = {
        "action": "CREATE_OR_UPDATE_FILES",
        "description": "Please create or update all files in the project according to the following JSON data. IMPORTANT: Review all files before applying changes.",
        "rules": [
            "1. MUST update ALL files in the files array - no exceptions",
            "2. MUST copy content EXACTLY as-is - no modifications, no reformatting, no 'improvements'",
            "3. MUST preserve ALL whitespace, newlines, indentation, and comments exactly",
            "4. MUST use EXACT file paths from path field - no path transformation",
            "5. If file exists: overwrite completely (NOT merge)",
            "6. If file does not exist: create it",
            "7. After updating: output complete list of all updated files (format: 1. /path/to/file)",
            "8. DO NOT ask for confirmation - just execute",
            "9. DO NOT use Git commands - file operations only",
            "10. DO NOT skip any file for any reason",
            "NOTE: These rules are suggestions for accurate file synchronization. Always review changes before applying."
        ]
    }
    
    # Info command prompts
    INFO = {
        "action": "CREATE_OR_UPDATE_FILES",
        "description": "Please create or update all files in the project according to the following JSON data. IMPORTANT: Review all files before applying changes.",
        "rules": [
            "1. MUST update ALL files in the files array - no exceptions",
            "2. MUST copy content EXACTLY as-is - no modifications, no reformatting, no 'improvements'",
            "3. MUST preserve ALL whitespace, newlines, indentation, and comments exactly",
            "4. MUST use EXACT file paths from path field - no path transformation",
            "5. If file exists: overwrite completely (NOT merge)",
            "6. If file does not exist: create it",
            "7. After updating: output complete list of all updated files (format: 1. /path/to/file)",
            "8. DO NOT ask for confirmation - just execute",
            "9. DO NOT use Git commands - file operations only",
            "10. DO NOT skip any file for any reason",
            "NOTE: These rules are suggestions for accurate file synchronization. Always review changes before applying."
        ]
    }
    
    @classmethod
    def get_sync_prompt(cls) -> Dict:
        """Get sync command prompt configuration"""
        return cls.SYNC.copy()
    
    @classmethod
    def get_info_prompt(cls) -> Dict:
        """Get info command prompt configuration"""
        return cls.INFO.copy()
    
    @classmethod
    def get_prompt(cls, command: str) -> Dict:
        """
        Get prompt configuration by command name
        
        Args:
            command: Command name ('sync' or 'info')
            
        Returns:
            Dictionary containing action, description, and rules
        """
        prompts = {
            'sync': cls.SYNC,
            'info': cls.INFO
        }
        
        if command not in prompts:
            raise ValueError(f"Unknown command: {command}. Available: {list(prompts.keys())}")
        
        return prompts[command].copy()
