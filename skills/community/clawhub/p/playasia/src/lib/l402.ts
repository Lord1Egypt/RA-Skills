import type { L402Result } from './types.js';

const BASE_URL = process.env.PA_BASE_URL || 'https://www.play-asia.com';

/**
 * Build a versioned URL path: /l402/v1/{action}?params
 */
function buildUrl(action: string, params: Record<string, string> = {}): URL {
	const url = new URL(`/l402/v1/${action}`, BASE_URL);
	for (const [k, v] of Object.entries(params)) {
		if (v !== undefined && v !== '') {
			url.searchParams.set(k, v);
		}
	}
	return url;
}

/**
 * Make a request to the PA L402 endpoint.
 * Handles 402 (payment required) responses transparently.
 */
export async function l402Fetch(
	action: string,
	params: Record<string, string> = {},
	l402Token?: string,
): Promise<L402Result> {
	const url = buildUrl(action, params);

	const headers: Record<string, string> = {
		'Accept': 'application/json',
		'User-Agent': 'playasia-mcp/0.1.0',
	};

	if (l402Token) {
		headers['Authorization'] = `L402 ${l402Token}`;
	}

	const res = await fetch(url.toString(), { headers });

	if (res.status === 402) {
		const body = await res.json() as Record<string, unknown>;
		return {
			status: 'payment_required',
			resource: body.resource as string,
			price_sats: body.price_sat as number,
			invoice: body.invoice as string,
			macaroon: body.macaroon as string,
			payment_hash: body.payment_hash as string,
			expires: body.expires as number,
		};
	}

	if (!res.ok) {
		const body = await res.json().catch(() => ({})) as Record<string, unknown>;
		throw new Error((body.message as string) || `HTTP ${res.status}`);
	}

	return { status: 'ok', data: await res.json() };
}

/**
 * Make a request to a PA L402 authenticated endpoint (platform token).
 */
export async function platformFetch(
	action: string,
	params: Record<string, string> = {},
	token: string,
	method: 'GET' | 'POST' = 'GET',
	body?: Record<string, unknown>,
): Promise<Record<string, unknown>> {
	const url = buildUrl(action, params);

	const headers: Record<string, string> = {
		'Accept': 'application/json',
		'User-Agent': 'playasia-mcp/0.1.0',
		'X-PA-Token': token,
	};

	const init: RequestInit = { method, headers };
	if (body && method === 'POST') {
		headers['Content-Type'] = 'application/json';
		init.body = JSON.stringify(body);
	}

	const res = await fetch(url.toString(), init);
	const data = await res.json() as Record<string, unknown>;

	if (!res.ok) {
		throw new Error(
			(data.message as string) || (data.error as string) || `HTTP ${res.status}`,
		);
	}

	return data;
}

/** URL where users generate platform tokens */
export function createTokenUrl(): string {
	return `${BASE_URL}/account/access-tokens`;
}
