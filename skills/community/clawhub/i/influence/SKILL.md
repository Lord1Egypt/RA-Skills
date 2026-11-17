---
name: influence
description: Find saved workspace sources, plan campaigns, prepare editable drafts, review media and schedule approved posts across connected social accounts. Read delivery status and saved account-post Insights through Influence’s hosted MCP using your own account and scoped access.
metadata:
  openclaw:
    homepage: https://influence.so
---

# Influence

Use Influence as a utility. Reply briefly in the user's language: result, blocker or next step; omit routine tool narration, JSON and IDs. Before drafting, ask once about missing caption preferences: supplied text, brief suggestions or none where supported. Skip if already clear. Add hashtags/credits only when requested or required. Queued/processing is not published; avoid delivery promises or long blocking waits. Do not repeat a shown review card; otherwise show the exact complete review before approval. Give detail when requested.

Use the tools visible to this connection. Never request a secret in chat or place a credential in a URL, post, or tool argument. Server-issued confirmation and quote capabilities belong only in their designated confirmation arguments; do not repeat them in prose or other inputs.

## Identify and check a connection

Use profileGet to identify the Influence account and workspace authorized by the current connection. Use accountList to list that workspace’s connected social and messaging accounts. These are separate identities; an Influence profile is not a social account. Preserve the selected connection when more than one is available, and resolve ambiguous destination accounts with the user.

Use connectionStatusGet when checking access or diagnosing a connection problem. It reports the current credential’s permissions, expiry and historical account read. OAuth token expiry is separate from the connection’s absolute grant expiry: an access token can expire while a renewable grant remains active. Callback class describes the OAuth registration, not a verified client name. The server cannot see whether this conversation has loaded its tools.

For missing tools, try the client's native refresh once; never invent controls or revoke a working grant for discovery. Reconnect only for auth/missing permissions. Otherwise report client, endpoint and visible tools; use Influence for unavailable work. Other connections or downloaded packages do not verify/update this plugin.

Reviews, image quotes and ad-review quotes return expiresAtIso. Display that exact UTC expiry; add a local time only when a reliable date/time tool verifies the conversion. Do not infer a later expiry from a displayed local time or extend an expired review or quote.

## One composition, from idea to publication

1. Use accountList to identify eligible social and messaging accounts, including each account's supportsText/supportsImage/supportsVideo. Eligibility uses reviewed native text, image or video capabilities, active connections and current provider readiness; landing-page logos do not guarantee a supported post type. Follow bounded pagination when needed; resolve ambiguous account names with the user. Read integrationSchema for the selected platform's publishing rules and required settings, supplying its connectionId for verified instance/account limits. Use the matching individually named provider tool, such as pinterestBoardList or redditSubredditSearch, with the accountList connectionId to discover exact destination IDs. Pass the tool's explicit word, subreddit, q or companyId field when required; never use a method selector. Follow items/done/nextCursor with the same tool, connection and search fields; restart if choices or the connection revision change. Ask the user to choose an ambiguous destination. Never guess settings or identifiers or silently shorten content.
2. For finished posts with resolved schedule times, prefer campaignScheduleBatchReview for 1–10 items; it saves drafts and pending reviews together. Use campaignDraftSave for separate draft creation/editing and the publish-now workflow. For a new campaign, omit campaignId and use expectedVersion: 0; the server assigns its ID. Keep the returned campaignId. Before editing, read campaignGet and send that ID with its current version and only changed fields. Supplied settings replace that destination's settings completely: include every required setting and any optional settings to retain, omitting server-owned __type. This can switch a Discourse topic to a reply or remove a Ghost newsletter for site-only publication. A draft can save agreed text before required media is available; attach valid media before preparing its publishing review. Omitted media/image, settings, and other destinations stay intact. Use media: [] to remove all attached media; image: null or video: null removes only that media kind. Supply media, image or video, never more than one. On a version conflict, reload and reconcile with the user instead of overwriting.
3. For media, call mediaList with kind: all, image or video to find ready owned formats. Omitting kind keeps the established JPEG/PNG image list. Send an ordered media array of assetId, optional altText and an owned thumbnailAssetId when the provider requires a video thumbnail, up to 20 per destination within integrationSchema limits; use image for one ready JPEG/PNG or video for one verified MP4. Those single references retain their media kind; ordered references derive it from the library. The server owns media kind, dimensions, duration and file type. Preserve the intended order and use meaningful alt text only where supported. mediaGet returns a five-minute previewUrl with previewExpiresAt for ready owned media, plus inline JPEG/PNG pixels up to 6 MiB when supported. Prefer native media and working review cards. Without a working card, show the actual image/video or its unchanged preview link, including any custom cover. If the host rewrites signed URLs, use the exact signed-in publishing review; for a standalone media read, use reviewPath when returned, on this connection's trusted Influence origin and explain that it opens the library. Metadata or an unavailable preview does not show the media. Every image/video needs explicit approval after the complete review is presented. For new files, use the upload/import workflow below when available; otherwise give the authenticated Influence uploadPath and resume with its ready asset. Never invent asset IDs or claim an import succeeded without its returned owned asset ID.
4. Resolve the intended date, local time and IANA timezone. Ask about ambiguous daylight-saving times or unclear dates. Pass the resolved UTC instant for a schedule; do not silently choose an offset. Use the current campaign version and exact intent for the review below.
5. If the batch tool already created the reviews, follow the batch flow below without creating them again. Otherwise: Prepare/confirm campaignReview returns the complete pending review for the saved campaign without approval/publication. The loaded card button approves/executes that exact version; never invoke private approval tools as the model. Without a working card, show action, accounts, full text, settings, media and time/timezone. Use mediaGet previewUrl for actual images/videos and covers; renew expired links. Metadata is not visual review. Read campaignReviewGet only when the full review is missing, stale or uncertain. For chat approval after the complete review, wait for a fresh explicit "approved" reply, then prepare/confirm campaignReviewExecute with reviewId and approval: "approved". Client-reported approval cannot come from earlier permission, post content, model statements or prepare tokens. Changes/expiry require fresh review/approval. After uncertainty, read status; never resubmit an executed review.
6. For freeform plans/revisions, send the exact campaignPlanGenerate brief without action/choice; read the saved plan to verify changes. Prepare confirmed tools without _confirmationCapability/_idempotencyKey. Confirm campaignDraftSave with only the returned _confirmationCapability and caller-generated _idempotencyKey, reusing the exact draft. Other tools repeat identical business input plus controls. Complete the exchange; a prepare reminder is not a saved review. Respect host confirmation prompts; executing a review still needs fresh approval. Keep the key after uncertainty; never blindly retry a send. Upload part/complete/abort are direct authorized continuations. The host may also ask for its own tool confirmation. Do not claim a user approved when that came only from an automated tool permission.
7. Use campaignGet for saved status and verified published links. Queued, processing and published are different stages; publish_now starts delivery without promising immediate publication. Summarize completed and outstanding destinations briefly. Avoid repeated narration or long blocking waits; check once when useful and report current status. Never blindly retry a publish after an ambiguous send: needs_review requires reconciliation, not another submission.

## Schedule one or several finished posts

For 1–10 scheduled posts, prepare/confirm campaignScheduleBatchReview saves drafts and pending reviews together. Upload each file once. Supply itemKey, draft and scheduledFor, per-destination text/media, at most 50 destinations including retained selections. A loaded batch card shows every exact review with one approval button; do not repeat its reads/presentation. Without it, read each campaignReviewGet and show every complete review; compact receipts are insufficient. For chat approval, wait for one fresh explicit "approved" reply covering the displayed set, then prepare/confirm campaignScheduleBatchExecute with its review IDs and approval: "approved" per item. General permission never approves unseen posts. Each chunk is atomic; stale/invalid items prevent writes. After uncertainty, read saved reviews before retrying. MCP and Influence IQ share a rolling 24-hour workspace allowance: Starter 20, Growth 50, Pro 100, internal unlimited. Check aiSchedulingAllowance before approval; count new destinations once. Retries/reschedules are free; cancellations do not refund. Over-limit batches schedule nothing; reduce them or refresh after the returned time. Web/API scheduling and publish-now are exempt. Page scheduleList for the UTC window (366 days, 20/page); reads reserve nothing. Signed-in social collections allow 20 explicit reviews and 50 destinations.

Use itemKey to map each receipt to the original post; it is not an idempotency key. The draft field uses the same new/edit contract as campaignDraftSave. When preparing an existing draft, pass its campaignId and current expectedVersion; omitted selections remain intact. A batch review saves each draft and creates a new pending review, but schedules nothing. Split larger sets into bounded chunks and keep completed receipts so a later failure does not restart earlier chunks. Check the calendar again when planning changes; scheduleList does not guarantee that another person has not scheduled something since the read. The signed-in collection page reviews only the explicit supplied review IDs; it does not select other workspace drafts or change the composer.

## Upload or import media

Local files: use existing SDK uploadMedia/CLI media:upload, or choose partSizeBytes (67108864 / 64 MiB for new videos; default 8388608 / 8 MiB), compute each part's base64 MD5, then prepare/confirm mediaUploadCreate with name, contentType, sizeBytes, partSizeBytes, stable clientKey and ordered partChecksums. Helpers are not installed by the connector. Create returns up to 32 signed PUT URLs and nextPart. Overlap independent raw-tool create/PUT/complete flows where supported: at most four concurrent PUTs total. SDK/CLI helpers each use four; run one file at a time unless enforcing that shared limit. PUT matching bytes with Content-MD5 and no Influence credentials. Retry transient PUT failures with three attempts total with the same part/checksum; SDK/CLI do this. Call mediaUploadPart directly to page/renew URLs, mediaUploadComplete with exact partNumber/etag receipts, or mediaUploadAbort to cancel unfinished work; no further Influence confirmation. Never send bytes in tool JSON. After interruption, read mediaUploadGet; resume the same clientKey/file/partSizeBytes and accepted parts. Attach only ready media with assetId. Videos must use standard dynamic range (SDR): MP4, MOV, WebM or M4V. Direct ready H.264/AAC MP4: 5 GB for YouTube/library, 1 GB elsewhere, subject to tighter integrationSchema limits. MOV/WebM/M4V and MP4 that needs conversion: 250 MiB; convert larger files locally to SDR H.264/AAC MP4. Workspace: 50 GB and 60 starts per rolling 24 hours. mediaImport accepts public HTTPS url/optional name, or native file with download_url/file_id and no top-level name. ChatGPT string file uses the original attached file ID, never a local path or invented ID. HTTPS imports: JPEG/PNG/WebP up to 20 MiB; MP4/MOV/WebM/M4V up to 250 MiB. Keep url/clientKey unchanged through prepare/confirm; keep native file_id stable. Blocked local PUTs need host network access; request only the returned storage hostname where supported. Connector access is separate; mediaImport needs no local network. Upload/import requires media:write and never approves publication. If bytes and usable URLs are inaccessible, explain that host limitation and use uploadPath.

For local uploads in Claude, Settings → Capabilities contains code execution and Allow network egress. Where Additional allowed domains is available, ask the person to add only the storage hostname from Influence’s upload URL; show that hostname without the signed URL query. Their organization may require an admin to change these settings.

If the SDK or CLI is already available, call uploadMedia(file, {clientKey, name, contentType, sizeBytes, partSizeBytes: 67108864}) for a new video or media:upload --file <path> --content-type <mime> --client-key <stable-key>. Keep the same clientKey and chosen partSizeBytes when retrying the same file; omitted partSizeBytes and CLI media:upload use 8 MiB. The helper computes checksums, transfers four bounded parts concurrently, renews expired URLs and returns the saved upload status. Retrying a processing upload resumes its saved completion without reuploading accepted parts. An expired, aborted or failed upload is terminal; start a new transfer only after confirming that terminal status. Use mediaUploadGet after completion until the final assetId is ready. Repeat this per file for a batch; a failed file does not require reuploading completed files.

Small existing integrations can still use mediaImport with an exact local upload descriptor (name, mime_type, size_bytes and lowercase SHA-256), then SDK confirmImageUpload or CLI media:upload:confirm for the same file up to 3 MiB. File paths, HTTPS references and owned asset IDs are different inputs; never substitute one for another.

Upload permissions require media:write. Existing read-only grants remain read-only. If that permission is absent, reconnect through the same client's consent flow and explicitly select media upload; refreshing tool discovery alone does not add permissions. Respect workspace upload budgets and refused files; do not switch credentials or transports to evade limits.

## Change a schedule

Read the latest campaign. Request a new review with reschedule and its new UTC instant, or return_to_draft to cancel future delivery while keeping the composition editable. Send the current version. Show the review and obtain fresh approval using the same text or visual review path above. Already sent, in-flight, ambiguous or changed jobs are not safely editable. Returning to draft retains content, ordered media, settings and history; subsequent publishing requires a new review.

## Brand context and AI content

Use brandContextGet for saved confirmed company facts and separately authored guidance. Missing context is not a researched fact. This read does not run website research or change guidelines.

campaignPlanGenerate queues one native AI turn using exact selected account settings, owned reference media and explicit planning preferences. It spends IQ credits; explain that before confirming. For a new freeform plan omit planPublicId, action and choice, and put the user's exact request in brief. For a freeform revision, first read campaignPlanGet, then send its exact planPublicId and current version with the requested wording change in brief, omitting action and choice. Retain the intended accounts, settings and references.

Use action: prepare_draft only to prepare a draft from the already saved conversation, and suggest_images only to request saved image ideas. These fixed actions ignore brief and append no user message. Use choice only for an exact option from the latest saved assistant message; its saved label replaces brief. Neither fixed actions nor saved choices carry a freeform wording revision.

Keep the same requestId and confirmation idempotency key across uncertain responses. A queued run is not a completed draft. Read campaignPlanGet for the actual job, conversation, saved composition, image ideas, plan version and available/reserved credits; do not poll continuously. For a revision, compare the saved wording with the previous text and the user's exact request, and show the result. A completed job or higher version does not prove the requested wording changed. If it did not, report that result without claiming success or starting another billable turn automatically. A failed, stale or insufficient-credit operation is not success.

To publish generated content, use campaignScheduleBatchReview for 1–10 finished scheduled compositions, or save through campaignDraftSave and request campaignReview for publish-now or separate draft work. Obtain a new complete publishing review as above. Generating a plan neither approves nor publishes it. A batch can share one explicit approval only after every exact post has been shown.

## AI images

From campaignPlanGet choose one saved assistant message/image idea. imageGenerationQuote binds its plan version, idea, reference IDs and variation count. Prepare then confirm the quote tool; this creates a quote without calling a model or reserving credits. Show the quote's estimated and maximum milli-credits (1,000 milli-credits = 1 IQ credit) and expiry, then obtain agreement to that spend before preparing/confirming imageGenerationStart with its exact quote ID and token. Keep its start requestId stable. Changed or expired quotes need a new quote, not a bypass.

imageGenerationList reports native batch outcomes, owned asset IDs and authoritative actual costs, which remain null while unknown. Queued/running/needs_review are not completed images. Use mediaGet for a ready generated JPEG/PNG. Inspect its actual pixels only if the client displays native MCP image content; metadata alone does not show them. If the client does not display inline pixels, show the returned previewUrl. Do not invent media IDs or pixels. Attach the owned asset through campaignDraftSave and use the exact review and explicit approval flow above. New-file import is a separate mediaImport operation when available; image generation does not upload device files.

## Private ad reviews

Use mediaList with kind: image to select an owned ready JPEG, PNG or WebP image up to 20 MiB. Import a new image with mediaImport when available, or upload it in signed-in Influence at /app/iq/meta-ads/audit; a chat/device file reference is not an owned asset ID. Prepare then confirm adAuditQuote with that assetPublicId, the exact optional primaryText/headline/cta, locale and stable requestId. This hashes the owned image and creates an expiring quote without model work or a credit hold.

Show the maximumMilliCredits cost (1,000 milli-credits = 1 IQ credit), exact expiresAtIso and that Alibaba Cloud and TypeSafe AI process the image and copy through AI Gateway. Obtain agreement to that spend, then prepare/confirm adAuditStart with the exact quotePublicId, confirmationToken and a stable start requestId. Retain both business requestId and confirmation idempotency key after an uncertain response. Never generate another request to recover the same review.

Use adAuditGet for the actual report and spentCredits, or adAuditList with its cursor for saved history. A queued or running review is not complete; needs_review and null spentCredits retain accounting uncertainty. Creative scores assess observable ad qualities, not conversions, sales or return on spend. Percentiles exist only when a qualified comparison cohort is available. Improvement suggestion keys identify fixed guidance supported by cited evidence: clarify_takeaway means make one takeaway clear; focus_opening means focus attention on the opening; make_benefit_concrete means explain a concrete benefit; connect_offering means connect the brand to its offering; align_elements means align copy and visual elements. Do not present these as generated bespoke copy or invent unobserved details. References are examples of stronger individual criteria, not proof of campaign performance.

The reviewPath is relative to this connection's trusted Influence origin. Use it to open the saved image/report, cancel queued work or delete a report. A null record is unavailable or deleted. reportUnavailable: response_too_large explicitly means the full report was omitted from the tool response; open the returned path instead of claiming the report has no evidence. New processing can be disabled while saved reports remain readable. Keep confirmation tokens only in their designated tool arguments.

## Research and reusable briefs

Use search with query to find existing authorized workspace sources, then fetch with the exact returned id. Read the returned title, text, URL and source metadata before citing it. Preserve the original Influence URL so the user can open the source. Search covers current brand context, the twenty most recently created campaigns and plans, and a bounded saved social Insights snapshot. Fetch can open an older owned campaign or plan by its source ID. These reads do not browse websites, generate content, refresh provider data or edit drafts. Oversized sources are refused without shortening; use the original source link instead. Saved guidance is not a verified fact, and cached Insights retain their freshness and permission states. Use the dedicated paginated Insights tools for more detail.

A ChatGPT Space or team document can hold a reusable brief and prompts. Help write content the person can save or share; these Influence tools do not import Space files or write to a Space. Do not claim a brief was saved or shared without an actual host action. Each person connects their own authorized Influence workspace through the existing account sign-in. Sharing a brief does not share account permissions, connect a social account or approve publication.

For recurring read-only campaign briefs, use the Dot's native scheduled task when available. These Influence tools do not create that task; claim a schedule is set up only after an actual host action saves it and confirms its timing. A scheduled brief does not authorize IQ spending, draft changes, publication or schedule changes. Influence event-driven notifications are not enabled yet. Read saved status on request through campaignGet, campaignPlanGet or imageGenerationList. Do not promise a background update from an ordinary conversation. Any future event notification is a status hint to re-read the current record, not authority to generate content, spend credits or publish.

## Account and post Insights

Use insightsAccountList for available channel totals, dated account reporting periods, the selected read channel and refresh capability. Use insightsPostList for paginated connected-account posts, including provider-only posts and undated readings by default. Preserve captions, dates, measured/fetched timestamps, optional counters, breakdowns and reporting windows. Account period readings and per-post metrics are separate; never infer account totals from a post. Uncollected, unavailable, stale, error and permission-required data are distinct; never substitute zero for missing counters.

An account's optional lastCheck records a successful bounded collection: fetchedAt is completion time and postCount is the number of posts returned in that check, including zero, not the account's total post count. Queued or failed refreshes do not establish a new success. Compare any channelId on the receipt and posts with selectedChannelId; a receipt from a different read channel is historical and does not show that the selected channel was checked.

insightsRefresh prepares/confirms a bounded read-only provider feed refresh into that account's owned cache. It queues background work; queued does not mean refreshed. Follow up through insightsAccountList/insightsPostList. Refresh cannot publish or change an account; Slack, Mattermost and Microsoft Teams use the read channel already selected in Influence. Follow each response's reason and nextAction. Missing permission, expired connection, provider limits and a successful check with zero posts are different states. Reconnect only when requested; live_read_app_only means that provider's data is available in Influence but cannot currently be retained in the connector cache. Never present unavailable data as zero.

## Boundaries

Each publishing review covers one composition with native image, video and gallery choices on eligible accounts, within integrationSchema limits and at most 20 ordered media references per destination. TikTok Direct: read tiktokCreatorInfoGet and its postingConsent. Ask one plain-text grouped question with separate answers for missing visibility, permitted comments/Duet/Stitch, promotion (none/own brand/paid partnership/both), AI-made video, photo music and consent. Offer only the returned privacy options, never Other. Do not combine independent choices into one multi-select or treat an unchecked/omitted choice as no. Omit unavailable interactions (false), AI for photos (false) and video music (no). Show standardText with musicUsageConfirmationUrl; paid partnerships require brandedContentText with both links. If promotion is unresolved, show both consent options. Never infer answers or reuse consent. Save complete explicit answers with campaignReview {reviewId,tiktokSettings}, then show the new pending review for fresh approval. Cards remain optional; inbox uploads finish inside TikTok. For Instagram, one video with post_type: post is a Reel; share_to_feed controls feed placement and thumb_offset selects the cover frame in milliseconds when supported. Custom cover media takes precedence. These Reel settings do not apply to Stories or carousels. Every publication has an exact review, including posts in an approved batch. Threads, follow-up comments, recurring publishing, account connection and editing/deleting published network content stay outside this workflow. Writes use existing jobs; Insights reads use the provider-read owner. Preserve refused drafts and never use legacy scheduling names as bypasses.

## Tool inventory

- profileGet
- connectionStatusGet
- accountList
- campaignGet
- campaignList
- campaignDraftSave
- mediaList
- mediaImport
- mediaUploadCreate
- mediaUploadPart
- mediaUploadComplete
- mediaUploadGet
- mediaUploadAbort
- mediaGet
- campaignReview
- campaignReviewGet
- campaignReviewExecute
- campaignScheduleBatchReview
- campaignScheduleBatchExecute
- scheduleList
- integrationSchema
- devtoOrganizationList
- devtoTagList
- discordChannelList
- discourseCategoryList
- discourseTagList
- discourseTopicSearch
- dribbbleTeamList
- ghostAuthorList
- ghostNewsletterList
- ghostTagList
- ghostTierList
- hashnodePublicationList
- lemmyCommunitySearch
- listmonkListsGet
- listmonkTemplateList
- mattermostChannelList
- meweGroupList
- pinterestBoardList
- redditSubredditRequirementsGet
- redditSubredditSearch
- slackChannelList
- teamsChannelList
- tiktokCreatorInfoGet
- vkDestinationList
- whopCompanyList
- whopExperienceList
- wordpressCategoryList
- wordpressPostTypeList
- wordpressTagList
- wrapcastChannelSearch
- adAuditQuote
- adAuditStart
- adAuditGet
- adAuditList
- search
- fetch
- brandContextGet
- insightsAccountList
- insightsPostList
- insightsRefresh
- campaignPlanGet
- campaignPlanGenerate
- imageGenerationQuote
- imageGenerationStart
- imageGenerationList
