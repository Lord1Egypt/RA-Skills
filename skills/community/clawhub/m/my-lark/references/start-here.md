# 第一次使用 - 快速入门

## 第一步：确认环境就绪

```bash
# 检查 Python 版本（需要 ≥ 3.10）
python3 --version

# 检查依赖已安装
pip show larksuiteoapi

# 检查凭证文件存在
cat ~/.lark_tokens.json
```

如果凭证文件不存在或格式错误，先参考 SKILL.md「安装步骤」配置。

---

## 第二步：验证 App Token（快速测试）

```bash
curl -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_xxxxxxxx", "app_secret": "your_secret"}'
```

返回内容中包含 `"tenant_access_token"` 即表示凭证有效。

---

## 第三步：选择一个场景

| 你想做什么 | 用哪个命令 |
|-----------|---------|
| 发消息到群 | `python3 /workspace/skills/lark-skill/lark_mcp.py send <chat_id> <内容>` |
| 查我的群列表 | `python3 /workspace/skills/lark-skill/lark_mcp.py chats` |
| 搜索云文档 | `python3 /workspace/skills/lark-skill/lark_mcp.py search <关键词>` |
| 读取文档内容 | `python3 /workspace/skills/lark-skill/lark_mcp.py call docx_v1_document_rawContent '{"document_id":"xxx"}'` |
| 查飞书用户信息 | `python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_user_batchGetId '{}'` |

> **找 chat_id**：先运行 `chats` 命令，返回的列表里每个群都有对应的 `chat_id`。

---

## 第四步：发送第一条消息

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py send oc_xxxxxxxxxxxxxxxx "你好，这是一条测试消息"
```

成功发送后飞书群会收到消息。

---

## 遇到问题？

| 现象 | 第一步排查 |
|------|-----------|
| 报权限错误（99991403）| 确认 `~/.lark_tokens.json` 中 app_id/app_secret 正确 |
| 报 Token 无效（99991663）| 凭证文件过期，重新获取 app_secret |
| 报机器人不在群里（99991700）| 把应用机器人拉入目标群聊 |
| 报找不到文件 | 确认文件 ID 正确，文档是否已分享给应用 |

详细错误码见 `references/errors.md`。
