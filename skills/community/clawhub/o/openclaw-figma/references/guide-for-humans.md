# Figma × AI 工作流指南（面向人类）

> 本指南面向 Omada 产品和研发团队，说明如何利用 Figma MCP + AI Agent 提升设计到代码的效率。

---

## 一、能做什么？

### 1. 设计稿 → 前端代码（最成熟）
把 Figma 设计稿喂给 AI（Claude Code / Codex），自动生成 React/Vue/HTML 代码。
- 支持指定使用现有组件库（如 Ant Design），AI 不会重新造轮子
- 预计前端实现时间缩短 40-70%

### 2. 运行中的页面 → Figma 设计图层（新能力）
Claude Code 开发的页面可以直接 `Send to Figma`，变成可编辑的 Figma 图层。
- 设计师可以直接在上面批注和修改
- 适合"代码先行"的原型迭代场景

### 3. 组件库审查与对齐
AI 可以读取组件库，对比设计稿中实际使用的组件与组件库定义，发现不一致。

### 4. 设计 Token 提取
自动提取颜色、间距、字体等设计变量，生成 CSS Variables / JS Token 文件。

---

## 二、前置条件

| 条件 | 状态 | 说明 |
|------|------|------|
| Figma Personal Access Token | ✅ 已配置 | 用于 API 读取 |
| 组件库 Published | ✅ 1743+848 组件 | WEB + APP 两套完整组件库 |
| MCP Server | ✅ 免费可用 | Remote MCP，无需桌面端 |
| Code Connect | ❌ 需 Org plan | 组件库到代码仓库的映射（可选，没有也能工作） |
| Editor 权限 | ⚠️ 当前 viewer | 写回 Figma 需要 editor 权限 |

---

## 三、推荐工作流

### 场景 A：新功能前端实现

```
设计师完成 Figma → 复制 Frame 链接 → 告诉 Jarvis/Claude Code
→ AI 读取设计 + 组件库 → 生成代码 → 开发者审查/微调
```

**人类需要做的**：提供 Figma Frame 链接 + 指定前端框架/组件库

### 场景 B：组件库覆盖度审查

```
Jarvis 扫描项目文件 → 对比组件库 → 输出未覆盖的组件清单
```

**人类需要做的**：提供项目文件链接

### 场景 C：快速原型

```
告诉 AI 功能需求 → AI 生成代码 → Send to Figma → 设计师审查
```

**人类需要做的**：描述需求，设计师在 Figma 中审查

---

## 四、局限性

1. **无法自动发现文件**：Figma API 不支持列出 workspace 所有文件（非 Enterprise 限制），新文件需手动告知
2. **Code Connect 需 Org plan**：组件库 ↔ 代码仓库的精确映射需要升级 Figma plan
3. **写回 Figma 需 Editor 权限**：当前账号是 viewer，需要文件所有者授予编辑权限才能使用 `use_figma` 写入
4. **图片/资源不支持写入**：MCP write 目前不能导入图片资源
5. **大文件可能超时**：超大设计文件的 API 请求需要分页处理

---

## 五、常见问题

**Q: 不升级 Org plan，AI 生成的代码质量如何？**
A: 仍然可用。AI 通过读取组件库的 published components 名称和结构来推断映射关系。Code Connect 只是让映射更精确，没有它也能工作。

**Q: 需要设计师改变工作习惯吗？**
A: 不需要。设计师正常在 Figma 中工作，只是多了一个"给 AI 提供 Frame 链接"的步骤。

**Q: 安全性如何？**
A: Figma Token 仅存在于 Jarvis 本地环境，不会外传。MCP OAuth 由 Figma 官方处理。设计文件数据不会离开 Figma 和 AI 的加密通道。
