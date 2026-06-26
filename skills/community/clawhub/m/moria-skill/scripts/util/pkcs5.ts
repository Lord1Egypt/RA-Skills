export class ErrPaddingSize extends Error {
    constructor() {
        super("padding size error");
    }
}

export class PKCS5 {
    static padding(src: Uint8Array, blockSize: number): Uint8Array {
        const padLen = blockSize - (src.length % blockSize);
        const out = new Uint8Array(src.length + padLen);
        out.set(src);
        out.fill(padLen, src.length);
        return out;
    }

    static unpadding(src: Uint8Array, blockSize: number): Uint8Array {
        const len = src.length;
        const padLen = src[len - 1];

        if (padLen > len || padLen > blockSize || padLen === 0) {
            throw new ErrPaddingSize();
        }

        for (let i = 0; i < padLen; i++) {
            if (src[len - 1 - i] !== padLen) {
                throw new ErrPaddingSize();
            }
        }
        
        return src.slice(0, len - padLen);
    }
}
