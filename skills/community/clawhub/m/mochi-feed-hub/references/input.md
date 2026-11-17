# JSON actions

Actions add(url,id optional), feeds, poll(feedId optional), search(query optional,unread boolean,feedId optional,limit 1..1000), mark(ids,read default true), ack(noticeIds), import-file(feedId,file,notify default false), opml-import(file), opml-export(output optional). Feed body<=5MiB, parsed entries <=2000 per refresh. XML DTD/entities rejected. OPML import supports nested outline elements. State .mochilab/feed-hub; watch by host scheduling poll, then deliver returned notifications and ack successful noticeIds.
