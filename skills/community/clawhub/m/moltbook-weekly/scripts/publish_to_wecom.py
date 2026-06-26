#!/usr/bin/env python3
"""
企业微信文档发布器
实际调用 wecom_mcp 创建和编辑文档
"""

import subprocess
import json
import time
from datetime import datetime

class WeComPublisher:
    """企业微信文档发布器"""
    
    def __init__(self):
        self.docid = None
    
    def create_doc(self, title="MoltbookAgent 周报"):
        """创建企业微信文档"""
        cmd = f'''python3 -c "
import subprocess
result = subprocess.run([
    'openclaw', 'mcp', 'call', 'wecom_mcp',
    '{{\"command\": \"call\", \"tool\": \"doc\", \"subtool\": \"create_doc\", \"args\": {{\"doc_type\": 3, \"doc_name\": \"{title}\"}}}}'
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
"'''
        
        print(f"📄 创建文档: {title}")
        print("💡 命令:")
        print(f"wecom_mcp call doc create_doc '{{\"doc_type\": 3, \"doc_name\": \"{title}\"}}'")
        print()
        print("⚠️ 由于 wecom_mcp 是 MCP 工具，需要在交互环境中调用")
        print("请手动执行以下步骤:")
        print()
        print("1. 创建文档:")
        print(f'   wecom_mcp call doc create_doc \'{{"doc_type": 3, "doc_name": "{title}"}}\'')
        print()
        print("2. 记录返回的 docid")
        print()
        print("3. 使用 docid 编辑内容")
        
        return None
    
    def edit_doc(self, docid, content):
        """编辑文档内容"""
        print(f"\n✏️ 编辑文档: {docid}")
        print(f"内容长度: {len(content)} 字符")
        print()
        print("💡 命令:")
        # 需要转义 content 中的特殊字符
        escaped_content = content.replace('"', '\\"').replace("\n", "\\n")
        print(f'wecom_mcp call doc edit_doc_content \'{{"docid": "{docid}", "content": "{escaped_content[:200]}...", "content_type": 1}}\'')
    
    def publish_report(self, markdown_content, title=None):
        """发布完整报告"""
        title = title or f"周报 {datetime.now().strftime('%Y-%m-%d')}"
        
        print("="*60)
        print("📤 企业微信文档发布指南")
        print("="*60)
        
        # 步骤1: 创建文档
        print("\n步骤 1: 创建文档")
        print("-"*60)
        print(f'wecom_mcp call doc create_doc \'{{"doc_type": 3, "doc_name": "{title}"}}\'')
        
        # 步骤2: 编辑内容
        print("\n步骤 2: 编辑内容 (使用步骤1返回的 docid)")
        print("-"*60)
        
        # 生成编辑命令（截断内容避免过长）
        content_preview = markdown_content[:500].replace('"', '\\"').replace("\n", "\\n")
        print(f'# 保存 markdown 到文件，然后引用')
        print(f'echo "{content_preview}..." > /tmp/report.md')
        print(f'# 然后编辑文档（需要手动处理大内容）')
        
        print("\n" + "="*60)
        print("⚠️ 注意: wecom_mcp 是 MCP 工具，无法通过脚本直接调用")
        print("请复制上方命令，在启用了 wecom 插件的 OpenClaw 环境中执行")
        print("="*60)

def main():
    """生成示例周报并输出发布命令"""
    from create_weekly_report import WeeklyReportGenerator
    
    # 生成周报内容
    generator = WeeklyReportGenerator()
    markdown = generator.generate_markdown()
    
    # 保存到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = f"/tmp/weekly_report_{timestamp}.md"
    with open(filepath, 'w') as f:
        f.write(markdown)
    
    print(f"✅ 报告已生成: {filepath}")
    
    # 输发布指南
    publisher = WeComPublisher()
    publisher.publish_report(markdown)
    
    print(f"\n💾 完整报告文件: {filepath}")
    print("📋 请复制内容到企业微信文档，或使用上述命令发布")

if __name__ == "__main__":
    main()
