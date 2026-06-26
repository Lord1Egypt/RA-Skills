---
name: openclaw-m0-setup
description: Cloud Memory (m0) 服务当前处于内测阶段，需要申请 IP 白名单才能使用。此 Skill 引导用户获取公网 IP 并联系管理员申请访问权限。
version: 0.2.1
metadata: {"openclaw":{"emoji":"🧠","requires":{"env":[],"bins":["curl"]}}}
---

# Cloud Memory (m0) — 内测访问申请

Cloud Memory 服务当前处于 **内测阶段**，仅对已加入白名单的 IP 开放访问。你当前的 IP 尚未被授权。

请按以下步骤获取访问权限。

---

## Step 1 — 获取本机公网 IP

执行以下命令获取当前机器的公网 IP 地址：

```bash
curl -s cip.cc | head -3
```

如果 `cip.cc` 不可用，依次尝试以下备选方案：

```bash
curl -s ifconfig.me
```

```bash
curl -s ipinfo.io/ip
```

```bash
curl -s httpbin.org/ip
```

从输出中提取 IP 地址，记为 `{PUBLIC_IP}`。

---

## Step 2 — 告知用户

向用户展示以下信息：

> **Cloud Memory 服务当前处于内测阶段** 🔒
>
> 你的公网 IP 地址是：`{PUBLIC_IP}`
>
> 该 IP 尚未加入访问白名单，暂时无法使用 Cloud Memory 服务。
>
> **如何获取访问权限：**
>
> 请将以下信息发送给服务管理员，申请加入白名单：
>
> - **公网 IP**：`{PUBLIC_IP}`
> - **用途说明**：（简要说明使用场景，如"个人开发测试"）
>
> 管理员完成白名单配置后（通常几分钟内），你即可重新运行此安装流程。

---

## Step 3 — 验证是否已开通

用户反馈已加白后，可通过以下命令验证：

```bash
curl -s "{ENDPOINT}/api/health"
```

- 返回 `{"status":"ok"}` 且后续 API 调用不再返回 403 → 已开通，重新运行完整安装流程
- 仍返回 403 → 尚未生效，请稍等片刻或再次联系管理员确认

`{ENDPOINT}` 若用户已提供直接使用，否则提示用户提供服务地址。
