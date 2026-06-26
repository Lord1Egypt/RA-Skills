const HOST = 'https://moria.fun';

export interface Token {
    creator: string;
    mint: string;
    name: string;
    symbol: string;
    ipfs_url: string;
    create_timestamp: number;
    migration_quote_threshold: string;
    migration_threshold: string;
    status: number;
}

export async function getMyTokens(privy_device_id: string): Promise<Token[] | null> {
    const res = await fetch(`${HOST}/api/agent/my_tokens?privy_device_id=${encodeURIComponent(privy_device_id)}`, {
        headers: { 'accept': 'application/json' }
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to fetch shopper info: ${res.status} ${res.statusText} - ${errorText}`);
    }

    const data = await res.json();

    if (data.code != 200 || !data.tokens) {
        throw new Error(JSON.stringify(data.message));
    }

    return data.tokens as Token[];
}

export async function getMyMinttoTokens(privy_device_id: string): Promise<Token[] | null> {
    const res = await fetch(`${HOST}/api/agent/my_mintto_tokens?privy_device_id=${encodeURIComponent(privy_device_id)}`, {
        headers: { 'accept': 'application/json' }
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to fetch shopper info: ${res.status} ${res.statusText} - ${errorText}`);
    }

    const data = await res.json();

    if (data.code != 200 || !data.tokens) {
        throw new Error(JSON.stringify(data.message));
    }

    return data.tokens as Token[];
}

export async function getMintToTokens(privy_device_id: string): Promise<Token[] | null> {
    const res = await fetch(`${HOST}/api/agent/mintto_tokens?privy_device_id=${encodeURIComponent(privy_device_id)}`, {
        headers: { 'accept': 'application/json' }
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to fetch shopper info: ${res.status} ${res.statusText} - ${errorText}`);
    }

    const data = await res.json();

    if (data.code != 200) {
        throw new Error(JSON.stringify(data.message));
    }

    return data.tokens? data.tokens as Token[]: null;
}

export async function getDammV2Tokens(privy_device_id: string): Promise<Token[] | null> {
    const res = await fetch(`${HOST}/api/agent/dammv2_tokens?privy_device_id=${encodeURIComponent(privy_device_id)}`, {
        headers: { 'accept': 'application/json' }
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to fetch shopper info: ${res.status} ${res.statusText} - ${errorText}`);
    }

    const data = await res.json();

    if (data.code != 200 || !data.tokens) {
        throw new Error(JSON.stringify(data.message));
    }

    return data.tokens as Token[];
}