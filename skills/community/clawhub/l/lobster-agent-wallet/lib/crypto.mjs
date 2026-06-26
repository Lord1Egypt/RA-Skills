/**
 * Agent Wallet — Crypto Utilities
 * 
 * Phase 2: Full EIP-712 typed data signing via viem.
 * Private key loaded into viem account (memory only) — NEVER logged/exported.
 */

import { privateKeyToAccount } from 'viem/accounts';

/**
 * Get viem account from private key.
 * Private key exists in viem memory only — never serialized or logged.
 */
export function getAccount(privateKey) {
  return privateKeyToAccount(privateKey);
}

/**
 * Derive Ethereum address from private key.
 */
export function privateKeyToAddress(privateKey) {
  return getAccount(privateKey).address.toLowerCase();
}

/**
 * Sign EIP-712 typed data and return full EIP-3009 authorization.
 * 
 * Creates a TransferWithAuthorization signature for gasless USDC transfers.
 * Used by the x402 payment protocol.
 * 
 * @param {string} privateKey - Hex private key (0x-prefixed)
 * @param {Object} requirement - x402 payment requirement { network, maxAmountRequired, payTo, asset }
 * @param {number} x402Version - Protocol version
 * @returns {Object} Payment payload with signature + authorization
 */
export async function createEIP3009Signature(privateKey, requirement, x402Version = 1) {
  const account = getAccount(privateKey);

  // Parse network from EIP-155 namespace (e.g., "eip155:8453")
  const chainId = parseInt(requirement.network.split(':')[1], 10);

  // Generate cryptographically secure random nonce (32 bytes)
  const nonceBytes = new Uint8Array(32);
  crypto.getRandomValues(nonceBytes);
  const nonce = `0x${Buffer.from(nonceBytes).toString('hex')}`;

  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(now - 60);
  const validBefore = BigInt(now + (requirement.maxTimeoutSeconds || requirement.requiredDeadlineSeconds || 300));

  // Parse amount: decimal string ("5.00") or base units
  const maxAmount = requirement.maxAmountRequired;
  let value;
  if (typeof maxAmount === 'string' && maxAmount.includes('.')) {
    value = BigInt(Math.floor(parseFloat(maxAmount) * 1e6));
  } else if (x402Version >= 2 || String(maxAmount).length > 6) {
    value = BigInt(maxAmount);
  } else {
    value = BigInt(maxAmount) * BigInt(1e6);
  }

  const authorization = {
    from: account.address,
    to: requirement.payTo || requirement.payToAddress,
    value,
    validAfter,
    validBefore,
    nonce,
  };

  const domain = {
    name: requirement.extra?.name || 'USD Coin',
    version: requirement.extra?.version || '2',
    chainId,
    verifyingContract: requirement.asset || requirement.usdcAddress,
  };

  const types = {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
    ],
  };

  const signature = await account.signTypedData({
    domain,
    types,
    primaryType: 'TransferWithAuthorization',
    message: authorization,
  });

  return {
    x402Version: 1,
    scheme: requirement.scheme || 'exact',
    network: requirement.network,
    payload: {
      signature,
      authorization: {
        ...authorization,
        value: value.toString(),
        validAfter: validAfter.toString(),
        validBefore: validBefore.toString(),
      },
    },
  };
}
