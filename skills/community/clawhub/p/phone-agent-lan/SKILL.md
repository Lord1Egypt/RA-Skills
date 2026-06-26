---
name: phone-agent
description: 手机操控技能。通过 USB ADB 连接安卓手机，捕获屏幕、分析 UI 元素、执行点击/滑动/输入等操作。当用户要求操控手机、执行 App 操作、打开应用、发送消息时使用。
---

# 📱 手机操控技能 (phone-agent)

## 功能概览
- 通过 USB ADB 连接安卓手机
- 捕获手机屏幕（UI Dump，无需 AI 看图）
- 分析界面元素位置（XML 结构解析）
- 执行 UI 操作：点击、滑动、输入文字、按键
- 打开 App、搜索联系人、发送简单消息

## 限制
- ⚠️ 无法直接输入中文（ADB `input text` 绕过输入法，只能输入英文/数字/拼音）
- ⚠️ 需要 USB 调试权限
- ⚠️ 部分国产手机（如小米）需要额外开启"USB 调试安全设置"

---

## 第一部分：手机端配置（新手机一次性操作）

### 1. 开启开发者选项
1. 设置 → 关于手机 → 连续点击"MIUI 版本号"7次
2. 返回设置 → 更多设置 → 开发者选项

### 2. 开启 USB 调试
1. 开发者选项 → 开启"USB 调试"
2. **小米额外设置**：开发者选项 → 开启"USB 调试(安全设置)"
   - 这个需要 SIM 卡关联的小米账号登录后才能开启
   - 或者插 SIM 卡重启后自动解锁

### 3. 连接手机
1. 用 USB 线连接手机和 Mac（电脑）
2. 手机上弹出"允许 USB 调试"→ 点"允许"
3. 建议同时开启"充电模式下允许 ADB"

### 4. 调整手机设置（避免息屏断开）
1. 设置 → 显示 → 息屏时间 → 改为"最长"
2. 或保持手机在充电状态

### 5. 检查连接
```bash
adb devices
```
应显示设备 ID，如 `803203a    device`

---

## 第二部分：Skill 安装检查清单

### 依赖工具（已预装）
- ✅ `adb`（Android SDK Platform Tools）
- ✅ `python3`（内置）
- ✅ 截图工具（系统自带）

### 验证安装
```bash
# 检查 adb
adb version

# 检查 skill 脚本
ls -la ~/.openclaw/skills/phone-agent/agent.py
```

---

## 第三部分：Skill 使用方法

### 基本命令

```bash
# 查看连接状态
python3 ~/.openclaw/skills/phone-agent/agent.py connected

# 截图并保存到临时文件
python3 ~/.openclaw/skills/phone-agent/agent.py screenshot

# 获取屏幕尺寸
python3 ~/.openclaw/skills/phone-agent/agent.py size

# 点击坐标 (x, y)
python3 ~/.openclaw/skills/phone-agent/agent.py tap 500 1000

# 滑动 (x1, y1, x2, y2, duration)
python3 ~/.openclaw/skills/phone-agent/agent.py swipe 600 2400 600 800

# 输入文字（仅英文/数字）
python3 ~/.openclaw/skills/phone-agent/agent.py text "hello"

# 按键
python3 ~/.openclaw/skills/phone-agent/agent.py home      # HOME 键
python3 ~/.openclaw/skills/phone-agent/agent.py back      # 返回键
python3 ~/.openclaw/skills/phone-agent/agent.py power     # 电源键

# 启动 App（包名）
python3 ~/.openclaw/skills/phone-agent/agent.py start com.tencent.mm

# 强制停止 App
python3 ~/.openclaw/skills/phone-agent/agent.py stop com.tencent.mm
```

---

## 第四部分：典型工作流程

### 流程一：打开微信并搜索联系人

```bash
# 1. 启动微信
adb shell monkey -p com.tencent.mm -c android.intent.category.LAUNCHER 1

# 2. 等待启动后，dump UI 结构
adb exec-out uiautomator dump /sdcard/dump.xml && adb pull /sdcard/dump.xml /tmp/dump.xml

# 3. 分析 XML，找到搜索按钮坐标
python3 << 'EOF'
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/dump.xml')
root = tree.getroot()
for node in root.iter():
    text = node.attrib.get('text', '')
    bounds = node.attrib.get('bounds', '')
    if '搜索' in text or 'search' in text.lower():
        print(f"TEXT: {text}, BOUNDS: {bounds}")
EOF

# 4. 点击搜索按钮（如坐标 [912,140][1056,284]）
python3 ~/.openclaw/skills/phone-agent/agent.py tap 984 212

# 5. 输入搜索文字
python3 ~/.openclaw/skills/phone-agent/agent.py text "蓝汐"

# 6. 在搜索结果 XML 中找到联系人坐标，点击进入
```

### 流程二：发送消息

```bash
# 1. 在聊天界面，找到输入框和发送按钮的坐标
# 2. 点击输入框
python3 ~/.openclaw/skills/phone-agent/agent.py tap 540 2534

# 3. 输入文字
python3 ~/.openclaw/skills/phone-agent/agent.py text "hello"

# 4. 点击发送按钮（如坐标 [1020,1476][1170,1608]）
python3 ~/.openclaw/skills/phone-agent/agent.py tap 1095 1542
```

---

## 第五部分：UI Dump 分析指南

### 获取 UI 结构
```bash
adb exec-out uiautomator dump /sdcard/dump.xml && adb pull /sdcard/dump.xml /tmp/dump.xml
```

### 分析脚本
```python
import xml.etree.ElementTree as ET

tree = ET.parse('/tmp/dump.xml')
root = tree.getroot()

# 查找所有可点击元素
for node in root.iter():
    text = node.attrib.get('text', '')
    bounds = node.attrib.get('bounds', '')
    clickable = node.attrib.get('clickable', '')
    resource_id = node.attrib.get('resource-id', '')
    
    if clickable == 'true' and text:
        print(f"TEXT: {text!r}, BOUNDS: {bounds}, ID: {resource_id}")

# 查找特定关键词
for node in root.iter():
    text = node.attrib.get('text', '')
    bounds = node.attrib.get('bounds', '')
    if '微信' in text or '搜索' in text:
        print(f"FOUND: {text!r}, BOUNDS: {bounds}")
```

### 从 bounds 计算点击坐标
```python
# bounds = "[228,1766][1008,1835]"
# 中心点: x = (228+1008)/2 = 618, y = (1766+1835)/2 = 1800
```

---

## 第六部分：常见问题

### Q: USB 频繁断开
**A:** 
1. 手机息屏后会断开 → 开启"保持唤醒"或"充电模式下调试"
2. USB 线质量差 → 换一根好线
3. 重启 ADB: `adb kill-server && adb start-server`

### Q: 点击位置不准
**A:** 
1. 确认屏幕分辨率：`adb shell wm size`
2. UI Dump 的 bounds 是物理坐标，直接计算中心点点击
3. 多次点击有偏移可以调整 ±10-20 像素

### Q: 无法输入中文
**A:** 
- ADB `input text` 只能输入 ASCII 字符
- 解决方案：
  1. 在手机上预先打开输入法，让 AI 控制粘贴
  2. 使用 ClipboardManager（需要 App 配合）
  3. 通过 App Inventor 开发专用剪贴板 App

### Q: 小米手机点击无效
**A:** 
- 必须开启"USB 调试(安全设置)"
- 设置 → 更多设置 → 开发者选项 → USB 调试安全设置

### Q: 如何获取 App 包名？
**A:**
```bash
# 方法1: 列出已安装包
adb shell pm list packages | grep 关键词

# 方法2: 在 Play 商店查看 URL 中的 id
# 方法3: 用 UI Dump 分析桌面图标
```

---

## 附录：常用 App 包名

| App | 包名 |
|-----|------|
| 微信 | `com.tencent.mm` |
| QQ | `com.tencent.mobileqq` |
| 美团 | `com.sankuai.meituan` |
| 淘宝 | `com.taobao.taobao` |
| 支付宝 | `com.eg.android.AlipayGphone` |
| 抖音 | `com.ss.android.ugc.aweme` |
| 小红书 | `com.xingin.xhs` |
| Blued | `com.soft.blued` |
