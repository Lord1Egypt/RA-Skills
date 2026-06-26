# 项目地图

## 1. 生成链路

- `backend/services/chat_handler.py`
  处理会话、流式生成、主题继承、编辑指令和版本同步，是用户请求进入 PPT 流程后的主干。
- `backend/services/ppt_generator.py`
  负责页数解析、工具消息整理、运行 slide design / edit agent。
- `backend/deeppresenter/prompts/slide_design_prompt.py`
  当前最重要的生成约束来源，定义了固定尺寸、布局模型、字体/配色、图表和图片使用规则。
- `backend/deeppresenter/main.py`
  将 markdown / agent 结果转成 slide HTML，再调用 html2pptx 生成最终文件。

## 2. 版本与编辑链路

- `backend/routers/ppt.py`
  项目、版本、单页编辑 API 入口。首次编辑会自动创建原始子版本快照。
- `backend/database/crud.py`
  版本、项目、slide 的读写逻辑在这里落库。
- `backend/routers/conversations.py`
  会话维度和 PPT 项目数据之间有同步逻辑，改版本展示或当前版本选择时要一起看。

## 3. 导出与分享链路

- `backend/routers/export.py`
  导出、分享、文件名处理、分享页 HTML 规范化入口。
- `backend/services/export_client.py`
  后端调用 `export_tool` 的客户端。
- `export_tool/app/services/pptx_service.py`
  HTML -> PPTX 的关键实现。会处理 Google Fonts、Playwright 页面注入和 `dom-to-pptx` bundle 加载。
- `export_tool/dom-to-pptx/`
  真正的转换库源码和构建产物位置。bundle 缺失时通常要来这里排查。

## 4. 前端主要挂载点

- `frontend/client/src/pages/Home.tsx`
  首页和会话主流程的重要页面。
- `frontend/client/src/pages/PPTPlayer.tsx`
  播放 / 查看某个 PPT 项目和版本时的重要入口。
- `frontend/client/src/hooks/useConversationManager.ts`
  会话、项目、版本、slide 数据拼装的关键 hook。
- `frontend/client/src/components/RightPanel/`
  大纲、预览、任务计划、搜索等右侧面板能力集中在这里。
- `frontend/client/src/components/DownloadModal.tsx`
  导出交互入口之一，改导出参数或流程时通常要一起看。

## 5. 当前项目特征

- 这是“AI 生成 + 在线预览编辑 + 多格式导出”的整链路项目，不是只生成静态 HTML。
- 运行时对 slide 尺寸约束非常敏感，视觉改动可能同时影响预览、分享和导出。
- 当前 `chat_handler.py` 里存在 `_strip_images_from_html`，说明运行策略对图片资源较保守；改图片能力时要确认是否和现有约束冲突。
- `backend/routers/export.py` 会给分享页注入统一字体和 `1280x720` 渲染基线，浏览器侧“看起来正常”不代表导出侧也正常。

