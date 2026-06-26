# 日历 API（Calendar）

## 快速调用

# 获取日历列表
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_calendars '{}'

# 创建日程
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_events '{"summary":"会议标题","start_time":"2026-03-28T10:00:00+08:00","end_time":"2026-03-28T11:00:00+08:00"}'

# 查询忙闲
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_freebusy_query '{"time_min":"2026-03-28T00:00:00+08:00","time_max":"2026-03-29T00:00:00+08:00","who":["ou_032ca29de8829b1a71272844465a4df3"]}'

## API 分类

calendar_v4_calendars - 获取日历列表
calendar_v4_events / events_list / events_update / events_delete - 日程 CRUD
calendar_v4_freebusy_query - 查询忙闲状态
calendar_v4_attendees_list / calendar_v4_attendees_create - 参与者管理
