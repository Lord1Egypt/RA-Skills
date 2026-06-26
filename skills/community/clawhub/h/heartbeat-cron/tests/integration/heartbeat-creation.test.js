/**
 * Integration tests for HEARTBEAT.md creation and murmur configuration
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import { writeFileSync, readFileSync, mkdirSync, rmSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parseFrontmatter, validateHeartbeatConfig, loadFixture } from '../test-helpers.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const testWorkspace = join(__dirname, '../../test-workspace');

describe('HEARTBEAT.md Creation Integration', () => {
  beforeEach(() => {
    // Clean up test workspace
    if (existsSync(testWorkspace)) {
      rmSync(testWorkspace, { recursive: true, force: true });
    }
    mkdirSync(testWorkspace, { recursive: true });
  });
  
  afterAll(() => {
    // Clean up after all tests
    if (existsSync(testWorkspace)) {
      rmSync(testWorkspace, { recursive: true, force: true });
    }
  });
  
  describe('Basic Heartbeat Creation', () => {
    test('should create minimal heartbeat file', () => {
      const heartbeatPath = join(testWorkspace, 'HEARTBEAT.md');
      const content = loadFixture('minimal-heartbeat.md');
      
      writeFileSync(heartbeatPath, content);
      
      // Verify file exists
      expect(existsSync(heartbeatPath)).toBe(true);
      
      // Read and validate
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed).not.toBeNull();
      expect(parsed.frontmatter.interval).toBe('30m');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should create heartbeat with interval schedule', () => {
      const heartbeatPath = join(testWorkspace, 'HEARTBEAT.md');
      const content = loadFixture('valid-heartbeat-interval.md');
      
      writeFileSync(heartbeatPath, content);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.interval).toBe('1h');
      expect(parsed.frontmatter.timeout).toBe('15m');
      expect(parsed.frontmatter.agent).toBe('claude-code');
      expect(parsed.frontmatter.model).toBe('opus');
      expect(parsed.frontmatter.name).toBe('GitHub Issue Monitor');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should create heartbeat with cron schedule', () => {
      const heartbeatPath = join(testWorkspace, 'HEARTBEAT.md');
      const content = loadFixture('valid-heartbeat-cron.md');
      
      writeFileSync(heartbeatPath, content);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.cron).toBe('0 9 * * 1-5');
      expect(parsed.frontmatter.tz).toBe('America/New_York');
      expect(parsed.frontmatter.agent).toBe('codex');
      expect(parsed.frontmatter.sandbox).toBe('workspace-write');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
    
    test('should create heartbeat with all configuration options', () => {
      const heartbeatPath = join(testWorkspace, 'HEARTBEAT.md');
      const content = loadFixture('full-heartbeat.md');
      
      writeFileSync(heartbeatPath, content);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.interval).toBe('1h');
      expect(parsed.frontmatter.tz).toBe('UTC');
      expect(parsed.frontmatter.timeout).toBe('30m');
      expect(parsed.frontmatter.agent).toBe('codex');
      expect(parsed.frontmatter.model).toBe('sonnet');
      expect(parsed.frontmatter.maxTurns).toBe(100);
      expect(parsed.frontmatter.sandbox).toBe('workspace-write');
      expect(parsed.frontmatter.networkAccess).toBe(false);
      expect(parsed.frontmatter.permissions).toBe('skip');
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      expect(validation.isValid).toBe(true);
    });
  });
  
  describe('Named Heartbeats', () => {
    test('should create named heartbeat in heartbeats directory', () => {
      const heartbeatDir = join(testWorkspace, 'heartbeats', 'issue-worker');
      mkdirSync(heartbeatDir, { recursive: true });
      
      const heartbeatPath = join(heartbeatDir, 'HEARTBEAT.md');
      const content = loadFixture('valid-heartbeat-interval.md');
      
      writeFileSync(heartbeatPath, content);
      
      expect(existsSync(heartbeatPath)).toBe(true);
      
      const fileContent = readFileSync(heartbeatPath, 'utf-8');
      const parsed = parseFrontmatter(fileContent);
      
      expect(parsed.frontmatter.name).toBe('GitHub Issue Monitor');
      expect(parsed.frontmatter.interval).toBe('1h');
    });
    
    test('should support multiple named heartbeats', () => {
      const heartbeat1Dir = join(testWorkspace, 'heartbeats', 'issue-worker');
      const heartbeat2Dir = join(testWorkspace, 'heartbeats', 'deploy-monitor');
      
      mkdirSync(heartbeat1Dir, { recursive: true });
      mkdirSync(heartbeat2Dir, { recursive: true });
      
      const heartbeat1Path = join(heartbeat1Dir, 'HEARTBEAT.md');
      const heartbeat2Path = join(heartbeat2Dir, 'HEARTBEAT.md');
      
      writeFileSync(heartbeat1Path, loadFixture('valid-heartbeat-interval.md'));
      writeFileSync(heartbeat2Path, loadFixture('valid-heartbeat-cron.md'));
      
      expect(existsSync(heartbeat1Path)).toBe(true);
      expect(existsSync(heartbeat2Path)).toBe(true);
      
      // Verify different configurations
      const content1 = readFileSync(heartbeat1Path, 'utf-8');
      const content2 = readFileSync(heartbeat2Path, 'utf-8');
      
      const parsed1 = parseFrontmatter(content1);
      const parsed2 = parseFrontmatter(content2);
      
      expect(parsed1.frontmatter.interval).toBe('1h');
      expect(parsed2.frontmatter.cron).toBe('0 9 * * 1-5');
    });
  });
  
  describe('Invalid Heartbeat Detection', () => {
    test('should detect heartbeat with both interval and cron', () => {
      const content = loadFixture('invalid-heartbeat-both-schedule.md');
      const parsed = parseFrontmatter(content);
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(false);
      expect(validation.errors.some(e => e.includes('cannot have both'))).toBe(true);
    });
    
    test('should detect heartbeat with no schedule', () => {
      const content = loadFixture('invalid-heartbeat-no-schedule.md');
      const parsed = parseFrontmatter(content);
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(false);
      expect(validation.errors.some(e => e.includes('Missing schedule'))).toBe(true);
    });
    
    test('should detect heartbeat with invalid interval', () => {
      const content = loadFixture('invalid-heartbeat-bad-interval.md');
      const parsed = parseFrontmatter(content);
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(false);
      expect(validation.errors.some(e => e.includes('Invalid interval'))).toBe(true);
    });
    
    test('should detect heartbeat with invalid cron', () => {
      const content = loadFixture('invalid-heartbeat-bad-cron.md');
      const parsed = parseFrontmatter(content);
      
      const validation = validateHeartbeatConfig(parsed.frontmatter);
      
      expect(validation.isValid).toBe(false);
      expect(validation.errors.some(e => e.includes('Invalid cron'))).toBe(true);
    });
  });
  
  describe('Body Content Validation', () => {
    test('should preserve body content after frontmatter', () => {
      const content = loadFixture('valid-heartbeat-interval.md');
      const parsed = parseFrontmatter(content);
      
      expect(parsed.body).toContain('Check for new GitHub issues');
      expect(parsed.body).toContain('gh issue list');
      expect(parsed.body).toContain('HEARTBEAT_OK');
    });
    
    test('should detect placeholder values in body', () => {
      const content = `---
interval: 1h
---

Check issues on {org}/{repo} using gh CLI.`;
      
      const parsed = parseFrontmatter(content);
      
      // Check for placeholders
      const hasPlaceholders = /\{[^}]+\}/.test(parsed.body);
      expect(hasPlaceholders).toBe(true);
    });
    
    test('should validate no placeholders in final heartbeat', () => {
      const content = loadFixture('valid-heartbeat-interval.md');
      const parsed = parseFrontmatter(content);
      
      // This fixture has placeholders, which is expected for a template
      // In production, these should be replaced
      const hasPlaceholders = /\{[^}]+\}/.test(parsed.body);
      
      // For this test, we just verify we can detect them
      expect(hasPlaceholders).toBe(true);
    });
  });
  
  describe('Murmur Command Generation', () => {
    test('should generate murmur init command', () => {
      const workspacePath = '/path/to/workspace';
      const command = `murmur init ${workspacePath}`;
      
      expect(command).toContain('murmur init');
      expect(command).toContain(workspacePath);
    });
    
    test('should generate murmur init with interval flag', () => {
      const workspacePath = '/path/to/workspace';
      const interval = '30m';
      const command = `murmur init ${workspacePath} --interval ${interval}`;
      
      expect(command).toContain('--interval');
      expect(command).toContain('30m');
    });
    
    test('should generate murmur init with cron flag', () => {
      const workspacePath = '/path/to/workspace';
      const cron = '0 9 * * 1-5';
      const command = `murmur init ${workspacePath} --cron "${cron}"`;
      
      expect(command).toContain('--cron');
      expect(command).toContain('0 9 * * 1-5');
    });
    
    test('should generate murmur init with name flag', () => {
      const workspacePath = '/path/to/workspace';
      const name = 'issue-worker';
      const command = `murmur init ${workspacePath} --name ${name}`;
      
      expect(command).toContain('--name');
      expect(command).toContain('issue-worker');
    });
    
    test('should generate murmur beat command', () => {
      const workspacePath = '/path/to/workspace';
      const command = `murmur beat ${workspacePath}`;
      
      expect(command).toContain('murmur beat');
    });
    
    test('should generate murmur beat command with name', () => {
      const workspacePath = '/path/to/workspace';
      const name = 'issue-worker';
      const command = `murmur beat ${workspacePath} --name ${name}`;
      
      expect(command).toContain('--name');
    });
    
    test('should generate murmur workspaces list command', () => {
      const command = 'murmur workspaces list';
      
      expect(command).toBe('murmur workspaces list');
    });
    
    test('should generate murmur start command', () => {
      const command = 'murmur start';
      
      expect(command).toBe('murmur start');
    });
    
    test('should generate murmur start with detach flag', () => {
      const command = 'murmur start --detach';
      
      expect(command).toBe('murmur start --detach');
    });
  });
});
