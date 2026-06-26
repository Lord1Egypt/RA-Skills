import { l402Fetch, createTokenUrl } from '../lib/l402.js';
import type { L402PaymentRequired } from '../lib/types.js';

/** Search the Play-Asia digital product catalog */
export async function searchProducts(args: {
	query?: string;
	limit?: number;
	offset?: number;
	currency?: string;
}): Promise<string> {
	const params: Record<string, string> = {};
	if (args.query) { params.q = args.query; }
	if (args.limit) { params.limit = String(Math.min(args.limit, 200)); }
	if (args.offset) { params.offset = String(args.offset); }
	if (args.currency) { params.currency = args.currency; }

	const result = await l402Fetch('catalog', params);
	if (result.status === 'payment_required') {
		return JSON.stringify(result); // shouldn't happen — catalog is free
	}
	return JSON.stringify(result.data);
}

/** Get current price for a product by PAX code */
export async function getProductPrice(args: { pax: string }): Promise<string> {
	const result = await l402Fetch('price', { pax: args.pax });
	if (result.status === 'payment_required') {
		return JSON.stringify(result);
	}
	return JSON.stringify(result.data);
}

/** Buy a digital product via Lightning L402 payment */
export async function buyDigitalProduct(args: {
	pax: string;
	l402_token?: string;
}): Promise<string> {
	const result = await l402Fetch('product', { pax: args.pax }, args.l402_token);

	if (result.status === 'payment_required') {
		const pr = result as L402PaymentRequired;
		return JSON.stringify({
			payment_required: true,
			price_sats: pr.price_sats,
			lightning_invoice: pr.invoice,
			macaroon: pr.macaroon,
			payment_hash: pr.payment_hash,
			expires_at: pr.expires,
			instruction: `Pay the Lightning invoice, then call buy_digital_product again with l402_token = "${pr.macaroon}:PREIMAGE" (replace PREIMAGE with the hex preimage from your Lightning wallet).`,
		});
	}

	return JSON.stringify(result.data);
}

/** Get L402 resource pricing */
export async function getPricing(): Promise<string> {
	const result = await l402Fetch('pricing');
	if (result.status === 'ok') {
		return JSON.stringify(result.data);
	}
	return JSON.stringify(result);
}

/** Get BTC exchange rates (L402-gated, ~$0.001) */
export async function getExchangeRates(args: {
	l402_token?: string;
}): Promise<string> {
	const result = await l402Fetch('btc/rates', {}, args.l402_token);
	if (result.status === 'payment_required') {
		const pr = result as L402PaymentRequired;
		return JSON.stringify({
			payment_required: true,
			price_sats: pr.price_sats,
			lightning_invoice: pr.invoice,
			macaroon: pr.macaroon,
			payment_hash: pr.payment_hash,
			expires_at: pr.expires,
			instruction: `Pay the Lightning invoice, then call get_exchange_rates again with l402_token = "${pr.macaroon}:PREIMAGE".`,
		});
	}
	return JSON.stringify(result.data);
}

/** Require-token helper text for tools that need auth */
export const TOKEN_REQUIRED_MSG = `This tool requires a PA Platform token. Generate one at: ${createTokenUrl()}\nThen add PA_TOKEN to your MCP server config.`;
