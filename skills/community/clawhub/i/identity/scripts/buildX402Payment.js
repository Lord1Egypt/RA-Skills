const fs = require("fs");
const os = require("os");
const path = require("path");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const {
  hashstr,
  outputSuccess,
  outputError,
  outputInputRequired,
  getUserWallet,
  createAuthRequestMessage,
  getRequiredDidEntry,
} = require("./shared/utils");
const { getInitializedRuntime } = require("./shared/bootstrap");
const { x402Client } = require("@x402/core/client");
const { ExactEvmScheme } = require("@x402/evm/exact/client");
const {
  createHumanProofExtension,
  MissingAttestationsError,
  checkAttestation,
  isMaxUseExceededError,
} = require("@billionsnetwork/x402-human-proof-client");
const { toClientEvmSigner } = require("@x402/evm");
const {
  schemaId,
  transactionSender,
  requiredAttestationsMessage,
} = require("./shared/constants");
const { createPOUScope, createAuthScope } = require("./shared/scopes");
const { signChallenge } = require("./signChallenge");
const { v4: uuidv4 } = require("uuid");

function getPaymentHash(payment) {
  return hashstr(JSON.stringify(payment));
}

function getPaymentRequiredHash(paymentRequired) {
  return hashstr(JSON.stringify(paymentRequired));
}

function parsePaymentRequiredHeader(headerValue) {
  const trimmed = headerValue.trim();
  return trimmed.startsWith("{")
    ? JSON.parse(trimmed)
    : JSON.parse(atob(trimmed));
}

async function fetchPaymentRequired(url) {
  let response;
  try {
    response = await fetch(url);
  } catch (e) {
    outputError(`Failed to reach resource: ${e.message || e}`, true);
    return;
  }
  if (response.status !== 402) {
    outputError(`Expected 402 from ${url}, got ${response.status}`, true);
    return;
  }
  const headerValue = response.headers.get("payment-required");
  if (!headerValue) {
    outputError(
      "Resource returned 402 but no PAYMENT-REQUIRED header",
      true,
    );
    return;
  }
  try {
    return parsePaymentRequiredHeader(headerValue);
  } catch (e) {
    outputError(
      `PAYMENT-REQUIRED header is not valid JSON or Base64 JSON: ${e.message || e}`,
      true,
    );
  }
}

function persistPaymentRequired(paymentRequired) {
  const hash = getPaymentRequiredHash(paymentRequired);
  const filePath = path.join(os.tmpdir(), `${hash}.json`);
  const tempPath = `${filePath}.tmp`;
  fs.writeFileSync(tempPath, JSON.stringify(paymentRequired, null, 2), "utf-8");
  fs.renameSync(tempPath, filePath);
  return { hash, filePath };
}

function loadPaymentRequiredFile(filePath) {
  let raw;
  try {
    raw = fs.readFileSync(filePath, "utf-8");
  } catch (e) {
    outputError(
      `Failed to read --paymentRequiredFilePath ${filePath}: ${e.message || e}`,
      true,
    );
    return;
  }
  try {
    return JSON.parse(raw);
  } catch (e) {
    outputError(
      `--paymentRequiredFilePath ${filePath} is not valid JSON: ${e.message || e}`,
      true,
    );
  }
}

function getRequiredAttestations(payment) {
  return (payment.extra && payment.extra.requiredAttestations) || [];
}

async function getMissingAttestations(did, payment) {
  const requiredAttestations = getRequiredAttestations(payment);
  const results = await Promise.all(
    requiredAttestations.map(async (id) => ({
      id,
      exists: await checkAttestation(did, id),
    })),
  );
  return results.filter((r) => !r.exists).map((r) => r.id);
}

async function createAttestationLinks(
  attestationSchemaIds,
  transactionSenderAddr,
  did,
  entry,
  kms,
) {
  return await Promise.all(
    attestationSchemaIds.map(async (attestationSchemaId) => {
      if (attestationSchemaId !== schemaId) {
        throw new Error(
          `Unknown attestation requirement with schema ${attestationSchemaId}`,
        );
      }
      const scope = [
        createPOUScope(transactionSenderAddr),
        createAuthScope(did),
      ];
      const signedChallenge = await signChallenge(
        { name: uuidv4(), description: uuidv4() },
        entry,
        kms,
      );
      return await createAuthRequestMessage(signedChallenge, scope);
    }),
  );
}

async function handleMissingAttestations(error, entry, kms) {
  const attestationLinks = await createAttestationLinks(
    error.attestationRequirements,
    transactionSender,
    entry.did,
    entry,
    kms,
  );
  outputInputRequired(
    {
      attestationsRequired: true,
      message: requiredAttestationsMessage,
      attestationLinks,
    },
    true,
  );
}

async function buildPaymentInfo(payment, entry, kms) {
  const requiredAttestations = getRequiredAttestations(payment);
  const missingAttestations = await getMissingAttestations(entry.did, payment);

  let attestationLinks = [];
  if (missingAttestations.length > 0) {
    attestationLinks = await createAttestationLinks(
      missingAttestations,
      transactionSender,
      entry.did,
      entry,
      kms,
    );
  }

  return {
    hash: getPaymentHash(payment),
    amount: payment.amount,
    asset: (payment.extra && payment.extra.name) || payment.asset,
    network: payment.network,
    requiredAttestations,
    hasAllAttestations: missingAttestations.length === 0,
    attestationLinks,
  };
}

function parseCliArgs() {
  return yargs(hideBin(process.argv))
    .scriptName("buildX402Payment")
    .usage(
      "$0 [options]\n\n" +
        "Execute the x402 payment flow in two phases.\n\n" +
        "Phase 1 — Discover (--resource only):\n" +
        "  Fetches the 402 challenge from the resource, caches the\n" +
        "  PAYMENT-REQUIRED payload to a temp file named by its hash, and\n" +
        "  returns { paymentRequiredFilePath, paymentOptions }. Never signs a\n" +
        "  payment. Pass --paymentHash here is an error.\n\n" +
        "Phase 2 — Execute (--paymentRequiredFilePath + --paymentHash):\n" +
        "  Reads the cached payment-required file, looks up the chosen option\n" +
        "  by --paymentHash, and signs/sends the payment. Cannot be combined\n" +
        "  with --resource.",
    )
    .option("resource", {
      type: "string",
      describe:
        "Phase 1 only. URL of the resource that returns 402 with a " +
        "PAYMENT-REQUIRED header. Mutually exclusive with " +
        "--paymentRequiredFilePath and --paymentHash.",
    })
    .option("paymentRequiredFilePath", {
      type: "string",
      describe:
        "Phase 2 only. Path to the cached payment-required JSON file " +
        "returned by phase 1. Must be combined with --paymentHash. " +
        "Mutually exclusive with --resource.",
    })
    .option("paymentHash", {
      type: "string",
      describe:
        "Phase 2 only. Hash of the payment option to execute (from phase 1's " +
        "paymentOptions[].hash). Must be combined with --paymentRequiredFilePath.",
    })
    .option("did", {
      type: "string",
      describe:
        "Optional. DID to use for signing. Defaults to the default DID in local storage.",
    })
    .example(
      "$0 --resource https://api.example.com/paid",
      "Phase 1: discover payment options and cache the challenge",
    )
    .example(
      "$0 --paymentRequiredFilePath /tmp/<hash>.json --paymentHash <hash>",
      "Phase 2: execute the selected payment from the cached challenge",
    )
    .example(
      "$0 --resource https://api.example.com/paid --did did:iden3:...",
      "Phase 1 with an explicit DID instead of the default",
    )
    .check((argv) => {
      const hasResource = Boolean(argv.resource);
      const hasFilePath = Boolean(argv.paymentRequiredFilePath);
      const hasHash = Boolean(argv.paymentHash);

      if (!hasResource && !hasFilePath) {
        throw new Error(
          "Provide --resource (phase 1) or --paymentRequiredFilePath + --paymentHash (phase 2).",
        );
      }
      if (hasResource && hasFilePath) {
        throw new Error(
          "--resource and --paymentRequiredFilePath are mutually exclusive. " +
            "Use --resource alone for phase 1, or " +
            "--paymentRequiredFilePath + --paymentHash for phase 2.",
        );
      }
      if (hasResource && hasHash) {
        throw new Error(
          "--paymentHash is not allowed with --resource. Run phase 1 with " +
            "--resource alone, then pass the returned paymentRequiredFilePath " +
            "together with --paymentHash in phase 2.",
        );
      }
      if (hasFilePath && !hasHash) {
        throw new Error(
          "--paymentHash is required with --paymentRequiredFilePath (phase 2).",
        );
      }
      return true;
    })
    .strict()
    .help("help")
    .alias("help", "h")
    .wrap(Math.min(120, yargs().terminalWidth()))
    .fail((msg, err, y) => {
      console.error(y.help());
      console.error(`\nError: ${msg || (err && err.message) || "invalid arguments"}`);
      process.exit(1);
    })
    .parse();
}

function requirePaymentResourceUrl(paymentRequired) {
  const paymentResource = paymentRequired.resource;
  if (!paymentResource || !paymentResource.url) {
    outputError("paymentRequired.resource.url is required", true);
    return null;
  }
  return paymentResource;
}

async function runDiscovery(args, entry, kms) {
  const paymentRequired = await fetchPaymentRequired(args.resource);
  const paymentResource = requirePaymentResourceUrl(paymentRequired);
  if (!paymentResource) return;

  const { filePath } = persistPaymentRequired(paymentRequired);
  const paymentOptions = await Promise.all(
    paymentRequired.accepts.map((p) => buildPaymentInfo(p, entry, kms)),
  );

  outputInputRequired(
    {
      resource: {
        url: paymentResource.url,
        description: paymentResource.description,
      },
      paymentOptions,
      paymentRequiredFilePath: filePath,
    },
    true,
  );
}

async function main() {
  try {
    const args = parseCliArgs();

    const { kms, memoryKeyStore, didsStorage } = await getInitializedRuntime();
    const entry = await getRequiredDidEntry(didsStorage, args.did);

    // Phase 1: --resource only. Fetch, cache, return options.
    if (args.resource) {
      await runDiscovery(args, entry, kms);
      return;
    }

    // Phase 2: --paymentRequiredFilePath + --paymentHash. Load file, find hash, execute.
    const paymentRequired = loadPaymentRequiredFile(args.paymentRequiredFilePath);
    const paymentResource = requirePaymentResourceUrl(paymentRequired);
    if (!paymentResource) return;

    const matched = paymentRequired.accepts.find(
      (p) => getPaymentHash(p) === args.paymentHash,
    );
    if (!matched) {
      outputError("No payment matching the provided --paymentHash", true);
      return;
    }
    paymentRequired.accepts = [matched];

    // Phase 2: Single payment - check attestations before proceeding
    const selectedPayment = paymentRequired.accepts[0];
    const missingAttestations = await getMissingAttestations(
      entry.did,
      selectedPayment,
    );

    if (missingAttestations.length > 0) {
      const attestationLinks = await createAttestationLinks(
        missingAttestations,
        transactionSender,
        entry.did,
        entry,
        kms,
      );
      outputInputRequired(
        {
          attestationsRequired: true,
          message: requiredAttestationsMessage,
          attestationLinks,
        },
        true,
      );
      return;
    }

    // Phase 4: Execute payment and fetch the resource
    const { wallet } = await getUserWallet(entry, memoryKeyStore);
    const signer = toClientEvmSigner(wallet);

    const x402 = new x402Client();
    x402.register("eip155:*", new ExactEvmScheme(signer));
    x402.registerExtension(
      createHumanProofExtension({
        address: wallet.address,
        pubKey: wallet.publicKey,
        signMessage: (msg) => wallet.signMessage({ message: msg }),
      }),
    );
    x402.onPaymentCreationFailure(async ({ error }) => {
      if (error instanceof MissingAttestationsError) {
        await handleMissingAttestations(error, entry, kms);
      }
    });

    let paymentPayload;
    try {
      paymentPayload = await x402.createPaymentPayload(paymentRequired);
    } catch (error) {
      if (error instanceof MissingAttestationsError) {
        return;
      } else {
        throw error;
      }
    }

    // Phase 5: Fetch the resource with the payment signature
    const paymentSignature = btoa(JSON.stringify(paymentPayload));
    const url = paymentResource.url;
    let response;
    response = await fetch(url, {
      headers: { "PAYMENT-SIGNATURE": paymentSignature },
    });

    if (response.status === 402) {
      console.log(response);
      if (isMaxUseExceededError({ response })) {
        outputInputRequired(
          {
            maxUseExceeded: true,
            message:
              "Payment has exceeded its maximum allowed uses. Choose a different payment or contact the resource provider.",
          },
          true,
        );
      }
      // if not max use exceeded, check for new payment required
      const newPaymentRequired = response.headers.get("payment-required");
      if (newPaymentRequired) {
        outputInputRequired({ newPaymentRequired: newPaymentRequired }, true);
        return;
      }
      outputError("Received 402 but no PAYMENT-REQUIRED header found", true);
      return;
    }

    const responseText = await response.text();
    let responseBody;
    try {
      responseBody = JSON.parse(responseText);
    } catch {
      responseBody = responseText;
    }

    if (response.ok) {
      outputSuccess(responseBody, true);
    } else {
      outputError(
        `HTTP ${response.status}: ${typeof responseBody === "string" ? responseBody : JSON.stringify(responseBody)}`,
        true,
      );
    }
  } catch (error) {
    outputError(error, true);
  }
}

main();
