# 项目记忆 - IMA 知识库整理

## 用户背景
- IMA 用户名：wowkie
- 关注领域：AI+教育、AI+体育（运动科学）
- 目标：建立结构化知识库，支撑 RAG 检索增强生成，用于撰写个性化文档

## IMA 知识库 ID
- wowkie的知识库：`0019ed21e8806f81`（主知识库，根目录作为"收件箱"）
- 结题知识库：`7453321606477909`（项目知识库）

## 分类体系（6 类）
1. AI+体育 - 运动捕捉、穿戴传感器、体测、赛事AI、竞技训练
2. AI+教育研究 - 教育智能体、学习投入度、作业评估、学生画像、教师转型
3. AI教学工具实操 - 交互式网页制作、部署、数据分析
4. 教育政策文件 - 官方指引、意见、方案、通知
5. AI见解与培训 - 技术观点、趋势分析、培训资源
6. 待清理-无关内容 - 与主题无关的内容

## 自动化任务
- ID: `automation-1785299014871`
- 名称: IMA知识库定期整理
- 频率: 每周日 10:00
- 功能: 扫描新增内容 → 分类 → 更新 tracker.json → 重新生成分类 Word 索引文档 → 生成报告

## IMA API 限制
- 不支持：删除、移动、建文件夹、打标签、重命名知识库
- 支持：列表、搜索、添加知识、导入URL、创建media（上传文件）、获取内容（fetch_media_content）

## 分类索引文档方案（替代物理文件夹）
- 方案：用 Word 索引文档实现"逻辑分类"，不依赖物理文件夹
- 生成脚本：`.workbuddy/ima-tracker/generate_index_docs.py`（python-docx）
- 文档目录：`.workbuddy/ima-tracker/category_docs/`
- 5 个有效分类各一个 .docx 文件，记录标题、来源、导入日期
- RAG 链路：用户指定分类 → 读索引文档获取 media_id → fetch_media_content 拉全文 → 生成文档

## 关键文件
- 追踪文件：`.workbuddy/ima-tracker/tracker.json`
- 文档生成脚本：`.workbuddy/ima-tracker/generate_index_docs.py`（生成后自动复制到用户目录）
- 分类索引文档（工作目录）：`.workbuddy/ima-tracker/category_docs/*.docx`
- 分类索引文档（用户指定目录）：`D:\tuixiu 20240906备份\tuixiu\tui xiu\教学材料\2026-2027（1）数智素养与工具应用\workbuddy\ima知识库检索文档\`
- 整理指南：`IMA知识库整理指南.html`
- 报告目录：`.workbuddy/ima-tracker/reports/`

## Skill 与版权
- Skill 名称：ima-kb-organizer
- Skill 路径：`~/.workbuddy/skills/ima-kb-organizer/`
- 打包文件：`ima-kb-organizer.zip`
- 作者：sus-yugaohe
- 许可协议：CC BY-NC 4.0
- 版本：1.0.0
- 复盘文档：`IMA知识库智能整理_方法论与实践复盘.docx`
- 使用说明：`IMA知识库整理技能_使用说明.docx`
- 上线渠道：ClawHub（https://clawhub.ai/）— GitHub 登录，上传 zip，提交审核（1-3 工作日）
