# OpenClaw Hot Skills

- ClawHub: https://clawhub.ai/tengj/openclaw-hot-skills
- GitHub: https://github.com/tengj/openclaw-hot-skills
- Author: tengj
- Dependency: requires `clawhub` CLI

发现 ClawHub 上值得关注的热门 Skill，并整理成可读、可安装、可决策的榜单。

它不是简单把搜索结果原样丢出来，而是会帮你做二次整理：
- 看最近最热门的 Skill
- 看更适合“装机必备”的 Skill
- 按主题找某个方向下的热门 Skill
- 自动补全 ClawHub 链接
- 标注本地是否已安装
- 在安装前先做安全审查

---

## 这个 Skill 能做什么

### 1) 全站趋势榜
查看 ClawHub 最近比较热门、值得关注的 Skill。

示例：
- 看看最近热门 skill
- 来一版最近趋势榜
- 最近大家都在装什么 skill

### 2) 装机必备榜
查看更适合长期常用、装机优先级高的 Skill。

示例：
- 来一版装机必备榜
- 给我最常装的 skill
- 新手必备 skill 有哪些

### 3) 主题热门榜
按具体主题找相关 Skill，比如 PDF、GitHub、知识库、浏览器自动化、语音转文字等。

示例：
- 找 PDF 相关热门 skill
- 搜 GitHub 相关 skill
- 看知识库类热门 skill
- 找浏览器自动化方向的 skill

### 4) 已安装状态标注
展示热门 Skill 时，会同时标注：
- 已安装
- 未安装

### 5) 先审后装
如果你说“安装这个 skill”，不会直接安装，而是会先检查：
- 是否有可疑外部请求
- 是否读取敏感文件
- 是否有危险命令
- 是否存在隐藏 prompt injection 风险

---

## 输出长什么样

典型输出格式：

```text
1. Summarize（summarize）【已安装】
- 用途：总结网页、PDF、图片、音频、YouTube 等内容
- 热度：下载 120133 / 当前安装 2562 / 星标 481
- 推荐理由：通用性最强，几乎所有内容处理场景都能用上
- 链接：https://clawhub.com/skills/summarize
```

如果你需要，也可以进一步输出：
- 更适合大多数人
- 更适合开发者
- 更适合知识管理

---

## 排序逻辑

### 趋势榜
优先使用：
- `trending`

### 装机必备榜
优先使用：
- `installsAllTime`
- `installs`

如果 ClawHub 限流或相关接口不可用，会自动 fallback 到：
- `downloads`
- 再结合 `installsCurrent`
- 再结合 `stars`
- 再人工筛掉不适合“装机必备”的小众 Skill

### 主题热门榜
会综合考虑：
- 主题相关性
- 下载量
- 安装量
- 星标
- summary 是否清晰
- 是否真的适合这个主题场景

---

## 安装后的交互方式

你可以继续说：
- 安装第 3 个
- 安装 summarize
- 先审查后安装 github
- 对比这几个 skill 哪个更适合我
- 切换成装机必备榜
- 再来一版 PDF 相关榜单

---

## 适合谁

这个 Skill 适合：
- 想快速了解 ClawHub 生态的人
- 想找“装了就能用”的高价值 Skill 的人
- 想按主题找 Skill 的人
- 想安装前先做一轮安全检查的人

---

## 文件说明

- `SKILL.md`：Skill 主体说明，供 OpenClaw / Agent 触发使用
- `README.md`：给人看的使用说明，适合放 GitHub 仓库首页

---

## 后续可扩展方向

未来还可以继续增强：
- 分主题的更细分类榜单（如 OCR / PDF 提取 / PDF 总结）
- 支持“适合新手 / 适合开发者 / 适合内容创作者”的更多分层
- 对热门 Skill 做更深入的 inspect / compare
