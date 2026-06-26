import { ethers } from "ethers";
import axios from "axios";
import fs from "fs/promises";
import path from "path";

const ENDPOINT_URL = "https://srv.ethermail.io";
const DOMAIN = "moltmail.io";

const STATE_DIR = path.resolve(process.cwd(), "state");
const AUTH_PATH = path.join(STATE_DIR, "auth.json");
const CONFIG_PATH = path.join(STATE_DIR, "config.enc.json");

type AuthData = {
    token: string;
    issuedAt: string;
    userId?: string;
};

export type PrivacyWallType = 'FILTER_ANY_EMAIL_WEB3' | 'FILTER_ANYONE_MY_COMMUNITIES' | 'FILTER_ONLY_COMPANIES_MY_COMMUNITIES';

export const getWalletNonce = async (walletAddress: string) => {
    if (!walletAddress) {
        throw new Error("Wallet address is required");
    } else if (!ethers.isAddress(walletAddress)) {
        throw new Error(`Wallet ${walletAddress} is not a valid EVM address`);
    }

    const headers = await getRequestHeaders();
    const response = await axios.post(
        `${ENDPOINT_URL}/nonce`,
        {
            walletAddress: walletAddress.toLowerCase()
        },
        {
            headers
        }
    );

    return response.data.nonce;
}

export const loginWalletInbox = async (walletAddress: string, signature: string, isMPC: boolean, afid?: string) => {
    if (!ethers.isAddress(walletAddress)) {
        throw new Error(`Wallet ${walletAddress} is not a valid EVM address`);
    }

    const web3Address = getEmailFromWallet(walletAddress);
    const headers = await getRequestHeaders();

    const body: Record<string, any> = {
        web3Address,
        signature,
        isMPC,
        platformData: {
          ai_agent: true,
          platform: "openclaw"
        }
    };

    if (afid) {
        body.afid = afid;
    }

    const response = await axios.post(
        `${ENDPOINT_URL}/authenticate`,
        body,
        {
            headers,
        }
    );

    return response.data.token;
}

export const completeOnboarding = async (walletAddress: string) => {
    if (!ethers.isAddress(walletAddress)) {
        throw new Error(`Wallet ${walletAddress} is not a valid EVM address`);
    }

    const headers = await getRequestHeaders();
    const response = await axios.post(
        `${ENDPOINT_URL}/users/onboarding`,
        {
            email: '',
            isSso: false,
        },
        { headers }
    );

    return response.data;
}

export const saveLoginToken = async (token: string) => {
    const tokenPayload = decodeJwtPayload(token);

    const tokenData = {
        token,
        issuedAt: new Date(tokenPayload['iat'] * 1000),
        expiringAt: new Date(tokenPayload['exp'] * 1000),
        userId: tokenPayload['sub'],
    }

    await fs.writeFile(
        AUTH_PATH,
        JSON.stringify(tokenData, null, 2),
        { mode: 0o600 }
    );
}

export const getLoginToken = async (): Promise<string> => {
    try {
        const raw = await fs.readFile(AUTH_PATH, "utf8");
        const data: AuthData = JSON.parse(raw);

        if (typeof data.token !== "string" || data.token.length === 0) {
            return "";
        }

        const payload = decodeJwtPayload<{ exp?: number }>(data.token);
        if (payload.exp && Date.now() >= payload.exp * 1000) {
            console.warn("Login token has expired. Please run `npm run login` again.");
            return "";
        }

        return data.token;
    } catch {
        return "";
    }
};

export const getRequestHeaders = async () => {
    const headers = {
        "Content-Type": "application/json",
            "Accept": "application/json",
    }

    const loginToken = await getLoginToken();
    if (loginToken) {
        headers['X-Access-Token'] = loginToken
    }

    return headers;
}

export type AuthInfo = { token: string; userId: string };

export const loadAuth = async (): Promise<AuthInfo> => {
    const raw = await fs.readFile(AUTH_PATH, "utf8");
    const data = JSON.parse(raw);
    const token = data.token;
    if (!token) throw new Error("No auth token found. Run `npm run login` first.");

    const payload = decodeJwtPayload<{ exp?: number; sub?: string }>(token);
    if (payload.exp && Date.now() >= payload.exp * 1000) {
        throw new Error("Auth token expired. Run `npm run login` again.");
    }

    const userId = data.userId || payload.sub;
    if (!userId) throw new Error("No userId in auth data. Run `npm run login` again.");

    return { token, userId };
};

export const getConfiguredAddress = async (): Promise<string> => {
    const raw = await fs.readFile(CONFIG_PATH, "utf8");
    const config = JSON.parse(raw);
    if (!config.address) throw new Error("No address in config. Run `npm run setup` first.");
    return config.address;
};

export const getReferralCode = async (): Promise<string | undefined> => {
    try {
        const raw = await fs.readFile(CONFIG_PATH, "utf8");
        const config = JSON.parse(raw);
        return config.referralCode || undefined;
    } catch {
        return undefined;
    }
};

export type EmailAddress = { name: string; address: string };

export type SendEmailPayload = {
    from: EmailAddress;
    to: EmailAddress[];
    cc?: EmailAddress[];
    bcc?: EmailAddress[];
    subject: string;
    html: string;
    text?: string;
};

export type ReplyEmailPayload = SendEmailPayload & {
    reference: { action: "reply"; id: string; mailbox: string };
};

export const listMailboxes = async (userId: string) => {
    const headers = await getRequestHeaders();
    const response = await axios.get(
        `${ENDPOINT_URL}/users/${userId}/mailboxes`,
        { headers, params: { counters: true } }
    );
    return response.data;
};

export const searchEmails = async (
    userId: string,
    mailboxId: string,
    page: number = 1,
    limit: number = 10,
    next?: string
) => {
    const headers = await getRequestHeaders();
    const params: Record<string, string | number> = { page, limit, mailbox: mailboxId };
    if (next) params.next = next;

    const response = await axios.get(
        `${ENDPOINT_URL}/users/${userId}/search`,
        { headers, params }
    );
    return response.data;
};

export const getEmailContent = async (userId: string, mailboxId: string, messageId: string) => {
    const headers = await getRequestHeaders();
    const response = await axios.get(
        `${ENDPOINT_URL}/users/${userId}/mailboxes/${mailboxId}/messages/${messageId}`,
        { headers }
    );
    return response.data;
};

export const markEmailAsRead = async (userId: string, mailboxId: string, messageId: string) => {
    const headers = await getRequestHeaders();
    const response = await axios.put(
        `${ENDPOINT_URL}/users/${userId}/mailboxes/${mailboxId}/messages/${messageId}`,
        { seen: true },
        { headers }
    );
    return response.data;
};

export const sendEmail = async (userId: string, payload: SendEmailPayload) => {
    const headers = await getRequestHeaders();
    const response = await axios.post(
        `${ENDPOINT_URL}/users/${userId}/submit`,
        {
            uploadOnly: false,
            isDraft: false,
            from: payload.from,
            to: payload.to,
            cc: payload.cc || [],
            bcc: payload.bcc || [],
            attachments: [],
            subject: payload.subject,
            date: "",
            text: payload.text || "",
            html: payload.html,
        },
        { headers }
    );
    return response.data;
};

export const replyToEmail = async (userId: string, payload: ReplyEmailPayload) => {
    const headers = await getRequestHeaders();
    const response = await axios.post(
        `${ENDPOINT_URL}/users/${userId}/submit`,
        {
            reference: payload.reference,
            uploadOnly: false,
            isDraft: false,
            from: payload.from,
            to: payload.to,
            cc: payload.cc || [],
            bcc: payload.bcc || [],
            attachments: [],
            subject: payload.subject,
            date: "",
            text: payload.text || "",
            html: payload.html,
        },
        { headers }
    );
    return response.data;
};

export const getEarnedCoins = async () => {
    const headers = await getRequestHeaders();
    const response = await axios.get(
        `${ENDPOINT_URL}/users/rewards-pool`,
        { headers }
    );
    return response.data?.current_pool?.emc_available ?? 0;
};

export const listAddreses = async () => {
    const headers = await getRequestHeaders();
    const response = await axios.get(
        `${ENDPOINT_URL}/addresses`,
        { headers }
    );
    return response.data;
};

export const getEmailFromWallet = (walletAddress: string) => {
    if (!ethers.isAddress(walletAddress)) {
        throw new Error(`Wallet ${walletAddress} is not a valid EVM address`);
    }

    return `${walletAddress.toLowerCase()}@${DOMAIN}`;
}

function decodeJwtPayload<T = any>(token: string): T {
    try {
        const base64Url = token.split('.')[1];                    // get payload part
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayload);
    } catch (err) {
        console.error("Invalid JWT format", err);
        throw err;
    }
}
