/**
 * HyperNatt BTC signal skill — x402 REST client (Node, axios only).
 *
 * Usage:
 *   node handler.js
 *   X402_PAYMENT_B64=... node handler.js
 */
import axios from "axios";

const SIGNAL_URL =
    process.env.HYPERNATT_SIGNAL_URL ||
    "https://hypernatt.com/api/m2m/signal";

function summarize(payload) {
    const cycle = payload?.cycle || {};
    const proof = payload?.proof || {};
    const track = proof.track_record || {};
    return {
        product: payload?.product,
        has_active: payload?.has_active,
        issued_at: payload?.issued_at,
        direction: cycle.direction ?? null,
        cycle_id: cycle.cycle_id ?? null,
        total_legs: cycle.total_legs ?? null,
        idle: payload?.idle ?? null,
        track_record: {
            url: track.url || "https://hypernatt.com/stats",
            win_rate: track.win_rate,
            total_trades: track.total_trades,
        },
        proof_snapshot_hash: proof.snapshot_hash,
        disclaimer:
            payload?.disclaimer ||
            "Live verifiable Mimo cycle state only. Not a trade recommendation.",
    };
}

async function main() {
    const payment = process.env.X402_PAYMENT_B64 || "";
    const headers = { Accept: "application/json" };
    if (payment) {
        headers["X-Payment"] = payment;
        headers["Payment-Signature"] = payment;
    }

    const response = await axios.get(SIGNAL_URL, {
        headers,
        validateStatus: () => true,
        timeout: 20000,
    });

    const out = {
        status: response.status,
        data:
            response.status === 200
                ? summarize(response.data)
                : response.data,
    };
    console.log(JSON.stringify(out, null, 2));

    if (response.status === 402) {
        console.error(
            "Hint: sign x402 payment ($0.01 USDC Base) and set X402_PAYMENT_B64",
        );
        process.exit(2);
    }
    process.exit(response.status === 200 ? 0 : 1);
}

main().catch((err) => {
    console.error(err.message || err);
    process.exit(1);
});
