import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { detectRiskyCapabilities } from '../src/classify.js';
import type { DiscoveredFile } from '../src/types.js';

function file(content: string): DiscoveredFile[] {
  return [{ path: 'test-input.ts', content }];
}

describe('risky capability detection', () => {
  it('detects eval() but ignores variable names containing "eval"', () => {
    const source = [
      'const evaluator = 1;',
      '// evaluation helper',
      'const result = eval(userCode);',
    ].join('\n');

    const caps = detectRiskyCapabilities(file(source));

    assert.equal(caps.length, 1, 'should find exactly one capability');
    assert.equal(caps[0].capability, 'eval()');
    assert.equal(caps[0].severity, 'critical');
    assert.equal(caps[0].line, 3);
  });

  it('detects dynamic require(variable) but ignores static require("fs")', () => {
    const source = [
      "const fs = require('fs');",
      "const path = require('path');",
      'const mod = require(pluginName);',
    ].join('\n');

    const caps = detectRiskyCapabilities(file(source));

    assert.equal(caps.length, 1, 'should flag only the dynamic require');
    assert.equal(caps[0].capability, 'dynamic require()');
    assert.equal(caps[0].severity, 'high');
    assert.equal(caps[0].line, 3);
  });

  it('detects net.createServer as a network listener', () => {
    const source = [
      "const net = require('net');",
      'const server = net.createServer((socket) => {',
      '  socket.end();',
      '});',
    ].join('\n');

    const caps = detectRiskyCapabilities(file(source));
    const listener = caps.find((c) => c.capability === 'network listener');

    assert.ok(listener, 'should detect network listener capability');
    assert.equal(listener.severity, 'high');
    assert.equal(listener.line, 2);
  });
});
