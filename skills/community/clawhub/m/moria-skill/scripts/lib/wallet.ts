const HOST = 'https://moria.fun';

export interface Wallet {
    privy_device_id: string;
    key: string;
    private_key: string;
}

export async function getWallet(code: string): Promise<Wallet | null> {

    const res = await fetch(`${HOST}/api/agent/wallet?code=${code}`, {
        headers: { 'accept': 'application/json' }
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to fetch shopper info: ${res.status} ${res.statusText} - ${errorText}`);
    }

    const data = await res.json();

    if (data.code != 200 || !data.wallet) {
        throw new Error(JSON.stringify(data.message));
    }

    return data.wallet as Wallet;
}
