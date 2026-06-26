#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCF 评级与发表状态查询测试文件

快速测试论文发表状态查询和 CCF 评级功能

使用方法:
    python scripts/test_publication_status.py

或测试特定论文:
    python scripts/test_publication_status.py --title "论文标题" --venue "期刊/会议名称"
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.core.publication_status import (
    get_publication_status,
    calculate_authority_score,
    _normalize_venue_name,
    _check_ccf_rank,
    CCF_A_JOURNALS,
    CCF_B_JOURNALS,
    CCF_C_JOURNALS,
    CCF_A_CONFERENCES,
    CCF_B_CONFERENCES,
    CCF_C_CONFERENCES,
)


# =========================
# 测试用例
# =========================

TEST_CASES = [
    # 真实论文测试案例（端到端测试）
    {
        "title": "Latent Watermark: Inject and Detect Watermarks in Latent Diffusion Space",
        "venue": "IEEE Transactions on Multimedia",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "【真实论文】IEEE TMM - CCF-B 期刊"
    },
    {
        "title": "Watermarking Makes Language Models Radioactive",
        "venue": "ICML",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "【真实论文】ICML - CCF-A 会议"
    },
    {
        "title": "A Certified Robust Watermark For Large Language Models",
        "venue": "",
        "source": "arxiv",
        "url": "https://arxiv.org/abs/2401.12345",
        "expected_ccf": "",
        "expected_type": "preprint",
        "description": "【真实论文】arXiv 预印本"
    },
    
    # ==================== CCF-A 类期刊测试 ====================
    {
        "title": "Test TPAMI",
        "venue": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：IEEE TPAMI"
    },
    {
        "title": "Test IJCV",
        "venue": "International Journal of Computer Vision",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：IJCV"
    },
    {
        "title": "Test JMLR",
        "venue": "Journal of Machine Learning Research",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：JMLR"
    },
    {
        "title": "Test AI Journal",
        "venue": "Artificial Intelligence",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：Artificial Intelligence"
    },
    {
        "title": "Test TACL",
        "venue": "Transactions of the Association for Computational Linguistics",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：TACL"
    },
    {
        "title": "Test TIP",
        "venue": "IEEE Transactions on Image Processing",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "journal",
        "description": "CCF-A 期刊：IEEE TIP"
    },
    {
        "title": "Test TMM",
        "venue": "IEEE Transactions on Multimedia",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "CCF-B 期刊：IEEE TMM"
    },
    
    # ==================== CCF-B 类期刊测试 ====================
    {
        "title": "Test TNNLS",
        "venue": "IEEE Transactions on Neural Networks and Learning Systems",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "CCF-B 期刊：IEEE TNNLS"
    },
    {
        "title": "Test Neural Networks",
        "venue": "Neural Networks",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "CCF-B 期刊：Neural Networks"
    },
    {
        "title": "Test Pattern Recognition",
        "venue": "Pattern Recognition",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "CCF-B 期刊：Pattern Recognition"
    },
    {
        "title": "Test KAIS",
        "venue": "Knowledge and Information Systems",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "journal",
        "description": "CCF-B 期刊：KAIS"
    },
    
    # ==================== CCF-C 类期刊测试 ====================
    {
        "title": "Test NPL",
        "venue": "Neural Processing Letters",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "journal",
        "description": "CCF-C 期刊：Neural Processing Letters"
    },
    {
        "title": "Test PR Letters",
        "venue": "Pattern Recognition Letters",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "journal",
        "description": "CCF-C 期刊：Pattern Recognition Letters"
    },
    {
        "title": "Test ESWA",
        "venue": "Expert Systems with Applications",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "journal",
        "description": "CCF-C 期刊：ESWA"
    },
    {
        "title": "Test Neurocomputing",
        "venue": "Neurocomputing",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "journal",
        "description": "CCF-C 期刊：Neurocomputing"
    },
    
    # ==================== CCF-A 类会议测试 ====================
    {
        "title": "Test CVPR",
        "venue": "CVPR",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：CVPR"
    },
    {
        "title": "Test NeurIPS",
        "venue": "NeurIPS",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：NeurIPS"
    },
    {
        "title": "Test ICML",
        "venue": "ICML",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ICML"
    },
    {
        "title": "Test ICLR",
        "venue": "ICLR",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ICLR"
    },
    {
        "title": "Test ACL",
        "venue": "ACL",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ACL"
    },
    {
        "title": "Test EMNLP",
        "venue": "EMNLP",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：EMNLP"
    },
    {
        "title": "Test ICCV",
        "venue": "ICCV",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ICCV"
    },
    {
        "title": "Test ECCV",
        "venue": "ECCV",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ECCV"
    },
    {
        "title": "Test AAAI",
        "venue": "AAAI",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：AAAI"
    },
    {
        "title": "Test IJCAI",
        "venue": "IJCAI",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：IJCAI"
    },
    {
        "title": "Test KDD",
        "venue": "KDD",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：KDD"
    },
    {
        "title": "Test SIGMOD",
        "venue": "SIGMOD",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：SIGMOD"
    },
    {
        "title": "Test VLDB",
        "venue": "VLDB",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：VLDB"
    },
    {
        "title": "Test ICDE",
        "venue": "ICDE",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ICDE"
    },
    {
        "title": "Test SIGIR",
        "venue": "SIGIR",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：SIGIR"
    },
    {
        "title": "Test WWW",
        "venue": "The Web Conference",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：WWW"
    },
    {
        "title": "Test CCS",
        "venue": "CCS",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：CCS"
    },
    {
        "title": "Test S&P",
        "venue": "IEEE Symposium on Security and Privacy",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：IEEE S&P (Oakland)"
    },
    {
        "title": "Test USENIX Security",
        "venue": "USENIX Security Symposium",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：USENIX Security"
    },
    {
        "title": "Test NDSS",
        "venue": "NDSS",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：NDSS"
    },
    {
        "title": "Test ICSE",
        "venue": "ICSE",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ICSE"
    },
    {
        "title": "Test FSE",
        "venue": "FSE",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：FSE/SIGSOFT"
    },
    {
        "title": "Test ISSTA",
        "venue": "ISSTA",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：ISSTA"
    },
    {
        "title": "Test PLDI",
        "venue": "PLDI",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：PLDI"
    },
    {
        "title": "Test POPL",
        "venue": "POPL",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：POPL"
    },
    {
        "title": "Test OSDI",
        "venue": "OSDI",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：OSDI"
    },
    {
        "title": "Test SOSP",
        "venue": "SOSP",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：SOSP"
    },
    {
        "title": "Test SIGCOMM",
        "venue": "SIGCOMM",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：SIGCOMM"
    },
    {
        "title": "Test INFOCOM",
        "venue": "INFOCOM",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：INFOCOM"
    },
    {
        "title": "Test MobiCom",
        "venue": "MobiCom",
        "source": "semantic",
        "expected_ccf": "A",
        "expected_type": "conference",
        "description": "CCF-A 会议：MobiCom"
    },
    
    # ==================== CCF-B 类会议测试 ====================
    {
        "title": "Test WACV",
        "venue": "WACV",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：WACV"
    },
    {
        "title": "Test CIKM",
        "venue": "CIKM",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：CIKM"
    },
    {
        "title": "Test RecSys",
        "venue": "RecSys",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：RecSys"
    },
    {
        "title": "Test ECIR",
        "venue": "ECIR",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ECIR"
    },
    {
        "title": "Test ICDT",
        "venue": "ICDT",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ICDT"
    },
    {
        "title": "Test EDBT",
        "venue": "EDBT",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：EDBT"
    },
    {
        "title": "Test ICANN",
        "venue": "ICANN",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ICANN"
    },
    {
        "title": "Test ICONIP",
        "venue": "ICONIP",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ICONIP"
    },
    {
        "title": "Test ACCV",
        "venue": "ACCV",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ACCV"
    },
    {
        "title": "Test BMVC",
        "venue": "BMVC",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：BMVC"
    },
    {
        "title": "Test ICIP",
        "venue": "ICIP",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ICIP"
    },
    {
        "title": "Test ConLL",
        "venue": "CoNLL",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：CoNLL"
    },
    {
        "title": "Test ASIACRYPT",
        "venue": "ASIACRYPT",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ASIACRYPT"
    },
    {
        "title": "Test ESORICS",
        "venue": "ESORICS",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ESORICS"
    },
    {
        "title": "Test ACSAC",
        "venue": "ACSAC",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：ACSAC"
    },
    {
        "title": "Test DSN",
        "venue": "DSN",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：DSN"
    },
    {
        "title": "Test RAID",
        "venue": "RAID",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：RAID"
    },
    {
        "title": "Test CHES",
        "venue": "CHES",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：CHES"
    },
    {
        "title": "Test TCC",
        "venue": "TCC",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：TCC"
    },
    {
        "title": "Test PKC",
        "venue": "PKC",
        "source": "semantic",
        "expected_ccf": "B",
        "expected_type": "conference",
        "description": "CCF-B 会议：PKC"
    },
    
    # ==================== CCF-C 类会议测试 ====================
    {
        "title": "Test IJCNN",
        "venue": "IJCNN",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：IJCNN"
    },
    {
        "title": "Test ICPR",
        "venue": "ICPR",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：ICPR"
    },
    {
        "title": "Test DASFAA",
        "venue": "DASFAA",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：DASFAA"
    },
    {
        "title": "Test APWeb",
        "venue": "APWeb",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：APWeb"
    },
    {
        "title": "Test ICC",
        "venue": "ICC",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：ICC"
    },
    {
        "title": "Test GLOBECOM",
        "venue": "GLOBECOM",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：GLOBECOM"
    },
    {
        "title": "Test LCN",
        "venue": "LCN",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：LCN"
    },
    {
        "title": "Test ACNS",
        "venue": "ACNS",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：ACNS"
    },
    {
        "title": "Test AsiaCCS",
        "venue": "AsiaCCS",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：AsiaCCS"
    },
    {
        "title": "Test ICICS",
        "venue": "ICICS",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：ICICS"
    },
    {
        "title": "Test TrustCom",
        "venue": "TrustCom",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：TrustCom"
    },
    {
        "title": "Test ICISP",
        "venue": "ACISP",
        "source": "semantic",
        "expected_ccf": "C",
        "expected_type": "conference",
        "description": "CCF-C 会议：ACISP"
    },
    
    # ==================== 预印本测试 ====================
    {
        "title": "Test arXiv Preprint",
        "venue": "",
        "source": "arxiv",
        "url": "https://arxiv.org/abs/2401.12345",
        "expected_ccf": "",
        "expected_type": "preprint",
        "description": "预印本：arXiv 无发表 venue"
    },
    
    # ==================== 未评级期刊/会议测试 ====================
    {
        "title": "Test Unknown Journal",
        "venue": "Journal of Unknown Research",
        "source": "semantic",
        "expected_ccf": "",
        "expected_type": "journal",
        "description": "未评级期刊"
    },
    {
        "title": "Test Unknown Conference",
        "venue": "International Conference on Unknown Topics",
        "source": "semantic",
        "expected_ccf": "",
        "expected_type": "conference",
        "description": "未评级会议"
    },
]


def run_tests():
    """运行所有测试用例"""
    print("=" * 70)
    print("CCF 评级与发表状态查询 - 测试套件")
    print("=" * 70)
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"[{i}/{len(TEST_CASES)}] {test['description']}")
        print(f"  论文：{test['title']}")
        print(f"  Venue: {test['venue'] or '(无)'}")
        
        paper = {
            "title": test["title"],
            "venue": test.get("venue", ""),
            "source": test.get("source", "semantic"),
            "url": test.get("url", ""),
        }
        
        result = get_publication_status(paper, use_api=False)
        
        # 检查 CCF 评级
        ccf_match = result["ccf_rank"] == test["expected_ccf"]
        type_match = result["publication_type"] == test["expected_type"]
        
        is_preprint_correct = result["is_preprint"] == (test["expected_type"] == "preprint")
        
        if ccf_match and type_match and is_preprint_correct:
            print(f"  ✅ PASS")
            print(f"     CCF-{result['ccf_rank'] or '未评级'} | 类型：{result['publication_type']} | 权威度：{calculate_authority_score(result):.2f}")
            passed += 1
        else:
            print(f"  ❌ FAIL")
            print(f"     期望：CCF-{test['expected_ccf'] or '未评级'} | 类型：{test['expected_type']}")
            print(f"     实际：CCF-{result['ccf_rank'] or '未评级'} | 类型：{result['publication_type']}")
            print(f"     预印本：{result['is_preprint']} (期望：{test['expected_type'] == 'preprint'})")
            failed += 1
        
        print()
    
    print("=" * 70)
    print(f"测试结果：{passed} 通过 / {failed} 失败 / {passed + failed} 总计")
    print("=" * 70)
    
    if failed > 0:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查 CCF 数据库或匹配逻辑")
        return False
    else:
        print(f"\n✅ 所有测试通过！")
        return True


def test_venue_normalization():
    """测试 venue 名称标准化"""
    print("\n" + "=" * 70)
    print("Venue 名称标准化测试")
    print("=" * 70)
    
    test_venues = [
        ("IEEE Transactions on Multimedia", "ieee transactions multimedia"),
        ("The International Conference on Computer Vision", "conference computer vision"),
        ("Neural Information Processing Systems", "neural information processing systems"),
        ("", ""),
        (None, ""),
    ]
    
    for input_venue, expected in test_venues:
        result = _normalize_venue_name(input_venue)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{input_venue}' → '{result}' (期望：'{expected}')")


def test_ccf_database():
    """显示当前 CCF 数据库统计"""
    print("\n" + "=" * 70)
    print("CCF 数据库统计")
    print("=" * 70)
    
    print(f"\n会议:")
    print(f"  CCF-A: {len(CCF_A_CONFERENCES)} 个")
    print(f"  CCF-B: {len(CCF_B_CONFERENCES)} 个")
    print(f"  CCF-C: {len(CCF_C_CONFERENCES)} 个")
    
    print(f"\n期刊:")
    print(f"  CCF-A: {len(CCF_A_JOURNALS)} 个")
    print(f"  CCF-B: {len(CCF_B_JOURNALS)} 个")
    print(f"  CCF-C: {len(CCF_C_JOURNALS)} 个")
    
    print(f"\n总计：{len(CCF_A_CONFERENCES) + len(CCF_B_CONFERENCES) + len(CCF_C_CONFERENCES) + len(CCF_A_JOURNALS) + len(CCF_B_JOURNALS) + len(CCF_C_JOURNALS)} 个 venue")


def interactive_test():
    """交互式测试单篇论文"""
    print("\n" + "=" * 70)
    print("交互式测试 - 输入论文信息")
    print("=" * 70)
    
    title = input("\n论文标题：")
    venue = input("发表 venue (期刊/会议名称): ")
    source = input("来源 (arxiv/semantic，默认 semantic): ") or "semantic"
    url = input("论文 URL (可选): ")
    
    paper = {
        "title": title,
        "venue": venue,
        "source": source,
        "url": url,
    }
    
    result = get_publication_status(paper, use_api=False)
    
    print("\n" + "-" * 50)
    print("查询结果:")
    print(f"  预印本：{'是' if result['is_preprint'] else '否'}")
    print(f"  发表 venue: {result['publication'] or '无'}")
    print(f"  CCF 评级：{result['ccf_rank'] or '未评级'}")
    print(f"  类型：{result['publication_type']}")
    print(f"  置信度：{result['confidence']}")
    print(f"  权威度分数：{calculate_authority_score(result):.2f}")
    print("-" * 50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CCF 评级与发表状态查询测试")
    parser.add_argument("--run-tests", action="store_true", help="运行完整测试套件")
    parser.add_argument("--show-db", action="store_true", help="显示 CCF 数据库统计")
    parser.add_argument("--test-venue-norm", action="store_true", help="测试 venue 名称标准化")
    parser.add_argument("--interactive", action="store_true", help="交互式测试单篇论文")
    parser.add_argument("--title", type=str, help="测试特定论文标题")
    parser.add_argument("--venue", type=str, help="测试特定 venue")
    
    args = parser.parse_args()
    
    # 默认行为：运行所有测试
    if not any([args.run_tests, args.show_db, args.test_venue_norm, args.interactive, args.title]):
        args.run_tests = True
    
    if args.run_tests:
        success = run_tests()
        sys.exit(0 if success else 1)
    
    if args.show_db:
        test_ccf_database()
    
    if args.test_venue_norm:
        test_venue_normalization()
    
    if args.interactive:
        interactive_test()
    
    if args.title:
        paper = {
            "title": args.title,
            "venue": args.venue or "",
            "source": "semantic",
        }
        result = get_publication_status(paper, use_api=False)
        print(f"\n论文：{args.title}")
        print(f"Venue: {args.venue or '(无)'}")
        print(f"结果：CCF-{result['ccf_rank'] or '未评级'} | 类型：{result['publication_type']} | 权威度：{calculate_authority_score(result):.2f}")
