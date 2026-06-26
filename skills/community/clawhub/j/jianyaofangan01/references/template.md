# 简要方案模板参考

## 模板结构

模板为标准 .docx 文件，包含以下要素：

### 封面页
- 标题行：居中、22pt、加粗、颜色 #1E386B
- 日期：居中、16pt、加粗
- 封面与目录之间有分页符

### 自动目录
- 使用 Word 自动目录控件（SDT），用户右键→更新域即可刷新
- **生成脚本不可删除或替换此控件**
- **不可额外添加静态目录文本**

### 正文章节结构
```
一、背景概述（Heading 1）
二、现状分析（Heading 1）
三、问题及需求分析（Heading 1）
    （一）首要需求：XXX（Heading 2）
    （二）主要需求一：XXX（Heading 2）
    （三）主要需求二：XXX（Heading 2）
    （四）次要需求：XXX（Heading 2）
    （四）其他需求：XXX（Heading 2）
四、规划建议（Heading 1）
    （一）XXX（Heading 2）
        工作目标（Heading 3）
        详细工作内容（Heading 3）
        预期收益（Heading 3）
五、预算概要（Heading 1）
    （一）优先建设（Heading 2）
    （二）逐步推进（Heading 2）
    （三）可选模块（Heading 2）
```

### 样式规格
| 样式 | 字号 | 说明 |
|------|------|------|
| Normal | 10.5pt（五号） | 正文 |
| Heading 1 | 16pt（三号） | 一级标题，加粗 |
| Heading 2 | 15pt（小三号） | 二级标题，加粗 |
| Heading 3 | 14pt（四号） | 三级标题，加粗 |

## Python 脚本生成规范

### 环境要求
```bash
pip3 install python-docx
```

### 核心操作

**1. 修改段落文本（保留原有格式）**
```python
def set_para_text(para, text):
    # 保存原格式
    first_run = para.runs[0] if para.runs else None
    font_size = first_run.font.size if first_run else None
    # 清除所有 run
    for r in list(para.runs):
        r._element.getparent().remove(r._element)
    # 添加新 run
    run = para.add_run(text)
    if font_size: run.font.size = font_size
```

**2. 插入新段落**
```python
def insert_para_after(ref_para, text):
    new_p = doc.add_paragraph(text, style='Normal')
    ref_para._element.addnext(new_p._element)
    return new_p
```

**3. 删除段落**
```python
p._element.getparent().remove(p._element)
```

**4. 页面分页**
```python
# 在段落中插入分页符
run = para.add_run()
br = OxmlElement('w:br')
br.set(qn('w:type'), 'page')
run._element.append(br)
```

### 关键注意事项

1. **分页符位置**：必须放在章节标题**之前**的段落上，不可放在标题段落内部
2. **SDT 自动目录**：`body.find(qn('w:sdt'))` 保留，不删除、不修改
3. **标题编号**：章节标题之间的空白段必须是 Normal 样式，不能用 Heading 样式，否则 Word 自动编号错误
4. **段落增删顺序**：批量删除段落时按索引**逆序**进行以保持索引稳定
5. **新段落插入**：使用 `addnext` 在指定段落后插入，保持文档顺序

## 语言风格要点

### 政府公文风格
- 避免口语化："搞""挺""很多""非常" → 用"较为""相对""在一定程度上"
- 用词正式："规划"而非"计划"，"开展"而非"进行"，"拟"而非"打算"
- 引用规范：政策法规用书名号，如《网络安全法》
- 避免主观表述：不用"我们""你们""我觉得"

### IT 术语
- 信创、超融合、主动防御、纵深防护、安全态势感知
- EOL/EOS、WAF、XDR、MSS、SOAR、IAST
- Agent、智能体、渗透测试、漏洞扫描

### 禁用表达
- ❌ "搞定""弄好""很多""挺"
- ❌ "大概""差不多""应该是"
- ❌ "我们""你们"——公文用客观表达

## 模板原文

模板文件由用户提供并存储于飞书知识库，生成脚本读取模板、填充内容后另存为新文件，不可修改原模板。
