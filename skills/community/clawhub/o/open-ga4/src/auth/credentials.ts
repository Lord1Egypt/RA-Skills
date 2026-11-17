import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import type { ServiceAccount } from "./jwt.js";

/**
 * Credential discovery.
 *
 * Deliberately mirrors Google's own Application Default Credentials order so
 * that anyone who already authenticated for another Google tool, or who is
 * migrating from a GA4 skill that used `GOOGLE_APPLICATION_CREDENTIALS`, is
 * already set up and has nothing to configure.
 */

export type CredentialKind = "service_account" | "authorized_user";

export type Credential =
  | {
      kind: "service_account";
      account: ServiceAccount;
      /** Where it came from, for `doctor`. Never contains key material. */
      source: string;
    }
  | {
      kind: "authorized_user";
      clientId: string;
      clientSecret: string;
      refreshToken: string;
      quotaProjectId?: string;
      source: string;
    };

/** One place the loader looked, and what it found. Drives the diagnose output. */
export type CredentialProbe = {
  label: string;
  path: string;
  status: "used" | "absent" | "unreadable" | "invalid";
  detail?: string;
};

export type CredentialResolution =
  | { ok: true; credential: Credential; probes: CredentialProbe[] }
  | { ok: false; probes: CredentialProbe[] };

export type CredentialEnvironment = {
  env?: NodeJS.ProcessEnv;
  home?: string;
  readFileImpl?: (filePath: string) => Promise<string>;
};

/** Where gcloud writes `application-default login` output on each platform. */
export function applicationDefaultCredentialsPath(home: string, platform = process.platform): string {
  if (platform === "win32") {
    const appData = process.env.APPDATA ?? path.join(home, "AppData", "Roaming");
    return path.join(appData, "gcloud", "application_default_credentials.json");
  }
  return path.join(home, ".config", "gcloud", "application_default_credentials.json");
}

function expandHome(filePath: string, home: string): string {
  if (filePath === "~") {
    return home;
  }
  if (filePath.startsWith("~/")) {
    return path.join(home, filePath.slice(2));
  }
  return filePath;
}

/**
 * A generous cross-platform stand-in for PATH_MAX. Node exposes no such
 * constant; real limits differ by OS (Linux 4096, macOS and older Windows
 * far less), so this only needs to catch what is obviously not a path
 * anyone would type or configure, not match any one OS exactly.
 */
const MAX_PLAUSIBLE_PATH_LENGTH = 4096;

/**
 * True when a value that failed the `{`-prefixed inline-JSON check still
 * plainly is not a file path either: a base64-encoded key, a bare PEM
 * block, or JSON that kept its surrounding quotes from a .env file are the
 * common near-misses, and all are either multi-line, unusually long, or carry
 * a PEM header. Catching these before a filesystem read is attempted matters
 * because a failed read's own error can embed the attempted path verbatim
 * (see the ENAMETOOLONG/EACCES/ENOTDIR handling below), which would otherwise
 * leak exactly the value this check exists to keep out of a path.
 *
 * The PEM test is `-----BEGIN`, not the words `PRIVATE KEY`. Every PEM block
 * opens with that marker, so nothing real is lost, and a pasted JSON key is
 * caught earlier by the `{` test regardless. `PRIVATE KEY` on its own also
 * matched a perfectly ordinary path: somebody who keeps their key in
 * `~/PRIVATE KEYS/ga4.json` had it refused, and the refusal deliberately does
 * not say what tripped it (naming the marker would itself be an excerpt of a
 * private key), so there was no way to work out why from the message.
 */
function looksLikeAMisplacedKeyRatherThanAPath(value: string): boolean {
  return value.includes("\n") || value.length > MAX_PLAUSIBLE_PATH_LENGTH || value.includes("-----BEGIN");
}

/**
 * Parse a Google credential file.
 *
 * Both shapes Google emits are accepted: a service-account key (what you
 * download from IAM) and an authorized-user file (what
 * `gcloud auth application-default login` writes).
 */
export function parseCredentialFile(contents: string, source: string): Credential {
  let parsed: Record<string, unknown>;
  try {
    parsed = JSON.parse(contents) as Record<string, unknown>;
  } catch {
    throw new Error("file is not valid JSON");
  }

  const type = typeof parsed.type === "string" ? parsed.type : undefined;

  if (type === "authorized_user") {
    const clientId = stringField(parsed, "client_id");
    const clientSecret = stringField(parsed, "client_secret");
    const refreshToken = stringField(parsed, "refresh_token");
    if (!clientId || !clientSecret || !refreshToken) {
      throw new Error("authorized-user file is missing client_id, client_secret, or refresh_token");
    }
    return {
      kind: "authorized_user",
      clientId,
      clientSecret,
      refreshToken,
      quotaProjectId: stringField(parsed, "quota_project_id"),
      source,
    };
  }

  if (type === "external_account" || type === "impersonated_service_account") {
    throw new Error(
      `credential type "${type}" is not supported; use a service-account key or gcloud application-default credentials`,
    );
  }

  const clientEmail = stringField(parsed, "client_email");
  const privateKey = stringField(parsed, "private_key");
  if (!clientEmail || !privateKey) {
    throw new Error(
      "service-account file is missing client_email or private_key; download the key file again from Google Cloud",
    );
  }

  return {
    kind: "service_account",
    account: {
      clientEmail,
      // Key files store the PEM with literal "\n" when they have been passed
      // through an environment variable or a shell.
      privateKey: privateKey.replace(/\\n/g, "\n"),
      tokenUri: stringField(parsed, "token_uri"),
    },
    source,
  };
}

function stringField(record: Record<string, unknown>, key: string): string | undefined {
  const value = record[key];
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

/**
 * Walk the credential sources in order and return the first usable one,
 * along with a record of everything that was tried.
 */
export async function resolveCredentials(
  options: CredentialEnvironment = {},
): Promise<CredentialResolution> {
  const env = options.env ?? process.env;
  const home = options.home ?? homedir();
  const read = options.readFileImpl ?? ((filePath: string) => readFile(filePath, "utf8"));

  const probes: CredentialProbe[] = [];

  const candidates: Array<{ label: string; path: string; displayPath?: string } | undefined> = [
    env.GOOGLE_APPLICATION_CREDENTIALS
      ? {
          label: "GOOGLE_APPLICATION_CREDENTIALS",
          path: expandHome(env.GOOGLE_APPLICATION_CREDENTIALS, home),
        }
      : undefined,
    { label: "gcloud application-default credentials", path: applicationDefaultCredentialsPath(home) },
  ];

  // GA4_CREDENTIALS is the highest-priority source and accepts either form
  // someone downloading a key ends up with: the file's contents, pasted
  // straight in, or a path to where they saved it. The two are told apart by
  // whether the trimmed value starts with a brace.
  const inline = env.GA4_CREDENTIALS?.trim();
  if (inline !== undefined && inline !== "") {
    if (inline.startsWith("{")) {
      try {
        const credential = parseCredentialFile(inline, "GA4_CREDENTIALS (pasted key)");
        probes.push({ label: "GA4_CREDENTIALS (pasted key)", path: "(inline)", status: "used" });
        return { ok: true, credential, probes };
      } catch {
        // Deliberately does not include the value, any excerpt of it, or the
        // underlying parser error: JSON.parse embeds the offending text in
        // its message, and a malformed pasted key is still a private key.
        // Probe details are printed to a terminal, read by an agent, and
        // sent to whatever model provider is configured.
        probes.push({
          label: "GA4_CREDENTIALS (pasted key)",
          path: "(inline)",
          status: "invalid",
          detail: "the value starts with { but is not valid service-account JSON",
        });
        // Returns immediately rather than falling through to the other
        // sources: someone who pasted a key and got it wrong needs to hear
        // that the key they pasted is wrong, not that gcloud credentials are
        // also absent.
        return { ok: false, probes };
      }
    }
    if (looksLikeAMisplacedKeyRatherThanAPath(inline)) {
      // Refuse to treat this as a path at all, the same shape the
      // malformed-inline branch above uses: a fixed detail, a placeholder in
      // place of the value, and an immediate return. Attempting to read it
      // would risk a filesystem error whose own message embeds the attempted
      // path verbatim (Node's errno messages quote it), which is exactly the
      // leak this whole check exists to prevent.
      probes.push({
        label: "GA4_CREDENTIALS (file)",
        path: "(GA4_CREDENTIALS value)",
        status: "invalid",
        // Deliberately does not say what specifically about the value looked
        // wrong (a newline, its length, a PEM marker): naming the marker
        // that tripped the check is itself an excerpt of a private key.
        detail:
          "the value is not JSON and does not look like a file path either; check that a key " +
          "was not pasted where a path was expected",
      });
      return { ok: false, probes };
    }
    // The real path is still used to actually read the file; only what is
    // shown in a probe is replaced, since this value came from an
    // environment variable that a person could have pasted a key into
    // rather than a path, and a probe is printed to a terminal, read by an
    // agent, and sent to whatever model provider is configured.
    candidates.unshift({
      label: "GA4_CREDENTIALS (file)",
      path: expandHome(inline, home),
      displayPath: "(GA4_CREDENTIALS value)",
    });
  }

  for (const candidate of candidates) {
    if (!candidate) {
      continue;
    }
    const shown = { label: candidate.label, path: candidate.displayPath ?? candidate.path };
    let contents: string;
    try {
      contents = await read(candidate.path);
    } catch (error) {
      const code = (error as NodeJS.ErrnoException)?.code;
      probes.push({
        ...shown,
        status: code === "ENOENT" ? "absent" : "unreadable",
        // Only the errno code, never the error's own message: Node's errno
        // messages embed the path they tried to open verbatim, and that path
        // may be a mis-pasted key rather than a real path (see
        // looksLikeAMisplacedKeyRatherThanAPath above, which only catches
        // the common cases, not every possible one).
        detail: code === "ENOENT" ? undefined : (code ?? "could not be read"),
      });
      continue;
    }
    try {
      const credential = parseCredentialFile(contents, candidate.label);
      // The placeholder above exists because this value could have been a
      // mis-pasted key rather than a path; a value that just parsed as a
      // valid credential file is provably neither. Showing the real path
      // only here, on success, cannot leak key material the way a failure's
      // path could, and hiding it unconditionally would cost every
      // successful diagnosis its only way to say which key file was
      // actually used, which matters most for a stale path pointing at the
      // wrong file.
      probes.push({ label: candidate.label, path: candidate.path, status: "used" });
      return { ok: true, credential, probes };
    } catch (error) {
      probes.push({ ...shown, status: "invalid", detail: describe(error) });
    }
  }

  return { ok: false, probes };
}

function describe(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}
