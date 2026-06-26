---
name: huo15-doc-template / 火一五文档模板
description: 【版权：青岛火一五信息科技有限公司 账号：huo15】Word/文档生成首选技能。触发词：写word、写文档、写个文档、重新写、重新生成、生成word、生成文档、创建word、创建文档、导出word、导出文档、下载word、下载文档、.docx、word文档、Word文档、写合同、写报价单、写说明书、写会议纪要、合同模板、报价单模板、文档模板、公司文档、正式文档、公文、标书、方案文档、年度报告、通知、请示、报告、函。所有 Word 文档、.docx 文件、公文、合同、报价单、说明书、会议纪要、发货单、PDA 单据等文档生成任务自动使用本技能。
---

## 重要：此为首选文档技能
所有 Word 文档生成任务都必须使用此技能


## ⚠️ 强制检查清单（生成文档前必须完成）

> **新用户必读！每次生成文档前对照检查，否则文档不合格！**

- [ ] **LOGO 是否添加？** —— 页眉必须有 LOGO + 公司名称 + 底线
- [ ] **页码是否添加？** —— 页脚必须有"第 X 页 共 Y 页"
- [ ] **字体是否正确？** —— 正文仿宋，标题黑体/楷体
- [ ] **页面边距是否正确？** —— 上下 3.7/3.5cm，左右 2.8/2.6cm
- [ ] **命名是否规范？** —— 文档类型_客户名称_日期.docx

**如果没有完成以上检查，文档不允许交付！**

---

## 🚀 快速开始

> **重要**：代码模板直接写在 SKILL.md 中，复制使用即可！无需 pip install！

```python
# 一步创建符合公司规范的文档
doc = create_formatted_doc(
    title="销售合同",
    company_name="青岛火一五信息科技有限公司",
    insert_vision=True  # 可选：插入公司愿景理念
)
doc.add_paragraph("合同正文内容...")
doc.save("CONTRACT_客户名_20250319.docx")
```

> **LOGO/公司信息会自动从公司系统获取**，无需手动配置！

---

# 文档模板技能

## 快速开始

1. **字体设置**：默认使用仿宋，小四（12pt）
2. **页面边距**：上下 3.7/3.5cm，左右 2.8/2.6cm
3. **页眉**：LOGO + 公司名称 + 底线
4. **页脚**：页码居中，格式"第 X 页 共 Y 页"，仿宋小四

---

## 配置规则

### 字体规范
- **默认正文**：仿宋，小四（12pt）
- **一级标题**：黑体，小三（15pt），加粗
- **二级标题**：楷体，小四（12pt），加粗
- **三级标题**：仿宋，小四（12pt），加粗

**WPS 字体兼容**：
- 汉字字体：使用 `仿宋`
- 每个 run 都要设置字体域 `w:eastAsia`

---

## ⚠️ 重要：Markdown 语法转换规则

### 禁止直接在 Word 中使用 Markdown 语法

**严禁将 Markdown 语法直接写入 Word 文档**，例如：
- ❌ 错误：`**加粗文本**` → Word 中会显示星号
- ❌ 错误：`| 列1 | 列2 |` → Word 中会显示管道符
- ❌ 错误：`# 一级标题` → Word 中会显示井号

### 正确转换方法

#### 1. 加粗转换
- Markdown：`**这是加粗**`
- Word：设置 `run.bold = True`

```python
# 错误示例（不要这样写！）
p = doc.add_paragraph("**这是加粗**")  # ❌ 会显示星号

# 正确示例
p = doc.add_paragraph("这是加粗")
p.runs[0].bold = True  # ✅ 真正加粗
```

#### 2. 表格转换
- Markdown：
```
| 列1 | 列2 | 列3 |
|------|------|------|
| 内容 | 内容 | 内容 |
```
- Word：使用 `doc.add_table()` 创建表格

```python
# 正确示例
table = doc.add_table(rows=2, cols=3)
table.style = 'Table Grid'

# 设置表头
header_cells = table.rows[0].cells
header_cells[0].text = "列1"
header_cells[1].text = "列2"
header_cells[2].text = "列3"

# 设置表头样式
for cell in header_cells:
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.name = '黑体'
            run.font.size = Pt(12)
```

#### 3. 标题转换
- Markdown：`# 一级标题`
- Word：添加段落并设置样式

```python
# 正确示例
p = doc.add_paragraph("一级标题")
p.runs[0].bold = True
p.runs[0].font.name = '黑体'
p.runs[0].font.size = Pt(15)
```

### 自检清单（生成文档前必查）

生成文档后，检查以下内容：
- [ ] 文档中是否有 `**`、`__`、`#` 等 Markdown 符号？
- [ ] 表格是否使用了 `|` 管道符？
- [ ] 链接是否显示了 `[文字](URL)` 格式？
- [ ] 列表是否显示了 `-` 或 `*` 前缀？

**如果有任何一项为"是"，则文档不合格，需要重新生成**

---

## 🚀 核心函数（必须使用）

### 公司信息获取函数

```python
import ssl
import json
import os
import urllib.request
import xmlrpc.client

# ============== 公司信息配置 ==============
USER_HOME = os.path.expanduser("~")
LOGO_DIR = os.path.join(USER_HOME, ".huo15", "assets")
DEFAULT_LOGO_PATH = os.path.join(LOGO_DIR, "logo.png")

# 备用 LOGO URL
FALLBACK_LOGO_URL = 'https://tools.huo15.com/uploads/images/system/logo-colours.png'
COMPANY_LOGO_URL = 'https://huihuoyun.huo15.com/web/image/website/1/logo'

def get_company_info_from_system():
    """
    从公司系统(Odoo)获取公司信息
    返回: dict {
        'company_name': str,
        'logo_path': str,
        'vision': str,      # 公司愿景
        'philosophy': str,  # 公司理念
        'slogan': str        # slogan
    }
    """
    company_info = {
        'company_name': '青岛火一五信息科技有限公司',
        'vision': '推动B端用户向全场景人工智能机器人转变',
        'philosophy': '打破信息孤岛，用一套系统驱动企业增长',
        'slogan': '',
        'logo_path': None
    }
    
    # 1. 尝试从公司系统获取
    try:
        # 读取 Odoo 配置
        agent_id = os.environ.get('OC_AGENT_ID', 'main')
        agents_dir = os.path.expanduser('~/.openclaw/agents')
        creds_file = os.path.join(agents_dir, agent_id, 'odoo_creds.json')
        
        if os.path.exists(creds_file):
            with open(creds_file, 'r') as f:
                creds = json.load(f)
            
            # 获取全局配置
            openclaw_cfg_file = os.path.expanduser('~/.openclaw/openclaw.json')
            if os.path.exists(openclaw_cfg_file):
                with open(openclaw_cfg_file, 'r') as f:
                    cfg = json.load(f)
                    odoo_env = cfg.get('skills', {}).get('entries', {}).get('huo15-odoo', {}).get('env', {})
                    url = odoo_env.get('ODOO_URL', 'https://huihuoyun.huo15.com')
                    db = odoo_env.get('ODOO_DB', 'huo15_prod')
                user = creds.get('user', '')
                password = creds.get('password', '')
                
                if user and password:
                    # 连接 Odoo
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    
                    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
                    uid = common.authenticate(db, user, password, {})
                    
                    if uid:
                        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
                        
                        # 获取公司配置 (res.company)
                        company_data = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                            [[('id', '=', 1)]], {'fields': ['name', 'logo'], 'limit': 1})
                        
                        if company_data:
                            company_info['company_name'] = company_data[0].get('name', company_info['company_name'])
                            logo_id = company_data[0].get('logo')
                            if logo_id:
                                # 下载 LOGO
                                logo_url = f'{url}/web/image/res.company/{logo_id}/logo'
                                ensure_logo_downloaded(logo_url, DEFAULT_LOGO_PATH)
                                company_info['logo_path'] = DEFAULT_LOGO_PATH
                        
                        # 获取系统参数 (ir.config_parameter) - 愿景/理念
                        vision_config = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                            [[('key', '=', 'huo15.company.vision')]], {'fields': ['value'], 'limit': 1})
                        if vision_config and vision_config[0].get('value'):
                            company_info['vision'] = vision_config[0]['value']
                        
                        philosophy_config = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                            [[('key', '=', 'huo15.company.philosophy')]], {'fields': ['value'], 'limit': 1})
                        if philosophy_config and philosophy_config[0].get('value'):
                            company_info['philosophy'] = philosophy_config[0]['value']
                        
                        slogan_config = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                            [[('key', '=', 'huo15.company.slogan')]], {'fields': ['value'], 'limit': 1})
                        if slogan_config and slogan_config[0].get('value'):
                            company_info['slogan'] = slogan_config[0]['value']
        else:
            # 无凭证，使用备用 LOGO
            ensure_logo_downloaded(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
            company_info['logo_path'] = DEFAULT_LOGO_PATH
    except Exception as e:
        print(f"获取公司信息失败，使用默认信息: {e}")
        # 备用：下载默认 LOGO
        ensure_logo_downloaded(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
        company_info['logo_path'] = DEFAULT_LOGO_PATH
    
    # 确保 LOGO 存在
    if not company_info['logo_path'] or not os.path.exists(company_info['logo_path']):
        ensure_logo_downloaded(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
        company_info['logo_path'] = DEFAULT_LOGO_PATH
    
    return company_info

def ensure_logo_downloaded(url, dest_path):
    """确保 LOGO 已下载"""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return dest_path
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✓ LOGO 已下载: {dest_path}")
    except Exception as e:
        print(f"⚠ LOGO 下载失败: {e}")
        # 尝试备用 URL
        try:
            urllib.request.urlretrieve(FALLBACK_LOGO_URL, dest_path)
            print(f"✓ 备用 LOGO 已下载: {dest_path}")
        except:
            pass
    return dest_path
```

### 字体设置函数

```python
def set_chinese_font(run, font_name='仿宋', font_size=12, bold=False):
    """
    设置中文字体，确保WPS和Word兼容
    必须对每个run都调用此函数！
    """
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.bold = bold
    return run
```

### 页眉函数（含 LOGO + 公司名称 + 底线）

```python
def add_header_with_logo(doc, logo_path=None, company_name=None):
    """添加页眉：LOGO + 公司名称 + 底线"""
    if logo_path is None or company_name is None:
        info = get_company_info_from_system()
        logo_path = logo_path or info.get('logo_path') or DEFAULT_LOGO_PATH
        company_name = company_name or info.get('company_name', '青岛火一五信息科技有限公司')
    
    section = doc.sections[0]
    header = section.header
    header.paragraphs.clear()
    section.header_distance = Cm(1.5)
    
    # 添加 LOGO + 公司名称
    paragraph = header.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # 添加 LOGO
    if os.path.exists(logo_path):
        try:
            run = paragraph.add_run()
            run.add_picture(logo_path, height=Cm(1.0))
        except:
            pass
    
    # 添加公司名称
    run = paragraph.add_run(f' {company_name}')
    set_chinese_font(run, '黑体', 10)
    
    # 添加底线
    pPr = OxmlElement('w:pPr')
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)
    paragraph._element.insert(0, pPr)
    
    return header
```

### 页脚函数（页码）

```python
def add_footer_with_page_numbers(doc):
    """添加页脚：第 X 页 共 Y 页"""
    section = doc.sections[0]
    section.footer_distance = Cm(1.5)
    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    for text, is_field in [("第", False), ("PAGE", True), ("页 共", False), ("NUMPAGES", True), ("页", False)]:
        run = paragraph.add_run(text)
        set_chinese_font(run, '仿宋', 12)
        if is_field:
            fldChar1 = OxmlElement('w:fldChar')
            fldChar1.set(qn('w:fldCharType'), 'begin')
            instrText = OxmlElement('w:instrText')
            instrText.text = text
            fldChar2 = OxmlElement('w:fldChar')
            fldChar2.set(qn('w:fldCharType'), 'end')
            run._element.clear()
            run._element.append(fldChar1)
            run._element.append(instrText)
            run._element.append(fldChar2)
```

### 创建文档主函数

```python
def create_formatted_doc(title="", logo_path=None, company_name=None, insert_vision=False):
    """
    🚀 一条命令创建符合公司规范的 Word 文档
    
    参数:
        title: 文档标题（可选）
        logo_path: LOGO 图片路径（可选，默认自动获取）
        company_name: 公司名称（可选，默认自动获取）
        insert_vision: 是否在公司名称后插入愿景理念（可选，默认False）
    
    返回:
        doc: python-docx Document 对象
    
    使用示例:
        doc = create_formatted_doc("销售合同")
        doc.add_paragraph("合同正文内容...")
        doc.save("CONTRACT_客户_20250319.docx")
    """
    # 1. 创建文档
    doc = Document()
    
    # 2. 设置页面边距（GB/T 9704-2012）
    for section in doc.sections:
        section.top_margin = Cm(3.7)
        section.bottom_margin = Cm(3.5)
        section.left_margin = Cm(2.8)
        section.right_margin = Cm(2.6)
    
    # 3. 添加页眉（LOGO + 公司名）
    add_header_with_logo(doc, logo_path, company_name)
    
    # 4. 添加页脚（页码）
    add_footer_with_page_numbers(doc)
    
    # 5. 设置默认字体
    style = doc.styles['Normal']
    style.font.name = '仿宋'
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋')
    
    # 6. 添加标题（如果提供）
    if title:
        p = doc.add_paragraph(title)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            set_chinese_font(run, '黑体', 22, True)
    
    return doc

def add_vision_paragraph(doc, company_info=None):
    """
    在文档末尾添加公司愿景理念段落（分两行，左对齐）
    用于需要展示公司文化的正式文档
    """
    if company_info is None:
        company_info = get_company_info_from_system()
    
    vision = company_info.get('vision', '')
    philosophy = company_info.get('philosophy', '')
    
    if not vision and not philosophy:
        return
    
    # 添加分隔线
    p = doc.add_paragraph()
    run = p.add_run('─' * 40)
    set_chinese_font(run, '仿宋', 10)
    
    # 愿景（左对齐）
    if vision:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(f'【愿景】{vision}')
        set_chinese_font(run, '楷体', 11)
    
    # 理念（左对齐）
    if philosophy:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(f'【理念】{philosophy}')
        set_chinese_font(run, '楷体', 11)
```

---

## 📁 文档命名规则（必须遵循）

### 命名格式

```
[文档类型]_[客户名称]_[项目名称]_[日期]_[版本].docx
```

### 命名元素说明

| 元素 | 说明 | 示例 | 必填 |
|------|------|------|------|
| 文档类型 | 具体文档类型 | 合同、报价单、发货单、会议纪要、技术方案 | ✅ |
| 客户名称 | 客户公司简称 | 阿里、腾讯、华为、海尔 | ✅ |
| 项目名称 | 项目名称（可选） | ERP、MES、WMS、OA | ○ |
| 日期 | 文档日期，格式 YYYYMMDD | 20250319 | ✅ |
| 版本 | 版本号 v1.0（可选，默认 v1.0） | v1.0、v1.1、v2.0 | ○ |

### 自动命名函数

```python
import datetime

def generate_doc_name(doc_type, customer_name, project_name="", version="v1.0"):
    """
    生成符合规范的文档名称
    
    参数:
        doc_type: 文档类型编码（如 CONTRACT, QUOTE）
        customer_name: 客户名称
        project_name: 项目名称（可选）
        version: 版本号（可选，默认 v1.0）
    
    返回:
        文档名称字符串，如 CONTRACT_阿里_钉钉OA_20250319_v1.0.docx
    """
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    customer = customer_name.replace("有限公司", "").replace("股份有限公司", "").replace("集团", "").strip()
    project = project_name.strip() if project_name else ""
    
    parts = [doc_type, customer]
    if project:
        parts.append(project)
    parts.append(date_str)
    
    if version and version != "v1.0":
        parts.append(version)
    
    return "_".join(parts) + ".docx"
```

---

## 公司信息

- 公司名称：青岛火一五信息科技有限公司
- 默认愿景：推动B端用户向全场景人工智能机器人转变
- 默认理念：打破信息孤岛，用一套系统驱动企业增长
- LOGO：从公司系统自动获取

---

## 文档结构

1. 合同标题 - 居中，黑体二号加粗
2. 合同编号 - 居中，仿宋三号
3. 签订日期 - 居中，仿宋三号
4. 一，二，三...章 - 楷体三号加粗
5. 签署栏 - 盖章、法定代表人、日期

---

## 触发关键词

**文档生成类（自动触发本技能）：**
- 写word、写文档、写个文档
- 生成word、生成文档、创建word、创建文档
- 导出word、导出文档、下载word、下载文档
- .docx、word文档、Word文档、Word生成、生成Word

**具体文档类（自动触发本技能）：**
- 写合同、写报价单、写说明书、写会议纪要
- 合同模板、报价单模板、文档模板、公司文档

**正式文档类（自动触发本技能）：**
- 正式文档、公文、标书、方案文档
- 年度报告、通知、请示、报告、函
