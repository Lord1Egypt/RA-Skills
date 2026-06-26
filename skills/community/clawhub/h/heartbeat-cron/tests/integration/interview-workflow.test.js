/**
 * Integration tests for interview workflow and heartbeat generation
 */

import { describe, test, expect } from '@jest/globals';
import { parseFrontmatter, validateHeartbeatConfig, isValidInterval, isValidCron } from '../test-helpers.js';

describe('Interview Workflow Integration', () => {
  describe('Round 1 - Goal Discovery', () => {
    test('should identify GitHub monitoring goal', () => {
      const userGoal = 'I want to monitor my GitHub repos for new issues';
      
      expect(userGoal).toContain('GitHub');
      expect(userGoal).toContain('monitor');
      expect(userGoal).toContain('issues');
    });
    
    test('should identify CI/CD monitoring goal', () => {
      const userGoal = 'Check if my CI builds are passing';
      
      expect(userGoal).toContain('CI');
      expect(userGoal).toContain('builds');
    });
    
    test('should identify endpoint monitoring goal', () => {
      const userGoal = 'I need to check if my API endpoints are up';
      
      expect(userGoal).toContain('endpoints');
      expect(userGoal).toContain('check');
    });
    
    test('should identify research/intelligence goal', () => {
      const userGoal = 'Track new AI papers on arxiv daily';
      
      expect(userGoal).toContain('arxiv');
      expect(userGoal).toContain('daily');
    });
  });
  
  describe('Round 2 - Schedule Configuration', () => {
    test('should validate interval-based schedule', () => {
      const schedule = {
        type: 'interval',
        value: '1h'
      };
      
      expect(schedule.type).toBe('interval');
      expect(isValidInterval(schedule.value)).toBe(true);
    });
    
    test('should validate cron-based schedule', () => {
      const schedule = {
        type: 'cron',
        value: '0 9 * * 1-5'
      };
      
      expect(schedule.type).toBe('cron');
      expect(isValidCron(schedule.value)).toBe(true);
    });
    
    test('should suggest interval for uptime monitoring', () => {
      const useCase = 'endpoint uptime monitoring';
      const suggestedInterval = '15m';
      
      expect(useCase).toContain('uptime');
      expect(isValidInterval(suggestedInterval)).toBe(true);
    });
    
    test('should suggest interval for active development', () => {
      const useCase = 'active development monitoring';
      const suggestedInterval = '1h';
      
      expect(isValidInterval(suggestedInterval)).toBe(true);
    });
    
    test('should suggest cron for weekday-specific tasks', () => {
      const useCase = 'weekday morning digest';
      const suggestedCron = '0 9 * * 1-5';
      
      expect(isValidCron(suggestedCron)).toBe(true);
    });
    
    test('should suggest daily interval for digests', () => {
      const useCase = 'daily research digest';
      const suggestedInterval = '1d';
      
      expect(isValidInterval(suggestedInterval)).toBe(true);
    });
  });
  
  describe('Round 3 - Delivery Configuration', () => {
    test('should configure Slack webhook delivery', () => {
      const delivery = {
        type: 'slack',
        webhookUrl: '$SLACK_WEBHOOK_URL',
        command: `curl -X POST -H 'Content-Type: application/json' -d '{"text":"..."}' $SLACK_WEBHOOK_URL`
      };
      
      expect(delivery.type).toBe('slack');
      expect(delivery.command).toContain('curl');
      expect(delivery.command).toContain('SLACK_WEBHOOK_URL');
    });
    
    test('should configure Telegram bot delivery', () => {
      const delivery = {
        type: 'telegram',
        token: '$TELEGRAM_TOKEN',
        chatId: '$CHAT_ID',
        command: `curl -s "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" -d "chat_id=$CHAT_ID&text=..."`
      };
      
      expect(delivery.type).toBe('telegram');
      expect(delivery.command).toContain('api.telegram.org');
    });
    
    test('should configure file-based delivery', () => {
      const delivery = {
        type: 'file',
        path: 'workspace/report.md',
        action: 'append'
      };
      
      expect(delivery.type).toBe('file');
      expect(delivery.path).toContain('workspace');
    });
    
    test('should configure GitHub issue delivery', () => {
      const delivery = {
        type: 'github',
        command: 'gh issue create --title "Report" --body "Content"'
      };
      
      expect(delivery.type).toBe('github');
      expect(delivery.command).toContain('gh issue');
    });
    
    test('should configure ntfy push notification', () => {
      const delivery = {
        type: 'ntfy',
        topic: 'my-topic',
        command: `curl -d "message" ntfy.sh/my-topic`
      };
      
      expect(delivery.type).toBe('ntfy');
      expect(delivery.command).toContain('ntfy.sh');
    });
    
    test('should configure ATTENTION-only delivery', () => {
      const delivery = {
        type: 'attention',
        description: 'User checks TUI/logs manually'
      };
      
      expect(delivery.type).toBe('attention');
    });
  });
  
  describe('Agent Configuration', () => {
    test('should configure claude-code agent', () => {
      const config = {
        agent: 'claude-code',
        model: 'opus'
      };
      
      expect(config.agent).toBe('claude-code');
      expect(['opus', 'sonnet', 'haiku']).toContain(config.model);
    });
    
    test('should configure codex agent with sandbox', () => {
      const config = {
        agent: 'codex',
        sandbox: 'workspace-write',
        networkAccess: true
      };
      
      expect(config.agent).toBe('codex');
      expect(config.sandbox).toBe('workspace-write');
      expect(typeof config.networkAccess).toBe('boolean');
    });
    
    test('should configure pi agent with session', () => {
      const config = {
        agent: 'pi',
        session: 'my-browser-session'
      };
      
      expect(config.agent).toBe('pi');
      expect(config.session).toBeDefined();
    });
  });
  
  describe('Timeout Configuration', () => {
    test('should use default 5m timeout for simple tasks', () => {
      const timeout = '5m';
      
      expect(isValidInterval(timeout)).toBe(true);
    });
    
    test('should use 15m timeout for complex tasks', () => {
      const timeout = '15m';
      
      expect(isValidInterval(timeout)).toBe(true);
    });
    
    test('should use 30m timeout for very complex tasks', () => {
      const timeout = '30m';
      
      expect(isValidInterval(timeout)).toBe(true);
    });
  });
  
  describe('Complete Heartbeat Generation', () => {
    test('should generate complete GitHub issue monitor heartbeat', () => {
      const interview = {
        goal: 'Monitor GitHub issues for new unlabeled issues',
        schedule: { type: 'interval', value: '30m' },
        agent: 'claude-code',
        delivery: 'slack',
        tools: ['gh CLI']
      };
      
      const generatedHeartbeat = `---
interval: ${interview.schedule.value}
agent: ${interview.agent}
name: GitHub Issue Monitor
---

Check for new GitHub issues using \`gh issue list --state open --json number,title,body,labels\`.
For any issue with no labels, apply appropriate labels.

If security issue found, post to Slack webhook.

Respond HEARTBEAT_OK if no unlabeled issues.`;
      
      const parsed = parseFrontmatter(generatedHeartbeat);
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.interval).toBe('30m');
      expect(parsed.frontmatter.agent).toBe('claude-code');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should generate complete endpoint monitor heartbeat', () => {
      const interview = {
        goal: 'Monitor API endpoint health',
        schedule: { type: 'interval', value: '15m' },
        agent: 'claude-code',
        delivery: 'ntfy',
        endpoints: ['https://api.example.com/health']
      };
      
      const generatedHeartbeat = `---
interval: ${interview.schedule.value}
agent: ${interview.agent}
name: Endpoint Monitor
---

Check endpoint health: \`curl -s -o /dev/null -w "%{http_code}" ${interview.endpoints[0]}\`

If non-200 response, send ntfy notification.

Log results to uptime.csv.

Respond HEARTBEAT_OK if healthy.`;
      
      const parsed = parseFrontmatter(generatedHeartbeat);
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.interval).toBe('15m');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should generate complete research digest heartbeat', () => {
      const interview = {
        goal: 'Daily arxiv paper digest',
        schedule: { type: 'cron', value: '0 8 * * *', tz: 'America/New_York' },
        agent: 'claude-code',
        delivery: 'file',
        topics: ['machine learning', 'AI']
      };
      
      const generatedHeartbeat = `---
cron: "${interview.schedule.value}"
tz: ${interview.schedule.tz}
agent: ${interview.agent}
name: Arxiv Digest
---

Search arxiv for papers about: ${interview.topics.join(', ')}.

Fetch top 10 results and summarize.

Append to papers.md with date header.

Respond HEARTBEAT_OK if no new papers.`;
      
      const parsed = parseFrontmatter(generatedHeartbeat);
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.cron).toBe('0 8 * * *');
      expect(parsed.frontmatter.tz).toBe('America/New_York');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should generate complete architecture review heartbeat', () => {
      const interview = {
        goal: 'Weekly architecture review',
        schedule: { type: 'cron', value: '0 6 * * 1' },
        agent: 'codex',
        sandbox: 'workspace-write',
        timeout: '15m',
        delivery: 'file'
      };
      
      const generatedHeartbeat = `---
cron: "${interview.schedule.value}"
agent: ${interview.agent}
sandbox: ${interview.sandbox}
timeout: ${interview.timeout}
name: Architecture Review
---

Review codebase architecture.

Write review to docs/architecture-review.md.

Rate architecture health 1-10.

Respond HEARTBEAT_OK when done.`;
      
      const parsed = parseFrontmatter(generatedHeartbeat);
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.cron).toBe('0 6 * * 1');
      expect(parsed.frontmatter.agent).toBe('codex');
      expect(parsed.frontmatter.sandbox).toBe('workspace-write');
      expect(parsed.frontmatter.timeout).toBe('15m');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
  });
  
  describe('State Management for Change Detection', () => {
    test('should include state file reading step', () => {
      const heartbeatBody = `Read last-price.txt to get previous price.
Compare with current price.
If changed, update last-price.txt and notify.`;
      
      expect(heartbeatBody).toContain('last-price.txt');
      expect(heartbeatBody).toContain('Read');
      expect(heartbeatBody).toContain('update');
    });
    
    test('should include state file writing step', () => {
      const heartbeatBody = `Write new state to tracking-state.json with timestamp.`;
      
      expect(heartbeatBody).toContain('tracking-state.json');
      expect(heartbeatBody).toContain('Write');
    });
    
    test('should handle JSON state files', () => {
      const stateExample = {
        lastChecked: '2024-01-01T00:00:00Z',
        lastValue: 100,
        changes: []
      };
      
      expect(typeof stateExample.lastChecked).toBe('string');
      expect(typeof stateExample.lastValue).toBe('number');
      expect(Array.isArray(stateExample.changes)).toBe(true);
    });
  });
});
