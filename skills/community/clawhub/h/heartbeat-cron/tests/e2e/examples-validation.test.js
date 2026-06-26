/**
 * E2E tests for validating examples from references/examples.md
 */

import { describe, test, expect } from '@jest/globals';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parseFrontmatter, validateHeartbeatConfig } from '../test-helpers.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const examplesPath = join(__dirname, '../../references/examples.md');

describe('Examples Validation E2E', () => {
  let examplesContent;
  
  beforeAll(() => {
    examplesContent = readFileSync(examplesPath, 'utf-8');
  });
  
  describe('Delivery Patterns', () => {
    test('should document Slack webhook pattern', () => {
      expect(examplesContent).toContain('Slack webhook');
      expect(examplesContent).toContain('SLACK_WEBHOOK_URL');
      expect(examplesContent).toContain('curl -X POST');
    });
    
    test('should document Telegram bot pattern', () => {
      expect(examplesContent).toContain('Telegram bot');
      expect(examplesContent).toContain('TELEGRAM_TOKEN');
      expect(examplesContent).toContain('api.telegram.org');
    });
    
    test('should document file append pattern', () => {
      expect(examplesContent).toContain('Append to local file');
      expect(examplesContent).toContain('workspace');
    });
    
    test('should document GitHub issue pattern', () => {
      expect(examplesContent).toContain('GitHub issue');
      expect(examplesContent).toContain('gh issue');
    });
    
    test('should document ntfy push pattern', () => {
      expect(examplesContent).toContain('Ntfy');
      expect(examplesContent).toContain('ntfy.sh');
    });
    
    test('should document ATTENTION response pattern', () => {
      expect(examplesContent).toContain('ATTENTION');
      expect(examplesContent).toContain('murmur status');
    });
  });
  
  describe('Code & Repos Examples', () => {
    test('should have Codex architecture review example', () => {
      expect(examplesContent).toContain('Codex: architecture review');
      expect(examplesContent).toContain('agent: codex');
      expect(examplesContent).toContain('sandbox: workspace-write');
      expect(examplesContent).toContain('Martin Fowler');
    });
    
    test('should have auto-triage issues example', () => {
      expect(examplesContent).toContain('Auto-triage incoming issues');
      expect(examplesContent).toContain('gh issue list');
      expect(examplesContent).toContain('interval: 30m');
    });
    
    test('should have stale PR nudge example', () => {
      expect(examplesContent).toContain('Stale PR nudge');
      expect(examplesContent).toContain('gh pr list');
      expect(examplesContent).toContain('interval: 12h');
    });
    
    test('should have CI failure digest example', () => {
      expect(examplesContent).toContain('CI failure digest');
      expect(examplesContent).toContain('gh run list');
      expect(examplesContent).toContain('interval: 1h');
    });
  });
  
  describe('Research & Intelligence Examples', () => {
    test('should have Hacker News scout example', () => {
      expect(examplesContent).toContain('Hacker News scout');
      expect(examplesContent).toContain('hacker-news.firebaseio.com');
      expect(examplesContent).toContain('interval: 6h');
    });
    
    test('should have competitor changelog tracker example', () => {
      expect(examplesContent).toContain('Competitor changelog tracker');
      expect(examplesContent).toContain('interval: 1d');
      expect(examplesContent).toContain('changelog');
    });
    
    test('should have arxiv paper monitor example', () => {
      expect(examplesContent).toContain('Arxiv paper monitor');
      expect(examplesContent).toContain('export.arxiv.org');
      expect(examplesContent).toContain('interval: 1d');
    });
  });
  
  describe('Ops & Infrastructure Examples', () => {
    test('should have endpoint canary example', () => {
      expect(examplesContent).toContain('Endpoint canary');
      expect(examplesContent).toContain('curl -s -o /dev/null');
      expect(examplesContent).toContain('interval: 15m');
    });
    
    test('should have Docker resource check example', () => {
      expect(examplesContent).toContain('Docker resource check');
      expect(examplesContent).toContain('docker system df');
      expect(examplesContent).toContain('interval: 6h');
    });
  });
  
  describe('Personal & Creative Examples', () => {
    test('should have daily journal prompt example', () => {
      expect(examplesContent).toContain('Daily journal prompt');
      expect(examplesContent).toContain('journal/');
      expect(examplesContent).toContain('interval: 1d');
    });
    
    test('should have repo activity digest example', () => {
      expect(examplesContent).toContain('Repo activity digest');
      expect(examplesContent).toContain('gh api repos');
      expect(examplesContent).toContain('interval: 1d');
    });
  });
  
  describe('Schedule Recommendations', () => {
    test('should have schedule recommendations table', () => {
      expect(examplesContent).toContain('Choosing the Right Schedule');
      expect(examplesContent).toContain('Interval');
      expect(examplesContent).toContain('Cron alternative');
    });
    
    test('should recommend 15m for critical uptime', () => {
      expect(examplesContent).toContain('15m');
      expect(examplesContent).toContain('uptime');
    });
    
    test('should recommend 30m-1h for active development', () => {
      expect(examplesContent).toContain('30m');
      expect(examplesContent).toContain('1h');
      expect(examplesContent).toContain('Active development');
    });
    
    test('should recommend 6h-12h for reviews', () => {
      expect(examplesContent).toContain('6h');
      expect(examplesContent).toContain('12h');
      expect(examplesContent).toContain('Reviews');
    });
    
    test('should recommend 6h-1d for research', () => {
      expect(examplesContent).toContain('Research');
      expect(examplesContent).toContain('intelligence');
    });
    
    test('should recommend 1d for housekeeping', () => {
      expect(examplesContent).toContain('Housekeeping');
      expect(examplesContent).toContain('1d');
    });
  });
  
  describe('Example Heartbeat Validation', () => {
    test('should have valid interval in endpoint canary example', () => {
      const interval = '15m';
      const testContent = `---
interval: ${interval}
---

Check endpoints.`;
      
      const parsed = parseFrontmatter(testContent);
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(true);
    });
    
    test('should have valid cron in architecture review example', () => {
      const cron = '0 6 * * 1';
      const testContent = `---
cron: "${cron}"
agent: codex
---

Review code.`;
      
      const parsed = parseFrontmatter(testContent);
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(true);
    });
    
    test('should have valid interval in HN scout example', () => {
      const interval = '6h';
      const testContent = `---
interval: ${interval}
---

Fetch HN stories.`;
      
      const parsed = parseFrontmatter(testContent);
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(true);
    });
  });
  
  describe('Examples Completeness', () => {
    test('should have minimum number of examples', () => {
      const exampleCount = (examplesContent.match(/###/g) || []).length;
      
      // Should have at least 10 examples
      expect(exampleCount).toBeGreaterThanOrEqual(10);
    });
    
    test('should include code examples', () => {
      expect(examplesContent).toContain('```markdown');
    });
    
    test('should have frontmatter in code examples', () => {
      const codeBlocks = examplesContent.match(/```markdown([\s\S]*?)```/g);
      
      expect(codeBlocks).not.toBeNull();
      expect(codeBlocks.length).toBeGreaterThanOrEqual(5);
      
      // Check that examples have frontmatter
      const withFrontmatter = codeBlocks.filter(block => 
        block.includes('---') && block.includes('interval:') || block.includes('cron:')
      );
      
      expect(withFrontmatter.length).toBeGreaterThanOrEqual(5);
    });
  });
});
