# MBTI Master - 安装指南

**创建者：** 申建  
**版本：** 1.0.0  
**许可证：** MIT License（允许自由使用、修改和分发）

## 快速安装

### 方法1：自动安装脚本

```bash
# 下载并安装
curl -fsSL https://your-domain.com/mbti-master/install.sh | bash
```

### 方法2：手动安装

```bash
# 1. 下载skill包
wget https://your-domain.com/mbti-master/mbti-master.skill.tar.gz

# 2. 解压到skills目录
tar -xzf mbti-master.skill.tar.gz -C ~/.openclaw/skills/

# 3. 添加执行权限
chmod -R +x ~/.openclaw/skills/mbti-master/scripts/
```

## 使用方法

### 基础命令

```bash
# 快速人格测试（5分钟）
bash ~/.openclaw/skills/mbti-master/scripts/quick_test.sh

# 查看特定类型分析
bash ~/.openclaw/skills/mbti-master/scripts/type_analysis.sh INTJ

# 查看兼容性
bash ~/.openclaw/skills/mbti-master/scripts/compatibility.sh INTJ ENFP

# 16型人格速查表
bash ~/.openclaw/skills/mbti-master/scripts/type_cheatsheet.sh

# 认知功能详解
bash ~/.openclaw/skills/mbti-master/scripts/cognitive_functions.sh

# 人格猜猜看游戏
bash ~/.openclaw/skills/mbti-master/scripts/guess_game.sh

# 今日运势
bash ~/.openclaw/skills/mbti-master/scripts/daily_horoscope.sh INTJ
```

## 功能特性

- ✅ 4维度8题快速测试
- ✅ 16型人格完整分析
- ✅ 荣格8种认知功能深度解析
- ✅ 人格兼容性匹配系统
- ✅ 趣味互动游戏
- ✅ 日运生成器（娱乐）
- ✅ 全部本地化运行，保护隐私

## 系统要求

- Bash 4.0+
- 支持颜色的终端（可选）
- 约 50KB 磁盘空间

## 卸载

```bash
rm -rf ~/.openclaw/skills/mbti-master
```

## 更新日志

### v1.0.0 (2026-03-03)
- 初始版本发布
- 包含7个核心功能脚本
- 支持16种人格类型完整分析

## 贡献与反馈

如发现bug或有改进建议，欢迎提交Issue或Pull Request。

## 免责声明

本工具基于荣格认知功能理论和MBTI框架开发，仅供娱乐和自我探索参考。人格类型不应作为评判他人或做出重大人生决策的唯一依据。

---

**开源协议：** MIT License  
**作者：** 申建  
**创建日期：** 2026-03-03