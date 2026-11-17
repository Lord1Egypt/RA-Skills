# 蓝牙键盘配对（Logitech K780/K380 类）

配合 `bluetoothctl` 交互式配对的补充细节，聚焦「键盘类外设」的配对方式与失败模式识别。

## 配对方式（罗技官方文档确认）

1. 键盘进入配对模式：长按 Easy-Switch 键（F1/F2/F3 之一）约 **3 秒**，至指示灯**快速闪烁**。配对窗口持续约 **3 分钟**（不是 30 秒），不用赶。
2. 主机端 `bluetoothctl` 走标准流程（agent on → default-agent → scan on → devices → scan off → pair <MAC>）。
3. 主机显示 6 位码（`[agent] Passkey: 655109`，DisplayPasskey）。
4. **用户在键盘敲入这 6 位数字，然后按 Enter**。官方文档原文：`Type the on-screen password and press enter or return.`（中文版：`输入屏幕上显示的代码，然后按下键盘上的 Enter 键`）。

关键结论：配对不是「输入快慢」问题，而是「键盘输入 Passkey + Enter」这个操作本身。

## 多槽位双 MAC 现象

Easy-Switch 三槽位（F1/F2/F3）各自广播**不同的 MAC 地址**。同一把键盘可能扫出多个地址（例如 `...A2:35` 与 `...A2:38`），须以**当前活跃广播槽**的 MAC 为准，否则 pair 会 `not available`。

## 三种失败模式识别（本会话实测 + 官方文档验证）

| 现象 | 含义 | 对策 |
|------|------|------|
| `AuthenticationCanceled` | 认证窗口内没完成输入/确认 | 压缩「发码→输入」节奏，用户见码即输 |
| `not available` | 失败后系统已移除设备记录 | 设备重进配对模式（长按 Easy-Switch 3s），先 `scan on` 再 `pair` |
| 连接即断、Passkey 未出现 | 配对方式细节未对上（非输入速度） | 停止盲目重试，查厂商官方配对文档 |

## 诊断原则：盲试 ≥2 次失败即查官方文档

同一操作盲目重试两次仍失败，说明「反复失败 = 细节没对上」，不是速度快慢问题。此时应先停手，查厂商官方配对文档（`web_search "<品牌> <型号> 配对 方法 配对码 Passkey Enter"`），确认配对方式后再重试。避免无效重复试错。
