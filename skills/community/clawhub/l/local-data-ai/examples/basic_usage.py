#!/usr/bin/env python3
"""
LocalDataAI 使用示例
"""

import os
import sys

# 添加 scripts 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from local_ai_engine import LocalAIEngine, Document
from file_parser import FileParser, parse_file
from vector_store import VectorStore
from sandbox import SecureSandbox, temporary_sandbox
from large_file_handler import LargeFileHandler
from compliance_logger import ComplianceLogger


def example_1_basic_qa():
    """示例 1: 基础文件问答"""
    print("=" * 60)
    print("示例 1: 基础文件问答")
    print("=" * 60)
    
    # 初始化引擎
    engine = LocalAIEngine()
    parser = FileParser()
    
    # 解析文件
    doc = parser.parse("./示例文档.pdf")
    print(f"解析完成: {doc.title}, 页数: {doc.page_count}")
    
    # AI 问答
    questions = [
        "这份文档的核心内容是什么？",
        "文档中提到了哪些关键数据？",
        "请总结一下主要结论"
    ]
    
    for q in questions:
        print(f"\n问: {q}")
        answer = engine.ask(doc, q)
        print(f"答: {answer}")
    
    print("\n")


def example_2_summarize():
    """示例 2: 生成文档摘要"""
    print("=" * 60)
    print("示例 2: 生成文档摘要")
    print("=" * 60)
    
    engine = LocalAIEngine()
    parser = FileParser()
    
    doc = parser.parse("./合同.pdf")
    
    # 三种摘要模式
    for mode in ["brief", "core", "detailed"]:
        summary = engine.summarize(doc, mode=mode)
        print(f"\n【{mode} 模式摘要】")
        print(summary)
    
    print("\n")


def example_3_extract_entities():
    """示例 3: 提取关键信息"""
    print("=" * 60)
    print("示例 3: 提取关键信息")
    print("=" * 60)
    
    engine = LocalAIEngine()
    parser = FileParser()
    
    doc = parser.parse("./合同.pdf")
    
    # 提取多种类型信息
    entity_types = ["人名", "金额", "日期", "公司名称"]
    entities = engine.extract(doc, types=entity_types)
    
    print("\n提取结果:")
    for entity_type, values in entities.items():
        print(f"  {entity_type}: {values}")
    
    print("\n")


def example_4_multi_file_search():
    """示例 4: 多文件检索"""
    print("=" * 60)
    print("示例 4: 多文件检索")
    print("=" * 60)
    
    engine = LocalAIEngine()
    parser = FileParser()
    
    # 加载多个文档
    docs = [
        parser.parse("./文档1.pdf"),
        parser.parse("./文档2.pdf"),
        parser.parse("./文档3.docx")
    ]
    
    # 跨文档检索
    keywords = "项目预算"
    results = engine.search(docs, keywords, match_mode="fuzzy")
    
    print(f"\n检索关键词: {keywords}")
    print(f"找到 {len(results)} 个匹配结果:")
    
    for i, result in enumerate(results[:5], 1):
        print(f"\n  [{i}] 来源: {result.doc_id}")
        print(f"      相关度: {result.score:.2f}")
        print(f"      内容: {result.content[:100]}...")
    
    print("\n")


def example_5_cross_document_qa():
    """示例 5: 跨文档问答"""
    print("=" * 60)
    print("示例 5: 跨文档问答")
    print("=" * 60)
    
    engine = LocalAIEngine()
    parser = FileParser()
    
    # 加载多个相关文档
    docs = [
        parser.parse("./合同_v1.pdf"),
        parser.parse("./合同_v2.pdf"),
        parser.parse("./补充协议.pdf")
    ]
    
    # 跨文件问答
    question = "对比三个版本的合同，有哪些主要变更？"
    answer = engine.ask_multi(docs, question)
    
    print(f"\n问: {question}")
    print(f"答: {answer}")
    print("\n")


def example_6_secure_sandbox():
    """示例 6: 安全沙箱处理"""
    print("=" * 60)
    print("示例 6: 安全沙箱处理")
    print("=" * 60)
    
    def process_file_in_sandbox(file_path):
        """沙箱内的处理函数"""
        parser = FileParser()
        return parser.parse(file_path)
    
    # 使用沙箱上下文管理器
    with temporary_sandbox() as sandbox:
        result = sandbox.process_file(
            "./敏感文档.pdf",
            process_file_in_sandbox
        )
        
        print(f"\n沙箱处理完成: {result.title}")
        print(f"沙箱 ID: {sandbox.sandbox_id}")
        
        # 获取统计信息
        stats = sandbox.get_statistics()
        print(f"处理文件数: {stats['processed_files_count']}")
    
    # 退出沙箱后自动清理
    print("沙箱已自动清理")
    print("\n")


def example_7_large_file_processing():
    """示例 7: 大文件处理"""
    print("=" * 60)
    print("示例 7: 大文件处理")
    print("=" * 60)
    
    def progress_callback(progress):
        """进度回调函数"""
        print(f"\r进度: {progress['percentage']:.1f}% "
              f"({progress['completed_chunks']}/{progress['total_chunks']})", 
              end="", flush=True)
    
    # 创建大文件处理器
    handler = LargeFileHandler(
        chunk_size_mb=50,
        max_workers=4,
        progress_callback=progress_callback
    )
    
    def parse_chunk(file_path):
        """解析分片"""
        parser = FileParser()
        return parser.parse(file_path)
    
    # 处理大文件
    print("开始处理大文件...")
    result = handler.process_large_file(
        "./大文件.pdf",
        parse_chunk
    )
    
    print("\n")
    if result['success']:
        print(f"处理完成! 共 {result['chunks']} 个分片")
    else:
        print(f"处理失败: {result['error']}")
    
    print("\n")


def example_8_audit_logging():
    """示例 8: 审计日志"""
    print("=" * 60)
    print("示例 8: 审计日志")
    print("=" * 60)
    
    logger = ComplianceLogger(retention_days=90)
    
    # 记录操作
    log_id = logger.log_operation(
        user_id="user_001",
        action="parse",
        file_name="./合同.pdf",
        file_size=1024000,
        result="success",
        metadata={"pages": 10, "engine": "pymupdf"},
        session_id="session_abc123"
    )
    
    print(f"\n日志已记录: {log_id}")
    
    # 读取日志
    logs = logger.read_logs(
        start_date="2026-03-01",
        end_date="2026-03-31",
        user_id="user_001"
    )
    
    print(f"查询到 {len(logs)} 条日志记录")
    
    # 导出审计报告
    report_path = logger.export_audit_report(
        start_date="2026-03-01",
        end_date="2026-03-31",
        format="json",
        include_watermark=True
    )
    
    print(f"审计报告已导出: {report_path}")
    print("\n")


def example_9_complete_workflow():
    """示例 9: 完整工作流"""
    print("=" * 60)
    print("示例 9: 完整工作流 - 合同审查")
    print("=" * 60)
    
    # 初始化组件
    engine = LocalAIEngine()
    parser = FileParser()
    vector_store = VectorStore()
    logger = ComplianceLogger()
    
    # 1. 解析合同
    print("\n[1/5] 解析合同文件...")
    contract = parser.parse("./采购合同.pdf")
    print(f"      解析完成: {contract.title}, {contract.page_count} 页")
    
    # 2. 存储到向量库
    print("\n[2/5] 构建向量索引...")
    doc_id = vector_store.add_document(contract)
    print(f"      文档 ID: {doc_id}")
    
    # 3. AI 分析
    print("\n[3/5] AI 智能分析...")
    analysis = {
        "合同类型": engine.ask(contract, "这是什么类型的合同？"),
        "关键条款": engine.ask(contract, "列出所有关键条款"),
        "风险点": engine.ask(contract, "这份合同有哪些潜在风险？"),
        "摘要": engine.summarize(contract, mode="core")
    }
    
    for key, value in analysis.items():
        print(f"      {key}: {value[:50]}...")
    
    # 4. 记录审计日志
    print("\n[4/5] 记录审计日志...")
    log_id = logger.log_operation(
        user_id="legal_team",
        action="contract_review",
        file_name="./采购合同.pdf",
        file_size=os.path.getsize("./采购合同.pdf") if os.path.exists("./采购合同.pdf") else 0,
        result="success",
        metadata={"analysis_items": list(analysis.keys())}
    )
    print(f"      日志 ID: {log_id}")
    
    # 5. 导出报告
    print("\n[5/5] 生成审查报告...")
    report = {
        "contract_info": {
            "title": contract.title,
            "pages": contract.page_count,
            "doc_id": doc_id
        },
        "analysis": analysis,
        "audit_log_id": log_id,
        "generated_at": "2026-03-16T10:00:00"
    }
    
    print("      审查报告生成完成")
    print("\n" + "=" * 60)
    print("工作流完成!")
    print("=" * 60)


def main():
    """主函数"""
    print("\n")
    print("*" * 60)
    print(" LocalDataAI - 本地私有数据 AI 处理")
    print(" 使用示例集")
    print("*" * 60)
    print("\n")
    
    # 运行示例（注释掉的示例需要实际文件）
    
    # example_1_basic_qa()
    # example_2_summarize()
    # example_3_extract_entities()
    # example_4_multi_file_search()
    # example_5_cross_document_qa()
    # example_6_secure_sandbox()
    # example_7_large_file_processing()
    example_8_audit_logging()
    example_9_complete_workflow()
    
    print("\n所有示例运行完成!")


if __name__ == "__main__":
    main()
