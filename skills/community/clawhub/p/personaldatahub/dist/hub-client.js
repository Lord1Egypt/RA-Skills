/**
 * Thin HTTP client wrapping the PersonalDataHub App API endpoints.
 * The skill does not know about manifests or policies — it simply
 * sends requests with a `purpose` string. The Hub resolves the policy internally.
 */
export class HubClient {
    hubUrl;
    apiKey;
    constructor(config) {
        this.hubUrl = config.hubUrl.replace(/\/+$/, '');
        this.apiKey = config.apiKey;
    }
    /**
     * Pull data from a source through PersonalDataHub.
     * The Hub applies the owner's manifest/policy to filter, redact, and shape the data.
     */
    async pull(params) {
        const res = await fetch(`${this.hubUrl}/app/v1/pull`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
            },
            body: JSON.stringify(params),
        });
        if (!res.ok) {
            const text = await res.text();
            throw new HubApiError('pull', res.status, text);
        }
        return res.json();
    }
    /**
     * Propose an outbound action through PersonalDataHub staging.
     * The action goes to the owner's staging queue for review before execution.
     */
    async propose(params) {
        const res = await fetch(`${this.hubUrl}/app/v1/propose`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
            },
            body: JSON.stringify(params),
        });
        if (!res.ok) {
            const text = await res.text();
            throw new HubApiError('propose', res.status, text);
        }
        return res.json();
    }
}
export class HubApiError extends Error {
    endpoint;
    statusCode;
    body;
    constructor(endpoint, statusCode, body) {
        super(`PersonalDataHub API error on ${endpoint}: ${statusCode} - ${body}`);
        this.endpoint = endpoint;
        this.statusCode = statusCode;
        this.body = body;
        this.name = 'HubApiError';
    }
}
