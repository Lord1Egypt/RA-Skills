# 日语会话作业批改 - 详细流程

## 适用场景
- 学生提交音频文件（MP3/MP4/M4A/WAV）作为日语会话作业
- 教师按SKILL能力评估体系完成：文件下载 → 音频转写 → 维度化评分 → 成绩录入 → 汇总上传全流程

---

---

## Step 1：下载学生提交文件
### 核心目标
按SKILL数据标准化要求，获取学生作业文件及关联身份信息，为后续评估建立基础数据链路

### 命令
```bash
python3 scripts/download_audio_submissions.py COURSE_ID ASSIGNMENT_ID
```

### 流程（SKILL数据规范对齐）
1. 读取 config.json 获取 Canvas API Token（符合SKILL接口鉴权规范）
2. 调用API：GET /courses/:id/assignments/:id/submissions?include[]=attachments,user
 - 过滤仅保留音频/视频类附件（符合SKILL作业文件类型白名单）
3. 按SKILL文件存储规范，将文件下载到本地 `/tmp/canvas_audio_CID_AID/[学号]/[作业类型]/` 目录
4. 生成标准化 `submission_map.json`（SKILL数据字段要求）：
 ```json
 {
 "user_id": "Canvas用户ID",
 "student_id": "学号",
 "name": "姓名",
 "file_name": "原始文件名",
 "local_path": "本地存储路径",
 "file_type": "音频/视频（SKILL分类）",
 "assignment_id": "作业ID",
 "course_id": "课程ID"
 }
 ```

### 输出（符合SKILL数据格式）
- 结构化音频文件存储目录（按学号/作业类型分层）
- 标准化 submission_map.json（含SKILL要求的核心关联字段）

---

## Step 2：Whisper 音频转写（SKILL转写规范）
### 预处理规则（SKILL媒体处理标准）
| 文件格式 | 处理方式（符合SKILL音频编码规范） |
|----------|----------------------------------|
| MP4（视频）| ffmpeg 转换为 WAV（16kHz/16bit/单声道）再转写 |
| MP3/M4A/WAV | 校验编码格式，非16kHz则转码后再转写 |

### 转换 + 转写命令
```bash
# 视频/非标准音频 → SKILL标准WAV
ffmpeg -y -i "input.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/[学号]_audio.wav

# Whisper 语音转文字：
 - 使用 medium 模型，固定不切换，不可替换 tiny/base/large 等其他
 - 输出纯文本文件
 - 异常处理规则：
 - 音频损坏/空文件/无法识别 → 标记「转写失败」
 - 自动移入 `./error_audio/`，触发人工复核
 - 跳过自动评分，不直接判定低分
```

### 输出
- 转写文本文件命名：`[学号]_[作业ID]_transcript.txt`
- 文本格式：逐句分行，标注关键发音时间戳（满足SKILL发音评估溯源要求）

---

## Step 3：基于SKILL体系逐题评分
### SKILL评分维度（CAF三维框架，每题满分10分）
| SKILL维度 | 权重 | 评估要点（贴合SKILL能力指标） |
|-----------|------|--------------------------------|
| C 复杂性（Complexity） | 80% | 内容贴合与表达复杂度 |
| A 准确性（Accuracy） | 10% | 语法、词汇、语音规范 |
| F 流利度（Fluency） | 10% | 话语输出节奏、连贯性、停顿与沉默控制容 |

### 总分计算（SKILL分数换算规则）
总分 = 各题得分之和 ÷ 题目数（换算为满分10分，保留1位小数，符合SKILL分数展示规范）

### 等级划分（与SKILL能力等级映射）
| SKILL等级 | 分数区间 | 能力描述（对齐SKILL日语会话等级） |
|-----------|----------|------------------------------------|
| 优秀（Proficient） | 8.0 ~ 10.0 | 完全符合SKILL高阶会话能力要求，可流畅完成目标场景沟通 |
| 良好（Competent） | 6.0 ~ 7.9 | 符合SKILL中阶会话能力要求，核心沟通无明显障碍 |
| 合格（Basic） | 4.0 ~ 5.9 | 达到SKILL基础会话能力要求，可完成核心信息传递 |
| 需加强（Developing） | < 4.0 | 未达到SKILL基础会话能力要求，需针对性强化核心能力 |

### 输出格式（SKILL标准化评语模板）
```markdown
## [学生姓名]（[学号]）| SKILL日语会话作业评估

### 【逐题评分（SKILL维度）】
**问题1：** [题目内容]
> **学生回答：** [转写文本]
 X/10分 — 扣分原因（关联SKILL维度：如「内容准确性未达SKILL场景应答规范」）

### 【SKILL总分】X/10 | 等级：[SKILL等级]

**SKILL能力亮点：**
- [贴合SKILL维度的优点，如「发音符合SKILL日语发音标准，核心单词无错误」]

**SKILL能力待提升点：**
- [关联SKILL维度的问题，如「语法未符合SKILL中阶语法规范，存在助词使用错误」]
- [关联SKILL维度的问题，如「回答完整性未达SKILL场景应答要求，缺失关键信息」]

**SKILL针对性巩固建议：**
1. [贴合SKILL提升路径，如「强化SKILL语法分级中N3级助词使用规则，完成5个场景专项练习」]
2. [贴合SKILL提升路径，如「按SKILL发音标准，跟读核心单词音频并录制对比，纠正音近错误」]
```

---

## Step 4：录入 Canvas 成绩（SKILL数据同步规范）
### 核心目标
将SKILL评分结果同步至Canvas，确保成绩/评语符合SKILL数据上报要求

### 命令（SKILL标准化调用）
```bash
# 直接传入SKILL标准化评语
python3 scripts/grade_submission.py COURSE_ID ASSIGNMENT_ID USER_ID GRADE --comment "[SKILL标准化评语内容]"

# 读取SKILL格式评语文件
python3 scripts/grade_submission.py COURSE_ID ASSIGNMENT_ID USER_ID GRADE --comment-file [学号]_SKILL_comment.txt
```

### API 调用（符合SKILL数据传输规范）
PUT /courses/:id/assignments/:id/submissions/:user_id
Content-Type: application/x-www-form-urlencoded
```
submission[posted_grade]=[SKILL换算后分数]
comment[text_comment]=[完整SKILL评估评语]
comment[attempt]=1
comment[external_tool_comment]=SKILL日语会话作业评估（标记SKILL体系来源）
```

---

## Step 5：上传SKILL汇总表到个人文件空间
### 核心目标
按SKILL报表规范生成汇总表，完成标准化上传及链接输出

### 命令（SKILL报表上传规范）
```bash
python3 scripts/send_summary_message.py [--docx PATH]
```
- 默认读取 `Generated_Document/[课程ID]_SKILL日语会话作业汇总表.docx`（SKILL报表命名规范）
- 汇总表字段：学号、姓名、SKILL总分、SKILL等级、核心能力亮点、主要待提升点（贴合SKILL报表模板）
- 上传到发件人的个人文件空间（POST /users/:id/files），按SKILL要求设置文件权限为`private`
- 输出符合SKILL链接规范的文件下载地址

### API 调用（SKILL文件上传标准）
1. POST /users/:id/files
 参数（SKILL必填）：
 ```
 name: [课程ID]_SKILL日语会话作业汇总表.docx
 size: [文件大小]
 content_type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
 parent_folder_id: [SKILL指定文件目录ID]
 ```
2. 接收返回的 upload_url, upload_params, id
3. multipart/form-data POST 到 S3

---

## Canvas API 关键参数（SKILL适配版）
| 用途 | 端点 | 核心参数（SKILL扩展） |
|------|------|-----------------------|
| 下载提交含附件 | GET /courses/:id/assignments/:id/submissions | include[]=attachments,user<br>filter[file_type]=audio,video（SKILL文件过滤） |
| 评分+评语 | PUT /courses/:id/assignments/:id/submissions/:uid | submission[posted_grade]（SKILL换算分数）<br>comment[text_comment]（SKILL标准化评语）<br>comment[external_tool_comment]=SKILL评估（标记来源） |
| 上传到个人文件空间 | POST /users/:id/files | name（SKILL命名规范）<br>size, content_type<br>parent_folder_id（SKILL指定目录） |
