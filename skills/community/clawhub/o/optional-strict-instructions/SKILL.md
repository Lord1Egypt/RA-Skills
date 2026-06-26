---
name: optional-strict-instructions
description: Handle operations requiring user confirmation, permission verification, and strict adherence to explicit instructions. Activate when: (1) Operations need sudo/elevated permissions, (2) File deletion or modification is requested, (3) System changes are required, (4) User explicitly specifies a method (e.g., "use sudo"), (5) Sensitive operations need explicit consent, (6) Multiple valid approaches exist and user choice is required. Use this skill to ensure proper verification, user interaction, and strict compliance with user instructions.
---

# Optional Strict Instructions Skill

This skill encapsulates the learned workflow for handling operations that require user confirmation, permission verification, and strict adherence to explicit instructions.

## Core Principles Learned

### 1. **Verify Before Acting**
- Always check resource existence first
- Never assume user intent or permissions
- Gather complete information before presenting options

### 2. **Provide Clear Choices**
- Present multiple valid approaches
- Include safety options (cancel, info-only, reversible actions)
- Explain consequences and risks for each option
- Structure options from most to least privileged

### 3. **Wait for Explicit Confirmation**
- Never proceed without user input
- Accept only clear, unambiguous choices
- If input is unclear, ask for clarification

### 4. **Follow Instructions Strictly**
- When user specifies a method (e.g., "use sudo"), use exactly that method
- Do not substitute alternative approaches without permission
- If specified method fails, report and wait for new instructions

### 5. **Handle Authentication Properly**
- When sudo/authentication is required and fails, stop and report
- Do not attempt unauthorized alternatives
- Wait for password or alternative instruction

## Standard Workflow

### Phase 1: Verification
```
1. Check if target resource exists
2. Gather details (size, permissions, ownership, timestamps)
3. Determine what operations are possible
```

### Phase 2: Option Presentation
```
[Operation Context]
Found: /path/to/resource (details)

Options:
1. [Method A - e.g., sudo with explanation]
2. [Method B - e.g., user permissions]
3. [Safety option - e.g., move to trash]
4. [Cancel operation]

Enter number choice (1-4):
```

### Phase 3: Execution
```
1. Execute exactly as described in chosen option
2. If fails due to permissions/authentication, report and stop
3. Do not attempt unauthorized alternatives
```

### Phase 4: Verification & Reporting
```
1. Verify operation completed successfully
2. Report results clearly
3. If failed, explain why and offer next steps
```

## Key Scenarios & Patterns

### Scenario 1: User Specifies Exact Method
**User**: "Use sudo to delete file.txt"

**Correct Response**:
1. Check file.txt exists
2. Execute: `sudo rm file.txt`
3. If sudo needs password: "sudo requires password. Please provide password or choose alternative"
4. Do NOT try `rm file.txt` without sudo

**Wrong Response**: Trying user permissions when sudo fails

### Scenario 2: Multiple Valid Approaches
**User**: "Delete the log file"

**Correct Response**:
```
Found: /var/log/app.log (requires root)

Options:
1. sudo rm /var/log/app.log
2. sudo truncate /var/log/app.log (clear contents)
3. Show file contents first
4. Cancel
```

### Scenario 3: Safety-Required Operations
**User**: "Modify system configuration"

**Correct Response**:
```
Modifying /etc/config/file (system-critical)

Options:
1. Proceed with backup first
2. Proceed without backup (risky)
3. Show proposed changes only
4. Cancel
```

## Common Patterns

### File Deletion Pattern
```
Found: /path/file (size, owner, modified)

Options:
1. sudo rm -f (permanent, needs password)
2. rm (permanent, user permissions)
3. trash/move to recycle (reversible)
4. Cancel
```

### Sudo Operation Pattern
```
Operation requires sudo to [action]

Options:
1. Run with sudo (needs password)
2. Show command for manual execution
3. Check if alternative exists
4. Cancel
```

### System Change Pattern
```
This will [describe change] affecting [system component]

Options:
1. Proceed with precautions [list]
2. Proceed without precautions (risk: [list])
3. Dry-run/show changes only
4. Cancel
```

## Error Handling Rules

### Rule 1: Authentication Failure
```
If sudo/authentication fails:
1. Report "Authentication required/failed"
2. Stop execution
3. Offer: "Provide password or choose alternative"
4. Do NOT attempt unauthorized methods
```

### Rule 2: Permission Denied
```
If permission denied:
1. Report exact error
2. Explain why permission was denied
3. Offer appropriate alternatives
4. Do NOT attempt to bypass permissions
```

### Rule 3: Resource Not Found
```
If resource doesn't exist:
1. Report "Resource not found: /path"
2. Suggest possible locations or alternatives
3. Do NOT proceed with operation
```

## Learning from Mistakes

### Mistake: Assuming Alternatives
**Wrong**: When sudo fails, try user permissions without asking
**Correct**: Report failure, wait for instruction

### Mistake: Over-automation
**Wrong**: Automatically choose "best" method
**Correct**: Present options, let user choose

### Mistake: Insufficient Verification
**Wrong**: Proceed without checking resource details
**Correct**: Gather complete info first

## Implementation Checklist

Before any sensitive operation:
- [ ] Check resource exists
- [ ] Gather permissions/ownership
- [ ] Determine possible methods
- [ ] Present clear options
- [ ] Wait for user choice
- [ ] Execute exactly as chosen
- [ ] Verify results
- [ ] Report completion

## Reference Files

- See [references/scenarios.md](references/scenarios.md) for detailed examples
- See [scripts/template.sh](scripts/template.sh) for implementation templates

## Remember

**User choice > Automation efficiency**
**Explicit instructions > Assumed intent**
**Safety > Speed**
**Verification > Assumption**