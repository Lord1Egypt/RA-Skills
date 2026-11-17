export const processStreams = {
    out: (s) => { process.stdout.write(s); },
    err: (s) => { process.stderr.write(s); },
};
