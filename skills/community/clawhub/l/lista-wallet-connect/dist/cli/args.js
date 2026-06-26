import { parseArgs } from "util";
export function parseCliInput() {
    const { positionals, values } = parseArgs({
        allowPositionals: true,
        options: {
            chains: { type: "string" },
            topic: { type: "string" },
            address: { type: "string" },
            message: { type: "string" },
            chain: { type: "string" },
            to: { type: "string" },
            data: { type: "string" },
            value: { type: "string" },
            gas: { type: "string" },
            gasPrice: { type: "string" },
            all: { type: "boolean" },
            clean: { type: "boolean" },
            open: { type: "boolean" },
            "no-simulate": { type: "boolean" },
            "debug-log-file": { type: "string" },
            help: { type: "boolean", short: "h" },
        },
    });
    return {
        command: positionals[0],
        help: Boolean(values.help),
        debugLogFile: values["debug-log-file"],
        args: {
            ...values,
            noSimulate: values["no-simulate"],
        },
    };
}
