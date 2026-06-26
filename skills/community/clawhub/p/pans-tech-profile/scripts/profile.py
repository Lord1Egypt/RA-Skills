#!/usr/bin/env python3
"""
pans-tech-profile - 公司技术栈与算力需求分析工具

分析目标公司的技术栈和算力需求，为 AI 算力销售提供客户画像。
"""

import argparse
import json
import sys
import re
from datetime import datetime
from typing import Optional

# 尝试导入可选依赖
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


# ============ 配置 ============

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 常见技术栈关键词
TECH_KEYWORDS = {
    "languages": {
        "Python": ["python", "pyTorch", "tensorflow", "keras"],
        "JavaScript": ["javascript", "js", "react", "vue", "angular"],
        "TypeScript": ["typescript", "ts", "next.js", "nest"],
        "Java": ["java", "spring", "springboot"],
        "Go": ["go ", "golang", "gin", "echo"],
        "Rust": ["rust", "tokio", "actix"],
        "C++": ["c++", "cuda", "cpp"],
        "C#": ["c#", ".net", "asp.net"],
    },
    "ml_frameworks": {
        "PyTorch": ["pytorch", "torch"],
        "TensorFlow": ["tensorflow", "keras"],
        "JAX": ["jax", "flax"],
        "MXNet": ["mxnet"],
        "PaddlePaddle": ["paddle", "paddlenlp"],
    },
    "cloud": {
        "AWS": ["aws", "amazon web", "ec2", "s3", "lambda"],
        "Google Cloud": ["google cloud", "gcp", "cloud.google"],
        "Azure": ["azure", "microsoft azure"],
        "阿里云": ["阿里云", "aliyun"],
        "腾讯云": ["腾讯云", "tencent cloud"],
        "火山引擎": ["火山引擎", "volcengine"],
    },
    "mlops": {
        "Kubernetes": ["kubernetes", "k8s"],
        "Docker": ["docker"],
        "MLflow": ["mlflow"],
        "Kubeflow": ["kubeflow"],
        "Ray": ["ray ", "ray.io"],
        "Weights & Biases": ["weights & biases", "wandb"],
    },
    "vector_db": {
        "Pinecone": ["pinecone"],
        "Weaviate": ["weaviate"],
        "Milvus": ["milvus"],
        "Qdrant": ["qdrant"],
        "Chroma": ["chroma"],
    },
    "llm": {
        "OpenAI": ["openai", "gpt"],
        "Anthropic": ["anthropic", "claude"],
        "Meta LLaMA": ["llama", "meta ai"],
        "Mistral": ["mistral"],
        "Cohere": ["cohere"],
        "本地部署": ["self-hosted", "selfhosted", "本地部署"],
    }
}

# 算力需求估算参数
GPU_ESTIMATES = {
    "startup": {"gpu_hours_per_month": 100, "gpu_type": "A10G", "monthly_cost_usd": 500},
    "mid": {"gpu_hours_per_month": 2000, "gpu_type": "A100", "monthly_cost_usd": 15000},
    "large": {"gpu_hours_per_month": 10000, "gpu_type": "H100", "monthly_cost_usd": 100000},
    "enterprise": {"gpu_hours_per_month": 50000, "gpu_type": "H100", "monthly_cost_usd": 400000},
}


# ============ 工具函数 ============

def check_dependencies():
    """检查并提示安装依赖"""
    missing = []
    if not REQUESTS_AVAILABLE:
        missing.append("requests")
    if not BS4_AVAILABLE:
        missing.append("beautifulsoup4")
    
    if missing:
        print(f"⚠️  缺少依赖库: {', '.join(missing)}", file=sys.stderr)
        print(f"安装命令: pip install {' '.join(missing)}", file=sys.stderr)
        return False
    return True


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """获取网页内容"""
    if not REQUESTS_AVAILABLE:
        return None
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return None


def extract_tech_stack(html: str) -> dict:
    """从HTML中提取技术栈关键词"""
    if not BS4_AVAILABLE:
        # 简单文本匹配
        text = html.lower()
    else:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
    
    found = {"languages": [], "ml_frameworks": [], "cloud": [], "mlops": [], "vector_db": [], "llm": []}
    
    for category, techs in TECH_KEYWORDS.items():
        for tech, keywords in techs.items():
            for kw in keywords:
                if kw in text:
                    if tech not in found[category]:
                        found[category].append(tech)
                    break
    
    return found


def analyze_company(company: str, domain: str = None, deep: bool = False) -> dict:
    """分析公司技术栈"""
    if domain is None:
        # 从公司名推断域名
        domain = company.lower().replace(" ", "").replace(",", "") + ".com"
    
    result = {
        "company": company,
        "domain": domain,
        "analyzed_at": datetime.now().isoformat(),
        "tech_stack": {"languages": [], "ml_frameworks": [], "cloud": [], "mlops": [], "vector_db": [], "llm": []},
        "signals": [],
        "gpu_estimate": None,
        "sales_recommendation": None,
    }
    
    # 抓取官网
    urls_to_check = [f"https://{domain}"]
    if deep:
        urls_to_check.extend([
            f"https://{domain}/careers",
            f"https://{domain}/about",
            f"https://{domain}/technology",
        ])
    
    all_tech = {"languages": [], "ml_frameworks": [], "cloud": [], "mlops": [], "vector_db": [], "llm": []}
    
    for url in urls_to_check:
        html = fetch_url(url)
        if html:
            result["signals"].append({"source": url, "status": "fetched"})
            tech = extract_tech_stack(html)
            for cat, items in tech.items():
                for item in items:
                    if item not in all_tech[cat]:
                        all_tech[cat].append(item)
        else:
            result["signals"].append({"source": url, "status": "failed"})
    
    result["tech_stack"] = all_tech
    
    # 估算算力需求
    result["gpu_estimate"] = estimate_gpu_needs(result)
    
    # 销售建议
    result["sales_recommendation"] = generate_recommendation(result)
    
    return result


def estimate_gpu_needs(profile: dict) -> dict:
    """估算GPU需求"""
    tech = profile.get("tech_stack", {})
    llm_count = len(tech.get("llm", []))
    ml_count = len(tech.get("ml_frameworks", []))
    
    # 基于技术栈判断规模
    score = 0
    if llm_count > 0:
        score += 3
    if ml_count > 0:
        score += 2
    if "Kubernetes" in tech.get("mlops", []) or "Docker" in tech.get("mlops", []):
        score += 1
    if "AWS" in tech.get("cloud", []) or "Google Cloud" in tech.get("cloud", []):
        score += 1
    
    if score >= 4:
        tier = "enterprise"
    elif score >= 3:
        tier = "large"
    elif score >= 2:
        tier = "mid"
    else:
        tier = "startup"
    
    estimate = GPU_ESTIMATES[tier].copy()
    estimate["tier"] = tier
    estimate["confidence"] = "medium" if score >= 3 else "low"
    
    return estimate


def generate_recommendation(profile: dict) -> dict:
    """生成销售建议"""
    tech = profile.get("tech_stack", {})
    gpu = profile.get("gpu_estimate", {})
    tier = gpu.get("tier", "startup")
    
    # 优先级
    priority_map = {"enterprise": "A", "large": "B", "mid": "C", "startup": "D"}
    
    # 切入角度
    angles = []
    if "PyTorch" in tech.get("ml_frameworks", []):
        angles.append("PyTorch 训练优化")
    if "llm" in tech.get("llm", []) or len(tech.get("llm", [])) > 0:
        angles.append("LLM 推理加速")
    if "Kubernetes" in tech.get("mlops", []):
        angles.append("K8s 集群管理")
    if "vector_db" in tech.get("vector_db", []):
        angles.append("向量数据库需求")
    
    if not angles:
        angles = ["技术栈调研", "初步接触"]
    
    return {
        "priority": priority_map.get(tier, "D"),
        "estimated_monthly_budget": gpu.get("monthly_cost_usd", 0),
        "suggested_angles": angles,
        "next_steps": f"针对 {profile['company']} 的 {angles[0]} 需求进行针对性沟通"
    }


def format_output(profile: dict, fmt: str) -> str:
    """格式化输出"""
    if fmt == "json":
        return json.dumps(profile, indent=2, ensure_ascii=False)
    
    elif fmt == "markdown":
        return format_markdown(profile)
    
    else:  # text
        return format_text(profile)


def format_text(profile: dict) -> str:
    """纯文本格式"""
    lines = []
    lines.append("=" * 50)
    lines.append(f"公司技术画像: {profile['company']}")
    lines.append("=" * 50)
    
    lines.append(f"\n📌 基本信息")
    lines.append(f"  域名: {profile['domain']}")
    lines.append(f"  分析时间: {profile['analyzed_at']}")
    
    tech = profile.get("tech_stack", {})
    if tech.get("languages"):
        lines.append(f"\n💻 编程语言: {', '.join(tech['languages'])}")
    if tech.get("ml_frameworks"):
        lines.append(f"🤖 ML框架: {', '.join(tech['ml_frameworks'])}")
    if tech.get("cloud"):
        lines.append(f"☁️ 云服务: {', '.join(tech['cloud'])}")
    if tech.get("mlops"):
        lines.append(f"🔧 MLOps: {', '.join(tech['mlops'])}")
    if tech.get("llm"):
        lines.append(f"🧠 LLM: {', '.join(tech['llm'])}")
    
    gpu = profile.get("gpu_estimate", {})
    lines.append(f"\n⚡ 算力需求评估")
    lines.append(f"  规模等级: {gpu.get('tier', 'unknown')}")
    lines.append(f"  GPU类型: {gpu.get('gpu_type', 'N/A')}")
    lines.append(f"  月估算成本: ${gpu.get('monthly_cost_usd', 0):,}")
    lines.append(f"  可信度: {gpu.get('confidence', 'low')}")
    
    rec = profile.get("sales_recommendation", {})
    lines.append(f"\n🎯 销售建议")
    lines.append(f"  优先级: {rec.get('priority', 'N/A')}")
    lines.append(f"  建议角度: {', '.join(rec.get('suggested_angles', []))}")
    lines.append(f"  下一步: {rec.get('next_steps', 'N/A')}")
    
    lines.append(f"\n📡 信号来源")
    for sig in profile.get("signals", []):
        status = "✓" if sig.get("status") == "fetched" else "✗"
        lines.append(f"  {status} {sig.get('source', '')}")
    
    return "\n".join(lines)


def format_markdown(profile: dict) -> str:
    """Markdown格式"""
    lines = []
    lines.append(f"# {profile['company']} 技术画像")
    lines.append("")
    lines.append(f"**域名**: {profile['domain']}")
    lines.append(f"**分析时间**: {profile['analyzed_at']}")
    lines.append("")
    
    tech = profile.get("tech_stack", {})
    
    if tech.get("languages"):
        lines.append("## 💻 编程语言")
        for lang in tech["languages"]:
            lines.append(f"- {lang}")
        lines.append("")
    
    if tech.get("ml_frameworks"):
        lines.append("## 🤖 ML框架")
        for fw in tech["ml_frameworks"]:
            lines.append(f"- {fw}")
        lines.append("")
    
    if tech.get("cloud"):
        lines.append("## ☁️ 云服务")
        for c in tech["cloud"]:
            lines.append(f"- {c}")
        lines.append("")
    
    if tech.get("mlops"):
        lines.append("## 🔧 MLOps")
        for m in tech["mlops"]:
            lines.append(f"- {m}")
        lines.append("")
    
    if tech.get("llm"):
        lines.append("## 🧠 LLM")
        for llm in tech["llm"]:
            lines.append(f"- {llm}")
        lines.append("")
    
    gpu = profile.get("gpu_estimate", {})
    lines.append("## ⚡ 算力需求评估")
    lines.append("")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|------|-----|")
    lines.append(f"| 规模等级 | {gpu.get('tier', 'unknown')} |")
    lines.append(f"| GPU类型 | {gpu.get('gpu_type', 'N/A')} |")
    lines.append(f"| 月估算成本 | ${gpu.get('monthly_cost_usd', 0):,} |")
    lines.append(f"| 可信度 | {gpu.get('confidence', 'low')} |")
    lines.append("")
    
    rec = profile.get("sales_recommendation", {})
    lines.append("## 🎯 销售建议")
    lines.append("")
    lines.append(f"- **优先级**: {rec.get('priority', 'N/A')}")
    lines.append(f"- **预估月预算**: ${rec.get('estimated_monthly_budget', 0):,}")
    lines.append(f"- **建议角度**: {', '.join(rec.get('suggested_angles', []))}")
    lines.append(f"- **下一步**: {rec.get('next_steps', 'N/A')}")
    lines.append("")
    
    lines.append("## 📡 数据来源")
    lines.append("")
    for sig in profile.get("signals", []):
        status = "✅" if sig.get("status") == "fetched" else "❌"
        lines.append(f"{status} {sig.get('source', '')}")
    
    return "\n".join(lines)


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(
        description="分析目标公司的技术栈和算力需求",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/profile.py --company "OpenAI"
  python3 scripts/profile.py --domain openai.com --format json
  python3 scripts/profile.py --company "字节跳动" --deep
        """
    )
    
    parser.add_argument("--company", type=str, help="公司名称 (二选一)")
    parser.add_argument("--domain", type=str, help="公司域名 (二选一)")
    parser.add_argument("--format", type=str, choices=["text", "json", "markdown"], default="text", help="输出格式")
    parser.add_argument("--deep", action="store_true", help="深度分析 (更多数据源)")
    parser.add_argument("--output", type=str, help="输出到文件")
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.company and not args.domain:
        parser.error("必须提供 --company 或 --domain")
    
    company = args.company or args.domain.split(".")[0].capitalize()
    domain = args.domain or None
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    print(f"🔍 分析公司: {company} ...", file=sys.stderr)
    
    # 分析
    profile = analyze_company(company, domain, args.deep)
    
    # 输出
    output = format_output(profile, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
