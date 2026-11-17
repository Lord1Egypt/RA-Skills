import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from card_cleaner import (
    build_knowledge_points,
    clean_authors,
    clean_card,
    clean_title,
    title_is_placeholder,
)


def test_clean_title_falls_back_to_source_file_for_bullet_placeholder():
    source_file = "王琦教授治疗气郁质失眠经验_郑璐玉.pdf"
    assert title_is_placeholder("• 1853 •")
    assert clean_title("• 1853 •", source_file) == "王琦教授治疗气郁质失眠经验"


def test_clean_title_falls_back_for_citation_like_header():
    source_file = "7 Machine learning-assisted rapid determination for traditional Chinese Medicine Constitution.pdf"
    title = "Sun et al. Chinese Medicine (2024) 19:127"
    assert title_is_placeholder(title)
    assert clean_title(title, source_file) == "Machine learning assisted rapid determination for traditional Chinese Medicine Constitution"


def test_clean_authors_removes_institutions_and_prefers_filename_author_when_noisy():
    authors = [
        "王济",
        "北京市朝阳区北三环东路号北京中医药大学国家中医体质与治未病研究院",
        "邮编：",
        "电话：-",
    ]
    source_file = "中医体质辨识客观化研究进展_蔡煜阳.pdf"
    assert clean_authors(authors, source_file=source_file, title="• 6611 •") == ["蔡煜阳"]


def test_build_knowledge_points_prefers_specific_content():
    card = {
        "source_type": "clinical_experience",
        "knowledge_points": [
            {"category": "theory", "content": "本文涉及气郁质相关研究", "importance": "high", "evidence_level": "B"}
        ],
        "clinical_insights": "体质辨识的客观化让辨体从主观走向客观，是精准运用体质学防治疾病的基础。",
        "diagnostic_approach": {"key_points": "辨证要点强调辨体-辨病-辨证相结合。"},
        "treatment_approach": {"principle": "疏肝解郁", "main_formula": "二陈汤", "herbs": ["柴胡", "当归"]},
        "evidence_sentences": [],
        "conclusions": "",
        "abstract": "",
        "related_constitutions": ["气郁质"],
        "related_diseases": ["失眠"],
    }

    points = build_knowledge_points(card)
    contents = [point["content"] for point in points]

    assert all("本文涉及" not in content for content in contents)
    assert any("辨证要点" in content for content in contents)
    assert any("治疗原则" in content for content in contents)
    assert any("核心方药" in content for content in contents)


def test_clean_card_updates_multiple_fields():
    card = {
        "card_id": "WQ-EXP-999",
        "source_type": "clinical_experience",
        "source_file": "王琦教授治疗气郁质失眠经验_郑璐玉.pdf",
        "title": "• 1853 •",
        "authors": ["王琦", "电话：-", "北京市朝阳区北三环东路号北京中医药大学号信箱"],
        "clinical_insights": "王琦教授治疗气郁质失眠强调辨体-辨病-辨证相结合。",
        "knowledge_points": [{"category": "theory", "content": "本文涉及气郁质相关研究"}],
        "evidence_sentences": [],
        "related_constitutions": ["气郁质", "气郁质"],
        "related_diseases": ["失眠"],
    }

    cleaned, report = clean_card(card)

    assert cleaned["title"] == "王琦教授治疗气郁质失眠经验"
    assert "title" in report["changed_fields"]
    assert cleaned["related_constitutions"] == ["气郁质"]
    assert cleaned["knowledge_points"]
