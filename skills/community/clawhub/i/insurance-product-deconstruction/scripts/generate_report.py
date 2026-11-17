#!/usr/bin/env python3
"""Generate Obsidian report skeleton directly from extracted data.
Claude only reviews and polishes — does not write from scratch.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CACHE_DIR = ".product-cache"

try:
    from scripts.config import get_obsidian_output
    OBSIDIAN_BASE = get_obsidian_output()
except ImportError:
    OBSIDIAN_BASE = Path.home() / "Documents"


def _load(product_dir: Path, name: str, default=None):
    path = product_dir / CACHE_DIR / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _clean(text: str) -> str:
    """Clean extracted text: remove page footers, normalize whitespace."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r"^本条款第\s*\d+\s*页\s*共\s*\d+\s*页$", s):
            continue
        if re.match(r"^本合同第\s*\d+\s*页\s*共\s*\d+\s*页$", s):
            continue
        cleaned.append(s)
    return "\n".join(cleaned)


def _clause_text(clauses: dict, key: str) -> str:
    """Get clause text as string (clauses values are lists)."""
    val = clauses.get(key, "")
    if isinstance(val, list):
        return val[0] if val else ""
    return str(val)


def _extract_numbers_from_clauses(clauses: dict) -> dict:
    """Extract key numbers from clause text."""
    nums = {}

    # 投保年龄
    scope = _clause_text(clauses, "投保范围")
    m = re.search(r"(\d+)周岁.*?至\s*(\d+)周岁", scope)
    if m:
        nums["投保年龄"] = f"{m.group(1)}-{m.group(2)}周岁"

    # 犹豫期
    hesitation = _clause_text(clauses, "犹豫期")
    m = re.search(r"(\d+)日", hesitation)
    if m:
        nums["犹豫期"] = f"{m.group(1)}日"

    # 宽限期
    grace = _clause_text(clauses, "宽限期")
    m = re.search(r"(\d+)日", grace)
    if m:
        nums["宽限期"] = f"{m.group(1)}日"

    # 保单贷款比例
    loan = _clause_text(clauses, "保单贷款")
    m = re.search(r"(\d+)%", loan)
    if m:
        nums["保单贷款比例"] = f"{m.group(1)}%"

    # 贷款期限
    m = re.search(r"最长不超过(\d+)个月", loan)
    if m:
        nums["贷款期限"] = f"{m.group(1)}个月"

    # 减保上限
    reduce = _clause_text(clauses, "减保")
    m = re.search(r"不得超过.*?(\d+)%", reduce)
    if m:
        nums["减保上限"] = f"{m.group(1)}%/年"

    # 到达年龄给付比例
    duty = _clause_text(clauses, "保险责任")
    ratios = re.findall(r"(\d+)[-－]?\d*周岁.*?(\d+)%", duty)
    if ratios:
        # Deduplicate (same ratios appear in clause 2 and 3)
        seen = set()
        unique = []
        for a, p in ratios:
            key = f"{a}_{p}"
            if key not in seen:
                seen.add(key)
                unique.append(f"{a}周岁{p}%")
        nums["给付比例"] = "、".join(unique)

    # 年度有效保额增长率
    m = re.search(r"\(1\+(\d+\.?\d*)%\)", duty)
    if m:
        nums["年度增长率"] = f"{m.group(1)}%"

    return nums


def _extract_product_info(manual: dict, underwriting: str, nums: dict, product_name: str = "") -> dict:
    """Extract basic product information."""
    info = {}

    # From manual
    须知 = manual.get("投保须知", "")
    m = re.search(r"投保范围[：:]\s*(.+)", 须知)
    if m:
        info["投保范围"] = m.group(1).strip()
    elif nums.get("投保年龄"):
        info["投保范围"] = nums["投保年龄"]

    m = re.search(r"保险期间[：:]\s*(.+)", 须知)
    if m:
        info["保险期间"] = m.group(1).strip()

    m = re.search(r"交费方式[：:]\s*(.+)", 须知)
    if m:
        info["缴费方式"] = m.group(1).strip()

    # 产品名称 from manual content or underwriting
    for source in [underwriting, 须知]:
        m = re.search(r"险种名称[：:].*?((?:\S+寿险|\S+年金|\S+重疾)\S*)", source)
        if m:
            info["产品名称"] = m.group(1).strip()
            break

    # 承保公司 from manual, underwriting, or product name
    for source in [underwriting, 须知] + list(manual.values()):
        # Try exact match first, then relaxed (handles OCR spaces)
        m = re.search(r"(\S+人寿\S*有限公司)", source)
        if m:
            info["承保公司"] = m.group(1).strip()
            break
        m = re.search(r"(\S+人寿)\S*股份\w*公司", source)
        if m:
            info["承保公司"] = m.group(1).strip() + "保险股份有限公司"
            break
    if "承保公司" not in info:
        # Fallback: extract from product name or directory name
        for name in [product_name]:
            m = re.search(r"(\S+人寿)", name)
            if m:
                info["承保公司"] = m.group(1).strip() + "保险股份有限公司"
                break

    # 产品代码 from underwriting (8-digit code)
    m = re.search(r"\b(\d{8})\b", underwriting)
    if m:
        info["产品代码"] = m.group(1)

    return info


def _count_exemptions_inline(exclusion_text: str) -> int:
    """Count unique numbered exclusion items: (1), (2), ..."""
    if not exclusion_text:
        return 0
    items = re.findall(r"[(\（]\d+[)\）]", exclusion_text)
    return len(set(items))


def generate_report(product_dir: Path) -> str:
    """Generate the full Obsidian report Markdown."""
    product_dir = product_dir.resolve()

    # Load all data
    report_input = _load(product_dir, "report-input.json")
    if not report_input:
        raise FileNotFoundError(f"report-input.json not found in {product_dir}")

    clauses = report_input.get("clauses", {})
    manual = report_input.get("manual_content", {})
    underwriting = report_input.get("underwriting_rules", "")
    surrender = report_input.get("surrender_rules", "")
    facts = report_input.get("facts", {})
    tables = report_input.get("table_data", {})
    sources = report_input.get("source_files", [])

    product_name = product_dir.name

    # Extract structured data
    nums = _extract_numbers_from_clauses(clauses)
    info = _extract_product_info(manual, underwriting, nums, product_name)

    # Get duty text for later use
    duty_text = _clause_text(clauses, "保险责任")

    # Count exclusion items from the exclusion clause only
    other_exempt = ""
    for k, v in clauses.items():
        if "免责" in k or "责任免除" in k:
            other_exempt += _clause_text(clauses, k)
    exemption_count = _count_exemptions_inline(other_exempt)

    # Detect product type (enhanced)
    manual_text = " ".join(manual.values())
    all_text = product_name + " " + manual_text + " " + duty_text
    
    # 增额终身寿
    if ("增额终身寿" in all_text or 
        ("终身寿险" in all_text and ("年度保额增长率" in all_text or "复利递增" in all_text or "增额" in all_text))):
        product_type = "增额终身寿"
    # 养老年金
    elif ("养老年金" in all_text or 
          ("年金" in all_text and ("退休" in all_text or "养老" in all_text or "领取" in all_text))):
        product_type = "养老年金"
    # 快返年金
    elif ("快返年金" in all_text or 
          ("年金" in all_text and ("快速回本" in all_text or "短期" in all_text or "快返" in all_text))):
        product_type = "快返年金"
    # 杠杆寿
    elif ("定期寿险" in all_text or 
          ("寿险" in all_text and ("杠杆" in all_text or "高保障" in all_text or "定期" in all_text))):
        product_type = "杠杆寿"
    # 重疾险
    elif "重疾" in all_text or "重大疾病" in all_text:
        product_type = "重疾险"
    # 医疗险
    elif "医疗险" in all_text or "百万医疗" in all_text or "住院医疗" in all_text:
        product_type = "医疗险"
    # 年金险（通用）
    elif "年金" in all_text:
        product_type = "年金险"
    # 终身寿险（通用）
    elif "终身寿险" in all_text:
        product_type = "终身寿险"
    else:
        product_type = "寿险"

    # Detect dividend type
    if "分红" in product_name or "分红" in manual_text:
        dividend_type = "分红型"
    else:
        dividend_type = ""

    # Detect dividend method
    dividend_method = ""
    dividend_clause = _clause_text(clauses, "保单红利")
    if "增加保险金额" in dividend_clause or "增额" in dividend_clause:
        dividend_method = "增额分红"
    elif "现金红利" in dividend_clause:
        dividend_method = "现金红利"
    elif "英式分红" in dividend_clause:
        dividend_method = "英式分红"

    # Detect waiting period
    waiting = "无"
    if "等待期" in duty_text:
        m = re.search(r"等待期.*?(\d+)", duty_text)
        if m:
            waiting = f"{m.group(1)}日"

    # Build YAML frontmatter
    yaml_lines = [
        "---",
        f"产品名称: {product_name}",
        f"承保公司: {info.get('承保公司', '未识别')}",
        f"产品类型: {dividend_type}{product_type}" if dividend_type else f"产品类型: {product_type}",
    ]

    if info.get("产品代码"):
        yaml_lines.append(f"产品代码: {info['产品代码']}")
    if nums.get("投保年龄"):
        yaml_lines.append(f"承保年龄上限: {nums['投保年龄'].split('-')[-1] if '-' in nums['投保年龄'] else nums['投保年龄']}")
    if info.get("缴费方式"):
        yaml_lines.append(f"缴费方式: {info['缴费方式']}")
    if info.get("保险期间"):
        yaml_lines.append(f"保障期: {info['保险期间']}")
    if nums.get("年度增长率"):
        yaml_lines.append(f"年度保额增长率: {nums['年度增长率']}")
    if dividend_method:
        yaml_lines.append(f"分红类型: {dividend_method}")
    if nums.get("减保上限"):
        yaml_lines.append(f"减保上限: {nums['减保上限']}")
    yaml_lines.append(f"免责条款数量: {exemption_count}")
    if "第二投保人" in clauses:
        yaml_lines.append("支持第二投保人: 是")
    if "保单贷款" in clauses:
        loan_ratio = nums.get("保单贷款比例", "?")
        yaml_lines.append(f"支持保单贷款: 是（{loan_ratio}现金价值）")
    yaml_lines.append("---")

    # Build report sections
    sections = []

    # 一、产品基础信息
    sections.append("## 一、产品基础信息\n")
    sections.append("| 字段 | 内容 |")
    sections.append("|------|------|")
    sections.append(f"| 产品名称 | {product_name} |")
    sections.append(f"| 产品类型 | {dividend_type}{product_type} |" if dividend_type else f"| 产品类型 | {product_type} |")
    if info.get("投保范围"):
        sections.append(f"| 承保年龄 | {info['投保范围']} |")
    if info.get("缴费方式"):
        sections.append(f"| 缴费期间 | {info['缴费方式']} |")
    if info.get("保险期间"):
        sections.append(f"| 保障期间 | {info['保险期间']} |")
    if nums.get("犹豫期"):
        sections.append(f"| 犹豫期 | {nums['犹豫期']}，扣除不超过10元工本费 |")
    sections.append(f"| 等待期 | {waiting} |")
    if nums.get("给付比例"):
        sections.append(f"| 到达年龄给付比例 | {nums['给付比例']} |")
    if nums.get("年度增长率"):
        sections.append(f"| 年度有效保额增长率 | {nums['年度增长率']}复利递增 |")

    # 二、核心保障责任
    sections.append("\n## 二、核心保障责任拆解\n")
    if duty_text:
        sections.append("### 保险责任\n")
        sections.append("\n")
        sections.append(_clean(duty_text))
        sections.append("")

    if dividend_clause:
        sections.append("### 保单红利\n")
        sections.append("\n")
        sections.append(_clean(dividend_clause))

        # Add mandatory uncertainty warning
        sections.append("")
        sections.append("> **红利不确定性提示**：保单红利是不确定的，某些年度可能为零。红利分配取决于公司分红保险业务的实际经营成果。")
        sections.append("")

    # 产品类型专属分析
    sections.append("\n### 产品类型专属分析\n")
    
    if product_type == "增额终身寿":
        sections.append("**增额终身寿核心关注点**：\n")
        sections.append("1. **现金价值增长率**：年度保额增长率，复利递增效果")
        sections.append("2. **回本年限**：现金价值超过已交保费的时间")
        sections.append("3. **分红方式**：交清增额/保额分红/累计生息，哪种收益更高")
        sections.append("4. **减保灵活性**：急用钱能不能取出来，上限多少")
        sections.append("")
        sections.append("**对比重点**：现金价值表、IRR、分红演示")
        sections.append("")
    
    elif product_type == "养老年金":
        sections.append("**养老年金核心关注点**：\n")
        sections.append("1. **领取金额**：每年/每月能领多少钱")
        sections.append("2. **保证领取期限**：保证领取多少年，提前身故怎么处理")
        sections.append("3. **领取方式**：即期领取 vs 延期领取")
        sections.append("4. **祝寿金/满期金**：有没有额外收益")
        sections.append("")
        sections.append("**对比重点**：领取金额、保证期限、身故保障")
        sections.append("")
    
    elif product_type == "杠杆寿":
        sections.append("**杠杆寿核心关注点**：\n")
        sections.append("1. **杠杆倍数**：保额÷保费，越高越好")
        sections.append("2. **保障期限**：覆盖负债期（房贷、孩子成长期）")
        sections.append("3. **健康告知**：能不能买得到")
        sections.append("4. **免责条款**：什么情况不赔")
        sections.append("")
        sections.append("**对比重点**：杠杆倍数、保费、保障期限")
        sections.append("")
    
    elif product_type == "快返年金":
        sections.append("**快返年金核心关注点**：\n")
        sections.append("1. **回本年限**：多久能回本（通常3-5年）")
        sections.append("2. **前期领取金额**：前几年能拿到多少钱")
        sections.append("3. **现金价值走势**：回本后还能涨多少")
        sections.append("4. **灵活性**：能不能减保、贷款")
        sections.append("")
        sections.append("**对比重点**：回本年限、前期领取、灵活性")
        sections.append("")
    
    elif product_type == "重疾险":
        sections.append("**重疾险核心关注点**：\n")
        sections.append("1. **病种数量**：重疾/中症/轻症分别多少种")
        sections.append("2. **赔付比例**：重疾赔多少、中症赔多少、轻症赔多少")
        sections.append("3. **豁免责任**：被保人/投保人豁免")
        sections.append("4. **特定疾病额外赔**：有没有额外赔付")
        sections.append("")
        sections.append("**对比重点**：赔付比例、病种数量、豁免责任")
        sections.append("")

    # 三、现金价值与收益分析
    sections.append("\n## 三、现金价值与收益分析\n")
    # From manual example
    example = manual.get("投保示例", "")
    if example:
        sections.append("### 投保示例（产品说明书载明）\n")
        sections.append("\n")
        sections.append(_clean(example))
        sections.append("")
    else:
        sections.append("<!-- 请补充：产品说明书中的投保示例数据 -->\n")

    # 四、免责条款
    sections.append("\n## 四、免责条款与重要提示\n")
    sections.append("### 责任免除条款\n")
    # Find all exclusion-related clauses
    exclusion_text = ""
    for k, v in clauses.items():
        if "免责" in k or "责任免除" in k:
            exclusion_text += _clause_text(clauses, k) + "\n"
    if not exclusion_text:
        # Try to find in duty text
        m = re.search(r"(2\.5\s*责任免除.*?)(?=2\.6|$)", duty_text, re.DOTALL)
        if m:
            exclusion_text = m.group(1)

    if exclusion_text:
        sections.append("\n")
        sections.append(_clean(exclusion_text))
    else:
        sections.append("<!-- 请从条款中补充责任免除条款 -->\n")

    # 退保损失
    sections.append("\n### 退保损失提示\n")
    sections.append("- 犹豫期内退保：扣除不超过10元工本费后退还全部已交保费")
    sections.append("- 犹豫期后退保：退还合同现金价值，前期现金价值较低，退保会有较大损失")
    sections.append("")

    # 五、投保规则与权益
    sections.append("\n## 五、投保规则与权益\n")
    if underwriting:
        sections.append("### 投保规则\n")
        sections.append("\n")
        sections.append(_clean(underwriting))
        sections.append("")

    sections.append("### 核心保单权益\n")
    for kw in ["减保", "保单贷款", "自动垫交", "减额交清", "第二投保人", "宽限期", "复效"]:
        for clause_key, clause_val in clauses.items():
            text = _clause_text(clauses, clause_key)
            if kw in clause_key or kw in text[:50]:
                sections.append(f"**{kw}**")
                sections.append(f"\n")
                summary = _clean(text[:500])
                sections.append(summary)
                sections.append("")
                break

    # 六、增值服务
    sections.append("\n## 六、增值服务清单\n")
    # Search for service-related content
    service_found = False
    for source in [underwriting, surrender, manual.get("投保须知", "")]:
        if "增值服务" in source or "健康管理" in source or "绿通" in source:
            sections.append("\n")
            service_found = True
            break
    if not service_found:
        sections.append("本次提供的原始文件中未发现增值服务相关资料。\n")

    # 七、优缺点
    sections.append("\n## 七、优缺点与适合人群\n")
    sections.append("### 优点\n")
    sections.append("\n")
    sections.append("\n")

    sections.append("### 缺点\n")
    sections.append("\n")
    sections.append("\n")

    sections.append("### 适合人群\n")
    sections.append("\n")
    sections.append("\n")

    # 八、YAML对比字段
    sections.append("\n## 八、对比模板预留字段\n")
    sections.append("```yaml")
    sections.append("---")
    for line in yaml_lines[1:-1]:  # Skip first --- and last ---
        sections.append(line)
    sections.append("---")
    sections.append("```")

    # Assemble
    report = "\n".join(yaml_lines) + "\n\n" + "\n".join(sections)

    return report


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <product_dir>", file=sys.stderr)
        sys.exit(1)

    product_dir = Path(sys.argv[1])
    if not product_dir.is_dir():
        print(f"Not a directory: {product_dir}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(product_dir)

    # Write to Obsidian
    output_path = OBSIDIAN_BASE / f"{product_dir.name}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    # Also write to product directory for review
    review_path = product_dir / "report-draft.md"
    review_path.write_text(report, encoding="utf-8")

    print(json.dumps({
        "status": "ok",
        "obsidian_path": str(output_path),
        "review_path": str(review_path),
        "report_length": len(report),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
