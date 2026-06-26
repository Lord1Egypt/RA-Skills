import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { searchProducts, getProductPrice, buyDigitalProduct, getPricing, getExchangeRates } from './tools/shopping.js';
import { getWalletBalance, getTransactions, buyWithWallet, getOrders, getOrder, submitEnquiry, getEnquiries, getEnquiry, replyToEnquiry, closeEnquiry } from './tools/account.js';
import { createTokenUrl } from './lib/l402.js';

const server = new Server(
	{ name: 'playasia', version: '0.1.0' },
	{ capabilities: { tools: {} } },
);

// ── Tool definitions ──

const TOOLS = [
	// Shopping (L402 — works without token)
	{
		name: 'search_products',
		description: 'Search Play-Asia\'s catalog of digital products (game codes, eShop cards, PSN vouchers, Roblox, etc.). Returns products with prices in USD and satoshis, cover image URLs, and popularity rank. Free, no token needed.',
		inputSchema: {
			type: 'object' as const,
			properties: {
				query: { type: 'string', description: 'Search query (e.g. "Nintendo eShop 5000 yen", "PSN 50 USD", "Roblox")' },
				limit: { type: 'number', description: 'Max results (default 20, max 200)' },
				offset: { type: 'number', description: 'Pagination offset' },
				currency: { type: 'string', description: 'Optional: add local currency prices (e.g. "EUR", "JPY", "GBP")' },
			},
		},
	},
	{
		name: 'get_product_price',
		description: 'Get the current price for a specific digital product by PAX code. Returns price in USD and satoshis, cover image URL, and stock status. Free.',
		inputSchema: {
			type: 'object' as const,
			required: ['pax'],
			properties: {
				pax: { type: 'string', description: 'PAX product code (e.g. "PAX0004012102")' },
			},
		},
	},
	{
		name: 'buy_digital_product',
		description: `Buy a digital product (game code, eShop card, PSN voucher, etc.) using Lightning Network (L402 protocol).

Two-step flow:
1. Call without l402_token → returns a Lightning invoice with the price in sats
2. Pay the invoice with any Lightning wallet to get the preimage
3. Call again with l402_token = "MACAROON:PREIMAGE" → receive the digital code instantly

No account needed. Fully autonomous agent purchase via Bitcoin Lightning.`,
		inputSchema: {
			type: 'object' as const,
			required: ['pax'],
			properties: {
				pax: { type: 'string', description: 'PAX product code to purchase' },
				l402_token: { type: 'string', description: 'L402 auth token: "MACAROON:PREIMAGE" — from paying the Lightning invoice returned by a previous call' },
			},
		},
	},
	{
		name: 'get_pricing',
		description: 'Get current L402 pricing for all API resources. Most are free. The buy_digital_product tool costs the actual product price in satoshis.',
		inputSchema: { type: 'object' as const, properties: {} },
	},
	{
		name: 'get_exchange_rates',
		description: 'Get BTC/fiat exchange rates for 30+ currencies, plus crypto rates (ETH, SOPH) in USD/sats/BTC. L402-gated (~1 sat). Useful for converting sats prices to local currency.',
		inputSchema: {
			type: 'object' as const,
			properties: {
				l402_token: { type: 'string', description: 'L402 auth token if previously paid' },
			},
		},
	},

	// Wallet + Account tools (require PA_TOKEN)
	{
		name: 'get_wallet_balance',
		description: `Get your Play-Asia wallet balance. Use this to check funds before purchasing with buy_with_wallet. Requires PA_TOKEN (generate at ${createTokenUrl()}).`,
		inputSchema: { type: 'object' as const, properties: {} },
	},
	{
		name: 'get_transactions',
		description: `Get your wallet transaction history. Shows top-ups and purchases. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			properties: {
				limit: { type: 'number', description: 'Max results (default 20, max 100)' },
				offset: { type: 'number', description: 'Pagination offset' },
			},
		},
	},
	{
		name: 'buy_with_wallet',
		description: `Buy a digital product using your Play-Asia wallet balance. The token must have "purchase" scope and sufficient balance. Fully autonomous — no redirect needed. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			required: ['pax'],
			properties: {
				pax: { type: 'string', description: 'PAX product code to purchase' },
			},
		},
	},
	{
		name: 'get_orders',
		description: `List your recent orders. Requires PA_TOKEN (generate at ${createTokenUrl()}).`,
		inputSchema: {
			type: 'object' as const,
			properties: {
				limit: { type: 'number', description: 'Max results (default 20, max 100)' },
				offset: { type: 'number', description: 'Pagination offset' },
			},
		},
	},
	{
		name: 'get_order',
		description: `Get full order details including items, status, and purchased digital codes. Use this to retrieve codes after a purchase. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			required: ['order_id'],
			properties: {
				order_id: { type: 'number', description: 'Order ID' },
			},
		},
	},
	{
		name: 'submit_enquiry',
		description: `Submit a customer service enquiry/ticket. Requires PA_TOKEN. Use #ORDER_ID (e.g. "#12345678") as reference for order-related issues.`,
		inputSchema: {
			type: 'object' as const,
			required: ['subject', 'message', 'reference'],
			properties: {
				subject: { type: 'string', description: 'Ticket subject' },
				message: { type: 'string', description: 'Your message' },
				reference: { type: 'string', description: 'Reference — use #ORDER_ID for order issues (e.g. "#12345678"), or free text' },
				attachments: {
					type: 'array',
					description: 'Optional file attachments (max 5, max 5MB each)',
					items: {
						type: 'object',
						required: ['filename', 'content_type', 'data'],
						properties: {
							filename: { type: 'string', description: 'File name' },
							content_type: { type: 'string', description: 'MIME type (e.g. "image/png")' },
							data: { type: 'string', description: 'Base64-encoded file content' },
						},
					},
				},
			},
		},
	},
	{
		name: 'get_enquiries',
		description: `List your customer service tickets. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			properties: {
				status: { type: 'string', enum: ['open', 'closed'], description: 'Filter by status' },
			},
		},
	},
	{
		name: 'get_enquiry',
		description: `Get a specific ticket with full conversation thread. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			required: ['ticket_id'],
			properties: {
				ticket_id: { type: 'number', description: 'Ticket ID' },
			},
		},
	},
	{
		name: 'reply_to_enquiry',
		description: `Reply to an existing customer service ticket. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			required: ['ticket_id', 'message'],
			properties: {
				ticket_id: { type: 'number', description: 'Ticket ID to reply to' },
				message: { type: 'string', description: 'Your reply message' },
			},
		},
	},
	{
		name: 'close_enquiry',
		description: `Close/resolve an open customer service ticket. Requires PA_TOKEN.`,
		inputSchema: {
			type: 'object' as const,
			required: ['ticket_id'],
			properties: {
				ticket_id: { type: 'number', description: 'Ticket ID to close' },
			},
		},
	},
];

// ── Handlers ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
	tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
	const { name, arguments: args = {} } = request.params;

	try {
		let result: string;

		switch (name) {
			// Shopping (L402)
			case 'search_products':
				result = await searchProducts(args as Parameters<typeof searchProducts>[0]);
				break;
			case 'get_product_price':
				result = await getProductPrice(args as Parameters<typeof getProductPrice>[0]);
				break;
			case 'buy_digital_product':
				result = await buyDigitalProduct(args as Parameters<typeof buyDigitalProduct>[0]);
				break;
			case 'get_pricing':
				result = await getPricing();
				break;
			case 'get_exchange_rates':
				result = await getExchangeRates(args as Parameters<typeof getExchangeRates>[0]);
				break;

			// Account (platform token)
			case 'get_wallet_balance':
				result = await getWalletBalance();
				break;
			case 'get_transactions':
				result = await getTransactions(args as Parameters<typeof getTransactions>[0]);
				break;
			case 'buy_with_wallet':
				result = await buyWithWallet(args as Parameters<typeof buyWithWallet>[0]);
				break;
			case 'get_orders':
				result = await getOrders(args as Parameters<typeof getOrders>[0]);
				break;
			case 'get_order':
				result = await getOrder(args as Parameters<typeof getOrder>[0]);
				break;
			case 'submit_enquiry':
				result = await submitEnquiry(args as Parameters<typeof submitEnquiry>[0]);
				break;
			case 'get_enquiries':
				result = await getEnquiries(args as Parameters<typeof getEnquiries>[0]);
				break;
			case 'get_enquiry':
				result = await getEnquiry(args as Parameters<typeof getEnquiry>[0]);
				break;
			case 'reply_to_enquiry':
				result = await replyToEnquiry(args as Parameters<typeof replyToEnquiry>[0]);
				break;
			case 'close_enquiry':
				result = await closeEnquiry(args as Parameters<typeof closeEnquiry>[0]);
				break;

			default:
				return {
					content: [{ type: 'text', text: `Unknown tool: ${name}` }],
					isError: true,
				};
		}

		return {
			content: [{ type: 'text', text: result }],
		};
	} catch (err) {
		const message = err instanceof Error ? err.message : String(err);
		return {
			content: [{ type: 'text', text: `Error: ${message}` }],
			isError: true,
		};
	}
});

// ── Start ──

const transport = new StdioServerTransport();
await server.connect(transport);
