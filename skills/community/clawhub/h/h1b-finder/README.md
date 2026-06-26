# H1B Sponsor Finder for OpenClaw

Find H1B sponsor companies and visa-friendly jobs faster.

快速查找 H1B sponsor 公司和支持工签的岗位。

This ClawHub skill helps users search historical H1B / H-1B sponsor activity by company, role, city, state, and year, so they can narrow a US job search toward employers with prior visa sponsorship records.

这个 ClawHub 技能帮助用户按公司、岗位、城市、州和年份检索历史 H1B / H-1B sponsor 活跃度，更快筛出有过工签支持记录的美国雇主。

## Features

- Find H1B / H-1B sponsor companies by role, employer, city, state, or year
- Compare sponsor history across employers
- Review filing-based role, location, and salary signals when available
- Support natural English and Chinese queries

- 按岗位、公司、城市、州或年份查找 H1B sponsor 公司
- 对比不同雇主的 sponsor 历史
- 在有记录时查看岗位、地区和薪资相关信号
- 自然支持英文和中文提问

## Example queries

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

## Install

```bash
npx clawhub install h1b-finder
```

## Use

Ask practical questions about sponsor companies, visa sponsorship employers, employer comparisons, or filing history.

直接提问 sponsor 公司、工签支持雇主、雇主对比或历史提交记录相关问题即可。

```text
Use $h1b-finder to find H1B sponsor companies for backend engineer near Washington DC.
```

```text
用 $h1b-finder 帮我找华盛顿 DC 附近愿意 sponsor Backend Engineer 的公司。
```

## What you'll get

- A short answer first, then a ranked shortlist or comparison
- Employer names with role, location, or filing-history context
- Salary or trend notes when the records support them
- Caveats when data is incomplete, delayed, or not directly comparable

## Limitations and disclaimer

- Data may be incomplete or delayed.
- Results may not reflect current openings or current hiring plans.
- Historical filing activity is a useful signal, not a guarantee of sponsorship.
- This skill is not legal advice. Verify before making visa or job decisions.

- 数据可能不完整，也可能存在滞后。
- 结果不一定反映当前岗位开放情况或当前招聘计划。
- 历史提交记录只能作为参考信号，不代表一定会 sponsor。
- 本技能不构成法律建议；在做签证或求职决定前请自行核实。

## Links

- Homepage: https://h1bfinder.com
- Repository: https://github.com/ewangchong/h1bfinder.com
