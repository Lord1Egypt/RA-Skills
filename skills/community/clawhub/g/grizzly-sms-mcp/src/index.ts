import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { createServer } from 'node:http';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import dotenv from 'dotenv';
import { GrizzlySMSClient } from './grizzly-sms-client.js';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __dirname = dirname(fileURLToPath(import.meta.url));

const API_KEY = process.env.GRIZZLY_SMS_API_KEY || process.env.SMS_ACTIVATE_API_KEY;
const BASE_URL = process.env.GRIZZLY_SMS_BASE_URL || process.env.SMS_ACTIVATE_BASE_URL || 'https://api.grizzlysms.com';

if (!API_KEY) {
  console.error('GRIZZLY_SMS_API_KEY or SMS_ACTIVATE_API_KEY environment variable is required');
  process.exit(1);
}

const client = new GrizzlySMSClient(API_KEY, BASE_URL);

const servicesData = JSON.parse(
  readFileSync(join(__dirname, '../docs/services.json'), 'utf-8')
);

const serviceMap = new Map<string, string>(servicesData.map((s: any) => [s.name.toLowerCase(), s.code]));

const server = new Server(
  {
    name: 'mcp-grizzly-sms',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

//const GetBalanceSchema = z.object({});

const RequestNumberSchema = z.object({
  service: z.string().describe('Service code or name (e.g., "tg", "Telegram", "wa", "WhatsApp")'),
  country: z.union([z.number(), z.string()]).optional().describe('Country ID (e.g., 0 for Russia) or "*" or "any" for any country'),
  operator: z.string().optional().describe('Operator name'),
  forward: z.number().optional().describe('Forward option (0 or 1)'),
  ref: z.string().optional().describe('Referral code'),
  ref_id: z.string().optional().describe('Referral ID'),
  maxPrice: z.number().optional().describe('Maximum price'),
  providerIds: z.string().optional().describe('Comma-separated provider IDs'),
  exceptProviderIds: z.string().optional().describe('Comma-separated provider IDs to exclude'),
  phoneException: z.string().optional().describe('Comma-separated phone numbers to exclude'),
  activationType: z.number().optional().describe('Activation type (1, 2, 3, or 4)'),
        version: z.enum(['v1', 'v2']).optional().describe('API version (v1=plain text, v2=JSON with details)'),
});

const SetStatusSchema = z.object({
  activationId: z.string().describe('Activation ID'),
  status: z.number().describe('Status code: 1=report SMS sent, 3=request another code, 6=complete activation, 8=cancel activation'),
});

const GetStatusSchema = z.object({
  activationId: z.string().describe('Activation ID'),
});

const GetPricesSchema = z.object({
  country: z.union([z.number(), z.string()]).optional().describe('Country ID or "*" for any country'),
  service: z.string().optional().describe('Service code'),
  version: z.enum(['v1', 'v2', 'v3']).optional().describe('API version (v1, v2, or v3)'),
});

//const GetCountriesSchema = z.object({});

//onst GetServicesSchema = z.object({});

const tools: Tool[] = [
  {
    name: 'get_balance',
    description: 'Get account balance',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'get_wallet',
    description: 'Get USDT TRC-20 crypto wallet address for balance top-up. Send USDT to this address (min 50 USD). Funds credit automatically.',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'request_number',
    description: 'Request a phone number for SMS verification',
    inputSchema: {
      type: 'object',
      properties: {
        service: { type: 'string', description: 'Service code or name (e.g., "tg", "Telegram", "wa", "WhatsApp")' },
        country: { type: 'string', description: 'Country ID (e.g., 0 for Russia) or "*" or "any" for any country' },
        operator: { type: 'string', description: 'Operator name' },
        forward: { type: 'number', description: 'Forward option (0 or 1)' },
        ref: { type: 'string', description: 'Referral code' },
        ref_id: { type: 'string', description: 'Referral ID' },
        maxPrice: { type: 'number', description: 'Maximum price' },
        providerIds: { type: 'string', description: 'Comma-separated provider IDs' },
        exceptProviderIds: { type: 'string', description: 'Comma-separated provider IDs to exclude' },
        phoneException: { type: 'string', description: 'Comma-separated phone numbers to exclude' },
        activationType: { type: 'number', description: 'Activation type (1, 2, 3, or 4)' },
        version: { type: 'string', enum: ['v1', 'v2'], description: 'API version (v1=plain text, v2=JSON with details)' },
      },
      required: ['service'],
    },
  },
  {
    name: 'set_status',
    description: 'Change activation status',
    inputSchema: {
      type: 'object',
      properties: {
        activationId: { type: 'string', description: 'Activation ID' },
        status: { type: 'number', description: 'Status code: 1=report SMS sent, 3=request another code, 6=complete activation, 8=cancel activation' },
      },
      required: ['activationId', 'status'],
    },
  },
  {
    name: 'get_status',
    description: 'Get activation status and SMS code',
    inputSchema: {
      type: 'object',
      properties: {
        activationId: { type: 'string', description: 'Activation ID' },
      },
      required: ['activationId'],
    },
  },
  {
    name: 'get_prices',
    description: 'Get prices for services by country',
    inputSchema: {
      type: 'object',
      properties: {
        country: { type: 'string', description: 'Country ID or "*" for any country' },
        service: { type: 'string', description: 'Service code' },
        version: { type: 'string', enum: ['v1', 'v2', 'v3'], description: 'API version (v1, v2, or v3)' },
      },
    },
  },
  {
    name: 'get_countries',
    description: 'Get list of available countries',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'get_services',
    description: 'Get list of available services',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
  const { name, arguments: args = {} } = request.params;

  try {
    switch (name) {
      case 'get_balance': {
        const balance = await client.getBalance();
        return {
          content: [
            {
              type: 'text',
              text: `Balance: ${balance.balance} ${balance.currency}`,
            },
          ],
        };
      }

      case 'get_wallet': {
        const wallet = await client.getWallet();
        return {
          content: [
            {
              type: 'text',
              text: `USDT TRC-20 wallet: ${wallet.wallet_address}\nMinimum top-up: 50 USD. Funds credit automatically to your Grizzly balance.`,
            },
          ],
        };
      }

      case 'request_number': {
        const params = RequestNumberSchema.parse(args);
        
        let serviceCode = params.service;
        const serviceLower = params.service.toLowerCase();
        if (serviceMap.has(serviceLower)) {
          serviceCode = serviceMap.get(serviceLower)!;
        }
        
        const result = await client.getNumber({
          service: serviceCode,
          country: params.country,
          operator: params.operator,
          forward: params.forward,
          ref: params.ref,
          ref_id: params.ref_id,
          maxPrice: params.maxPrice,
          providerIds: params.providerIds,
          exceptProviderIds: params.exceptProviderIds,
          phoneException: params.phoneException,
          activationType: params.activationType,
        }, params.version || 'v1');
        
        let responseText = `Phone number requested successfully!\nActivation ID: ${result.activationId}\nPhone: ${result.phone}`;
        
        // Add additional info for v2 responses
        if (params.version === 'v2') {
          if (result.activationCost) {
            responseText += `\nCost: ${result.activationCost}`;
          }
          if (result.currency) {
            responseText += `\nCurrency: ${result.currency}`;
          }
          if (result.countryCode) {
            responseText += `\nCountry Code: ${result.countryCode}`;
          }
          if (result.canGetAnotherSms) {
            responseText += `\nCan Get Another SMS: ${result.canGetAnotherSms}`;
          }
          if (result.activationTime) {
            responseText += `\nActivation Time: ${result.activationTime}`;
          }
        }
        
        return {
          content: [
            {
              type: 'text',
              text: responseText,
            },
          ],
        };
      }

      case 'set_status': {
        const params = SetStatusSchema.parse(args);
        const result = await client.setStatus(params.activationId, params.status);
        return {
          content: [
            {
              type: 'text',
              text: `Status updated: ${result.status}`,
            },
          ],
        };
      }

      case 'get_status': {
        const params = GetStatusSchema.parse(args);
        const result = await client.getStatus(params.activationId);
        
        let message = `Status: ${result.status}`;
        if (result.code) {
          message += `\nCode: ${result.code}`;
        }
        
        return {
          content: [
            {
              type: 'text',
              text: message,
            },
          ],
        };
      }

      case 'get_prices': {
        const params = GetPricesSchema.parse(args);
        const prices = await client.getPrices(params.country, params.service, params.version || 'v1');
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(prices, null, 2),
            },
          ],
        };
      }

      case 'get_countries': {
        const countries = await client.getCountries();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(countries, null, 2),
            },
          ],
        };
      }

      case 'get_services': {
        const services = await client.getServices();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(services, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
    };
  }
});

async function readBody(req: import('node:http').IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  const raw = Buffer.concat(chunks).toString('utf-8');
  if (!raw) return undefined;
  try {
    return JSON.parse(raw);
  } catch {
    return undefined;
  }
}

async function main() {
  const transportMode = process.env.MCP_TRANSPORT || 'stdio';

  if (transportMode === 'http') {
    const port = parseInt(process.env.MCP_PORT || '3000', 10);
    const transport = new StreamableHTTPServerTransport();
    await server.connect(transport);

    const httpServer = createServer(async (req, res) => {
      if (req.url && !req.url.startsWith('/mcp') && req.url !== '/' && !req.url.startsWith('/?')) {
        res.statusCode = 404;
        res.end();
        return;
      }
      try {
        let parsedBody: unknown;
        if (req.method === 'POST') {
          parsedBody = await readBody(req);
        }
        await transport.handleRequest(req as any, res, parsedBody);
      } catch (err) {
        console.error('Request error:', err);
        res.statusCode = 500;
        res.end();
      }
    });

    httpServer.listen(port, '0.0.0.0', () => {
      console.error(`Grizzly SMS MCP server listening on http://0.0.0.0:${port}/mcp`);
    });
  } else {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('Grizzly SMS MCP server running (stdio)...');
  }
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});