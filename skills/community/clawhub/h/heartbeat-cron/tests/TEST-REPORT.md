# heartbeat-cron Test Report

**Generated:** 2026-03-22T03:07:22.962Z

---

## 📊 Summary

| Metric | Status | Value |
|--------|--------|-------|
| Test Files | ✅ | 7 test files |
| Unit Tests | ✅ | 3 files |
| Integration Tests | ✅ | 2 files |
| E2E Tests | ✅ | 2 files |
| Fixtures | ✅ | 8 files |

## 📈 Coverage Results

| Metric | Coverage | Target | Status |
|--------|----------|--------|--------|
| Lines | 98.9% | 80% | ✅ |
| Statements | 98.9% | 80% | ✅ |
| Branches | 98.97% | 80% | ✅ |
| Functions | 100% | 80% | ✅ |

## 📁 Test Structure

### Unit Tests
- **frontmatter-parser.test.js** - YAML frontmatter parsing and extraction
  - Valid frontmatter parsing
  - Boolean and numeric value handling
  - Quoted string handling
  - Comment handling
  - Error cases (missing delimiter, no frontmatter)
  
- **config-validation.test.js** - Configuration validation
  - Interval format validation (15m, 1h, 6h, 1d)
  - Cron expression validation (5-field format)
  - Timezone validation (IANA format)
  - Agent validation (claude-code, codex, pi)
  - Sandbox validation (read-only, workspace-write, danger-full-access)
  - Permissions validation (skip only)
  - Complete config validation with error reporting
  
- **skill-parser.test.js** - SKILL.md structure validation
  - Metadata validation (name, version, author)
  - Required sections (Context, Workflow, Rules)
  - Workflow steps (0-5)
  - Interview rounds (1, 1b, 2, 3, 3b)
  - Frontmatter field documentation
  - Trigger keywords
  - Code examples
  - Content quality checks

### Integration Tests
- **heartbeat-creation.test.js** - HEARTBEAT.md creation
  - Basic heartbeat creation (minimal, interval, cron, full config)
  - Named heartbeats in heartbeats/ directory
  - Multiple heartbeats support
  - Invalid heartbeat detection
  - Body content validation
  - Murmur command generation
  
- **interview-workflow.test.js** - Interview workflow
  - Goal discovery (Round 1)
  - Schedule configuration (Round 2)
  - Delivery configuration (Round 3)
  - Agent configuration
  - Timeout configuration
  - Complete heartbeat generation
  - State management for change detection

### E2E Tests
- **complete-workflow.test.js** - Full workflow scenarios
  - Scenario 1: GitHub Issue Triage Bot
  - Scenario 2: Endpoint Uptime Monitor
  - Scenario 3: Daily Research Digest
  - Scenario 4: Multi-Heartbeat Repository
  - Scenario 5: Codex Architecture Review
  - Scenario 6: Pi Browser Automation
  
- **examples-validation.test.js** - Examples validation
  - Delivery patterns (Slack, Telegram, file, GitHub, ntfy, ATTENTION)
  - Code & repos examples
  - Research & intelligence examples
  - Ops & infrastructure examples
  - Personal & creative examples
  - Schedule recommendations
  - Example completeness

## 🗂️ Test Fixtures

### Valid Heartbeats
- valid-heartbeat-interval.md - Interval-based schedule with claude-code
- valid-heartbeat-cron.md - Cron schedule with codex and timezone
- minimal-heartbeat.md - Minimal valid configuration
- full-heartbeat.md - All configuration options

### Invalid Heartbeats
- invalid-heartbeat-both-schedule.md - Both interval and cron (invalid)
- invalid-heartbeat-no-schedule.md - Missing schedule (invalid)
- invalid-heartbeat-bad-interval.md - Invalid interval format
- invalid-heartbeat-bad-cron.md - Invalid cron expression

## 🔧 Helper Functions

Test utilities in test-helpers.js:

- parseFrontmatter(content) - Parse YAML frontmatter
- isValidInterval(interval) - Validate interval format
- isValidCron(cron) - Validate cron expression
- isValidTimezone(tz) - Validate timezone
- isValidAgent(agent) - Validate agent type
- isValidSandbox(sandbox) - Validate sandbox type
- isValidPermissions(permissions) - Validate permissions
- loadFixture(filename) - Load fixture file
- validateHeartbeatConfig(frontmatter) - Complete validation

## 📋 Murmur Commands Tested

- `murmur init {path}` - Initialize workspace
- `murmur init {path} --interval 30m` - With interval
- `murmur init {path} --cron "0 9 * * 1-5"` - With cron
- `murmur init {path} --name issue-worker` - Named heartbeat
- `murmur beat {path}` - Test execution
- `murmur beat {path} --name {name}` - Named heartbeat test
- `murmur workspaces list` - List workspaces
- `murmur start` - Start daemon
- `murmur start --detach` - Background mode

## ✅ Test Coverage Areas

### Frontmatter Fields
- [x] interval
- [x] cron
- [x] tz (timezone)
- [x] timeout
- [x] agent
- [x] model
- [x] maxTurns
- [x] name
- [x] description
- [x] session (pi)
- [x] sandbox (codex)
- [x] networkAccess (codex)
- [x] permissions

### Validation Rules
- [x] Schedule required (interval or cron)
- [x] Cannot have both interval and cron
- [x] Interval format validation
- [x] Cron expression validation
- [x] Timezone format validation
- [x] Agent type validation
- [x] Sandbox type validation
- [x] Permissions validation
- [x] Timeout format validation

### Workflow Steps
- [x] Preflight (murmur check)
- [x] Interview (5 rounds)
- [x] Draft (HEARTBEAT.md creation)
- [x] Test (murmur beat)
- [x] Evaluate (user feedback)
- [x] Register (murmur init)

### Delivery Patterns
- [x] Slack webhook
- [x] Telegram bot
- [x] File append
- [x] GitHub issue
- [x] Ntfy push
- [x] ATTENTION response

## 🎯 Coverage Threshold

**Target: >80%**

Current coverage meets threshold: ✅ YES

## 📝 Recommendations

1. **Maintain Coverage**: Keep coverage above 80% as new features are added
2. **Add More E2E Scenarios**: Consider adding tests for:
   - Error handling in murmur commands
   - Network failure scenarios
   - Credential management
3. **Performance Tests**: Consider adding tests for:
   - Large heartbeat files
   - Many named heartbeats
   - Long-running workflows

---

*Report generated by generate-report.js*
