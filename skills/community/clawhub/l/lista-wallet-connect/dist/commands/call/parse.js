import { parseUnits } from "viem";
function parseValue(value) {
    if (!value || value === "0")
        return undefined;
    if (value.startsWith("0x"))
        return value;
    if (value.includes(".")) {
        const wei = parseUnits(value, 18);
        return "0x" + wei.toString(16);
    }
    return "0x" + BigInt(value).toString(16);
}
function parseGas(value) {
    if (!value)
        return undefined;
    if (value.startsWith("0x"))
        return value;
    return "0x" + BigInt(value).toString(16);
}
export function buildCallTransaction(from, to, args) {
    const tx = {
        from,
        to,
    };
    if (args.data) {
        tx.data = args.data.startsWith("0x") ? args.data : "0x" + args.data;
    }
    const value = parseValue(args.value);
    if (value)
        tx.value = value;
    const gas = parseGas(args.gas);
    if (gas)
        tx.gas = gas;
    const gasPrice = parseGas(args.gasPrice);
    if (gasPrice)
        tx.gasPrice = gasPrice;
    return tx;
}
