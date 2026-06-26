import * as fs from 'fs';
import * as path from 'path';
import base64 from 'base64-js';

export interface VaultData {
    secretKey: string; // Base64 encoded
    did: string;
}

export function saveKey(agentDir: string, secretKey: Uint8Array, did: string) {
    const vaultPath = path.join(agentDir, 'vault.json');
    const data: VaultData = {
        secretKey: base64.fromByteArray(secretKey),
        did: did
    };
    fs.writeFileSync(vaultPath, JSON.stringify(data, null, 2));
    // Simulate setting permissions: chmod 600
    fs.chmodSync(vaultPath, 0o600);
}

export function loadKey(agentDir: string): { secretKey: Uint8Array, did: string } {
    const vaultPath = path.join(agentDir, 'vault.json');
    if (!fs.existsSync(vaultPath)) throw new Error(`No vault found for ${agentDir}`);
    const data: VaultData = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'));
    return {
        secretKey: base64.toByteArray(data.secretKey),
        did: data.did
    };
}
