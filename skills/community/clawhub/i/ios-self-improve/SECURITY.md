# Security Information

## Safety Features

This skill implements the following safety measures:

1. **Platform-Safe Operations**
   - Only activates when platform=ios or platform=multi-platform
   - Disabled for other platforms to prevent conflicts

2. **Dependency Validation**
   - Requires developer-self-improve-core as dependency
   - Validates dependency before execution

3. **Code Analysis (Read-Only)**
   - Static code analysis only (no modifications)
   - No code execution or evaluation

4. **Transparent Checks**
   - All check results are logged
   - Users can review all findings

## Permissions

This skill requires:
- Read/write access to its own directory
- Read access to developer-self-improve-core configuration
- No external network access
- No system-level permissions

## Dependencies

- developer-self-improve-core (required)
- bash (standard shell)
- find (standard utility)
- grep (standard utility)

No external or untrusted dependencies.

## Contact

For security concerns, please contact: lijiujiu
