# music-education-research-writer

## Skill 简介

`music-education-research-writer` 是一个面向社科类学术研究与学术论文写作的标准化 Skill，重点服务以下研究方向：

- 音乐研究
- 教育研究
- 音乐教育交叉研究
- AI + 音乐教育研究
- 高中音乐课程、音乐审美、音乐创作教学、人机协作音乐创作等应用型研究

它不鼓励“直接一键生成整篇论文”，而是聚焦论文最关键、最有研究含量的前期模块：

1. 文献综述
2. 理论框架 / 概念模型 / 分析模型建构
3. 研究空白识别

## 适用场景

适合以下需求：

- 基于用户已有文献与笔记生成结构化文献综述
- 从论文、政策、课堂观察、问卷、访谈中提炼理论观念与变量关系
- 识别研究对象、研究场景、研究方法、理论整合、数据类型等方面的空白
- 为开题报告、核心期刊论文、课程研究或课堂实践研究提供前期论证
- 帮助中国语境下的音乐教育研究形成“问题意识 + 理论贡献 + 方法严谨性 + 中国教育情境”的论文基础

## 安装方式

### 方式 1：直接使用本地文件夹

将整个 `music-education-research-writer/` 文件夹放入你的 Skills 目录或待上传目录中。

### 方式 2：使用压缩包

可直接使用：

- `music-education-research-writer.zip`
- `music-education-research-writer.skill`

其中 `.skill` 本质上是保留根目录结构的 ZIP 包，只是扩展名改为 `.skill`。

## 文件结构

```text
music-education-research-writer/
├── SKILL.md
├── README.md
├── references/
│   ├── workflow.md
│   ├── evidence_hierarchy.md
│   ├── social_science_methods.md
│   ├── music_education_ontology.md
│   ├── literature_review_principles.md
│   ├── theory_modeling_guide.md
│   ├── research_gap_taxonomy.md
│   └── ima_integration.md
├── templates/
│   ├── literature_review_template.md
│   ├── theory_model_template.md
│   ├── research_gap_matrix_template.md
│   ├── opening_report_argument_template.md
│   ├── journal_article_outline_template.md
│   ├── classroom_practice_research_design_template.md
│   ├── evidence_chain_table_template.md
│   └── literature_concept_theory_method_gap_map.md
├── examples/
│   ├── example_ai_music_education_review.md
│   ├── example_large_corpus_triage.md
│   ├── example_theory_model.md
│   └── example_research_gap_matrix.md
├── tests/
│   ├── sample_user_request.md
│   ├── sample_large_corpus_request.md
│   ├── sample_corpus_notes.md
│   ├── expected_output_checklist.md
│   └── pre_publish_checklist.md
├── scripts/
│   ├── validate_skill.py
│   └── package_skill.py
└── dist/
    ├── music-education-research-writer.zip
    └── music-education-research-writer.skill
```

## 如何准备 iMA 导出材料

这个 Skill 不伪造 iMA API，也不会假设 iMA 一定存在正式接口。推荐做法是把 iMA 中的材料导出到本地文件夹，再交给 Skill 分析。

推荐目录结构：

```text
research_corpus/
├── literature/
├── policy/
├── notes/
├── observations/
├── interviews/
├── questionnaires/
└── manifest.md
```

推荐准备内容：

- PDF 文献
- Word 文档
- Markdown 笔记
- TXT 摘录
- 微信公众号导出文章
- 课堂观察记录
- 研究日志
- 问卷结果
- 访谈材料
- 政策与课程标准文本

推荐 `manifest.md` 字段：

- `source_id`
- `file_name`
- `source_type`
- `origin`
- `verification_status`
- `notes`

## 如何准备本地 research_corpus 文件夹

如果你不用 iMA，也可以直接准备本地 `research_corpus/` 文件夹。建议：

1. 按资料类型建子文件夹。
2. 给每份资料编一个稳定 ID，例如 `A01`、`B03`、`D02`。
3. 把未核验材料标记为 `待核验`。
4. 将课堂观察、问卷、访谈与正式文献分开。
5. 如果是中文核心期刊写作，尽量单独放一个 `core_journals/` 或在 `manifest.md` 中注明 CSSCI / 北大核心属性。

## 示例调用语句

```text
请基于我提供的 research_corpus 文件夹，先帮我做一份关于“AI辅助高中音乐创作教学中的人机协作机制”的文献综述结构表，再生成可扩写段落，并给出证据链追踪表。
```

```text
我有一些 CSSCI 论文、课程标准、课堂观察记录和学生问卷。请不要直接代写全文，先帮我建立理论框架、概念模型和研究空白矩阵。
```

```text
请读取我导出的 iMA 笔记、微信文章摘录和本地 PDF 文献，区分证据等级，判断哪些结论可以写进开题报告，哪些还需要补充文献。
```

## 输出示例

Skill 的典型输出包含：

- 研究任务诊断
- 研究框架表
- 证据等级与证据链表
- 文献综述结构表
- 可扩写综述段落
- 理论模型 / 分析框架 / 论文写作模型
- 研究空白矩阵
- `需要补充的文献清单`
- 材料筛选与优先处理建议

可参考：

- [example_ai_music_education_review.md](./examples/example_ai_music_education_review.md)
- [example_theory_model.md](./examples/example_theory_model.md)
- [example_research_gap_matrix.md](./examples/example_research_gap_matrix.md)
- [example_large_corpus_triage.md](./examples/example_large_corpus_triage.md)

## Token 高效使用说明

这个 Skill 默认不会一次性生成超长论文内容，也不会默认穷尽式总结所有材料。

默认行为是：

1. 先判断
2. 再筛选
3. 再建框架
4. 再局部扩写
5. 最后才生成正文

默认采用 `Standard Mode`。

你可以这样切换模式：

- `请用 Brief Mode 快速判断。`
- `请用 Standard Mode 输出结构化分析。`
- `请用 Deep Mode 展开成论文正文。`

当用户材料很多时，Skill 会先做：

- 材料总览
- 材料分类
- 高相关材料清单
- 可暂缓材料清单
- 优先处理建议

而不会默认把所有材料全部深度分析。这样可以减少 token 浪费，同时提高学术研究效率。

## 学术诚信声明

本 Skill 明确禁止以下行为：

- 伪造作者
- 伪造年份
- 伪造期刊
- 伪造 DOI
- 伪造政策文件
- 用“看似学术”的语言掩盖证据不足
- 把公众号文章、课堂笔记、个人经验伪装成同行评审结论
- 输出不可追溯引用

本 Skill 允许帮助用户形成段落，但必须说明依据来自哪里，并在证据不足时输出 `需要补充的文献清单`。

如果用户要求直接生成整篇论文，应先建议拆解为：

1. 综述
2. 理论
3. 方法
4. 数据
5. 讨论

## 安全声明

这是一个面向学术研究写作的 Skill，不应申请过多权限。

禁止：

- 自动读取用户全盘文件
- 自动上传文件
- 自动联网下载不明脚本
- 自动执行 shell 命令
- 自动读取 API key / token / cookies / 浏览器数据

允许：

- 读取用户明确提供的文件夹
- 读取用户导出的文献笔记
- 读取用户明确放入 `research_corpus` 的资料
- 生成 Markdown、表格、研究框架、模型说明、研究问题建议
- 生成证据链追踪表

## 如何打包成 zip / .skill 文件

### 先运行校验

```bash
python3 scripts/validate_skill.py .
```

### 方式 A：打包为普通 ZIP

```bash
python3 scripts/package_skill.py . --format zip
```

生成：

```text
dist/music-education-research-writer.zip
```

### 方式 B：打包为 ClawHub / OpenClaw 风格 .skill 包

```bash
python3 scripts/package_skill.py . --format skill
```

生成：

```text
dist/music-education-research-writer.skill
```

### 同时生成两种格式

```bash
python3 scripts/package_skill.py . --format both
```

## 如何提交到 SkillHub / ClawHub

建议提交流程：

1. 运行 `python3 scripts/validate_skill.py .`
2. 确认 `tests/pre_publish_checklist.md` 中所有项目都通过
3. 生成 `.zip` 或 `.skill`
4. 检查压缩包内是否保留根目录 `music-education-research-writer/`
5. 检查 `SKILL.md` frontmatter 是否只包含 `name` 和 `description`
6. 检查示例、模板、参考文档是否齐全
7. 检查 Token Efficiency Protocol 是否已落实到 SKILL、模板、示例与测试文件
8. 在 SkillHub / ClawHub 的发布页填写名称、简介、标签与说明
9. 上传 `music-education-research-writer.zip` 或 `music-education-research-writer.skill`
10. 在发布说明中注明：本 Skill 不联网抓取、不伪造文献、依赖用户提供语料

## 本地创建文件的命令

如果你想从零创建同名目录，可用：

```bash
mkdir -p music-education-research-writer/{references,templates,examples,tests,scripts,dist}
```

如果你想直接打包当前目录：

```bash
cd music-education-research-writer
python3 scripts/validate_skill.py .
python3 scripts/package_skill.py . --format both
```
