/**
 * HTTP client for Broker APIs with exponential backoff (max 3 retries)
 */

import crypto from 'crypto';

const MAX_RETRIES = 3;
const BASE_DELAY_MS = 500;

function generateReqId() {
  return `req_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
}

async function fetchWithRetry(url, options, retries = MAX_RETRIES) {
  const reqId = options.headers?.['X-Request-Id'] || generateReqId();
  options.headers = { ...options.headers, 'X-Request-Id': reqId };

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, options);

      // Retry only on 5xx or network errors
      if (res.status >= 500 && attempt < retries) {
        const delay = BASE_DELAY_MS * Math.pow(2, attempt);
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }

      return res;
    } catch (err) {
      if (attempt < retries) {
        const delay = BASE_DELAY_MS * Math.pow(2, attempt);
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }
      throw err;
    }
  }
}

export class BrokerClient {
  constructor(brokerUrl, accessToken) {
    this.brokerUrl = brokerUrl.replace(/\/$/, '');
    this.accessToken = accessToken;
  }

  _headers(extra = {}) {
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.accessToken}`,
      ...extra,
    };
  }

  async register(clawid, pubkey, groupName, force = false) {
    const headers = this._headers();
    if (force) headers['X-Force-Register'] = 'true';

    const res = await fetchWithRetry(`${this.brokerUrl}/register`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ clawid, pubkey, group_name: groupName }),
    });
    return { status: res.status, data: await res.json() };
  }

  /**
   * Re-register using pubkey signature when access_token is stale/lost.
   * Sends X-Force-Register + X-Force-Challenge + X-Force-Signature headers.
   */
  async reregisterWithSignature(clawid, pubkey, challenge, signature) {
    const headers = {
      'Content-Type': 'application/json',
      'X-Force-Register': 'true',
      'X-Force-Challenge': challenge,
      'X-Force-Signature': signature,
    };
    const res = await fetchWithRetry(`${this.brokerUrl}/register`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ clawid, pubkey }),
    });
    return { status: res.status, data: await res.json() };
  }

  async getPeers() {
    const res = await fetchWithRetry(`${this.brokerUrl}/peers`, {
      method: 'GET',
      headers: this._headers(),
    });
    return { status: res.status, data: await res.json() };
  }

  async getPeer(clawid) {
    const res = await fetchWithRetry(
      `${this.brokerUrl}/peer?clawid=${encodeURIComponent(clawid)}`,
      { method: 'GET', headers: this._headers() }
    );
    return { status: res.status, data: await res.json() };
  }

  async send(payload) {
    const res = await fetchWithRetry(`${this.brokerUrl}/send`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify(payload),
    });
    return { status: res.status, data: await res.json() };
  }

  async pull(clawid) {
    const res = await fetchWithRetry(`${this.brokerUrl}/pull`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ clawid }),
    });
    return { status: res.status, data: await res.json() };
  }

  async ack(clawid, msgIds) {
    const res = await fetchWithRetry(`${this.brokerUrl}/ack`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ clawid, msg_ids: msgIds }),
    });
    return { status: res.status, data: await res.json() };
  }

  async getAllowlist() {
    const res = await fetchWithRetry(`${this.brokerUrl}/allowlist`, {
      method: 'GET',
      headers: this._headers(),
    });
    return { status: res.status, data: await res.json() };
  }

  async updateAllowlist(action, clawid) {
    const res = await fetchWithRetry(`${this.brokerUrl}/allowlist`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ action, clawid }),
    });
    return { status: res.status, data: await res.json() };
  }

  async groupCreate(groupId, ownerClawid, members = [], policy = {}) {
    const res = await fetchWithRetry(`${this.brokerUrl}/group/create`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ group_id: groupId, owner_clawid: ownerClawid, members, policy }),
    });
    return { status: res.status, data: await res.json() };
  }

  async groupJoin(groupId, clawid, inviteToken) {
    const res = await fetchWithRetry(`${this.brokerUrl}/group/join`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ group_id: groupId, clawid, invite_token: inviteToken }),
    });
    return { status: res.status, data: await res.json() };
  }

  async groupLeave(groupId, clawid, operatorClawid) {
    const res = await fetchWithRetry(`${this.brokerUrl}/group/leave`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify({ group_id: groupId, clawid, operator_clawid: operatorClawid }),
    });
    return { status: res.status, data: await res.json() };
  }

  async groupPeers(groupId) {
    const res = await fetchWithRetry(`${this.brokerUrl}/group/peers?group_id=${encodeURIComponent(groupId)}`, {
      method: 'GET',
      headers: this._headers(),
    });
    return { status: res.status, data: await res.json() };
  }

  async groupSend(payload) {
    const res = await fetchWithRetry(`${this.brokerUrl}/group/send`, {
      method: 'POST',
      headers: this._headers(),
      body: JSON.stringify(payload),
    });
    return { status: res.status, data: await res.json() };
  }
}

export function createClient(config) {
  return new BrokerClient(config.broker_url, config.access_token);
}
