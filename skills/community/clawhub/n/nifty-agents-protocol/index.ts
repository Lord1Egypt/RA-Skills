import nacl from 'tweetnacl';
import naclUtil from 'tweetnacl-util';
const { decodeUTF8, encodeUTF8 } = naclUtil;
import { optimize } from 'svgo';
import * as crypto from 'crypto';
import base64 from 'base64-js';

// --- Types ---

export interface AgentIdentity {
    did: string;
    publicKey: Uint8Array;
    secretKey: Uint8Array;
}

export interface PrivateClaim {
    recipientDID: string;
    encryptedData: string; // Base64
}

export interface VerificationResult {
    isValid: boolean;
    creator: string;
    currentOwner: string;
    chain: string[];
    metadata: any;
}

// --- Constants & Helpers ---

const DID_PREFIX = 'did:key:z6Mk';

// SVGO config for canonicalization - deterministic output
const SVGO_CONFIG = {
    plugins: [
        'preset-default',
        {
            name: 'convertPathData',
            params: {
                noSpaceAfterFlags: true,
                floatPrecision: 2
            }
        },
        'sortAttrs'
    ]
};

function safeJsonParse(str: string): any {
    return JSON.parse(str, (key, value) => {
        if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
            return undefined; // Strip dangerous keys
        }
        return value;
    });
}

function toBase64(arr: Uint8Array): string {
    return base64.fromByteArray(arr);
}

function fromBase64(str: string): Uint8Array {
    const padded = str + '='.repeat((4 - (str.length % 4)) % 4);
    return base64.toByteArray(padded);
}

// --- Core Logic ---

/**
 * Generates a portable Ed25519 identity following the did:key:z6Mk standard.
 */
export function generateIdentity(): AgentIdentity {
    const keyPair = nacl.sign.keyPair();
    const did = DID_PREFIX + toBase64(keyPair.publicKey).replace(/=/g, '');
    return {
        did,
        publicKey: keyPair.publicKey,
        secretKey: keyPair.secretKey
    };
}

export async function canonicalizeSVG(svg: string): Promise<string> {
    const result = optimize(svg, SVGO_CONFIG as any);
    return result.data;
}

export function computeHash(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * Signs an SVG and embeds the Genesis Manifest.
 */
export async function signSVG(svg: string, identity: AgentIdentity, extraMetadata: any = {}): Promise<string> {
    // Remove existing metadata for hashing
    const cleanSVG = svg.replace(/\s*<metadata>[\s\S]*?<\/metadata>\s*/g, '');
    const canonical = await canonicalizeSVG(cleanSVG);
    const hash = computeHash(canonical);
    const signature = nacl.sign.detached(decodeUTF8(hash), identity.secretKey);
    
    const manifest = {
        version: "1.0",
        creator: identity.did,
        hash: hash,
        signature: toBase64(signature),
        transfers: [],
        ...extraMetadata
    };

    const manifestBase64 = base64.fromByteArray(decodeUTF8(JSON.stringify(manifest)));

    // Embed in <metadata>
    if (svg.includes('<metadata>')) {
        return svg.replace(/<metadata>[\s\S]*?<\/metadata>/, `<metadata>nasp:${manifestBase64}</metadata>`);
    } else {
        return svg.replace(/<svg(.*?)>/, `<svg$1>\n<metadata>nasp:${manifestBase64}</metadata>`);
    }
}

/**
 * Verifies the integrity and full provenance chain of a Nifty SVG.
 */
export async function verifySVG(svg: string): Promise<VerificationResult> {
    const metadataMatch = svg.match(/<metadata>nasp:(.*?)<\/metadata>/);
    if (!metadataMatch) throw new Error('No NASP metadata found');

    const manifest = safeJsonParse(encodeUTF8(fromBase64(metadataMatch[1])));
    
    // Hash the visual content (excluding metadata)
    const cleanSVG = svg.replace(/\s*<metadata>[\s\S]*?<\/metadata>\s*/g, '');
    const canonical = await canonicalizeSVG(cleanSVG);
    const hash = computeHash(canonical);

    if (hash !== manifest.hash) {
        return { isValid: false, creator: manifest.creator, currentOwner: '', chain: [], metadata: manifest };
    }

    // Verify Creator Signature
    const creatorPubKey = fromBase64(manifest.creator.replace(DID_PREFIX, ''));
    const isValidCreator = nacl.sign.detached.verify(
        decodeUTF8(hash),
        fromBase64(manifest.signature),
        creatorPubKey
    );

    if (!isValidCreator) {
        return { isValid: false, creator: manifest.creator, currentOwner: '', chain: [], metadata: manifest };
    }

    // Verify Transfer Chain
    let currentOwner = manifest.creator;
    const chain = [manifest.creator];

    for (const transfer of manifest.transfers) {
        const ownerPubKey = fromBase64(currentOwner.replace(DID_PREFIX, ''));
        const transferPayload = `${hash}:${transfer.to}:${transfer.timestamp}`;
        
        const isValidTransfer = nacl.sign.detached.verify(
            decodeUTF8(transferPayload),
            fromBase64(transfer.signature),
            ownerPubKey
        );

        if (!isValidTransfer) {
            return { isValid: false, creator: manifest.creator, currentOwner, chain, metadata: manifest };
        }
        currentOwner = transfer.to;
        chain.push(currentOwner);
    }

    return {
        isValid: true,
        creator: manifest.creator,
        currentOwner,
        chain,
        metadata: manifest
    };
}

/**
 * Transfers ownership by appending a new signed grant to the metadata.
 */
export async function transferSVG(svg: string, fromIdentity: AgentIdentity, toDID: string): Promise<string> {
    const audit = await verifySVG(svg);
    if (!audit.isValid) throw new Error('Cannot transfer invalid SVG');
    if (audit.currentOwner !== fromIdentity.did) {
        throw new Error(`Signer ${fromIdentity.did} is not the current owner (${audit.currentOwner})`);
    }

    const manifest = audit.metadata;
    const timestamp = new Date().toISOString();
    const transferPayload = `${manifest.hash}:${toDID}:${timestamp}`;
    const signature = nacl.sign.detached(decodeUTF8(transferPayload), fromIdentity.secretKey);

    manifest.transfers.push({
        to: toDID,
        timestamp,
        signature: toBase64(signature)
    });

    const newManifestBase64 = base64.fromByteArray(decodeUTF8(JSON.stringify(manifest)));
    return svg.replace(/<metadata>nasp:(.*?)<\/metadata>/, `<metadata>nasp:${newManifestBase64}</metadata>`);
}
