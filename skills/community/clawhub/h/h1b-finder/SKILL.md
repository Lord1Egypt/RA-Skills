---
name: h1b-finder
description: Find H1B / H-1B sponsor companies, visa sponsorship employers, and sponsor history for US jobs.
version: 1.1.1
acceptLicenseTerms: true
metadata:
  openclaw:
    emoji: "💼"
    requires:
      apis:
        - h1bfinder.com
    recommend:
      agents:
        - engineering
        - marketing
        - legal
        - finance
    version: 1.1.1
    author: h1bfinder.com
    homepage: https://h1bfinder.com
---

# H1B Sponsor Finder / H1B Sponsor 查询

Find H1B sponsor companies and visa-friendly jobs faster.

快速查找 H1B sponsor 公司和支持工签的岗位。

## English capability bullets

- Find H1B / H-1B sponsor companies by role, employer, city, state, or year.
- Compare sponsor history across companies such as Amazon, Google, and Microsoft.
- Surface filing-based role, location, and salary signals when records support it.
- Narrow a US job search toward employers with historical visa sponsorship activity.

## 中文功能要点

- 按岗位、公司、城市、州或年份查找 H1B sponsor 公司。
- 对比 Amazon、Google、Microsoft 等公司的 sponsor 历史和活跃度。
- 在有记录时给出岗位、地区和薪资相关的提交信号。
- 帮你先筛出更可能支持工签的美国雇主，再决定投递方向。

## Best for / 适合谁

- International students, OPT candidates, early-career job seekers, and experienced candidates targeting US employers with work visa support.
- People researching H1B sponsor companies, visa sponsorship jobs, H1B-friendly employers, or filing history before applying.
- 想找 H1B 雇主、工签支持岗位、Sponsor 公司，或先看 sponsor 记录再投递的中英文用户。
- 想按岗位、城市、州、年份或公司名缩小美国求职范围的用户。

## Example queries / 示例问题

### English

- Find H1B sponsor companies for data engineer roles in Seattle.
- Find H1B sponsoring employers for software engineer in Virginia.
- Compare H1B sponsor activity for Amazon, Google, and Microsoft.
- Find entry-level H1B-friendly jobs for new grads in New York.
- Find companies sponsoring product manager roles in California.
- Find H1B jobs near Washington DC for backend engineers.
- Show employers that filed for data analyst roles in Texas.

### 中文

- 帮我找 Seattle 的 Data Engineer H1B sponsor 公司。
- 查 Virginia 的 Software Engineer sponsor 雇主。
- 对比 Amazon、Google、Microsoft 的 H1B sponsor 活跃度。
- 找适合应届生的 H1B 友好公司，最好在 New York。
- 找支持 Product Manager 的 sponsor 公司，范围看 California。
- 找华盛顿 DC 附近适合 Backend Engineer 的 H1B 工作。
- 查哪些公司给 Data Analyst 岗位提交过 H1B，最好看 Texas。

## What you'll get / 输出内容

- A short answer first, then a ranked shortlist or compact comparison.
- Employer names with role, location, year, or filing-history context.
- Salary or trend notes when the underlying filing records support them.
- Caveats when coverage is thin, delayed, or not directly comparable.
- A useful next step, such as narrowing by city, role, employer, or fiscal year.

- 先给一句结论，再给简明 shortlist 或公司对比。
- 展示雇主名称，以及岗位、地区、年份或提交历史的上下文。
- 如果底层记录支持，会补充薪资或趋势提示。
- 当覆盖不足、数据滞后或口径不完全可比时，会明确提醒。
- 最后给出下一步建议，比如继续按城市、岗位、公司或财年细化。

## When to use this skill / 何时使用这个技能

Use this skill when the user is asking about H1B sponsor companies, visa sponsorship jobs, companies that filed H1B, H1B-friendly employers, US jobs with work visa support, or sponsor history by company, role, city, state, or year.

当用户在问 H1B sponsor 公司、支持工签的美国岗位、哪些公司提交过 H1B、H1B 友好雇主、某公司或某岗位的 sponsor 历史时，应优先使用这个技能。

It is especially useful for queries that sound like sponsor lookup, employer comparison, filing-history research, or "which companies are more likely to support work visas for this role?"

尤其适合这类问题：查 sponsor 公司、比较雇主 sponsor 活跃度、看历史提交记录，或者问“这个岗位哪些公司更可能支持工签？”

## Search basis / 检索依据

- Uses historical public labor disclosure data surfaced through h1bfinder.com.
- Best for sponsor lookup, filing-history research, employer comparison, and role/location exploration.
- Helpful for finding sponsor leads, but it is not a live job board and not an official government source.

- 基于 h1bfinder.com 提供的历史公开劳工披露数据进行检索和整理。
- 适合做 sponsor 查询、提交记录研究、雇主对比，以及岗位和地区探索。
- 适合找 sponsor 线索，但它不是实时职位板，也不是政府官方数据入口。

## Response style / 输出方式

- Prefer concise, decision-oriented answers over long background explanations.
- Translate the request into practical filters such as employer, title, city, state, year, or comparison scope.
- If the request is underspecified, make one reasonable assumption and state it briefly.
- Ask a follow-up only when the missing detail would materially change the result.

- 先给实用结论，再补充必要说明，不要先讲长背景。
- 尽量把问题转成公司、岗位、城市、州、年份或对比范围等筛选条件。
- 如果信息不完整，可以做一个合理默认假设，并简短说明。
- 只有在缺少关键信息会明显影响结果时，才继续追问。

## Notes / 注意事项

- Data may be incomplete, delayed, or uneven across employers, roles, locations, and years.
- Historical filing results do not guarantee that a company is hiring now or still offering sponsorship.
- This skill is informational only. It is not legal advice, immigration advice, or a guarantee of job outcomes.
- Verify important details yourself before making job-search, visa, or legal decisions.
- Homepage: https://h1bfinder.com

- 数据可能不完整，也可能存在滞后，不同公司、岗位、地区和年份的覆盖度会不同。
- 历史提交记录不代表公司当前一定在招聘，也不代表现在仍然提供 sponsor。
- 本技能仅提供信息参考，不构成法律建议、移民建议或求职结果保证。
- 在做求职、签证或法律相关决定前，请自行进一步核实。
- 主页：https://h1bfinder.com
