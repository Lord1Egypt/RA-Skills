/**
 * ⚠️ 本文件由 OpenAPI 契约生成，前端 agent 禁止手改。
 * 新增端点流程：改 standards/{project}-openapi.yaml → 重新生成本文件 → 两端同步。
 *
 * 替换说明：
 *   - 将 {Project} 替换为你的项目名
 *   - 按你的 OpenAPI YAML 定义填充下方的 API 函数
 *   - 每个端点一行，格式：
 *     n: (params) => request<ResponseType>('METHOD', '/api/v1/path', body, params),
 */
/* eslint-disable */

// ── 运行时配置 ────────────────────────────────────
let _baseUrl = '';
let _getToken: () => string | null = () => null;

export function configureApiClient(opts: { baseUrl: string; getToken: () => string | null }) {
  _baseUrl = opts.baseUrl;
  _getToken = opts.getToken;
}

// ── 请求基础设施 ──────────────────────────────────
async function request<T>(method: string, path: string, body?: unknown, params?: Record<string, string>): Promise<T> {
  const url = new URL(`${_baseUrl}${path}`);
  if (params) Object.entries(params).forEach(([k, v]) => { if (v !== undefined) url.searchParams.set(k, v); });

  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = _getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(url.toString(), { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new ApiError(res.status, err.message ?? res.statusText);
  }
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); this.name = 'ApiError'; }
}

// ══════════════════════════════════════════════════════
// 以下按 OpenAPI YAML 定义填充你的端点
// ══════════════════════════════════════════════════════

// 示例：认证模块
export const auth = {
  health: () =>
    request<{ code: number; message: string; data: { status: string } }>('GET', '/api/v1/auth/health'),

  login: (body: { username: string; password: string }) =>
    request<{ code: number; message: string; data: { accessToken: string; refreshToken: string } }>('POST', '/api/v1/auth/login', body),
};

// ── 在下方添加你的端点 ─────────────────────────────
// 格式：每个端点 = 一个箭头函数，返回 request<返回类型>(方法, 路径, body?, params?)
//
// export const resource = {
//   list: (params?) => request<Paginated<Item>>('GET', '/api/v1/items', undefined, params),
//   get: (id) => request<Single<Item>>('GET', `/api/v1/items/${id}`),
//   create: (body) => request<Single<Item>>('POST', '/api/v1/items', body),
//   update: (id, body) => request<Single<Item>>('PUT', `/api/v1/items/${id}`, body),
//   delete: (id) => request<Single<null>>('DELETE', `/api/v1/items/${id}`),
// };
// ────────────────────────────────────────────────────

// ── 类型别名 ──────────────────────────────────────
type Single<T> = { code: number; message: string; data: T };
type Paginated<T> = { code: number; message: string; data: { records: T[]; total: number; page: number; size: number } };
