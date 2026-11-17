"""Fallback requirement extraction without model or network dependencies."""

import re


SKILLS = ("Java", "Python", "Go", "Spring Boot", "MySQL", "Redis", "Docker", "Kubernetes")
_EXACT_PROTECTED_TRAITS = {
    "汉族",
    "满族",
    "回族",
    "藏族",
    "维吾尔族",
    "蒙古族",
    "壮族",
}
_PROTECTED_TRAIT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"男性|女性|性别",
        r"年龄|限\s*\d{1,2}\s*岁|\d{2}\s*岁(?:以下|以内|以上|及以下|及以上)",
        r"婚育|已婚|已育",
        r"(?:民族|(?:汉|满|回|藏|维吾尔|蒙古|壮)族).{0,6}(?:优先|不限|要求|限制)",
        r"本地户籍|(?:户籍|籍贯).{0,4}(?:优先|要求|限制)",
        r"(?:无|特定|不得有).{0,4}宗教|宗教.{0,4}(?:优先|限制|要求)",
        r"身体健康",
        r"外貌|形象气质",
        r"星座.{0,6}(?:不限|优先|要求|限制)",
        r"(?:(?:A|B|AB|O)型血|血型).{0,6}(?:不限|优先|要求|限制)",
        r"身高\s*\d+(?:\.\d+)?\s*(?:cm|厘米|米)?\s*(?:以上|以下|及以上|及以下|以内)?",
        r"(?:无|不得有|拒绝|排除|不接受).{0,4}残疾|残疾.{0,6}(?:优先|限制)",
    )
)
_LIST_REQUIREMENT_KEYS = (
    "required_skills",
    "preferred_skills",
    "responsibilities",
    "other_requirements",
)


def is_discriminatory_requirement(value: object) -> bool:
    """Return whether a free-text requirement contains prohibited criteria."""
    if not isinstance(value, str):
        return False
    normalized = value.strip()
    return normalized in _EXACT_PROTECTED_TRAITS or any(
        pattern.search(normalized) for pattern in _PROTECTED_TRAIT_PATTERNS
    )


def sanitize_requirements(requirements: dict) -> dict:
    """Return a copy with protected or unrelated trait criteria removed."""
    sanitized = dict(requirements)
    if is_discriminatory_requirement(sanitized.get("education")):
        sanitized["education"] = None

    for key in _LIST_REQUIREMENT_KEYS:
        values = sanitized.get(key)
        if isinstance(values, list):
            sanitized[key] = [
                value
                for value in values
                if not is_discriminatory_requirement(value)
            ]
    return sanitized


class RuleBasedExtractor:
    """Extract a stable requirement schema from a Chinese job description."""

    def extract(self, description: str) -> dict:
        text = description.replace("，", ",").replace("、", ",")
        years = re.search(r"(\d+)\s*年(?:以上)?(?:[^,。]{0,8})经验", text)

        requirements = {
            "education": "本科及以上" if re.search(r"本科(?:以上|及以上)", text) else None,
            "experience_years": int(years.group(1)) if years else None,
            "required_skills": [skill for skill in SKILLS if skill.lower() in text.lower()],
            "preferred_skills": [],
            "responsibilities": [],
            "other_requirements": [
                item.strip()
                for item in text.split(",")
                if item.strip()
            ],
        }
        return sanitize_requirements(requirements)
