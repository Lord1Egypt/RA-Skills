#!/usr/bin/env python3
"""
论文深度阅读报告生成器 v4.0
最终版：保留自动提取 + 结构化框架
"""

import os
import re
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)


class DeepPaperReaderV4:
    """深度论文阅读器 v4.0 - 框架版"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.clean_text = ""
        self.metadata = {}
        self.key_data = {}
        
    def extract_full_text(self):
        """提取PDF全文并清洗"""
        print(f"📄 正在提取: {os.path.basename(self.pdf_path)}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    self.raw_text += page_text + "\n"
        
        # 清洗文本
        self.clean_text = self._clean_text(self.raw_text)
        print(f"   ✓ 已提取 {len(self.clean_text)} 字符")
        return self.clean_text
    
    def _clean_text(self, text):
        """文本清洗"""
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        text = re.sub(r'(\d)\s+(\d)\s*(g/L|mM|mg/mL|μg/mL)', r'\1\2\3', text)
        text = re.sub(r'(\d)\s+(\d)\s*(°C|℃)', r'\1\2\3', text)
        text = re.sub(r'(\d)\s+(\d{3})(?!\d)', r'\1\2', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'Page\s*\d+', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def query_title_from_doi(self, doi):
        """从DOI查询标题"""
        try:
            doi = doi.strip()
            if not doi.startswith('10.'):
                return None
            url = f"https://api.crossref.org/works/{doi}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read())
                title = data.get('message', {}).get('title', [''])[0]
                return title if title else None
        except Exception as e:
            print(f"   ⚠ DOI查询失败: {e}")
            return None
    
    def parse_metadata(self):
        """解析元数据"""
        text = self.clean_text
        
        # DOI
        doi_match = re.search(r'10\.\d{4,}/[a-zA-Z0-9\-\.]+', text)
        doi = doi_match.group() if doi_match else ""
        self.metadata['doi'] = doi
        
        # 标题查询
        if doi:
            print(f"   🔍 正在从DOI查询标题...")
            title_from_api = self.query_title_from_doi(doi)
            if title_from_api:
                self.metadata['title'] = title_from_api
                print(f"   ✓ 标题查询成功")
        
        if 'title' not in self.metadata:
            self.metadata['title'] = self._extract_title_from_pdf(text)
        
        # 日期
        dates = re.findall(r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})', text, re.IGNORECASE)
        if dates:
            self.metadata['received'] = dates[0]
            if len(dates) > 1:
                self.metadata['accepted'] = dates[1]
        
        # 期刊
        journal_patterns = [
            (r'Nature\s+Communications', 'Nature Communications'),
            (r'\bMicrobiome\b', 'Microbiome'),
            (r'\bNature\b', 'Nature'),
            (r'\bScience\b', 'Science'),
            (r'\bCell\b', 'Cell'),
        ]
        for pattern, name in journal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.metadata['journal'] = name
                break
        
        # 作者
        self.metadata['authors'] = self._extract_authors(text)
        
        # 通讯作者
        corr_match = re.search(r'(?:\*Corresponding author|Correspondence)[^\n]*:\s*([^\n]+)', text, re.IGNORECASE)
        if corr_match:
            self.metadata['correspondence'] = corr_match.group(1).strip()
        
        return self.metadata
    
    def _extract_title_from_pdf(self, text):
        """从PDF提取标题"""
        lines = text.split('\n')
        for line in lines[:25]:
            line = line.strip()
            if (len(line) > 30 and 
                not line.startswith('http') and 
                not re.match(r'^\d+\s', line) and
                'Received' not in line and
                'doi' not in line.lower()):
                return re.sub(r'\s+', ' ', line)
        return "未找到标题"
    
    def _extract_authors(self, text):
        """提取作者"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'Received' in line:
                for j in range(max(0, i-4), i+1):
                    candidate = lines[j].strip()
                    if (candidate and len(candidate) > 20 and len(candidate) < 500 and
                        'doi' not in candidate.lower() and not re.match(r'^\d+', candidate)):
                        authors = re.sub(r'\s+', ' ', candidate)
                        authors = re.sub(r'\d+', '', authors)
                        return authors.strip()
        return "未找到作者"
    
    def extract_key_data(self):
        """提取关键数据"""
        text = self.clean_text
        data = {}
        
        # 百分比
        percents = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        data['percentages'] = sorted(list(set(percents)), key=lambda x: float(x), reverse=True)[:15]
        
        # 浓度
        concentrations = re.findall(r'(\d+(?:\.\d+)?)\s*(g/L|mM|M|mg/mL|μg/mL)', text, re.IGNORECASE)
        data['concentrations'] = list(set(concentrations))[:10]
        
        # 指标
        metrics = {}
        r2_matches = re.findall(r'R²?\s*[=≈]\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if r2_matches:
            metrics['R²'] = r2_matches[0]
        f1_matches = re.findall(r'F1\s*(?:score)?\s*[=≈]\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if f1_matches:
            metrics['F1'] = f1_matches[0]
        data['metrics'] = metrics
        
        # 温度
        temp_matches = re.findall(r'(\d{1,3})\s*°?C', text, re.IGNORECASE)
        valid_temps = [t for t in temp_matches if 20 <= int(t) <= 50]
        data['temperatures'] = sorted(list(set(valid_temps)), key=lambda x: int(x), reverse=True)[:8]
        
        self.key_data = data
        return data
    
    def generate_report(self, output_dir):
        """生成深度阅读报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = self.metadata.get('title', '未找到标题')
        authors = self.metadata.get('authors', '未找到作者')
        if authors and len(authors) > 300:
            authors = authors[:300] + "..."
        
        # 格式化关键数据
        key_data_text = ""
        if self.key_data.get('metrics'):
            key_data_text += "\n**关键指标:**\n"
            for k, v in self.key_data['metrics'].items():
                key_data_text += f"- {k}: {v}\n"
        
        if self.key_data.get('percentages'):
            key_data_text += f"\n**百分比数据:** {', '.join(self.key_data['percentages'][:8])}"
        
        if self.key_data.get('concentrations'):
            conc_strs = [f"{c[0]}{c[1]}" for c in self.key_data['concentrations']]
            key_data_text += f"\n\n**浓度数据:** {', '.join(conc_strs[:6])}"
        
        if self.key_data.get('temperatures'):
            key_data_text += f"\n\n**温度条件:** {', '.join(self.key_data['temperatures'][:5])}°C"
        
        report = f"""# 深度阅读报告：{title}

**生成时间**: {timestamp}  
**源文件**: {os.path.basename(self.pdf_path)}

---

## 第一部分：基础信息（自动提取）

| 字段 | 内容 |
|:---|:---|
| **标题** | {title} |
| **中文标题** | [待翻译] |
| **期刊** | {self.metadata.get('journal', '未知')} |
| **DOI** | {self.metadata.get('doi', '未知')} |
| **作者** | {authors} |
| **通讯作者** | {self.metadata.get('correspondence', '未找到')} |
| **接收日期** | {self.metadata.get('received', '未知')} |
| **发表日期** | {self.metadata.get('accepted', '未知')} |

{key_data_text}

---

## 第二部分：核心理解

*本部分由AI进行深度分析*

### 1. 这篇论文到底在做什么？
[AI分析中...]

### 2. 为什么要做这个？
[AI分析中...]

### 3. 是怎么做到的？
[AI分析中...]

### 4. 做得怎么样？
[AI分析中...]

### 5. 意味着什么？
[AI分析中...]

---

## 第三部分：批判性分析

*本部分由AI进行深度分析*

### 1. 优点/亮点
[AI分析中...]

### 2. 潜在问题/局限
[AI分析中...]

### 3. 未解决的关键问题
[AI分析中...]

---

## 第四部分：用户研究的关联

*本部分由用户补充*

### 1. 相关度评估
- [ ] 高：直接相关，可借鉴
- [ ] 中：间接相关，有参考价值
- [ ] 低：领域较远，仅作了解

**说明**：[由用户填写]

### 2. 可借鉴之处
- 技术方法：[由用户填写]
- 分析思路：[由用户填写]
- 实验设计：[由用户填写]

### 3. 可能的应用场景
- 研究方向：[由用户填写]
- 实际应用：[由用户填写]

### 4. 补充笔记
[由用户填写]

---

*报告生成时间：{timestamp}*

*💡 提示：请查看同目录下的完整分析版本（带AI深度分析内容）*
"""
        
        # 保存报告
        base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        report_name = f"{base_name}_深度阅读报告.md"
        report_path = os.path.join(output_dir, report_name)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"   ✓ 框架报告已生成: {report_name}")
        return report_path


def batch_process(pdf_dir):
    """批量处理PDF文件"""
    pdf_dir = Path(pdf_dir)
    output_dir = pdf_dir
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ 未找到PDF文件: {pdf_dir}")
        return []
    
    print(f"\n📂 找到 {len(pdf_files)} 个PDF文件")
    print(f"📁 输出目录: {output_dir}")
    
    results = []
    for pdf_file in pdf_files:
        reader = DeepPaperReaderV4(str(pdf_file))
        reader.extract_full_text()
        reader.parse_metadata()
        reader.extract_key_data()
        result = reader.generate_report(str(output_dir))
        if result:
            results.append(result)
    
    # 生成汇总报告
    if results:
        summary = f"""# 深度阅读汇总

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**处理文件数**: {len(results)}  
**源目录**: {pdf_dir}

## 工作流程

1. 自动提取基础信息 ✓
2. 人工深度分析（需要进一步处理）
3. 由用户补充"用户研究的关联"部分

## 已生成框架报告

"""
        for r in results:
            report_name = os.path.basename(r)
            summary += f"- {report_name}\n"
        
        summary += """
---

## 下一步

请查看生成的框架报告，然后告诉我：
1. 需要我进行深度分析的具体论文
2. 或批量进行深度分析

我将对每篇论文进行真正的理解性分析，生成完整的深度阅读报告。
"""
        
        summary_path = os.path.join(output_dir, "深度阅读汇总.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n✅ 汇总报告: 深度阅读汇总.md")
    
    print(f"\n🎉 框架生成完成! 请告诉我是否需要进行深度分析。")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python deep_reader.py <PDF目录>")
        sys.exit(1)
    
    pdf_dir = sys.argv[1]
    batch_process(pdf_dir)
