# 快速入门指南

## 3 步开始使用

### Step 1: 安装 Skill

将 `openclaw-skill` 文件夹复制到 OpenClaw Gateway 的 skills 目录，然后执行依赖安装。

```bash
cp -r openclaw-skill /path/to/openclaw/gateway/skills/
cd /path/to/openclaw/gateway/skills/openclaw-skill
npm install
```

### Step 2: 配置

在 OpenClaw 界面中填写配置：
- **SaaS 平台地址**：`https://open.tyzxwl.cn`
- **API 密钥**：从平台获取

### Step 3: 开始使用

直接在对话中输入：

```
帮我写一篇关于 [主题] 的文章，用 [模板名] 模板发布到公众号
```

---

## 快速命令

| 命令 | 说明 |
|------|------|
| `/publish` | 开始发布流程 |
| `/quota` | 查询发布额度 |
| `/preview` | 预览排版效果 |
| `/status taskId=xxx` | 查询发布状态 |
| 写一篇...发到公众号 | AI 写作+发布 |
| 排版发布 + 内容 | 仅排版已有内容 |
| 查询额度 | 自然语言查额度 |
| 预览一下 | 自然语言预览 |
| 懒人编辑器 | 唤起技能 |

---

## 示例

```
/publish 写一篇 ChatGPT 的科普文章，用科技蓝模板
```

```
帮我写个美食探店文案发到公众号
```

```
把这篇文章排版后发布：# 标题\n\n内容...
```

```
查询额度
```

```
懒人编辑器
```

---

**需要帮助？** 查看 `FAQ.md` 或联系 lanren0405@163.com
