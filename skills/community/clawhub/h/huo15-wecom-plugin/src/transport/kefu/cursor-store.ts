const DEDUP_LIMIT = 2000;
const SINGLE_ACCOUNT_LIMIT = 500;

type AccountKefuState = {
  cursorByOpenKfId: Map<string, string>;
  seenMsgIds: Map<string, number>;
  inflightByOpenKfId: Set<string>;
};

const accountStates = new Map<string, AccountKefuState>();

function ensureState(accountId: string): AccountKefuState {
  let state = accountStates.get(accountId);
  if (!state) {
    state = {
      cursorByOpenKfId: new Map(),
      seenMsgIds: new Map(),
      inflightByOpenKfId: new Set(),
    };
    accountStates.set(accountId, state);
  }
  return state;
}

export function readKefuCursor(accountId: string, openKfId: string): string | undefined {
  return accountStates.get(accountId)?.cursorByOpenKfId.get(openKfId);
}

export function writeKefuCursor(accountId: string, openKfId: string, cursor: string): void {
  if (!cursor) return;
  const state = ensureState(accountId);
  state.cursorByOpenKfId.set(openKfId, cursor);
}

export function clearKefuCursor(accountId: string, openKfId?: string): void {
  const state = accountStates.get(accountId);
  if (!state) return;
  if (openKfId) {
    state.cursorByOpenKfId.delete(openKfId);
    return;
  }
  state.cursorByOpenKfId.clear();
}

export function rememberKefuMsgId(accountId: string, msgId: string): boolean {
  if (!msgId) return true;
  const state = ensureState(accountId);
  if (state.seenMsgIds.has(msgId)) {
    state.seenMsgIds.set(msgId, Date.now());
    return false;
  }
  state.seenMsgIds.set(msgId, Date.now());
  if (state.seenMsgIds.size > SINGLE_ACCOUNT_LIMIT) {
    const excess = state.seenMsgIds.size - SINGLE_ACCOUNT_LIMIT;
    let removed = 0;
    for (const key of state.seenMsgIds.keys()) {
      if (removed >= excess) break;
      state.seenMsgIds.delete(key);
      removed++;
    }
  }
  // Global safety prune across accounts to bound memory.
  let total = 0;
  for (const s of accountStates.values()) total += s.seenMsgIds.size;
  if (total > DEDUP_LIMIT) {
    for (const s of accountStates.values()) {
      const overflow = Math.max(0, s.seenMsgIds.size - SINGLE_ACCOUNT_LIMIT);
      if (overflow === 0) continue;
      let removed = 0;
      for (const key of s.seenMsgIds.keys()) {
        if (removed >= overflow) break;
        s.seenMsgIds.delete(key);
        removed++;
      }
    }
  }
  return true;
}

export function beginKefuPull(accountId: string, openKfId: string): boolean {
  const state = ensureState(accountId);
  if (state.inflightByOpenKfId.has(openKfId)) return false;
  state.inflightByOpenKfId.add(openKfId);
  return true;
}

export function endKefuPull(accountId: string, openKfId: string): void {
  accountStates.get(accountId)?.inflightByOpenKfId.delete(openKfId);
}

export function __resetKefuCursorStoreForTests(): void {
  accountStates.clear();
}
