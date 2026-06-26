---
name: openclaw-cls-collector
description: "OpenClaw 可观测数据一键采集部署。当用户提到 OpenClaw 采集、CLS 采集部署、一键部署采集器时使用此 Skill。"
---

# OpenClaw CLS 可观测一键采集部署

为 OpenClaw 一键部署可观测数据采集，将运行数据上报到腾讯云 CLS（日志服务）。

## 触发后的交互流程

触发此 Skill 后，**直接向用户收集信息**，简洁输出，不要输出大段说明。

向用户输出以下内容（保持简洁）：

```
开始部署 OpenClaw 可观测采集，请提供以下信息：

1. SecretId（必填）
2. SecretKey（必填）
3. Region（可选，默认 ap-guangzhou 广州）

> 默认在广州地域创建 OpenClaw 专用 CLS 主题。可选地域：ap-shanghai / ap-beijing / ap-chengdu / ap-hongkong / ap-singapore
> 密钥获取：https://console.cloud.tencent.com/cam/capi
> ⚠️ 此方式仅建议测试使用。生产环境建议自行在终端执行，见下方命令。

生产环境推荐自行执行：
curl -fsSL -o /tmp/cls-openclaw-setup https://mirrors.tencent.com/install/cls/openclaw/setup.sh && chmod +x /tmp/cls-openclaw-setup && /tmp/cls-openclaw-setup --secret-id <SecretId> --secret-key <SecretKey> --region ap-guangzhou
```

**重要**：必须等待用户提供 SecretId 和 SecretKey 后才能继续，不要使用占位符执行命令。

## 执行部署

收到用户密钥后，依次执行以下命令。

**注意：`setup` 是二进制可执行文件，不是 shell 脚本，不能通过 `bash` 或管道执行。**

```bash
curl -fsSL -o /tmp/cls-openclaw-setup https://mirrors.tencent.com/install/cls/openclaw/setup.sh
chmod +x /tmp/cls-openclaw-setup
/tmp/cls-openclaw-setup \
  --secret-id <用户提供的SecretId> \
  --secret-key <用户提供的SecretKey> \
  --region <用户选择的地域，默认 ap-guangzhou>
```

## 部署完成后：输出仪表盘链接

部署成功、主题创建完成后，从输出中提取**日志主题 ID（topicId）**，结合**地域（region）**拼接仪表盘链接：

```
https://console.cloud.tencent.com/cls/dashboard/d?templateId=cost-governance-dashboard&var-ds={region},{topicId}&time=now-7d,now&timezone=browser
```

- `var-ds=` 后面是 `{region},{topicId}`，英文逗号连接，无空格
- 示例：`var-ds=ap-guangzhou,fa47580b-74aa-43ff-b772-07036cdf28e7`

向用户提示：**「部署完成，通过以下链接查看 OpenClaw 可观测仪表盘：」** 并附上拼接好的链接。

## 异常处理

| 错误场景 | 排查建议 |
|---------|---------|
| 认证失败 | 确认 SecretId/SecretKey 是否正确，是否有 CLS 权限 |
| 地域不支持 | 检查 Region 拼写，确认已开通 CLS |
| ARM 架构不支持 | 需使用 x86 机器 |
| Windows 不支持 | 需使用 Linux/macOS |
| LogListener 版本冲突 | 旧版本（< 3.4.0）需先升级 |
| 网络连接失败 | 确认可访问腾讯云 API 端点 |

## 注意事项

- 执行完成后不要在对话中重复展示完整密钥
- 不支持的环境会给出明确提示
- 已有 LogListener（≥ 3.4.0）会跳过安装直接配置
- 自动创建的 CLS 资源默认 30 天保留期
