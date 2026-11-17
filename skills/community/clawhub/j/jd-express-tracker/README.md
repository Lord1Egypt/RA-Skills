# 京东快递查件专家（JD Express Tracker）

京东物流（JD Logistics）运单全流程追踪 Agent。专注实时轨迹查询、派送时效预估、异常诊断与多单批量查询。

## 类型

Agent 型（单个 AI 专家）

## 核心能力

1. **运单号识别与校验**：自动识别并校验京东系运单号（JD / JDV / VA 前缀，15-18 位）。
2. **实时物流轨迹查询**：返回从揽件 → 中转 → 派送 → 签收的完整节点（时间/地点/动作/脱敏操作员）。
3. **派送时效预估**：根据当前节点和历史平均时长，给出预计送达窗口。
4. **异常诊断**：识别长时间无更新、派送失败、中转滞留、地址异常等，给出处理建议。
5. **多单批量查询**：一次最多 10 单，逗号 / 换行分隔即可。

## 使用示例

- 「请提供你的京东快递运单号（通常以 JD 开头、15-18 位），我帮你查询最新物流轨迹与派送进度。」
- 「帮我看看我的京东快递为什么延迟了，预计还要多久能到。」
- 「我有多个京东运单号，能一次性批量查询所有包裹的状态吗？」

## 目录结构

```
jd-express-tracker/
├── .codebuddy-plugin/
│   └── plugin.json            # 专家注册清单
├── agents/
│   └── jd-express-tracker.md  # Agent 定义
├── skills/
│   └── jd-express-tracking/
│       ├── SKILL.md           # 运单查询技能说明
│       └── references/
│           └── api-spec.md    # 京东接口详细规范（请求头/参数/鉴权）
├── avatars/
│   └── expert.png             # 专家头像（512x512 PNG）
└── README.md
```

## 头像

头像位于 `avatars/expert.png`（JD 快递盒 + EXPRESS 徽章主题）。如需替换为自定义形象，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装与注册

```bash
python3 scripts/register_expert.py ~/.workbuddy/plugins/marketplaces/my-experts/plugins/jd-express-tracker/
```

## 打包分享

```bash
python3 scripts/package_expert.py ~/.workbuddy/plugins/marketplaces/my-experts/plugins/jd-express-tracker/
```

## 注意事项

- 仅服务**京东快递**（含京东物流、京东自营、京东第三方承运的 JD 系运单）。识别为顺丰、中通等非京东单号时，会提示用户切换到对应专家。
- 运单号属于敏感信息，**不写入日志**、操作员手机号脱敏为 `138****0000` 形式。
- 物流数据存在 5-30 分钟延迟，结果中会注明「数据来自京东物流系统，仅供参考」。
- 涉及派送员联系方式、改派等需登录京东账户的操作，引导用户到京东 APP 处理。
