---
name: liuli-jinshan-bridge
version: 1.0.1
description: >-
  直接读写金山文档 / WPS 多维表格（通过 WPS 开放平台 dbsheet API，user token 授权链路）。
  当用户提到金山文档、WPS 多维表、kdocs、多维表格、"把数据写进金山/那张表"、"读一下多维表/某张表的记录"、
  "新增/查询表格行"、或粘贴 kdocs.cn 链接要求读写其内容时触发。
  即使用户没说"API""接口"，只要意图是对金山/WPS 多维表格做读取或写入，也应使用本技能。
  注意：本技能不负责把文件存到 139 移动云盘（那是「云盘文件管理」），只针对金山文档/WPS 多维表。
metadata:
  openclaw:
    emoji: 🌉
---

# 琉璃金山桥 · 金山文档多维表读写桥

把 WPS 开放平台「企业自建应用 + user token」链路封装成可直接调用的读写能力：一句对话，即可对指定多维表读取结构 / 新增记录。

## 前置条件（首次一次性配置，详见 references/setup.md）
本技能**不内置任何密钥**。运行前需在本机 `~/.config/wps-openapi/`（权限 600）放好：
- `client_id`（应用 AppID）
- `client_secret`（应用 AppSecret，带外注入，切勿入对话/信箱/日志）
- `refresh_token`（user OAuth 授权后获得，365 天长效；过期需重走一次授权）

脚本会在 access_token 临期时用 refresh_token **自动续期并滚动更新**，因此日常使用一般无需再交互授权。

## 能力与调用

所有脚本在 `scripts/` 下，凭证只从 `~/.config/wps-openapi/` 读取，输出**绝不打印 token/secret 明文**。

### 1. 读取表结构（schema：拿到 sheet_id 与字段）
```bash
node scripts/dbsheet_schema.cjs <file_id>
```
输出该多维表的子表（sheet）与字段（field）概要，供后续写记录定位 `sheet_id` / 字段名。

### 2. 新增一条记录
```bash
node scripts/dbsheet_record_create.cjs <file_id> <sheet_id> '<主字段名>' '<值>'
```
在指定子表写一行（最小可用：单个主字段）。成功返回 record id。

### 3. 仅刷新 / 查看 token 健康
```bash
node scripts/wps_auth.cjs --selftest
```
强制用 refresh 换一次新 token 并校验可用（不落明文）。

> `file_id` 取自 kdocs 链接（`https://www.kdocs.cn/l/<id>` 或分享详情中的数字 file_id）；具体以 schema 接口回包为准。

## 典型工作流
1. 用户给一个多维表 / kdocs 链接要读写；
2. 先 `dbsheet_schema.cjs` 读结构，确认 sheet_id 与字段名；
3. 再 `dbsheet_record_create.cjs` 写一行（或按需求扩展批量/查询）；
4. 把真实 HTTP 状态与 record id 回执用户。

## 关键技术约束（务必知悉，见 references/setup.md 详解）
- **user token 路线**：操作个人空间多维表，app token 会因缺文件级 scope 报 403；必须走 user OAuth。
- **redirect_uri 必须与后台授权时完全一致**（含末尾斜杠），否则 code 换 token 失败。
- **refresh 轮换**：每次刷新会使旧 refresh 失效，脚本已自动落新值；多端共用同一把 refresh 须约定单一持有方轮换。
- **写记录非幂等**：全成全败；多端并发写同一表须错开时间。
- **本应用未开启接口签名**：调用只需 `Authorization: Bearer <token>`，无需 KSO-1 签名头。

## 安全红线（不可破）
- AppSecret / access_token / refresh_token / 授权 code 的**明文**一律：不入对话、不入信箱、不入代码、不入日志、**不打进技能分发包**。
- 凭证仅存活于 `~/.config/wps-openapi/` 600 文件；带外获取的密钥邮件"即用即焚"。
