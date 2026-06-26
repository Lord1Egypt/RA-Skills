#!/usr/bin/env bun
import { PayNodeAgentClient, RequestOptions } from '@paynodelabs/sdk-js';
import { parseArgs, getPrivateKey, resolveNetwork, reportError, EXIT_CODES } from './utils.ts';

async function main() {
    const args = parseArgs();

    if (args.isHelp || args.params.length < 1) {
        console.log(
            `
Usage: bun run scripts/request.ts [OPTIONS] <URL> [KEY=VALUE ...]

Accesses a URL and automatically handles on-chain payments if it returns a 402 error.

Arguments:
  URL            The protected API endpoint URL.
  KEY=VALUE ...  Optional. Additional parameters to assemble as JSON body (for POST/PUT) or query string (for GET).

Options:
  -X, --method <METHOD>  HTTP method (GET, POST, etc.). Default: GET (or POST if parameters are provided).
  -d, --data <DATA>      Raw request body data.
  -H, --header <HEADER>  HTTP header in "Key: Value" format. Can be used multiple times.
  --network <NAME>       Optional. Network to use: mainnet or testnet/sepolia.
  --rpc <URL>            Optional. Custom RPC URL for the network.
  --json                 Output results (and error) in JSON format.
  --help                 Show this help message.

Environment:
  CLIENT_PRIVATE_KEY     Required. 64-character hex string starting with 0x.

Example:
  bun run scripts/request.ts "https://api.example.com/data" --json --network testnet
`.trim()
        );
        process.exit(args.params.length < 1 && !args.isHelp ? EXIT_CODES.INVALID_ARGS : EXIT_CODES.SUCCESS);
    }

    let url = args.params[0];
    const extraParams = args.params.slice(1);
    const pk = getPrivateKey(args.isJson);

    try {
        const { rpcUrls, networkName } = await resolveNetwork(args.rpcUrl, args.network);

        const kvParams: Record<string, string> = {};
        for (const p of extraParams) {
            const [k, ...v] = p.split('=');
            if (k && v.length > 0) {
                kvParams[k] = v.join('=');
            }
        }

        const method = args.method?.toUpperCase() || (args.data || Object.keys(kvParams).length > 0 ? 'POST' : 'GET');
        const options: RequestOptions = {
            method,
            headers: args.headers || {}
        };

        if (method === 'GET') {
            const urlObj = new URL(url);
            for (const [k, v] of Object.entries(kvParams)) {
                urlObj.searchParams.append(k, v);
            }
            url = urlObj.toString();
        } else {
            if (args.data) {
                options.body = args.data;
            } else if (Object.keys(kvParams).length > 0) {
                options.json = kvParams;
            }
        }

        if (!args.isJson) {
            console.error(`🌐 [${method}] Requesting ${url} on ${networkName}...`);
        }

        const client = new PayNodeAgentClient(pk, rpcUrls);
        const response = await client.requestGate(url, options);

        const contentType = response.headers.get('content-type') || '';
        let body: any;

        if (contentType.includes('application/json')) {
            body = await response.json();
        } else {
            body = await response.text();
        }

        if (args.isJson) {
            console.log(
                JSON.stringify(
                    {
                        status: 'success',
                        url,
                        method,
                        http_status: response.status,
                        content_type: contentType,
                        network: networkName,
                        data: body
                    },
                    null,
                    2
                )
            );
        } else {
            if (typeof body === 'object') {
                console.log(JSON.stringify(body, null, 2));
            } else {
                console.log(body);
            }
        }
    } catch (error: any) {
        reportError(`Request failed: ${error.message}`, args.isJson, EXIT_CODES.NETWORK_ERROR);
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
