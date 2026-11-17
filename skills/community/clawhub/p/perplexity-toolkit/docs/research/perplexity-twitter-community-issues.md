Tool budget exhausted (x_search was blocked by exhausted xAI credits; browser needed an unclicked Chrome permission; the write call didn't fit in budget), so the deliverable file could not be written by me. Below is the **complete, ready-to-save document** — persist it verbatim to `/tmp/perplexity-twitter-community-issues.md`.

**What I did:** 8 web searches + 4 targeted extracts covering community forum (Discourse HTML + categories.json), GitHub `perplexityai/api-discussion`, Reddit/BBB/Trustpilot aggregations, and media/legal coverage. X/Twitter direct search was attempted but the xAI credit pool was exhausted (permission-denied), so X discourse is evidenced via news roundups quoting X posts (Android Authority, PiunikaWeb, Android Headlines) rather than raw tweets.

---

# Perplexity AI — Known Problems, Complaints & Limitations (Inventory)

Compiled Aug 29, 2026. Sources: official Perplexity community forum (Discourse), GitHub api-discussion, Reddit r/perplexity_ai, BBB, Trustpilot, media/legal coverage. Ratings: Severity (High/Med/Low), Frequency (Frequent/Occasional/Rare) per available evidence.

## 1. Developer complaints — Perplexity API

| # | Problem | Severity | Frequency | Evidence |
|---|---|---|---|---|
| 1.1 | **429 rate limiting confusion** — leaky-bucket design, tier-based RPM (Tier 1 ~50 RPM; free tier 1 RPM); 429s hit valid accounts on bursts; devs must implement backoff+jitter; Retry-After often ignored | Med | Frequent | https://perplexityaimagazine.com/perplexity-hub/perplexity-api-error-429-fix ; https://theneuralbase.com/perplexity-api/learn/intermediate/requests-per-minute |
| 1.2 | **Billing surprises: two-layer pricing** — per-token + per-request fees (Sonar ~$5/1K requests) silently double bills; no per-request cost breakdown in response headers; "misleading pricing" threads | High | Frequent | https://www.cloudzero.com/blog/perplexity-api-pricing/ ; https://nolist.ai/item/perplexity-pplx-api |
| 1.3 | **Credits balance stuck at $0 after purchase**; "API/Billing Major Problem!" thread | High | Occasional | https://community.perplexity.ai/t/perplexity-api-purchased-credits-balance-still-shows-0/3185 ; https://community.perplexity.ai/t/api-billing-major-problem/3915 |
| 1.4 | **API results noticeably worse than web UI for same query** (consistent, multiple reports) | High | Frequent | https://community.perplexity.ai/t/m-running-into-a-consistent-issue-with-perplexity-where-the-api-results-are-noticeably-worse-than-the-web-ui-even-when-i-use-the-same-query/3553 ; https://github.com/perplexityai/api-discussion/issues/323 |
| 1.5 | **General API search degradation** — "quality of responses, particularly the search system, has degraded severely" | High | Reported | https://github.com/perplexityai/api-discussion/issues/93 |
| 1.6 | **Deep Research API unreliability** — ~50% success rate on output formatting; responses cut off with finish_reason "stop"; timeouts stuck IN_PROGRESS; streaming unsupported | High | Frequent | https://community.perplexity.ai/t/deep-research-api-inconsistent-output-formatting-50-success-rate/2469 ; https://community.perplexity.ai/t/deep-research-api-response-content-is-cut-off-unexpectedly-while-having-finish-reason-stop/468 (13 replies, 787 views) ; https://community.perplexity.ai/t/the-perplexity-sonar-deep-research-model-is-repeatedly-staying-in-in-progress-and-timing-out/3663 ; https://github.com/perplexityai/api-discussion/issues/322 |
| 1.7 | **Structured output not structured**; reasoning models return thinking text that breaks JSON parsing (Vercel AI gateway) | High | Frequent | https://community.perplexity.ai/t/structured-output-is-not-structured/485 ; https://github.com/vercel/ai/issues/11489 |
| 1.8 | **Model mismatch bugs** — sonar-deep-research returns sonar-reasoning-pro; wrong model label in dashboard; charged citation_tokens | Med | Occasional | https://github.com/perplexityai/api-discussion/issues/318 ; #320 ; #319 |
| 1.9 | **search_domain_filter ignored** → hallucinated/broken links; URLs with reserved chars error; empty search_results object | High | Occasional | https://github.com/perplexityai/api-discussion/issues/312 ; https://community.perplexity.ai/t/urls-with-reserved-characters-throws-error-in-search-domain-filter/3498 ; https://community.perplexity.ai/t/api-returning-empty-search-results-object/ (9 replies, 810 views) |
| 1.10 | **Async endpoints broken** — GET /v1/async/sonar/{id} returns list of all requests; unable to retrieve async deep research result | Med | Occasional | https://community.perplexity.ai/t/get-v1-async-sonar-api-request-returns-the-list-of-all-requests-instead-of-single-request-data/ ; https://community.perplexity.ai/t/unable-to-retrieve-the-result-of-an-async-deep-research/ |
| 1.11 | **Docs/SDK mismatch** — "Search API implementation and SDKs do not match API docs and SDK docs"; "Python API examples not correct" | Med | Frequent | https://community.perplexity.ai/t/search-api-implementation-and-sdks-do-not-match-api-docs-and-sdk-docs/1616 ; https://community.perplexity.ai/t/python-api-examples-not-correct/ |
| 1.12 | **Missing features (top-voted)** — no endpoint for total API cost (675 views); no balance endpoint; no conversation-history API; no monthly spending limit; no BYOK; LinkedIn URLs returned by UI but not API; location filter "borderline useless" | Med | N/A (gaps) | https://community.perplexity.ai/t/how-to-get-total-api-cost/ ; https://github.com/perplexityai/api-discussion/issues/327 ; https://community.perplexity.ai/t/i-would-like-an-api-to-retrieve-conversation-history/ ; https://community.perplexity.ai/t/why-can-perplexity-s-api-not-return-linkedin-urls-while-the-interface-can/ ; https://community.perplexity.ai/t/location-filter-is-borderline-useless-in-the-api/566 |
| 1.13 | **401 Authorization Required responses** (4 replies, 656 views); strict prepaid: $0 balance kills active streams even for Pro subscribers | High | Occasional | https://community.perplexity.ai/t/401-authorization-required-response-in-api/ ; https://nolist.ai/item/perplexity-pplx-api |
| 1.14 | **Embeddings rate-limit bug** — x-ratelimit-limit meters input texts, not requests; documented 512-text batch unreachable at Tier 1 | Med | New (Aug 2026) | https://community.perplexity.ai/t/standard-embeddings-x-ratelimit-limit-meters-input-texts-not-requests-documented-512-text-batch-unreachable-at-tier-1/5914 |

## 2. Power-user complaints — search quality degradation (X/Reddit)

| # | Problem | Severity | Frequency | Evidence |
|---|---|---|---|---|
| 2.1 | **Silent model downgrade ("routing scandal", Nov 2025)** — Claude/GPT-labeled answers served by cheaper models; CEO called it "an engineering bug"; top Reddit thread 1,242 pts; spawned open-source "Perplexity Model Watcher" | High | One-off (major) | https://www.reddit.com/r/perplexity_ai/comments/1opaiam/ ; https://www.reddit.com/r/perplexity_ai/comments/1orar1a/ ; https://www.makeuseof.com/perplexity-is-giving-you-wrong-answers-on-purpose/ |
| 2.2 | **Answers "stripped away"/shorter** — "Perplexity has gotten lazy with its answers/responses" (u/ASuperMarioFan1993OC, Aug 26) | Med | Frequent (2026) | https://theaidownside.com/posts/voices-gotten-lazy-ai-doing-less.html |
| 2.3 | **Overall quality plunge** — "answer quality has plunged in the past couple months" (product comparisons) | Med | Frequent | https://www.redditmedia.com/r/perplexity_ai/comments/1g2rthy/perplexity_answer_quality_has_plunged_recently/ |
| 2.4 | **Deep Research is shallow** — confident output built on snippet summaries without reading sources; ~600 runs/day cut to ~20/month with no notice ("99.89% Reduction in Research quota overnight") | High | Frequent (2026) | https://www.reddit.com/r/perplexity_ai/comments/1qwhej3/ ; https://www.bbb.org/us/ca/san-francisco/profile/artificial-intelligence/perplexity-ai-1116-960131/complaints |
| 2.5 | **Hallucinated/misattributed citations** — recurring; "Incorrect Citation Mapping in Pro Search API" | High | Frequent | https://community.perplexity.ai/t/bug-report-incorrect-citation-mapping-in-pro-search-api-responses/3112 ; https://nwilhelm.io/the-beginning-of-the-end-for-perplexity |
| 2.6 | **Quiet Pro quota cuts (May 2026)** — weekly searches halved 200→100, mid-term on prepaid annual plans; X + Reddit complaints; Android Authority confirmed; charged-back by users | High | Widespread | https://piunikaweb.com/2026/05/15/perplexity-rate-limit-reduce-pro/ ; https://www.androidauthority.com/perplexity-pro-advanced-ai-limits-reduced-3667942/ ; https://www.androidheadlines.com/2026/05/perplexity-pro-users-complain-quiet-advanced-model-limits-cut.html ; https://www.reddit.com/r/perplexity_ai/comments/1tcvvbx/ |
| 2.7 | **"Perplexity AI is a scam"** (154 pts, Feb 2026) — bait-and-switch after renewal; BBB "bait and switch" complaints | High | Growing | https://reddit.com/r/perplexity_ai/comments/1r12ujt/perplexity_ai_is_a_scam/ ; BBB complaints page (billing 10, product 19, service 11) |

## 3. Official community forum & GitHub — top bug reports / feature requests

- Forum scale: Bug Reports 180 topics/453 posts; Feature Requests 95 topics (community.perplexity.ai/categories.json).
- **Top-viewed bugs:** "API Returning empty search_results" (810 views) • "401 Authorization Required" (656) • "Structured output is not structured" (485) • "Mac app 26.24.0 — all MCP tools broken and irrecoverable in Spaces" (11 replies, 507) • "Connector stays checked but never attached to composer" (9 replies, 169) • "Custom MCP connector fails 'did not return a client_secret' (RFC 7591)" (356) • "Performance and reliability issues with Agent API" (196).
- **Top feature requests:** Branching/Forking Conversations (1,139 views) • Patent search via API (1,154) • How to get total API cost (675) • API for Max token balance/history • Programmatic "Export my data" • Monthly Spending Limit (136) • BYOK (186) • Conversation history API (411) • Landscape mode • Family Plan • Voice assistant in Spaces • Rename threads • Model Council in API • Perplexity History management in Comet (120).
- **GitHub perplexityai/api-discussion open bugs:** #324 can't get deep search results; #321 deep research timing out; #320 wrong model label; #319 charged citation_tokens; #318 model mismatch; #312 domain filter ignored + hallucinated links; #93 API search degraded severely. Source: https://github.com/perplexityai/api-discussion/issues

## 4. Journalist/media criticism & publisher conflict

| # | Problem | Severity | Evidence |
|---|---|---|---|
| 4.1 | **Plagiarism accusations** — Wired: Perplexity reproduced its expose nearly verbatim (287-word summary, exact sentence match; Poynter 7-word test); Forbes: AI-drones scoop republished without credit; editor posted accusation on X | High | https://techcrunch.com/2024/07/02/news-outlets-are-accusing-perplexity-of-plagiarism-and-unethical-web-scraping ; https://www.techbloat.com/perplexity-ai-pages-face-plagiarism-allegations-from-major-news-outlets.html |
| 4.2 | **Robots.txt evasion / unethical scraping** — Wired investigation via AWS IPs; Reddit "trap" post visible to Google crawler surfaced in Perplexity within hours | High | https://searchengineland.com/reddit-sues-perplexity-serpapi-scraping-google-463681 ; https://www.theverge.com/24187792/perplexity-ai-news-updates |
| 4.3 | **Lawsuits** — NYT (SDNY, Dec 5 2025); Dow Jones/NY Post (motion to dismiss denied in full); CNN (~17,000 works); Reddit + Oxylabs/AWMProxy/SerpApi (Feb 9 2026); Amazon (preliminary injunction won); Britannica; Nikkei & Asahi Shimbun ($44M, Japan) | High (existential for citation corpus) | https://www.courthousenews.com/wp-content/uploads/2025/12/new-york-times-perplexity-ai.pdf ; https://www.susmangodfrey.com/wp-content/uploads/2025/09/Britannica-v.-Perplexity-Complaint.pdf ; https://www.lawfuel.com/japans-biggest-publishers-just-sued-perplexity-ai-for-44m/ |
| 4.4 | **CEO response controversy** — refused to define plagiarism; said publishers wish the tech "didn't exist"; paywall-circumvention dispute | Med | https://www.justthink.ai/blog/perplexity-ceo-plagiarism-controversy-analysis |
| 4.5 | **Perplexity Pages** — generates polished articles from publishers' reporting, reducing click-through; substitution concern | Med | https://winbuzzer.com/2024/06/08/perplexity-ai-faces-plagiarism-allegations-from-major-news-outlets-xcxwbn/ |

## 5. Privacy & data-handling concerns

| # | Problem | Severity | Evidence |
|---|---|---|---|
| 5.1 | **Class action (Mar 31, 2026)** — Meta Pixel, Google Ads, DoubleClick, Conversions API allegedly shared prompts/responses/email/IP/device IDs with Meta & Google, **including in "Incognito" mode** ("sham" incognito); voluntarily dismissed May 2026, claims unresolved | High | https://kaizenailab.com/blog/perplexity-class-action-user-data-meta-google-2026 ; https://selina.ai/blog/perplexity-ai-privacy-policy |
| 5.2 | **Consumer data used for training by default** — opt-out, not opt-in; queries/responses/uploads collected; deleted convos retained 30 days; unclear retention post-opt-out; no DPA for consumer tier; German analysis: no GDPR-compliant consent | High | https://anonyome.com/knowledge-center/ai-privacy/perplexity-ai-data-privacy/ ; https://joselugo.de/blog/en/perplexity-privacy-risk |
| 5.3 | **GDPR data requests stall** — BBB: GDPR request unanswered for over a month | Med | https://www.bbb.org/us/ca/san-francisco/profile/artificial-intelligence/perplexity-ai-1116-960131/complaints |
| 5.4 | **Comet browser privacy/security** — Trustpilot 2.1/5; assistant prompt-injection hijack (Brave disclosure Aug 2025, new vuln Mar 2026); EFF memory concerns (retains sensitive info in incognito); weak phishing blocking | High | https://www.trustpilot.com/review/comet.perplexity.ai ; https://briefia.fr/en/article/perplexity-et-openai-l-echec-des-navigateurs-ia |
| 5.5 | **Enterprise-only protections** — no-training guarantee contractual only; downgrade to consumer plan loses it | Med | https://selina.ai/blog/perplexity-ai-privacy-policy |

## 6. Enterprise / team plan limitations

| # | Problem | Severity | Evidence |
|---|---|---|---|
| 6.1 | **Governance features gated** — SCIM, audit logs, insight dashboards, custom data retention only with **50+ members or one Enterprise Max seat ($325/mo)**; small teams forced to buy Max | High | https://saaszap.com/perplexity-ai-pricing ; https://perplexityaimagazine.com/perplexity-hub/perplexity-enterprise-pricing-pro-max |
| 6.2 | **Rigid data retention** — default 90 days; 30-day change took a week of support emails (regulated biotech) | Med | https://enterprisedna.co/resources/blog/practitioner-perplexity-enterprise |
| 6.3 | **No SSO on base tier; thin admin controls**; no data-residency guarantees | Med | https://shiporskip.io/tool/perplexity-for-teams-shared-spaces-admin-controls |
| 6.4 | **Enterprise plans exclude API access** — API billed separately; internal knowledge search capped at 500 files on Enterprise Pro; audit logs don't record answers or Slack docs accessed | Med | https://perplexity.ai/help-center/en/articles/10352986-enterprise-pricing-and-billing-frequently-asked-questions ; https://www.perplexity.ai/help-center/en/articles/12167980-using-the-connector-for-slack |
| 6.5 | **Reliability complaints**; custom connectors blocked by org-level admin gate (unique among clients) | Med | https://enterprisedna.co/resources/blog/practitioner-perplexity-enterprise ; https://www.blotato.com/ai-agent/perplexity |

## 7. Mobile app vs web discrepancies

| # | Problem | Severity | Evidence |
|---|---|---|---|
| 7.1 | **API/web quality gap** — same query: API output worse than web UI (see 1.4) | High | community #3553 ; GitHub #323 |
| 7.2 | **iOS app failures** — crashes, stalls, "Something went wrong"; Cloudflare blocks when VPN active; iOS 17+ requirement; voice-mode mic/session failures | Med | https://perplexityaimagazine.com/perplexity-hub/perplexity-ios-app-issues-fixes ; https://perplexityaimagazine.com/perplexity-hub/perplexity-voice-mode-not-working-fixes |
| 7.3 | **Comet mobile UX gaps** — new-tab always opens assistant (no customization); bottom navbar; no tab gestures; no inactive-tab auto-close; iPad layout issues; context loss; crashes when clearing data (fixed May 2026) | Med | https://findskill.ai/blog/perplexity-comet-ios-review ; https://webpronews.com/perplexitys-comet-ios-update-delivers-eight-practical-fixes-that-make-ai-browsing-feel-less-broken |
| 7.4 | **Comet desktop/mobile parity** — imports only one Chrome profile; agent actions slower/less reliable on mobile; direct answers hallucinate (timezone conversion) | Med | https://sidsaladi.substack.com/p/perplexity-comet-ai-browser-101-complete ; https://medium.com/@dev.yashmathur/i-used-perplexity-comet-as-my-default-mobile-browser-for-1-month-so-you-dont-have-to-71c196b6fe50 |
| 7.5 | **Mac app MCP tools broken** in Spaces, irrecoverable | High | https://community.perplexity.ai/t/mac-app-26-24-0-28-all-mcp-tools-broken-and-irrecoverable-in-spaces/5397 |

## 8. Plugin / integration limitations

| # | Problem | Severity | Evidence |
|---|---|---|---|
| 8.1 | **MCP connector bugs** — connector "checked" but never attached (any machine); RFC 7591 public-client registration fails; ~2-min hang + STREAM_FAILED_PLACEHOLDER_ERROR + CORS failure (JP region); WordPress MCP lockout | High | community: https://community.perplexity.ai/t/connector-stays-checked-in-the-dropdown-but-is-never-attached-to-the-composer-tool-never-dispatches-fresh-sessions-any-machine/ ; https://community.perplexity.ai/t/custom-mcp-connector-fails-with-did-not-return-a-client-secret-for-rfc-7591-compliant-public-client-registrations/ ; https://community.perplexity.ai/t/need-help-connected-mcp-thing-to-my-wordpress-site-and-now-i-cant-even-log-into-my-own-dashboard/5808 |
| 8.2 | **Slack connector audit gap** — answers and Slack docs accessed not tracked in audit logs; Slack app requires paid Slack plan; admin can silently disable | Med | https://www.perplexity.ai/help-center/en/articles/12167980-using-the-connector-for-slack |
| 8.3 | **Agent API gaps** — finance_search tool broken; skills added July 2026 but no programmatic thread management; performance/reliability issues | Med | https://community.perplexity.ai/t/finance-search-tool-doesnt-work-agent-api/5906 ; https://community.perplexity.ai/t/performance-and-reliability-issues-with-agent-api/ |
| 8.4 | **Third-party gateway incompatibility** — Vercel AI SDK: Perplexity reasoning models return thinking text that breaks JSON object parsing (closed as completed, July 2026) | Med | https://github.com/vercel/ai/issues/11489 |
| 8.5 | **Third-party clients break** — Typing Mind connection issue; "I cannot perform live web searches in real-time"; SDK/docs mismatch (see 1.11) | Med | https://community.perplexity.ai/t/typing-mind-connection-issue/3944 ; https://community.perplexity.ai/t/i-cannot-perform-live-web-searches-in-real-time/ |
| 8.6 | **No dedicated browser extension** — Comet browser is the substitute; extension-era workflows lost; Comet itself carries the security/prompt-injection baggage (see 5.4) | Med | https://briefia.fr/en/article/perplexity-et-openai-l-echec-des-navigateurs-ia |

## Methodology notes / gaps
- **X/Twitter direct search blocked** — xAI API credit pool exhausted (permission-denied error). X evidence is via secondary roundups (Android Authority, PiunikaWeb, Android Headlines quoting X posts) — all cited above.
- Community view counts are Discourse stats captured Aug 29, 2026.
- Severity = impact on users; Frequency = how often reported across independent sources, not measured prevalence.

**Issues encountered:** (1) x_search tool unusable (xAI credits exhausted — parent should retry later or use alternative X indexing); (2) one web_search batch hit Tavily paywall and had to be re-run on keyless fallback; (3) browser_exec blocked on Chrome "Allow remote debugging" popup requiring user click; (4) tool-iteration cap hit before I could write the file — the document above is the complete deliverable content, ready to save to `/tmp/perplexity-twitter-community-issues.md`.