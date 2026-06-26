import { readFile, stat } from "fs/promises";
import { basename, extname } from "path";

const pinataJWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3MWFjOWM1OC1iYzYxLTQ5NjUtODRiNy0wNzg4ZmM4MTFhODciLCJlbWFpbCI6Im91ZmVpODJAMTYzLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiIxNzU1OGZhNTkyMmU2NjU0YWM3ZiIsInNjb3BlZEtleVNlY3JldCI6ImYzZGIwMGNkMDI5ZTg0YmI4MTc5MjYyMzQ5NTAzMjA4YzI4ZTEwNzNjMTBkYjI3YmQ0Y2ZjZGY0M2I2NjcxZDUiLCJleHAiOjE4MDE5MDUyNTB9.BDOWgd6m6cp4msDcZd3JP15KC1SVRlnEQLff9OH7qRM";
const pinataGatewayURL = 'https://gateway.pinata.cloud/ipfs/';

const PINATA_PIN_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS";

const MAX_IMAGE_BYTES = 3 * 1024 * 1024; // 3 MB

const MIME_BY_EXT: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".json": "application/json",
};

function guessMime(filePath: string): string {
    const ext = extname(filePath).toLowerCase();
    return MIME_BY_EXT[ext] ?? "application/octet-stream";
}

function genURL(ipfsHash: string): string {
    const hash = String(ipfsHash || "").replace(/^ipfs:\/\//, "").trim();
    if (!hash) return "";
    return `${pinataGatewayURL}${hash}`;
}

type PinataPinFileResponse = {
    IpfsHash: string;
    PinSize?: number;
    Timestamp?: string;
};

type PinataErrorBody = {
    error?: { details?: string; reason?: string };
    message?: string;
};

type PinFileMeta = { name?: string };

async function pinFileToPinata(
    fileBlob: Blob,
    filename: string,
    meta: PinFileMeta = {}
): Promise<PinataPinFileResponse> {
    const form = new FormData();
    form.append("file", fileBlob, filename);
    form.append(
        "pinataMetadata",
        JSON.stringify({ name: meta.name ?? filename })
    );
    form.append("pinataOptions", JSON.stringify({ cidVersion: 0 }));

    const res = await fetch(PINATA_PIN_URL, {
        method: "POST",
        headers: { Authorization: `Bearer ${pinataJWT}` },
        body: form,
    });

    const text = await res.text();
    if (!res.ok) {
        let detail = text;
        try {
            const j = JSON.parse(text) as PinataErrorBody;
            detail =
                j.error?.details || j.error?.reason || j.message || text;
        } catch {
            /* keep text */
        }
        throw new Error(`Pinata upload failed (${res.status}): ${detail}`);
    }
    const data = JSON.parse(text) as PinataPinFileResponse;
    if (!data.IpfsHash) {
        throw new Error("Pinata response missing IpfsHash");
    }
    return data;
}

export type UploadIpfsResult = {
    ipfsHash: string;
    gatewayUrl: string;
    pinata: PinataPinFileResponse;
};

/**
 * Upload a local image file to IPFS via Pinata.
 */
export async function uploadImage(filePath: string): Promise<UploadIpfsResult> {
    const st = await stat(filePath);
    if (!st.isFile()) {
        throw new Error(`Not a file: ${filePath}`);
    }

    if (st.size > MAX_IMAGE_BYTES) {
        throw new Error(`Image exceeds ${MAX_IMAGE_BYTES} bytes (3 MB). Use a smaller file.`);
    }
    const buf = await readFile(filePath);
    const name = basename(filePath);
    const mime = guessMime(filePath);
    const blob = new Blob([buf], { type: mime });
    const pinata = await pinFileToPinata(blob, name, { name: "Image file" });
    const ipfsHash = pinata.IpfsHash;
    return {
        ipfsHash,
        gatewayUrl: genURL(ipfsHash),
        pinata,
    };
}

/**
 * Upload a local JSON file to IPFS via Pinata (file bytes unchanged).
 */
export async function uploadJson(
    filename: string,
    context: string
): Promise<UploadIpfsResult> {
    try {
        JSON.parse(context.trim());
    } catch {
        throw new Error(`Invalid JSON`);
    }
    const name = filename.toLowerCase().endsWith(".json") ? filename : `${filename}.json`;
    const blob = new Blob([context], { type: "application/json" });
    const pinata = await pinFileToPinata(blob, name, { name: "JSON metadata" });
    const ipfsHash = pinata.IpfsHash;
    return {
        ipfsHash,
        gatewayUrl: genURL(ipfsHash),
        pinata,
    };
}

export async function uploadJsonFile(
    filePath: string
): Promise<UploadIpfsResult> {
    const st = await stat(filePath);
    if (!st.isFile()) {
        throw new Error(`Not a file: ${filePath}`);
    }
    const buf = await readFile(filePath);
    const raw = buf.toString("utf8").replace(/^\uFEFF/, "");
    try {
        JSON.parse(raw.trim());
    } catch {
        throw new Error(`Invalid JSON in file: ${filePath}`);
    }
    const base = basename(filePath);
    const name = base.toLowerCase().endsWith(".json") ? base : `${base}.json`;
    const blob = new Blob([buf], { type: "application/json" });
    const pinata = await pinFileToPinata(blob, name, { name: "JSON metadata" });
    const ipfsHash = pinata.IpfsHash;
    console.log("ipfsHash", ipfsHash);
    console.log("gatewayUrl", genURL(ipfsHash));
    console.log("pinata", pinata);
    return {
        ipfsHash,
        gatewayUrl: genURL(ipfsHash),
        pinata,
    };
}