import pytest

from hr_recruitment_onboarding_skill.services.jd_renderer import render_jd
from hr_recruitment_onboarding_skill.services.rule_based_extractor import RuleBasedExtractor


def test_extracts_java_requirements():
    result = RuleBasedExtractor().extract(
        "本科以上，3年以上Java开发经验，熟悉Spring Boot、MySQL和Redis，具备企业系统开发经验。"
    )

    assert result["education"] == "本科及以上"
    assert result["experience_years"] == 3
    assert result["required_skills"] == ["Java", "Spring Boot", "MySQL", "Redis"]


def test_requirements_use_exact_six_key_schema():
    result = RuleBasedExtractor().extract("熟悉Python，能够独立交付。")

    assert list(result) == [
        "education",
        "experience_years",
        "required_skills",
        "preferred_skills",
        "responsibilities",
        "other_requirements",
    ]


@pytest.mark.parametrize(
    "discriminatory_requirement",
    [
        "男性优先",
        "女性优先",
        "限35岁以下",
        "已婚已育优先",
        "汉族",
        "本地户籍",
        "无宗教信仰",
        "身体健康",
        "形象气质佳",
        "星座不限",
        "O型血优先",
        "身高170cm以上",
        "无残疾",
    ],
)
def test_extractor_excludes_discriminatory_requirements(discriminatory_requirement):
    result = RuleBasedExtractor().extract(f"熟悉Python，{discriminatory_requirement}，能够独立交付。")

    assert discriminatory_requirement not in result["other_requirements"]


@pytest.mark.parametrize(
    "occupational_requirement",
    [
        "熟悉Python和Docker",
        "负责健康数据平台开发",
        "开展多民族市场用户研究",
        "能搬运20公斤物料",
        "掌握O型血检测流程",
        "具备残疾人服务经验",
    ],
)
def test_extractor_keeps_job_related_requirements(occupational_requirement):
    result = RuleBasedExtractor().extract(occupational_requirement)

    assert occupational_requirement in result["other_requirements"]


@pytest.mark.parametrize(
    "discriminatory_requirement",
    [
        "男性优先",
        "女性优先",
        "限35岁以下",
        "已婚已育优先",
        "汉族",
        "本地户籍",
        "无宗教信仰",
        "身体健康",
        "形象气质佳",
        "星座不限",
        "O型血优先",
        "身高170cm以上",
        "无残疾",
    ],
)
def test_renderer_excludes_discriminatory_input(discriminatory_requirement):
    markdown = render_jd(
        {
            "job_title": "工程师",
            "requirements": {"other_requirements": [discriminatory_requirement]},
        }
    )

    assert discriminatory_requirement not in markdown


def test_renderer_keeps_job_related_requirements():
    requirements = [
        "熟悉Python和Docker",
        "负责健康数据平台开发",
        "能搬运20公斤物料",
        "掌握O型血检测流程",
        "具备残疾人服务经验",
    ]

    markdown = render_jd(
        {
            "job_title": "工程师",
            "requirements": {"other_requirements": requirements},
        }
    )

    assert all(requirement in markdown for requirement in requirements)


def test_renderer_uses_required_headings_and_omits_empty_values():
    markdown = render_jd(
        {
            "job_title": "Java工程师",
            "requirements": {
                "education": "本科及以上",
                "experience_years": 3,
                "required_skills": ["Java", "Spring Boot"],
                "preferred_skills": [],
                "responsibilities": [],
                "other_requirements": [],
            },
        }
    )

    assert "## 岗位职责" in markdown
    assert "## 任职资格" in markdown
    assert "本科及以上" in markdown
    assert "3年以上经验" in markdown
    assert "Java、Spring Boot" in markdown
    assert "请以实际工作需要为准，欢迎符合岗位能力要求的人才投递。" in markdown
