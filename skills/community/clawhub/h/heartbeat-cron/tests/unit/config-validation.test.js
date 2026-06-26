/**
 * Unit tests for configuration validation
 */

import { describe, test, expect } from '@jest/globals';
import {
  isValidInterval,
  isValidCron,
  isValidTimezone,
  isValidAgent,
  isValidSandbox,
  isValidPermissions,
  validateHeartbeatConfig
} from '../test-helpers.js';

describe('Configuration Validation', () => {
  describe('isValidInterval', () => {
    test('should accept valid minute intervals', () => {
      expect(isValidInterval('15m')).toBe(true);
      expect(isValidInterval('30m')).toBe(true);
      expect(isValidInterval('1m')).toBe(true);
      expect(isValidInterval('60m')).toBe(true);
    });
    
    test('should accept valid hour intervals', () => {
      expect(isValidInterval('1h')).toBe(true);
      expect(isValidInterval('6h')).toBe(true);
      expect(isValidInterval('12h')).toBe(true);
      expect(isValidInterval('24h')).toBe(true);
    });
    
    test('should accept valid day intervals', () => {
      expect(isValidInterval('1d')).toBe(true);
      expect(isValidInterval('7d')).toBe(true);
      expect(isValidInterval('30d')).toBe(true);
    });
    
    test('should reject invalid interval formats', () => {
      expect(isValidInterval('5x')).toBe(false);
      expect(isValidInterval('1w')).toBe(false);
      expect(isValidInterval('100')).toBe(false);
      expect(isValidInterval('m15')).toBe(false);
      expect(isValidInterval('')).toBe(false);
    });
    
    test('should reject non-string values', () => {
      expect(isValidInterval(15)).toBe(false);
      expect(isValidInterval(null)).toBe(false);
      expect(isValidInterval(undefined)).toBe(false);
      expect(isValidInterval({})).toBe(false);
    });
    
    test('should reject out-of-range values', () => {
      expect(isValidInterval('0m')).toBe(false);
      expect(isValidInterval('2000m')).toBe(false);
      expect(isValidInterval('0h')).toBe(false);
      expect(isValidInterval('500h')).toBe(false);
      expect(isValidInterval('0d')).toBe(false);
      expect(isValidInterval('1000d')).toBe(false);
    });
  });
  
  describe('isValidCron', () => {
    test('should accept valid cron expressions', () => {
      expect(isValidCron('0 9 * * 1-5')).toBe(true);
      expect(isValidCron('*/30 * * * *')).toBe(true);
      expect(isValidCron('0 0 * * *')).toBe(true);
      expect(isValidCron('0 9 * * 1')).toBe(true);
      expect(isValidCron('* * * * *')).toBe(true);
    });
    
    test('should reject invalid cron expressions', () => {
      expect(isValidCron('invalid')).toBe(false);
      expect(isValidCron('0 9 * *')).toBe(false); // Missing field
      expect(isValidCron('0 9 * * 1-5 extra')).toBe(false); // Extra field
      expect(isValidCron('')).toBe(false);
    });
    
    test('should reject non-string values', () => {
      expect(isValidCron(123)).toBe(false);
      expect(isValidCron(null)).toBe(false);
      expect(isValidCron(undefined)).toBe(false);
      expect(isValidCron([])).toBe(false);
    });
    
    test('should accept cron with step values', () => {
      expect(isValidCron('*/15 * * * *')).toBe(true);
      expect(isValidCron('0 */2 * * *')).toBe(true);
    });
    
    test('should accept cron with ranges', () => {
      expect(isValidCron('0 9-17 * * 1-5')).toBe(true);
      expect(isValidCron('0 0 1-15 * *')).toBe(true);
    });
  });
  
  describe('isValidTimezone', () => {
    test('should accept valid IANA timezones', () => {
      expect(isValidTimezone('America/New_York')).toBe(true);
      expect(isValidTimezone('Europe/London')).toBe(true);
      expect(isValidTimezone('Asia/Shanghai')).toBe(true);
      expect(isValidTimezone('UTC')).toBe(true);
      expect(isValidTimezone('America/Los_Angeles')).toBe(true);
    });
    
    test('should reject invalid timezone formats', () => {
      expect(isValidTimezone('EST')).toBe(false);
      expect(isValidTimezone('PST')).toBe(false);
      expect(isValidTimezone('GMT+8')).toBe(false);
      expect(isValidTimezone('')).toBe(false);
      expect(isValidTimezone('invalid')).toBe(false);
    });
    
    test('should reject non-string values', () => {
      expect(isValidTimezone(123)).toBe(false);
      expect(isValidTimezone(null)).toBe(false);
      expect(isValidTimezone(undefined)).toBe(false);
    });
  });
  
  describe('isValidAgent', () => {
    test('should accept valid agents', () => {
      expect(isValidAgent('claude-code')).toBe(true);
      expect(isValidAgent('codex')).toBe(true);
      expect(isValidAgent('pi')).toBe(true);
    });
    
    test('should reject invalid agents', () => {
      expect(isValidAgent('gpt')).toBe(false);
      expect(isValidAgent('claude')).toBe(false);
      expect(isValidAgent('')).toBe(false);
      expect(isValidAgent(null)).toBe(false);
    });
  });
  
  describe('isValidSandbox', () => {
    test('should accept valid sandbox types', () => {
      expect(isValidSandbox('read-only')).toBe(true);
      expect(isValidSandbox('workspace-write')).toBe(true);
      expect(isValidSandbox('danger-full-access')).toBe(true);
    });
    
    test('should reject invalid sandbox types', () => {
      expect(isValidSandbox('full-access')).toBe(false);
      expect(isValidSandbox('write')).toBe(false);
      expect(isValidSandbox('')).toBe(false);
      expect(isValidSandbox(null)).toBe(false);
    });
  });
  
  describe('isValidPermissions', () => {
    test('should accept "skip"', () => {
      expect(isValidPermissions('skip')).toBe(true);
    });
    
    test('should reject other values', () => {
      expect(isValidPermissions('deny')).toBe(false);
      expect(isValidPermissions('allow')).toBe(false);
      expect(isValidPermissions('')).toBe(false);
      expect(isValidPermissions(null)).toBe(false);
    });
  });
  
  describe('validateHeartbeatConfig', () => {
    test('should validate config with interval', () => {
      const config = {
        interval: '1h',
        name: 'Test'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    test('should validate config with cron', () => {
      const config = {
        cron: '0 9 * * 1-5',
        tz: 'America/New_York'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    test('should reject config with no schedule', () => {
      const config = {
        name: 'No Schedule'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Missing schedule: must have either "interval" or "cron"');
    });
    
    test('should reject config with both interval and cron', () => {
      const config = {
        interval: '1h',
        cron: '0 9 * * 1-5'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid schedule: cannot have both "interval" and "cron"');
    });
    
    test('should reject config with invalid interval', () => {
      const config = {
        interval: '5x'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid interval'))).toBe(true);
    });
    
    test('should reject config with invalid cron', () => {
      const config = {
        cron: 'invalid'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid cron'))).toBe(true);
    });
    
    test('should reject config with invalid agent', () => {
      const config = {
        interval: '1h',
        agent: 'gpt'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid agent'))).toBe(true);
    });
    
    test('should reject config with invalid sandbox', () => {
      const config = {
        interval: '1h',
        agent: 'codex',
        sandbox: 'invalid'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid sandbox'))).toBe(true);
    });
    
    test('should reject config with invalid permissions', () => {
      const config = {
        interval: '1h',
        permissions: 'deny'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid permissions'))).toBe(true);
    });
    
    test('should reject config with invalid timezone', () => {
      const config = {
        cron: '0 9 * * 1-5',
        tz: 'EST'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid timezone'))).toBe(true);
    });
    
    test('should reject config with invalid timeout', () => {
      const config = {
        interval: '1h',
        timeout: '5x'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(false);
      expect(result.errors.some(e => e.includes('Invalid timeout'))).toBe(true);
    });
    
    test('should accept comprehensive valid config', () => {
      const config = {
        interval: '1h',
        tz: 'UTC',
        timeout: '15m',
        agent: 'codex',
        model: 'opus',
        maxTurns: 50,
        sandbox: 'workspace-write',
        networkAccess: true,
        permissions: 'skip',
        name: 'Comprehensive Test'
      };
      
      const result = validateHeartbeatConfig(config);
      
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });
});
