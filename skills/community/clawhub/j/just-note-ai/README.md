# 记一下 (just-note)

> 像发消息一样记录一切，AI 自动分类整理，让知识自然生长。

## 设计理念

**AI 做大脑（理解/分类），CLI 做手脚（执行）**

- **消息模式**（主要）：微信/飞书发消息 → AI 自动理解分类 → 调用 CLI 写入
- **CLI 模式**（备用）：明确指定参数 → CLI 直接执行 → 写入文件

## 快速开始

### 安装

```bash
# 克隆或复制到 OpenClaw skills 目录
cp -r ~/openclaw/workspace/skills/just-note ~/.openclaw/skills/just-note

# 测试安装
just-note help
```

### 使用

#### 方式 1：微信/飞书消息（推荐）

发送消息即可，AI 自动分类：
```
花了 200 块买书
```

AI 自动处理：
- 类型：expense
- 金额：200
- 标签：[book, learning]

#### 方式 2：CLI 命令（调试用）

明确指定参数：
```bash
just-note write --type expense --amount 200 --tags "book,learning" --content "买书"
```

查看今日记录：
```bash
just-note today
```

搜索历史记录：
```bash
just-note search "产品"
```

## 功能特性

- ✅ 零摩擦输入（微信/飞书消息）
- ✅ AI 自动分类（9 类内容）
- ✅ AI 标签生成
- ✅ AI 标题生成
- ✅ 统一存储，多视图呈现
- ✅ 智能检索（关键词 + 类型）
- ✅ 日记视图（按天聚合）
- ✅ 周报/月报（AI 生成）

## 内容类型

| 类型 | 说明 |
|------|------|
| inspiration | 灵感、创意 |
| idea | 想法、心得 |
| knowledge | 知识点 |
| expense | 支出 |
| income | 收入 |
| diary | 日记 |
| task | 待办 |
| quote | 引用 |
| other | 其他 |

## 文档

完整文档见 [SKILL.md](SKILL.md)

## 许可证

MIT License
