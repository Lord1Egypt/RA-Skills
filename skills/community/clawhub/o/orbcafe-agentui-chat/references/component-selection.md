# Component Selection

## Use `AgentPanel`

Choose `AgentPanel` when:
- 需要标准头部标题和描述
- 聊天区域是页面主体的一部分
- 不需要自定义 copilot 浮窗壳

## Use `StdChat`

Choose `StdChat` when:
- 已经有自己的页面容器或弹窗容器
- 只需要消息区 + 输入区
- 需要 streaming 和 card hooks，但不需要 copilot header/collapse 语义

## Use `CopilotChat`

Choose `CopilotChat` when:
- 要做右下角 copilot 或悬浮助手
- 需要带 header 的轻量面板内容
- 准备自己控制 open/close、position、drag、snap、resize

## Do not route here

- 报表、筛选、分页、variant：去 `orbcafe-stdreport-workflow`
- 页面壳层、导航、locale：去 `orbcafe-layout-navigation`
- 详情页、graph、agent settings：去 `orbcafe-graph-detail-ai`
- pivot / AINav 语音导航：去 `orbcafe-pivot-ainav`
