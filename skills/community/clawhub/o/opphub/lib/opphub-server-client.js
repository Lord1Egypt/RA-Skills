//
//   bin/opphub-configure.js list 写死 isDefault: i === 0, 没合并 server 端选中态
//   修: 抽 getDefaultChannel 到 lib, configure list + oauth-login status 都用同一个
//

import { readToken } from "./opphub-plugin-client.js";

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";

// 返回 { selected: { channelType, channelId, isDefault } | null, hint }
//   selected != null → 用户已设默认通道 (plugin CLI configure 设的)
//   selected == null → 用户没设 (走 plugin CLI configure 才会设)
//   err  → token 无效 / server 不通
export async function getDefaultChannel() {
  const tok = await readToken();
  if (!tok?.access_token) {
    return { selected: null, hint: "未登录 (token 缺失)" };
  }
  const url = `${API_BASE}/api/user/channels/default`;
  try {
    const resp = await fetch(url, {
      method: "GET",
      headers: { Authorization: `Bearer ${tok.access_token}` },
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      return {
        selected: null,
        hint: `server 返 ${resp.status}: ${data?.message ?? data?.error ?? "unknown"}`,
      };
    }
    if (data?.ok && data?.isDefault) {
      return {
        selected: {
          channelType: data.channelType,
          channelId: data.channelId,
          isDefault: true,
        },
        hint: `默认通道已设: ${data.channelType}:${data.channelId}`,
      };
    }
    return {
      selected: null,
      hint: data?.error === "no_default"
        ? "未设默认通道 (跑 openclaw opphub configure)"
        : "server 返回非 ok/非 isDefault",
    };
  } catch (e) {
    return { selected: null, hint: `server 调用失败: ${e?.message ?? String(e)}` };
  }
}
