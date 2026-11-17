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
export type Credential = {
    kind: "service_account";
    account: ServiceAccount;
    /** Where it came from, for `doctor`. Never contains key material. */
    source: string;
} | {
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
export type CredentialResolution = {
    ok: true;
    credential: Credential;
    probes: CredentialProbe[];
} | {
    ok: false;
    probes: CredentialProbe[];
};
export type CredentialEnvironment = {
    env?: NodeJS.ProcessEnv;
    home?: string;
    readFileImpl?: (filePath: string) => Promise<string>;
};
/** Where gcloud writes `application-default login` output on each platform. */
export declare function applicationDefaultCredentialsPath(home: string, platform?: NodeJS.Platform): string;
/**
 * Parse a Google credential file.
 *
 * Both shapes Google emits are accepted: a service-account key (what you
 * download from IAM) and an authorized-user file (what
 * `gcloud auth application-default login` writes).
 */
export declare function parseCredentialFile(contents: string, source: string): Credential;
/**
 * Walk the credential sources in order and return the first usable one,
 * along with a record of everything that was tried.
 */
export declare function resolveCredentials(options?: CredentialEnvironment): Promise<CredentialResolution>;
