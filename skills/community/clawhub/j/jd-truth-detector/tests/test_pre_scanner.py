from scripts.pre_scanner import scan


def test_red_flag_factory_keywords(jd_red_flag):
    result = scan(jd_red_flag)
    assert result["red_flag_keywords"]["抗压"] >= 3
    assert result["red_flag_keywords"]["狼性"] >= 1
    assert result["red_flag_keywords"]["996"] == 0


def test_clean_jd_no_red_flags(jd_clean):
    result = scan(jd_clean)
    assert result["red_flag_keywords"]["抗压"] == 0
    assert result["red_flag_keywords"]["狼性"] == 0


def test_structure_salary_detected(jd_clean):
    result = scan(jd_clean)
    assert result["structure"]["salary_mentioned"] is True


def test_structure_tech_versions(jd_clean):
    result = scan(jd_clean)
    assert result["structure"]["tech_stack_listed"] is True
