import assert from 'node:assert/strict';
import { test } from 'node:test';
import { redactContent, buildRedactor } from '../src/redactor.ts';

test('redacts API key', () => {
  const { result, count } = redactContent('key is REDACTED-SECRET', { redactEmail: false });
  assert.ok(result.includes('<REDACTED:api_key_generic>'));
  assert.equal(count, 1);
});

test('redacts Bearer token', () => {
  const { result, count } = redactContent('Authorization: Bearer eyJlongtoken123456789012345', { redactEmail: false });
  assert.ok(result.includes('<REDACTED:bearer_header>'));
  assert.equal(count, 1);
});

test('redacts JWT', () => {
  const jwt = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';
  const { result, count } = redactContent(jwt, { redactEmail: false });
  assert.ok(result.includes('<REDACTED:jwt>'));
  assert.equal(count, 1);
});

test('redacts long hex secret', () => {
  const { result, count } = redactContent('token: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2', { redactEmail: false });
  assert.ok(result.includes('<REDACTED:long_hex_secret>'));
  assert.equal(count, 1);
});

test('does NOT redact email by default', () => {
  const { result, count } = redactContent('user@example.com', { redactEmail: false });
  assert.equal(result, 'user@example.com');
  assert.equal(count, 0);
});

test('DOES redact email when enabled', () => {
  const { result, count } = redactContent('user@example.com', { redactEmail: true });
  assert.ok(result.includes('<REDACTED:email>'));
  assert.equal(count, 1);
});

test('does not redact normal text', () => {
  const text = 'My role is senior engineer at Klik';
  const { result, count } = redactContent(text, { redactEmail: false });
  assert.equal(result, text);
  assert.equal(count, 0);
});
