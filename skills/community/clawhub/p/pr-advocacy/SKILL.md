# PR Advocacy Skill

## Purpose
Actively monitor, respond to, and drive Pull Request reviews to completion. This skill ensures PRs don't get stuck in review limbo and addresses maintainer feedback promptly.

## Core Responsibilities

### 1. PR Status Monitoring
- Check PR status every heartbeat cycle (1 hour)
- Monitor CI/CD check results
- Track reviewer comments and requested changes
- Identify blocking vs non-blocking feedback

### 2. Professional Response Protocol
- Acknowledge all reviewer feedback within 24 hours
- Provide clear, technical responses to questions
- Implement requested changes promptly when valid
- Politely justify decisions when disagreeing with feedback

### 3. Proactive Issue Resolution
- Fix CI/CD failures immediately
- Address merge conflicts proactively  
- Update documentation when code changes
- Add tests for edge cases identified by reviewers

### 4. PR Health Assessment
- **Green Status**: All checks pass, no pending reviews → Wait for merge
- **Yellow Status**: Minor feedback, passing checks → Respond and wait
- **Red Status**: Failing checks or major feedback → Immediate action required
- **Stale Status**: No activity for 48+ hours → Gentle ping to reviewers

## PR Status Processing Rules

### OPEN State Handling
When a PR is in OPEN state:
- **Check for maintainer/reviewer comments** pointing out issues
- **If feedback requires changes**:
  - Analyze the specific feedback content
  - Create fixes according to maintainer suggestions
  - Automatically commit changes to the PR branch
  - Update PR description if needed
  - Record fix details for learning
- **If no issues found**:
  - Continue monitoring CI/CD status
  - Wait for merge approval

### CLOSED/REJECTED State Handling  
When a PR is CLOSED or REJECTED:
- **Immediately remove from active tracking list**
- **Stop all monitoring activities** for this PR
- **Record closure reason** for future learning and improvement
- **Do not attempt to resubmit** unless explicitly instructed

### MERGED State Handling
When a PR is successfully MERGED:
- **Remove from active tracking list**
- **Add to merged records** for success tracking
- **Celebrate the contribution!**
- **Update skills and workflows** based on successful patterns

## Real-time Tracking List Synchronization

### Automatic Updates
- **After any PR status change**, immediately update the tracking list file
- **When PRs are added/removed**, synchronize the tracking list in real-time
- **Prevent information loss** by ensuring all changes are persisted to disk
- **Maintain accurate state** by writing updates immediately after processing

### Tracking List File Management
- **Location**: `/Users/hope/.openclaw/agents/coding/workspace/memory/pr-tracking-list.md`
- **Format**: Markdown with clear sections for active, closed, and merged PRs
- **Updates**: Atomic writes to prevent corruption during concurrent access
- **Backup**: Maintain version history through git commits for rollback capability

### Synchronization Workflow
1. **Detect PR status change** (OPEN/CLOSED/MERGED)
2. **Process the change** according to status rules
3. **Update tracking list file** immediately with new state
4. **Verify file integrity** to ensure no data loss
5. **Log the update** for audit trail and debugging

### Error Handling
- **File write failures**: Retry with exponential backoff
- **Concurrent access**: Use atomic file operations to prevent race conditions
- **Data corruption**: Validate file format before and after updates
- **Recovery**: Maintain backup copies for emergency restoration

## Implementation Guidelines

### Check Status Analysis
```bash
# Check PR status and checks
gh pr view <PR_NUMBER> --json statusCheckRollup,reviewDecision

# Common check statuses:
# - SUCCESS: All good
# - FAILURE: Needs immediate fixing  
# - PENDING: Still running
# - NEUTRAL: Non-blocking (like coverage)
```

### Reviewer Feedback Response Template
```
Thanks for the review! 

For [specific comment]:
- [Action taken or explanation]
- [Technical justification if disagreeing]

I've [implemented the change / pushed an update / clarified the approach] in [commit reference].

Let me know if you need any additional changes!
```

### Common PR Issues & Solutions

#### CI/CD Failures
- **Lint errors**: Run `npm run lint -- --fix` locally first
- **Test failures**: Reproduce locally, add missing test cases
- **Build errors**: Verify dependencies, check Node.js version compatibility

#### Code Review Feedback  
- **Style issues**: Follow project's `.editorconfig` and style guide
- **Architecture concerns**: Reference existing patterns in codebase
- **Security concerns**: Prioritize security fixes, add validation layers

#### Documentation Gaps
- **Missing docs**: Add/update relevant documentation files
- **Inconsistent formatting**: Use project's markdown template
- **Outdated examples**: Update code examples to match new implementation

## Automation Integration

### Heartbeat Integration
- Integrate with existing heartbeat monitoring system (every hour)
- Add PR status to daily summary reports
- Escalate stale PRs after 48 hours of inactivity

### Memory Tracking
- Maintain PR tracking list in workspace memory
- **Automatically clean up closed/rejected PRs** from tracking list
- **Real-time synchronization** of tracking list file after any PR status change
- Record resolution outcomes for learning
- Update core memory with successful advocacy patterns

### Automatic Response Workflow
1. **Detect feedback** on OPEN PRs
2. **Analyze requirements** and create appropriate fixes
3. **Commit changes** to existing PR branch
4. **Update tracking status** and notify maintainers
5. **Handle closure** by removing from active monitoring
6. **Synchronize tracking list file** immediately after any change

## Success Metrics

- **Response time**: < 24 hours to reviewer feedback
- **Resolution rate**: > 90% of PRs merged within 7 days  
- **Rework rate**: < 10% of PRs require major revisions after initial review
- **Maintainer satisfaction**: Positive feedback from maintainers on communication quality
- **Data integrity**: 100% tracking list accuracy with zero information loss

## Best Practices

### Communication
- Be concise but thorough in responses
- Use code blocks for technical explanations
- Reference specific line numbers when discussing changes
- Thank reviewers for their time and expertise

### Technical Excellence  
- Ensure changes are minimal and focused
- Maintain backward compatibility when possible
- Follow project conventions exactly
- Test changes thoroughly before pushing

### Professionalism
- Never argue with reviewers; seek to understand their perspective
- Admit mistakes quickly and fix them
- Offer to help with related issues when appropriate
- Celebrate successful merges and thank maintainers