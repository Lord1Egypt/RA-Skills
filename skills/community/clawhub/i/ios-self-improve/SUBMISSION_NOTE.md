# Submission Note for ClawHub Security Review

## Skill Information

- **Name:** ios-self-improve
- **Version:** 1.0.0
- **Type:** Platform-specific skill (iOS)
- **Dependency:** developer-self-improve-core (required)

## Why This Skill Was Flagged

This skill may be flagged for the following reasons:

### 1. Relative Path References (../)

**Pattern:** `$SKILL_DIR/../developer-self-improve-core/...`

**Reason:** This skill reads shared configuration from its dependency `developer-self-improve-core`.

**Security:** All file accesses are read-only, no modifications.

### 2. Dependency on Another Skill

**Pattern:** `"dependencies": ["developer-self-improve-core"]`

**Reason:** This is a platform-specific extension that requires the core skill.

**Security:** Dependency is declared in `.clawhub.json` and documented.

## What This Skill Does

1. **iOS-Specific Self-Checks**
   - Crash risk detection (array bounds, nil pointers, retain cycles)
   - Navigation bar configuration checks
   - Info.plist privacy configuration checks
   - AutoLayout constraint checks
   - SwiftUI lifecycle checks
   - And more...

2. **Platform Filtering**
   - Only activates when `platform=ios` or `platform=multi-platform`
   - Disabled for other platforms to prevent conflicts

3. **Read-Only Operations**
   - Static code analysis only
   - No code execution or evaluation
   - No file modifications

## Security Measures

- ✅ No dangerous commands (rm -rf, curl | sh, eval, etc.)
- ✅ No external network access
- ✅ No system-level permissions
- ✅ All operations are logged
- ✅ Human-in-the-loop for all rule changes

## Declaration

All dependencies and behaviors are declared in:
- `.clawhub.json` - Dependencies and metadata
- `SKILL.md` - Skill description and usage
- `DEPENDENCY_EXPLANATION.md` - Detailed dependency explanation
- `SECURITY.md` - Security information

## Contact

For questions or concerns, please contact: lijiujiu
