#!/usr/bin/env python3
"""
ontology-clawra 典型场景库
内置常见场景的默认值，减少用户回答压力
"""

TYPICAL_SCENARIOS = {
    # ========== 燃气工程场景 ==========
    "gas_regulator": {
        "name": "调压箱选型",
        "category": "燃气工程",
        "scenarios": {
            "south_building": {
                "name": "南方多层住宅",
                "description": "无集中供暖，每户配置双眼灶+热水器",
                "assumptions": {
                    "region": "南方",
                    "has_heating": False,
                    "gas_devices": ["双眼灶", "热水器"],
                    "building_type": "多层(7层以下)",
                    "pressure": "中压0.1-0.4MPa"
                },
                "calculation": {
                    "single_load": "1.6-2.3 m³/h",
                    "simultaneity_factor": 0.35,
                    "total_formula": "Q = n × q × K",
                    "example_result": "100户 → 60-70 m³/h → RTZ-50/25"
                }
            },
            "north_building_no_heating": {
                "name": "北方多层住宅(无供暖)",
                "description": "无集中供暖，每户配置双眼灶+热水器",
                "assumptions": {
                    "region": "北方",
                    "has_heating": False,
                    "gas_devices": ["双眼灶", "热水器"],
                    "building_type": "多层(7层以下)",
                    "pressure": "中压0.1-0.4MPa"
                },
                "calculation": {
                    "single_load": "1.6-2.3 m³/h",
                    "simultaneity_factor": 0.35,
                    "total_formula": "Q = n × q × K",
                    "example_result": "100户 → 60-70 m³/h → RTZ-50/25"
                }
            },
            "north_building_heating": {
                "name": "北方高层住宅(自采暖)",
                "description": "有壁挂炉供暖，每户配置双眼灶+壁挂炉",
                "assumptions": {
                    "region": "北方",
                    "has_heating": True,
                    "heating_type": "壁挂炉自采暖",
                    "gas_devices": ["双眼灶", "壁挂炉"],
                    "building_type": "高层(18层以上)",
                    "pressure": "中压0.1-0.4MPa"
                },
                "calculation": {
                    "single_load": "3.0-4.0 m³/h",
                    "simultaneity_factor": 0.25,
                    "total_formula": "Q = n × q × K",
                    "example_result": "100户 → 100-120 m³/h → RTZ-100/25"
                }
            },
            "villa": {
                "name": "别墅区",
                "description": "每户配置齐全，用气量大",
                "assumptions": {
                    "region": "任意",
                    "has_heating": True,
                    "heating_type": "壁挂炉/集中供暖",
                    "gas_devices": ["双眼灶", "热水器", "壁挂炉", "地暖"],
                    "building_type": "别墅",
                    "pressure": "中压0.1-0.4MPa"
                },
                "calculation": {
                    "single_load": "4.0-6.0 m³/h",
                    "simultaneity_factor": 0.2,
                    "total_formula": "Q = n × q × K",
                    "example_result": "30户 → 30-40 m³/h → RTZ-50/25"
                }
            }
        }
    },
    
    # ========== 商业场景 ==========
    "restaurant": {
        "name": "商业餐厅",
        "category": "商业用气",
        "scenarios": {
            "small_restaurant": {
                "name": "小型餐厅",
                "description": "10桌以下，常规炒菜",
                "assumptions": {
                    "seats": "10桌以下",
                    "cooking_equipment": ["双眼灶", "煲仔炉"],
                    "operating_hours": "10-14, 17-21"
                },
                "calculation": {
                    "single_load": "5-10 m³/h",
                    "simultaneity_factor": 0.5,
                    "example_result": "10桌 → 25-50 m³/h"
                }
            },
            "large_restaurant": {
                "name": "大型餐厅",
                "description": "20桌以上，多种烹饪设备",
                "assumptions": {
                    "seats": "20桌以上",
                    "cooking_equipment": ["双眼灶", "煲仔炉", "蒸柜", "炸炉"],
                    "operating_hours": "10-14, 17-21"
                },
                "calculation": {
                    "single_load": "15-25 m³/h",
                    "simultaneity_factor": 0.4,
                    "example_result": "30桌 → 180-300 m³/h"
                }
            }
        }
    },
    
    # ========== 工业场景 ==========
    "industrial": {
        "name": "工业用气",
        "category": "工业",
        "scenarios": {
            "factory": {
                "name": "工厂食堂",
                "description": "员工食堂，用气时间集中",
                "assumptions": {
                    "employees": "500人以下",
                    "meals_per_day": "两餐",
                    "cooking_time": "1.5小时集中"
                },
                "calculation": {
                    "single_load": "0.1 m³/h/人",
                    "simultaneity_factor": 0.6,
                    "example_result": "500人 → 30 m³/h"
                }
            }
        }
    }
}


def get_scenario(category, scenario_key=None):
    """获取场景"""
    if category not in TYPICAL_SCENARIOS:
        return None
    
    scenario_data = TYPICAL_SCENARIOS[category]
    
    if scenario_key:
        return scenario_data["scenarios"].get(scenario_key)
    
    return scenario_data


def list_scenarios(category=None):
    """列出所有场景"""
    if category:
        return TYPICAL_SCENARIOS.get(category, {})
    return TYPICAL_SCENARIOS


def match_scenario(category, user_answers):
    """
    根据用户回答匹配典型场景
    user_answers: dict，如 {"region": "南方", "has_heating": False}
    """
    if category not in TYPICAL_SCENARIOS:
        return None
    
    scenarios = TYPICAL_SCENARIOS[category]["scenarios"]
    
    # 精确匹配
    for key, scenario in scenarios.items():
        assumptions = scenario.get("assumptions", {})
        match = True
        for q, a in user_answers.items():
            if assumptions.get(q) != a:
                match = False
                break
        if match:
            return {
                "key": key,
                "name": scenario["name"],
                "description": scenario["description"],
                "assumptions": assumptions,
                "calculation": scenario["calculation"]
            }
    
    # 部分匹配 - 返回最接近的
    return None


def generate_confirmation_questions(category, user_answers):
    """
    生成确认问题
    返回: [(问题, 选项, 默认值)]
    """
    questions = {
        "gas_regulator": [
            ("所在地区", ["南方", "北方"], "南方"),
            ("是否有集中供暖", ["是", "否"], "否"),
            ("建筑类型", ["多层(7层以下)", "高层(7-18层)", "超高层(18层以上)"], "多层(7层以下)"),
            ("用气设备", ["双眼灶+热水器", "双眼灶+壁挂炉", "全配置"], "双眼灶+热水器")
        ],
        "restaurant": [
            ("餐厅规模", ["小型(10桌以下)", "中型(10-20桌)", "大型(20桌以上)"], "小型(10桌以下)"),
            ("烹饪设备", ["常规炒菜", "多功能"], "常规炒菜")
        ]
    }
    
    return questions.get(category, [])


def main():
    """测试"""
    print("=" * 50)
    print("典型场景库测试")
    print("=" * 50)
    
    # 列出所有场景
    print("\n📁 可用场景类别:")
    for cat, data in TYPICAL_SCENARIOS.items():
        print(f"  • {cat}: {data['name']}")
    
    # 测试匹配
    print("\n🔍 场景匹配测试:")
    test_answers = {"region": "南方", "has_heating": False}
    result = match_scenario("gas_regulator", test_answers)
    if result:
        print(f"  匹配结果: {result['name']}")
        print(f"  描述: {result['description']}")
        print(f"  计算结果: {result['calculation']['example_result']}")
    
    # 生成确认问题
    print("\n❓ 典型确认问题:")
    questions = generate_confirmation_questions("gas_regulator", {})
    for q, options, default in questions:
        print(f"  • {q}: {options} (默认: {default})")


if __name__ == "__main__":
    main()
