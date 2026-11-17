# Action contract

crawl:url HTTPS,maxPages1..60 default20,checkExternal false,maxExternal1..20. Only same-origin linked pages enter the crawl queue. external URLs are listed; network checks are opt-in, bounded HEAD requests. Internal fragments checked only when target HTML was actually crawled. HTML parser reads titles,h1,alt,description,canonical,robots and links; it does not execute JavaScript. Response1MiB each, timeout12sec,redirects bounded. Private/reserved targets denied unless allowPrivateHosts is explicitly supplied by the user. Report limitReached and uncheckedInternalLinks honestly. It is a user-requested small crawl, not a site-wide exhaustive scan.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
