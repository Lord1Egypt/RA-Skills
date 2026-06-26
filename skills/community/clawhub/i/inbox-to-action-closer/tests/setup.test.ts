import { describe, it, expect } from 'vitest';

describe('project setup', () => {
  it('has ESM module type configured', async () => {
    const pkg = await import('../package.json', { with: { type: 'json' } });
    expect(pkg.default.type).toBe('module');
  });

  it('has no runtime dependencies', async () => {
    const pkg = await import('../package.json', { with: { type: 'json' } });
    expect(pkg.default.dependencies).toBeUndefined();
  });

  it('has required devDependencies', async () => {
    const pkg = await import('../package.json', { with: { type: 'json' } });
    const devDeps = pkg.default.devDependencies;
    expect(devDeps).toHaveProperty('typescript');
    expect(devDeps).toHaveProperty('vitest');
    expect(devDeps).toHaveProperty('tsx');
  });
});
