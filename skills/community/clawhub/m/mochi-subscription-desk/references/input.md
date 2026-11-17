# JSON actions

Actions put(subscription), list, remove(id), forecast(from,to), poll(date,advanceDays default7), ack(noticeIds). Subscription {id,title,start ISO date,amount decimal string,currency three-letter uppercase,unit:day|month|year defaultmonth,interval 1..120 default1,cancelLeadDays 0..365,end optional,enabled defaulttrue}. Amount <=1 billion and <=4 decimal places. Forecast horizon<=3660days, no FX conversion. poll dates and advanceDays are local-calendar dates (choose the schedule's timezone explicitly). .mochilab/subscription-desk stores plans and notices.
