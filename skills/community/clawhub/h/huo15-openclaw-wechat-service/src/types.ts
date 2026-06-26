/**
 * 微信服务号（公众号）插件类型定义
 *
 * - 配置 schema：`channels["wechat-service"].{enabled, defaultAccount, accounts}`（v1.0.1+ 必须 kebab-case，与 channel id 对齐）
 * - 每个 account 独立 appId/appSecret/token/encodingAESKey，支持按事件类型路由到不同 agent
 */

export type WechatServiceEncryptMode = "plain" | "compatible" | "safe";

export type WechatServiceDmPolicy = "open" | "pairing" | "allowlist" | "disabled";

export type WechatServiceDmConfig = {
  policy?: WechatServiceDmPolicy;
  allowFrom?: Array<string | number>;
};

export type WechatServiceNetworkConfig = {
  egressProxyUrl?: string;
  timeoutMs?: number;
  mediaDownloadTimeoutMs?: number;
  apiBaseUrl?: string;
};

export type WechatServiceMediaConfig = {
  tempDir?: string;
  retentionHours?: number;
  cleanupOnStart?: boolean;
  maxBytes?: number;
  downloadTimeoutMs?: number;
  localRoots?: string[];
};

export type WechatServiceEventRouting = {
  subscribe?: string;
  unsubscribe?: string;
  scan?: string;
  click?: string;
  view?: string;
  location?: string;
  scancodePush?: string;
  scancodeWaitmsg?: string;
  picSysphoto?: string;
  picPhotoOrAlbum?: string;
  picWeixin?: string;
  locationSelect?: string;
  templateSendJobFinish?: string;
  massSendJobFinish?: string;
};

export type WechatServiceRoutingConfig = {
  defaultAgent?: string;
  events?: WechatServiceEventRouting;
  failClosedOnDefaultRoute?: boolean;
};

export type WechatServiceKnowledgeOdooConfig = {
  url: string;
  db: string;
  username: string;
  password: string;
  articleParentId?: number;
};

export type WechatServiceKnowledgeSyncConfig = {
  enabled?: boolean;
  localPath?: string;
  odoo?: WechatServiceKnowledgeOdooConfig;
};

export type WechatServiceReplyMode = "async" | "passive";

export type WechatServiceAccountConfig = {
  enabled?: boolean;
  name?: string;
  appId: string;
  appSecret: string;
  token: string;
  encodingAESKey?: string;
  encryptMode?: WechatServiceEncryptMode;
  originalId?: string;
  welcomeText?: string;
  replyMode?: WechatServiceReplyMode;
  replyPlaceholderText?: string;
  dm?: WechatServiceDmConfig;
  routing?: WechatServiceRoutingConfig;
  knowledgeSync?: WechatServiceKnowledgeSyncConfig;
  network?: WechatServiceNetworkConfig;
};

/**
 * 角色权限定义：toolName → ["action1","action2"] | "*"（全部 action）
 */
export type RoleToolPermissions = {
  tools?: Record<string, string[] | "*">;
};

/**
 * 动态 Agent 派生配置（与 @huo15/wecom dynamicAgents 同构）
 *
 * - 启用后，每个 openid 会派生一个独立 agent，实现"一粉一会话"
 * - 公众号没有群聊概念，`groupEnabled` 字段保留是为了 schema 与 wecom 对齐，默认 false
 * - `adminUsers` 列表里的 openid 会绕过动态路由，始终使用静态 main agent
 */
export type WechatServiceDynamicAgentsConfig = {
  enabled?: boolean;
  dmCreateAgent?: boolean;
  /** 公众号无群聊场景；保留字段是为了配置形态与 wecom 对齐，默认 false */
  groupEnabled?: boolean;
  adminUsers?: string[];
  /**
   * **权限模式（v2.1.0+）**
   *
   *  - `"open"`（默认）—— 所有 agent 可执行所有 tool action（v0.x ~ v2.0 行为）
   *  - `"admin-only"` —— 写操作仅 main agent 或 adminUsers；读操作放行
   *  - `"role-based"`（v2.2.0+）—— 按 roles / rolePermissions 细粒度控制每个用户的 tool 权限
   *
   * 写操作包括：发文章 / 群发 / 改菜单 / 改用户标签 / 创建卡券 / 给任意 openid
   *   发模板/订阅消息等。
   * 读操作包括：list / get / OCR / OAuth flow / analytics 查询等。
   *
   * 不影响"自然对话"路径（粉丝跟公众号的正常聊天回复走 dispatcher 直接调
   *   sendCustomerServiceMessage，不经 tool）。
   */
  permissionMode?: "open" | "admin-only" | "role-based";
  /**
   * **角色映射（v2.2.0+）**：角色名 → openid 列表。
   * 仅在 permissionMode = "role-based" 时生效。
   * 未匹配的 openid 使用 defaultRole（默认 "customer"）。
   */
  roles?: Record<string, string[]>;
  /**
   * **角色权限（v2.2.0+）**：角色名 → tool/action 权限定义。
   * 仅在 permissionMode = "role-based" 时生效。
   * 未配置的角色使用内置默认权限。
   */
  rolePermissions?: Record<string, RoleToolPermissions>;
  /**
   * **默认角色（v2.2.0+）**：未在 roles 中匹配到的 openid 的兜底角色。
   * 仅在 permissionMode = "role-based" 时生效。默认 "customer"。
   */
  defaultRole?: string;
  /**
   * **默认 persona preset（v2.3.0+）**：动态 agent 派生时给"未匹配 role-based 模式"的
   * 新 agent 注入哪一份 system instructions（人设 prompt）。
   *
   * 内置可选值：
   *  - `"it-support"`（默认）—— 通用 OpenClaw IT 学习客服（开源 / 教学场景）
   *  - `"huo15-customer"` —— 火一五·逸寻智库公众号客服（含 6 产品 / 4 服务 / 课程库 / 转化路径，配合 ~/.openclaw/kb/shared/wiki/huo15-*.md 共享 KB 使用）
   *  - `"none"` / `"off"` —— 不注入 persona，agent 用 OpenClaw 默认行为
   *
   * 仅当 permissionMode != "role-based" 时生效；role-based 模式下走护栏 prompt（v2.2.0）。
   * 用户可通过覆盖 agents.list[].instructions 字段做单 agent 自定义。
   *
   * 完整 persona 文档（运维者参考）见插件包内 `templates/personas/<preset>/{soul,identity,user,agents}.md`。
   */
  defaultInstructionsPreset?: "it-support" | "huo15-customer" | "none" | "off" | string;
};

/**
 * 自动回复 / 业务时间配置（v2.2.0+）
 */
export type WechatServiceBusinessHoursSchedule = {
  days: number[];
  start: string;
  end: string;
};

export type WechatServiceBusinessHoursConfig = {
  timezone?: string;
  schedule?: WechatServiceBusinessHoursSchedule[];
  offHoursMessage?: string;
};

export type WechatServiceAutoReplyConfig = {
  /** 关注后欢迎语模板，支持 {{nickname}} 变量 */
  welcomeText?: string;
  /** 关键词 → 回复文本映射 */
  keywords?: Record<string, string>;
  /** 业务时间配置 */
  businessHours?: WechatServiceBusinessHoursConfig;
};

export type WechatServiceConfig = {
  enabled?: boolean;
  defaultAccount?: string;
  accounts?: Record<string, WechatServiceAccountConfig>;
  media?: WechatServiceMediaConfig;
  network?: WechatServiceNetworkConfig;
  routing?: WechatServiceRoutingConfig;
  knowledgeSync?: WechatServiceKnowledgeSyncConfig;
  dynamicAgents?: WechatServiceDynamicAgentsConfig;
  /** 自动回复配置（v2.2.0+） */
  autoReply?: WechatServiceAutoReplyConfig;
};

export type ResolvedMode = "disabled" | "matrix";

export type ResolvedWechatServiceAccount = {
  accountId: string;
  name?: string;
  enabled: boolean;
  configured: boolean;
  appId: string;
  appSecret: string;
  token: string;
  encodingAESKey: string;
  encryptMode: WechatServiceEncryptMode;
  originalId: string;
  replyMode: WechatServiceReplyMode;
  replyPlaceholderText: string;
  welcomeText: string;
  routing: WechatServiceRoutingConfig;
  dm?: WechatServiceDmConfig;
  knowledgeSync?: WechatServiceKnowledgeSyncConfig;
  network?: WechatServiceNetworkConfig;
  config: WechatServiceAccountConfig;
};

export type ResolvedWechatServiceAccounts = {
  mode: ResolvedMode;
  defaultAccountId: string;
  accounts: Record<string, ResolvedWechatServiceAccount>;
};

export type WechatServiceMsgType =
  | "text"
  | "image"
  | "voice"
  | "video"
  | "shortvideo"
  | "location"
  | "link"
  | "event"
  | "unknown";

export type WechatServiceEventType =
  | "subscribe"
  | "unsubscribe"
  | "SCAN"
  | "LOCATION"
  | "CLICK"
  | "VIEW"
  | "scancode_push"
  | "scancode_waitmsg"
  | "pic_sysphoto"
  | "pic_photo_or_album"
  | "pic_weixin"
  | "location_select"
  | "TEMPLATESENDJOBFINISH"
  | "MASSSENDJOBFINISH";

export type WechatServiceInboundMessage = {
  toUserName: string;
  fromUserName: string;
  createTime: number;
  msgType: WechatServiceMsgType;
  msgId?: string;
  content?: string;
  picUrl?: string;
  mediaId?: string;
  format?: string;
  recognition?: string;
  thumbMediaId?: string;
  locationX?: number;
  locationY?: number;
  scale?: number;
  label?: string;
  title?: string;
  description?: string;
  url?: string;
  event?: WechatServiceEventType;
  eventKey?: string;
  ticket?: string;
  latitude?: number;
  longitude?: number;
  precision?: number;
  raw: Record<string, unknown>;
  rawXml: string;
};

export type WechatServiceTransport = "webhook";

export type WechatServiceConversation = {
  peerKind: "direct";
  peerId: string;
  senderId: string;
};

export type WechatServiceReplyContext = {
  accountId: string;
  toUserName: string;
  fromUserName: string;
  receivedAt: number;
};

export type WechatServiceUnifiedInboundEvent = {
  accountId: string;
  transport: WechatServiceTransport;
  messageId: string;
  text: string;
  senderName?: string;
  conversation: WechatServiceConversation;
  replyContext: WechatServiceReplyContext;
  raw: WechatServiceInboundMessage;
};

export type WechatServicePassiveReply =
  | { type: "text"; content: string }
  | { type: "image"; mediaId: string }
  | { type: "voice"; mediaId: string }
  | {
      type: "video";
      mediaId: string;
      title?: string;
      description?: string;
    }
  | { type: "music"; title?: string; description?: string; musicUrl?: string; hqMusicUrl?: string; thumbMediaId: string }
  | {
      type: "news";
      articles: Array<{
        title: string;
        description?: string;
        picUrl?: string;
        url?: string;
      }>;
    }
  | { type: "transfer_customer_service"; kfAccount?: string };
