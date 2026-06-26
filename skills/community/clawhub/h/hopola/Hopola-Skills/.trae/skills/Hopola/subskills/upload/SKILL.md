---
name: "hopola-upload"
description: "上传图片与结果资源到 MAAT。Invoke when generated assets need stable hosted URLs for delivery."
---

# Hopola Upload

## 作用
负责上传生成资源并返回稳定链接，供报告引用与分发。

## 触发时机
- `upload_enabled=true`
- 主技能阶段为 `upload`

## 输入
- `files`：本地文件路径数组或图片 URL 数组
- `session_uploaded_images`：当前会话中用户上传的图片引用（附件路径/markdown 图片源/文件句柄）
- `auto_upload_session_images`：是否自动处理会话上传图片（默认 `true`）
- `metadata`：可选附加信息
- `maat_upload_script_path`：默认 `scripts/maat_upload.py`
- `MAAT_TOKEN_API`：上传凭证策略端点（默认 `https://strategy.stariidata.com/upload/policy`）
- `MAAT_TOKEN_API_ALLOWED_HOSTS`：可允许的上传策略主机列表（逗号分隔）
- 历史兼容：`MEITU_TOKEN_API`、`NEXT_PUBLIC_MAAT_TOKEN_API`、`NEXT_PUBLIC_MEITU_TOKEN_API`

## 输出
- `uploaded_urls`
- `upload_status`
- `error_message`
- `source_mapping`：输入来源与最终 URL 的映射（`session|explicit_url|local_file`）

## 执行流程
1. 先做输入归一化：
   - 合并 `files` 与 `session_uploaded_images`。
   - 去重（按标准化 URL 或绝对路径）。
   - 将输入分为三类：`explicit_url`、`local_file`、`session`。
2. 对每个本地/会话文件做基础校验：存在性、格式、大小（<=20MB）。
3. 对 `explicit_url` 先做可访问性验证；可访问则直接复用，不重复上传。
   - 若 URL 非公网可访问（如内网域名、localhost、私有网段或临时签名已失效），按需下载到本地后走 MAAT 上传，返回稳定公网链接。
4. 对需上传的文件统一走 MAAT：
   - 调用 `python3 __SKILL_DIR__/../../scripts/maat_upload.py --file <local_file> --json`
   - 以 MAAT 返回 URL 作为最终交付链接
5. 对 MAAT 返回 URL 做可访问性校验：
   - 先 `HEAD`
   - 如异常再 `GET` 抽样验证
6. 记录每个文件最终链路：`maat|reuse_url`，并写入 `source_mapping`。

## 规则
- 单文件大小不得超过 20MB。
- 上传凭证由 MAAT policy 服务发放，密钥仅从环境变量读取，不在输出中回显。
- 上传策略端点按 `MAAT_TOKEN_API > 历史字段 > 默认端点` 解析，且主机必须命中允许列表。
- 自定义端点命中后输出结构化审计日志（不含敏感参数）。
- 请求日志允许输出接口与状态，不允许输出密钥、签名、token 原文。
- `OPENCLAW_REQUEST_LOG` 默认关闭，仅显式设置为 `1` 时输出调试请求日志。
- 当 `auto_upload_session_images=true` 且存在会话上传图片时，必须优先处理并返回可复用 URL。
- 会话图片上传成功后，应将首图作为上游默认 `primary_source_image_url` 候选值。
- 对商品图链路中的 `product_image_url`，只要输入不是稳定公网 URL（本地路径/会话附件/markdown 图片/非公网 URL），必须先上传并回填后才能进入生图阶段。

## 错误处理
- `missing api key`：提示用户检查 MAAT 相关环境变量配置。
- MAAT 上传失败：返回聚合错误与下一步建议（换图/重试/检查网络与权限）。
- 会话上传图片解析为空：返回 `upload_status=failed` 与缺失说明，提示用户重新上传或显式提供 URL。
- 商品图依赖上传失败时，必须显式标记上游应终止生成并返回可执行重试建议，不允许跳过上传继续生图。
