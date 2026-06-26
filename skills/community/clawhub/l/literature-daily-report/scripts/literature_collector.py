#!/usr/bin/env python3
"""
每日文献收集器 v2.0 - 生命科学 x AI
目标期刊：Nature 系列 (含子刊), Cell 系列 (含子刊), Science 系列 (含子刊)
           生信期刊：Bioinformatics, Nucleic Acids Research, Genome Biology 等
关注领域：宏基因组学、病原真菌学、生信分析方法、AI/ML

v2.0 更新：
- 获取每篇文献的摘要内容
- 为每篇文献生成智能总结
- 以编辑身份整理日报（前言 + 详细介绍 + 总结）
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import os
import re
from urllib.parse import quote
import time
import subprocess

# 配置
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/literature")
MAX_RESULTS = 50
ABSTRACT_CACHE_FILE = os.path.expanduser("~/.openclaw/workspace/literature/abstract_cache.json")

# Zotero 配置
ZOTERO_SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/zotero/scripts/zotero.py")
ZOTERO_GROUP_ID = os.environ.get("ZOTERO_GROUP_ID") or "6489333"  # BioCiaoLab Group Library
ZOTERO_COLLECTION_NAME = "每日文献速递"  # Zotero 收藏夹名称

# CNS 核心期刊列表
CNS_JOURNALS = [
    "Nature",
    "Cell", 
    "Science",
    "Nature Biotechnology",
    "Nature Methods",
    "Nature Genetics",
    "Nature Microbiology",
    "Nature Communications",
    "Nature Medicine",
    "Nature Ecology & Evolution",
    "Nature Cancer",
    "Cell Stem Cell",
    "Cell Reports",
    "Cell Host & Microbe",
    "Molecular Cell",
    "Immunity",
    "Neuron",
    "Science Advances",
    "Genome Biology",
    "Genome Research",
]

# 搜索关键词组合（生命科学 x AI）
SEARCH_QUERIES = [
    # 宏基因组学 + AI/ML
    '(metagenomics[Title/Abstract]) AND ((artificial intelligence[Title/Abstract]) OR (machine learning[Title/Abstract]) OR (deep learning[Title/Abstract]) OR (neural network[Title/Abstract]))',
    
    # 病原真菌 + 生信/AI
    '(fungal pathogen[Title/Abstract] OR pathogenic fungus[Title/Abstract] OR mycology[Title/Abstract]) AND ((bioinformatics[Title/Abstract]) OR (artificial intelligence[Title/Abstract]) OR (machine learning[Title/Abstract]))',
    
    # 生信方法开发 + AI
    '(bioinformatics[Title/Abstract]) AND ((method[Title/Abstract] OR tool[Title/Abstract] OR pipeline[Title/Abstract]) AND (artificial intelligence[Title/Abstract] OR machine learning[Title/Abstract] OR deep learning[Title/Abstract]))',
    
    # 单细胞生信 + AI
    '(single-cell[Title/Abstract]) AND ((bioinformatics[Title/Abstract]) OR (artificial intelligence[Title/Abstract]) OR (machine learning[Title/Abstract]))',
    
    # 基因组学 + AI
    '(genomics[Title/Abstract]) AND ((artificial intelligence[Title/Abstract]) OR (machine learning[Title/Abstract]) OR (deep learning[Title/Abstract]))',
]

# 目标期刊
HIGH_IMPACT_JOURNALS = [
    "Nature", "Nature Biotechnology", "Nature Methods", "Nature Genetics",
    "Nature Microbiology", "Nature Communications", "Nature Medicine",
    "Nature Cell Biology", "Nature Structural & Molecular Biology",
    "Nature Machine Intelligence", "Nature Cancer", "Nature Ecology & Evolution",
    "Cell", "Cell Systems", "Cell Reports", "Molecular Cell",
    "Cell Host & Microbe", "Cell Genomics", "Immunity", "Neuron",
    "Science", "Science Advances", "Science Translational Medicine",
    "Genome Biology", "Genome Research", "Bioinformatics",
    "Nucleic Acids Research", "BMC Bioinformatics", "PLOS Computational Biology",
    "Briefings in Bioinformatics", "GigaScience",
]

# 领域分类关键词
CATEGORY_KEYWORDS = {
    "单细胞组学": ["single-cell", "scRNA-seq", "scATAC-seq", "spatial transcriptomics", "单细胞"],
    "宏基因组学": ["metagenomics", "microbiome", "16S", "metatranscriptomics", "宏基因组"],
    "病原真菌": ["fungal", "fungus", "pathogen", "Candida", "Aspergillus", "Cryptococcus", "真菌", "病原"],
    "生信方法": ["bioinformatics", "algorithm", "pipeline", "tool", "method", "computational", "生信", "方法"],
    "AI/ML": ["artificial intelligence", "machine learning", "deep learning", "neural network", "transformer", "LLM", "AI", "ML"],
    "基因组学": ["genomics", "genome", "pan-genome", "structural variation", "基因组"],
    "蛋白质组学": ["proteomics", "mass spectrometry", "peptide", "protein structure", "蛋白质组"],
    "表观遗传": ["epigenetics", "methylation", "chromatin", "ATAC-seq", "ChIP-seq", "表观"],
}


def load_abstract_cache():
    """加载摘要缓存"""
    if os.path.exists(ABSTRACT_CACHE_FILE):
        try:
            with open(ABSTRACT_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def save_abstract_cache(cache):
    """保存摘要缓存"""
    try:
        os.makedirs(os.path.dirname(ABSTRACT_CACHE_FILE), exist_ok=True)
        with open(ABSTRACT_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save abstract cache: {e}")


def fetch_pubmed_abstract(pmid):
    """从 PubMed 获取单篇文献的摘要"""
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        summary_url = f"{base_url}/esummary.fcgi"
        summary_params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "json"
        }
        
        response = requests.get(summary_url, params=summary_params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        article = data.get("result", {}).get(pmid, {})
        if article:
            return {
                "title": article.get("title", ""),
                "authors": [a.get("name", "") for a in article.get("authors", [])][:5],
                "journal": article.get("source", ""),
                "pubdate": article.get("pubdate", ""),
                "abstract": article.get("fulljournalname", ""),  # 摘要需要另外获取
            }
        return None
    except Exception as e:
        print(f"Error fetching PubMed abstract for {pmid}: {e}")
        return None


def fetch_pubmed_abstracts_batch(pmids):
    """批量获取 PubMed 文献摘要"""
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        ids = ",".join(pmids)
        
        # 使用 EFetch 获取摘要
        fetch_url = f"{base_url}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ids,
            "rettype": "abstract",
            "retmode": "xml"
        }
        
        response = requests.get(fetch_url, params=fetch_params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        abstracts = {}
        
        for article in root.findall('.//PubmedArticle'):
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else None
            
            if pmid:
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else ""
                
                abstract_elem = article.find('.//AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
                
                journal_elem = article.find('.//Journal/Title')
                journal = journal_elem.text if journal_elem is not None else ""
                
                pubdate_elem = article.find('.//PubDate/Year')
                pubdate = pubdate_elem.text if pubdate_elem is not None else ""
                
                authors = []
                for author in article.findall('.//Author'):
                    last_name = author.find('LastName')
                    fore_name = author.find('ForeName')
                    if last_name is not None:
                        name = last_name.text
                        if fore_name is not None:
                            name += " " + fore_name.text
                        authors.append(name)
                
                abstracts[pmid] = {
                    "title": title,
                    "authors": authors[:5],
                    "journal": journal,
                    "pubdate": pubdate,
                    "abstract": abstract if abstract else "No abstract available"
                }
        
        return abstracts
    except Exception as e:
        print(f"Error fetching PubMed abstracts batch: {e}")
        return {}


def fetch_biorxiv_abstract(doi):
    """从 bioRxiv 获取摘要"""
    try:
        # bioRxiv API
        api_url = f"https://api.biorxiv.org/details/{doi}"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("collection"):
            item = data["collection"][0]
            return {
                "title": item.get("title", ""),
                "authors": [a.strip() for a in item.get("authors", "").split(";")[:5] if a.strip()],
                "journal": f"bioRxiv - {item.get('category', 'preprint')}",
                "pubdate": item.get("date", ""),
                "abstract": item.get("abstract", "No abstract available")
            }
        return None
    except Exception as e:
        return None


def fetch_arxiv_abstract(arxiv_id):
    """从 arXiv 获取摘要"""
    try:
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        ns = {'': 'http://www.w3.org/2005/Atom'}
        
        entry = root.find('entry', ns)
        if entry is not None:
            title_elem = entry.find('title', ns)
            title = title_elem.text if title_elem is not None else ""
            title = ' '.join(title.split())
            
            summary_elem = entry.find('summary', ns)
            abstract = summary_elem.text if summary_elem is not None else "No abstract available"
            if abstract:
                abstract = ' '.join(abstract.split())
            
            authors = [author.find('name', ns).text for author in entry.findall('author', ns) if author.find('name', ns) is not None][:5]
            
            date_elem = entry.find('published', ns)
            date = date_elem.text[:10] if date_elem is not None else ""
            
            return {
                "title": title,
                "authors": authors,
                "journal": "arXiv",
                "pubdate": date,
                "abstract": abstract
            }
        return None
    except Exception as e:
        return None


def generate_summary(abstract, title, categories):
    """基于摘要生成文献总结（100-150 字），始终使用中文格式"""
    if not abstract or abstract == "No abstract available":
        return "暂无摘要"
    
    # 如果摘要是英文，先翻译成中文格式的描述
    is_english = bool(re.match(r'^[a-zA-Z]', abstract.strip()))
    
    # 提取关键信息
    summary_parts = []
    
    # 1. 研究目的/背景
    purpose_patterns = [
        r"(?:we developed|we present|we propose|this study|here we)\s+([^.]+\.?)",
        r"(?:开发 | 提出 | 构建 | 设计 )[^\.,]+[。\.]",
    ]
    found_purpose = False
    for pattern in purpose_patterns:
        match = re.search(pattern, abstract, re.IGNORECASE)
        if match and match.group(1):
            purpose = match.group(1).strip()
            if len(purpose) < 150:
                summary_parts.append(f"{purpose}")
                found_purpose = True
                break
    
    if not found_purpose and is_english:
        # 如果是英文摘要，提取第一句作为背景描述
        first_sentence = re.split(r'[.!?]+', abstract)[0].strip()
        if first_sentence:
            summary_parts.append(f"【研究目的】{first_sentence}")
    elif not found_purpose:
        # 中文摘要直接提取相关句子
        sentences = re.split(r'[。！？]+', abstract)
        for sent in sentences[:3]:
            if any(kw in sent for kw in ["本文", "我们", "本研究", "开发", "提出"]):
                summary_parts.append(sent + "。")
                if len(summary_parts) >= 2:
                    break
    
    # 2. 方法/技术
    method_patterns = [
        r"(?:using|based on|by|with|采用 | 基于 | 利用 )[^\.,]+[。\.]",
    ]
    found_method = False
    for pattern in method_patterns:
        matches = re.findall(pattern, abstract, re.IGNORECASE)
        if matches:
            for match in matches[:1]:
                if match and len(match) < 150:
                    summary_parts.append(f"【方法】{match.strip()}")
                    found_method = True
                    break
        if found_method:
            break
    
    # 3. 主要发现/结果
    result_patterns = [
        r"(?:results show|demonstrate|reveal|indicate|suggest|found that|结果显示 | 发现 | 表明 )[^\.,]+[。\.]",
    ]
    found_result = False
    for pattern in result_patterns:
        matches = re.findall(pattern, abstract, re.IGNORECASE)
        if matches:
            for match in matches[:1]:
                if match and len(match) < 180:
                    summary_parts.append(f"【研究结果】{match.strip()}")
                    found_result = True
                    break
        if found_result:
            break
    
    # 如果没有提取到足够的信息，使用摘要的主要内容
    if len(summary_parts) < 2:
        # 提取前 2-3 个句子
        sentences = re.split(r'[.!?]+\s*', abstract)[:3]
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        if sentences:
            summary_parts = sentences[:2]
            if len(summary_parts) < 2:
                summary_parts.append("...")
    
    # 合并并截断，确保总长度不超过 250 字
    summary = " ".join(summary_parts)
    if len(summary) > 250:
        summary = summary[:247] + "..."
    
    return summary


def categorize_article(title, abstract):
    """根据标题和摘要对文献进行分类"""
    text = (title + " " + abstract).lower()
    categories = []
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            categories.append(category)
    
    return categories if categories else ["其他"]


def check_zotero_credentials():
    """检查 Zotero 凭证是否配置"""
    api_key = os.environ.get("ZOTERO_API_KEY")
    group_id = ZOTERO_GROUP_ID  # BioCiaoLab group
    return bool(api_key and group_id)


def get_zotero_collections_for_group():
    """获取 Group Library 下的所有收藏夹（按分类）"""
    try:
        env = os.environ.copy()
        if ZOTERO_GROUP_ID:
            env["ZOTERO_GROUP_ID"] = ZOTERO_GROUP_ID
        
        result = subprocess.run(
            ["python3", ZOTERO_SCRIPT, "collections", "--json"],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode != 0:
            return {}
        
        import json
        collections = json.loads(result.stdout)
        
        # 按收藏夹名称建立 key->name 映射
        coll_map = {}
        for coll in collections:
            coll_map[coll.get("key")] = coll.get("name", "")
        
        return coll_map
    except Exception as e:
        print(f"Warning: Cannot get Zotero collections: {e}")
        return {}


def add_to_zotero(articles, date_str):
    """将文献添加到 Zotero Group Library (BioCiaoLab)"""
    try:
        from pyzotero import zotero as pyzotero_module
    except ImportError:
        print("⚠️ pyzotero 未安装，跳过 Zotero 录入")
        return {"added": 0, "skipped": 0, "failed": 0}
    
    # 获取 API key 和 group id
    api_key = os.environ.get("ZOTERO_API_KEY")
    group_id = ZOTERO_GROUP_ID  # BioCiaoLab = 6489333
    
    if not api_key or not group_id:
        print("⚠️ Zotero 凭证未配置 (需要 ZOTERO_API_KEY 和 ZOTERO_GROUP_ID)，跳过 Zotero 录入")
        return {"added": 0, "skipped": 0, "failed": 0}
    
    print(f"📚 开始录入 Zotero Group Library (BioCiaoLab)...")
    
    # 使用在线 API 模式
    try:
        zot = pyzotero_module.Zotero(group_id, 'group', api_key=api_key)
        zot.num_items()  # 测试连接
    except Exception as e:
        print(f"⚠️ Zotero 连接失败: {e}，跳过 Zotero 录入")
        return {"added": 0, "skipped": 0, "failed": 0}
    
    # 获取收藏夹映射（按分类）
    collections = get_zotero_collections_for_group()
    print(f"  现有收藏夹: {list(collections.values())}")
    category_to_key = {name: key for key, name in collections.items()}
    
    # 自动创建缺失的分类收藏夹
    all_categories = set()
    for article in articles:
        cats = categorize_article(article.get("title", ""), article.get("abstract", ""))
        all_categories.update(cats)
    
    for cat in all_categories:
        if cat not in category_to_key:
            try:
                # 创建新收藏夹（注意：需要传入列表格式）
                new_coll = zot.create_collections([{"name": cat}])
                if new_coll.get("success"):
                    new_key = list(new_coll["success"].keys())[0]
                    category_to_key[cat] = new_key
                    print(f"  ✅ 已创建收藏夹: {cat}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  ⚠️ 创建收藏夹失败: {cat} - {e}")
    
    print(f"  最终收藏夹: {list(category_to_key.keys())}")
    
    added = 0
    skipped = 0
    failed = 0
    
    for article in articles:
        try:
            source = article.get("source", "")
            pmid = article.get("pmid", "")
            title = article.get("title", "")
            authors = article.get("authors", [])
            journal = article.get("journal", "")
            pubdate = article.get("pubdate", "")
            abstract = article.get("abstract", "")
            url = article.get("url", "")
            
            # 获取文献分类
            categories = categorize_article(title, abstract)
            primary_category = categories[0] if categories else None
            
            # 构建标签
            tags = [f"literature-daily", date_str] + categories
            
            # 构建作者
            creators = []
            for author in authors[:5]:
                parts = author.split()
                if len(parts) >= 2:
                    creators.append({
                        "creatorType": "author",
                        "firstName": " ".join(parts[:-1]),
                        "lastName": parts[-1]
                    })
                else:
                    creators.append({
                        "creatorType": "author",
                        "lastName": author
                    })
            
            # 构建 Zotero 条目
            item_data = {
                "itemType": "journalArticle",
                "title": title,
                "creators": creators if creators else [{"creatorType": "author", "lastName": "Unknown"}],
                "publicationTitle": journal,
                "date": pubdate,
                "abstractNote": abstract,
                "url": url,
                "tags": [{"tag": t} for t in tags]
            }
            
            # 添加 PMID
            if pmid and "PubMed" in source:
                item_data["PMID"] = pmid
            
            # 添加 DOI
            doi = article.get("doi", "")
            if not doi and article.get("pmid", "") and "10." in article.get("pmid", ""):
                doi = article.get("pmid", "")
            if doi and "10." in doi:
                item_data["DOI"] = doi
            
            # 先搜索是否已存在（基于标题匹配）
            existing = zot.items(q=title[:100], limit=1)
            if existing:
                skipped += 1
                print(f"  ⏭️ 已存在: {title[:50]}... [{primary_category}]")
                time.sleep(0.1)
                continue
            
            # 创建条目
            try:
                resp = zot.create_items([item_data])
                if resp and len(resp.get("success", {})) > 0:
                    new_key = list(resp["success"].keys())[0]
                    
                    # 添加到分类收藏夹
                    coll_key = category_to_key.get(primary_category) if primary_category else None
                    if coll_key:
                        zot.addto_collection(coll_key, new_key)
                    
                    added += 1
                    print(f"  ✅ 已添加: {title[:50]}... [{primary_category}]")
                else:
                    failed += 1
                    print(f"  ❌ 添加失败: {title[:50]}... - 创建响应异常")
            except Exception as create_err:
                if "duplicate" in str(create_err).lower():
                    skipped += 1
                    print(f"  ⏭️ 已存在: {title[:50]}... [{primary_category}]")
                else:
                    failed += 1
                    print(f"  ❌ 添加失败: {title[:50]}... - {str(create_err)[:60]}")
            
            time.sleep(0.3)  # 避免 API 限流
            
        except Exception as e:
            failed += 1
            print(f"  ❌ 添加异常: {article.get('title', '')[:50]}... - {e}")
    
    print(f"📚 Zotero (BioCiaoLab) 录入完成: 新增 {added}, 跳过 {skipped}, 失败 {failed}")
    return {"added": added, "skipped": skipped, "failed": failed}


def fetch_articles_with_abstracts(query, days_back=1, max_results=20):
    """从 PubMed 搜索并获取摘要"""
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y/%m/%d")
        date_to = datetime.now().strftime("%Y/%m/%d")
        
        search_url = f"{base_url}/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": f"({query}) AND ({date_from}[PDAT] : {date_to}[PDAT])",
            "retmax": max_results,
            "sort": "date",
            "retmode": "json"
        }
        
        response = requests.get(search_url, params=search_params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        id_list = data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return []
        
        # 批量获取摘要
        abstracts = fetch_pubmed_abstracts_batch(id_list)
        
        articles = []
        for pmid in id_list:
            if pmid in abstracts:
                info = abstracts[pmid]
                articles.append({
                    "pmid": pmid,
                    "title": info["title"],
                    "authors": info["authors"],
                    "journal": info["journal"],
                    "pubdate": info["pubdate"],
                    "abstract": info["abstract"],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "source": "PubMed"
                })
        
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []


def fetch_cns_journal_articles(days_back=3, max_results_per_journal=5):
    """专门抓取 CNS 等主流期刊的最新文章"""
    all_cns_articles = []
    
    # 构建 CNS 期刊查询 - 使用 OR 组合多个期刊
    journal_query = " OR ".join([f'"{j}"[Journal]' for j in CNS_JOURNALS])
    
    # 核心搜索词（热门领域）
    core_queries = [
        "machine learning[Title/Abstract] OR deep learning[Title/Abstract] OR artificial intelligence[Title/Abstract]",
        "bioinformatics[Title/Abstract] OR computational biology[Title/Abstract]",
        "single-cell[Title/Abstract] OR scRNA-seq[Title/Abstract] OR spatial transcriptomics[Title/Abstract]",
        "metagenomics[Title/Abstract] OR microbiome[Title/Abstract] OR microbiota[Title/Abstract]",
        "genomics[Title/Abstract] OR genome[Title/Abstract] OR proteomics[Title/Abstract]",
        "fungal[Title/Abstract] OR pathogen[Title/Abstract] OR fungus[Title/Abstract]",
    ]
    
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y/%m/%d")
        date_to = datetime.now().strftime("%Y/%m/%d")
        
        for query in core_queries:
            search_term = f"({journal_query}) AND ({query}) AND ({date_from}[PDAT] : {date_to}[PDAT])"
            
            search_url = f"{base_url}/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": search_term,
                "retmax": max_results_per_journal,
                "sort": "date",
                "retmode": "json"
            }
            
            try:
                response = requests.get(search_url, params=search_params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                id_list = data.get("esearchresult", {}).get("idlist", [])
                if id_list:
                    # 批量获取摘要
                    abstracts = fetch_pubmed_abstracts_batch(id_list)
                    
                    for pmid in id_list:
                        if pmid in abstracts:
                            info = abstracts[pmid]
                            # 检查是否已经是 CNS 期刊
                            journal = info.get("journal", "").lower()
                            is_cns = any(cns.lower() in journal for cns in CNS_JOURNALS)
                            
                            if is_cns:
                                all_cns_articles.append({
                                    "pmid": pmid,
                                    "title": info["title"],
                                    "authors": info["authors"],
                                    "journal": info["journal"],
                                    "pubdate": info["pubdate"],
                                    "abstract": info["abstract"],
                                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                                    "source": "PubMed-CNS"
                                })
                
                time.sleep(0.3)  # 避免 API 限流
            except Exception as e:
                print(f"  Warning: Failed to fetch CNS query: {e}")
                continue
    
    except Exception as e:
        print(f"Error fetching CNS articles: {e}")
    
    # 去重
    seen = set()
    unique_articles = []
    for article in all_cns_articles:
        pmid = article.get("pmid")
        if pmid not in seen:
            seen.add(pmid)
            unique_articles.append(article)
    
    return unique_articles


def fetch_biorxiv_articles_with_abstracts(days_back=1, max_results=30):
    """从 bioRxiv 获取文献和摘要"""
    try:
        date_from_str = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        date_to_str = datetime.now().strftime("%Y-%m-%d")
        
        biorxiv_api_url = f"https://api.biorxiv.org/details/biorxiv/{date_from_str}/{date_to_str}/0/json"
        response = requests.get(biorxiv_api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        collection = data.get("collection", [])
        keywords = ["metagenomics", "fungal", "pathogen", "bioinformatic", "machine learning", 
                   "deep learning", "artificial intelligence", "genomic", "single-cell", 
                   "neural network", "algorithm", "computational", "microbiome"]
        
        articles = []
        for item in collection:
            title = item.get("title", "")
            abstract = item.get("abstract", "")
            title_lower = title.lower()
            abstract_lower = abstract.lower()
            
            if any(kw in title_lower or kw in abstract_lower for kw in keywords):
                authors_str = item.get("authors", "")
                authors = [a.strip() for a in authors_str.split(";")[:5] if a.strip()]
                
                articles.append({
                    "pmid": item.get("doi", ""),
                    "title": title,
                    "authors": authors,
                    "journal": f"bioRxiv - {item.get('category', 'preprint')}",
                    "pubdate": item.get("date", ""),
                    "abstract": abstract if abstract else "No abstract available",
                    "url": item.get("biorxiv_url", f"https://doi.org/{item.get('doi', '')}"),
                    "source": "bioRxiv"
                })
        
        # 获取后续页面
        total = data.get("messages", [{}])[0].get("total", 0)
        cursor = 0
        while len(articles) < max_results and cursor < min(total, 100):
            cursor += 30
            next_url = f"https://api.biorxiv.org/details/biorxiv/{date_from_str}/{date_to_str}/{cursor}/json"
            try:
                next_response = requests.get(next_url, timeout=30)
                next_response.raise_for_status()
                next_data = next_response.json()
                next_collection = next_data.get("collection", [])
                
                for item in next_collection:
                    title = item.get("title", "")
                    abstract = item.get("abstract", "")
                    title_lower = title.lower()
                    abstract_lower = abstract.lower()
                    
                    if any(kw in title_lower or kw in abstract_lower for kw in keywords):
                        authors_str = item.get("authors", "")
                        authors = [a.strip() for a in authors_str.split(";")[:5] if a.strip()]
                        
                        articles.append({
                            "pmid": item.get("doi", ""),
                            "title": title,
                            "authors": authors,
                            "journal": f"bioRxiv - {item.get('category', 'preprint')}",
                            "pubdate": item.get("date", ""),
                            "abstract": abstract if abstract else "No abstract available",
                            "url": item.get("biorxiv_url", f"https://doi.org/{item.get('doi', '')}"),
                            "source": "bioRxiv"
                        })
            except Exception:
                break
        
        return articles
    except Exception as e:
        print(f"Error fetching from bioRxiv: {e}")
        return []


def fetch_arxiv_articles_with_abstracts(days_back=1, max_results=20):
    """从 arXiv 获取文献和摘要"""
    try:
        date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        date_to = datetime.now().strftime("%Y%m%d")
        submitted_date_filter = f"submittedDate:[{date_from}0000 TO {date_to}2359]"
        query = quote(f"((cat:q-bio OR cat:cs.AI OR cat:cs.LG) AND (machine learning OR deep learning OR bioinformatics OR metagenomics)) AND {submitted_date_filter}")
        url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        ns = {'': 'http://www.w3.org/2005/Atom'}
        
        articles = []
        for entry in root.findall('entry', ns):
            title_elem = entry.find('title', ns)
            title = title_elem.text if title_elem is not None else ""
            title = ' '.join(title.split())
            
            summary_elem = entry.find('summary', ns)
            abstract = summary_elem.text if summary_elem is not None else "No abstract available"
            if abstract:
                abstract = ' '.join(abstract.split())
            
            authors = [author.find('name', ns).text for author in entry.findall('author', ns) if author.find('name', ns) is not None][:5]
            
            id_elem = entry.find('id', ns)
            url = id_elem.text if id_elem is not None else ""
            
            date_elem = entry.find('published', ns)
            date = date_elem.text[:10] if date_elem is not None else ""
            
            articles.append({
                "pmid": url.split('/')[-1] if url else "",
                "title": title,
                "authors": authors,
                "journal": "arXiv",
                "pubdate": date,
                "abstract": abstract,
                "url": url,
                "source": "arXiv"
            })
        
        return articles
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
        return []


def select_featured_articles(articles, max_featured=8):
    """选择重点推荐文章（基于期刊影响力、相关性等）"""
    # 优先级评分
    def score_article(article):
        score = 0
        journal = article.get("journal", "").lower()
        title = article.get("title", "").lower()
        abstract = article.get("abstract", "").lower()
        
        # 高影响力期刊加分
        high_impact = ["nature", "science", "cell", "genome biology", "genome research", 
                      "nature biotechnology", "nature methods", "molecular cell"]
        if any(hij in journal for hij in high_impact):
            score += 10
        
        # 方法开发加分
        method_keywords = ["method", "tool", "pipeline", "framework", "algorithm", "software"]
        if any(mk in title or mk in abstract for mk in method_keywords):
            score += 5
        
        # 单细胞/AI 加分
        hot_topics = ["single-cell", "deep learning", "transformer", "foundation model"]
        if any(ht in title or ht in abstract for ht in hot_topics):
            score += 3
        
        return score
    
    # 排序并选择
    scored = sorted(articles, key=score_article, reverse=True)
    return scored[:max_featured]


def generate_editorial_intro(articles, date_str):
    """生成编辑前言"""
    total = len(articles)
    sources = {}
    categories = set()
    cns_count = 0
    
    for article in articles:
        source = article.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + 1
        
        # 统计 CNS 文献
        journal = article.get("journal", "").lower()
        if any(cns.lower() in journal for cns in CNS_JOURNALS):
            cns_count += 1
        
        # 分类统计
        cats = categorize_article(article.get("title", ""), article.get("abstract", ""))
        categories.update(cats)
    
    intro = f"""## 📰 编辑前言

**日期**: {date_str}

今日共追踪到 **{total}** 篇与生命科学×AI 交叉领域相关的新文献。

"""
    
    # CNS 特别提示
    if cns_count > 0:
        intro += f"> 🎯 **CNS 核心期刊**: {cns_count} 篇（Nature/Cell/Science 系列，近3天）\n\n"
    
    intro += """**来源分布**：
"""
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        intro += f"- {source}: {count} 篇\n"
    
    intro += f"""
**热点领域**：
{', '.join(list(categories)[:6]) if categories else '广泛领域'}

今日研究热点集中在 """ + "、".join(list(categories)[:4]) + """等方向。以下为您精选重点文献和详细解读。

---

"""
    return intro


def generate_daily_summary(articles):
    """生成每日总结"""
    if not articles:
        return "## 📝 编辑总结\n\n今日暂无新文献匹配筛选条件。"
    
    # 统计趋势
    categories_count = {}
    for article in articles:
        cats = categorize_article(article.get("title", ""), article.get("abstract", ""))
        for cat in cats:
            categories_count[cat] = categories_count.get(cat, 0) + 1
    
    # 找出最热门的 3 个领域
    top_categories = sorted(categories_count.items(), key=lambda x: -x[1])[:3]
    
    # 生成总结
    summary = """## 📝 编辑总结

### 今日趋势
"""
    for cat, count in top_categories:
        emoji = {"单细胞组学": "🧫", "宏基因组学": "🧬", "AI/ML": "🤖", 
                "生信方法": "🔧", "基因组学": "🧬", "病原真菌": "🍄"}.get(cat, "📌")
        summary += f"{emoji} **{cat}**: {count} 篇文献\n"
    
    summary += """
### 编者点评

"""
    
    # 根据文献内容生成点评
    if any("single-cell" in (a.get("title", "") + a.get("abstract", "")).lower() for a in articles):
        summary += "单细胞技术持续火热，多项新方法涌现，特别是在空间转录组和整合分析方向。\n\n"
    
    if any("machine learning" in (a.get("title", "") + a.get("abstract", "")).lower() or 
           "deep learning" in (a.get("title", "") + a.get("abstract", "")).lower() for a in articles):
        summary += "AI/ML 在生物信息学中的应用进一步深入，从传统的分类预测向生成模型和基础模型演进。\n\n"
    
    if any("method" in a.get("title", "").lower() or "tool" in a.get("title", "").lower() for a in articles):
        summary += "方法学开发活跃，多个新工具和流程发布，建议关注开源实现和基准测试。\n\n"
    
    summary += """**建议**：重点关注高影响力期刊的方法学论文和 bioRxiv 上的预印本，及时追踪领域前沿。

---
"""
    return summary


def generate_mark_report_v2(articles, date_str):
    """生成 Markdown 报告（v2.0 版本 - 带摘要和总结）"""
    
    # 1. 编辑前言
    report = f"""# 📚 每日文献速递 - {date_str}

"""
    report += generate_editorial_intro(articles, date_str)
    
    # 1.5 CNS 专区和预览（如果有 CNS 文章）
    cns_articles = [a for a in articles if any(cns.lower() in a.get("journal", "").lower() for cns in CNS_JOURNALS)]
    if cns_articles:
        report += """## 🏆 CNS 核心期刊精选

以下为今日 CNS（Nature/Cell/Science）系列期刊发表的相关研究：

"""
        for i, article in enumerate(cns_articles[:5], 1):
            title = article.get("title", "")
            authors = ", ".join(article.get("authors", [])[:3])
            if len(article.get("authors", [])) > 3:
                authors += " et al."
            journal = article.get("journal", "")
            pubdate = article.get("pubdate", "")
            url = article.get("url", "")
            abstract = article.get("abstract", "No abstract available")
            
            summary = generate_summary(abstract, title, [])
            
            report += f"""### {i}. {title}

**作者**: {authors}  
**期刊**: 🏆 **{journal}** | **发表日期**: {pubdate}  
**链接**: [{url}]({url})

**📋 核心总结**: {summary}

---

"""
    
    # 2. 重点推荐（带摘要和总结）
    # 优先选择 CNS 文章
    featured = select_featured_articles(articles, max_featured=8)
    if featured:
        report += """## ⭐ 重点推荐

以下为您精选今日最具价值的文献，附详细解读：

"""
        for i, article in enumerate(featured, 1):
            title = article.get("title", "")
            authors = ", ".join(article.get("authors", [])[:3])
            if len(article.get("authors", [])) > 3:
                authors += " et al."
            journal = article.get("journal", "")
            pubdate = article.get("pubdate", "")
            url = article.get("url", "")
            abstract = article.get("abstract", "No abstract available")
            
            # 分类标签
            categories = categorize_article(title, abstract)
            tags = " | ".join([f"`{cat}`" for cat in categories[:3]])
            
            # 生成总结
            summary = generate_summary(abstract, title, categories)
            
            report += f"""### {i}. {title}

{tags}

**作者**: {authors}  
**期刊**: {journal} | **发表日期**: {pubdate}  
**链接**: [{url}]({url})

**📋 核心总结**: {summary}

---

"""
    
    # 3. 完整文献列表
    report += """## 📖 完整文献列表

"""
    
    # 按来源分组
    sources = {}
    for article in articles:
        source = article.get("source", "Unknown")
        if source not in sources:
            sources[source] = []
        sources[source].append(article)
    
    for source, items in sorted(sources.items(), key=lambda x: -len(x[1])):
        # 跳过已经在重点推荐中出现的文章
        featured_titles = {a.get("title", "") for a in featured}
        other_items = [a for a in items if a.get("title", "") not in featured_titles]
        
        if not other_items:
            continue
        
        report += f"### {source} ({len(other_items)} 篇)\n\n"
        for i, article in enumerate(other_items, 1):
            title = article.get("title", "")
            authors = ", ".join(article.get("authors", [])[:3])
            if len(article.get("authors", [])) > 3:
                authors += " et al."
            journal = article.get("journal", "")
            pubdate = article.get("pubdate", "")[:10]
            url = article.get("url", "")
            abstract = article.get("abstract", "No abstract available")
            
            # 生成简短总结
            summary = generate_summary(abstract, title, [])
            
            report += f"**{i}. {title}**\n"
            report += f"- 作者：{authors}\n" if authors else ""
            report += f"- 期刊：{journal}\n" if journal else ""
            report += f"- 日期：{pubdate}\n" if pubdate else ""
            report += f"- 链接：{url}\n"
            report += f"- **摘要**: {summary}\n"
            report += "\n"
    
    # 4. 编辑总结
    report += generate_daily_summary(articles)
    
    # 5. 页脚
    report += f"""*报告生成时间*: {datetime.now().strftime("%Y-%m-%d %H:%M")}

*筛选领域*:
- 宏基因组学 × AI/ML
- 病原真菌学 × 生物信息
- 生物信息方法开发 × AI
- 单细胞组学 × 计算方法
- 基因组学 × 机器学习
"""
    
    return report


def main():
    """主函数"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"🤖 开始收集 {today} 的文献...")
    
    all_articles = []
    
    # 从 CNS 期刊抓取（优先，搜索最近 3 天）
    print("🔍 搜索 CNS 主流期刊 (Nature/Cell/Science 系列)...")
    cns_articles = fetch_cns_journal_articles(days_back=3, max_results_per_journal=5)
    all_articles.extend(cns_articles)
    print(f"  - 找到 {len(cns_articles)} 篇 CNS 文献")
    
    # 从 PubMed 搜索（搜索最近 2 天）
    print("🔍 搜索 PubMed...")
    for query in SEARCH_QUERIES:
        articles = fetch_articles_with_abstracts(query, days_back=2, max_results=20)
        all_articles.extend(articles)
        print(f"  - 找到 {len(articles)} 篇")
        time.sleep(0.5)  # 避免 API 限流
    
    # 从 bioRxiv 搜索
    print("🔍 搜索 bioRxiv...")
    biorxiv_articles = fetch_biorxiv_articles_with_abstracts(days_back=1, max_results=30)
    all_articles.extend(biorxiv_articles)
    print(f"  - 找到 {len(biorxiv_articles)} 篇")
    
    # 从 arXiv 搜索
    print("🔍 搜索 arXiv...")
    arxiv_articles = fetch_arxiv_articles_with_abstracts(days_back=1, max_results=20)
    all_articles.extend(arxiv_articles)
    print(f"  - 找到 {len(arxiv_articles)} 篇")
    
    # 去重（基于标题）
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title = article.get("title") if article else None
        if not title:
            continue
        title_norm = re.sub(r'[^\w]', '', title.lower())
        if title_norm and title_norm not in seen_titles:
            seen_titles.add(title_norm)
            unique_articles.append(article)
    
    print(f"\n✅ 总共找到 {len(unique_articles)} 篇唯一文献")
    
    # 生成报告（v2.0）
    report = generate_mark_report_v2(unique_articles, today)
    
    # 保存报告
    output_file = os.path.join(OUTPUT_DIR, f"literature-{today}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📝 报告已保存：{output_file}")
    
    # 同时更新最新报告
    latest_file = os.path.join(OUTPUT_DIR, "latest.md")
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 复制到 ClawLib 科研日报目录
    clawlib_dir = os.path.expanduser("~/.openclaw/workspace/ClawLib/科研日报")
    try:
        import shutil
        shutil.copy2(output_file, os.path.join(clawlib_dir, f"literature-{today}.md"))
        shutil.copy2(latest_file, os.path.join(clawlib_dir, "latest.md"))
        print(f"📚 已同步到 ClawLib：{clawlib_dir}")
    except Exception as e:
        print(f"⚠️ ClawLib 同步失败：{e}")
    
    # 录入 Zotero
    zotero_result = add_to_zotero(unique_articles, today)
    
    # 发送到 Matrix
    print("📤 发送报告到 Matrix...")
    try:
        from message import message
        message(action="send", channel="matrix", message=report)
        print("✅ 文献日报已成功发送到 Matrix")
    except Exception as e:
        print(f"⚠️ Matrix 发送失败：{e}")
    
    # 输出摘要
    print(f"\n📋 今日文献摘要:")
    sources_count = {}
    for article in unique_articles:
        source = article.get("source", "Unknown")
        sources_count[source] = sources_count.get(source, 0) + 1
    
    for source, count in sources_count.items():
        print(f"  - {source}: {count} 篇")
    
    zotero_status = f", Zotero 录入 {zotero_result['added']} 篇" if zotero_result['added'] > 0 or zotero_result['skipped'] > 0 else ""
    print(f"\n✨ v2.0 功能：已为每篇文献生成摘要总结，并添加编辑前言和总结部分{zotero_status}")


if __name__ == "__main__":
    main()