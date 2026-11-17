"""
knowledge-collector 测试脚本
测试自动分类、信息提取、模板填充、domain-kit集成、批量导入
"""
import sys
import json
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collector import classify, extract_metadata, fill_template, collect
from batch_import import batch_import


def test_classify():
    """测试自动分类"""
    print("=" * 60)
    print("测试1: 自动分类")
    print("=" * 60)
    
    test_cases = [
        {
            "text": "AM600 PLC 程序模块化编程规范，使用 InoProShop 开发",
            "expected_direction": "非标自动化",
            "expected_type": "软件"
        },
        {
            "text": "WCS 系统 AGV 调度算法，路径规划优化",
            "expected_direction": "物流自动化",
            "expected_type": "算法"
        },
        {
            "text": "视觉检测算法，YOLO 模型训练，缺陷检测准确率 98%",
            "expected_direction": "工业视觉",
            "expected_type": "算法"
        },
        {
            "text": "空调外机装配线方案，节拍 30 秒/件，10 个工站",
            "expected_direction": "非标自动化",
            "expected_type": "方案"
        }
    ]
    
    passed = 0
    for i, tc in enumerate(test_cases, 1):
        result = classify(tc["text"])
        dir_ok = result["direction"] == tc["expected_direction"]
        type_ok = result["type"] == tc["expected_type"]
        status = "✅" if (dir_ok and type_ok) else "❌"
        print(f"{status} 用例{i}: 方向={result['direction']}(期望{tc['expected_direction']}) "
              f"类型={result['type']}(期望{tc['expected_type']}) 置信度={result['confidence']:.2f}")
        if dir_ok and type_ok:
            passed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过\n")
    return passed == len(test_cases)


def test_extract_metadata():
    """测试信息提取"""
    print("=" * 60)
    print("测试2: 信息提取")
    print("=" * 60)
    
    text = """
    项目 IV2615 使用 AM600 PLC，通过 EtherCAT 通信控制 IS620N 伺服。
    上位机使用 Python + Qt 开发，通过 Modbus TCP 读取传感器数据。
    """
    
    result = extract_metadata(text)
    
    print(f"设备型号: {result['equipment_models']}")
    print(f"协议: {result['protocols']}")
    print(f"项目编号: {result['project_ids']}")
    print(f"标签: {result['tags']}")
    
    # 验证
    assert "AM600" in result["equipment_models"], "应提取到 AM600"
    assert "IS620N" in result["equipment_models"], "应提取到 IS620N"
    assert "EtherCAT" in result["protocols"], "应提取到 EtherCAT"
    assert "Modbus TCP" in result["protocols"], "应提取到 Modbus TCP"
    assert "IV2615" in result["project_ids"], "应提取到 IV2615"
    
    print("\n✅ 信息提取测试通过\n")
    return True


def test_fill_template():
    """测试模板填充"""
    print("=" * 60)
    print("测试3: 模板填充")
    print("=" * 60)
    
    classification = {"direction": "非标自动化", "type": "经验", "level": "L4", "confidence": 0.85}
    metadata = {"equipment_models": ["AM600"], "protocols": ["EtherCAT"], "project_ids": ["IV2615"], "tags": ["AM600", "EtherCAT", "IV2615"]}
    raw_text = "AM600 EtherCAT 从站掉线排查经验..."
    
    result = fill_template(classification, metadata, raw_text, title="测试标题")
    
    assert "# 测试标题" in result, "应包含标题"
    assert "AM600" in result, "应包含设备型号"
    assert "原始内容" in result, "应包含原始内容章节"
    
    print(f"生成的 Markdown 长度: {len(result)} 字符")
    print(f"前 200 字符:\n{result[:200]}...")
    print("\n✅ 模板填充测试通过\n")
    return True


def test_collect_integration():
    """测试完整收集流程（domain-kit 集成）"""
    print("=" * 60)
    print("测试4: domain-kit 集成")
    print("=" * 60)
    
    text = """
    WCS 系统任务调度算法优化
    
    使用遗传算法优化 AGV 路径规划，任务完成时间减少 15%。
    输入：任务列表、AGV 位置、地图信息
    输出：最优路径、预计完成时间
    """
    
    result = collect(text, source_type="manual", title="WCS 任务调度算法优化")
    
    print(f"Entity ID: {result['entity_id']}")
    print(f"分类: {result['classification']}")
    print(f"元数据: {result['metadata']}")
    print(f"研究室: {result['research_room']}")
    
    assert result["entity_id"], "应生成 entity_id"
    assert result["classification"]["direction"] == "物流自动化", "应分类为物流自动化"
    assert result["research_room"] == "物流自动化研究室", "应推送给物流自动化研究室"
    
    print("\n✅ domain-kit 集成测试通过\n")
    return True


def test_batch_import():
    """测试批量导入"""
    print("=" * 60)
    print("测试5: 批量导入")
    print("=" * 60)
    
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()
    try:
        # 创建测试文件（内容需要 >50 字符）
        test_files = [
            ("test1.md", "# PLC 编程规范\n\nAM600 PLC 程序模块化编程，使用 ST 语言开发功能块，每个工站一个 FB，包含初始化、自动运行、手动运行、故障处理四个子程序。"),
            ("test2.txt", "视觉检测算法优化\n\n使用 YOLO 模型进行缺陷检测，通过数据增强和迁移学习，准确率从 92% 提升到 98%，召回率从 88% 提升到 95%。"),
            ("test3.py", "# WCS 调度算法\ndef optimize_path():\n    # 路径规划优化，使用遗传算法\n    # 任务完成时间减少 15%\n    pass"),
            ("test4.unsupported", "不支持的文件类型，这个文件应该被跳过，因为扩展名不在支持列表中。")
        ]
        
        for filename, content in test_files:
            with open(Path(temp_dir) / filename, "w", encoding="utf-8") as f:
                f.write(content)
        
        # 执行批量导入
        report = batch_import(temp_dir)
        
        print(f"\n导入报告:")
        print(f"  总文件数: {report['total_files']}")
        print(f"  成功: {report['success']}")
        print(f"  失败: {report['failed']}")
        print(f"  跳过: {report['skipped']}")
        
        assert report["total_files"] == 4, "应有 4 个文件"
        assert report["success"] == 3, "应成功导入 3 个"
        assert report["skipped"] == 1, "应跳过 1 个"
        
        print("\n✅ 批量导入测试通过\n")
        return True
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("knowledge-collector 测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        test_classify,
        test_extract_metadata,
        test_fill_template,
        test_collect_integration,
        test_batch_import
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 测试失败: {e}\n")
            results.append(False)
    
    print("=" * 60)
    print(f"总计: {sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
