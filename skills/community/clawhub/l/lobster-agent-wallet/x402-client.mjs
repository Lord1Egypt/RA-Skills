/**
 * x402 Client — Lightweight x402 payment implementation
 * 
 * Adapted from the x402 skill (MIT, lumenfromthefuture).
 * Supports paying for resources on Base via EIP-3009 gasless USDC transfers.
 * 
 * Security: All signing uses the wallet account in memory.
 * No private keys are ever stored or logged.
 */

// Supported networks (Base + Base Sepolia)
const SUPPORTED_NETWORKS = {
  'eip155:8453': {
    chainId: 8453,
    name: 'Base',
    usdcAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  },
  'eip155:84532': {
    chainId: 84532,
    name: 'Base Sepolia',
    usdcAddress: '0x036CbD53842c5426634e7929541eC2318f3dCF7e',
  },
};

/**
 * Parse x402 payment requirements from a 402 response.
 */
export async function parsePaymentRequired(response) {
  // Try X-Payment-Required header first
  const header = response.headers.get('X-Payment-Required');
  if (header) {
    try {
      const parsed = JSON.parse(header);
      if (parsed.accepts) return parsed;
    } catch {
      try {
        const decoded = atob(header);
        const parsed = JSON.parse(decoded);
        if (parsed.accepts) return parsed;
      } catch {}
    }
  }

  // Try JSON body
  try {
    const body = await response.clone().json();
    if (body.accepts) return body;
  } catch {}

  return null;
}

/**
 * Create EIP-3009 transferWithAuthorization signature.
 */
export async function createPaymentSignature(account, requirement, x402Version = 1) {
  const network = SUPPORTED_NETWORKS[requirement.network];
  if (!network) {
    throw new Error(`Unsupported network: ${requirement.network}`);
  }

  // Generate random nonce (crypto secure)
  const nonceBytes = new Uint8Array(32);
  crypto.getRandomValues(nonceBytes);
  const nonce = `0x${Buffer.from(nonceBytes).toString('hex')}`;

  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(now - 60);
  const validBefore = BigInt(now + (requirement.maxTimeoutSeconds || requirement.requiredDeadlineSeconds || 300));

  // Parse amount
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
    chainId: network.chainId,
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
    scheme: requirement.scheme,
    network: requirement.network,
    payload: {
      signature,
      authorization,
    },
  };
}

/**
 * Encode payment payload as X-Payment header value.
 */
export function encodePaymentHeader(payment) {
  const serializable = {
    ...payment,
    payload: {
      ...payment.payload,
      authorization: {
        ...payment.payload.authorization,
        value: payment.payload.authorization.value.toString(),
        validAfter: payment.payload.authorization.validAfter.toString(),
        validBefore: payment.payload.authorization.validBefore.toString(),
      },
    },
  };
  return btoa(JSON.stringify(serializable));
}

/**
 * Fetch with automatic x402 payment handling.
 * Requires explicit --confirm flag.
 */
export async function x402Fetch(account, url, options = {}) {
  // Initial request
  const response = await fetch(url, options);

  if (response.status !== 402) {
    return response;
  }

  // Parse payment requirements
  const requirements = await parsePaymentRequired(response);
  if (!requirements) {
    throw new Error('Received HTTP 402 but could not parse payment requirements');
  }

  // Find supported payment option
  const requirement = requirements.accepts.find(
    r => r.scheme === 'exact' && SUPPORTED_NETWORKS[r.network]
  );

  if (!requirement) {
    throw new Error('No supported x402 payment options found for this endpoint');
  }

  // Create and sign payment
  const payment = await createPaymentSignature(account, requirement, requirements.x402Version);

  // Retry with payment header
  const paidResponse = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-Payment': encodePaymentHeader(payment),
    },
  });

  return paidResponse;
}
