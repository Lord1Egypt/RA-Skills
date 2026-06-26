/** L402 payment required response — agent must pay the Lightning invoice */
export interface L402PaymentRequired {
	status: 'payment_required';
	resource: string;
	price_sats: number;
	invoice: string;
	macaroon: string;
	payment_hash: string;
	expires: number;
}

/** Successful L402/API response */
export interface L402Success {
	status: 'ok';
	data: unknown;
}

export type L402Result = L402PaymentRequired | L402Success;

/** Auth error — agent needs a platform token */
export interface AuthError {
	error: string;
	create_token_url?: string;
	message?: string;
}

/** Product from catalog search */
export interface CatalogProduct {
	pax: string;
	name: string;
	prod_code: string;
	version: string;
	version_code: string;
	/** Cover image URL (CDN), null if product has no image */
	image_url: string | null;
	/** Popularity rank — lower = more popular, null if unranked */
	rank: number | null;
	price: {
		usd: number;
		sats: number;
		btc: number;
		[currency: string]: number | undefined;
	};
	in_stock: number;
	buy_url: string;
	steam_code?: string;
}

/** Digital product delivery */
export interface DigitalDelivery {
	status: string;
	product: string;
	code?: string;
	type?: string;
	data?: string;
	content_type?: string;
	order_id: number;
}
