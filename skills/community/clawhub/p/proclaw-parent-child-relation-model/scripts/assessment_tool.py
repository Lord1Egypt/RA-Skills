#!/usr/bin/env python3
"""
亲子关系评估量表生成工具
生成可打印的评估量表，包含孩子状态、亲子关系、父母状态三个维度
"""

import argparse
import json
import sys
from datetime import datetime


def generate_child_assessment_form() -> str:
    """生成孩子状态评估表"""
    html = """
    <div class="assessment-form" id="child-assessment">
        <h2>孩子状态评估表</h2>
        <p class="subtitle">请根据孩子最近一个月的情况评分 (1=很差 5=很好)</p>
        
        <table class="assessment-table">
            <thead>
                <tr>
                    <th>维度</th>
                    <th>评估项目</th>
                    <th>评分(1-5)</th>
                    <th>备注</th>
                </tr>
            </thead>
            <tbody>
                <!-- 主体性 -->
                <tr class="section-header">
                    <td colspan="4"><strong>主体性指标</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">主体性</td>
                    <td>是否有主见，能表达自己想法</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>是否能独立做决定（适合年龄）</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>是否对自己的行为负责</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>是否有自信面对挑战</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 情绪 -->
                <tr class="section-header">
                    <td colspan="4"><strong>情绪指标</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">情绪</td>
                    <td>情绪是否稳定</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>是否能识别和表达情绪</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>面对挫折的恢复能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>情绪失控的频率</td>
                    <td><input type="number" min="1" max="5" class="score-input inverse"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 动力 -->
                <tr class="section-header">
                    <td colspan="4"><strong>动力指标</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">动力</td>
                    <td>学习/探索的主动性</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>对新事物的好奇心</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>完成任务的内驱力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>对未来的期待感</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 社交 -->
                <tr class="section-header">
                    <td colspan="4"><strong>社交指标</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">社交</td>
                    <td>与同龄人相处能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>表达能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>合作能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>冲突解决能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
            </tbody>
        </table>
        
        <div class="summary-section">
            <h3>总体评价</h3>
            <textarea class="summary-textarea" rows="4" placeholder="请记录对孩子整体状态的观察和评价"></textarea>
        </div>
    </div>
    """
    return html


def generate_relationship_assessment_form() -> str:
    """生成亲子关系评估表"""
    html = """
    <div class="assessment-form" id="relationship-assessment">
        <h2>亲子关系评估表</h2>
        <p class="subtitle">请根据最近一个月的情况评分 (1=从不/很差 5=总是/很好)</p>
        
        <table class="assessment-table">
            <thead>
                <tr>
                    <th>维度</th>
                    <th>评估项目</th>
                    <th>评分(1-5)</th>
                    <th>备注</th>
                </tr>
            </thead>
            <tbody>
                <!-- 沟通 -->
                <tr class="section-header">
                    <td colspan="4"><strong>沟通质量</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">沟通</td>
                    <td>孩子是否愿意分享学校/生活的事</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>对话中是否感到平等和尊重</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>孩子是否会主动寻求你的意见</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>冲突后能否有效修复</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 联结 -->
                <tr class="section-header">
                    <td colspan="4"><strong>情感联结</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">联结</td>
                    <td>孩子是否享受与你在一起的时光</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>孩子是否信任你</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>孩子是否会向你寻求安慰</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>肢体接触的频率和质量</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 边界 -->
                <tr class="section-header">
                    <td colspan="4"><strong>边界状态</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">边界</td>
                    <td>亲子冲突的频率</td>
                    <td><input type="number" min="1" max="5" class="score-input inverse"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>冲突的激烈程度</td>
                    <td><input type="number" min="1" max="5" class="score-input inverse"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>孩子是否需要过度服从</td>
                    <td><input type="number" min="1" max="5" class="score-input inverse"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>双方是否都有独立空间</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
            </tbody>
        </table>
        
        <div class="summary-section">
            <h3>关系亮点</h3>
            <textarea class="summary-textarea" rows="3" placeholder="请记录亲子关系中做得好的方面"></textarea>
            
            <h3>需要改善</h3>
            <textarea class="summary-textarea" rows="3" placeholder="请记录需要改善的方面"></textarea>
        </div>
    </div>
    """
    return html


def generate_parent_assessment_form() -> str:
    """生成父母状态评估表"""
    html = """
    <div class="assessment-form" id="parent-assessment">
        <h2>父母状态自评表</h2>
        <p class="subtitle">请根据您最近一个月的情况评分 (1=从不/很差 5=总是/很好)</p>
        
        <table class="assessment-table">
            <thead>
                <tr>
                    <th>维度</th>
                    <th>评估项目</th>
                    <th>评分(1-5)</th>
                    <th>备注</th>
                </tr>
            </thead>
            <tbody>
                <!-- 情绪 -->
                <tr class="section-header">
                    <td colspan="4"><strong>自身情绪管理</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">情绪</td>
                    <td>面对孩子问题时能保持冷静</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>不在情绪激动时做决定</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>能识别并表达自己的情绪</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>有情绪时能找到健康宣泄方式</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 认知 -->
                <tr class="section-header">
                    <td colspan="4"><strong>认知模式</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">认知</td>
                    <td>相信孩子有解决问题的能力</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>能区分"我的焦虑"和"孩子的问题"</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>能看到孩子的进步而非只看到问题</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>愿意学习和改变自己的方式</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                
                <!-- 行为 -->
                <tr class="section-header">
                    <td colspan="4"><strong>教养行为</strong></td>
                </tr>
                <tr>
                    <td rowspan="4">行为</td>
                    <td>给孩子提供选择而非强制命令</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>解释规则背后的原因</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>尊重孩子的感受和意见</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
                <tr>
                    <td>允许孩子犯错并从中学习</td>
                    <td><input type="number" min="1" max="5" class="score-input"></td>
                    <td><input type="text" class="note-input"></td>
                </tr>
            </tbody>
        </table>
        
        <div class="summary-section">
            <h3>自我反思</h3>
            <textarea class="summary-textarea" rows="4" placeholder="请反思自己在亲子关系中的角色和表现"></textarea>
            
            <h3>成长目标</h3>
            <textarea class="summary-textarea" rows="3" placeholder="请写下你想要改善的具体方面"></textarea>
        </div>
    </div>
    """
    return html


def generate_complete_html() -> str:
    """生成完整的HTML评估工具"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>亲子关系评估量表</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
        }}
        
        .meta-info {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .meta-item label {{
            font-weight: 600;
        }}
        
        .meta-item input {{
            padding: 8px 12px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 6px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 14px;
        }}
        
        .meta-item input::placeholder {{
            color: rgba(255,255,255,0.7);
        }}
        
        .assessment-form {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        
        .assessment-form h2 {{
            color: #667eea;
            margin-bottom: 8px;
            font-size: 1.5em;
        }}
        
        .subtitle {{
            color: #666;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
        
        .assessment-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        
        .assessment-table th,
        .assessment-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        .assessment-table th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
            font-size: 0.9em;
        }}
        
        .assessment-table .section-header td {{
            background: #f0f0f5;
            color: #667eea;
            font-weight: 600;
            font-size: 0.95em;
        }}
        
        .score-input {{
            width: 60px;
            padding: 8px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            color: #667eea;
        }}
        
        .score-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .score-input.inverse {{
            color: #e74c3c;
        }}
        
        .note-input {{
            width: 150px;
            padding: 8px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
        }}
        
        .note-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .summary-section {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }}
        
        .summary-section h3 {{
            color: #555;
            margin: 15px 0 10px;
            font-size: 1.1em;
        }}
        
        .summary-textarea {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
        }}
        
        .summary-textarea:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .print-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .print-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .print-btn {{
                display: none;
            }}
            
            .assessment-form {{
                box-shadow: none;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>亲子关系评估量表</h1>
            <p>全方位评估孩子状态、亲子关系、父母状态的标准化工具</p>
            <div class="meta-info">
                <div class="meta-item">
                    <label>孩子姓名:</label>
                    <input type="text" placeholder="请输入">
                </div>
                <div class="meta-item">
                    <label>年龄:</label>
                    <input type="text" placeholder="如 8岁">
                </div>
                <div class="meta-item">
                    <label>评估日期:</label>
                    <input type="text" value="{datetime.now().strftime('%Y-%m-%d')}">
                </div>
                <div class="meta-item">
                    <label>评估人:</label>
                    <input type="text" placeholder="请输入">
                </div>
            </div>
        </div>
        
        {generate_child_assessment_form()}
        {generate_relationship_assessment_form()}
        {generate_parent_assessment_form()}
        
    </div>
    
    <button class="print-btn" onclick="window.print()">打印评估表</button>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="亲子关系评估量表生成工具")
    parser.add_argument("--output", "-o", type=str, default="assessment-forms.html", help="输出HTML文件路径")
    parser.add_argument("--preview", "-p", action="store_true", help="输出JSON格式预览")
    
    args = parser.parse_args()
    
    if args.preview:
        # 输出JSON格式的评估框架
        preview = {
            "title": "亲子关系评估量表",
            "version": "1.0",
            "assessment_forms": [
                {
                    "name": "孩子状态评估表",
                    "dimensions": ["主体性", "情绪", "动力", "社交"],
                    "items_count": 16
                },
                {
                    "name": "亲子关系评估表",
                    "dimensions": ["沟通", "联结", "边界"],
                    "items_count": 12
                },
                {
                    "name": "父母状态自评表",
                    "dimensions": ["情绪", "认知", "行为"],
                    "items_count": 12
                }
            ],
            "scoring_guide": {
                "1": "很差/从不",
                "2": "较差/偶尔",
                "3": "一般/有时",
                "4": "较好/经常",
                "5": "很好/总是"
            }
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
    else:
        html_content = generate_complete_html()
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"评估量表已生成: {args.output}")
        print(f"文件大小: {len(html_content)} 字节")


if __name__ == "__main__":
    main()
