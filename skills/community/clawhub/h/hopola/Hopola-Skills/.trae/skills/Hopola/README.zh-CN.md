# Hopola（ClawHub 发布版）

## 简介
Hopola 是一个从检索到多媒体生成再到交付的流水线技能，覆盖：
- 网页检索
- 图片生成
- 视频生成
- 3D 模型生成
- Logo 设计
- 商品图生成
- 结果上传
- Markdown 报告输出

## 能力架构
- 主技能：`SKILL.md`
- 版本文件：`VERSION.txt`
- 子技能：`subskills/` 下 8 个能力单元
- 问询模板：`playbooks/design-intake.md`
- 脚本：`scripts/` 下发布校验与打包工具
- 资产：`assets/` 下 logo、cover、flow

## 安全配置
- 必须由用户主动配置环境变量 `OPENCLOW_KEY`。
- 未配置 `OPENCLOW_KEY` 时必须在 `precheck` 阶段直接拦截，返回 `GATEWAY_KEY_MISSING`，禁止继续调用 Gateway 生成功能。
- 可选配置 `MAAT_TOKEN_API` 指向上传凭证策略接口；未配置时默认使用 `https://strategy.stariidata.com/upload/policy`。
- 历史字段 `MEITU_TOKEN_API`、`NEXT_PUBLIC_MAAT_TOKEN_API`、`NEXT_PUBLIC_MEITU_TOKEN_API` 仍可兼容读取，但建议统一迁移到 `MAAT_TOKEN_API`。
- `MAAT_TOKEN_API_ALLOWED_HOSTS` 用于约束上传策略端点主机（逗号分隔）；默认可信主机包含 `strategy.stariidata.com`。
- `OPENCLAW_REQUEST_LOG` 默认关闭（`0`）；仅在排查上传问题时临时开启，排查完成后应立即关闭。
- `config.template.json` 仅保存 `key_env_name` 和空 `key_value` 占位。
- 发布前执行校验脚本阻断明文 key。

## 快速开始
```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## 调度策略
- 生成类任务采用“固定工具优先，自动发现回退”。
- 当固定工具不可用时，调用 `/api/gateway/mcp/tools` 选择匹配工具。
- 当用户仅上传会话图片（未提供公网 URL）时，先自动读取会话图片并走上传子技能，回填为可访问 URL 后再进入抠图/商品图/3D 等依赖图片输入的阶段。
- 商品图阶段若 `product_image_url` 为非 URL 输入（本地路径、附件引用、markdown 图片源），必须先上传并回填 URL，未成功回填前禁止触发生图。
- 商品图阶段必须满足 `source_image_confirmed=true`，且该源图必须是用户提供或用户明确确认的真实商品图；否则返回 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE` 并停止调用生图工具。
- 商品图调用前统一执行前置校验：工具可用性、参考图可访问性、参数完整性（`image_list`、`prompt`、`output_format`、`size`）。
- 商品图调用时 `image_list` 只能包含已确认的 `product_image_url`，禁止使用占位图、代理图或模型生成图替代源图。
- 当前置校验失败时，返回统一 `structured_error`（含 `code`、`stage`、`message`、`details`、`retry_suggestions`）供 OpenClaw 侧直接处理重试。

## 上传策略
- 上传阶段仅使用 MAAT 直传，统一通过 `scripts/maat_upload.py` 执行。
- 当前策略不使用 Gateway 上传端点，也不再将 MAAT 作为回退分支。
- 对上传返回的 URL 持续做可访问性校验，仅交付稳定可访问链接。
- 调试日志会对敏感字段做脱敏处理，但仍建议只在必要时开启请求日志。

## ClawHub 审核说明（可直接粘贴）
- 必需凭证：`OPENCLOW_KEY`（未配置即 precheck 阶段返回 `GATEWAY_KEY_MISSING` 并中止流程）。
- 外部网络域名：`hopola.ai`（Gateway 工具发现与调用）、`strategy.stariidata.com`（上传策略获取，支持 `MAAT_TOKEN_API` 覆盖但受 `MAAT_TOKEN_API_ALLOWED_HOSTS` 约束）。
- 本地文件访问用途：仅用于读取用户输入文件和会话上传图片并执行上传，不扫描无关目录，不写入用户私有内容。
- 计费保护：无 `OPENCLOW_KEY` 不会进入生成调用；仅在网关鉴权通过时触发真实生成链路与积分扣减。
- 日志策略：`OPENCLAW_REQUEST_LOG=0` 默认关闭；调试开启时对 token、policy、签名与凭证参数强制脱敏。

## 上架文件
- `Hopola-Skills/hopola-clawhub-v<version>-*.zip`
- `README.zh-CN.md`
- `README.en.md`
- `RELEASE.md`
