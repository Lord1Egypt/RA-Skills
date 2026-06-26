# 环境变量获取指南

## ① FEISHU_APP_ID / FEISHU_APP_SECRET（飞书应用凭证）

在飞书开放平台创建自建应用即可获得。

### 创建应用

| 步骤 | 操作 |
|------|------|
| 1 | 打开 https://open.feishu.cn/app 并登录飞书账号 |
| 2 | 点击右上角「创建企业自建应用」 |
| 3 | 填写应用名称（如"发票报销机器人"）、描述 |
| 4 | 创建成功后进入应用详情页 |

### 获取凭证

左侧菜单 →「凭证与基础信息」：

```
App ID:      cli_a930938b51789cc5   ← 直接可见，复制
App Secret:  cYJH706...             ← 点"显示"按钮获取
```

### 配置权限

应用必须开启以下权限，否则 API 调用会返回 403：

| 权限名称 | 权限代码 | 用途 |
|---------|---------|------|
| 获取用户发给机器人的消息 | `im:message` | 接收用户发送的发票图片/PDF |
| 获取用户在群中发给机器人的消息 | `im:message.group_at_msg` | 群聊中 @ 机器人（可选）|
| 以应用的身份发送消息 | `im:message:send_as_bot` | 发送确认卡片和通知 |
| 获取资源（图片与文件） | `im:resource` | 下载发票图片和 PDF |
| 审批实例:创建 | `approval:instance:create` | 提交费用报销审批 |
| 审批实例:只读 | `approval:instance:readonly` | 查询审批状态 |

配置路径：
1. 应用详情 →「权限管理」
2. 搜索以上权限并添加
3. 「版本管理与发布」→「创建版本」
4. 填写版本号（如 1.0.0）和更新说明
5. 提交审核
6. 企业自建应用由公司飞书管理员在管理后台审批

> ⚠️ 审核通过后应用才能正常调用 API，否则会返回权限不足错误。

---

## ② APPROVAL_CODE（审批模板 Code）

### 方法一：从审批模板 URL 复制（推荐）

1. 飞书客户端 →「审批」应用 →「模板管理」
2. 找到「费用报销agent版」模板，点击进入
3. 浏览器地址栏 URL 末尾的 UUID 即为 Approval Code：

```
https://www.feishu.cn/approval/...?approval_code=6FD315B4-3F00-4B88-A1D5-476804FDDB86
                                                       ↑ 这就是 Approval Code
```

### 方法二：通过 API 查询

```bash
lark-cli api GET /open-apis/approval/v4/approvals \
  --params '{"page_size":20}' \
  -q '.data.items[] | select(.approval_name | contains("费用报销")) | .approval_code'
```

### 如果没有该模板

1. 飞书审批 →「模板管理」→「新建模板」
2. 模板名称：费用报销agent版
3. 添加以下表单控件（控件 ID已在代码中固化）：

| 控件名 | 控件类型 | 控件 ID |
|--------|---------|---------|
| 报销类型 | radioV2 | `widget16510509268920001` |
| 报销事由 | textarea | `widget16510509704570001` |
| 费用明细 | fieldList | `widget16510509950440001` |
| 费用汇总(自动) | formula | `widget16510509818090001` |
| 附件 | attachmentV2 | `widget16510510447300001` |

4. 发布模板
5. 从模板详情页 URL 复制 Approval Code

---

## ③ BOT_DIR（项目路径）

```bash
export BOT_DIR=/path/to/invoice-approval-bot
```

其中包含以下核心文件：
- `invoice_orchestrator.py` — 主程序
- `invoice_ocr.py` — OCR 引擎
- `lark_cli_wrapper.py` — 飞书 CLI 封装
- `invoice_handler.py` — 审批表单构建
- `requirements.txt` — Python 依赖
- `.env` — 配置文件
