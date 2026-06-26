/**
 * Pair command -- create a new WalletConnect pairing session (EVM only).
 */

import QRCode from "qrcode";
import { mkdirSync } from "fs";
import { join } from "path";
import { execSync } from "child_process";
import { parseAccountId, parseChainId } from "@walletconnect/utils";
import { getClient } from "../client.js";
import { saveSession, SESSIONS_DIR } from "../storage.js";
import { printErrorJson, printJson } from "../output.js";
import type { ParsedArgs } from "../types.js";

/**
 * Detect if running in a terminal environment where we should auto-open QR.
 * Returns true for: direct terminal, SSH, VSCode integrated terminal
 * Returns false for: piped output, Claude Code extension, programmatic usage
 *
 * @param forceOpen - If true (--open flag), always open regardless of environment
 */
function shouldAutoOpenQR(forceOpen?: boolean): boolean {
  // --open flag forces opening in agent environments (Claude, Codex, Cursor)
  if (forceOpen) return true;

  // If stdout is not a TTY, we're being piped/captured - output image data instead
  if (!process.stdout.isTTY) return false;

  // Check for Claude Code / agent environment
  if (process.env.CLAUDE_CODE || process.env.AGENT_MODE) return false;

  // Default: auto-open in terminal
  return true;
}

/**
 * Open file with system default application (cross-platform)
 */
function openFile(filePath: string): boolean {
  const platform = process.platform;
  try {
    if (platform === "darwin") {
      execSync(`open "${filePath}"`);
    } else if (platform === "win32") {
      execSync(`start "" "${filePath}"`);
    } else {
      execSync(`xdg-open "${filePath}"`);
    }
    return true;
  } catch {
    return false;
  }
}

function buildQrOpenCommands(qrPath: string): { macos: string; linux: string; windows: string } {
  return {
    macos: `open "${qrPath}"`,
    linux: `xdg-open "${qrPath}"`,
    windows: `start "" "${qrPath}"`,
  };
}

const NAMESPACE_CONFIG: Record<string, { methods: string[]; events: string[] }> = {
  eip155: {
    methods: ["personal_sign", "eth_sendTransaction", "eth_signTypedData_v4"],
    events: ["chainChanged", "accountsChanged"],
  },
};

function shortAddress(address: string): string {
  if (!address || address.length < 10) return address;
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

function buildPairSummary(accounts: string[]): {
  chains: string[];
  addresses: string[];
  primaryAccount?: { chain: string; address: string; display: string };
} {
  const parsed = accounts
    .map((account) => {
      try {
        const info = parseAccountId(account);
        return {
          chain: `${info.namespace}:${info.reference}`,
          address: info.address,
        };
      } catch {
        return null;
      }
    })
    .filter((item): item is { chain: string; address: string } => item !== null);

  const chains = Array.from(new Set(parsed.map((item) => item.chain)));
  const addresses = Array.from(new Set(parsed.map((item) => item.address)));
  const primary = parsed[0];

  return {
    chains,
    addresses,
    primaryAccount: primary
      ? {
          chain: primary.chain,
          address: primary.address,
          display: shortAddress(primary.address),
        }
      : undefined,
  };
}

export async function cmdPair(args: ParsedArgs): Promise<void> {
  const chains = args.chains ? args.chains.split(",") : ["eip155:56", "eip155:1"];

  const byNamespace: Record<string, string[]> = {};
  for (const chain of chains) {
    const { namespace } = parseChainId(chain);
    if (!NAMESPACE_CONFIG[namespace]) {
      printErrorJson({
        error: `Unsupported namespace: ${namespace}. Only EVM (eip155) is supported.`,
      });
      process.exit(1);
    }
    if (!byNamespace[namespace]) byNamespace[namespace] = [];
    byNamespace[namespace].push(chain);
  }

  const requiredNamespaces: Record<string, { chains: string[]; methods: string[]; events: string[] }> = {};
  for (const [ns, nsChains] of Object.entries(byNamespace)) {
    requiredNamespaces[ns] = {
      chains: nsChains,
      ...NAMESPACE_CONFIG[ns],
    };
  }

  const debug = process.env.WC_DEBUG === "1";
  const t0 = Date.now();

  const client = await getClient();
  if (debug) console.error(`[WC] getClient() done in ${Date.now() - t0}ms`);

  const t1 = Date.now();
  const { uri, approval } = await client.connect({ requiredNamespaces });
  if (debug) console.error(`[WC] client.connect() done in ${Date.now() - t1}ms`);

  const qrPath = join(SESSIONS_DIR, `qr-${Date.now()}.png`);
  mkdirSync(SESSIONS_DIR, { recursive: true });
  await QRCode.toFile(qrPath, uri!, { width: 400, margin: 2 });
  const qrMarkdown = `![WalletConnect QR](${qrPath})`;
  const qrOpenCommands = buildQrOpenCommands(qrPath);
  const openclawMediaDirective = `MEDIA:${qrPath}`;

  const autoOpen = shouldAutoOpenQR(args.open);
  let openedBySystem = false;

  // Auto-open QR in terminal environments
  if (autoOpen) {
    openedBySystem = openFile(qrPath);
  }

  // Build output for agent/CLI environments.
  const output: Record<string, unknown> = {
    status: "waiting_for_approval",
    interactionRequired: true,
    userReminder:
      "Wallet pairing is waiting for your confirmation. Please open your wallet app and approve or reject the request.",
    message: "Scan and approve this WalletConnect request in your wallet app.",
    qrPath,
    qrMarkdown,
    uri,
    deliveryPlan: {
      preferred: ["image_attachment", "markdown_image"],
      fallback: "wc_uri",
      fallbackWhen: [
        "image_not_supported",
        "image_render_failed",
        "image_delivery_failed",
      ],
      image: {
        qrPath,
        qrMarkdown,
        qrOpenCommands,
      },
      wcUri: {
        uri,
      },
    },
    deliveryHint:
      "Primary delivery is QR image (qrPath/qrMarkdown). Use wc URI only when image rendering or image delivery is not supported.",
    openclaw: {
      mediaDirective: openclawMediaDirective,
      fallbackUri: uri,
      rule:
        "For OpenClaw channel delivery, emit mediaDirective as a standalone line first. Only use fallbackUri when media delivery is unsupported or fails.",
    },
  };

  if (!autoOpen || !openedBySystem) {
    output.note =
      "If QR image preview is unavailable, try opening qrPath with a system image viewer first. Use the wc URI only if image rendering/delivery is not supported.";
    output.qrOpenCommands = qrOpenCommands;
  }

  if (autoOpen && !openedBySystem) {
    output.openFailed = true;
  }

  printJson(output);

  try {
    const session = await approval();
    const accounts = Object.values(session.namespaces).flatMap((ns) => ns.accounts || []);
    const walletName = session.peer?.metadata?.name || "Unknown Wallet";
    const pairedAt = new Date().toISOString();
    const summary = buildPairSummary(accounts);

    saveSession(session.topic, {
      accounts,
      chains,
      peerName: walletName,
      createdAt: pairedAt,
    });

    printJson({
      status: "paired",
      message: `Wallet connected successfully (${walletName}).`,
      topic: session.topic,
      accounts,
      peerName: walletName,
      pairedAt,
      summary: {
        chainCount: summary.chains.length,
        accountCount: accounts.length,
        chains: summary.chains,
        primaryAccount: summary.primaryAccount,
      },
      nextActions: [
        "Use whoami/status to verify the active session.",
        "Use auth if a consent signature is required before operations.",
      ],
    });
  } catch (err) {
    printJson({ status: "rejected", error: (err as Error).message });
  }

  await client.core.relayer.transportClose().catch(() => {});
  process.exit(0);
}
