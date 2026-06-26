# Dependency Explanation

## Required Dependency

This skill requires `developer-self-improve-core` as a mandatory dependency.

## Why This Dependency?

`ios-self-improve` is a platform-specific skill that provides iOS-specific self-checks and rules. It depends on `developer-self-improve-core` for:

1. **Core Self-Improvement Logic**
   - Rule proposal generation
   - Rule confirmation workflow
   - Memory management

2. **Platform Configuration**
   - Shared configuration file (`config.yaml`)
   - Platform switching (ios/android/flutter/etc.)

## How Dependency Is Used

This skill reads the platform configuration from `developer-self-improve-core`:

```bash
# Read platform configuration
AUTO_CONFIG="$SKILL_DIR/../developer-self-improve-core/config/config.yaml"
PLATFORM=$(grep "^platform:" "$AUTO_CONFIG" | cut -d: -f2)

# Call core skill for rule generation
"$SKILL_DIR/../developer-self-improve-core/scripts/developer-self-improve-core.sh" post-check "$content" "$scene"
```

## Security Notes

- All file accesses are read-only
- No external network calls
- No system-level operations
- All operations are logged

## Declared In

This dependency is declared in:
- `.clawhub.json` → `"dependencies": ["developer-self-improve-core"]`
- `SKILL.md` → "依赖：developer-self-improve-core（必须启用）"
