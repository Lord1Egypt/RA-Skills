# JSON actions

Actions put(event), list, remove(id), upcoming(from YYYY-MM-DD,days 1..730), poll(now ISO offset timestamp optional,catchupHours 1..168), notifications, ack(noticeIds), import-holidays(file,advanceDays optional,time optional), export-ics(from,to,output optional). Event {id,title,month:1..12,day,calendar:gregorian|lunar,year optional,kind:birthday|anniversary|custom,timezone default Asia/Shanghai,time default 09:00,advanceDays default [7,1,0],feb29:feb28|mar1|skip,leapMonth boolean,leapPolicy:skip|regular,enabled boolean,onDate optional ISO date}. Use year for a birth/marriage year; onDate for a single occurrence. Holiday file {country,year,source:https URL,timezone,days:[{date,name,type:holiday|workday|observance}]}. Data stays in this agent's .mochilab/important-dates. A scheduler is needed for unattended notifications.

Lunar birthdays accept lunarShortMonth:lastday(default)|skip for years when the selected month has no day30.
