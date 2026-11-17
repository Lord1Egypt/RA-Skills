export type Streams = { out: (s: string) => void; err: (s: string) => void };

export const processStreams: Streams = {
  out: (s) => { process.stdout.write(s); },
  err: (s) => { process.stderr.write(s); },
};
