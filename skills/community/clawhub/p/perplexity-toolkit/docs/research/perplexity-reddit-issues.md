I've hit the tool-call cap. I gathered 297 unique Reddit thread URLs across 50 search queries and extracted full content from 6 key threads. The file write to `/tmp/perplexity-reddit-issues.md` could not be executed — the complete document is below, ready to save verbatim.

# Perplexity AI — Known Problems & Complaints from Reddit (Research Inventory)

**Method:** 50 site-restricted search queries across r/perplexity_ai, r/Perplexity, r/AIDangers, r/artificial, r/ChatGPTPro, r/LocalLLaMA, r/singularity, r/technology, r/webdev. 297 unique thread URLs collected; 6 threads fully extracted (web_extract). **Note:** Reddit's JSON API and old.reddit mirrors are blocked from this network — only direct www.reddit.com extraction worked. Severity/frequency are inferred from thread volume + extracted content; "extracted" = full post text read, "title-only" = corroborated by headline only.

---

## 1. SEARCH QUALITY ISSUES (hallucinations, wrong sources, outdated info) — HIGHEST COMPLAINT DENSITY

### 1.1 Fabricated answers with no basis — CRITICAL, very frequent
- "Perplexity is constantly lying" — user reports ~80% of answers claim info that "didn't exist anywhere"; cited links led to 404s or pages with no matching content; when challenged, Perplexity apologized and admitted being wrong. [extracted](https://www.reddit.com/r/perplexity_ai/comments/1p76syf/perplexity_is_constantly_lying/)
- "Perplexity AI lies and fabricate false answers" [title-only](https://www.reddit.com/r/Perplexity/comments/1qiv7gp/perplexity_ai_lies_and_fabricate_false_answers/)
- "Perplexity is consistently wrong" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qolpfs/perplexity_is_consistently_wrong)
- "WTF happened to Perplexity?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1hy7oj0/wtf_happened_to_perplexity/)
- "Is perplexity shutting off or pivoting? … labs are giving wrong answer, peak hallucinations ever seen" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1p6dox1/is_perplexity_shutting_off_or_pivoting_because/)

### 1.2 Wrong answers even with sources; self-correction only after user challenges — MAJOR, frequent
- "Pro user — most answers are wrong": user gets wrong answers on basic + research queries; after asking it to double-check, Perplexity admits error and gives right answer; user questions trusting it at all and considers switching to Anthropic/OpenAI/xAI directly. [extracted](https://www.reddit.com/r/perplexity_ai/comments/1orgbzq/pro_user_most_answer_are_wrong/)
- "I am really getting tired of Perplexity getting it wrong and correcting itself after I spot an error": Labs mode produces fabricated graphs ("synthetic data" instead of real measurements) and source-attributed info that is still wrong; error rate has *increased* in recent months. [extracted](https://www.reddit.com/r/perplexity_ai/comments/1ncabcz/i_am_really_getting_tired_of_perplexity_getting/)
- "I'm finding perplexity is giving me alot of incorrect [answers]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1u6i4pz/im_finding_perplexity_is_giving_me_alot_of)
- "Has perplexity response accuracy significantly reduced recently?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nojir4/has_perplexity_response_accuracy_significantly)
- "Has Perplexity Pro quality seriously taken a nose dive!" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1fvl54y/quality_of_perplexity_pro_has_seriously_taken_a)
- "Is Perplexity declining?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1tirzww/is_perplexity_declining/)
- "Is perplexity getting worse" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1gaw6tm/is_perplexity_getting_worse/)
- "Perplexity Explains Why It Gives Me Wrong Answers" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pvn5kn/perplexity_explains_why_it_gives_me_wrong_answers/)
- "Why does Perplexity fail so much?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1cgn3dg/why_does_perplexity_fail_so_much/)

### 1.3 Fabricated citations / wrong references — MAJOR, very frequent
- "Perplexity Gives Wrong Citation/Link Most the Time" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1j1gke5/perplexity_gives_wrong_citationlink_most_the_time)
- "References incorrect" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1dh3es0/references_incorrect)
- "Citations are wrong" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1fyhctp/citations_are_wrong/)
- "Incorrect Citations" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1chmjne/incorrect_citations/)
- "A Global Debug Card I use for Perplexity-style citation, retrieval, and research failures" [title-only](https://www.reddit.com/r/Perplexity/comments/1rn1uh6/a_global_debug_card_i_use_for_perplexitystyle.json)

### 1.4 Fabricated content in a factual-adjacent domain (medical) — CRITICAL safety issue, once documented prominently
- r/AIDangers: Perplexity fabricated doctor reviews (fake 5-star ratings, quotes that don't exist in any cited source) about a real doctor; also cites third-party findings — a 2025 academic study found Perplexity fabricated 72% of references checked (~3 errors/citation, worst of tested chatbots except Copilot); GPTZero found AI-generated/fabricated sources within 3 searches; Dow Jones & NY Post suing over fabricated/falsely-attributed news. [extracted](https://www.reddit.com/r/AIDangers/comments/1o857ih/perplexity_is_fabricating_medical_reviews_and/)
- "Which AI lies the most? I tested GPT, Perplexity, Claude..." [title-only](https://www.reddit.com/r/learnmachinelearning/comments/1p7f2g6/which_ai_lies_the_most_i_tested_gpt_perplexity/)

### 1.5 Outdated info / wrong date filtering — MINOR→MAJOR, recurring
- "Date of news are not what I ask for" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nhthcm/date_of_news_are_not_what_i_ask_for.json)
- "Perplexity heavily shapes its answers on sources on the [basis of training data bias]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1py3c3a/perplexity_heavily_shapes_its_answers_on_sources)

---

## 2. PRO/SUBSCRIPTION COMPLAINTS — HIGHEST VOLUME, MANY "SCAM" POSTS

### 2.1 Auto-renewal charges + AI-bot refund wall — CRITICAL, frequent
- "Perplexity just stole $200 from me and their AI support bot is literally refusing to let me talk to a human": $200 annual auto-renewal fired after a free-promo year; AI bot "Sam" refused refund (missed 72-hr window), refused human escalation ("cannot be overridden by any team member"), and leaked regional refund policy (EU/UK/Turkey 14 days, SK/Brazil 7 days, everyone else 72 hours). Thread commenters split; some defend auto-renew as standard, others flag AI-only support as unacceptable. [extracted](https://www.reddit.com/r/perplexity_ai/comments/1sv2tq1/perplexity_just_stole_200_from_me_and_their_ai/)
- "Perplexity Pro double billing complaint" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1srx59t/perplexity_pro_double_billing_complaint)
- "Getting refund for double billing" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qkhyme/getting_refund_for_double_billing)

### 2.2 Sudden downgrades / revoked paid status — CRITICAL, frequent
- "Frustrated with Perplexity cancelling my PAID Pro [subscription]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1rq4i0n/frustrated_with_perplexity_cancelling_my_paid_pro)
- "My 1 year Pro account was suddenly downgraded!" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1rpgny9/my_1_year_pro_account_was_suddenly_downgraded)
- "Suspended Pro Subscription" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r9d2ha/suspended_pro_subscription)
- "Perplexity Pro account Suspended" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1t2xity/perplexity_pro_account_suspended)
- "Perplexity suspended my Pro account with zero explanation" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1s50boc/perplexity_suspended_my_pro_account_with_zero)
- "Perplexity suspended my free 1-year Pro plan citing TOS" [title-only](https://www.reddit.com/r/Perplexity/comments/1sqwbuj/perplexity_suspended_my_free_1year_pro_plan)
- "I got downgraded to free, even I referred 5 people last months" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1dabcrs/i_got_downgraded_to_free_even_i_reffered_5_people)
- "Signed Up for Pro but Eliot Cancelled My Pro Sub" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1cnimf5/signed_up_for_pro_but_eliot_cancelled_my_pro_sub)
- "Steps to take if you are affected by the PRO cancellation as EU user" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r9y82u/steps_to_take_if_you_are_affected_by_the_pro)

### 2.3 Bans / account suspensions tied to user behavior — MAJOR, recurring
- "Perplexity Pro users are being banned because they broke rules" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qv80pz/the_perplexity_pro_users_are_being_banned_because)
- "Banned from Perplexity after helping them grow" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1ou1qez/banned_from_perplexity_after_helping_them_grow)
- "Perplexity banned me from their Discord, Reddit, and will..." [title-only](https://www.reddit.com/r/Perplexity/comments/1r7mhm7/perplexity_banned_me_rfrom_their_discord_reddit)

### 2.4 Feature gating / silent limits / model switches — MAJOR, very frequent
- "Perplexity lowered Labs queries from 50 to 25 for Pro subscribers" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qjr1xx/perplexity_lowered_labs_queries_from_50_to_25_for)
- "Did Perplexity reduce the pro searches?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r5g6t7/did_perplexity_reduce_the_pro_searches)
- "Notes on the new limits for Perplexity Pro" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r1xg6i/notes_on_the_new_limits_for_perplexity_pro)
- "Perplexity Pro is silently switching models mid-conversation" [title-only](https://www.reddit.com/r/Perplexity/comments/1rxbhro/perplexity_pro_is_silently_switching_models)
- "Perplexity keeps switching Claude Sonnet 4.6 Thinking to [a cheaper model]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1tnjpui/perplexity_keeps_switching_claude_sonnet_46)
- "Perplexity Pro on Android: Chosen model automatically [reverts]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m0ccqt/perplexity_pro_on_android_chosen_model)
- "Perplexity automatically switches to learning mode" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1p75260/perplexity_automatically_switches_to_learning_mode)
- "Is Perplexity lying about what models you can use?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1lziyvt/is_perplexity_lying_about_what_models_you_can_use)
- "Listen carefully: NO I don't want to help you improve your model… NO I don't want you to always select the best model for me!" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nwcs54/listen_carefully_no_i_dont_want_to_help_you)
- "Are you seriously all ok with the way perplexity treat [customers]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1oyvdcw/are_you_seriously_all_ok_with_the_way_perplexity)
- "Perplexity is STILL DELIBERATELY SCAMMING AND [degrades service]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pjmkmj/perplexity_is_still_deliberately_scamming_and)
- "Perplexity AI is a scam" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r12ujt/perplexity_ai_is_a_scam)
- "What the, the pro plan has much lower weekly limits now?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pje7re/what_the_the_pro_plan_has_much_lower_weekly)
- "Some of the math behind the enshittification of your $20 Perplexity Pro plan" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1riesnr/some_of_the_math_behind_the_enshittification_of)

### 2.5 Refund/cancellation difficulties — MAJOR, recurring
- "Hard reminder to never sign up for an annual plan" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1otqb2h/hard_reminder_to_never_sign_up_for_an_annual_plan)
- "I asked Perplexity to refund my annual membership fee proportionally… These are the answers" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qytcst/i_asked_perplexity_to_refund_my_annual_membership)
- "Perplexity subscription cancellation and consequences" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1t4a26l/perplexity_subscription_cancellation_and)
- "I 'was' canceled my yearly pro subscription and…" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1fy7vyo/i_was_canceled_my_yearly_pro_subscription_and)
- "Perplexity Customer Support Review" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pol3yb/perplexity_customer_support_review)
- "Best way to contact support?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nenmo4/best_way_to_contact_support)

### 2.6 Max tier / value complaints — MAJOR, growing
- "I upgraded to Max… I regret it" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1uwibta/i_upgraded_to_maxi_regret_it)
- "Why is everyone saying perplexity is dead? Paying $20 for over a year" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r00vpi/why_is_everyone_saying_perplexity_is_dead_paying)
- "I feel like Perplexity Pro just isn't worth it anymore" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1t2koa5/i_feel_like_perplexity_pro_just_isnt_worth_it)
- "I'M NOT BUYING MAX, PLEASE UNDERSTAND THIS" [title-only](https://reddit.com/r/perplexity_ai/comments/1rfsupq/im_not_buying_max_please_understand_this)
- "Perplexity Pro is a Scam and Officially Obsolete: Why I'm Canceling after 1 Year" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qjxbmb/perplexity_pro_is_a_scam_and_officially_obsolete/) *(also used as a live example — the "Perplexity explained why they switched" drama thread)* [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jhciwr/perplexity_replies_to_why_they_switched_follow_up)
- "Today I canceled perplexity plus" [title-only](https://www.reddit.com/r/perplexity_ai/comments/17sex0n/today_i_canceled_perplexity_plus/)
- "I asked Perplexity to tell me how Perplexity cheated us and here is what I got" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1kbe9hv/i_asked_perplexity_to_tell_me_how_perplexity/)

---

## 3. API LIMITATIONS

### 3.1 API pricing complaints — MAJOR, recurring
- "Ridiculous API cost of Perplexity AI" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jbky3f/ridiculous_api_cost_of_perplexity_ai)
- "$5 monthly API credits for Pro users discontinued" (confirmed) [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r4cztm/confirmed_5_monthly_api_credits_for_pro_users)
- "Did Perplexity remove the $5 API credit that comes with the $20 subscription?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1rbcu0m/did_perplexity_remove_the_5_api_credit_that_comes)

### 3.2 Poor model quality through API — MAJOR, recurring
- "Is it just me, or are Perplexity's API models… bad?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m4kddv/is_it_just_me_or_do_perplexitys_api_models_are_bad)
- "Is SONAR bad?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1ju8dmf/is_sonar_bad)

### 3.3 Rate limits — MAJOR, recurring
- "Here are the real Perplexity rate limits" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r02if1/here_are_the_real_perplexity_rate_limits)
- "10,000 credits in one hour — Perplexity Computer burns credits" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1s7top5/10000_credits_in_one_hour_perplexity_computer)
- Deep research API comparison (positioning) [title-only](https://reddit.com/r/AI_Agents/comments/1s7rteo/deepresearch_api_comparison_2026)

### 3.4 API key / auth bugs — MINOR
- "Is perplexity API key free? lol there is some bug" [title-only](https://reddit.com/r/perplexity_ai/comments/1fto7gc/is_perplexity_api_key_free_lol_there_is_some_bug)

---

## 4. BROWSER/APP BUGS

### 4.1 Context loss in chats — MAJOR, recurring
- "Sometimes perplexity loses the context" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1bq01b3/sometimes_perplexity_looses_the_context/)
- "Context Loss Issue with Perplexity.AI" [title-only](https://www.reddit.com/r/perplexity_ai/comments/14122ub/context_loss_issue_with_perplexityai/)
- "Perplexity forgets all context (example provided)" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1dfp01v/perplexity_forgets_all_context_example_provided/)
- "Perplexity can no longer read previous messages" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1i23pil/perplexity_can_no_longer_read_previous_messages/)
- "Notice something with long chats" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pdlmfr/notice_something_with_long_chats.json)
- "Is it just me or does Perplexity seem to have almost [no memory]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1cwzod9/is_it_just_me_or_perplexity_seem_to_have_almost/)

### 4.2 Search feature failing / not searching — MAJOR, recurring
- "Perplexity is not searching any sources for me" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1kc3pi9/perplexity_is_not_searching_any_sources_for_me)
- "Perplexity stopped doing search, instead giving tips how to [search]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1q85cgf/perplexity_stopped_doing_search_instead_giving)
- "Perplexity Not Returning Results. Anyone Else?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1mkrmvo/perplexity_not_returning_results_anyone_else)
- "Since when can Perplexity not search online?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1i0clmh/since_when_can_perplexity_not_search_online)
- "It just keeps on loading, no answers were given to me" [title-only](https://www.reddit.com/r/perplexity_ai/comments/16v7ku5/it_just_keeps_on_loading_no_answers_were_given_to)
- "Fix the web search enabling on its own please" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1ke4khq/fix_the_web_search_enabling_on_its_own_please)
- "Perplexity App Not Loading Results—Need Help!" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1hktly8/perplexity_app_not_loading_resultsneed_help)

### 4.3 Mobile app bugs — MAJOR, recurring
- "Endless Bugs, TERRIBLE UX" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nvz0nr/endless_bugs_terrible_ux)
- "WHY has the ANDROID APP been bugged for 24 HOUR ALREADY?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1n819bf/why_has_the_android_app_been_bugged_for_24_hour)
- "Android app [broken]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jqm7wx/android_app)
- "Can't see responses" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1n8e4be/cant_see_responses)
- "Just updated my Perplexity.ai app on iPhone 3 days ago. Today no read chats" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jdf7mb/just_updated_my_perplexityai_app_on_iphone_3_days)
- "Perplexity Pro Running Slow on Mobile – Anyone Else?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1ii969t/perplexity_pro_running_slow_on_mobile_anyone_else)
- "What's up with Perplexity's Voice Mode?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1lsu13j/whats_up_with_perplexitys_voice_mode)
- "Perplexity new voice mode sucks" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1izbol6/perplexity_new_voice_mode_sucks)
- "Strange issue downloading Perplexity on macOS" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m2crg4/strange_issue_downloading_perplexity_on_mac_os)

### 4.4 Web/desktop issues — MINOR→MAJOR, recurring
- "Perplexity not working on Safari today" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1fkhhyp/perplexity_not_working_on_safari_today/)
- "Perplexity Computer keeps freezing" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1rpduwz/perplexity_computer_keeps_freezing.json)
- "Some annoying bugs/issues" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1cwow4b/some_annoying_bugsissues/)
- "Why is Perplexity suddenly not doing what it's [told]?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/17v8q07/why_is_perplexity_suddenly_not_doing_what_its/)
- Cloudflare blocking legitimate users [title-only](https://www.reddit.com/r/perplexity_ai/comments/16sj2tn/cloudflare_security_blocks_me_when_trying_to_use/)

---

## 5. COMPARISON / SWITCHING AWAY

- "Bye bye perplexity" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1vb2feu/bye_bye_perplexity)
- "What are your favorite Perplexity alternatives? I'm leaving this service for good, I'm sick of this shit" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1fs6rxo/what_are_your_favorite_perplexity_alternatives_im)
- "Why are Perplexity users migrating away? Is it that bad…?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1u63nq1/why_are_perplexity_users_migrating_away_is_it)
- "Need an alternative to Perplexity now that it seems to be limiting Pro users" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qngqyy/need_an_alternative_to_perplexity_now_that_it)
- "Best Perplexity alternatives" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1rkm91n/best_perplexity_alternatives/)
- "Best Alternative to Perplexity's Deep Research?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1r14kva/best_alternative_to_perplexitys_deep_research/)
- "Does Perplexity make sense in 2026?" [title-only](https://reddit.com/r/perplexity_ai/comments/1qsufri/does_perplexity_make_sense_in_2026) — skeptical re-evaluation
- "What are the best alternatives to Perplexity in 2026?" [title-only](https://www.reddit.com/r/aiagents/comments/1tlir73/what_are_the_best_alternatives_to_perplexity_in/oni3xe5/)
- "Gemini Pro Deep Research Better Than Perplexity?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m2ddvl/gemini_pro_deep_research_better_than_perplexity)
- "Gemini vs Perplexity for my 2026" [title-only](https://reddit.com/r/perplexity_ai/comments/1q0vchs/gemini_vs_perplexity_for_my_2026)
- "Which AI is accurate for search?? gemini or grok or perplexity or chatgpt??" [title-only](https://reddit.com/r/perplexity_ai/comments/1q89y4l/which_ai_is_accurate_for_search_gemini_or_grok_or)
- "I'm tired of people recommending Perplexity over Google search or other AI platforms" [title-only](https://www.reddit.com/r/artificial/comments/1oq4ybp/im_tired_of_people_recommending_perplexity_over)
- "OpenAI Pro vs. Perplexity Deep Search for Research — is the price difference worth it?" [title-only](https://www.reddit.com/r/ChatGPTPro/comments/1iw4rjk/openai_pro_vs_perplexity_deep_search_for_research)
- "Perplexity vs ChatGPT (I think I have a good explanation)" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1bc03vx/perplex_vs_chatgpt_i_think_i_have_a_good/)
- "Comparing output quality — Perplexity Pro vs ChatGPT" [title-only](https://www.reddit.com/r/perplexity_ai/comments/17j7k1b/comparing_output_quality_perplexity_pro_vs_chatgpt/)

---

## 6. ACADEMIC / DEEP RESEARCH PROBLEMS

### 6.1 Deep Research hallucinations — CRITICAL, recurring
- "Warning: Worst case of hallucination using Perplexity Deep [Research]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1iyylmo/warning_worst_case_of_hallucination_using/)
- "Warning about Perplexity AI Deep Research, it [fabricates]" [title-only](https://www.reddit.com/r/singularity/comments/1iqjmng/warning_about_perplexity_ai_deep_research_it/)
- "Perplexity deep search sucks!" [title-only](https://www.reddit.com/r/ArtificialInteligence/comments/1kcqyuq/perplexity_deep_search_sucks)
- "Perplexity RESEARCH is DEAD. What's wrong with [it]?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1prby1g/perplexity_research_is_dead_whats_wrong_with/)

### 6.2 Academic research problems — MAJOR, recurring
- "How good is Perplexity with Academic Research?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/18wk8gw/how_good_is_perplexity_with_academic_research/)
- "Is Perplexity Pro subscription worth it for Studies and Academics?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jgz51u/is_perplexity_pro_subscription_worth_it_for)
- "How good is Perplexity Deep Research?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1j7dl2m/how_good_is_perplexity_deep_research/)
- "What types of queries does Perplexity struggle with?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1i26vey/what_types_of_queries_does_perplexity_struggle.json)
- "Is Perplexity lying about what models you can use?" (model gating during research) [title-only](https://www.reddit.com/r/perplexity_ai/comments/1lziyvt/is_perplexity_lying_about_what_models_you_can_use)
- Deep research comparison threads ("For those that have tried all three…", "8 deep research APIs side-by-side") [title-only](https://www.reddit.com/r/perplexity_ai/comments/1iqjoy9/for_those_that_have_tried_all_three_how_does_deep/) / [title-only](https://www.reddit.com/r/deep_research/comments/1pxa1df/i_tested_8_deep_research_apis_sidebyside_heres.json)

---

## 7. COLLECTIONS / SPACES LIMITATIONS — LOWEST SIGNAL

- "Anyone else facing a bug with Spaces right now" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1k9vz46/anyone_else_facing_a_bug_with_spaces_right_now)
- "What's this weird behavior of Perplexity saving a [thread to Spaces?]" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1q7fw96/whats_this_weird_behavior_of_perplexity_saving_a)
- "New feature: Perplexity AI Pro Spaces" (feature-launch thread with mixed reception) [title-only](https://www.reddit.com/r/perplexity_ai/comments/1g611dv/new_feature_perplexity_ai_pro_spaces)
- **Assessment:** dedicated complaints are rare vs. other categories; Collections/Spaces pain is mostly subsumed under context-loss and auto-filing weirdness. Severity: minor–major, low frequency.

---

## 8. IMAGE GENERATION COMPLAINTS — MAJOR, FREQUENT CLUSTER

- "Image-gen suddenly completely broken" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1lqkuqv/imagegen_suddenly_completely_broken)
- "Is it me or is Perplexity just bad at creating images?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m00emz/is_it_me_or_is_perplexity_just_bad_at_creating)
- "Generate image 👎" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1njhffk/generate_image)
- "Playground Image Generation is…bad?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1exygs3/playground_image_generation_isbad)
- "Generating images on Perplexity is a pain" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1gn480y/generating_images_on_perplexity_is_a_pain)
- "Image generation — not good" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1eyrip2/image_generation_not_good)
- "I tried image generation in Perplexity… it didn't go well" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1h34eo8/i_tried_image_generation_in_perplexity_it_didnt)
- "Why can't Perplexity do the same quality of image-gen that [others]?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1jonwxi/why_cant_perplexity_do_the_same_quality_of)

---

## 9. PRIVACY / DATA / LEGAL CONCERNS — MAJOR, RECURRING & RISING

### 9.1 Lawsuits & scraping controversies — CRITICAL (reputational/legal)
- NYT suing Perplexity for copyright infringement [title-only](https://www.reddit.com/r/perplexity_ai/comments/1pezbe5/the_new_york_times_is_suing_perplexity_for)
- Reddit suing Perplexity: "Reddit drags Perplexity in a new lawsuit, accusing it of building a $20 billion company off stolen data" + Perplexity's response thread [title-only](https://www.reddit.com/r/technology/comments/1oe6c1t/reddit_drags_perplexity_in_a_new_lawsuit_accusing) / [title-only](https://www.reddit.com/r/perplexity_ai/comments/1odpofv/our_response_to_reddits_lawsuit)
- "Perplexity's grand theft AI" [title-only](https://www.reddit.com/r/technology/comments/1dqbv52/perplexitys_grand_theft_ai)
- Amazon wins court order to block Perplexity's AI shopping agent [title-only](https://reddit.com/r/artificial/comments/1rq6qpi/amazon_wins_court_order_to_block_perplexitys_ai)

### 9.2 Data-sharing lawsuit & Comet privacy — MAJOR
- "Perplexity AI sued over alleged data sharing with Meta and Google" [title-only](https://www.reddit.com/r/technology/comments/1s9pcwu/perplexity_ai_sued_over_alleged_data_sharing_with/)
- "Serious privacy issues — Perplexity refuses to address — thinking of leaving" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1prrewb/serious_privacy_issues_perplexity_refuses_to/)
- "Security Concern of Perplexity Comet" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1nahfs4/security_concern_of_perplexity_comet)
- "Perplexity CEO's response re: privacy for Comet" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1m1w0ri/perplexity_ceos_response_re_privacy_for_comet)
- "Please Don't Download The Comet Browser… BRO WHAT" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1o05bny/please_dont_download_the_comet_browser_bro_what)
- "Why does Perplexity need my phone number?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1snueyx/why_does_perplexity_need_my_phone_number)
- "Now that Perplexity AI is involved what are the privacy concerns?" [title-only](https://www.reddit.com/r/Rabbitr1/comments/19a41a7/now_that_perplexity_ai_is_involved_what_are_the/)
- Paywall-access debate — "Can Perplexity/Comet access paywalled web links?" [title-only](https://www.reddit.com/r/perplexity_ai/comments/1ozx3sh/can_perplexitycomet_access_paywalled_web_links/)

### 9.3 Community/user data handling — MAJOR (related to account suspensions)
- "The Perplexity Pro users are being banned because they broke rules" (users banned for using the product heavily) [title-only](https://www.reddit.com/r/perplexity_ai/comments/1qv80pz/the_perplexity_pro_users_are_being_banned_because)
- "Perplexity suspended my free 1-year Pro plan citing TOS" [title-only](https://www.reddit.com/r/Perplexity/comments/1sqwbuj/perplexity_suspended_my_free_1year_pro_plan)

---

## Cross-cutting observations (for the automation skill design)

1. **Hallucination + citation-fabrication is the #1 complaint** — any automation must verify every cited source by fetching it, and cross-check claims independently. Perplexity's own correction loop ("ask it to double-check") is the most commonly used mitigation.
2. **Silent model downgrades / auto model-switching are a top trust issue** — automation should pin models explicitly and detect when the chosen model was swapped.
3. **Rate limits shift without notice** (Pro searches cut, Labs 50→25, weekly limits lowered, $5 API credit killed) — automation must not hard-code limits; read current plan policy or handle 429s gracefully.
4. **AI-only support ("Sam") blocks human escalation and refunds** — if the skill touches billing, don't rely on support; warn users about auto-renew.
5. **Context loss in long chats** is documented — automation should keep external memory/session state rather than trusting Perplexity threads.
6. **Legal/privacy risk is now material** (NYT, Reddit, Dow Jones/NY Post, Amazon injunctions, data-sharing suit) — a skill sending sensitive data should flag this.
7. **Deep Research mode is the highest-stakes hallucination risk** (fabricated medical/legal/financial info; 72% fabricated-reference study) — treat Deep Research output as draft, never authoritative.
8. **Reddit subreddit hostility to criticism** is itself a pattern users complain about (r/perplexity_ai burying complaint posts, bans from Discord/Reddit) — anecdotal but repeatedly alleged.

## File delivery
The final report could not be written to `/tmp/perplexity-reddit-issues.md` because the tool-call iteration limit was reached during the investigation. The complete content above is ready to be saved verbatim to that path by the parent agent (or re-run this subagent with a higher cap to write it directly).

**Issues encountered:** Reddit JSON API + old.reddit + redlib + jina reader all blocked from this network (403/redirect-to-HTML); only direct www.reddit.com URL extraction works, which is token-expensive and limited extraction to 6 representative threads. ~291 of 297 evidence URLs are title-only corroboration from search results, which is still strong for an inventory (titles are user-authored complaint headlines).