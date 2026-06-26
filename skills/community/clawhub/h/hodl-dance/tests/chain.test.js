import { describe, it, expect } from 'vitest';
import { simulateBuy, simulateSell } from '../src/lib/chain.js';

describe('chain simulations', () => {
  // These are mathematical simulations based on the bonding curve formula.
  // We test the logic with known inputs rather than exact numbers from mainnet.

  describe('simulateBuy', () => {
    it('returns positive tokensOut and fee for a valid buy', async () => {
      // Using a real active bonding curve address from mainnet
      const curve = '0xd9403ade9b1ee520ff48836855603fb09019d916';
      const result = await simulateBuy(curve, 0.1);

      expect(result.tokensOut).toBeGreaterThan(0n);
      expect(result.fee).toBeGreaterThan(0n);
      expect(result.bnbNet).toBeGreaterThan(0n);
    });

    it('increases output when buying more BNB', async () => {
      const curve = '0xd9403ade9b1ee520ff48836855603fb09019d916';

      const small = await simulateBuy(curve, 0.01);
      const large = await simulateBuy(curve, 0.1);

      expect(large.tokensOut).toBeGreaterThan(small.tokensOut);
    });
  });

  describe('simulateSell', () => {
    it('returns positive bnbOut and fee for a valid sell', async () => {
      const curve = '0xd9403ade9b1ee520ff48836855603fb09019d916';
      const result = await simulateSell(curve, 1000000); // 1M tokens

      expect(result.bnbOut).toBeGreaterThan(0n);
      expect(result.fee).toBeGreaterThan(0n);
    });
  });
});