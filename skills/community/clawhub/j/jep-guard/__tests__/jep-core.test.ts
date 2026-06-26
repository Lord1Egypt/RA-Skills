import { JEPCore } from '../src/core/jep-core';

describe('JEPCore', () => {
  it('creates a signed Judge event', () => {
    const core = new JEPCore('test-agent');
    const event = core.createJudge({ action: 'test' }, 'test-agent');
    expect(event.verb).toBe('J');
    expect(event.who).toBe('test-agent');
    expect(event.jep).toBe('1');
    expect(event.sig).toBeDefined();
    expect(event.nonce).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i);
  });

  it('verifies its own signature', () => {
    const core = new JEPCore('test-agent');
    const event = core.createJudge({ action: 'test' }, 'test-agent');
    expect(core.verifySignature(event)).toBe(true);
  });

  it('detects tampering', () => {
    const core = new JEPCore('test-agent');
    const event = core.createJudge({ action: 'test' }, 'test-agent');
    event.what = 'tampered';
    expect(core.verifySignature(event)).toBe(false);
  });

  it('creates events with causal links', () => {
    const core = new JEPCore('test-agent');
    const parent = core.createJudge({ action: 'parent' }, 'test-agent');
    const child = core.createJudge({ action: 'child' }, 'test-agent', [parent.nonce]);

    expect(child.ref).toBe(parent.nonce);
    expect(core.dag.get(parent.nonce)).toBeDefined();
    expect(core.dag.get(child.nonce)).toBeDefined();
  });

  it('tracks event status', () => {
    const core = new JEPCore('test-agent');
    const event = core.createJudge({ action: 'test' }, 'test-agent');
    expect(core.getStatus(event.nonce)).toBe('pending');

    core.updateStatus(event.nonce, 'granted');
    expect(core.getStatus(event.nonce)).toBe('granted');
  });
});