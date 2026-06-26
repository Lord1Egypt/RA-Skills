# Mood Weather CLI 🌤️

> 用天气可视化你的心情！基于 AI 情绪分析，将文字转化为天气图标 + 治愈文案。

[![npm version](https://img.shields.io/npm/v/mood-weather-cli.svg)](https://www.npmjs.com/package/mood-weather-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 功能特性

- 🌤️ **6 种天气**：晴/多云/雾/雨/雷暴/彩虹，对应不同情绪
- 🤖 **AI 驱动**：基于 DeepSeek LLM 精准识别情绪
- 💬 **多语言**：支持中英文混合输入
- 🔄 **自动重试**：网络异常时自动重试 3 次
- 📊 **健康检查**：`mood --healthcheck` 一键诊断
- 📝 **历史记录**：自动保存分析历史（开发中）
- 📈 **情绪统计**：查看情绪分布（开发中）
- 📋 **周报生成**：周期性情绪报告（开发中）

---

## 🚀 快速开始

### 安装

```bash
npm install -g mood-weather-cli
```

### 配置 API 密钥

创建配置文件 `~/.mood-weather-cli.env`：

```bash
DEEPSEEK_API_KEY=sk-your-api-key-here
```

或者临时设置环境变量：

```bash
export DEEPSEEK_API_KEY=sk-your-api-key-here
```

> 获取 API 密钥：[DeepSeek 控制台](https://platform.deepseek.com/)

### 使用

```bash
# 基础用法
mood 今天心情超好的！

# 输出示例
☀️ 今天阳光灿烂，心情美美哒~
情绪类型：happy
置信度：90%
```

---

## 📖 命令说明

### 情绪分析

```bash
# 中文密语
mood 今天工作很顺利
心情 代码写完了
情绪 好开心

# 英文密语
analyze mood I finished the project
my mood today is great

# 大小写不敏感
Mood 好难过
MOOD 太棒了
```

### 健康检查

```bash
mood --healthcheck

# 输出示例
🌤️  Mood CLI 健康检查

✅ CLI 工具：/opt/homebrew/bin/mood
✅ API 密钥：已配置 (sk-xxxx...xxxx)
✅ 网络连接：正常
✅ DeepSeek 服务：在线

🎉 所有检查通过，可以正常使用！
```

### 查看帮助

```bash
mood --help
mood -h
```

### 高级功能（开发中）

```bash
# 查看情绪统计
mood --stats

# 查看历史记录
mood --history --page=1 --limit=10

# 生成周报
mood --report weekly
mood --report --month
```

---

## 🌤️ 情绪 - 天气映射

| 情绪 | 英文 | 天气图标 | 治愈文案 |
|------|------|---------|---------|
| 开心 | happy | ☀️ | 今天阳光灿烂，心情美美哒~ |
| 平静 | calm | ⛅ | 微风不燥，内心平静 |
| 迷茫 | confused | 🌫️ | 有点看不清方向，需要一点光 |
| 难过 | sad | 🌧️ | 心里在下雨，想找个抱抱 |
| 愤怒 | angry | ⛈️ | 情绪有点爆炸，需要冷静一下 |
| 希望 | hopeful | 🌈 | 雨过天晴，看见彩虹啦 |

---

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 是否必须 |
|--------|------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | ✅ 必须 |
| `MOOD_USER_ID` | 用户 ID（用于历史记录） | ❌ 可选 |

### 配置文件

位置：`~/.mood-weather-cli.env`

```bash
DEEPSEEK_API_KEY=sk-xxx
MOOD_USER_ID=wanwan
```

---

## ⚠️ 常见问题

### 未配置 API 密钥

```
❌ 未配置 DeepSeek API 密钥
修复：编辑 ~/.mood-weather-cli.env 或执行 export DEEPSEEK_API_KEY=sk-xxx
```

### API 密钥无效

```
❌ API 密钥无效或已过期
修复：检查密钥是否正确，或前往 DeepSeek 控制台重新生成
```

### 网络超时

```
❌ 网络超时，请检查连接
修复：检查网络或稍后重试
```

### CLI 工具未找到

```
❌ 未找到 mood 命令
修复：运行 npm install -g mood-weather-cli 或检查 PATH 配置
```

---

## 🧪 测试

```bash
# 运行测试脚本
npm test

# 或手动测试
bash test/test.sh
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

---

## 🙏 致谢

- [DeepSeek](https://deepseek.com/) 提供 AI 情绪分析能力
- [OpenClaw](https://openclaw.ai/) AI Agent 框架

---

## 📮 联系方式

- 作者：万万粥
- Email: wanwan_app@163.com
- GitHub: _(待补充)_

---

**🌤️ 愿你每天都有好心情！**
