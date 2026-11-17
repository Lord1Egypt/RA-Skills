// 目前仅支持一套环境（线索项目还在测试泳道，上线后如需切换正式域名，改这里或用环境变量覆盖即可）
export const DOMAIN =
  process.env.HAWKEYE_LEAD_DOMAIN ||
  "hawkeye-luren33.devops.sl.beta.xiaohongshu.com";

// 鹰眼的鉴权 cookie 命名规律是 `access-token-<域名>`（已通过浏览器实测确认），
// 因此默认直接从域名派生，无需单独维护；如遇到规律变化可用环境变量覆盖。
export const COOKIE_NAME =
  process.env.HAWKEYE_LEAD_COOKIE_NAME || `access-token-${DOMAIN}`;

export const BASE_URL = `https://${DOMAIN}`;

// 用于从 ~/.token/sso_token.json 里挑对应环境的免登录兜底 token（见 auth.js）。
// 根因已确认（见 apiClient.js 顶部注释）：merchant_lead 这批接口在 edith 网关上挂了专门的
// SSO 插件，这个插件不认这里挑出来的 ambient token，必须用 auth set-token 手动设置针对
// 当前域名签发的真实 cookie。上线到正式域名后这个插件是否认 ambient token 尚未实测确认。
export const AMBIENT_SSO_TIER = DOMAIN.includes(".sit.")
  ? "sit"
  : DOMAIN.includes(".beta.")
    ? "beta"
    : "prod";

