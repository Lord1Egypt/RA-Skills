/**
 * End-to-end tests for complete heartbeat-cron workflow
 */

import { describe, test, expect, beforeEach, afterAll } from '@jest/globals';
import { writeFileSync, readFileSync, mkdirSync, rmSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parseFrontmatter, validateHeartbeatConfig, loadFixture } from '../test-helpers.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const e2eWorkspace = join(__dirname, '../../e2e-workspace');

describe('E2E Complete Workflow', () => {
  beforeEach(() => {
    // Clean up e2e workspace
    if (existsSync(e2eWorkspace)) {
      rmSync(e2eWorkspace, { recursive: true, force: true });
    }
    mkdirSync(e2eWorkspace, { recursive: true });
  });
  
  afterAll(() => {
    // Clean up after all E2E tests
    if (existsSync(e2eWorkspace)) {
      rmSync(e2eWorkspace, { recursive: true, force: true });
    }
  });
  
  describe('Scenario 1: GitHub Issue Triage Bot', () => {
    test('should complete full workflow from interview to heartbeat creation', () => {
      // Step 1: User interview simulation
      const interview = {
        goal: 'Auto-triage incoming GitHub issues',
        details: {
          repo: 'myorg/myrepo',
          tools: ['gh CLI'],
          schedule: { type: 'interval', value: '30m' },
          timeout: '10m'
        },
        delivery: {
          type: 'slack',
          webhookEnv: 'SLACK_WEBHOOK_URL'
        },
        credentials: ['SLACK_WEBHOOK_URL', 'GITHUB_TOKEN']
      };
      
      // Step 2: Generate heartbeat
      const heartbeatContent = `---
interval: ${interview.details.schedule.value}
timeout: ${interview.details.timeout}
agent: claude-code
name: Issue Triage Bot
description: Auto-label and triage GitHub issues
---

Check for new unlabeled issues on ${interview.details.repo}:
\`gh issue list --state open --json number,title,body,labels --jq '.[] | select(.labels | length == 0)'\`

For each unlabeled issue:
1. Read title and body
2. Determine category: bug, feature, question, or security
3. Apply label: \`gh issue edit {number} --add-label {category}\`

If security issue detected, notify via Slack:
\`curl -X POST -H 'Content-Type: application/json' -d '{"text":"🚨 Security issue #{number}: {title}"}' $${interview.delivery.webhookEnv}\`

Respond HEARTBEAT_OK if no unlabeled issues.`;
      
      // Step 3: Write heartbeat file
      const heartbeatPath = join(e2eWorkspace, 'HEARTBEAT.md');
      writeFileSync(heartbeatPath, heartbeatContent);
      
      // Step 4: Validate heartbeat
      expect(existsSync(heartbeatPath)).toBe(true);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.interval).toBe('30m');
      expect(parsed.frontmatter.timeout).toBe('10m');
      expect(parsed.frontmatter.agent).toBe('claude-code');
      expect(parsed.frontmatter.name).toBe('Issue Triage Bot');
      
      // Step 5: Validate configuration
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
      expect(validation.errors).toHaveLength(0);
      
      // Step 6: Validate body content
      expect(parsed.body).toContain('gh issue list');
      expect(parsed.body).toContain('HEARTBEAT_OK');
      expect(parsed.body).toContain('SLACK_WEBHOOK_URL');
      
      // Step 7: Generate murmur commands
      const initCommand = `murmur init ${e2eWorkspace}`;
      const testCommand = `murmur beat ${e2eWorkspace}`;
      const startCommand = 'murmur start';
      
      expect(initCommand).toContain('murmur init');
      expect(testCommand).toContain('murmur beat');
      expect(startCommand).toBe('murmur start');
    });
  });
  
  describe('Scenario 2: Endpoint Uptime Monitor', () => {
    test('should complete full workflow for uptime monitoring', () => {
      const interview = {
        goal: 'Monitor API endpoint uptime and latency',
        details: {
          endpoints: [
            'https://api.example.com/health',
            'https://api.example.com/status'
          ],
          schedule: { type: 'interval', value: '15m' },
          latencyThreshold: '2s'
        },
        delivery: {
          type: 'ntfy',
          topic: 'my-service-alerts'
        }
      };
      
      const heartbeatContent = `---
interval: ${interview.details.schedule.value}
name: Uptime Monitor
description: Monitor API endpoints for availability and latency
---

Check endpoint health and latency:

For ${interview.details.endpoints[0]}:
\`curl -s -o /dev/null -w "%{http_code} %{time_total}" ${interview.details.endpoints[0]}\`

For ${interview.details.endpoints[1]}:
\`curl -s -o /dev/null -w "%{http_code} %{time_total}" ${interview.details.endpoints[1]}\`

If any endpoint returns non-200 or latency > ${interview.details.latencyThreshold}:
\`curl -d "ALERT: Endpoint down or slow" ntfy.sh/${interview.delivery.topic}\`

Log every check to uptime.csv:
\`echo "$(date -Iseconds),endpoint,status,latency" >> uptime.csv\`

Respond HEARTBEAT_OK if all endpoints healthy.`;
      
      const heartbeatPath = join(e2eWorkspace, 'HEARTBEAT.md');
      writeFileSync(heartbeatPath, heartbeatContent);
      
      expect(existsSync(heartbeatPath)).toBe(true);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.interval).toBe('15m');
      expect(parsed.frontmatter.name).toBe('Uptime Monitor');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
      
      // Verify body contains required elements
      expect(parsed.body).toContain('curl');
      expect(parsed.body).toContain('ntfy.sh');
      expect(parsed.body).toContain('uptime.csv');
    });
  });
  
  describe('Scenario 3: Daily Research Digest', () => {
    test('should complete full workflow for research aggregation', () => {
      const interview = {
        goal: 'Daily digest of AI papers from arxiv',
        details: {
          topics: ['machine learning', 'natural language processing', 'computer vision'],
          schedule: { 
            type: 'cron', 
            value: '0 8 * * *',
            tz: 'America/New_York'
          },
          maxPapers: 10
        },
        delivery: {
          type: 'file',
          path: 'papers.md'
        },
        agent: 'claude-code',
        model: 'opus'
      };
      
      const heartbeatContent = `---
cron: "${interview.details.schedule.value}"
tz: ${interview.details.schedule.tz}
agent: ${interview.agent}
model: ${interview.model}
name: Arxiv AI Digest
description: Daily digest of AI papers from arxiv
---

Search arxiv for recent papers about: ${interview.details.topics.join(', ')}.

API: \`curl -s "http://export.arxiv.org/api/query?search_query=all:${interview.details.topics[0]}&sortBy=submittedDate&sortOrder=descending&max_results=${interview.details.maxPapers}"\`

For each paper:
1. Extract title, authors, abstract, and link
2. Filter for relevance to AI/ML
3. Create one-sentence summary

Append to ${interview.delivery.path} with today's date header:

\`\`\`
## $(date +%Y-%m-%d)

- **Title** - Authors
  - Summary
  - [Link](url)
\`\`\`

Respond HEARTBEAT_OK if no relevant papers found.`;
      
      const heartbeatPath = join(e2eWorkspace, 'HEARTBEAT.md');
      writeFileSync(heartbeatPath, heartbeatContent);
      
      expect(existsSync(heartbeatPath)).toBe(true);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.cron).toBe('0 8 * * *');
      expect(parsed.frontmatter.tz).toBe('America/New_York');
      expect(parsed.frontmatter.agent).toBe('claude-code');
      expect(parsed.frontmatter.model).toBe('opus');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
      
      expect(parsed.body).toContain('arxiv');
      expect(parsed.body).toContain('papers.md');
    });
  });
  
  describe('Scenario 4: Multi-Heartbeat Repository', () => {
    test('should create multiple named heartbeats in same workspace', () => {
      // Create heartbeats directory structure
      const issueWorkerDir = join(e2eWorkspace, 'heartbeats', 'issue-worker');
      const deployMonitorDir = join(e2eWorkspace, 'heartbeats', 'deploy-monitor');
      const ciDigestDir = join(e2eWorkspace, 'heartbeats', 'ci-digest');
      
      mkdirSync(issueWorkerDir, { recursive: true });
      mkdirSync(deployMonitorDir, { recursive: true });
      mkdirSync(ciDigestDir, { recursive: true });
      
      // Heartbeat 1: Issue Worker
      const issueWorkerContent = `---
interval: 30m
agent: claude-code
name: Issue Worker
---

Check and triage GitHub issues.`;
      
      writeFileSync(join(issueWorkerDir, 'HEARTBEAT.md'), issueWorkerContent);
      
      // Heartbeat 2: Deploy Monitor
      const deployMonitorContent = `---
cron: "0 9 * * 1-5"
tz: America/New_York
agent: claude-code
name: Deploy Monitor
---

Monitor deployment status during business hours.`;
      
      writeFileSync(join(deployMonitorDir, 'HEARTBEAT.md'), deployMonitorContent);
      
      // Heartbeat 3: CI Digest
      const ciDigestContent = `---
interval: 1h
agent: claude-code
name: CI Digest
---

Check CI build status and report failures.`;
      
      writeFileSync(join(ciDigestDir, 'HEARTBEAT.md'), ciDigestContent);
      
      // Verify all heartbeats exist
      expect(existsSync(join(issueWorkerDir, 'HEARTBEAT.md'))).toBe(true);
      expect(existsSync(join(deployMonitorDir, 'HEARTBEAT.md'))).toBe(true);
      expect(existsSync(join(ciDigestDir, 'HEARTBEAT.md'))).toBe(true);
      
      // Validate each heartbeat
      const issueWorkerParsed = parseFrontmatter(
        readFileSync(join(issueWorkerDir, 'HEARTBEAT.md'), 'utf-8')
      );
      const deployMonitorParsed = parseFrontmatter(
        readFileSync(join(deployMonitorDir, 'HEARTBEAT.md'), 'utf-8')
      );
      const ciDigestParsed = parseFrontmatter(
        readFileSync(join(ciDigestDir, 'HEARTBEAT.md'), 'utf-8')
      );
      
      expect(issueWorkerParsed.frontmatter.interval).toBe('30m');
      expect(deployMonitorParsed.frontmatter.cron).toBe('0 9 * * 1-5');
      expect(ciDigestParsed.frontmatter.interval).toBe('1h');
      
      // All should be valid
      expect(validateHeartbeatConfig(issueWorkerParsed.frontmatter).isValid).toBe(true);
      expect(validateHeartbeatConfig(deployMonitorParsed.frontmatter).isValid).toBe(true);
      expect(validateHeartbeatConfig(ciDigestParsed.frontmatter).isValid).toBe(true);
    });
  });
  
  describe('Scenario 5: Codex Architecture Review', () => {
    test('should create Codex-specific heartbeat with sandbox config', () => {
      const interview = {
        goal: 'Weekly architecture review using Codex',
        details: {
          schedule: { type: 'cron', value: '0 6 * * 1' },
          timeout: '15m',
          sandbox: 'workspace-write',
          networkAccess: true
        },
        delivery: {
          type: 'file',
          path: 'docs/architecture-review.md'
        }
      };
      
      const heartbeatContent = `---
cron: "${interview.details.schedule.value}"
agent: codex
sandbox: ${interview.details.sandbox}
networkAccess: ${interview.details.networkAccess}
timeout: ${interview.details.timeout}
name: Architecture Review
description: Weekly architecture review with Codex
---

You are Martin Fowler. Review this codebase:

1. Read all source files
2. Trace dependency graph
3. Identify architecture smells
4. Evaluate module boundaries

Write detailed review to ${interview.delivery.path}:
- Specific file references
- Concrete refactoring recommendations
- Architecture health rating (1-10)

Respond HEARTBEAT_OK when done.`;
      
      const heartbeatPath = join(e2eWorkspace, 'HEARTBEAT.md');
      writeFileSync(heartbeatPath, heartbeatContent);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.agent).toBe('codex');
      expect(parsed.frontmatter.sandbox).toBe('workspace-write');
      expect(parsed.frontmatter.networkAccess).toBe(true);
      expect(parsed.frontmatter.timeout).toBe('15m');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
  });
  
  describe('Scenario 6: Pi Browser Automation', () => {
    test('should create Pi-specific heartbeat with browser session', () => {
      const interview = {
        goal: 'Monitor web dashboard for status changes',
        details: {
          schedule: { type: 'interval', value: '1h' },
          session: 'dashboard-session',
          urls: ['https://dashboard.example.com/status']
        },
        delivery: {
          type: 'telegram',
          tokenEnv: 'TELEGRAM_TOKEN',
          chatIdEnv: 'TELEGRAM_CHAT_ID'
        }
      };
      
      const heartbeatContent = `---
interval: ${interview.details.schedule.value}
agent: pi
session: ${interview.details.session}
name: Dashboard Monitor
description: Monitor web dashboard using Pi browser
---

Use Pi browser extension to check: ${interview.details.urls[0]}

Look for status indicators and alerts.

If status changed or alert found, send Telegram message:
\`curl -s "https://api.telegram.org/bot$${interview.delivery.tokenEnv}/sendMessage" -d "chat_id=$${interview.delivery.chatIdEnv}&text=Dashboard alert"\`

Respond HEARTBEAT_OK if no changes.`;
      
      const heartbeatPath = join(e2eWorkspace, 'HEARTBEAT.md');
      writeFileSync(heartbeatPath, heartbeatContent);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.agent).toBe('pi');
      expect(parsed.frontmatter.session).toBe('dashboard-session');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
  });
});
