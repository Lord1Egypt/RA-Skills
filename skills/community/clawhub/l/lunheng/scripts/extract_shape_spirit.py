#!/usr/bin/env python3
"""
《双百优秀裁判文书的形与神》结构化提取器
从 4 卷 PDF 中提取：章/节/案例/关键词/案情/撰写心得/专家评析
"""
import re
import json
import os
from pathlib import Path
import pdfplumber

LEARNINGS_DIR = Path(__file__).parent / "learnings"
OUTPUT_DIR = Path(__file__).parent / "data" / "shape_spirit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# PDF 文件映射
PDF_FILES = {
    "civil": "双百优秀裁判文书的形与神：裁判思路与说理技巧（民事卷） (最高人民法院审判管理办公室) .pdf",
    "criminal": "双百优秀裁判文书的形与神：裁判思路与说理技巧（刑事卷） (最高人民法院审判管理办公室).pdf",
    "commercial": "双百优秀裁判文书的形与神：裁判思路与说理技巧（商事，海事海商，知识产权卷） (最高人民法院审判管理办公室).pdf",
    "administrative": "双百优秀裁判文书的形与神：裁判思路与说理技巧（行政，国家赔偿，执行卷） (最高人民法院审判管理办公室).pdf",
}

# 章节名称映射（根据目录提取）
CHAPTER_PATTERNS = {
    "civil": [
        "一般民事类", "人格权纠纷", "婚姻家庭纠纷", "继承纠纷",
        "所有权纠纷", "劳动争议", "买卖合同纠纷", "借款合同纠纷",
        "租赁合同纠纷", "承揽合同纠纷", "建设工程合同纠纷",
        "委托合同纠纷", "服务合同纠纷", "其他合同纠纷",
        "侵权责任类", "机动车交通事故责任纠纷", "医疗损害责任纠纷",
        "环境污染责任纠纷", "产品责任纠纷",
    ],
    "criminal": [
        "刑事类", "危害公共安全罪", "破坏社会主义市场经济秩序罪",
        "侵犯公民人身权利罪", "侵犯财产罪", "妨害社会管理秩序罪",
        "贪污贿赂罪", "渎职罪",
    ],
    "commercial": [
        "商事类", "公司纠纷", "合伙企业纠纷", "保险纠纷",
        "票据纠纷", "破产纠纷", "海事海商类", "知识产权类",
        "著作权纠纷", "专利权纠纷", "商标权纠纷",
    ],
    "administrative": [
        "行政类", "行政处罚", "行政许可", "行政强制",
        "行政征收", "行政赔偿", "执行类",
    ],
}


def extract_text(pdf_path: str, start_page: int = 1, end_page: int = None) -> str:
    """用 pdfplumber 提取 PDF 文本（保留表格结构）"""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        end = end_page or len(pdf.pages)
        for i in range(start_page - 1, min(end, len(pdf.pages))):
            page = pdf.pages[i]
            page_text = page.extract_text() or ""
            # 提取表格并拼接到文本中
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        page_text += "\n" + " ".join(str(c or "") for c in row)
            text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_toc(pdf_path: str) -> str:
    """提取目录页（通常在前 30 页）"""
    return extract_text(pdf_path, 1, 30)


def parse_toc(text: str) -> list:
    """解析目录，提取案例位置"""
    cases = []
    # 匹配案例编号和标题
    # 格式：1·吉某某等和殷某1等生命权健康权身体权纠纷案
    pattern = r'(\d+)[·．.]\s*(.+?)(?:…|…{2,}|$)'
    for match in re.finditer(pattern, text):
        case_num = match.group(1)
        case_title = match.group(2).strip()
        # 清理标题中的特殊字符
        case_title = re.sub(r'[●◆■□◇○◎▲▼△▽]', '', case_title).strip()
        if len(case_title) > 5:  # 过滤太短的误匹配
            cases.append({
                "num": case_num,
                "title": case_title,
            })
    return cases


def extract_keywords(text: str) -> list:
    """提取关键词"""
    keywords = []
    # 匹配【关键词】或［关键词］
    pattern = r'[【\[]关键词[】\]][：:\s]*(.+?)(?:\n|$)'
    match = re.search(pattern, text)
    if match:
        kw_text = match.group(1)
        # 分割关键词
        kws = re.split(r'[、，,\s]+', kw_text)
        keywords = [k.strip() for k in kws if k.strip() and len(k.strip()) > 1]
    return keywords


def extract_sections(text: str) -> dict:
    """提取各部分：简要案情、撰写心得、专家评析"""
    sections = {}
    
    # 简要案情
    pattern = r'[简简]要案情[：:\s]*(.+?)(?=(?:二、|撰写心得|专家评析|【关键词|$))'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        sections["brief_facts"] = match.group(1).strip()[:2000]
    
    # 撰写心得
    pattern = r'撰写心得[：:\s]*(.+?)(?=(?:三、|专家评析|专家点评|$))'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        sections["writing_experience"] = match.group(1).strip()[:3000]
    
    # 专家评析
    pattern = r'专家评[析点][：:\s]*(.+?)(?=(?:$|\d+[·．.]))'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        sections["expert_analysis"] = match.group(1).strip()[:2000]
    
    return sections


def extract_case(text: str, case_num: str) -> dict:
    """提取单个案例的完整信息"""
    case = {
        "num": case_num,
        "title": "",
        "keywords": [],
        "sections": {},
    }
    
    # 提取案例标题
    title_pattern = rf'{re.escape(case_num)}[·．.]\s*(.+?)(?:\n|$)'
    match = re.search(title_pattern, text)
    if match:
        title = match.group(1).strip()
        title = re.sub(r'[●◆■□◇○◎▲▼△▽]', '', title).strip()
        case["title"] = title
    
    # 提取关键词
    case["keywords"] = extract_keywords(text)
    
    # 提取各部分
    case["sections"] = extract_sections(text)
    
    return case


def process_volume(volume_key: str, pdf_filename: str) -> dict:
    """处理单卷 PDF"""
    pdf_path = LEARNINGS_DIR / pdf_filename
    if not pdf_path.exists():
        print(f"❌ 文件不存在: {pdf_path}")
        return {}
    
    print(f"\n📖 处理: {volume_key}")
    print(f"   文件: {pdf_filename}")
    
    # 获取总页数
    info = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
    pages_match = re.search(r'Pages:\s+(\d+)', info.stdout)
    total_pages = int(pages_match.group(1)) if pages_match else 0
    print(f"   页数: {total_pages}")
    
    # 提取目录
    toc_text = extract_toc(str(pdf_path))
    toc_cases = parse_toc(toc_text)
    print(f"   目录中案例数: {len(toc_cases)}")
    
    # 提取全文（分块处理避免内存溢出）
    all_text = ""
    chunk_size = 50  # 每 50 页一块
    for start in range(1, total_pages + 1, chunk_size):
        end = min(start + chunk_size - 1, total_pages)
        chunk = extract_text(str(pdf_path), start, end)
        all_text += f"\n\n--- PAGE {start}-{end} ---\n\n{chunk}"
    
    # 提取案例
    cases = []
    for toc_case in toc_cases:
        case_text = all_text  # 简化：在全文中搜索
        case = extract_case(case_text, toc_case["num"])
        if case.get("title") or case.get("sections"):
            cases.append(case)
    
    print(f"   已提取案例: {len(cases)}")
    
    volume_data = {
        "volume": volume_key,
        "pdf": pdf_filename,
        "total_pages": total_pages,
        "toc_cases": toc_cases,
        "extracted_cases": cases,
    }
    
    return volume_data


def main():
    """主函数"""
    print("=" * 60)
    print("《双百优秀裁判文书的形与神》结构化提取")
    print("=" * 60)
    
    all_data = {}
    
    for volume_key, pdf_filename in PDF_FILES.items():
        volume_data = process_volume(volume_key, pdf_filename)
        all_data[volume_key] = volume_data
        
        # 保存单卷数据
        output_path = OUTPUT_DIR / f"{volume_key}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(volume_data, f, ensure_ascii=False, indent=2)
        print(f"   已保存: {output_path}")
    
    # 保存汇总索引
    index = {
        "title": "双百优秀裁判文书的形与神：裁判思路与说理技巧",
        "publisher": "最高人民法院审判管理办公室",
        "year": 2022,
        "volumes": {}
    }
    
    for vol_key, vol_data in all_data.items():
        index["volumes"][vol_key] = {
            "total_cases": len(vol_data.get("extracted_cases", [])),
            "toc_cases": len(vol_data.get("toc_cases", [])),
        }
    
    index_path = OUTPUT_DIR / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 索引已保存: {index_path}")
    print(f"\n📊 汇总:")
    for vol_key, vol_index in index["volumes"].items():
        print(f"   {vol_key}: {vol_index['total_cases']} 案例")
    
    total = sum(v["total_cases"] for v in index["volumes"].values())
    print(f"   总计: {total} 案例")


if __name__ == "__main__":
    main()
