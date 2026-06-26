import { describe, it, expect } from 'vitest';
import { isValidAddress } from '../src/lib/validators.js';

describe('validators', () => {
  describe('isValidAddress', () => {
    it('accepts valid lowercase address', () => {
      expect(isValidAddress('0x742d35cc6634c0532925a3b844bc454e4438f44e')).toBe(true);
    });

    it('accepts valid uppercase address', () => {
      expect(isValidAddress('0x742D35CC6634C0532925A3B844BC454E4438F44E')).toBe(true);
    });

    it('accepts mixed case address', () => {
      expect(isValidAddress('0x742d35Cc6634C0532925a3b844Bc454e4438f44E')).toBe(true);
    });

    it('rejects address without 0x prefix', () => {
      expect(isValidAddress('742d35cc6634c0532925a3b844bc454e4438f44e')).toBe(false);
    });

    it('rejects too short address', () => {
      expect(isValidAddress('0x742d35cc6634c0532925a3b844bc454e4438f4')).toBe(false);
    });

    it('rejects too long address', () => {
      expect(isValidAddress('0x742d35cc6634c0532925a3b844bc454e4438f44e11')).toBe(false);
    });

    it('rejects non-hex characters', () => {
      expect(isValidAddress('0x742d35cc6634c0532925a3b844bc454e4438f44g')).toBe(false);
    });

    it('rejects null/undefined/non-string', () => {
      expect(isValidAddress(null)).toBe(false);
      expect(isValidAddress(undefined)).toBe(false);
      expect(isValidAddress(12345)).toBe(false);
      expect(isValidAddress({})).toBe(false);
    });
  });
});