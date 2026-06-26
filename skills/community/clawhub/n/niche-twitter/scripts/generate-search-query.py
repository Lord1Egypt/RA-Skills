#!/usr/bin/env python3
import sys
import urllib.parse

if len(sys.argv) &lt; 2:
    print(&quot;Usage: python3 generate-search-query.py \&quot;[niche/topic]\&quot; [since] [verified]&quot;)
    sys.exit(1)

niche = sys.argv[1]
since = sys.argv[2] if len(sys.argv) &gt; 2 else &quot;2026-01-01&quot;
verified = &quot;filter:verified&quot; if len(sys.argv) &gt; 3 and sys.argv[3] == &quot;verified&quot; else &quot;&quot;

query = f&#39;&quot;{niche}&quot; OR #{niche.replace(&#39; &#39;, &#39;&#39;).lower()} {verified} min_faves:10 since:{since} lang:en&#39;

encoded = urllib.parse.quote(query)
url = f&quot;https://twitter.com/search?q={encoded}&amp;f=live&quot;
print(f&quot;Query: {query}&quot;)
print(f&quot;URL: {url}&quot;)
