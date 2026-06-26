/**
 * WeCom Target Resolver (企业微信目标解析器)
 * 
 * 解析 OpenClaw 的 `to` 字段（原始目标字符串），将其转换为企业微信支持的具体接收对象。
 * 支持显式前缀 (party:, tag: 等) 和基于规则的启发式推断。
 * 
 * **关于“目标发送”与“消息记录”的对应关系 (Target vs Inbound):**
 * - **发送 (Outbound)**: 支持一对多广播 (Party/Tag)。
 *   例如发送给 `party:1`，消息会触达该部门下所有成员。
 * - **接收 (Inbound)**: 总是来自具体的 **用户 (User)** 或 **群聊 (Chat)**。
 *   当成员回复部门广播消息时，可以视为一个新的单聊会话或在该成员的现有单聊中回复。
 *   因此，Outbound Target (如 Party) 与 Inbound Source (User) 不需要也不可能 1:1 强匹配。
 *   广播是“发后即忘” (Fire-and-Forget) 的通知模式，而回复是具体的会话模式。
 */

export interface WecomTarget {
    touser?: string;
    toparty?: string;
    totag?: string;
    chatid?: string;
    kefu?: {
        openKfId: string;
        externalUserId: string;
    };
}

export interface ScopedWecomTarget {
    accountId?: string;
    target: WecomTarget;
    rawTarget: string;
}

/**
 * Parse a `wecom-kefu:<accountId>:<openKfId>:<externalUserId>` or
 * `wecom-kefu:<openKfId>:<externalUserId>` target into its components.
 */
export function parseKefuScopedTarget(raw: string): {
    accountId?: string;
    openKfId: string;
    externalUserId: string;
} | undefined {
    const trimmed = raw.trim();
    if (!/^wecom-kefu:/i.test(trimmed)) return undefined;
    const rest = trimmed.replace(/^wecom-kefu:/i, "");
    const parts = rest.split(":");
    if (parts.length < 2) return undefined;
    if (parts.length >= 3) {
        const [accountId, openKfId, ...tail] = parts;
        const externalUserId = tail.join(":").trim();
        const openKfIdTrimmed = (openKfId ?? "").trim();
        const accountIdTrimmed = (accountId ?? "").trim();
        if (!openKfIdTrimmed || !externalUserId) return undefined;
        return {
            accountId: accountIdTrimmed || undefined,
            openKfId: openKfIdTrimmed,
            externalUserId,
        };
    }
    const [openKfId, ...tail] = parts;
    const externalUserId = tail.join(":").trim();
    const openKfIdTrimmed = (openKfId ?? "").trim();
    if (!openKfIdTrimmed || !externalUserId) return undefined;
    return {
        openKfId: openKfIdTrimmed,
        externalUserId,
    };
}

function parseUpstreamScopedTarget(raw: string): {
    accountId?: string;
    userId: string;
} | undefined {
    const legacyScoped = raw.match(/^wecom-agent-upstream:([^:]+):([^:]+):(.+)$/i);
    if (legacyScoped) {
        return {
            accountId: legacyScoped[1]?.trim(),
            userId: legacyScoped[3]?.trim() || "",
        };
    }

    const queryIndex = raw.indexOf("?upstream_corp=");
    if (queryIndex < 0 || !raw.startsWith("wecom-agent:")) {
        return undefined;
    }

    const pathPart = raw.slice(0, queryIndex);
    const match = pathPart.match(/^wecom-agent:([^:]+):user:(.+)$/i);
    if (!match) {
        return undefined;
    }

    return {
        accountId: match[1]?.trim(),
        userId: match[2]?.trim() || "",
    };
}

export function buildWecomContextTarget(contextToken: string): string {
    return `wecom:context:${contextToken}`;
}

export function buildWecomKefuTarget(params: {
    accountId?: string;
    openKfId: string;
    externalUserId: string;
}): string {
    const account = params.accountId?.trim();
    if (account) {
        return `wecom-kefu:${account}:${params.openKfId}:${params.externalUserId}`;
    }
    return `wecom-kefu:${params.openKfId}:${params.externalUserId}`;
}

export function resolveWecomContextTarget(raw: string | undefined): { contextToken: string } | undefined {
    const trimmed = raw?.trim();
    if (!trimmed) return undefined;
    const match = trimmed.match(/^(?:wecom|wechatwork|wework|qywx):context:(.+)$/i);
    const contextToken = match?.[1]?.trim();
    return contextToken ? { contextToken } : undefined;
}

/**
 * Parses a raw target string into a WeComTarget object.
 * 解析原始目标字符串为 WeComTarget 对象。
 * 
 * 逻辑:
 * 1. 先检查显式类型前缀 (user:, group:, party:, tag:) —— 优先匹配，不受命名空间前缀影响
 * 2. 移除标准命名空间前缀 (wecom:, qywx: 等)
 * 3. 再次检查类型前缀（处理 wecom:user:xxx 格式）
 * 4. 启发式回退 (无前缀时):
 *    - 以 "wr" 或 "wc" 开头 -> Chat ID (群聊)
 *    - 纯数字 -> 默认 User ID (用户)，避免误判部门导致 81013 错误
 *    - 其他 -> User ID (用户)
 * 
 * @param raw - The raw target string (e.g. "party:1", "zhangsan", "wecom:user:xxx")
 */
/**
 * Broadcast literal guard.
 * 企业微信 API 允许 touser="@all" 将消息推送到应用可见范围内全员。
 * 主 Agent 曾在群聊场景误把 "@all" 作为 `to` 传进来，导致文件泄露给全员。
 * 这里是防御性闸门：遇到任何广播字面量一律拒绝。如果确实需要部门/标签广播，
 * 调用方必须显式使用 `party:<id>` / `tag:<id>` 前缀并自行承担范围确认责任。
 */
const BROADCAST_LITERALS = new Set(["@all", "@everyone", "*", "all"]);

export function isBroadcastLiteral(raw: string | undefined): boolean {
    const trimmed = raw?.trim().toLowerCase();
    if (!trimmed) return false;
    return BROADCAST_LITERALS.has(trimmed);
}

export function resolveWecomTarget(raw: string | undefined, options?: { preferUserForDigits?: boolean }): WecomTarget | undefined {
    if (!raw?.trim()) return undefined;

    const trimmed = raw.trim();

    // 0. Broadcast literal guard — refuse `@all` / `@everyone` / `*` outright.
    // 任何落到这里的广播字面量都返回 undefined，让上游 resolveTargetOrThrow 给出清晰报错。
    if (isBroadcastLiteral(trimmed)) {
        console.warn(`[wecom-target] refusing broadcast literal target=${trimmed}`);
        return undefined;
    }

    // Also reject the stripped form (e.g. `wecom:user:@all` or `user:@all`).
    const strippedForCheck = trimmed
        .replace(/^(wecom-agent|wecom|wechatwork|wework|qywx):/i, "")
        .replace(/^(user|group|chat|party|dept|tag):/i, "")
        .trim();
    if (isBroadcastLiteral(strippedForCheck)) {
        console.warn(`[wecom-target] refusing broadcast literal (stripped) target=${trimmed}`);
        return undefined;
    }

    // 1. 先检查原始字符串中的类型前缀（处理 user:xxx 无前缀格式）
    // 这样即使没有 wecom: 前缀，也能正确识别类型
    if (/^user:/i.test(trimmed)) {
        return { touser: trimmed.replace(/^user:/i, "").trim() };
    }
    if (/^group:/i.test(trimmed) || /^chat:/i.test(trimmed)) {
        return { chatid: trimmed.replace(/^(group:|chat:)/i, "").trim() };
    }
    if (/^party:/i.test(trimmed) || /^dept:/i.test(trimmed)) {
        return { toparty: trimmed.replace(/^(party:|dept:)/i, "").trim() };
    }
    if (/^tag:/i.test(trimmed)) {
        return { totag: trimmed.replace(/^tag:/i, "").trim() };
    }

    // 2. Remove standard namespace prefixes (移除标准命名空间前缀)
    let clean = trimmed.replace(/^(wecom-agent|wecom|wechatwork|wework|qywx):/i, "");

    // 3. 再次检查类型前缀（处理 wecom:user:xxx 格式）
    if (/^user:/i.test(clean)) {
        return { touser: clean.replace(/^user:/i, "").trim() };
    }
    if (/^group:/i.test(clean) || /^chat:/i.test(clean)) {
        return { chatid: clean.replace(/^(group:|chat:)/i, "").trim() };
    }
    if (/^party:/i.test(clean) || /^dept:/i.test(clean)) {
        return { toparty: clean.replace(/^(party:|dept:)/i, "").trim() };
    }
    if (/^tag:/i.test(clean)) {
        return { totag: clean.replace(/^tag:/i, "").trim() };
    }

    // 4. Heuristics (启发式规则)

    // Chat ID typically starts with 'wr' or 'wc'
    // 群聊 ID 通常以 'wr' (外部群) 或 'wc' 开头
    if (/^(wr|wc)/i.test(clean)) {
        return { chatid: clean };
    }

    // Pure digits: Default to User (纯数字默认为用户)
    // 原因：1) Bot WS 主动推送只接受 touser/chatid，不接受 toparty/totag
    //      2) 用户 ID 在企业微信中常为纯数字
    //      3) 部门推送应使用显式前缀 "party:xxx" 或通过 Agent 模式
    // 如果确实需要发送到部门，请使用 party: 前缀或 Agent 路径
    if (/^\d+$/.test(clean)) {
        if (options?.preferUserForDigits === false) {
            return { toparty: clean };
        }
        return { touser: clean };
    }

    // Default to User (默认为用户)
    return { touser: clean };
}

export function resolveScopedWecomTarget(raw: string | undefined, defaultAccountId?: string): ScopedWecomTarget | undefined {
    if (!raw?.trim()) return undefined;

    const trimmed = raw.trim();

    const kefuScoped = parseKefuScopedTarget(trimmed);
    if (kefuScoped) {
        const accountId = kefuScoped.accountId || defaultAccountId;
        return {
            accountId,
            target: {
                touser: kefuScoped.externalUserId,
                kefu: {
                    openKfId: kefuScoped.openKfId,
                    externalUserId: kefuScoped.externalUserId,
                },
            },
            rawTarget: `${kefuScoped.openKfId}:${kefuScoped.externalUserId}`,
        };
    }

    const upstreamScoped = parseUpstreamScopedTarget(trimmed);
    if (upstreamScoped) {
        const accountId = upstreamScoped.accountId || defaultAccountId;
        return {
            accountId,
            target: { touser: upstreamScoped.userId },
            rawTarget: upstreamScoped.userId,
        };
    }

    const agentScoped = trimmed.match(/^wecom-agent:([^:]+):(.+)$/i);
    if (agentScoped) {
        const accountId = agentScoped[1]?.trim() || defaultAccountId;
        const rawTarget = agentScoped[2]?.trim() || "";
        // Agent scoped targets are almost always users in a conversation context.
        // In this scope, we prefer treating numeric IDs as User IDs to avoid 81013 errors.
        const target = resolveWecomTarget(rawTarget, { preferUserForDigits: true });
        return target ? { accountId, target, rawTarget } : undefined;
    }

    const target = resolveWecomTarget(trimmed);
    return target
        ? {
            accountId: defaultAccountId,
            target,
            rawTarget: trimmed,
        }
        : undefined;
}
