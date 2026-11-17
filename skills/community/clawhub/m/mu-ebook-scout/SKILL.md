---
name: mu-ebook-scout
display_name: 电子书下载器
version: 1.4.0
description: "Multi-source ebook search across 10 legal sources (public-domain classics, CBETA/ctext Chinese canon, LibriVox audiobooks, community netdisk book-lists via full GitHub code search, Google Books metadata). Use when the user wants to find or download a book, ebook, EPUB/PDF/MOBI file, or audiobook in Chinese or English — even without the word find, any mention of a book title together with epub/pdf/下载/电子书 counts. 不适用: academic papers or journal articles (use a general web search tool). 触发词/Triggers: find a book, ebook search, epub, public domain books, audiobook, 找书, 电子书, 公版书, 有声书, 下载书."
license: MIT
---

# mu-ebook-scout

Multi-source ebook search for legal public-domain, open-license, and
community-indexed books. The tool is a guide first: it surfaces ranked
links and direct download URLs; it only downloads after the user
explicitly asks for one.

**IRON LAW：①绝不空手而归——公版源零命中不是终点，必须继续解析直达链接（微信读书 deepLink、GitHub 网盘书单、IA 借阅页），全部失败才降级到入口链接；把搜索页丢给用户自己去搜=任务失败。②下载必须等用户明确指令（「下载第N条」或同等表述）才执行，禁止预下载、禁止批量。③网盘结果一律 LINK_ONLY 并如实标注版权状态，工具不碰网盘，除非用户明确要求代取。**

## When to use

- The user wants to find a book / ebook / EPUB / PDF / MOBI / audiobook.
- Public-domain classics, ancient Chinese texts, the Buddhist canon.
- Modern Chinese titles: community netdisk lists (github_lists source)
  cover copyrighted bestsellers — present them as link-only hits.

## Workflow

1. Run the search and wait for it to finish:
   ```bash
   bookscout search "书名"
   ```
2. Relay the results. The report groups hits by availability:
   ✅ direct download, 📖 read online / audiobook, 🔗 netdisk link-only,
   🛒 borrow / purchase. Present each hit's number, source, URL and
   formats in a clean readable list — summarize, do not dump raw output.
3. **Zero hits does not end the task** (IRON LAW ①). Try to resolve a
   direct link before falling back to entry links:
   - For copyrighted Chinese books, open the WeRead search page
     (`https://weread.qq.com/web/search/global?keyword=...`) and extract
     the matching book's `book-detail` deep link to hand over directly.
   - Check the Internet Archive details link — borrowable with a free
     account.
   Only when neither resolves, relay the search-entry links the tool
   printed (extended resources, manual entries, purchase channels).
4. Netdisk hits (ctfile / lanzou / baidu pan, marked link-only): give the
   user the link plus its extraction code if present. If the user asks
   you to fetch the file for them, follow
   [ctfile-playbook.md](references/ctfile-playbook.md) (ctfile links)
   or the netdisk flow that matches the host — always on explicit user
   request only (IRON LAW ③).
5. Stop and wait (IRON LAW ②). Only when the user explicitly says
   "下载第N条" or an equally unambiguous confirmation, run:
   ```bash
   bookscout get N
   ```
   Never download preemptively, never batch-download multiple items.

## Environment (optional, unlocks more sources)

- `GITHUB_TOKEN` / `BOOKSCOUT_GITHUB_TOKEN` — enables full GitHub code
  search for netdisk book-lists (anonymous: curated seeds only).
- `BOOKSCOUT_GOOGLE_BOOKS_KEY` — activates the Google Books source.
- `https_proxy` / `http_proxy` — standard proxy vars; needed in some
  networks to reach archive.org download nodes. See README Network FAQ.

## Rules

- Custom sources (user-configured) return link-only results. Give the
  user the link; never call `get` for these hits.
- If the search returns nothing, relay the manual entry points and
  legitimate borrow/purchase channels printed by the tool. Never leave
  the user empty-handed, and never invent sources the tool did not return.

## Known limitations

1. [P] Anna's Archive / LibGen / archive.org download nodes unreachable
   in some networks → blocked-network environments → hand over the
   entry links, suggest the standard proxy env vars (README Network FAQ).
2. [P] Non-bestseller titles may have no netdisk backup anywhere
   (book-list repos only index popular titles) → niche/professional
   books → resolve a WeRead deep link plus purchase channels, say so
   honestly instead of promising a file.
3. [P] Netdisk direct-link fetching needs a browser and breaks often
   (anti-bot verification, site redesigns) → agent-assisted netdisk
   downloads → fall back to link + extraction code for the user to
   download manually.

## references/ index

| File | Purpose |
| ---- | ------- |
| [ctfile-playbook.md](references/ctfile-playbook.md) | Five-step ctfile netdisk direct-link playbook (navigate → variables → API → curl → GBK unzip + magic-number verify) |
