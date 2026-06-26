/**
 * Unit tests for SKILL.md parsing and validation
 */

import { describe, test, expect } from '@jest/globals';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parseFrontmatter } from '../test-helpers.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillPath = join(__dirname, '../../SKILL.md');

describe('SKILL.md Parser', () => {
  let skillContent;
  
  beforeAll(() => {
    skillContent = readFileSync(skillPath, 'utf-8');
  });
  
  describe('Metadata Validation', () => {
    test('should have valid YAML frontmatter', () => {
      const result = parseFrontmatter(skillContent);
      
      expect(result).not.toBeNull();
      expect(result.frontmatter).toHaveProperty('name');
      expect(result.frontmatter).toHaveProperty('description');
      expect(result.frontmatter).toHaveProperty('metadata');
    });
    
    test('should have correct skill name', () => {
      const result = parseFrontmatter(skillContent);
      
      expect(result.frontmatter.name).toBe('heartbeat-cron');
    });
    
    test('should have metadata with author and version', () => {
      const result = parseFrontmatter(skillContent);
      
      // Check that author and version exist (either at top level or in metadata object)
      const author = result.frontmatter.metadata?.author || result.frontmatter.author;
      const version = result.frontmatter.metadata?.version || result.frontmatter.version;
      
      expect(author).toBeDefined();
      expect(version).toBeDefined();
    });
    
    test('should have semver version format', () => {
      const result = parseFrontmatter(skillContent);
      
      const version = result.frontmatter.metadata?.version || result.frontmatter.version;
      const semverPattern = /^\d+\.\d+\.\d+$/;
      
      expect(version).toBeDefined();
      expect(version).toMatch(semverPattern);
    });
  });
  
  describe('Required Sections', () => {
    test('should have Context section', () => {
      expect(skillContent).toContain('# Context');
    });
    
    test('should have HEARTBEAT.md Format section', () => {
      expect(skillContent).toContain('# HEARTBEAT.md Format');
    });
    
    test('should have Workflow section', () => {
      expect(skillContent).toContain('# Workflow');
    });
    
    test('should have Rules section', () => {
      expect(skillContent).toContain('# Rules');
    });
  });
  
  describe('Workflow Steps', () => {
    test('should have Preflight step (0)', () => {
      expect(skillContent).toContain('### 0. Preflight');
    });
    
    test('should have Interview step (1)', () => {
      expect(skillContent).toContain('### 1. Interview');
    });
    
    test('should have Draft step (2)', () => {
      expect(skillContent).toContain('### 2. Draft');
    });
    
    test('should have Test step (3)', () => {
      expect(skillContent).toContain('### 3. Test');
    });
    
    test('should have Evaluate step (4)', () => {
      expect(skillContent).toContain('### 4. Evaluate');
    });
    
    test('should have Register step (5)', () => {
      expect(skillContent).toContain('### 5. Register');
    });
  });
  
  describe('Interview Rounds', () => {
    test('should have Round 1 (The goal)', () => {
      expect(skillContent).toContain('**Round 1 — The goal:**');
    });
    
    test('should have Round 1b (Tool discovery)', () => {
      expect(skillContent).toContain('**Round 1b — Tool discovery:**');
    });
    
    test('should have Round 2 (The details)', () => {
      expect(skillContent).toContain('**Round 2 — The details:**');
    });
    
    test('should have Round 3 (Delivery)', () => {
      expect(skillContent).toContain('**Round 3 — Delivery:**');
    });
    
    test('should have Round 3b (Credentials)', () => {
      expect(skillContent).toContain('**Round 3b — Credentials (if needed):**');
    });
  });
  
  describe('Frontmatter Fields Documentation', () => {
    test('should document interval field', () => {
      expect(skillContent).toContain('interval:');
    });
    
    test('should document cron field', () => {
      expect(skillContent).toContain('cron:');
    });
    
    test('should document tz field', () => {
      expect(skillContent).toContain('tz:');
    });
    
    test('should document timeout field', () => {
      expect(skillContent).toContain('timeout:');
    });
    
    test('should document agent field', () => {
      expect(skillContent).toContain('agent:');
    });
    
    test('should document model field', () => {
      expect(skillContent).toContain('model:');
    });
    
    test('should document sandbox field', () => {
      expect(skillContent).toContain('sandbox:');
    });
    
    test('should document permissions field', () => {
      expect(skillContent).toContain('permissions:');
    });
  });
  
  describe('Trigger Keywords', () => {
    test('should list heartbeat trigger', () => {
      expect(skillContent).toContain('heartbeat');
    });
    
    test('should list murmur trigger', () => {
      expect(skillContent).toContain('murmur');
    });
    
    test('should list cron trigger', () => {
      expect(skillContent).toContain('cron');
    });
    
    test('should list recurring task trigger', () => {
      expect(skillContent).toContain('recurring task');
    });
    
    test('should list scheduled action trigger', () => {
      expect(skillContent).toContain('scheduled action');
    });
    
    test('should list monitor trigger', () => {
      expect(skillContent).toContain('monitor');
    });
    
    test('should list watch trigger', () => {
      expect(skillContent).toContain('watch');
    });
    
    test('should list automate trigger', () => {
      expect(skillContent).toContain('automate');
    });
  });
  
  describe('Code Examples', () => {
    test('should have murmur init examples', () => {
      expect(skillContent).toContain('murmur init');
    });
    
    test('should have murmur beat example', () => {
      expect(skillContent).toContain('murmur beat');
    });
    
    test('should have murmur workspaces list example', () => {
      expect(skillContent).toContain('murmur workspaces list');
    });
    
    test('should have murmur start example', () => {
      expect(skillContent).toContain('murmur start');
    });
  });
  
  describe('Rules Validation', () => {
    test('should mention not leaving placeholders', () => {
      expect(skillContent).toContain('{placeholder}');
    });
    
    test('should mention testing with murmur beat', () => {
      expect(skillContent).toContain('murmur beat');
    });
    
    test('should mention one heartbeat one purpose', () => {
      expect(skillContent).toContain('One heartbeat = one purpose');
    });
  });
  
  describe('Content Quality', () => {
    test('should have minimum content length', () => {
      expect(skillContent.length).toBeGreaterThan(5000);
    });
    
    test('should not contain TODO comments', () => {
      expect(skillContent).not.toMatch(/TODO/i);
    });
    
    test('should not contain FIXME comments', () => {
      expect(skillContent).not.toMatch(/FIXME/i);
    });
  });
});
