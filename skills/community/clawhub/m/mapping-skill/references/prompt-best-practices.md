# 最佳提示词实践

本文件用于沉淀 Mapping-Skill 在真实工作流中的高质量提示词模板。每当后续有新的实践文档，都应把可复用的提示词补充到这里。

## 使用原则

一个好的提示词通常会明确：
- 任务目标
- 要使用的脚本或工具
- 输入来源
- 输出格式
- 是否需要导入飞书
- 统计信息要求

---

## 1. OpenReview 论文爬取 + 飞书入表

### 模板

```text
请执行 OpenReview 论文爬取任务：
1. 使用 Mapping-Skill skill 根目录下的 `scripts/openreview_scraper.py` 脚本
2. 初始化爬虫时使用 api2.openreview.net 端点：
   scraper = OpenReviewScraper(
       username='XXXXXXX',
       password='XXXXXXX',
       baseurl='https://api2.openreview.net'
   )
3. 爬取 ICLR2025 的 5 篇论文（测试）+ https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-accept-oral（记着替换链接）
4. 保存 CSV 到 /tmp/ 目录
5. 创建新的飞书多维表格，按照 Mapping-Skill skill 根目录下的 `scripts/openreview_scraper.py` 脚本中爬取的数据来创建相应字段
6. 批量导入数据到多维表格
7. 返回多维表格链接和统计信息
```

### 为什么有效
- 明确要求使用已有脚本
- 指定了测试规模
- 明确了输出路径与飞书目标

---

## 2. CVF 论文爬取 + 邮箱提取 + 飞书入表

### 模板

```text
请执行 CVF 论文爬取任务：
1. 使用 Mapping-Skill skill 根目录下的 `scripts/cvf_paper_scraper.py` 脚本
2. 严格按照脚本中的 extract_emails_from_text() 函数提取邮箱
3. 爬取 ICCV2025 的 5 篇论文（测试）+ https://openaccess.thecvf.com/ICCV2025?day=all（记着替换链接）
4. 保存 CSV 到 /tmp/ 目录
5. 创建新的飞书多维表格，按照 Mapping-Skill skill 根目录下的 `scripts/cvf_paper_scraper.py` 脚本中爬取的数据来创建相应字段
6. 批量导入数据到多维表格
7. 返回多维表格链接和邮箱提取统计
```

### 为什么有效
- 把关键邮箱提取逻辑锁定到已有函数
- 避免模型自己发明不稳定的 PDF 提取方式

---

## 3. 飞书表格批量写邮件

### 模板

```text
请执行论文作者邮件生成任务：
【数据源】
表格链接：
【第一步：解析表格链接】
1. 从链接中提取 app_token（格式：/base/{app_token}）
2. 调用 feishu_bitable_app_table 的 list 接口获取 table_id
3. 验证表格可访问性
【第二步：分批读取论文数据】
1. 使用 feishu_bitable_app_table_record 的 list 操作
2. 分批读取（每批50条），使用 page_token 分页
3. 只提取必要字段：记录ID、论文标题、作者、邮箱、机构
4. 过滤条件：只处理有邮箱的记录
【第三步：确定研究领域】
1. 读取 Mapping-Skill skill 根目录下的 `references/field-mappings.md`
2. 根据论文标题和关键词，使用映射规则确定研究领域
3. 示例：
   - "Symmetry Understanding of 3D Shapes" → Computer Vision
   - "Efficient Adaptation of Vision Transformer" → NLP
【第四步：生成个性化邮件】
1. 读取 Mapping-Skill skill 根目录下的 `references/email-templates.md`
2. 根据研究领域选择对应模板（共22个领域）
3. 填充占位符：
   - {{researcher_name}} → 第一作者姓名
   - {{context_affiliation}} → 机构
   - {{research_field}} → 研究领域
   - {{technical_hook}} → 基于论文标题生成
   - {{talk_track_paragraph}} → 从 talk-tracks.md 选择
【第五步：批量更新多维表格】
1. 在多维表格中创建新字段："推荐邮件"（多行文本）
2. 使用 batch_update 批量更新每条记录
3. 每批最多 500 条
【第六步：验证和统计】
1. 验证邮件内容个性化
2. 返回统计：总计 X 条 / 成功 Y 条 / 失败 Z 条
3. 列出失败原因
【输出】
- 多维表格链接
- 生成统计
- 失败原因列表
```

### 为什么有效
- 把读表、映射、生成、回写拆成了明确阶段
- 降低了模型漏步骤的概率

---

## 4. 给定 URL 的全量人员信息抽取

### 模板

```text
1、请你调用BrightData-MCP工具，或者编写爬虫脚本，爬取 <某网站URL> 页面中的所有人员信息。
2、提取信息包括中文名，英文名，个人介绍信息、学术方向、学校和专业信息、工作经历、近期论文著作信息（包含论文名和论文链接）、github链接、个人主页链接、谷歌学术链接、领英链接、知乎链接、B站链接、邮箱等。
3、当前页面缺少邮箱的话，需要进入学者主页或论文链接页面，从里面提取作者们的邮箱。
4、保存到csv文件，然后将csv导入飞书多维表格。
```

### 为什么有效
- 定义了完整字段范围
- 指出了邮箱的二跳补全要求
- 明确了最终交付物是 CSV + 飞书多维表格

---

## 后续补充规则

每次新增最佳提示词时，建议附带：
- 适用场景
- 为什么有效
- 容易失败的点
- 是否依赖 OpenClaw / 飞书 / BrightData / 特定脚本
