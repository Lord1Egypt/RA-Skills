# MBTI Master

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://semver.org)

由 **ShenJian** 开发的MBTI人格类型分析工具，基于荣格认知功能理论。

## 功能特性

- 🧪 **快速测试**：4维度8题，5分钟获得你的MBTI类型
- 📊 **深度分析**：16型人格完整解析，包含认知功能栈
- 💕 **兼容性匹配**：查看任意两种类型的相处模式
- 🎮 **趣味游戏**：人格猜猜看、日运生成器
- 📚 **认知功能**：8种荣格认知功能详解
- 🔒 **本地运行**：完全离线，保护隐私

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/mbti-master.git
cd mbti-master

# 运行快速测试
bash scripts/quick_test.sh

# 查看特定类型分析
bash scripts/type_analysis.sh INTJ

# 查看兼容性
bash scripts/compatibility.sh INTJ ENFP
```

## 所有命令

| 命令 | 功能 |
|------|------|
| `quick_test.sh` | 4维度8题快速测试 |
| `type_analysis.sh [类型]` | 查看指定类型的详细分析 |
| `compatibility.sh [类型1] [类型2]` | 人格兼容性匹配 |
| `type_cheatsheet.sh` | 16型人格速查表 |
| `cognitive_functions.sh` | 8种认知功能详解 |
| `guess_game.sh` | 人格猜猜看游戏 |
| `daily_horoscope.sh [类型]` | 今日人格运势（娱乐） |

## 安装

### 方法1：Git克隆
```bash
git clone https://github.com/yourusername/mbti-master.git ~/.openclaw/skills/mbti-master
chmod -R +x ~/.openclaw/skills/mbti-master/scripts/
```

### 方法2：下载压缩包
```bash
wget https://github.com/yourusername/mbti-master/releases/download/v1.0.0/mbti-master.skill.tar.gz
tar -xzf mbti-master.skill.tar.gz -C ~/.openclaw/skills/
chmod -R +x ~/.openclaw/skills/mbti-master/scripts/
```

## 2026年MBTI新趋势

本工具包含现代MBTI理论的最新发展：
- 认知功能深度分析（超越简单四字母）
- 镜像类型与黄金配对理论
- 阴影人格概念
- 荣格八维功能详解

## 系统要求

- Bash 4.0+
- 约 50KB 磁盘空间
- 彩色终端支持（可选）

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

[MIT](LICENSE) © ShenJian

---

**作者：** ShenJian  
**创建日期：** 2026-03-03  
**开源协议：** MIT License（允许自由使用、修改和分发）