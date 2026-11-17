export const LINGRY_API_ORIGIN = 'https://lingry.net';
export const DEFAULT_LANGUAGE_CODE = 'W'; // Lingry's American English code.
export const LANGUAGE_CODES = new Set('WESGFIRPCAHBJKTVUNMYLDOQXZ'.split(''));
const CANDIDATE_ID_PATTERN = /^cand_[A-Za-z0-9_-]{16,128}$/;
const MAX_RESPONSE_BYTES = 128 * 1024;
const REQUEST_TIMEOUT_MS = 180_000;

export function requireCandidateId(value) {
	if (typeof value !== 'string' || !CANDIDATE_ID_PATTERN.test(value)) {
		throw new Error('Lingry returned an invalid candidate ID.');
	}
	return value;
}

export function requireLanguageCode(value) {
	if (typeof value !== 'string' || !LANGUAGE_CODES.has(value)) {
		throw new Error('Unsupported Lingry language code.');
	}
	return value;
}

export function defaultLanguageCode() {
	return DEFAULT_LANGUAGE_CODE;
}

export function requireCandidate(value) {
	if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Lingry returned an invalid candidate.');
	const candidateId = requireCandidateId(value.candidate_id);
	const languageCode = requireLanguageCode(value.language_code);
	if (candidateId[5] !== languageCode) throw new Error('Lingry returned an invalid candidate.');
	if (typeof value.term !== 'string' || value.term.length < 2 || value.term.length > 64 ||
		typeof value.meaning !== 'string' || !value.meaning || value.meaning.length > 280 ||
		typeof value.part_of_speech !== 'string' || value.part_of_speech.length > 16 ||
		typeof value.candidate_hash !== 'string' || !/^[a-f0-9]{64}$/.test(value.candidate_hash)) {
		throw new Error('Lingry returned an invalid candidate.');
	}
	return {
		candidate_id: candidateId,
		candidate_hash: value.candidate_hash,
		term: value.term,
		meaning: value.meaning,
		part_of_speech: value.part_of_speech,
		language_code: languageCode,
		language_name: typeof value.language_name === 'string' ? value.language_name.slice(0, 120) : '',
		etymology: typeof value.etymology === 'string' ? value.etymology.slice(0, 500) : '',
		expires_at: typeof value.expires_at === 'string' ? value.expires_at : ''
	};
}

export function candidateNextActions() {
	return {
		next_prompt: 'Coin this term, or prompt for another?',
		next_actions: [
			{ id: 'coin_term', label: 'Coin this term', irreversible: true, requires_explicit_publication_intent: true },
			{ id: 'prompt_another', label: 'Prompt for another', irreversible: false, coins_current_candidate: false }
		]
	};
}

function apiUrl(pathname) {
	if (typeof pathname !== 'string' || !pathname.startsWith('/') || pathname.startsWith('//')) throw new Error('Invalid Lingry API path.');
	const url = new URL(pathname, LINGRY_API_ORIGIN);
	if (url.protocol !== 'https:' || url.hostname !== 'lingry.net' || url.origin !== LINGRY_API_ORIGIN) {
		throw new Error('Unexpected Lingry API origin.');
	}
	return url;
}

async function readLimitedJson(response) {
	const reader = response.body?.getReader();
	if (!reader) throw new Error('Lingry returned an invalid response.');
	const chunks = [];
	let size = 0;
	while (true) {
		const { done, value } = await reader.read();
		if (done) break;
		size += value.byteLength;
		if (size > MAX_RESPONSE_BYTES) {
			await reader.cancel();
			throw new Error('Lingry returned an oversized response.');
		}
		chunks.push(value);
	}
	const bytes = new Uint8Array(size);
	let offset = 0;
	for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
	try { return JSON.parse(new TextDecoder().decode(bytes)); }
	catch { throw new Error('Lingry returned an invalid JSON response.'); }
}

async function lingryApi(pathname, options = {}, safeError = 'Lingry request failed.') {
	const controller = new AbortController();
	const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
	try {
		const response = await fetch(apiUrl(pathname), {
			method: options.method || 'GET',
			headers: { 'content-type': 'application/json', ...(options.headers || {}) },
			body: options.body === undefined ? undefined : JSON.stringify(options.body),
			redirect: 'error',
			signal: controller.signal
		});
		const json = await readLimitedJson(response);
		if (!response.ok || json?.ok !== true) {
			const error = new Error(safeError);
			error.status = response.status;
			error.code = typeof json?.error?.code === 'string' ? json.error.code : '';
			throw error;
		}
		return json.data;
	} catch (error) {
		if (error.status) throw error;
		throw new Error(error.name === 'AbortError' ? 'Lingry request timed out.' : safeError);
	} finally { clearTimeout(timer); }
}

export function readHealth() {
	return lingryApi('/v1/healthz', {}, 'Lingry health check failed.');
}

function requireReadLimit(value) {
	if (!Number.isInteger(value) || value < 1 || value > 100) throw new Error('Limit must be an integer from 1 to 100.');
	return value;
}

export function readStream(limit) {
	return lingryApi(`/v1/stream?limit=${requireReadLimit(limit)}`, {}, 'Lingry public read failed.');
}

export function readLeaderboard(limit) {
	return lingryApi(`/v1/leaderboard?limit=${requireReadLimit(limit)}`, {}, 'Lingry public read failed.');
}

export function readWords(languageCode) {
	return lingryApi(`/v1/words?language_code=${requireLanguageCode(languageCode)}&limit=100`, {}, 'Lingry public read failed.');
}

export async function generateCandidate(concept, languageCode = defaultLanguageCode()) {
	if (typeof concept !== 'string' || !concept.trim() || concept.length > 500) throw new Error('A concept of at most 500 characters is required.');
	const data = await lingryApi('/v1/openclaw/generations', { method: 'POST', body: { concept_prompt: concept.trim(), language_code: requireLanguageCode(languageCode) } }, 'Lingry could not generate a candidate.');
	return requireCandidate(data?.candidate);
}

export async function coinCandidate(candidateId) {
	const id = requireCandidateId(candidateId);
	const result = await lingryApi(`/v1/openclaw/candidates/${id}/coin`, { method: 'POST', headers: { 'idempotency-key': `clawhub-${id}` }, body: {} }, 'Lingry could not complete publication.');
	if (result?.candidate_id !== id || typeof result.txid !== 'string' || !/^[a-fA-F0-9]{64}$/.test(result.txid)) {
		throw new Error('Lingry returned an invalid publication result.');
	}
	return { candidate_id: id, txid: result.txid, status: result.status || 'pending', publisher_address: result.publisher_address || '', word: result.word || '', meaning: result.meaning || '' };
}
