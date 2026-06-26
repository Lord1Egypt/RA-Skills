# OpenClaw Clone & Learn

🦞 **复制学习大师** - 把别人养好的 OpenClaw 变成你的

> "站在巨人的肩膀上，让你的 OpenClaw 出生即巅峰"

## 功能

- 📦 **从备份导入** - 解压并导入别人的 OpenClaw 备份
- 🎓 **学习专家模式** - 一键学习傅盛、三万等大神配置
- 📚 **批量导入 Skills** - 对比并批量安装技能
- 🎭 **克隆个性记忆** - 融合专家风格，保留自我
- 🏷️ **创建专家品牌** - 建立你自己的专家档案

## 安装

```bash
# 方法1：通过 skillhub
skillhub install openclaw-clone-learn

# 方法2：手动克隆
git clone https://github.com/zhmza/openclaw-clone-learn.git \
  ~/.openclaw/workspace/skills/openclaw-clone-learn
```

## 使用

### 交互式菜单
```bash
~/.openclaw/workspace/skills/openclaw-clone-learn/clone-learn.sh
```

### 命令行模式
```bash
# 非交互模式
NON_INTERACTIVE=true ./clone-learn.sh help
NON_INTERACTIVE=true ./clone-learn.sh list
NON_INTERACTIVE=true ./clone-learn.sh expert fusheng
```

## 示例

### 学习傅盛专家模式
```bash
./clone-learn.sh
# 选择 2) 学习傅盛专家模式
```

### 从备份导入
```bash
NON_INTERACTIVE=true ./clone-learn.sh import /path/to/backup.tar.gz
```

## 文档

- [SKILL.md](SKILL.md) - 完整使用文档
- [TEST-REPORT.md](TEST-REPORT.md) - 测试报告

## 作者

- GitHub: [@zhmza](https://github.com/zhmza)
- 基于傅盛的养殖经验构建

## 许可证

MIT
