---
name: minimax-token-plan
description: 查询 MiniMax Token Plan 订阅套餐余额。引导用户配置 API Key（通过 openclaw config set 保存到本地环境变量），查询 M2.7 请求次数、TTS 字符、视频/图片生成配额等。
---

# MiniMax Token Plan 余额查询

## 功能说明

- 查询 M2.7 请求次数
- 查询 TTS HD 语音合成配额
- 查询 image-01 图片生成配额
- 查询 Hailuo 视频生成配额
- 查询 Music-2.5 音乐生成配额

## 首次使用：获取并配置 API Key

**第一步：获取 API Key**
1. 登录 https://platform.minimaxi.com
2. 进入 **用户中心 → 接口密钥**
3. 点击 **创建 Token Plan Key**（必须是 Token Plan 类型）
4. 复制生成的 Key

**快捷链接：**
- Token Plan 页面：https://platform.minimaxi.com/user-center/payment/token-plan
- 接口密钥管理：https://platform.minimaxi.com/user-center/basic-information/interface-key

**第二步：选择查询方式**
复制 Key 后直接粘贴给我，我会问你选择：

- **单次查询**：只查一次，不保存 Key
- **保存到本地**：Key 保存到本地环境变量，以后直接查询

---

## API Key 保存位置

选择保存后，Key 通过 `openclaw config set` 保存到本地环境变量：
```
openclaw config set env.MINIMAX_API_KEY <你的Key>
```

**说明：**
- Key 存储在 OpenClaw 配置文件（非明文显示）
- 仅本地存储，不会上传到任何第三方
- 每个用户的 OpenClaw 独立配置，互不影响

---

## 查询命令

配置好 Key 后，直接说：
- "查询额度"
- "M2.7 还剩多少"
- "Token Plan 报告"

**如果 Key 已保存**：直接查询，无需再提供 Key。
**如果 Key 未保存**：粘贴 Key 后选择是否保存。

---

## 字段映射（重要！）

API 返回的 `current_interval_usage_count` 实际表示**剩余额度**：
- `剩余 = current_interval_usage_count`
- `已用 = current_interval_total_count - current_interval_usage_count`

## 各模型单位

| 模型 | 单位 | 重置周期 |
|------|------|---------|
| M2.7 | 次请求/5h | 5小时滚动 |
| TTS HD | 字符/日 | 每日 |
| image-01 | 张/日 | 每日 |
| Hailuo-Fast | 个/日 | 每日 |
| Hailuo | 个/日 | 每日 |
| Music | 首/日 | 每日 |

## 套餐额度参考

**标准版：**
| 套餐 | M2.7 | TTS | image-01 | Hailuo | Music |
|------|------|-----|----------|--------|-------|
| Starter | 600次/5h | - | - | - | - |
| Plus | 1500次/5h | 4000字符/日 | 50张/日 | - | - |
| Max | 4500次/5h | 11000字符/日 | 120张/日 | 2个/日 | 4首/日 |

**极速版：**
| 套餐 | M2.7-hs | TTS | image-01 | Hailuo | Music |
|------|---------|-----|----------|--------|-------|
| Plus | 1500次/5h | 9000字符/日 | 100张/日 | - | - |
| Max | 4500次/5h | 19000字符/日 | 200张/日 | 3个/日 | 7首/日 |
| Ultra | 30000次/5h | 50000字符/日 | 800张/日 | 5个/日 | 15首/日 |

## 输出格式

```
📊 MiniMax Token Plan（17:54 UTC）

⏱ 滚动窗口（5小时）
━━━━━━━━━━━━━━━━━━━
🟢 M2.7
   4106/4500 次 · 91% · 3h后

📅 每日重置（00:00 UTC）
━━━━━━━━━━━━━━━━━━━
🟢 TTS HD
   11000/11000 字符 · 100% · 22h后
🟢 Hailuo-Fast
   2/2 个 · 100% · 22h后
🟢 Hailuo
   2/2 个 · 100% · 22h后
🟢 Music
   4/4 首 · 100% · 22h后
🟢 image-01
   120/120 张 · 100% · 22h后
```

**状态标签：**
- 🟢 充足（≥80%）
- 🟡 一般（30-80%）
- 🔵 快耗尽（<30%）
- 🔴 耗尽（0%）
