export const WEBHOOK_PATHS = {
  BOT: "/wecom/bot",
  BOT_ALT: "/wecom",
  AGENT: "/wecom/agent",
  KEFU: "/wecom/kefu",
  BOT_PLUGIN: "/plugins/wecom/bot",
  AGENT_PLUGIN: "/plugins/wecom/agent",
  KEFU_PLUGIN: "/plugins/wecom/kefu",
} as const;

export const API_ENDPOINTS = {
  GET_TOKEN: "https://qyapi.weixin.qq.com/cgi-bin/gettoken",
  SEND_MESSAGE: "https://qyapi.weixin.qq.com/cgi-bin/message/send",
  SEND_APPCHAT: "https://qyapi.weixin.qq.com/cgi-bin/appchat/send",
  UPLOAD_MEDIA: "https://qyapi.weixin.qq.com/cgi-bin/media/upload",
  DOWNLOAD_MEDIA: "https://qyapi.weixin.qq.com/cgi-bin/media/get",
  KEFU_SYNC_MSG: "https://qyapi.weixin.qq.com/cgi-bin/kf/sync_msg",
  KEFU_SEND_MSG: "https://qyapi.weixin.qq.com/cgi-bin/kf/send_msg",
  KEFU_ACCOUNT_LIST: "https://qyapi.weixin.qq.com/cgi-bin/kf/account/list",
  KEFU_UPLOAD_MEDIA: "https://qyapi.weixin.qq.com/cgi-bin/media/upload",
} as const;

export const LIMITS = {
  TEXT_MAX_BYTES: 20_480,
  TOKEN_REFRESH_BUFFER_MS: 60_000,
  REQUEST_TIMEOUT_MS: 15_000,
  MAX_REQUEST_BODY_SIZE: 1024 * 1024,
  BOT_WEBHOOK_PASSIVE_WINDOW_MS: 5_000,
  BOT_WEBHOOK_RESPONSE_URL_TTL_MS: 60 * 60 * 1000,
  BOT_STREAM_WINDOW_MS: 6 * 60 * 1000,
  BOT_WS_HEARTBEAT_MS: 30_000,
} as const;

export const CRYPTO = {
  PKCS7_BLOCK_SIZE: 32,
  AES_KEY_LENGTH: 32,
} as const;
