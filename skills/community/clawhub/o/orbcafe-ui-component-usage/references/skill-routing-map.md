# Skill Routing Map

## Route by intent

- Build list/report page with filters/table/variant/layout:
  - `orbcafe-stdreport-workflow`
- Build chart dialog, detail page, or AI settings flow:
  - `orbcafe-graph-detail-ai`
- Build app shell/header/navigation/i18n/layout transitions:
  - `orbcafe-layout-navigation`
- Build pivot analytics or voice navigation:
  - `orbcafe-pivot-ainav`
- Build chat page, assistant panel, or floating copilot:
  - `orbcafe-agentui-chat`

## Route by keywords

- `报表`, `列表`, `筛选`, `分页`, `变体`, `layout`, `quickCreate`:
  - StdReport skill
- `图表`, `graph`, `kpi`, `详情页`, `detail`, `ai prompt`, `agent settings`:
  - Graph+Detail+Agent skill
- `导航`, `壳层`, `header`, `menu`, `locale`, `主题切换`, `markdown`, `transition`:
  - Layout+Navigation skill
- `透视表`, `pivot`, `拖拽维度`, `preset`, `语音导航`, `space 长按`:
  - Pivot+AINav skill
- `聊天`, `chat`, `copilot`, `assistant`, `streaming`, `卡片消息`, `AgentUI`, `StdChat`, `CopilotChat`, `AgentPanel`:
  - AgentUI Chat skill

## Cross-skill composition

- StdReport + GraphReport: choose StdReport as primary, then attach graph options.
- DetailInfo + CTable: choose Graph+Detail+Agent skill.
- App shell + any page module: apply Layout+Navigation skill first for frame, then attach module skill.
- AgentUI + app shell: apply Layout+Navigation skill first for frame, then attach AgentUI Chat skill.
