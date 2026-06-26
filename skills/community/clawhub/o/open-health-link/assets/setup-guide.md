# Open Health Link 健康数据连接助手（当前：breo Scalp5）— 安装指南

## 前置条件

1. **OpenClaw** 已安装并正常运行
2. **Node.js** >= 18.0.0 已安装（[下载地址](https://nodejs.org/)）
3. **breo App** 已安装在手机上，且已注册并登录倍轻松账号
4. 至少使用 Scalp5 设备完成过一次头皮检测

## 安装步骤

### 1. 安装 Skill

将 `Open Health Link` 文件夹复制到 OpenClaw 的 skills 目录中：

```bash
# 方式一：放入个人共享目录（推荐，所有项目可用）
cp -r "Open Health Link" ~/.openclaw/skills/

# 方式二：放入当前工作区（仅当前项目可用）
cp -r "Open Health Link" ./skills/
```

### 2. 重启 OpenClaw

```bash
openclaw gateway restart
# 或在对话中输入 /new 开启新会话
```

### 3. 开始使用

在 OpenClaw 对话中直接说：

- "绑定倍轻松账号"
- "绑定breo账号"
- "打开 Open Health Link"
- "查看头皮报告"
- "我想看看我的头皮检测结果"

首次使用时，skill 会自动安装所需的 Node.js 依赖（仅需几秒），无需手动操作。

## 使用方式

### 绑定账号
对助手说 **"绑定倍轻松账号"** 或 **"绑定breo账号"**，按提示使用 breo App 扫描二维码即可完成授权。

### 查看头皮报告
对助手说 **"查看我的头皮报告"**，即可看到最近 90 天的检测报告摘要和详情。

### 查看护理方案
对助手说 **"查看头皮护理方案"**，即可获取基于检测数据的个性化护理建议。

### 解绑账号
对助手说 **"解绑倍轻松账号"**，即可清除本地授权信息。

## 常见问题

### Q: 二维码生成失败
请检查网络连接是否正常，确保可以访问倍轻松服务。

### Q: 扫码后一直等待
确保在breo App中完成了"同意授权"操作。授权有 10 分钟有效期，超时需重新发起。

### Q: OpenClaw 里二维码没有显示成图片
通常是会话渲染异常。请先让助手重新生成一次二维码并重新发送图片；当前仅支持二维码图片扫码授权，不支持授权链接跳转。

### Q: 查不到检测数据
确认是否在最近 90 天内使用 Scalp5 设备完成过头皮检测，且检测数据已同步到breo App。

## 数据安全

- 授权 Token 默认存储在当前 skill 目录下的 `.open-health-link-data/token.json`（随 skill 一并删除）
- 为兼容历史版本，也会兼容读取旧路径 `~/.openclaw/open-health-link/token.json` 与 `~/.openclaw/breo-scalp5/token.json`
- 不会上传到任何第三方服务
- 随时可通过"解绑倍轻松账号"清除所有本地凭证
