export class ErrBlockSize extends Error {
    constructor() {
        super("plaintext is not a multiple of the block size");
    }
}

const delta = 0x9e3779b9 >>> 0;
const blockSize = 8;
const byteSize = 4;
const byte2Size = 8;

// wheel 常量
export const Wheel2Chunk = 1;
export const Wheel4Chunk = 2;
export const Wheel8Chunk = 3;
export const Wheel16Chunk = 4;
export const Wheel32Chunk = 5;
export const Wheel64Chunk = 6;

const wheelChunk: Record<number, number> = {
    [Wheel2Chunk]: 2,
    [Wheel4Chunk]: 4,
    [Wheel8Chunk]: 8,
    [Wheel16Chunk]: 16,
    [Wheel32Chunk]: 32,
    [Wheel64Chunk]: 64,
};

// ====== LittleEndian 工具 ======
function readUint32LE(buf: Uint8Array, offset: number): number {
    return (
        buf[offset] |
        (buf[offset + 1] << 8) |
        (buf[offset + 2] << 16) |
        (buf[offset + 3] << 24)
    ) >>> 0;
}

function writeUint32LE(buf: Uint8Array, offset: number, value: number) {
    buf[offset] = value & 0xff;
    buf[offset + 1] = (value >>> 8) & 0xff;
    buf[offset + 2] = (value >>> 16) & 0xff;
    buf[offset + 3] = (value >>> 24) & 0xff;
}

// ====== TEA 核心 ======
function encryptTEA(
    y: number,
    z: number,
    key: number[],
    wheel: number
): [number, number] {
    let sum = 0 >>> 0;
    const rounds = wheelChunk[wheel];

    for (let i = 0; i < rounds; i++) {
        sum = (sum + delta) >>> 0;

        y =
            (y +
                (((z << 4) + key[0]) ^
                    (z + sum) ^
                    ((z >>> 5) + key[1]))) >>>
            0;

        z =
            (z +
                (((y << 4) + key[2]) ^
                    (y + sum) ^
                    ((y >>> 5) + key[3]))) >>>
            0;
    }

    return [y, z];
}

function decryptTEA(
    y: number,
    z: number,
    key: number[],
    wheel: number
): [number, number] {
    let sum = (delta << wheel) >>> 0;
    const rounds = wheelChunk[wheel];

    for (let i = 0; i < rounds; i++) {
        z =
            (z -
                (((y << 4) + key[2]) ^
                    (y + sum) ^
                    ((y >>> 5) + key[3]))) >>>
            0;

        y =
            (y -
                (((z << 4) + key[0]) ^
                    (z + sum) ^
                    ((z >>> 5) + key[1]))) >>>
            0;

        sum = (sum - delta) >>> 0;
    }

    return [y, z];
}

// ====== TEA 类 ======
export class TEA {
    private keyArr: number[];
    private wheel: number;
    private padding: any;

    constructor(key: Uint8Array, wheel: number, padding: any) {
        const tmpKey = new Uint8Array(16);
        tmpKey.set(key.slice(0, 16));

        this.keyArr = [
            readUint32LE(tmpKey, 0),
            readUint32LE(tmpKey, 4),
            readUint32LE(tmpKey, 8),
            readUint32LE(tmpKey, 12),
        ];

        this.wheel = wheel;
        this.padding = padding;
    }

    encrypt(src: Uint8Array): Uint8Array {
        let data = this.padding.padding(src, blockSize);

        for (let i = 0; i < data.length; i += 8) {
            let y = readUint32LE(data, i);
            let z = readUint32LE(data, i + 4);

            [y, z] = encryptTEA(y, z, this.keyArr, this.wheel);

            writeUint32LE(data, i, y);
            writeUint32LE(data, i + 4, z);
        }

        return data;
    }

    decrypt(src: Uint8Array): Uint8Array {
        if (src.length < blockSize || src.length % blockSize !== 0) {
            throw new ErrBlockSize();
        }

        const data = new Uint8Array(src);

        for (let i = 0; i < data.length; i += 8) {
            let y = readUint32LE(data, i);
            let z = readUint32LE(data, i + 4);

            [y, z] = decryptTEA(y, z, this.keyArr, this.wheel);

            writeUint32LE(data, i, y);
            writeUint32LE(data, i + 4, z);
        }

        return this.padding.unpadding(data, blockSize);
    }
}
