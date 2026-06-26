import { describe, it, expect } from 'vitest';
import { stripMongoFields } from '../src/lib/output.js';

describe('output helpers', () => {
  describe('stripMongoFields', () => {
    it('removes _id and __v from flat object', () => {
      const input = { _id: 'abc', __v: 0, name: 'Test', address: '0x123' };
      const result = stripMongoFields(input);

      expect(result).toEqual({ name: 'Test', address: '0x123' });
      expect(result._id).toBeUndefined();
      expect(result.__v).toBeUndefined();
    });

    it('recursively cleans nested arrays', () => {
      const input = {
        token: { _id: '1', name: 'Token' },
        trades: [
          { _id: 't1', __v: 1, amount: 100 },
          { _id: 't2', amount: 200 }
        ]
      };

      const result = stripMongoFields(input);

      expect(result.token).toEqual({ name: 'Token' });
      expect(result.trades[0]).toEqual({ amount: 100 });
      expect(result.trades[1]).toEqual({ amount: 200 });
    });

    it('handles arrays at top level', () => {
      const input = [
        { _id: '1', value: 10 },
        { _id: '2', __v: 3, value: 20 }
      ];

      const result = stripMongoFields(input);
      expect(result).toEqual([{ value: 10 }, { value: 20 }]);
    });

    it('returns primitives unchanged', () => {
      expect(stripMongoFields('hello')).toBe('hello');
      expect(stripMongoFields(42)).toBe(42);
      expect(stripMongoFields(null)).toBe(null);
    });
  });
});