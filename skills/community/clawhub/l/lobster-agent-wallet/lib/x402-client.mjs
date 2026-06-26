/**
 * x402 Client — HTTP 402 Payment Protocol
 * 
 * Pay for resources via the x402 protocol using gasless USDC on Base.
 * Uses EIP-3009 transferWithAuthorization for secure, gasless payments.
 * 
 * Security: Requires explicit --confirm flag before signing any transfers.
 * Private key is held in viem account (memory only) — never exposed.
 */

import { createEIP3009Signature } from './crypto.mjs';
import { getWallet } from './core.mjs';

// ─── Parse ───────────────────────────────────────────────────────────

/**
 * Parse x402 payment requirements from a 402 response.
 */
export async function parsePaymentRequired(response) {
  const header = response.headers.get('X-Payment-Required');
  if (header) {
    try {
      const parsed = JSON.parse(header);
      if (parsed.accepts) return parsed;
    } catch {
      try {
        const decoded = atob(header);
        return JSON.parse(decoded);
      } catch {}
    }
  }

  try {
    const body = await response.clone().json();
    if (body.accepts) return body;
  } catch {}

  return null;
}

// ─── Sign ────────────────────────────────────────────────────────────

/**
 * Encode payment payload as X-Payment header value (base64).
 */
export function encodePaymentHeader(payment) {
  return btoa(JSON.stringify(payment));
}

// ─── Fetch ───────────────────────────────────────────────────────────

/**
 * Fetch a resource with automatic x402 payment handling.
 * 
 * @param {string} url - Target URL
 * @param {string} privateKey - Wallet private key (from env)
 * @param {Object} options - Fetch options + { confirm: boolean }
 * @returns {Promise<Response>}
 */
export async function payX402(url, privateKey, options = {}) {
  if (!options.confirm) {
    throw new Error(
      'SECURITY: x402 payments require --confirm.\n' +
      'This will sign a USDC transfer authorization on-chain.\n' +
      'Pass { confirm: true } or use --confirm flag from CLI.'
    );
  }

  // Initial request
  const response = await fetch(url);
  
  // If not 402, return directly (no payment needed)
  if (response.status !== 402) {
    return { paid: false, status: response.status, response };
  }

  // Parse payment requirements
  const requirements = await parsePaymentRequired(response);
  if (!requirements) {
    throw new Error('HTTP 402 with unparseable payment requirements');
  }

  // Find a supported payment option (Base USDC)
  const option = requirements.accepts?.[0];
  if (!option || option.scheme !== 'exact') {
    throw new Error('No supported payment option (exact scheme on Base)');
  }

  // Sign the payment authorization
  const payment = await createEIP3009Signature(privateKey, option, requirements.x402Version || 1);

  // Retry with payment header
  const paidResponse = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-Payment': encodePaymentHeader(payment),
    },
  });

  return { paid: true, status: paidResponse.status, response: paidResponse };
}
