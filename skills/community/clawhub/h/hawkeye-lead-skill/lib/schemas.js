// 10 个线索接口的唯一 schema 真相来源。CLI（bin/cli.js）从这里动态生成子命令、
// flag、--help 文本和 --schema 输出；不再有单独维护的 API 白名单或字段文档。
//
// 字段权威来源：leaddatacollector 仓库 pom.xml 锁定的精确版本
// com.xiaohongshu.fls.thrift:lib-thrift-lead-data-collector-idls:0.0.4（下称"IDL jar"）——
// 反编译这个 RPC 请求/响应类的编译产物拿到的字段定义，比只读业务实现代码
// （LeadQueryServiceImpl / LeadOperationServiceImpl，分支 feature/add-insite-account-distribution-fields）
// 更权威，因为业务代码可能遗漏它没实际读取的 IDL 字段。
// 枚举值对照 leaddatacollector 的 enums/FollowStatus.java、AcceptLevel.java、LeadStatus.java、
// AuditStatus.java、TeamType.java、AttrCategoryEnum.java 源码逐一核实。
//
// 已确认但不属于任何单个接口的公共规律（写在这里，不写进每个 entry 重复一遍）：
// - 请求体字段是 snake_case，不是 camelCase（camelCase 会被网关静默忽略，不会报错）
// - 响应体统一是 {code, success, msg, data: {...}}
// - HTTP↔RPC 网关转发层本身（含 camelCase→snake_case 规律）不在 leaddatacollector 仓库里，
//   具体在哪个仓库未知，这层转发本身没有实测确认；已用真实 token 跑通过 HTTP 调用的接口见
//   下面每个 entry 的 verified 字段
// - 权限模型：私海列表的 owner 永远是当前登录人，传别的 owner_id 无效；没权限查看的线索会被
//   伪装成 "lead not found"，不会明确提示"无权限"

// ── 响应体共享 $defs（get_lead_detail 的 data.lead 与 list_private_leads / list_public_leads
//    的 data.leads[] 元素共用同一份 LeadDTO schema）──
const DEFS = {
  AttrDTO: {
    type: "object",
    description: "线索画像标签/属性",
    properties: {
      attr_key: { type: "string" },
      attr_label: { type: "string" },
      attr_values: { type: "array", items: { type: "string" } },
      source: { type: "string" },
      category: {
        type: "integer",
        enum: [0, 1],
        description: "0=普通（非标签类展示），1=标签类（公海/私海列表页展示的标签）",
      },
    },
  },
  FollowLogDTO: {
    type: "object",
    description: "跟进日志条目",
    properties: {
      content: { type: "string" },
      created_at: { type: "integer", description: "毫秒时间戳" },
      action_type: { type: "string" },
      action_name: { type: "string" },
      operator_id: { type: "string" },
      operator_name: { type: "string" },
    },
  },
  ScoreDetailDTO: {
    type: "object",
    description: "评分明细，均为 double",
    properties: {
      total_score: { type: "number" },
      ces_score: { type: "number" },
      fans_buying_score: { type: "number" },
      outer_gmv_score: { type: "number" },
      avg_item_price_score: { type: "number" },
      follower_score: { type: "number" },
    },
  },
  HotItemDTO: {
    type: "object",
    description: "热卖商品（结构上任何返回 outer_shops[] 的接口都可能带，只是 list 接口业务上大概率不填充，不是 get_lead_detail 独有字段）",
    properties: {
      item_id: { type: "string" },
      title: { type: "string" },
      image_urls: { type: "array", items: { type: "string" } },
      price: { type: "number" },
      month_sales: { type: "integer" },
      total_sales: { type: "integer" },
      item_url: { type: "string" },
    },
  },
  OuterShopDTO: {
    type: "object",
    description: "站外店铺信息",
    properties: {
      shop_id: { type: "string" },
      shop_name: { type: "string" },
      company_name: { type: "string" },
      license_no: { type: "string" },
      legal_person: { type: "string" },
      platform: { type: "integer", description: "站外平台 code，具体枚举定义未在 lead 模块内找到，暂不做值域约束" },
      platform_name: { type: "string" },
      shop_type_zh: { type: "string" },
      main_category: { type: "string" },
      location: { type: "string" },
      settle_status: { type: "string" },
      avg_item_price: { type: "integer" },
      month_gmv: { type: "integer" },
      year_gmv: { type: "integer" },
      b_level: { type: "string" },
      shop_url: { type: "string" },
      ext: { type: "object", description: "未知 key 集合，历史备注是资质/行业标签", additionalProperties: { type: "string" } },
      qcc_phone: {
        type: "string",
        description: "企业工商注册电话（企查查来源）。⚠️ 受 get_lead_detail 的 plain_phone 开关控制：plain_phone=false（list_* 接口固定用这个）时脱敏，true 时明文",
      },
      qcc_phone_zone: { type: "string", description: "qcc_phone 的区号部分" },
      hot_items: { type: "array", items: { $ref: "#/$defs/HotItemDTO" } },
    },
  },
  HotNoteDTO: {
    type: "object",
    description: "热门笔记",
    properties: {
      note_id: { type: "string" },
      title: { type: "string" },
      cover_url: { type: "string" },
      note_url: { type: "string" },
      like_count: { type: "integer" },
      fav_count: { type: "integer" },
      comment_count: { type: "integer" },
      published_at: { type: "integer", description: "毫秒时间戳" },
    },
  },
  InsiteAccountDTO: {
    type: "object",
    description: "站内小红书账号信息",
    properties: {
      author_id: { type: "string" },
      nickname: { type: "string" },
      account_url: { type: "string" },
      region: { type: "string" },
      follower_count: { type: "integer" },
      note_count: { type: "integer" },
      avg_note_ces: { type: "number" },
      fans_dgmv: { type: "integer" },
      fan_buyer_cnt30d: { type: "integer" },
      trade_fan_avg_dgmv: { type: "integer" },
      insite_carrier_dgmv30d: { type: "number" },
      insite_shop_url: { type: "string" },
      total_asset: { type: "integer" },
      like_cnt30d: { type: "integer" },
      fav_cnt30d: { type: "integer" },
      gender_dist: { type: "string", description: "JSON 字符串" },
      age_dist: { type: "string", description: "JSON 字符串" },
      fan_r_level_dist: { type: "string", description: "JSON 字符串" },
      fan_r4_plus_ratio: { type: "number" },
      carrier_dgmv_dist: { type: "string", description: "JSON 字符串" },
      ext: { type: "object", description: "资质/行业标签等", additionalProperties: { type: "string" } },
      hot_notes: { type: "array", items: { $ref: "#/$defs/HotNoteDTO" } },
      login_phone: {
        type: "string",
        description: "登录手机号。⚠️ 受 get_lead_detail 的 plain_phone 开关控制：plain_phone=false（list_* 接口固定用这个）时脱敏，true 时明文",
      },
      login_phone_zone: { type: "string" },
      pro_account_phone: {
        type: "string",
        description: "专业号客服电话。⚠️ 同 login_phone，受 plain_phone 开关控制",
      },
      pro_account_phone_zone: { type: "string" },
    },
  },
  LeadDTO: {
    type: "object",
    description: "线索完整信息。get_lead_detail 的 data.lead 与 list_private_leads / list_public_leads 的 data.leads[] 元素共用这份 schema",
    properties: {
      lead_id: { type: "string" },
      lead_name: { type: "string" },
      source_type: { type: "string" },
      score_level: { type: "string", enum: ["S0", "S1", "S2"] },
      score: { type: "number" },
      owner_id: { type: "string", description: "未认领时为空字符串" },
      owner_name: { type: "string", description: "未认领时为空字符串" },
      owner_email: { type: "string", description: "未认领时为空字符串" },
      owner_dept_id: { type: "string", description: "未认领时为空字符串" },
      owner_dept_name: { type: "string", description: "未认领时为空字符串" },
      claimed_at: { type: "integer", description: "认领时间戳（毫秒）" },
      follow_status: {
        type: "string",
        enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
      },
      accept_level: {
        type: "integer",
        enum: [300, 200, 100, -100],
        description: "300=P0(强意向) 200=P1(中意向) 100=P2(弱意向) -100=不采纳；未标记时字段可能缺省",
      },
      remark: { type: "string" },
      industry: { type: "string" },
      created_at: { type: "integer", description: "毫秒时间戳" },
      audit_status: {
        type: "integer",
        enum: [0, 1, 2, 3],
        description: "0=待审核 1=已上线（对普通用户可见） 2=已驳回 3=已下线",
      },
      team_type: {
        type: "integer",
        enum: [0, 1, 2],
        description: "0=生态+KA共享 1=生态 2=KA",
      },
      audit_time: { type: "integer", description: "毫秒时间戳" },
      lead_status: {
        type: "integer",
        enum: [0, 1, 2, 3, 4, 5],
        description: "0=未注册 1=已注册可客保 2=已开店可客保 3=未开店已客保 4=已开店已客保 5=已挂接(CRM)",
      },
      attrs: { type: "array", items: { $ref: "#/$defs/AttrDTO" } },
      follow_logs: { type: "array", items: { $ref: "#/$defs/FollowLogDTO" } },
      score_detail: { $ref: "#/$defs/ScoreDetailDTO" },
      outer_shops: { type: "array", items: { $ref: "#/$defs/OuterShopDTO" } },
      insite_accounts: { type: "array", items: { $ref: "#/$defs/InsiteAccountDTO" } },
    },
  },
};

const RESPONSE_ENVELOPE = {
  success: { type: "boolean" },
  code: { type: "integer" },
  msg: { type: "string" },
};

// list_private_leads / list_public_leads 共用的过滤字段（除各自独有的 follow_status/accept_level/not_online 外）
const LIST_COMMON_FILTER_PROPERTIES = {
  lead_id: { type: "string" },
  lead_name: { type: "string", description: "⚠️ 实测过滤没有明显生效，网关是否透传未确认" },
  industries: { type: "array", items: { type: "string" }, description: "⚠️ 未实测确认网关层是否透传" },
  score_level: { type: "string", enum: ["S0", "S1", "S2"], description: "⚠️ 未实测确认网关层是否透传" },
  keyword: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  platform: { type: "integer", description: "站外平台 code，枚举定义未确认；⚠️ 未实测确认网关层是否透传" },
  main_category: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  settle_status: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  outer_shop_type: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  avg_item_price_min: { type: "integer", description: "⚠️ 未实测确认网关层是否透传" },
  avg_item_price_max: { type: "integer", description: "⚠️ 未实测确认网关层是否透传" },
  insite_shop_type: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  follower_count_min: { type: "integer", description: "⚠️ 未实测确认网关层是否透传" },
  follower_count_max: { type: "integer", description: "⚠️ 未实测确认网关层是否透传" },
  province: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  brand_name: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  followable_status: { type: "string", description: "⚠️ 未实测确认网关层是否透传" },
  lead_status: {
    type: "integer",
    enum: [0, 1, 2, 3, 4, 5],
    description: "0=未注册 1=已注册可客保 2=已开店可客保 3=未开店已客保 4=已开店已客保 5=已挂接(CRM)；⚠️ 未实测确认网关层是否透传",
  },
  page_num: { type: "integer", default: 1, description: "✅ 已实测生效" },
  page_size: { type: "integer", default: 20, description: "✅ 已实测生效，服务端上限 500" },
};

export const API_SCHEMAS = {
  get_lead_detail: {
    id: "get_lead_detail",
    command: "get-lead-detail",
    path: "/edith/api/seller/merchant_lead/get_lead_detail",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "获取线索详情",
    notes: [
      "⚠️ 不是纯只读接口：当 source=private 且 plain_phone=true 时，(1) insite_accounts[].login_phone/pro_account_phone 和 outer_shops[].qcc_phone 会连同主手机号一起返回明文（默认脱敏）；(2) 如果该线索当前是 PENDING/CONTACTED 状态，会静默把跟进状态自动推进为 TALKING。没有明确业务需要、没有征得用户同意之前不要传 plain_phone=true。",
      "not_online 字段读 LeadQueryServiceImpl.getLeadDetail 方法体确认完全没被使用，传了没有任何效果，是 IDL 里的死字段。",
      "没有权限查看该 lead_id 时，响应会伪装成业务失败 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        source: { type: "string", enum: ["private", "public"], description: "私海详情传 private 才可能返回明文手机号，见 notes" },
        plain_phone: { type: "boolean", default: false, description: "是否返回明文手机号，见 notes 的 PII 警示" },
        not_online: { type: "boolean", description: "IDL 死字段，服务端不读取，传了无效果" },
      },
      required: ["lead_id"],
    },
    responseSchema: {
      type: "object",
      properties: { ...RESPONSE_ENVELOPE, data: { type: "object", properties: { lead: { $ref: "#/$defs/LeadDTO" } } } },
      $defs: DEFS,
    },
  },

  list_private_leads: {
    id: "list_private_leads",
    command: "list-private-leads",
    path: "/edith/api/seller/merchant_lead/list_private_leads",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "查询私海线索列表",
    notes: [
      "owner 永远是当前登录人，请求里没有也不能传别人的 owner——不存在“查别人私海”这回事。",
      "没有权限查看的线索会被伪装成 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
      "not_online 读 LeadQueryServiceImpl.listPrivateLeads 方法体确认服务端固定写死 false（只看已上线数据），忽略请求里传的值，因此这里不暴露 not_online 字段（跟 list_public_leads 不同）。",
      "只有 page_num/page_size/lead_id 是实测确认过真实生效的，其它过滤字段用之前先 --dry-run 看一眼、再拿真实调用验证效果。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        ...LIST_COMMON_FILTER_PROPERTIES,
        follow_status: {
          type: "string",
          enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
          description: "私海独有过滤字段；⚠️ 未实测确认网关层是否透传",
        },
        accept_level: {
          type: "integer",
          enum: [300, 200, 100, -100],
          description: "私海独有过滤字段，数字 code 不是字符串；⚠️ 未实测确认网关层是否透传",
        },
      },
      required: [],
    },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            page_num: { type: "integer" },
            page_size: { type: "integer" },
            leads: { type: "array", items: { $ref: "#/$defs/LeadDTO" } },
          },
        },
      },
      $defs: DEFS,
    },
  },

  list_public_leads: {
    id: "list_public_leads",
    command: "list-public-leads",
    path: "/edith/api/seller/merchant_lead/list_public_leads",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "查询公海线索列表",
    notes: [
      "not_online 这里服务端有实际读取（未传或 false → 只看已上线 audit_status=1；true → 只看未上线/待审核 0/2/3），跟 list_private_leads 里 not_online 被服务端忽略的情况不同。",
      "没有权限查看的线索会被伪装成 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
      "只有 page_num/page_size/lead_id 是实测确认过真实生效的，其它过滤字段用之前先 --dry-run 看一眼、再拿真实调用验证效果。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        ...LIST_COMMON_FILTER_PROPERTIES,
        not_online: { type: "boolean", description: "未传或 false=只看已上线；true=只看未上线/待审核。✅ 服务端实际读取" },
      },
      required: [],
    },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            page_num: { type: "integer" },
            page_size: { type: "integer" },
            leads: { type: "array", items: { $ref: "#/$defs/LeadDTO" } },
          },
        },
      },
      $defs: DEFS,
    },
  },

  private_stat: {
    id: "private_stat",
    command: "private-stat",
    path: "/edith/api/seller/merchant_lead/private_stat",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "私海线索概览统计",
    notes: ["ownerId 完全来自登录态（IDL 已删除 req.ownerId 字段），不需要也不能传参数。"],
    requestSchema: { type: "object", properties: {}, required: [] },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            following_count: { type: "integer", description: "跟进中（TALKING）" },
            converted_count: { type: "integer", description: "已客保（PROTECTED）" },
            settled_count: { type: "integer", description: "已入驻数" },
            active_count: { type: "integer", description: "动销数" },
            converted_gmv: { type: "integer", description: "转化累计 GMV" },
            public_total: { type: "integer", description: "对侧公海总数（权限过滤后）" },
          },
        },
      },
    },
  },

  public_stat: {
    id: "public_stat",
    command: "public-stat",
    path: "/edith/api/seller/merchant_lead/public_stat",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "公海数据信息",
    notes: [],
    requestSchema: { type: "object", properties: {}, required: [] },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            s0_count: { type: "integer" },
            s1_count: { type: "integer" },
            s2_count: { type: "integer" },
            private_total: { type: "integer", description: "当前用户自己的私海总数" },
          },
        },
      },
    },
  },

  update_follow_status: {
    id: "update_follow_status",
    command: "update-follow-status",
    path: "/edith/api/seller/merchant_lead/update_follow_status",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "更新跟进状态",
    notes: [
      "未经真实 HTTP 调用验证，字段已对照 RPC 源码 + IDL jar + FollowStatus 枚举源码三方确认。",
      "follow_status 服务端严格校验，传枚举外的值直接报错（不是静默忽略）。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        follow_status: {
          type: "string",
          enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
          description:
            "PENDING=待建联 CONTACTED=已建联 TALKING=沟通中 INTERESTED=有明确意向 NO_INTENT=无意向(终态) PROPOSAL_SENT=已提供营销方案 PROTECTED=已客保 SETTLED=已入驻(终态) CRM_BLOCKED=已被CRM挂接(终态)",
        },
      },
      required: ["lead_id", "follow_status"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  update_remark: {
    id: "update_remark",
    command: "update-remark",
    path: "/edith/api/seller/merchant_lead/update_remark",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "更新线索备注",
    notes: ["未经真实 HTTP 调用验证，字段已对照 RPC 源码 + IDL jar 确认。remark 传空字符串会被当成清空备注处理，不会报错。"],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        remark: { type: "string", description: "备注内容，允许空字符串（清空备注）" },
      },
      required: ["lead_id", "remark"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  update_accept_level: {
    id: "update_accept_level",
    command: "update-accept-level",
    path: "/edith/api/seller/merchant_lead/update_accept_level",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "更新采纳情况（私海优先级）",
    notes: [
      "未经真实 HTTP 调用验证，字段已对照 RPC 源码 + IDL jar + AcceptLevel 枚举源码三方确认。",
      "⚠️ accept_level 是数字 code，不是 \"P0\" 这种字符串；传枚举外的数字会被服务端拒绝。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        accept_level: {
          type: "integer",
          enum: [300, 200, 100, -100],
          description: "300=P0(强意向) 200=P1(中意向) 100=P2(弱意向) -100=不采纳",
        },
      },
      required: ["lead_id", "accept_level"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  claim_lead: {
    id: "claim_lead",
    command: "claim-lead",
    path: "/edith/api/seller/merchant_lead/claim_lead",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "认领线索",
    notes: [
      "未经真实 HTTP 调用验证，字段已对照 RPC 源码 + IDL jar 确认。",
      "认领人身份完全来自登录态（token 对应的操作人），不能代别人认领。",
      "业务错误“线索已被认领，请刷新页面查看最新数据”是正常的抢单失败场景，不代表调用方式错了。",
      "⚠️ 白名单接口里没有对应的“取消认领”接口，调用前必须格外谨慎——测试泳道也是真实数据（公海线索 2 万+条），不是沙箱假数据。",
    ],
    requestSchema: {
      type: "object",
      properties: { lead_id: { type: "string", description: "线索 ID" } },
      required: ["lead_id"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  assign_lead: {
    id: "assign_lead",
    command: "assign-lead",
    path: "/edith/api/seller/merchant_lead/assign_lead",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "分配线索",
    notes: [
      "未经真实 HTTP 调用验证，字段已对照 RPC 源码 + IDL jar 确认。",
      "只改归属人（owner），不会动跟进状态（follow_status）。",
      "触发分配动作的操作人来自登录态，跟 owner_* 字段（被分配人）是两个不同的角色，不要混淆。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        owner_id: { type: "string", description: "被分配人的操作人 ID（必填）" },
        owner_name: { type: "string" },
        owner_email: { type: "string" },
        owner_dept_id: { type: "string" },
        owner_dept_name: { type: "string" },
      },
      required: ["lead_id", "owner_id"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },
};

export function listCommands() {
  return Object.values(API_SCHEMAS);
}

export function getSchemaByCommand(command) {
  return listCommands().find((s) => s.command === command) || null;
}
