import { platformFetch, createTokenUrl } from '../lib/l402.js';

const NO_TOKEN = JSON.stringify({
	error: 'no_token',
	message: `PA Platform token not configured. Generate one at: ${createTokenUrl()}`,
	create_token_url: createTokenUrl(),
});

function requireToken(): string | null {
	const token = process.env.PA_TOKEN;
	if (!token) { return NO_TOKEN; }
	return null;
}

/** Get wallet balance */
export async function getWalletBalance(): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch('account/balance', {}, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Get wallet transaction history */
export async function getTransactions(args: {
	limit?: number;
	offset?: number;
}): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const params: Record<string, string> = {};
	if (args.limit) { params.limit = String(args.limit); }
	if (args.offset) { params.offset = String(args.offset); }

	const data = await platformFetch('account/transactions', params, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Buy a digital product using wallet balance */
export async function buyWithWallet(args: { pax: string }): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch(
		'account/buy', {},
		process.env.PA_TOKEN!, 'POST',
		{ pax: args.pax },
	);
	return JSON.stringify(data);
}

/** List recent orders */
export async function getOrders(args: {
	limit?: number;
	offset?: number;
}): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const params: Record<string, string> = {};
	if (args.limit) { params.limit = String(args.limit); }
	if (args.offset) { params.offset = String(args.offset); }

	const data = await platformFetch('account/orders', params, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Get order details */
export async function getOrder(args: { order_id: number }): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch('account/order', { oid: String(args.order_id) }, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Submit a customer service enquiry */
export async function submitEnquiry(args: {
	subject: string;
	message: string;
	reference: string;
	attachments?: Array<{ filename: string; content_type: string; data: string }>;
}): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const body: Record<string, unknown> = {
		subject: args.subject,
		message: args.message,
		reference: args.reference,
	};
	if (args.attachments?.length) { body.attachments = args.attachments; }

	const data = await platformFetch('cs/submit', {}, process.env.PA_TOKEN!, 'POST', body);
	return JSON.stringify(data);
}

/** List my enquiries/tickets */
export async function getEnquiries(args: {
	status?: string;
}): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const params: Record<string, string> = {};
	if (args.status) { params.status = args.status; }

	const data = await platformFetch('cs/enquiries', params, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Get enquiry details with full thread */
export async function getEnquiry(args: { ticket_id: number }): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch('cs/enquiry', { id: String(args.ticket_id) }, process.env.PA_TOKEN!);
	return JSON.stringify(data);
}

/** Reply to an existing enquiry */
export async function replyToEnquiry(args: {
	ticket_id: number;
	message: string;
}): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch(
		'cs/reply', {},
		process.env.PA_TOKEN!, 'POST',
		{ ticket_id: args.ticket_id, message: args.message },
	);
	return JSON.stringify(data);
}

/** Close/resolve an open enquiry */
export async function closeEnquiry(args: { ticket_id: number }): Promise<string> {
	const err = requireToken();
	if (err) { return err; }

	const data = await platformFetch(
		'cs/close', {},
		process.env.PA_TOKEN!, 'POST',
		{ ticket_id: args.ticket_id },
	);
	return JSON.stringify(data);
}
