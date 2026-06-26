# 快速安装与启动

## 适用对象

适合已经在用 OpenClaw，或者准备给 OpenClaw 增加桌面可视化交互层的用户。

## 方式一：源码运行（推荐）

```bash
git clone https://github.com/kk43994/kkclaw.git
cd kkclaw
npm install
npm start
```

### 为什么推荐源码运行

- 跟进小版本修复更方便，直接 `git pull`
- 配置和调试更灵活
- 更适合经常切换模型、Provider、TTS 或自己改桌面行为的人

## 方式二：下载安装包

最新版本：**v3.1.2**

- Windows: `KKClaw-Desktop-Pet-3.1.2-Setup.exe`
- macOS Intel: `KKClaw-Desktop-Pet-3.1.2-x64.dmg`
- macOS Apple Silicon: `KKClaw-Desktop-Pet-3.1.2-arm64.dmg`

下载地址：
- https://github.com/kk43994/kkclaw/releases

## 使用前提

为了获得完整体验，建议确保：

1. 已安装 Node.js
2. OpenClaw 能正常运行
3. Gateway 可连接
4. 如果要用语音播报 / 声音克隆，提前准备相应 TTS 配置

## 首次使用建议

1. 先跑通 OpenClaw 基础连接
2. 打开 kkclaw 的 Setup Wizard
3. 先完成模型、Gateway、TTS 的基础配置
4. 再去调情绪、声音、桌面表现这些增强项

## 相关链接

- GitHub 仓库：https://github.com/kk43994/kkclaw
- Releases：https://github.com/kk43994/kkclaw/releases
- 在线演示：https://kk43994.github.io/kkclaw/
