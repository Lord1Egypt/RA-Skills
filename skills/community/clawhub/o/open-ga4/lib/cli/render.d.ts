export type Streams = {
    out: (s: string) => void;
    err: (s: string) => void;
};
export declare const processStreams: Streams;
