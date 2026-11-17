# 已核验的来源流程（补充档案）

本文件记录**已由真实查询验证过**的入口、参数与页面结构，供下次直接复用。这些入口尚未写成站点档案，优先级等同 `references/sites/` 的已验证步骤。

使用时照本文件给的 URL 与控件直接操作；本文件记录的**障碍**（IP 授权、连接超时、需登录）是实测结果，不要假设重试就能过。

## COAJ 中国开放获取期刊数据库

- 入口：https://coaj.cn/
- 高级搜索：https://coaj.cn/search/advance
- “引用参考文献”（Cited References）检索栏共 **8 个字段**：
  引用作者、引用标题、引用年份、引用卷、引用期、引用起始页、引用结束页、引用资源。
- 页面结构：`文章` 与 `引用参考文献` 两个 tab；后者用 `el-select` + `el-input`，提交后跳
  `/search/reference?references=<encodeURIComponent(JSON)>`。
- 结果页：`/search/article?advanced=<encodeURIComponent(JSON)>`。

## 重庆图书馆集群数字图书馆（InDigLib）

- 可用入口：`http://113.207.111.42:9001/InDigLib/frontV2/SearchIndex!simple.action?opacType=local`
- 检索控件：`#select1`（任意词/ISBN/控制号/题名/作者/主题/分类号/索取号/出版年/出版社/语种）、
  `#text1`（检索词）；回车提交，结果页为
  `http://113.207.111.42:9001/InDigLib/OpacMarcSearchSolr!simpleSearch.action`。
- 结果页 facest：通借通还馆藏 / 本馆馆藏、所属馆、文献类型、著者、出版日期、分类。
- 注意：
  - 主入口 `http://222.177.237.197:8080/InDigLib/...` 从当前网络 **连接超时**；
  - `113.207.111.42:9001` 当前“本馆”范围为重庆少年儿童图书馆，查不到重庆图书馆主馆馆藏；
  - 该库对 IP 授权敏感，未授权时页面底部提示“您的 IP 地址 … 不在系统授权范围内”。

## 万方（补充）

- 期刊统计页：`https://c.wanfangdata.com.cn/magazine/<刊名拼音码>?tabId=analysis`
  （如《红外与毫米波学报》`hwyhmb`），可读“发文热度/文献量”。
- 年份分面：`https://s.wanfangdata.com.cn/paper?q=刊名:"<刊名>"`，结果页“年份”分面直接给出各年篇数。
- 学位论文阅读器：`https://f.wanfangdata.com.cn/online/pc/thesis/<id>`；
  左侧目录点击可跳章，正文表格文本可直接读取。
  其 URL 的 `transaction` 查询串含 `iploginservice`，**不是**登录页。

## 中科 VIPExam 考试库（补充）

- 入口：`http://lib.vipexam.org/`（https 证书无效）。
- 分类树：`POST http://lib.vipexam.org/web/getCouresTypeAll`（无需登录）。
- 试卷列表/套数：`POST http://lib.vipexam.org/exam/getExamListByTypeCode`
  （参数 `typeCode`、`totalDate`、`examstyle`、`page`、`limit`；需登录且 IP 在授权范围）。
- 分类 ID：职业资格 `ve05`、导游资格 `ve05013`、导游基础 `ve05013001`、
  导游实务 `ve05013002`、地方导游基础 `ve05013004`。

## 探测方法

对 SPA 站点先做静态侦察，能省掉大量点击。用 `curl` 取 HTML，再从里找接口线索：

```bash
curl -sL --max-time 20 -A "Mozilla/5.0" "https://example.com/page" | grep -oE '(RequestJson|fetch\(|axios\.|/api/[a-zA-Z0-9_/-]+|\.action|\.do)' | sort -u | head -40
```

拿到候选接口后，按接口名单独 `curl` 试一次，看是否直接返回 JSON —— 能返回就用 API，省掉整套点击。

静态侦察只扫首屏 HTML 与引用的脚本，**懒加载 chunk 里的接口可能漏掉**。漏掉时用浏览器点开对应功能，再：

```bash
playwright-cli -s=ilradar snapshot      # 看当前 DOM 结构
playwright-cli -s=ilradar network       # 看实际发出的请求，直接拿到接口地址
```

`network` 是补静态侦察盲区最直接的手段。
