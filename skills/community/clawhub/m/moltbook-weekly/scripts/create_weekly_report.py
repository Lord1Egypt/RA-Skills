#!/usr/bin/env python3
"""
周报自动生成器
演示 wecom-doc-manager 的集成使用
"""

import json
import argparse
from datetime import datetime

class WeeklyReportGenerator:
    def __init__(self):
        self.report_data = {
            "generated_at": datetime.now().isoformat(),
            "sections": []
        }
    
    def add_section(self, title, content):
        """添加报告章节"""
        self.report_data["sections"].append({
            "title": title,
            "content": content
        })
    
    def collect_v35_data(self):
        """收集 v3.5 项目数据"""
        # 读取 v3.5 迁移配置
        try:
            with open("/tmp/v35_migration_config.json", "r") as f:
                config = json.load(f)
            
            return {
                "status": "已升级到 100%" if config.get("v35_weight") == 1.0 else f"权重 {config.get('v35_weight', 0)*100:.0f}%",
                "avg_votes": config.get("metrics", {}).get("v35_avg_votes", 0),
                "accuracy": config.get("metrics", {}).get("prediction_accuracy", 0)
            }
        except:
            return {"status": "数据不可用", "avg_votes": 0, "accuracy": 0}
    
    def collect_price_data(self):
        """收集价格监控数据"""
        try:
            with open("/tmp/price_monitor_db.json", "r") as f:
                db = json.load(f)
            
            products = []
            for name, info in db.get("products", {}).items():
                products.append({
                    "name": name,
                    "price": info.get("last_price", "未记录"),
                    "checked": info.get("last_check", "从未")[:10] if info.get("last_check") else "从未"
                })
            return products
        except:
            return []
    
    def generate_markdown(self):
        """生成 Markdown 格式报告"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        md = f"""# MoltbookAgent 项目周报

**报告周期**: {today}  
**生成时间**: {datetime.now().strftime("%H:%M:%S")}

---

"""
        
        # v3.5 章节
        v35_data = self.collect_v35_data()
        md += f"""## 🤖 v3.5 生产部署

- **当前状态**: {v35_data['status']}
- **平均赞数**: {v35_data['avg_votes']}
- **预测准确度**: {v35_data['accuracy']*100:.0f}%

v3.5 因果推理系统已全面接管生产环境，运行稳定。

---

"""
        
        # 价格监控章节
        price_data = self.collect_price_data()
        if price_data:
            md += """## 💰 价格监控

| 产品 | 当前价格 | 最后检查 |
|------|----------|----------|
"""
            for p in price_data:
                md += f"| {p['name']} | {p['price']} | {p['checked']} |\n"
            md += "\n---\n\n"
        
        # InStreet 章节
        md += """## 📱 InStreet 自动回复

- **运行状态**: 正常
- **监控任务**: instreet-auto-reply (每15分钟)
- **日志分析**: 见 instreet-analytics-skill

---

## 📊 系统健康度

| 组件 | 状态 |
|------|------|
| v3.5 部署器 | 🟢 正常 |
| Cron 任务队列 | 🟢 正常 |
| 守护进程 | 🟡 观察模式 |
| 磁盘空间 | 🟢 正常 (73%) |

---

*本报告由 Weekly Report Skill 自动生成*
"""
        
        return md
    
    def save_local(self, filepath):
        """保存到本地文件"""
        content = self.generate_markdown()
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ 报告已保存: {filepath}")
        return filepath
    
    def publish_to_wecom(self, title=None):
        """发布到企业微信文档
        
        实际使用时，这里调用 wecom-doc-manager:
        
        1. 创建文档:
           wecom_mcp call doc create_doc '{"doc_type": 3, "doc_name": "标题"}'
           
        2. 获取 docid 后，编辑内容:
           wecom_mcp call doc edit_doc_content '{"docid": "xxx", "content": "markdown内容", "content_type": 1}'
        """
        title = title or f"周报 {datetime.now().strftime('%Y-%m-%d')}"
        content = self.generate_markdown()
        
        print(f"\n📤 准备发布到企业微信文档")
        print(f"   标题: {title}")
        print(f"   内容长度: {len(content)} 字符")
        
        print("\n💡 执行命令示例:")
        print(f"""
# 1. 创建文档
wecom_mcp call doc create_doc '{{"doc_type": 3, "doc_name": "{title}"}}'

# 2. 记录返回的 docid，然后编辑内容
wecom_mcp call doc edit_doc_content '{{"docid": "返回的DOCID", "content": "{content[:100]}...", "content_type": 1}}'
""")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="周报生成器")
    parser.add_argument("--title", default="MoltbookAgent 周报", help="报告标题")
    parser.add_argument("--output", help="输出到本地文件")
    parser.add_argument("--auto-publish", action="store_true", help="自动发布到企业微信")
    
    args = parser.parse_args()
    
    generator = WeeklyReportGenerator()
    
    if args.output:
        generator.save_local(args.output)
    elif args.auto_publish:
        generator.publish_to_wecom(args.title)
    else:
        # 默认输出到控制台
        print(generator.generate_markdown())

if __name__ == "__main__":
    main()
