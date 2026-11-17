# A report that compares several postings

Read this with `references/report-writing.md` when a client report covers more
than one posting — a discover consultation, or a ranking of postings the user
supplied. `report-writing.md` holds the rules every report follows; this file
adds the job directory, grouping and job-identity rules a single-posting report
never needs.

## Every retained posting is read in full

Before calling a consultation complete, read every retained posting in full.
The initial shortlist and the final report have different completeness standards:
unattempted summary cards are research leads, not completed report entries.
Keep an unavailable description only with a captured access failure, its visible
reason and an unresolved status. An explicitly requested preliminary delivery
may retain cards. Follow discover mode and `deliver.py` for the checked inputs;
reading a description does not imply a completed CV-to-requirement mapping.

## Group repeated postings without merging vacancies

Deduplicate repeated captures of the same source ID. In the reading directory,
exact company-and-full-title matches may share one row: list all cities and keep
every distinct posting link, labeled with its city and posting ID. Keep the source
records separate underneath so this display grouping does not merge vacancies or
evidence. Put each posting link on its own line, even when two short labels would
fit side by side. Different posting IDs with the same title and substantially
repeated descriptions are distinct official entries, not proof of independent
vacancies or hiring headcount. Keep their links without inflating the grouped-role
count. If only one city's full description was read, identify that city; its
requirements or verification status do not automatically apply to the others.
Different seniority, product, team or specialization means a different title and
must remain a separate row. For example, Beijing and Shanghai postings named
“AI产品经理（垂类场景）-Aime” can share a row with both links; “高级AI产品经理-飞书多维表格”
and “高级AI产品经理（基础产品方向）-抖音” cannot. State both the grouped-role count and
the underlying posting count. Exclude confirmed closed postings from the entire
client report, including historical appendices, links and count explanations.
Keep those records and their exclusion reasons in the private research log; only
include them in the report if the client specifically requests historical roles.

## The job directory is the source list

Use the job directory and its original posting links as the report's source
list. Do not add a separate source/methodology/scope chapter when that directory
already supplies the links.

Group the job directory by hiring company, keeping that company's roles
consecutive. Use separate company, position, location and original-link columns.
In the PDF, show a shared company name in a visibly merged cell spanning its
roles: internal row dividers must not cross that company cell. If the renderer
cannot merge cells, repeat the full company name on each row. Repeat it in plain
Markdown tables, which have no row spans; do not leave a blank company cell under
a full-width row divider. When a group crosses a page, repeat the company name
on the new page. Preserve each role's full title and distinct links, including
the city/ID grouping rules above. Company grouping does not merge different
roles or imply identical vacancies.

Put the complete directory after the recommendations. Paginate it by the rendered
height of whole entries, including their links, rather than imposing a fixed
number of rows that leaves large blank areas.

## The consultation-report pattern

When following a consultation-report example, preserve: a priority table;
numbered key jobs with consistent “匹配依据 / 经验缺口 / 投递准备” fields; a table
of remaining jobs and tradeoffs; numbered preparation steps; an interview
preparation list/table; and a job directory with company, full title,
location, reading status and usable source links. Use a linked contents list
for a multi-section report. Scale the rows to the actual evidence; never copy
the example's job count or fabricate entries to fill it.

## Keep job identities consistent across sections

Keep job identities consistent across the priority table, detailed sections
and directory. Prefer an unnumbered company-grouped directory: company, full
job title and original link identify the role without an awkward reordered rank
sequence. If the user requests displayed job numbers, retain each number across
sections; do not renumber merely because company grouping changes row order.
If a section promises the key or priority jobs,
its selection and order must follow the stated priority list; put the remaining
jobs in the remaining-jobs section. A deliberately different selection needs a
clear section label and a reason visible to the reader. An internal limit on
how many jobs were mapped is not a reader-facing reason to call lower-priority
jobs the priorities. Check the job identities and numbers, not just the counts.

## Two more questions for the full-report review

Add these to the reader questions in `report-writing.md`, "Review the rendered
report before delivery":

- Do the priority list, key-job section, remaining-job section and directory
  refer to the same jobs, keeping any displayed numbers stable? Check identities
  and order; correct an unexplained mismatch even when all section counts are
  correct.
- Is each role visibly attached to its company? Inspect the rendered group
  boundaries, including page breaks: merge company cells clearly or repeat
  the name, and keep every Markdown row's company identifiable.
