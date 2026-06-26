---
name: Phone Controller | 手机操控者
description: |
  AI phone controller via ADB + GLM. Controls Android with natural language. | 基于 AutoGLM-Phone 的手机操控技能，用自然语言控制安卓手机。
---

# Phone Controller | 手机操控者

通过自然语言控制安卓手机，AI 理解屏幕内容并自动规划执行步骤。

## 核心用法

用户说指令，如：
- "打开小红书搜索美食"
- "在QQ群里发消息"
- "帮我订外卖"

### 执行规则

- **只读操作**（浏览、搜索、查看）→ 直接执行
- **写入/发送操作**（发消息、下单、支付、改设置、删除数据）→ **必须先向用户确认操作内容，获得明确同意后才执行**
- **敏感界面**（登录页、支付页、银行 app）→ 提示用户手动操作，不自动执行
- **敏感 app 规避**：不要在银行、支付、密码管理、含隐私的聊天 app 中使用本技能
- **操作 allowlist 建议**：优先使用只读操作（查看、搜索）；写入操作仅限用户明确指定的 app 和动作
- 每步操作执行后，向用户汇报执行结果

---

## 执行前检测（必须）

每次使用前，先确认手机已连接且 ADB Keyboard 就绪：

```bash
cd ~/.openclaw/workspace/projects/phone-controller/Open-AutoGLM && source .venv/bin/activate
python main.py --list-devices --quiet
```

预期输出：`✓ 设备ID` 和 `ADB Keyboard...✅ OK`

---

## 完整部署指南

### 第一步：电脑端配置

**安装 ADB（Linux/macOS）**
```bash
# Linux
sudo apt install android-tools-adb

# macOS
brew install android-platform-tools

# 验证
adb --version
```

**克隆项目**
```bash
git clone https://github.com/zai-org/Open-AutoGLM.git \
  ~/.openclaw/workspace/projects/phone-controller/Open-AutoGLM
```

**安装 Python 依赖**
```bash
cd ~/.openclaw/workspace/projects/phone-controller/Open-AutoGLM
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .
```

---

### 第二步：手机端配置

**1. 开启开发者模式**
- 设置 → 关于手机 → 版本号连续点击 10 次
- 返回设置 → 系统 → 看到「开发者选项」

**2. 开启 USB 调试**
- 设置 → 开发者选项 → USB 调试 → 开启
- 手机用 USB 连接电脑

**3. 安装并启用 ADB Keyboard**
- 下载 ADBKeyboard.apk：https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk
- 安装后：设置 → 系统 → 语言与输入法 → 键盘 → 启用 ADB Keyboard
- 设为默认输入法

**4. 授权 USB 调试**
- 手机弹出「是否允许 USB 调试」→ 点击「允许并始终允许」

**5. 验证连接**
```bash
adb devices -l
# 预期输出示例：
# 5D7XUW9DYTWONR59       device usb:1-4 product:PDYT20 model:PDYT20 device:OP4E21
```

---

### 第三步：配置 API Key

从 https://open.bigmodel.cn 获取 API Key，然后在命令中使用：

```bash
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "你的API_KEY" \
  --max-steps 50 \
  "你的指令"
```

---

## 支持的操作

| 操作 | 描述 | 示例 |
|------|------|------|
| `Launch` | 启动应用 | `Launch app="微信"` |
| `Tap` | 点击坐标 | `Tap element=[500,300]` |
| `Type` | 输入文本 | `Type text="你好"` |
| `Swipe` | 滑动屏幕 | `Swipe start=[400,900] end=[400,300]` |
| `Back` | 返回 | - |
| `Home` | 回桌面 | - |
| `Long Press` | 长按 | - |
| `Double Tap` | 双击 | - |
| `Wait` | 等待 | `Wait duration="2 seconds"` |
| `Take_over` | 人工接管 | 登录/验证码等 |

---

## 常见问题排查

### 问题：adb devices 找不到设备
**解决：**
```bash
adb kill-server
adb start-server
adb devices -l
```

### 问题：手机提示「是否允许 USB 调试」
**解决：** 点击「允许并始终允许」（防止每次都要确认）

### 问题：OnePlus/OPPO 等设备 ADB Keyboard 检测失败
**解决：** `main.py` 已使用 `dumpsys input_method` 替代 `ime list -s`，无需手动修复

### 问题：ADB Keyboard 无法输入中文
**说明：** ADB Keyboard 仅支持英文/数字；中文由手机其他输入法完成，无需操作

### 问题：QQ/微信 等应用显示敏感界面无法截图
**说明：** 应用有安全限制，agent 会提示 `Take_over` 需要人工接管

---

## 安全与隐私 | Security & Privacy

### 数据披露

- 手机屏幕截图会发送到外部 GLM API（智谱 https://open.bigmodel.cn）进行理解
- **不要在以下界面使用本技能**：银行/支付 app、密码输入页、含个人隐私的聊天记录
- 智谱的数据政策请参考其官网

### 外部依赖说明

- **Open-AutoGLM**：来自 https://github.com/zai-org/Open-AutoGLM（开源项目）
  - 建议锁定已验证的 commit 或 release 版本，避免直接拉取最新 main 分支
- **ADBKeyboard.apk**：来自 https://github.com/senzhk/ADBKeyBoard
  - 建议下载后校验 APK 文件完整性
- 建议在安装前检查项目 star 数、最近更新时间和 issue 情况
- 建议使用专用测试设备，避免在主力手机上开启 USB 调试

### 使用后清理建议

1. 撤销 USB 调试授权：设置 → 开发者选项 → 撤销 USB 调试授权
2. 关闭 USB 调试：设置 → 开发者选项 → USB 调试 → 关闭
3. 切换回原输入法：设置 → 语言与输入法 → 恢复原默认键盘
4. 如不再需要，卸载 ADB Keyboard

## 项目来源

本技能基于 [zai-org/Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM)，开源项目，持续更新。

---

## 文件结构

```
~/.openclaw/workspace/skills/phone-controller/
  SKILL.md          # 技能说明

~/.openclaw/workspace/projects/phone-controller/
  README.md          # 用户级配置说明（含 API Key）
  Open-AutoGLM/     # GLM 官方项目
    main.py          # 主程序（含 OnePlus 补丁）
    .venv/           # Python 虚拟环境
    phone_agent/     # 核心模块
```