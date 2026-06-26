/**
 * api.mjs — API Client for Karpak Life + SBT
 */

import https from 'node:https';
import http from 'node:http';

function request(method, url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const opts = {
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method,
      headers: { 'Content-Type': 'application/json', ...headers },
    };
    const mod = parsed.protocol === 'https:' ? https : http;
    const req = mod.request(opts, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString();
        try { resolve({ status: res.statusCode, data: JSON.parse(raw) }); }
        catch { resolve({ status: res.statusCode, data: raw }); }
      });
    });
    req.on('error', reject);
    if (body !== undefined && body !== null) {
      req.write(typeof body === 'string' ? body : JSON.stringify(body));
    }
    req.end();
  });
}

export class ApiError extends Error {
  constructor(step, status, data) {
    const msg = typeof data === 'object' ? JSON.stringify(data) : String(data);
    super(`API error at ${step}: HTTP ${status} - ${msg}`);
    this.step = step;
    this.status = status;
    this.data = data;
  }
}

export function createApiClient(cfg) {
  return {
    async issueNonce(address) {
      const { status, data } = await request('POST', `${cfg.apiBase}/v1/auth:issueNonce`, { address });
      if (status !== 200) throw new ApiError('issueNonce', status, data);
      return data;
    },

    async verify(address, signature) {
      const { status, data } = await request('POST', `${cfg.apiBase}/v1/auth:verify`, { address, signature });
      if (status !== 200) throw new ApiError('verify', status, data);
      return data;
    },

    async updateProfile(token, nickname, identityType) {
      const { status, data } = await request('PUT', `${cfg.apiBase}/v1/me`,
        { nickname, avatarUrl: '', identityType },
        { 'X-Session-Token': token }
      );
      if (status !== 200) throw new ApiError('updateProfile', status, data);
      return data;
    },

    async getCredential(token) {
      const { status, data } = await request('GET', `${cfg.apiBase}/v1/me/credential`, null,
        { 'X-Session-Token': token }
      );
      if (status !== 200) throw new ApiError('getCredential', status, data);
      return data;
    },

    async getMintSignature(walletAddress, twitterUsername, contractAddress, chainId) {
      const { status, data } = await request('POST', `${cfg.sbtUrl}/api/mint-signature`, {
        walletAddress, twitterUsername, contractAddress, chainId,
      });
      if (status !== 200) throw new ApiError('mintSignature', status, data);
      return data;
    },

    async verifyStatus(walletAddress) {
      const { status, data } = await request('POST', `${cfg.sbtUrl}/api/verify-status`, { walletAddress });
      if (status !== 200) throw new ApiError('verifyStatus', status, data);
      return data;
    },

    async checkMintStatus() {
      const { status, data } = await request('GET', `${cfg.sbtUrl}/api/mint-status`);
      if (status !== 200) throw new ApiError('mintStatus', status, data);
      return data;
    },

    async waitForTx(txHash, timeoutMs = 60000) {
      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        try {
          const { data } = await request('POST', cfg.rpcUrl, {
            jsonrpc: '2.0', id: 1, method: 'eth_getTransactionReceipt', params: [txHash],
          });
          if (data?.result?.status === '0x1') return data.result;
          if (data?.result?.status === '0x0') throw new Error('Transaction reverted on chain');
        } catch (e) {
          if (e.message === 'Transaction reverted on chain') throw e;
        }
        await new Promise(r => setTimeout(r, 3000));
      }
      throw new Error(`Transaction not confirmed within ${timeoutMs / 1000}s`);
    },
  };
}
