#!/usr/bin/env python3
"""
Medical Record Structurer - Demo Script
Zero-configuration demo to try the skill immediately!
"""

import sys
import json
import argparse

# Add scripts directory to path
sys.path.insert(0, 'scripts')

from process_record import process_medical_record

# Sample medical records for demo
SAMPLE_RECORDS = [
    {
        "name": "急性胸痛病例",
        "text": "患者张三，男，58岁，主诉胸痛2小时，伴有呼吸困难。既往有高血压病史10年。体格检查：血压160/95mmHg，心率110次/分。初步诊断：急性冠脉综合征。治疗方案：立即给予阿司匹林300mg口服，硝酸甘油0.5mg舌下含服，联系心内科会诊。"
    },
    {
        "name": "发热咳嗽病例", 
        "text": "患者李四，女，32岁，主诉发热3天，最高体温39.2℃，伴有咳嗽、咳痰。无胸痛、呼吸困难。体格检查：咽部充血，双肺呼吸音粗，可闻及散在湿啰音。诊断：急性支气管炎。治疗：给予阿莫西林0.5g tid，复方甘草片2片 tid，建议休息、多饮水。"
    },
    {
        "name": "腹痛腹泻病例",
        "text": "患者王五，男，45岁，主诉腹痛、腹泻2天，每日大便5-6次，呈水样便，伴有恶心呕吐。无发热。体格检查：腹软，脐周压痛，肠鸣音亢进。诊断：急性胃肠炎。治疗：口服补液盐，蒙脱石散3g tid，诺氟沙星0.4g bid，建议清淡饮食。"
    }
]

def print_banner():
    """Print demo banner."""
    print("=" * 60)
    print("🏥 Medical Record Structurer - Demo")
    print("=" * 60)
    print("\n✨ Try the skill instantly - no configuration needed!")
    print("🎁 Each user gets 10 free calls\n")

def print_result(result, sample_name):
    """Pretty print the result."""
    print("\n" + "-" * 60)
    print(f"📋 处理结果: {sample_name}")
    print("-" * 60)
    
    if result.get('success'):
        # Show trial info
        if result.get('trial_mode'):
            print(f"\n🎁 免费试用模式 - 剩余次数: {result['trial_remaining']}")
        
        record = result.get('structured_record', {})
        
        # Patient info
        demo = record.get('patient_demographics', {})
        print(f"\n👤 患者信息:")
        print(f"   姓名: {demo.get('name', 'N/A')}")
        print(f"   性别: {demo.get('gender', 'N/A')}")
        print(f"   年龄: {demo.get('age', 'N/A')}")
        
        # Clinical info
        clinical = record.get('clinical_information', {})
        print(f"\n🏥 临床信息:")
        print(f"   主诉: {clinical.get('chief_complaint', 'N/A')}")
        if clinical.get('history_of_present_illness'):
            print(f"   现病史: {clinical.get('history_of_present_illness')}")
        if clinical.get('physical_examination'):
            print(f"   体格检查: {clinical.get('physical_examination')}")
        
        # Assessment
        assessment = record.get('assessment_and_plan', {})
        print(f"\n📊 评估与计划:")
        print(f"   诊断: {assessment.get('diagnosis', 'N/A')}")
        print(f"   治疗方案: {assessment.get('treatment_plan', 'N/A')}")
        if assessment.get('medications'):
            print(f"   药物: {assessment.get('medications')}")
        if assessment.get('follow_up_instructions'):
            print(f"   随访: {assessment.get('follow_up_instructions')}")
        
        # Full JSON
        print(f"\n📄 完整结构化输出 (JSON):")
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(f"\n❌ 错误: {result.get('error', 'Unknown error')}")

def main():
    parser = argparse.ArgumentParser(description='Medical Record Structurer Demo')
    parser.add_argument('--input', '-i', help='Custom medical record text to process')
    parser.add_argument('--output', '-o', help='Save output to file')
    parser.add_argument('--sample', '-s', type=int, choices=[1, 2, 3], help='Run specific sample (1-3)')
    args = parser.parse_args()
    
    print_banner()
    
    if args.input:
        # Process custom input
        print(f"📝 处理自定义输入...\n")
        result = process_medical_record(
            input_text=args.input,
            user_id="demo_user_001"
        )
        print_result(result, "自定义输入")
    elif args.sample:
        # Process specific sample
        sample = SAMPLE_RECORDS[args.sample - 1]
        print(f"📝 处理示例 {args.sample}: {sample['name']}\n")
        result = process_medical_record(
            input_text=sample['text'],
            user_id="demo_user_001"
        )
        print_result(result, sample['name'])
    else:
        # Run all samples
        print("📝 处理 3 个示例病历...\n")
        for i, sample in enumerate(SAMPLE_RECORDS, 1):
            result = process_medical_record(
                input_text=sample['text'],
                user_id="demo_user_001"
            )
            print_result(result, sample['name'])
            if i < len(SAMPLE_RECORDS):
                input("\n⏎ 按 Enter 继续下一个示例...")
    
    # Save output if requested
    if args.output and 'result' in locals():
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {args.output}")
    
    print("\n" + "=" * 60)
    print("✅ Demo 完成!")
    print("=" * 60)
    print("\n📚 下一步:")
    print("   - 查看完整文档: cat SKILL.md")
    print("   - 阅读使用示例: cat EXAMPLES.md")
    print("   - 开始免费试用: 使用你自己的病历文本")
    print("\n💡 提示: 每个用户有 10 次免费调用")
    print("=" * 60)

if __name__ == '__main__':
    main()
