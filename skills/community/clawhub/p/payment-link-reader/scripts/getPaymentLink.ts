#!/usr/bin/env npx tsx
/**
 * Payment Link Reader - Fetch product info from payment links
 *
 * Calls GStable API: GET /payment/link/:linkId
 * Docs: https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/
 *
 * Usage:
 *   npx tsx scripts/getPaymentLink.ts <link_id>
 *   npm run get-link -- <link_id>
 *
 * Example:
 *   npx tsx scripts/getPaymentLink.ts lnk_example_premium_plan_01
 */

const API_BASE = process.env.GSTABLE_API_BASE_URL || 'https://aipay.gstable.io/api/v1';

interface ProductData {
  productName: string;
  productDescription?: string;
  imageUrl?: string;
  attributes?: Array<{ name: string; value: string }>;
}

interface LineItem {
  quantity: number;
  productData: ProductData;
  unitPriceInUSD: string;
}

interface SupportedToken {
  chainName: string;
  chainId: string;
  tokenAddress: string;
  name: string;
  symbol: string;
  decimals: number;
  amountInToken: string;
  amountInUSD: string;
}

interface ApiResponse {
  code?: number;
  data?: RawLinkData;
  message?: string;
}

interface RawLinkData {
  linkId: string;
  linkVersion?: string;
  linkName: string;
  merchantId?: string;
  lineItems: LineItem[];
  aiView?: {
    supportedPaymentTokens?: SupportedToken[];
    pricingModel?: { type: string };
  };
}

interface ProductInfo {
  name: string;
  description?: string;
  imageUrl?: string;
  quantity: number;
  unitPriceUSD: string;
  attributes?: Array<{ name: string; value: string }>;
}

interface Output {
  linkId: string;
  linkName: string;
  products: ProductInfo[];
  supportedPaymentTokens?: Array<{
    symbol: string;
    chainName: string;
    chainId: string;
    amountInUSD: string;
  }>;
}

async function getPaymentLink(linkId: string): Promise<Output> {
  const url = `${API_BASE.replace(/\/$/, '')}/payment/link/${linkId}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
  });

  const json: ApiResponse = await res.json();

  if (json.code !== 0 && json.code !== undefined) {
    throw new Error(`API Error: ${json.message || 'Unknown'} (code: ${json.code})`);
  }

  const data: RawLinkData = json.data || (json as unknown as RawLinkData);

  if (!data?.lineItems) {
    throw new Error('Invalid response: missing lineItems');
  }

  const products: ProductInfo[] = data.lineItems.map((item) => ({
    name: item.productData?.productName || 'Unknown',
    description: item.productData?.productDescription,
    imageUrl: item.productData?.imageUrl,
    quantity: item.quantity ?? 1,
    unitPriceUSD: item.unitPriceInUSD ?? '0',
    attributes: item.productData?.attributes,
  }));

  const tokens = data.aiView?.supportedPaymentTokens?.map((t) => ({
    symbol: t.symbol,
    chainName: t.chainName,
    chainId: t.chainId,
    amountInUSD: t.amountInUSD,
  }));

  return {
    linkId: data.linkId,
    linkName: data.linkName || 'Unnamed',
    products,
    supportedPaymentTokens: tokens || [],
  };
}

function isValidLinkId(id: string): boolean {
  return /^lnk_[a-zA-Z0-9_]+$/.test(id);
}

/** Extract link_id from URL or raw link_id string */
function extractLinkId(input: string): string | null {
  const trimmed = input.trim();
  if (isValidLinkId(trimmed)) return trimmed;
  // Supports https://pay.gstable.io/link/lnk_xxx or https://aipay.gstable.io/.../link/lnk_xxx
  const match = trimmed.match(/\/link\/(lnk_[a-zA-Z0-9_]+)/);
  return match ? match[1] : null;
}

async function main() {
  const args = process.argv.slice(2);
  const rawInput = args[0];

  if (!rawInput) {
    console.error(`
Usage: npx tsx scripts/getPaymentLink.ts <link_id|url>

Parameters:
  link_id  Payment link ID (lnk_xxx) or full URL

Examples:
  npm run get-link -- lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua
  npm run get-link -- "https://pay.gstable.io/link/lnk_xxx"

Environment variables:
  GSTABLE_API_BASE_URL  Optional, API base URL, default https://aipay.gstable.io/api/v1
`);
    process.exit(1);
  }

  const parsed = extractLinkId(rawInput);
  if (!parsed) {
    console.error('Error: Please provide a valid link_id (lnk_xxx) or full payment link URL');
    process.exit(1);
  }

  try {
    const result = await getPaymentLink(parsed!);
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error('Request failed:', e instanceof Error ? e.message : e);
    process.exit(1);
  }
}

main();
