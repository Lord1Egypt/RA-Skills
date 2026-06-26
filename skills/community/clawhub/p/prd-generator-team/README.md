# PRD GENERATOR - Interactive Demo & iWiki Publish

【产品经理福音(^▽^)】该技能主要协助产品经理输出PRD文档，通过"PRD生成"关键词触发，确认需求信息，即可一键生成完整PRD文档 + 可交互HTML原型 ，并且支持一键发布到iWiki。

---

## 🚀 快速开始

### 安装

下载 `prd-generator-team` 文件并在AIcoding编辑器中（ 如：CodeBuddy / Workbuddy等）安装该skill

验证：在Chat中输入 `PRD生成`，正常响应即成功 ✅

💡**建议使用`Claude最新大模型`**

---

## ⚡ 3个核心指令（先看这里！）

> **所有指令都在 AIcoding编辑器的 Chat 对话框中输入。** Skill 通过特定的触发词识别你的意图，按格式输入成功率更高。

| 关键指令 | 说明 | 在Chat中输入 | 结果输出 |
|---------|------|-------------|---------|
| ① **PRD生成** | 一句话描述需求，自动生成完整PRD | `PRD生成 做一个签到打卡小程序，用户每天签到获积分兑礼品` | PRD文档（.md）+ 可交互HTML原型 + 页面截图 + 流程全景图 |
| ② **PRD修改** | 对已有PRD进行局部修改 | `PRD修改 quiz-game 补充积分过期规则` | 更新后的PRD文档 + HTML原型同步更新 |
| ③ **发布iwiki** | 一键发布PRD到iWiki | `发布iwiki` | 自动打包上传，iWiki页面即时可见 |
---

## ⚠️ 重要提醒

如果你的AIcoding编辑器配置了多个 Skill，可能存在指令冲突，使用时建议关闭非必要的 Skill，避免被其他 Skill 拦截。

---

## 💡 版本更新20260309

1、PC端截图1440px页面全链路适配；

2、修改防绕过机制，执行编辑前强制三项自检；

3、端口自动重试，不再占用固定端口；

4、提高PRD生成速度；

---

## ❓ FAQ

<details>
<summary><strong>Q：Skill安装后无响应？</strong></summary>

可能的原因和解决方法：

1. **Skill未成功导入**：检查 CodeBuddy → 设置 → Skills管理 中是否已显示 `prd-generator-team`
2. **建议模型**：建议选择claude-Opus最新版本，不同模型的理解、响应与执行效果存在差异。
3. **被其他Skill拦截**：如果安装了多个Skill，尝试在新的Chat窗口中单独输入指令
</details>

<details>
<summary><strong>Q：iWiki上传后图片不显示？</strong></summary>

请确认你是通过 Skill 的发布指令完成发布的，而非手动上传 .md 文件。正确操作方式：

1. 在 CodeBuddy Chat 中输入：**`发布iwiki`** 或 **`发布到iWiki {页面ID}`**
2. AI 会自动调用 Skill 内置的 `publish_to_iwiki.py` 脚本完成 zip 打包 + 图片上传 + 尺寸调整
3. 如果 Skill 未被正确触发（观察AI是否有读取 `SKILL.md` 的动作），请检查 Skill 是否在 Skills管理 中处于启用状态

> 💡 判断 Skill 是否成功触发：观察 AI 的执行过程中是否出现 **"读取 SKILL.md"** 的步骤提示。如果没有，说明 Skill 未被激活，需要检查安装和指令格式。
</details>

<details>
<summary><strong>Q：如何更新已发布的iWiki页面？</strong></summary>

1. 先使用 <code>PRD修改 {项目名} {修改内容}</code> 完成 PRD 内容修改
2. 然后输入 <code>发布到iWiki {父页面ID} --cover</code> 覆盖更新
</details>

<details>
<summary><strong>Q：支持哪些产品类型？</strong></summary>
小程序、H5、App、后台系统、API/服务 — 每种类型会自动裁剪适配（如API类型跳过HTML原型检查）。
</details>

---

## 📮 反馈与支持

技能持续迭代中，欢迎联系反馈问题与建议🌹

- 使用指南详细版：查阅 `guide.md`
- AI执行指令详情：查阅 `SKILL.md`
