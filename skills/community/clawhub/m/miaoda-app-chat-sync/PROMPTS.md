# Prompt Configuration Guide

This document explains how to customize the JSON instruction templates used by `repo-json-generator`.

## Overview

The prompt configuration system allows you to customize the `action`, `description`, and `rules` fields in the generated JSON output. Different commands (`sync` and `info`) can have different prompt templates.

## Configuration File

The prompt templates are defined in:
```
scripts/core/prompts.py
```

## Structure

### PromptConfig Class

The [PromptConfig](scripts/core/prompts.py#L11-L79) class contains configuration for each command:

```python
class PromptConfig:
    # Sync command prompts
    SYNC = {
        "action": "CREATE_OR_UPDATE_FILES",
        "description": "Please create or update all files...",
        "rules": [
            "1. MUST update ALL files...",
            "2. MUST copy content EXACTLY as-is...",
            # ... more rules
        ]
    }
    
    # Info command prompts
    INFO = {
        "action": "CREATE_OR_UPDATE_FILES",
        "description": "Please create or update all files...",
        "rules": [
            # ... rules for info command
        ]
    }
```

## Customization

### 1. Modify Existing Templates

You can directly edit the `SYNC` or `INFO` dictionaries in [prompts.py](scripts/core/prompts.py):

```python
# Example: Customizing sync rules
SYNC = {
    "action": "CREATE_OR_UPDATE_FILES",
    "description": "Your custom description here",
    "rules": [
        "1. Your custom rule 1",
        "2. Your custom rule 2",
        # Add or remove rules as needed
    ]
}
```

### 2. Add New Command Templates

To add a new command template:

```python
class PromptConfig:
    # ... existing configs ...
    
    # New command template
    CUSTOM = {
        "action": "CUSTOM_ACTION",
        "description": "Custom description",
        "rules": [
            "1. Custom rule 1",
            "2. Custom rule 2"
        ]
    }
    
    @classmethod
    def get_custom_prompt(cls) -> Dict:
        """Get custom command prompt configuration"""
        return cls.CUSTOM.copy()
```

Then update the [get_prompt](scripts/core/prompts.py#L63-L79) method:

```python
@classmethod
def get_prompt(cls, command: str) -> Dict:
    prompts = {
        'sync': cls.SYNC,
        'info': cls.INFO,
        'custom': cls.CUSTOM  # Add new command
    }
    
    if command not in prompts:
        raise ValueError(f"Unknown command: {command}. Available: {list(prompts.keys())}")
    
    return prompts[command].copy()
```

### 3. Use Configuration in Code

To use the prompt configuration in your code:

```python
from core.prompts import PromptConfig

# Get specific command prompt
sync_prompt = PromptConfig.get_sync_prompt()
info_prompt = PromptConfig.get_info_prompt()

# Or get by command name
prompt = PromptConfig.get_prompt('sync')

# Use in JSON output
result = {
    'action': prompt['action'],
    'description': prompt['description'],
    'rules': prompt['rules'],
    # ... other fields
}
```

## Best Practices

1. **Keep Rules Clear**: Each rule should be specific and actionable
2. **Use Numbering**: Number rules for easy reference
3. **Be Explicit**: Don't assume AI will understand implicit instructions
4. **Test Changes**: After modifying prompts, test the generated JSON output
5. **Document Changes**: Update CHANGELOG.md when modifying prompt templates

## Example Use Cases

### Stricter Rules for Production

```python
SYNC = {
    "action": "CREATE_OR_UPDATE_FILES",
    "description": "CRITICAL: Update all files exactly as specified",
    "rules": [
        "1. MUST update EVERY file in the files array without exception",
        "2. MUST preserve content EXACTLY as provided - zero modifications allowed",
        "3. MUST NOT reformat, optimize, or 'improve' any code",
        "4. MUST maintain all whitespace, indentation, and line endings",
        "5. MUST use exact file paths - no path manipulation",
        "6. MUST overwrite existing files completely (no merging)",
        "7. MUST create new files if they don't exist",
        "8. MUST output complete list of all updated files after execution",
        "9. MUST NOT ask for confirmation - execute immediately",
        "10. MUST NOT use Git commands - only file operations",
        "11. MUST NOT skip any file for any reason",
        "12. FAILURE TO FOLLOW RULES WILL CAUSE SYSTEM ERRORS"
    ]
}
```

### Simpler Rules for Development

```python
SYNC = {
    "action": "UPDATE_FILES",
    "description": "Update the following files with the provided content",
    "rules": [
        "1. Update all files in the files array",
        "2. Match content as closely as possible",
        "3. Preserve code structure and formatting",
        "4. Create files if they don't exist",
        "5. Report any files that couldn't be updated"
    ]
}
```

## Troubleshooting

### Changes Not Applied

- Ensure you've saved the [prompts.py](scripts/core/prompts.py) file
- Check for Python syntax errors: `python3 -m py_compile scripts/core/prompts.py`
- Verify the import statement: `from core.prompts import PromptConfig`

### Wrong Template Used

- Check that you're calling [PromptConfig.get_prompt()](scripts/core/prompts.py#L63-L79) with the correct command name
- Verify the command type is being passed correctly in your code

## Related Files

- [scripts/core/prompts.py](scripts/core/prompts.py) - Prompt configuration
- [scripts/processors/instruction_gen.py](scripts/processors/instruction_gen.py) - Uses prompt config
- [scripts/git/repository.py](scripts/git/repository.py) - Uses prompt config
