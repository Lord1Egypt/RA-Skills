## Description: <br>
Crawls Vietnam nutrition portal food and prepared-dish JSON pages with scrapling-official and uploads each raw provider record to Cloudflare R2 with stable keys and page-level pacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snailb1007](https://clawhub.ai/user/snailb1007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data-ingestion agents use this skill to preserve public nutrition-provider records from the Vietnam nutritional portal and store one raw record per Cloudflare R2 object. It is intended for page-sequential crawling where each page is fetched by scrapling-official, split into provider records, uploaded with stable object keys, and paced to avoid rapid follow-up requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes fetched provider records to Cloudflare R2, so broad credentials or shared buckets can expose or mix stored crawl data. <br>
Mitigation: Use a dedicated bucket or prefix, narrowly scoped R2 credentials, and separate source namespaces for foods and prepared dishes. <br>
Risk: Reruns can duplicate or overwrite objects if the storage layout is not confirmed before a full crawl. <br>
Mitigation: Start with skip-existing, conservative pagination, and stable provider identifiers such as _id or code before expanding the run. <br>
Risk: The skill depends on scrapling-official and provider JSON behavior, so unexpected fetch behavior or response shape changes can affect ingestion quality. <br>
Mitigation: Review the scrapling-official dependency and verify the canonical JSON payload and data array shape before uploading records. <br>


## Reference(s): <br>
- [Source Notes](references/source-notes.md) <br>
- [Vietnam nutrition foods lookup](https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-thuc-pham) <br>
- [Vietnam prepared-dish lookup](https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-mon-an) <br>
- [Observed foods JSON endpoint](https://viendinhduong.vn/api/fe/foodNatunal/getPageFoodData?page=1&pageSize=15&energy=0) <br>
- [Observed prepared-dish JSON endpoint](https://viendinhduong.vn/api/fe/tool/getPageFoodData?page=1&pageSize=15) <br>
- [ClawHub listing](https://clawhub.ai/snailb1007/nutrition-provider-r2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uv, scrapling-official, Cloudflare R2 credentials, stable object keys, per-record uploads, and skip-existing behavior for reruns.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
