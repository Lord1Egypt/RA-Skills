---
name: pptagent-collab
description: Use when working in the PPTAgent or BotSlide repository to add features, fix bugs, or adjust slide generation, editing, export, prompt rules, project versioning, or preview behavior. Especially useful for tasks involving 1280x720 slide constraints, deeppresenter prompt changes, HTML or PPTX export fidelity, frontend preview flows, and backend PPT project APIs.
---

# PPTAgent 协作 Skill

这个 skill 用于在 `PPTAgent / BotSlide` 仓库里做项目内协作，而不是泛化地“写 PPT”。

## 适用场景

- 修改 PPT 生成规则、页面布局、提示词或视觉约束
- 排查 HTML 预览和 PPTX 导出不一致
- 调整会话生成、PPT 项目版本、单页编辑或导出链路
- 修改前端预览、下载、分享、版本切换相关功能

## 触发关键词

当请求里出现下面这些方向时，应优先使用这个 skill：

- `PPTAgent`、`BotSlide`
- 幻灯片溢出、`1280x720`、固定画布、页高、版式锁定
- `deeppresenter`、`slide_design_prompt`
- `html -> pptx`、导出保真、样式丢失、字体丢失、分享页错位
- 单页编辑、版本快照、当前版本、项目列表、导出接口
- PPT 预览、下载、分享、右侧预览面板、会话生成

## 先判断任务落点

- 生成规则、页面溢出、视觉风格、图片禁用、尺寸锁定：
  先读 [references/slide-rules.md](references/slide-rules.md)
- 后端链路、版本管理、编辑保存、导出入口、前端挂载点：
  先读 [references/project-map.md](references/project-map.md)
- 需要跑命令、验证改动、补充 smoke test：
  先读 [references/validation.md](references/validation.md)

## 真相源优先级

当文档和代码不一致时，按下面优先级判断：

1. 运行时代码和当前 prompt
   - `backend/deeppresenter/prompts/slide_design_prompt.py`
   - `backend/services/chat_handler.py`
   - `backend/services/ppt_generator.py`
   - `backend/routers/ppt.py`
   - `backend/routers/export.py`
   - `export_tool/app/services/pptx_service.py`
2. 当前产品文档
   - `README_zh.md`
   - `README.md`
   - `export_tool/README.md`
3. 历史/说明性文档
   - `系统提示词.md`
   - `详细情况.md`
   - `API.md`

历史文档只作补充背景，不要在和代码冲突时把它们当成实现依据。

## 工作方式

1. 先定位用户要改的是哪一层：生成、编辑、预览、导出、版本管理，还是 UI 展示。
2. 不要只改第一个看见的文件；先顺着入口文件往调用链上下各看一层。
3. 只加载当前任务需要的 reference，保持上下文精简。
4. 如果任务涉及 slide HTML，默认保留固定画布思维，不要把页面当普通响应式网页处理。
5. 如果任务涉及导出保真，必须同时检查“生成的 HTML 假设”和“export_tool / dom-to-pptx 约束”。
6. 如果任务涉及版本或编辑行为，至少同时检查 router、service/chat_handler、crud 或 model 的对应路径。

## 常见任务速查

- 用户说“某页内容溢出、页面太长、生成页高度不对”：
  先看 `backend/deeppresenter/prompts/slide_design_prompt.py`，再看 [references/slide-rules.md](references/slide-rules.md)
- 用户说“预览正常，但导出 PPTX 样式错了”：
  先看 `backend/routers/export.py`、`export_tool/app/services/pptx_service.py`，再看 [references/validation.md](references/validation.md)
- 用户说“编辑某一页后版本不对、原始版本丢了”：
  先看 `backend/routers/ppt.py`、`backend/database/crud.py`、`backend/services/chat_handler.py`
- 用户说“首页/右侧预览/下载按钮行为有问题”：
  先看 `frontend/client/src/pages/Home.tsx`、`frontend/client/src/pages/PPTPlayer.tsx`、`frontend/client/src/hooks/useConversationManager.ts`
- 用户说“想改生成策略但文档互相打架”：
  先按“真相源优先级”回到运行时代码，不要先信历史文档

## 核心协作约束

- 这个项目的关键不是“生成漂亮 HTML”，而是“生成能被预览、编辑、分享、导出的稳定幻灯片 HTML”。
- 任何会影响页面结构的改动，都要优先保护 `1280x720` 画布约束和导出稳定性。
- 如果内容放不下，优先拆页、精简、改布局，不要通过把整页变高来解决。
- 当前代码里存在“旧规范文档”和“当前 prompt 实现”并存的情况；优先跟随当前代码。

## 输出要求

- 说明你改的是哪一层，以及为什么放在这一层改。
- 给出最小必要验证，而不是泛泛说“建议测试一下”。
- 如果没法完整验证，明确说明缺口，例如依赖未安装、外部服务未启动、只做了静态检查等。
