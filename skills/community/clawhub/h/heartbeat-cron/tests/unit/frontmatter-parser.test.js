/**
 * Unit tests for frontmatter parsing
 */

import { describe, test, expect } from '@jest/globals';
import { parseFrontmatter } from '../test-helpers.js';

describe('Frontmatter Parser', () => {
  describe('parseFrontmatter', () => {
    test('should parse valid frontmatter with interval', () => {
      const content = `---
interval: 1h
name: Test Heartbeat
---

This is the body content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result).not.toBeNull();
      expect(result.frontmatter).toEqual({
        interval: '1h',
        name: 'Test Heartbeat'
      });
      expect(result.body).toBe('This is the body content.');
    });
    
    test('should parse valid frontmatter with cron', () => {
      const content = `---
cron: "0 9 * * 1-5"
tz: America/New_York
---

Body here.`;
      
      const result = parseFrontmatter(content);
      
      expect(result).not.toBeNull();
      expect(result.frontmatter).toEqual({
        cron: '0 9 * * 1-5',
        tz: 'America/New_York'
      });
      expect(result.body).toBe('Body here.');
    });
    
    test('should parse frontmatter with boolean values', () => {
      const content = `---
networkAccess: true
permissions: skip
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.networkAccess).toBe(true);
      expect(result.frontmatter.permissions).toBe('skip');
    });
    
    test('should parse frontmatter with numeric values', () => {
      const content = `---
maxTurns: 50
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.maxTurns).toBe(50);
    });
    
    test('should parse frontmatter with quoted strings', () => {
      const content = `---
cron: "0 9 * * 1-5"
name: 'My Heartbeat'
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.cron).toBe('0 9 * * 1-5');
      expect(result.frontmatter.name).toBe('My Heartbeat');
    });
    
    test('should parse frontmatter with comments', () => {
      const content = `---
interval: 1h
# This is a comment
name: Test
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.interval).toBe('1h');
      expect(result.frontmatter.name).toBe('Test');
      expect(result.frontmatter.hasOwnProperty('comment')).toBe(false);
    });
    
    test('should handle empty body', () => {
      const content = `---
interval: 1h
---
`;
      
      const result = parseFrontmatter(content);
      
      expect(result).not.toBeNull();
      expect(result.frontmatter.interval).toBe('1h');
      expect(result.body).toBe('');
    });
    
    test('should handle multi-line body', () => {
      const content = `---
interval: 1h
---

Line 1
Line 2
Line 3`;
      
      const result = parseFrontmatter(content);
      
      expect(result.body).toContain('Line 1');
      expect(result.body).toContain('Line 2');
      expect(result.body).toContain('Line 3');
    });
    
    test('should return null for content without frontmatter', () => {
      const content = `This is just plain content without frontmatter.`;
      
      const result = parseFrontmatter(content);
      
      expect(result).toBeNull();
    });
    
    test('should return null for malformed frontmatter', () => {
      const content = `---
interval: 1h
name: Test

This is missing closing delimiter.`;
      
      const result = parseFrontmatter(content);
      
      expect(result).toBeNull();
    });
    
    test('should parse all valid frontmatter fields', () => {
      const content = `---
interval: 1h
tz: UTC
timeout: 15m
agent: claude-code
model: opus
maxTurns: 50
name: Full Test
description: A test heartbeat
---

Body content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter).toEqual({
        interval: '1h',
        tz: 'UTC',
        timeout: '15m',
        agent: 'claude-code',
        model: 'opus',
        maxTurns: 50,
        name: 'Full Test',
        description: 'A test heartbeat'
      });
    });
    
    test('should handle codex-specific fields', () => {
      const content = `---
agent: codex
sandbox: workspace-write
networkAccess: false
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.sandbox).toBe('workspace-write');
      expect(result.frontmatter.networkAccess).toBe(false);
    });
    
    test('should handle pi-specific fields', () => {
      const content = `---
agent: pi
session: my-session
---

Content.`;
      
      const result = parseFrontmatter(content);
      
      expect(result.frontmatter.session).toBe('my-session');
    });
  });
});
